#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHubBot Bridge for Community Outreach.
========================================
Synchronizes repository metadata and 14-day traffic analysis from GitHubBot
into the Community Outreach catalog (usecases.json).

Responsibilities:
1. Locate the canonical .GITHUBBOT workspace (repo_registry.json, traffic_report.md).
2. Enforce strict Fail-Closed exclusions:
   - Private repositories (systematic 0 traffic / internal modules)
   - Archived repositories
   - Foreign forks (e.g. Awesome-LLM, awesome-mcp-servers, etc.)
   - Organization/profile meta repos (.github, personal profile, impressum)
   - Duplicate personal mirrors (when canonical org repo exists)
3. Parse 14-day traffic metrics (total & unique views and clones).
4. Update usecases.json with fresh metrics, active flags, and reasons.
5. Provide traffic-based scoring for candidate selection.
"""

from __future__ import annotations

import html
import json
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

logger = logging.getLogger(__name__)

# Fallback names of personal/profile/meta repos never eligible for promotion
BLOCKED_META_REPOS = {
    "lukisch/lukisch",
    "lukisch/impressum",
}

BLOCKED_META_NAMES = {
    "lukisch",
    "impressum",
    ".github",
}

# Concrete high-value skills & innovative procedures promoted individually for specific problems
# Sourced from Innovations_Inventar_und_Prior_Art.md and Top_10_Innovativste_Verfahren.md
SPECIFIC_SKILL_PROFILES = [
    {
        "id": "skills/utilities/lebende-verfassung",
        "org": "ellmos-ai",
        "name": "lebende-verfassung",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/utilities/lebende-verfassung",
        "stars": 0,
        "summary": "Operationalisierte Verfassungs-Superposition: Räumt künftigen Generationen und Ungeborenen über "
        "einen algorithmischen Rawls-Schleier ein formales Veto-Recht gegen kurzfristige "
        "Gegenwartsoptimierungen ein.",
        "problems_solved": [
            "Etablierte KI-Ethik (Constitutional AI, RLHF) optimiert nur kurzfristig für lebende Gegenwarts-Nutzer",
            "Philosophische Verantwortungsethik (Hans Jonas, Rawls) galt bisher als technisch nicht "
            "in Code operationalisierbar",
            "Moralische Halluzinationen und Plausibilitäts-Urteile ohne mathematische "
            "Gegenfaktual-Pflicht und Evidenzhierarchie",
        ],
        "usecases": [
            "Konstitutionelle KI-Ethik & KI-Gouvernanz",
            "Entscheidungs-Prüfketten für gesellschaftliche und langfristige Systemauswirkungen",
            "Auditierung autonomer Handlungsentscheidungen",
        ],
        "target_platforms": [
            "Reddit r/ArtificialInteligence",
            "Reddit r/Philosophy",
            "Reddit r/LocalLLaMA",
            "LessWrong",
        ],
        "search_keywords": [
            "constitutional AI future generations",
            "rawlsian veil of ignorance code algorithm",
            "AI ethics superposition veto ungeborene",
        ],
        "priority": "high",
    },
    {
        "id": "skills/dev/software-in-worten",
        "org": "ellmos-ai",
        "name": "software-in-worten",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/dev/software-in-worten",
        "stars": 0,
        "summary": "Software in Worten & Blueprint-Architektur: Verschmilzt GUI und Instruktionsraum ('Der Klick ist "
        "der Prompt') über typisierte ASCII-Screens als buildfreie Brücke zwischen Mensch und KI-Agent.",
        "problems_solved": [
            "Fundamentale Entkopplung: Grafische Oberflächen für Menschen und Text-Skills für "
            "Sprachmodelle driften unweigerlich auseinander",
            "Extremer Token-Overhead und Latenzen bei Vision-Agenten (Computer Use / Screenshots)",
            "Aufwendige Frontend-Builds für einfache interaktive Werkzeuge und Prototypen",
        ],
        "usecases": [
            "Buildfreie Benutzeroberflächen für KI-gestützte Werkzeuge",
            "Bidirektionale UI-zu-Skill und Skill-zu-UI Synchronisation",
            "Materialisierter Prompt-Zustand für Human-in-the-Loop Interaktion",
        ],
        "target_platforms": ["Reddit r/webdev", "Reddit r/Frontend", "Reddit r/UXDesign", "HackerNews"],
        "search_keywords": [
            "click is the prompt UI AI",
            "text blueprint GUI AI agent",
            "software in worten prompt architecture",
        ],
        "priority": "high",
    },
    {
        "id": "skills/infrastructure/agents-bridge",
        "org": "ellmos-ai",
        "name": "agents-bridge",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/agents-bridge",
        "stars": 0,
        "summary": "Brokerloser Multi-Agenten-Konsens auf synchronisierten Dateisystemen: Koordiniert heterogene "
        "KI-Agenten (Claude, Codex, Gemini) über Cloud-Sync-Ordner mit Fail-Closed Locks, TTL und Null "
        "Server-Overhead.",
        "problems_solved": [
            "Multi-Agenten-Koordination über mehrere Rechner erfordert komplexe "
            "Server-Infrastruktur (Redis, Zookeeper, Raft)",
            "Dateikonflikte, gleichzeitiges Überschreiben und kaputte Locks bei Cloud-Dateisystemen "
            "(OneDrive, Dropbox)",
            "Verwaiste Deadlocks bei abstürzenden Agenten-Prozessen",
        ],
        "usecases": [
            "Serverlose Multi-Host-Flotten-Koordination",
            "Cross-Device Synchronisation heterogener KI-Agenten",
            "Fail-Closed Zugriffsschutz für geteilte Wissens- und Codebasen",
        ],
        "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/SelfHosted", "Reddit r/AgenticAI", "HackerNews"],
        "search_keywords": [
            "brokerless multi agent consensus file system",
            "fail-closed file locks cloud sync agent",
            "multi agent coordination without server",
        ],
        "priority": "high",
    },
    {
        "id": "skills/infrastructure/work-autonomous",
        "org": "ellmos-ai",
        "name": "work-autonomous",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/work-autonomous",
        "stars": 0,
        "summary": "Beweisbasierte Nicht-Abbruch-Prüfkette für autonome Loops (WAAFAP): Invertiert die Beweislast "
        "gegen Agentic Laziness – ein Loop darf erst enden, wenn formal bewiesen ist, dass keine Aufgabe "
        "mehr vorliegt.",
        "problems_solved": [
            "'Agentic Laziness': Autonome Coding-Agenten brechen vorzeitig mit 'Done!' ab, während "
            "ungetestete Fehler verbleiben",
            "Unbemerktes Liegenbleiben offener Aufgaben und Regressionen in autonomen Langläufern",
            "Mangel an kryptografisch referenzierten Abschlussbelegen (Receipts) für abgeschlossene Arbeiten",
        ],
        "usecases": [
            "Autonome Programmier-Loops und unbeaufsichtigte Refactorings",
            "SWE-Bench und Coding-Agent Selbstkontrolle",
            "Beweisbare Erschöpfung von Aufgabenlisten (WAAFAP)",
        ],
        "target_platforms": ["Reddit r/ClaudeAI", "Reddit r/LocalLLaMA", "Reddit r/MachineLearning", "HackerNews"],
        "search_keywords": [
            "agentic laziness premature exit fix",
            "quit requires proof of inactivity",
            "WAAFAP autonomous loop termination protocol",
        ],
        "priority": "high",
    },
    {
        "id": "skills/dev/piggyback-hosting",
        "org": "ellmos-ai",
        "name": "piggyback-hosting",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/dev/piggyback-hosting",
        "stars": 0,
        "summary": "Zero-State / Zero-User-Management Privacy-Architektur: Transformiert Web-Apps in eine "
        "haftungsfreie Zero-State-Infrastruktur via Client-Side SQLite (WASM/OPFS) und Client-Side BYOK.",
        "problems_solved": [
            "Enormer rechtlicher und technischer Overhead für Indie-Devs (DSGVO, Passwörter, "
            "User-DBs, Löschfristen, Auftragsverarbeitung)",
            "Hohe Server- und Datenbank-Hostingkosten für datenintensive SaaS-Prototypen",
            "Datenschutz- und Haftungsrisiken beim Speichern sensibler Nutzerdaten auf zentralen Servern",
        ],
        "usecases": [
            "Haftungsfreies Bereitstellen von KI-Tools und Web-Apps",
            "Client-Side SQLite-Datenbanken via Origin Private File System (OPFS)",
            "Local-First SaaS ohne Server-Datenbank",
        ],
        "target_platforms": ["Reddit r/webdev", "Reddit r/selfhosted", "Reddit r/privacy", "IndieHackers"],
        "search_keywords": [
            "zero-state web app architecture",
            "client side sqlite wasm opfs byok",
            "gdpr free web tool hosting local-first",
        ],
        "priority": "high",
    },
    {
        "id": "skills/utilities/paveman",
        "org": "ellmos-ai",
        "name": "paveman",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/utilities/paveman",
        "stars": 0,
        "summary": "Deterministische, modellfreie Regelkompression (Paveman / Knappform): Reduziert "
        "Markdown-Regelwerke um bis zu 40% Token ohne Modell-Inferenz, ohne Halluzinationsrisiko und bei "
        "100% semantischer Integrität.",
        "problems_solved": [
            "Systemprompts und Regelwerke verschwenden wertvollen Kontext durch Füllwörter und Höflichkeitsfloskeln",
            "Stochastische LLM-Kompression (wie LLMLingua) verwascht sicherheitskritische "
            "Imperative und erzeugt Halluzinationen",
            "Verlangsamte Inferenz und hohe API-Kosten durch aufgeblähte Instruktionssätze",
        ],
        "usecases": [
            "Token-Kompression für Systemprompts und Regelwerke",
            "Deterministische Markdown-Optimierung ohne Qualitätsverlust",
            "AST-bewahrende Regel-Entschlackung",
        ],
        "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/PromptEngineering", "Dev.to"],
        "search_keywords": [
            "deterministic prompt compression no LLM",
            "markdown token minifier rule compression",
            "paveman knappform prompt optimization",
        ],
        "priority": "high",
    },
    {
        "id": "skills/infrastructure/metacognitive-injectors",
        "org": "ellmos-ai",
        "name": "metacognitive-injectors",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/metacognitive-injectors",
        "stars": 0,
        "summary": "Kognitionspsychologisches Selbst-Auditing & Rehearsal-Loop: Implementiert exekutive "
        "Kontrollfunktionen (Miyake-Inhibition) als synchrone Preflight-Checks vor risikobehafteten "
        "Tool-Calls.",
        "problems_solved": [
            "Agenten führen irreversible System-Mutationen aus, ohne das erwartete Ergebnis vorher "
            "mental zu simulieren",
            "Sycophancy und Bestätigungsfehler führen zu vorschnellen Erfolgsmeldungen",
            "Fehlende Pufferung von Zwischenzielen im Arbeitsgedächtnis vor komplexen Tool-Ketten",
        ],
        "usecases": [
            "Exekutive Selbstkontrolle für autonome Agenten",
            "Mental Rehearsal vor Dateisystem- und Shell-Mutationen",
            "Inhibitorische Kontrolle gegen Sycophancy",
        ],
        "target_platforms": ["Reddit r/CognitiveScience", "Reddit r/ArtificialInteligence", "Reddit r/LocalLLaMA"],
        "search_keywords": [
            "metacognitive AI agent preflight check",
            "miyake executive control LLM inhibition",
            "mental rehearsal loop tool call AI",
        ],
        "priority": "high",
    },
    {
        "id": "skills/infrastructure/condition",
        "org": "ellmos-ai",
        "name": "condition",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/condition",
        "stars": 0,
        "summary": "Condition-Gate-Sprache für Prompts: Leichtgewichtige, deklarative Syntax für deterministische "
        "Teilblockaden und Fail-Closed Vorbedingungen direkt in Standard-Markdown.",
        "problems_solved": [
            "LLMs ignorieren Vorbedingungen in Fließtext-Prompts und führen nachfolgende Schritte ungeprüft aus",
            "Komplexe Orchestrierungs-Engines sind für einfache bedingte Anweisungen zu schwerfällig",
            "Mangel an maschinenlesbaren Schutz-Gates in modularen Arbeitsanweisungen",
        ],
        "usecases": [
            "Fail-Closed Gates in Markdown-Prompts",
            "Deterministische Schritt-für-Schritt Freigaben für Agenten",
            "Lineare Flusskontrolle ohne externe Orchestratoren",
        ],
        "target_platforms": ["Reddit r/PromptEngineering", "Reddit r/LocalLLaMA", "Dev.to"],
        "search_keywords": [
            "declarative condition syntax markdown prompts",
            "fail closed prompt gates condition",
            "prompt flow control gates",
        ],
        "priority": "high",
    },
    {
        "id": "skills/infrastructure/wayfinding-routing",
        "org": "ellmos-ai",
        "name": "wayfinding-routing",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/wayfinding-routing",
        "stars": 0,
        "summary": "Nautische Notfall-Navigation für KI-Agenten: Überträgt nautische Prinzipien (Celestial Fix, Dead "
        "Reckoning, Landfall-Protokoll) als Resilienz-System gegen semantische Desorientierung in großen "
        "Dateibäumen.",
        "problems_solved": [
            "Agenten verfangen sich in zirkulären Suchschleifen bei unvollständigem Kontext",
            "Verlust der Orientierung über den aktuellen Systemzustand nach langen Tool-Ketten",
            "Mangel an strukturierten Notfall-Protokollen bei schwerer semantischer Verwirrung",
        ],
        "usecases": [
            "Notfall-Navigation für desorientierte Sprachmodelle",
            "Koppelnavigation (Dead Reckoning) aus Zustands-Receipts",
            "Hard-Reset auf unveränderliche Polarstern-Referenzen",
        ],
        "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/ArtificialInteligence", "HackerNews"],
        "search_keywords": [
            "nautical navigation AI dead reckoning",
            "celestial fix agent disorientation",
            "wayfinding routing agent recovery",
        ],
        "priority": "high",
    },
    {
        "id": "skills/dev/pipeline-optimizer",
        "org": "ellmos-ai",
        "name": "pipeline-optimizer",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/dev/pipeline-optimizer",
        "stars": 0,
        "summary": "Deterministisches 6-Schritte-Verfahren zur schrittweisen Modernisierung und Optimierung "
        "bestehender Software- und Agent-Pipelines.",
        "problems_solved": [
            "Komplexe Legacy-Pipelines brechen bei unstrukturierten Refactorings",
            "Fehlende reproduzierbare Schritte zur Modernisierung von Automationsketten",
            "Ungenügende Regressionstests und Sicherheits-Gates bei Code-Umstellungen",
        ],
        "usecases": [
            "Modernisierung von CI/CD und Agent-Pipelines",
            "Schrittweise Code-Optimierung ohne Regressionsrisiko",
            "6-Schritte-Refactoring für Agentic Pipelines",
        ],
        "target_platforms": ["Reddit r/Python", "Reddit r/ExperiencedDevs", "Dev.to"],
        "search_keywords": [
            "pipeline optimization refactoring",
            "code pipeline modernization 6 step",
            "automated code refactoring protocol",
        ],
        "priority": "high",
    },
    {
        "id": "skills/game-dev/using-blender",
        "org": "ellmos-ai",
        "name": "using-blender",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/game-dev/using-blender",
        "stars": 0,
        "summary": "Spezifischer Skill für automatisierte Blender 3D-Asset-QA, Headless FBX/GLTF-Exporte und "
        "Python-Steuerung für Game-Developer.",
        "problems_solved": [
            "Manuelle, zeitraubende 3D-Asset-Exporte und fehlerhafte FBX-Reimporte in Game Engines",
            "Fehlende automatisierte Qualitätskontrolle für 3D-Modelle ohne Öffnen der Blender-GUI",
            "Schwierige Einbindung von Blender in headless CI/CD-Pipelines",
        ],
        "usecases": [
            "Headless Blender 3D-Automation",
            "Game Development CI/CD Pipelines",
            "Automatisierte Asset-Validierung",
        ],
        "target_platforms": ["Reddit r/blender", "Reddit r/gamedev", "Reddit r/IndieDev"],
        "search_keywords": ["blender headless export", "blender python automation game dev", "fbx qa blender script"],
        "priority": "high",
    },
    {
        "id": "skills/utilities/video-transcriber",
        "org": "ellmos-ai",
        "name": "video-transcriber",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/utilities/video-transcriber",
        "stars": 0,
        "summary": "Lokaler Transkriptions-Skill für Video- und Audio-Dateien mit segmentierten Timestamps ohne "
        "Cloud-Kosten und ohne API-Limits.",
        "problems_solved": [
            "Hohe API-Kosten bei kommerziellen Speech-to-Text-Diensten für lange Videos/Podcasts",
            "Datenschutzbedenken beim Hochladen sensibler Audio- und Videoaufnahmen in die Cloud",
            "Fehlende strukturierte Zeitstempel-Segmente für automatisierte Videoschnitte",
        ],
        "usecases": [
            "Lokale Video- und Podcast-Transkription",
            "Content Creation & Schnitt-Automatisierung",
            "Datenschutzkonforme Audio-Verarbeitung",
        ],
        "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/SelfHosted", "Reddit r/videoediting"],
        "search_keywords": [
            "local video transcription open source",
            "transcribe audio offline free",
            "video transcript timestamps python",
        ],
        "priority": "high",
    },
]


@dataclass
class TrafficData:
    views_total: int = 0
    views_unique: int = 0
    clones_total: int = 0
    clones_unique: int = 0
    top_referrers: list[dict[str, Any]] = field(default_factory=list)
    top_paths: list[dict[str, Any]] = field(default_factory=list)

    def traffic_score(self) -> int:
        """Weighted traffic score: unique clones weighted 2x, unique views 1x."""
        return self.clones_unique * 2 + self.views_unique


@dataclass
class RepoClassification:
    is_active: bool
    reason: str = ""
    visibility: str = "public"
    is_archived: bool = False
    is_fork: bool = False


def find_githubbot_dir(custom_path: str | Path | None = None) -> Path | None:
    """Find the canonical .GITHUBBOT directory."""
    if custom_path:
        p = Path(custom_path).resolve()
        if p.exists() and (p / "config" / "repo_registry.json").exists():
            return p

    env_dir = os.environ.get("GITHUBBOT_DIR")
    if env_dir:
        p = Path(env_dir).resolve()
        if p.exists():
            return p

    candidates = [
        Path.home() / "OneDrive" / ".GITHUBBOT",
        Path(__file__).resolve().parent.parent / ".GITHUBBOT",
    ]
    for c in candidates:
        if c.exists() and (c / "config" / "repo_registry.json").exists():
            return c
    return None


def parse_traffic_report(traffic_md_text: str) -> tuple[dict[str, TrafficData], set[str], set[str]]:
    """
    Parses traffic_report.md from GitHubBot.
    Returns:
      (traffic_by_repo, private_repos_set, archived_repos_set)
    """
    traffic_map: dict[str, TrafficData] = {}
    private_set: set[str] = set()
    archived_set: set[str] = set()

    # 1. Parse active repo traffic blocks
    pattern = re.compile(
        r"\*\*([a-zA-Z0-9_-]+)/([a-zA-Z0-9._-]+)\*\*\s*\n"
        r"\s*Views \(14d\):\s*(\d+)\s*gesamt\s*/\s*(\d+)\s*unique\s*\n"
        r"\s*Clones \(14d\):\s*(\d+)\s*gesamt\s*/\s*(\d+)\s*unique"
    )
    for m in pattern.finditer(traffic_md_text):
        org, name, vt, vu, ct, cu = m.groups()
        key = f"{org}/{name}".casefold()
        traffic_map[key] = TrafficData(
            views_total=int(vt),
            views_unique=int(vu),
            clones_total=int(ct),
            clones_unique=int(cu),
        )

    # 2. Parse private section
    priv_match = re.search(r"### Diese Module sind privat:\s*\n(.*?)(?=\n###|\Z)", traffic_md_text, re.DOTALL)
    if priv_match:
        for line in priv_match.group(1).strip().splitlines():
            m = re.match(r"-\s*\*\*([^*]+)\*\*\s*\(\d+\):\s*(.*)", line)
            if m:
                org = m.group(1).strip().casefold()
                names = [x.strip() for x in m.group(2).split(",") if x.strip()]
                for n in names:
                    private_set.add(f"{org}/{n.casefold()}")
                    private_set.add(n.casefold())

    # 3. Parse archived section
    arch_match = re.search(r"### Archiviert:\s*\n(.*?)(?=\n###|\Z)", traffic_md_text, re.DOTALL)
    if arch_match:
        for line in arch_match.group(1).strip().splitlines():
            m = re.match(r"-\s*\*\*([^*]+)\*\*\s*\(\d+\):\s*(.*)", line)
            if m:
                org = m.group(1).strip().casefold()
                names = [x.strip() for x in m.group(2).split(",") if x.strip()]
                for n in names:
                    archived_set.add(f"{org}/{n.casefold()}")
                    archived_set.add(n.casefold())

    return traffic_map, private_set, archived_set


def load_githubbot_registry(githubbot_dir: Path) -> dict[str, dict[str, Any]]:
    """Loads repo_registry.json from GitHubBot."""
    registry_path = githubbot_dir / "config" / "repo_registry.json"
    if not registry_path.exists():
        return {}
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        return data.get("repos", {})
    except Exception as exc:
        logger.warning("Could not read repo_registry.json: %s", exc)
        return {}


def _registry_entry(registry_repos: Mapping[str, Any], *keys: str) -> Mapping[str, Any]:
    """Registry lookup independent of GitHub's casing."""
    wanted = {key.strip().casefold() for key in keys}
    return next((value for key, value in registry_repos.items() if key.casefold() in wanted), None) or {}


