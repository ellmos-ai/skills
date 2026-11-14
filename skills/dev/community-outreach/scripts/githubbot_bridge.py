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

# Organizations completely excluded from outreach due to legal/regulatory compliance (Nutzerentscheid 2026-11-09)
BLOCKED_ORGS = {
    "biotec-line",
}

# Primary organizations for regular product/solution outreach (Nutzerentscheid 2026-11-09)
PRIMARY_OUTREACH_ORGS = {
    "ellmos-ai",
    "dev-bricks",
    "file-bricks",
    "doc-bricks",
    "open-bricks",
}

# Organizations used for scientific discourse & positioning on research topics rather than product promotion
DISCOURSE_ONLY_ORGS = {
    "research-line",
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
    {
        "id": "skills/infrastructure/skill-extractor",
        "org": "ellmos-ai",
        "name": "skill-extractor",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/skill-extractor",
        "stars": 0,
        "summary": "Skill-Extraktor aus Session-Transkripten: Segmentiert echte Chatverläufe in Stationen, bewertet Wiederverwendbarkeit und destilliert daraus portable SKILL.md-Pakete statt ad-hoc-Prompts.",
        "problems_solved": [
            "Erfolgreiche Problemlösungen in langen Coding-Agent-Sessions gehen im Chatverlauf verloren",
            "Manuelles Schreiben wiederverwendbarer Agent-Skills kostet Zeit und vergisst kritische Randfälle",
            "Unstrukturierte Massen-Transkripte lassen sich ohne Vorsegmentierung nicht sauber auswerten",
        ],
        "usecases": [
            "Automatische Destillation wiederverwendbarer Skills aus Claude/Codex/Gemini-Transkripten",
            "Bulk-Auswertung historischer Agent-Sessions per Stationen-Scoring",
            "Vermeidung von Skill-Duplikaten durch Abgleich mit bestehenden Skills",
        ],
        "target_platforms": ["Reddit r/ClaudeAI", "Reddit r/LocalLLaMA", "Reddit r/ChatGPTCoding"],
        "search_keywords": [
            "extract agent skill from chat transcript",
            "reusable claude code skill from session",
            "skill extractor llm transcripts",
        ],
        "priority": "high",
    },
    {
        "id": "skills/infrastructure/skill-explorer",
        "org": "ellmos-ai",
        "name": "skill-explorer",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/skill-explorer",
        "stars": 0,
        "summary": "Skill-Landschafts-Manager & Security-Auditor: Inventarisiert lokale Agent-Skills, erkennt Duplikate, bildet schlanke Familien-Router statt Kontext-Monolithen und prüft fremde Skills vor der Installation.",
        "problems_solved": [
            "Wachsende Sammlungen von 50+ SKILL.md-Dateien blähen das Kontextfenster von Coding-Agenten auf",
            "Überlappende oder doppelt installierte Skills führen zu widersprüchlichem Agentenverhalten",
            "Fehlende Sicherheitsprüfung beim Übernehmen externer Community-Skills",
        ],
        "usecases": [
            "Audit und Konsolidierung großer SKILL.md-Bibliotheken",
            "Generierung leichtgewichtiger Familien-Umbrella-Router",
            "Vorab-Sicherheitsprüfung neuer Skills und Plugins",
        ],
        "target_platforms": ["Reddit r/ClaudeAI", "Reddit r/LocalLLaMA", "Reddit r/AI_Agents"],
        "search_keywords": [
            "manage many claude skills context bloat",
            "skill router umbrella claude code",
            "audit agent skills library",
        ],
        "priority": "high",
    },
    {
        "id": "skills/dev/sec-supplychain",
        "org": "ellmos-ai",
        "name": "sec-supplychain",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/dev/sec-supplychain",
        "stars": 0,
        "summary": "Supply-Chain-Gate für KI-Skills, Plugins, Hooks und MCP-Server: Erzwingt 'Staging-then-promote' mit statischem Musterscanner gegen Prompt-Injection, Exfiltration und versteckte Shell-Payloads.",
        "problems_solved": [
            "Ungeprüft installierte Agent-Skills, MCP-Server oder Hooks können versteckte Prompt-Injections oder Credential-Exfiltration enthalten",
            "Agenten installieren fremde Pakete oft direkt in produktive Konfigurationsordner ohne Quarantäne-Stufe",
            "Fehlender deterministischer Vorab-Scanner für SKILL.md, hooks.json und MCP-Manifeste",
        ],
        "usecases": [
            "Quarantäne-Prüfung (Staging-then-promote) vor der Installation fremder Skills und MCP-Server",
            "Automatischer Musterscan auf verdächtige Netzwerk-, Shell- und Prompt-Injection-Muster",
            "Supply-Chain-Absicherung lokaler Multi-Agent-Umgebungen",
        ],
        "target_platforms": ["Reddit r/ClaudeAI", "Reddit r/netsec", "Reddit r/LocalLLaMA"],
        "search_keywords": [
            "mcp server security check before install",
            "agent skill prompt injection supply chain",
            "staging then promote ai plugins",
        ],
        "priority": "high",
    },
    {
        "id": "skills/infrastructure/automation-self-care",
        "org": "ellmos-ai",
        "name": "automation-self-care",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/infrastructure/automation-self-care",
        "stars": 0,
        "summary": "Anbieterneutrales Self-Care-Kernset für geplante KI-Automationen: Verbindet Policy-Linting, Lock-Governance, Readback-Pflicht und Rollback für unbeaufsichtigte Scheduled-Tasks über Claude, Codex und Gemini.",
        "problems_solved": [
            "Geplante Hintergrund-Agenten driften mit der Zeit auseinander, überschreiben gesperrte Dateien oder scheitern stillschweigend",
            "Fehlende einheitliche Sicherheits- und Readback-Gates über verschiedene Agent-Scheduler hinweg",
            "Regeldateien (CLAUDE.md, GEMINI.md) werden durch ungefilterte Automations-Laufberichte zugemüllt",
        ],
        "usecases": [
            "Selbstheilende Wartung für geplante KI-Agenten-Läufe und Desktop-Automationen",
            "Deterministisches Policy- und Lock-Linting vor jedem Scheduled-Task",
            "Flotten-Audit für wiederkehrende Hintergrund-Workflows",
        ],
        "target_platforms": ["Reddit r/ClaudeAI", "Reddit r/LocalLLaMA", "Reddit r/AI_Agents"],
        "search_keywords": [
            "scheduled ai agents self healing governance",
            "unattended coding agent tasks lock safety",
            "automation fleet audit llm",
        ],
        "priority": "high",
    },
    {
        "id": "skills/dev/compare-race",
        "org": "ellmos-ai",
        "name": "compare-race",
        "url": "https://github.com/ellmos-ai/skills/tree/master/skills/dev/compare-race",
        "stars": 0,
        "summary": "Multi-Modell-Vergleichsrennen (Stoppuhr oder Parallel-Race): Schickt denselben Prompt an mehrere LLMs und lässt das Startmodell Qualität, Korrektheit, Vollständigkeit, Instruktionstreue und Latenz bewerten.",
        "problems_solved": [
            "Subjektives Rätselraten, welches Modell (Claude, GPT/Codex, Gemini, lokales Ollama) eine konkrete Aufgabe besser löst",
            "Reine Latenz-Benchmarks ignorieren Instruktionstreue und inhaltliche Vollständigkeit",
            "Manuelles Copy-Pasten desselben Prompts in mehrere CLI-Agenten kostet unnötig Zeit",
        ],
        "usecases": [
            "Direkter A/B/C-Modellvergleich am selben Prompt (sequenziell per Stoppuhr oder parallel)",
            "Strukturierte Richter-Bewertung nach Qualität, Korrektheit und Zeit",
            "Empirische Modellauswahl für spezifische Projekt-Aufgaben",
        ],
        "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/ClaudeAI", "Reddit r/ChatGPTCoding"],
        "search_keywords": [
            "compare multiple llm models same prompt cli",
            "model race benchmark judge claude codex gemini",
            "parallel prompt evaluation local llm",
        ],
        "priority": "high",
    },
]

