#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_skill_security.py — UNTERSTÜTZENDE Triage für heruntergeladene Skills/Plugins vor Installation.

WICHTIG: Dieses Skript ist KEIN vollwertiger Sicherheits-Check und kein Ersatz dafür, dass das Modell
den Skill SELBST liest und beurteilt. Es ist eine schnelle, regex-basierte Vorpriorisierung mit klaren
Grenzen: es versteht keine Semantik/keinen Kontext, erkennt neue/kreative Obfuskation nicht, und
produziert bewusst False Positives (fail-safe). `PASS` heißt NUR „keine bekannten Muster gefunden",
NICHT „sicher"; `BLOCK` heißt „bekanntes Risiko-Muster", nicht zwingend „bösartig". Primär ist immer
das manuelle Lesen aller Dateien (SKILL.md, Skripte, package.json, Hooks) durch das Modell.

Staging-then-promote: Skill/Plugin in einen Staging-Ordner klonen, dort lesen + scannen, und erst nach
manuellem Urteil + expliziter Nutzer-Freigabe nach ~/.claude/skills/ kopieren. Nie auto-install.

Sucht nach: pipe-to-shell, eval/exec dekodierter Inhalte, Secret-Zugriffen (.ssh/.npmrc/.aws/Tokens),
ausgehendem Netzwerk in Skripten, npm install-/prepare-Hooks, selbst-registrierenden Hooks/Cron
(settings.json-Hooks, crontab, schtasks, launchctl, atexit) und Prompt-Injection in Markdown.

Dateiauswahl: Dateien mit bekannter Text-Endung werden gelesen; alle anderen (auch ohne Endung, z. B.
install, Makefile, Dockerfile, Git-Hooks) werden gelesen, sofern die ersten 8 KB kein NUL-Byte enthalten.
Nicht prüfbare Dateien (Binär, zu groß, nicht lesbar, Symlink) zählen als "unchecked" und werden im
Bericht aufgeführt. Symlinks werden nie gelesen. Der Ordner `.git` wird übergangen.

Exit-Code: 0 = PASS/REVIEW ohne Lücke, 1 = HIGH/CRITICAL gefunden (BLOCK), 2 = Nutzungsfehler,
3 = kein HIGH/CRITICAL, aber unchecked-Dateien (PASS-MIT-LÜCKEN / REVIEW-MIT-LÜCKEN: Lücke manuell schließen).