def classify_repo(
    repo_id: str,
    org: str,
    name: str,
    registry_repos: Mapping[str, Any],
    private_set: set[str],
    archived_set: set[str],
    all_catalog_repos: list[Mapping[str, Any]] | None = None,
) -> RepoClassification:
    """
    Applies strict fail-closed classification on a repository.
    """
    id_lower = repo_id.strip().casefold()
    name_lower = name.strip().casefold()
    org_lower = org.strip().casefold()

    # Check meta/profile repos
    if id_lower in BLOCKED_META_REPOS or name_lower in BLOCKED_META_NAMES or name_lower.startswith("."):
        return RepoClassification(is_active=False, reason="profile_meta")

    # Check against parsed traffic report private/archived lists
    if id_lower in private_set or name_lower in private_set:
        return RepoClassification(is_active=False, reason="private", visibility="private")

    if id_lower in archived_set or name_lower in archived_set:
        return RepoClassification(is_active=False, reason="archived", is_archived=True)

    # Check against GitHubBot repo_registry -- fail-closed: only a positive public record activates
    gh_info = _registry_entry(registry_repos, repo_id, f"{org}/{name}").get("github") or {}
    visibility = gh_info.get("visibility")

    if visibility != "public":
        reason = "private" if visibility == "private" else "unverified_visibility"
        return RepoClassification(is_active=False, reason=reason, visibility=str(visibility or "unknown"))
    if gh_info.get("archived") is not False:
        return RepoClassification(is_active=False, reason="archived", is_archived=True)
    if gh_info.get("fork") is not False:
        return RepoClassification(is_active=False, reason="foreign_fork", is_fork=True)

    # Deactivate generic monolithic skills hub -- specific skills are promoted individually
    if id_lower == "ellmos-ai/skills":
        return RepoClassification(is_active=False, reason="generic_hub_promoted_via_specific_skills")

    # Check duplicate personal mirrors under lukisch/ if canonical org repo exists
    if org_lower == "lukisch" and all_catalog_repos:
        has_org_canonical = any(
            str(r.get("name", "")).casefold() == name_lower and str(r.get("org", "")).casefold() != "lukisch"
            for r in all_catalog_repos
        )
        if has_org_canonical:
            return RepoClassification(is_active=False, reason="duplicate_personal_mirror")

    return RepoClassification(is_active=True, reason="eligible", visibility="public")


