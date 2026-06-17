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
ausgehendem Netzwerk in Skripten, npm pre/postinstall-Hooks, selbst-registrierenden Hooks/Cron
(settings.json-Hooks, crontab, schtasks, launchctl, atexit) und Prompt-Injection in Markdown.

Exit-Code: 0 = kein CRITICAL/HIGH (PASS), 1 = HIGH/CRITICAL gefunden (BLOCK), 2 = Nutzungsfehler.

Aufruf (Windows: PYTHONIOENCODING=utf-8 setzen):
    python scan_skill_security.py <pfad-zum-staging-ordner> [--json report.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TEXT_EXT = {".md", ".markdown", ".py", ".sh", ".bash", ".js", ".mjs", ".cjs", ".ts",
            ".json", ".ps1", ".psm1", ".lua", ".luau", ".toml", ".yaml", ".yml",
            ".bat", ".cmd", ".rb", ".pl", ".txt", ".cfg", ".ini"}
MAX_BYTES = 2_000_000  # je Datei

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
    # Netzwerk / Exfiltration
    (r"\b(requests\.(get|post)|urllib\.request|http\.client|fetch\(|axios|net\.connect|socket\.socket|nc\s|netcat)\b",
     "MEDIUM", "Ausgehendes Netzwerk aus Skript"),
    (r"https?://\d{1,3}(\.\d{1,3}){3}", "HIGH", "Hartkodierte IP-URL"),
    # npm install-Hooks
    (r"\"(pre|post)install\"\s*:", "HIGH", "npm pre/postinstall-Hook"),
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


def scan_file(path: Path, root: Path) -> list[dict]:
    findings = []
    try:
        if path.stat().st_size > MAX_BYTES:
            return [{"file": str(path.relative_to(root)), "severity": "MEDIUM",
                     "label": "Datei sehr groß — manuell prüfen", "line": 0, "excerpt": ""}]
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for rx, sev, lbl in COMPILED:
        for m in rx.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            excerpt = text[max(0, m.start() - 10): m.start() + 70].replace("\n", " ")
            findings.append({
                "file": str(path.relative_to(root)).replace("\\", "/"),
                "severity": sev, "label": lbl, "line": line_no,
                "excerpt": excerpt.strip()[:120],
            })
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Sicherheits-Scan eines gestagten Skills/Plugins.")
    ap.add_argument("target", help="Pfad zum Staging-Ordner.")
    ap.add_argument("--json", default=None, help="Report als JSON speichern.")
    args = ap.parse_args()

    root = Path(args.target)
    if not root.is_dir():
        print(f"FEHLER: kein Verzeichnis: {root}", file=sys.stderr)
        return 2

    all_findings = []
    scanned = 0
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXT:
            scanned += 1
            all_findings.extend(scan_file(p, root))

    all_findings.sort(key=lambda f: (-SEV_ORDER.get(f["severity"], 0), f["file"], f["line"]))
    counts = {s: sum(1 for f in all_findings if f["severity"] == s) for s in ("CRITICAL", "HIGH", "MEDIUM")}
    blocked = counts["CRITICAL"] > 0 or counts["HIGH"] > 0
    verdict = "BLOCK" if blocked else ("REVIEW" if counts["MEDIUM"] else "PASS")

    report = {"target": str(root), "files_scanned": scanned, "counts": counts,
              "verdict": verdict, "findings": all_findings}
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[security-scan] {root.name}: {scanned} Dateien · "
          f"CRITICAL={counts['CRITICAL']} HIGH={counts['HIGH']} MEDIUM={counts['MEDIUM']} → {verdict}")
    for f in all_findings[:40]:
        print(f"  [{f['severity']:8}] {f['file']}:{f['line']} — {f['label']}")
        if f["excerpt"]:
            print(f"             … {f['excerpt']}")
    if len(all_findings) > 40:
        print(f"  … und {len(all_findings) - 40} weitere (siehe --json).")
    print("HINWEIS: PASS heißt 'keine bekannten Muster', NICHT 'garantiert sicher'. "
          "Bei BLOCK/REVIEW vor Installation manuell prüfen.")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