# Core ecosystem flagships (always Tier 1 when not in cooldown)
CORE_ECOSYSTEM_FLAGSHIPS = {
    "ellmos-ai/bach": 99,
    "ellmos-ai/open-ocean": 99,
    "ellmos-ai/skills": 101,
}

CORE_FLAGSHIP_PROFILES = {
    "ellmos-ai/bach": {
        "summary": "BACH (Binary Autonomous Code Host): Lokales, datei- & textbasiertes Betriebssystem für LLM-Agenten mit 110+ Handlern, SQLite-Memory, Task-Queue, Lock-Governance und MCP-Brücke.",
        "problems_solved": [
            "LLM-Agenten verlieren ihren Kontext, Arbeitsstand und ihre Werkzeuge zwischen Sessions (Context Window Amnesie)",
            "Hohe Cloud-Abhängigkeit und fehlende deterministische Dateisystem-/SQLite-Steuerung bei proprietären Agent-Frameworks",
            "Mangelnde Nachvollziehbarkeit, fehlende Audit-Trails und unkoordinierte parallele Zugriffe mehrerer Agenten",
        ],
        "usecases": [
            "Persistentes lokales Agenten-Betriebssystem mit CLI-, API- und MCP-Schnittstelle",
            "Zentrale Koordination von Tasks, Skills, Memory und Wissen für Claude, Codex, Gemini und Ollama",
            "Nachvollziehbare Local-First-Automatisierung ohne Cloud-Lock-in",
        ],
        "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/AI_Agents", "Reddit r/ClaudeAI", "GitHub Discussions"],
        "search_keywords": [
            "local agent operating system sqlite memory",
            "persistent cli runtime for coding agents",
            "local first multi agent host open source",
        ],
    },
    "ellmos-ai/open-ocean": {
        "summary": "open-ocean: Local-first, verifizierbarer Kompositions-Installer mit Rollback-Lifecycle, der komplette KI-Agenten-Systeme aus deklarativen Rezepten und Bundles zusammensetzt — das freie Community-Gesamtsystem des ellmos-Ökosystems.",
        "problems_solved": [
            "Komplexe lokale Multi-Agenten-Setups lassen sich schwer reproduzierbar installieren, verifizieren und bei Fehlern sauber zurückrollen",
            "Fragmentierte Einzel-Tools, MCP-Server und Skills ohne deklarative Rezept- und Bundle-Komposition",
            "Intransparente Installer ohne kryptografische/deterministische Verifikation und Zero-Egress-Garantie",
        ],
        "usecases": [
            "Deklarative Zusammenstellung und Installation kompletter lokaler KI-Agenten-Umgebungen per Rezept",
            "Verifizierbare Updates und atomares Rollback für lokale Agent-Stacks",
            "Freies Community-Gesamtsystem des ellmos- und open-bricks-Ökosystems",
        ],
        "target_platforms": ["Reddit r/LocalLLaMA", "Reddit r/OpenSource", "Reddit r/AI_Agents", "GitHub Discussions"],
        "search_keywords": [
            "declarative installer for ai agent stack",
            "local first ai ecosystem recipe composer rollback",
            "open source agent system installer",
        ],
    },
    "ellmos-ai/skills": {
        "summary": "ellmos skills: Anbieterneutrale, portable SKILL.md-Bibliothek (140+ kuratierte öffentliche Skills mit CI-Quality-Gates, Katalog-CLI & JSON-Registry) für Claude Code, Codex, AGY/Gemini, BACH und lokale LLM-Workflows.",
        "problems_solved": [
            "Jeder Coding-Agent (Claude Code, Codex, Gemini/AGY) nutzt eigene Prompt-Ablagen statt einer gemeinsamen, geprüften SKILL.md-Bibliothek",
            "Ungetestete Community-Prompts ohne Frontmatter-Validierung, Sicherheits-Scanner und deterministische Begleitskripte",
            "Fehlender durchsuchbarer Katalog über Dev-, Infrastruktur-, Research- und Utility-Skills hinweg",
        ],
        "usecases": [
            "Gemeinsame portable Skill-Bibliothek für Claude Code, Codex, Gemini und lokale Agenten",
            "Einsatz geprüfter Standalone-Skills mit Python-Werkzeugen und CI-Vertragstests",
            "Browsen und Übernehmen einzelner SKILL.md-Pakete über Katalog-CLI oder Web-Katalog",
        ],
        "target_platforms": ["Reddit r/ClaudeAI", "Reddit r/ChatGPTCoding", "Reddit r/LocalLLaMA", "GitHub Discussions"],
        "search_keywords": [
            "portable SKILL.md library claude code codex",
            "shared agent skills repository open source",
            "reusable skills for coding agents",
        ],
    },
}