Aufruf (empfohlen, auch unter Windows):
    python -I -X utf8 scan_skill_security.py <pfad-zum-staging-ordner> [--json report.json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

TEXT_EXT = {".md", ".markdown", ".py", ".sh", ".bash", ".zsh", ".fish", ".js", ".mjs", ".cjs", ".jsx",
            ".ts", ".tsx", ".json", ".ps1", ".psm1", ".psd1", ".vbs", ".php", ".lua", ".luau", ".toml",
            ".yaml", ".yml", ".bat", ".cmd", ".rb", ".pl", ".txt", ".cfg", ".ini", ".html", ".htm", ".xml"}
MAX_BYTES = 2_000_000  # je Datei
SNIFF_BYTES = 8192  # NUL-Byte-Sniff für Dateien mit unbekannter/fehlender Endung

# (regex, severity, label). Regex case-insensitiv, multiline.
PATTERNS: list[tuple[str, str, str]] = [
    # pipe-to-shell
    (r"\b(curl|wget|iwr|invoke-webrequest)\b[^\n|]{0,200}\|\s*(sh|bash|zsh|iex|invoke-expression|python)\b",
     "CRITICAL", "pipe-to-shell (Download direkt ausführen)"),
    (r"\b(iex|invoke-expression)\b[^\n]{0,120}\b(downloadstring|webrequest|invoke-webrequest)",
     "CRITICAL", "PowerShell IEX(Download)"),
    # decode-then-exec
    (r"base64\s*(-d|--decode|-D)[^\n]{0,120}\|\s*(sh|bash|python)", "CRITICAL", "base64-decode|shell"),
    (r"\b(eval|exec)\s*\(\s*(atob|base64|fromCharCode|unescape|bytes\.fromhex|codecs\.decode)",
     "CRITICAL", "eval/exec dekodierter Daten"),
    (r"\bloadstring\s*\(", "HIGH", "loadstring (dynamische Codeausführung)"),
    (r"\beval\s*\(", "HIGH", "eval()"),
    (r"\bFunction\s*\(\s*['\"]", "HIGH", "Function()-Konstruktor (dyn. Code)"),
    (r"\bexec\s*\(", "MEDIUM", "exec()"),
    # process / shell aus Code
    (r"\b(os\.system|subprocess\.(Popen|run|call|check_output)|child_process|execSync|spawnSync)\b",
     "MEDIUM", "Prozess-/Shell-Aufruf aus Code"),
    (r"\b(Invoke-Expression|Start-Process)\b", "MEDIUM", "PowerShell Prozessstart"),
    # Secrets / Credentials
    (r"\.ssh/|id_rsa|id_ed25519|\.npmrc|\.aws/|aws_secret|credentials\.json|\.netrc",
     "HIGH", "Zugriff auf Secret-/Credential-Pfade"),
    (r"(?i)\b(API[_-]?KEY|AUTH[_-]?TOKEN|ACCESS[_-]?TOKEN|SECRET[_-]?KEY|PASSWORD)\b\s*[:=]",
     "MEDIUM", "Hartkodierter Secret-Bezug"),
    (r"process\.env\.[A-Z_]*(TOKEN|KEY|SECRET|PASS)", "MEDIUM", "Liest Secret-Env-Variable"),
    # Netzwerk / Exfiltration (\b nur um die Wort-Alternativen; fetch( und nc -e haben kein Wortende)
    (r"(\b(requests\.(get|post|put|patch|delete)|httpx\.\w+|urllib\.request|http\.client|axios|net\.connect|"
     r"socket\.socket|netcat|Invoke-RestMethod|Invoke-WebRequest)\b|\bfetch\s*\(|\bnc\s+[-\w])",
     "MEDIUM", "Ausgehendes Netzwerk aus Skript"),
    (r"https?://\d{1,3}(\.\d{1,3}){3}", "HIGH", "Hartkodierte IP-URL"),
    # npm install-Hooks (install und prepare laufen ebenfalls bei der Installation)
    (r"\"(pre|post)?install\"\s*:|\"prepare\"\s*:", "HIGH", "npm install-/prepare-Hook"),
    # selbst-registrierende Hooks / Cron / Scheduler
    (r"\b(crontab|schtasks|Register-ScheduledTask|launchctl|systemctl\s+enable|atexit\.register)\b",
     "HIGH", "Selbst-registrierender Hook/Scheduler/Cron"),
    (r"\"hooks\"\s*:|PreToolUse|PostToolUse|SessionStart", "MEDIUM", "Claude-Hook-Registrierung in Config"),
    # Obfuskation
    (r"(\\x[0-9a-fA-F]{2}){8,}", "HIGH", "Lange Hex-Escape-Kette (Obfuskation)"),
    (r"(chr\(\d+\)\s*\+\s*){6,}|string\.char\((\s*\d+\s*,){6,}", "HIGH", "char()-Kette (Obfuskation)"),
    # Prompt-Injection in Markdown/Text
    (r"(?i)ignore (all )?(previous|prior|above) (instructions|prompts|rules)",
     "HIGH", "Prompt-Injection: 'ignore previous instructions'"),
    (r"(?i)\b(disregard|override)\b[^\n]{0,40}\b(system prompt|instructions|guardrails)",
     "HIGH", "Prompt-Injection: Anweisungs-Override"),
    (r"[​‌‍⁠﻿]", "MEDIUM", "Unsichtbare Unicode-Zeichen (mögliche versteckte Anweisung)"),
]

COMPILED = [(re.compile(p, re.IGNORECASE | re.MULTILINE), sev, lbl) for p, sev, lbl in PATTERNS]
SEV_ORDER = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1}


def _finding(rel: str, severity: str, label: str, excerpt: str = "") -> dict:
    return {"file": rel, "severity": severity, "label": label, "line": 0, "excerpt": excerpt}