def sync_githubbot_traffic(
    usecases_path: Path,
    githubbot_dir: Path | None = None,
    import_missing_public: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    """
    Main synchronization routine:
    1. Loads traffic_report.md and repo_registry.json
    2. Updates every existing repository in usecases.json
    3. Excludes private/archived/fork/meta repos
    4. Injects traffic numbers and github metadata
    5. Optionally imports public repos with traffic missing from usecases.json
    6. Saves usecases.json atomically
    """
    gb_dir = githubbot_dir or find_githubbot_dir()
    if not gb_dir:
        return {"status": "error", "message": "GitHubBot directory not found"}

    traffic_file = gb_dir / "traffic_report.md"
    traffic_text = traffic_file.read_text(encoding="utf-8") if traffic_file.exists() else ""
    traffic_map, private_set, archived_set = parse_traffic_report(traffic_text)
    registry_repos = load_githubbot_registry(gb_dir)

    if not usecases_path.exists():
        return {"status": "error", "message": f"usecases.json not found at {usecases_path}"}

    usecases_data = json.loads(usecases_path.read_text(encoding="utf-8"))
    existing_repos = usecases_data.get("repositories", [])
    now_iso = datetime.now(timezone.utc).astimezone().isoformat()

    active_count = 0
    excluded_count = 0
    updated_count = 0
    imported_count = 0

    known_ids = set()
    # statically verified public skills (see test) are handled by the profile loop below
    profile_ids = {skill["id"].casefold() for skill in SPECIFIC_SKILL_PROFILES}

    for repo in existing_repos:
        repo_id = str(repo.get("id", ""))
        org = str(repo.get("org", ""))
        name = str(repo.get("name", ""))
        known_ids.add(repo_id.casefold())
        if repo_id.casefold() in profile_ids:
            continue

        classification = classify_repo(
            repo_id=repo_id,
            org=org,
            name=name,
            registry_repos=registry_repos,
            private_set=private_set,
            archived_set=archived_set,
            all_catalog_repos=existing_repos,
        )

        repo["active"] = classification.is_active
        repo["exclusion_reason"] = classification.reason if not classification.is_active else None

        # GitHub metadata
        gh_info = _registry_entry(registry_repos, repo_id, f"{org}/{name}").get("github") or {}
        repo["github_meta"] = {
            "visibility": gh_info.get("visibility", classification.visibility),
            "archived": gh_info.get("archived", classification.is_archived),
            "fork": gh_info.get("fork", classification.is_fork),
            "stars": gh_info.get("stars", repo.get("stars", 0)),
        }

        # Traffic data
        key_id = repo_id.casefold()
        key_name = f"{org}/{name}".casefold()
        tf = traffic_map.get(key_id) or traffic_map.get(key_name) or traffic_map.get(name.casefold())
        if tf:
            repo["traffic"] = {
                "views_14d": tf.views_total,
                "views_unique_14d": tf.views_unique,
                "clones_14d": tf.clones_total,
                "clones_unique_14d": tf.clones_unique,
                "traffic_score": tf.traffic_score(),
                "updated_at": now_iso,
            }
        else:
            repo["traffic"] = {
                "views_14d": 0,
                "views_unique_14d": 0,
                "clones_14d": 0,
                "clones_unique_14d": 0,
                "traffic_score": 0,
                "updated_at": now_iso,
            }

        # Priority adjustment based on proven traffic
        if repo["active"]:
            active_count += 1
            tf_score = repo["traffic"]["traffic_score"]
            # High interest tools get priority boost if not explicitly set
            if tf_score >= 80 or repo["traffic"]["clones_unique_14d"] >= 40:
                repo["priority"] = "high"
            elif repo.get("priority") not in ["high", "low"]:
                repo["priority"] = "normal"
        else:
            excluded_count += 1

        updated_count += 1

    # Optional import of missing public repos that have traffic
    if import_missing_public:
        for full_repo, tf in traffic_map.items():
            if full_repo in known_ids or "/" not in full_repo:
                continue
            org, name = full_repo.split("/", 1)
            classification = classify_repo(
                repo_id=full_repo,
                org=org,
                name=name,
                registry_repos=registry_repos,
                private_set=private_set,
                archived_set=archived_set,
                all_catalog_repos=existing_repos,
            )
            if not classification.is_active:
                continue

            gh_info = _registry_entry(registry_repos, full_repo).get("github") or {}
            desc = gh_info.get("description") or f"Open-source tool {name} by {org}"
            topics = gh_info.get("topics") or []

            new_repo = {
                "id": f"{org}/{name}",
                "org": org,
                "name": name,
                "url": f"https://github.com/{org}/{name}",
                "stars": gh_info.get("stars", 0),
                "summary": desc,
                "problems_solved": [
                    f"Bedarf an einer leichtgewichtigen, lokalen Open-Source-Lösung für {name}",
                    f"Vermeidung von Cloud-Abhängigkeiten und Vendor-Lock-in im Bereich {org}",
                    "Fehlende flexible Automatisierung oder spezialisiertes Tooling für Entwickler",
                ],
                "usecases": [
                    f"Einsatz im Bereich {org}",
                    f"Lokale Entwicklung und Automatisierung mit {name}",
                ],
                "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/OpenSource", "Reddit r/Python"],
                "search_keywords": [f"{name} open source", f"{name} alternative", f"{org} {name}"] + topics[:3],
                "last_promoted_at": None,
                "total_promotions": 0,
                "priority": "high" if tf.traffic_score() >= 80 else "normal",
                "active": True,
                "exclusion_reason": None,
                "github_meta": {
                    "visibility": "public",
                    "archived": False,
                    "fork": False,
                    "stars": gh_info.get("stars", 0),
                },
                "traffic": {
                    "views_14d": tf.views_total,
                    "views_unique_14d": tf.views_unique,
                    "clones_14d": tf.clones_total,
                    "clones_unique_14d": tf.clones_unique,
                    "traffic_score": tf.traffic_score(),
                    "updated_at": now_iso,
                },
            }
            existing_repos.append(new_repo)
            known_ids.add(full_repo.casefold())
            imported_count += 1
            active_count += 1

    # Inject specific high-value skills from SPECIFIC_SKILL_PROFILES
    for skill in SPECIFIC_SKILL_PROFILES:
        skill_id = skill["id"].casefold()
        existing = next((r for r in existing_repos if str(r.get("id", "")).casefold() == skill_id), None)
        if existing:
            existing.update(skill)
            existing["active"] = True
            existing["exclusion_reason"] = None
            existing["github_meta"] = {"visibility": "public", "archived": False, "fork": False, "stars": 0}
            active_count += 1
        else:
            entry = dict(skill)
            entry["last_promoted_at"] = None
            entry["total_promotions"] = 0
            entry["active"] = True
            entry["exclusion_reason"] = None
            entry["github_meta"] = {"visibility": "public", "archived": False, "fork": False, "stars": 0}
            entry["traffic"] = dict(skill.get("traffic", {}))
            entry["traffic"]["updated_at"] = now_iso
            existing_repos.append(entry)
            imported_count += 1
            active_count += 1

    usecases_data["updated_at"] = now_iso

    usecases_data["githubbot_sync"] = {
        "synced_at": now_iso,
        "githubbot_source": gb_dir.name,
        "active_repos": active_count,
        "excluded_repos": excluded_count,
        "imported_repos": imported_count,
    }

    if dry_run:
        return {"status": "dry-run", "total_repos": len(existing_repos), **usecases_data["githubbot_sync"]}

    # Write atomically
    temp_path = usecases_path.with_name(f".{usecases_path.name}.{os.getpid()}.tmp")
    temp_path.write_text(json.dumps(usecases_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp_path.replace(usecases_path)

    # Regenerate USECASES.md in parity with usecases.json
    md_path = usecases_path.parent / "USECASES.md"
    try:
        export_usecases_markdown(usecases_data, md_path)
    except Exception as exc:
        logger.warning("Could not export USECASES.md: %s", exc)

    return {
        "status": "success",
        "total_repos": len(existing_repos),
        "active_repos": active_count,
        "excluded_repos": excluded_count,
        "imported_repos": imported_count,
    }


_REPO_ID = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_ACTIVE_SCHEME = re.compile(r"(?i)\b(javascript|data|vbscript):")


def _md(value: Any) -> str:
    """Neutralise foreign metadata for Markdown: no HTML, no links, no table breaks."""
    text = html.escape(str(value if value is not None else ""), quote=False)
    text = _ACTIVE_SCHEME.sub(r"\1&#58;", text)
    for char in "\\`*_[]|":
        text = text.replace(char, "\\" + char)
    return " ".join(text.split())


def _safe_url(repo: Mapping[str, Any]) -> str:
    url = str(repo.get("url") or "")
    if url.startswith("https://github.com/") and not any(c in url for c in " <>()\"'`"):
        return url
    repo_id = str(repo.get("id") or "")
    return f"https://github.com/{repo_id}" if _REPO_ID.match(repo_id) else ""


def export_usecases_markdown(usecases_data: dict[str, Any], output_path: Path) -> None:
    """Regenerates USECASES.md from usecases_data to maintain strict parity.

    Foreign GitHub metadata is escaped; excluded repositories appear only as counts per reason,
    so names of private repositories never reach the Markdown file.
    """
    repos = usecases_data.get("repositories", [])
    active_repos = [r for r in repos if r.get("active", True)]
    excluded_repos = [r for r in repos if not r.get("active", True)]

    # Group active repos by org
    orgs: dict[str, list[dict[str, Any]]] = {}
    for r in active_repos:
        org = r.get("org", "sonstige")
        orgs.setdefault(org, []).append(r)

    today_str = datetime.now().strftime("%Y-%m-%d")

    lines = [
        "# Usecases & Problemlösungs-Katalog unserer Open-Source-Repositories",
        "",
        "> Dieses Verzeichnis erfasst alle aktiven, öffentlichen Repositories über alle Organisationen.",
        "> Es dient der Automatisierung als Wissensbasis, um in Online-Diskussionen (Reddit, YouTube, Foren) exakt passende, lösungsorientierte Hilfestellungen vorzuschlagen.",
        "",
        f"**Stand:** {today_str} | **Aktive öffentliche Repositories:** {len(active_repos)} | **Gesperrte/Ausgeschlossene Module:** {len(excluded_repos)}",
        "",
        "---",
        "",
        "## 1. Schnelle Übersichtstabelle (Use Cases, Gelöste Probleme & 14-Tage-Traffic)",
        "",
        "| Repo | Organisation | Kernfunktionalität | 14d-Traffic | Gelöste Probleme & Frustrationen | Zielgruppen & Suchbegriffe |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for r in active_repos:
        name = _md(r.get("name", ""))
        url = _safe_url(r)
        org = _md(r.get("org", ""))
        summary = _md(r.get("summary") or "")
        tf = r.get("traffic", {})
        clones_u = int(tf.get("clones_unique_14d", 0))
        views_u = int(tf.get("views_unique_14d", 0))
        tf_str = f"{clones_u} Clones / {views_u} Views (14d)"
        problems = "<br>• " + "<br>• ".join(_md(p) for p in (r.get("problems_solved") or ["Allgemeine Lösung"]))
        keywords = _md(", ".join(r.get("search_keywords") or [f"{r.get('name', '')} open source"]))
        lines.append(f"| [{name}]({url}) | {org} | {summary} | {tf_str} | {problems} | {keywords} |")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 2. Detaillierte Repositories nach Organisation",
            "",
        ]
    )

    for org_name in sorted(orgs.keys()):
        org_items = orgs[org_name]
        lines.append(f"### Organisation: {_md(org_name)} ({len(org_items)} Repos)")
        lines.append("")
        for r in sorted(org_items, key=lambda x: str(x.get("name", ""))):
            tf = r.get("traffic", {})
            lines.append(f"#### [{_md(r.get('name', ''))}]({_safe_url(r)})")
            lines.append(f"- **Beschreibung:** {_md(r.get('summary', ''))}")
            if tf:
                lines.append(
                    f"- **14-Tage-Traffic:** {int(tf.get('clones_14d', 0))} Clones "
                    f"({int(tf.get('clones_unique_14d', 0))} unique), {int(tf.get('views_14d', 0))} Views "
                    f"({int(tf.get('views_unique_14d', 0))} unique)"
                )
            lines.append("- **Gelöste Probleme:**")
            for p in r.get("problems_solved", []):
                lines.append(f"  - {_md(p)}")
            lines.append(f"- **Typische Usecases:** {_md(', '.join(r.get('usecases', [])))}")
            lines.append(f"- **Relevante Plattformen:** {_md(', '.join(r.get('target_platforms', [])))}")
            lines.append(f"- **Suchbegriffe:** {_md(', '.join(r.get('search_keywords', [])))}")
            lines.append("")

    if excluded_repos:
        lines.extend(
            [
                "---",
                "",
                "## 3. Ausgeschlossene & Deaktivierte Repositories (Audit-Trail)",
                "",
                "> Nur Anzahl je Grund; Namen stehen ausschließlich in usecases.json.",
                "",
                "| Ausschlussgrund | Anzahl |",
                "| :--- | :--- |",
            ]
        )
        reasons: dict[str, int] = {}
        for r in excluded_repos:
            reason = str(r.get("exclusion_reason") or "manual_deactivation")
            reasons[reason] = reasons.get(reason, 0) + 1
        for reason, count in sorted(reasons.items()):
            lines.append(f"| {_md(reason)} | {count} |")
        lines.append("")

    temp_path = output_path.with_name(f".{output_path.name}.tmp")
    temp_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temp_path.replace(output_path)


if __name__ == "__main__":
    workspace = Path(__file__).resolve().parent
    uc_path = workspace / "usecases.json"
    print(f"Syncing {uc_path} with GitHubBot...")
    res = sync_githubbot_traffic(uc_path)
    print(json.dumps(res, indent=2, ensure_ascii=False))