# Curated quality & idea scores for top module repositories (Tier 1 when low/medium attention <=6 views & unpromoted; Tier 2 when higher attention)
TOP_QUALITY_MODULE_SCORES = {
    "ellmos-ai/workflowhooker": 98,
    "doc-bricks/dokuzen": 98,
    "ellmos-ai/task-master": 97,
    "ellmos-ai/lock-master": 97,
    "dev-bricks/carecenter-for-codex": 96,
    "file-bricks/cloudlockfixer": 96,
    "ellmos-ai/decision-clicker": 94,
    "ellmos-ai/memoryhooker": 94,
    "ellmos-ai/usmc": 94,
    "ellmos-ai/hook-master": 93,
    "ellmos-ai/clirec": 93,
    "dev-bricks/codebox": 92,
    "file-bricks/explorerpro": 92,
    "ellmos-ai/clutch": 92,
    "file-bricks/softwarecenter": 91,
    "file-bricks/winstorepackager": 91,
    "file-bricks/promptboard": 91,
    "dev-bricks/methodenanalyser": 90,
    "doc-bricks/universaldocsgrabber": 90,
    "doc-bricks/universalinvoicemail": 89,
    "file-bricks/profiler": 89,
    "dev-bricks/devcenter": 89,
    "doc-bricks/mediabrain": 88,
    "doc-bricks/pdftopdfocr": 88,
    "file-bricks/sqliteviewer": 88,
    "ellmos-ai/swarm_ai": 88,
    "ellmos-ai/swarm-ai": 88,
    "ellmos-ai/rinnsal": 87,
    "ellmos-ai/compare-race": 87,
    "file-bricks/prosync": 86,
    "doc-bricks/litzentrum": 86,
    "ellmos-ai/doc-services": 86,
    "dev-bricks/safe-start-for-codex": 85,
    "ellmos-ai/anonymizer": 85,
    "ellmos-ai/coma": 85,
    "ellmos-ai/open-compute": 85,
    "ellmos-ai/sqlite-transit-sync": 85,
    "file-bricks/notespacellm": 85,
    "ellmos-ai/system-auditor": 84,
    "ellmos-ai/system-gap-master": 84,
    "ellmos-ai/marblerun": 84,
    "ellmos-ai/gardener": 84,
    "ellmos-ai/ai-media-editor": 84,
    "file-bricks/profiprompt": 84,
    "file-bricks/ampelclip": 84,
    "doc-bricks/cleanmarkdown": 84,
    "doc-bricks/dokureader": 84,
    "doc-bricks/universalmailcleaner": 83,
}