def scan_file(path: Path, root: Path) -> tuple[list[dict], str | None]:
    """Liefert (Funde, unchecked-Grund); unchecked-Grund ist None, wenn die Datei vollständig geprüft wurde."""
    rel = str(path.relative_to(root)).replace("\\", "/")
    if path.is_symlink():
        return [_finding(rel, "HIGH", f"Symlink -> {os.readlink(path)} (nicht gelesen)")], "Symlink"
    if not path.resolve().is_relative_to(root.resolve()):
        return [_finding(rel, "HIGH", "Datei liegt außerhalb des Staging-Ordners (nicht gelesen)")], "außerhalb Staging"
    try:
        if path.stat().st_size > MAX_BYTES:
            return [_finding(rel, "MEDIUM", "Datei sehr groß — manuell prüfen")], "zu groß"
        data = path.read_bytes()
    except OSError as e:
        return [_finding(rel, "MEDIUM", "nicht lesbar - manuell prüfen", str(e))], "nicht lesbar"
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = data.decode("utf-16", errors="replace")
    elif path.suffix.lower() not in TEXT_EXT and b"\0" in data[:SNIFF_BYTES]:
        return [], "Binärdatei"
    else:
        text = data.decode("utf-8", errors="replace")
    findings = []
    for rx, sev, lbl in COMPILED:
        for m in rx.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            excerpt = text[max(0, m.start() - 10): m.start() + 70].replace("\n", " ")
            findings.append({"file": rel, "severity": sev, "label": lbl, "line": line_no,
                             "excerpt": excerpt.strip()[:120]})
    return findings, None


def main() -> int:
    ap = argparse.ArgumentParser(description="Sicherheits-Scan eines gestagten Skills/Plugins.")
    ap.add_argument("target", help="Pfad zum Staging-Ordner.")
    ap.add_argument("--json", default=None, help="Report als JSON speichern.")
    args = ap.parse_args()
    # umgeleitete Ausgabe unter Windows (cp1252) darf an Sonderzeichen nicht abbrechen
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    root = Path(args.target)
    if not root.is_dir():
        print(f"FEHLER: kein Verzeichnis: {root}", file=sys.stderr)
        return 2

    all_findings = []
    unchecked = []
    scanned = 0
    for p in root.rglob("*"):
        if ".git" in p.relative_to(root).parts:
            continue
        if p.is_symlink() or p.is_file():
            found, reason = scan_file(p, root)
            all_findings.extend(found)
            if reason:
                unchecked.append({"file": str(p.relative_to(root)).replace("\\", "/"), "reason": reason})
            else:
                scanned += 1

    all_findings.sort(key=lambda f: (-SEV_ORDER.get(f["severity"], 0), f["file"], f["line"]))
    counts = {s: sum(1 for f in all_findings if f["severity"] == s) for s in ("CRITICAL", "HIGH", "MEDIUM")}
    blocked = counts["CRITICAL"] > 0 or counts["HIGH"] > 0
    base = "REVIEW" if counts["MEDIUM"] else "PASS"
    verdict = "BLOCK" if blocked else (base + "-MIT-LÜCKEN" if unchecked else base)

    report = {"target": str(root), "files_scanned": scanned, "unchecked": unchecked, "counts": counts,
              "verdict": verdict, "findings": all_findings}
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[security-scan] {root.name}: {scanned} Dateien geprüft, {len(unchecked)} unchecked · "
          f"CRITICAL={counts['CRITICAL']} HIGH={counts['HIGH']} MEDIUM={counts['MEDIUM']} → {verdict}")
    for f in all_findings[:40]:
        print(f"  [{f['severity']:8}] {f['file']}:{f['line']} — {f['label']}")
        if f["excerpt"]:
            print(f"             … {f['excerpt']}")
    if len(all_findings) > 40:
        print(f"  … und {len(all_findings) - 40} weitere (siehe --json).")
    for u in unchecked[:40]:
        print(f"  [UNCHECKED] {u['file']} — {u['reason']}")
    if len(unchecked) > 40:
        print(f"  … und {len(unchecked) - 40} weitere unchecked (siehe --json).")
    print("HINWEIS: PASS heißt 'keine bekannten Muster', NICHT 'garantiert sicher'. "
          "Bei BLOCK/REVIEW/LÜCKEN vor Installation manuell prüfen.")
    return 1 if blocked else (3 if unchecked else 0)


if __name__ == "__main__":
    raise SystemExit(main())