def compute_selection_tier(repo: Mapping[str, Any]) -> tuple[int, str, int]:
    """Classify a repository into the 3-stage outreach priority model (Nutzerentscheid 2026-11-09):
    - Tier 1: Best module repos by quality/idea with low-to-medium attention (views_unique_14d <= 6, unpromoted)
              PLUS core flagships (bach, open-ocean, skills) and standout skills (skills/*).
    - Tier 2: Best module repos by quality/idea that already have higher attention (views_unique_14d > 6 or already promoted).
    - Tier 3: Smaller repositories, specialty modules, seeds, and helper tools.
    """
    repo_id = str(repo.get("id", "")).strip().casefold()
    total_promotions = int(repo.get("total_promotions", 0))
    traffic = repo.get("traffic") or {}
    views_u = int(traffic.get("views_unique_14d", 0))

    if repo_id in CORE_ECOSYSTEM_FLAGSHIPS:
        base_q = CORE_ECOSYSTEM_FLAGSHIPS[repo_id]
        return 1, "tier1_core_flagship", base_q

    if repo_id.startswith("skills/"):
        base_q = 95
        if total_promotions == 0:
            return 1, "tier1_standout_skill", base_q
        return 2, "tier2_standout_skill_promoted", base_q

    if repo_id in TOP_QUALITY_MODULE_SCORES:
        base_q = TOP_QUALITY_MODULE_SCORES[repo_id]
        if total_promotions == 0 and views_u <= 6:
            return 1, "tier1_quality_low_medium_attention", base_q
        return 2, "tier2_quality_existing_attention", base_q

    return 3, "tier3_smaller_modules", 60


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
        repos = json.loads(registry_path.read_text(encoding="utf-8")).get("repos")
        return repos if isinstance(repos, dict) else {}
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

    # Check excluded organizations (e.g. biotec-line: legal/regulatory compliance exclusion)
    if org_lower in BLOCKED_ORGS or any(id_lower.startswith(f"{blocked}/") for blocked in BLOCKED_ORGS):
        return RepoClassification(is_active=False, reason="excluded_org_legal_compliance")

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

    # ellmos-ai/skills is promoted both as the general cross-agent skill library and via specific standout skills

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
    # a missing or broken source is not an empty snapshot: never deactivate or zero the catalog from it
    if not traffic_map or not registry_repos:
        missing = [
            n for n, ok in (("traffic_report.md", traffic_map), ("repo_registry.json", registry_repos)) if not ok
        ]
        return {"status": "error", "message": f"GitHubBot source missing, empty or unreadable: {', '.join(missing)}"}

    if not usecases_path.exists():
        return {"status": "error", "message": f"usecases.json not found at {usecases_path}"}

    usecases_data = json.loads(usecases_path.read_text(encoding="utf-8"))
    raw_existing_repos = usecases_data.get("repositories", [])
    # Remove any repositories belonging to permanently blocked organizations (e.g. biotec-line)
    existing_repos = [
        r
        for r in raw_existing_repos
        if str(r.get("org", "")).strip().casefold() not in BLOCKED_ORGS
        and not any(str(r.get("id", "")).strip().casefold().startswith(f"{b}/") for b in BLOCKED_ORGS)
    ]
    usecases_data["repositories"] = existing_repos
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
            org_norm = org.strip().casefold()
            if org_norm in DISCOURSE_ONLY_ORGS:
                repo["outreach_mode"] = "discourse_positioning"
                probs = repo.get("problems_solved") or []
                if any("Bedarf an einer leichtgewichtigen, lokalen Open-Source-Lösung" in str(p) for p in probs):
                    repo["problems_solved"] = [
                        f"Fachdiskussionen und aktuelle Tendenzen zum Forschungsthema von {name} identifizieren",
                        "Eigene wissenschaftliche Haltung, Methodik und Forschungsergebnisse sachlich in den Fachdiskurs einbringen",
                    ]
                    repo["usecases"] = [
                        "Wissenschaftlicher Themendiskurs & Positionsbestimmung (kein klassischer Tool-Pitch)",
                        f"Forschungsaustausch rund um {name}",
                    ]
            else:
                repo["outreach_mode"] = "solution_outreach"
            if key_id in CORE_FLAGSHIP_PROFILES:
                repo.update(CORE_FLAGSHIP_PROFILES[key_id])
            tf_score = repo["traffic"]["traffic_score"]
            sel_tier, sel_label, q_score = compute_selection_tier(repo)
            repo["selection_tier"] = sel_tier
            repo["selection_tier_label"] = sel_label
            repo["quality_score"] = q_score
            # High quality (Tier 1/2) or high interest tools get priority boost
            if sel_tier in (1, 2) or tf_score >= 80 or repo["traffic"]["clones_unique_14d"] >= 40:
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
            is_discourse = org.strip().casefold() in DISCOURSE_ONLY_ORGS

            new_repo = {
                "id": f"{org}/{name}",
                "org": org,
                "name": name,
                "url": f"https://github.com/{org}/{name}",
                "stars": gh_info.get("stars", 0),
                "summary": desc,
                "outreach_mode": "discourse_positioning" if is_discourse else "solution_outreach",
                "problems_solved": (
                    [
                        f"Fachdiskussionen und aktuelle Tendenzen zum Forschungsthema von {name} identifizieren",
                        "Eigene wissenschaftliche Haltung, Methodik und Forschungsergebnisse sachlich in den Fachdiskurs einbringen",
                    ]
                    if is_discourse
                    else [
                        f"Bedarf an einer leichtgewichtigen, lokalen Open-Source-Lösung für {name}",
                        f"Vermeidung von Cloud-Abhängigkeiten und Vendor-Lock-in im Bereich {org}",
                        "Fehlende flexible Automatisierung oder spezialisiertes Tooling für Entwickler",
                    ]
                ),
                "usecases": (
                    [
                        "Wissenschaftlicher Themendiskurs & Positionsbestimmung (kein klassischer Tool-Pitch)",
                        f"Forschungsaustausch rund um {name}",
                    ]
                    if is_discourse
                    else [
                        f"Einsatz im Bereich {org}",
                        f"Lokale Entwicklung und Automatisierung mit {name}",
                    ]
                ),
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
            if full_repo.casefold() in CORE_FLAGSHIP_PROFILES:
                new_repo.update(CORE_FLAGSHIP_PROFILES[full_repo.casefold()])
            sel_tier, sel_label, q_score = compute_selection_tier(new_repo)
            new_repo["selection_tier"] = sel_tier
            new_repo["selection_tier_label"] = sel_label
            new_repo["quality_score"] = q_score
            if sel_tier in (1, 2):
                new_repo["priority"] = "high"
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
            existing["traffic"] = {"updated_at": now_iso}  # GitHub measures no per-skill traffic
            existing["outreach_mode"] = "solution_outreach"
            sel_tier, sel_label, q_score = compute_selection_tier(existing)
            existing["selection_tier"] = sel_tier
            existing["selection_tier_label"] = sel_label
            existing["quality_score"] = q_score
            active_count += 1
        else:
            entry = dict(skill)
            entry["last_promoted_at"] = None
            entry["total_promotions"] = 0
            entry["active"] = True
            entry["exclusion_reason"] = None
            entry["outreach_mode"] = "solution_outreach"
            entry["github_meta"] = {"visibility": "public", "archived": False, "fork": False, "stars": 0}
            entry["traffic"] = dict(skill.get("traffic", {}))
            entry["traffic"]["updated_at"] = now_iso
            sel_tier, sel_label, q_score = compute_selection_tier(entry)
            entry["selection_tier"] = sel_tier
            entry["selection_tier_label"] = sel_label
            entry["quality_score"] = q_score
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

    # Both files change together or not at all: stage the JSON, write USECASES.md, then swap the JSON.
    md_path = usecases_path.parent / "USECASES.md"
    previous_md = md_path.read_bytes() if md_path.is_file() else None
    temp_path = usecases_path.with_name(f".{usecases_path.name}.{os.getpid()}.tmp")
    try:
        temp_path.write_text(json.dumps(usecases_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        export_usecases_markdown(usecases_data, md_path)
        try:
            temp_path.replace(usecases_path)
        except Exception:
            if previous_md is None:
                md_path.unlink(missing_ok=True)
            else:
                md_path.write_bytes(previous_md)
            raise
    except Exception as exc:
        logger.warning("Could not write the catalog: %s", exc)
        return {"status": "error", "message": f"catalog not written, nothing changed: {exc}"}
    finally:
        temp_path.unlink(missing_ok=True)

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
    if url.startswith("https://github.com/") and not any(c.isspace() or c in "<>()\"'`|" for c in url):
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
        tf_str = f"{clones_u} Clones / {views_u} Views (14d)" if "traffic_score" in tf else "nicht gemessen"
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
            if "traffic_score" in tf:  # skill profiles carry no measured traffic
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

    temp_path = output_path.with_name(f".{output_path.name}.{os.getpid()}.tmp")
    try:
        temp_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        temp_path.replace(output_path)
    finally:
        temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    workspace = Path(__file__).resolve().parent
    uc_path = workspace / "usecases.json"
    print(f"Syncing {uc_path} with GitHubBot...")
    res = sync_githubbot_traffic(uc_path)
    print(json.dumps(res, indent=2, ensure_ascii=False))
