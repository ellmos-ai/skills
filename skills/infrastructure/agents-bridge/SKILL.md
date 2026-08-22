---
name: agents-bridge
version: 3.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-07-04
updated: 2026-08-22
description: Portable, provider-neutral file bridge for bootstrap surfaces, truth pointers, separate memory silos, messaging, presence, cooperative locks, and reversible host recovery.

standalone: true
anthropic_compatible: true
category: infrastructure
tags: [multi-agent, bootstrap, recovery, messaging, memory, provider-neutral]
language: de
status: active
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
---

<img src="banner.png" width="100%" alt="agents-bridge banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


# AGENTS-BRIDGE (Deutsch)

Nutze diesen Skill, um ein kleines dateibasiertes Multi-Provider-System zu
erfassen, zu prüfen, zu übertragen oder wiederherzustellen. Pro Instanz gibt es
genau eine ausdrücklich gewählte Hauptanbieterdatei. Kein Anbieter, Dateiname,
Host oder Cloud-Verzeichnis ist implizit kanonisch.

## Workflow & Vorgehen

1. Lies alle lokalen Anweisungen, Locks und Datenschutzregeln für Quelle und
   Ziel. Bewahre fremde Änderungen.
2. Führe `python scripts/bridge.py discover --root <instanz>` aus. `discover`
   darf nur einen eindeutigen Marker `agents-bridge-primary: true` übernehmen.
   Bei keinem oder mehreren Claims stoppt der Workflow mit einem
   Decision-Briefing; es gibt keinen Dateinamen-Default.
3. Lege ein Profil gemäß `references/profile-v3.schema.json` an. Es benennt
   Hauptfläche, Anbieterflächen, Wahrheitsquellen, Pointergraph, Recovery,
   Memory-Silos, Messenger, Presence, Locks sowie Privacy-Includes/-Excludes.
4. Prüfe das Profil und erfasse die Instanz ohne Quellmutation:

   ```text
   python scripts/bridge.py profile-validate --profile <profil.json>
   python scripts/bridge.py capture --profile <profil.json> --root <quelle> --output <neues-paket>
   ```

5. Prüfe das Paket mit `doctor` und erzeuge mit `plan` oder `restore` ohne
   `--apply` eine Vorschau. Bestehende Dateien werden nie blind überschrieben.
6. Wende den Restore erst nach Prüfung mit `--apply --yes --backup-dir
   <backup> --receipt <receipt.json>` an. Danach folgen `verify` und ein echter
   nativer Lesetest für Claude, Codex/GPT, Gemini oder den neutralen Anbieter.
7. Bei Fehlern: Drift klären oder den exakten Receipt mit `rollback --yes`
   zurückrollen. Ein zweiter Restore muss `idempotent` melden.
8. Nutze `message send|ack|status`, `memory`, `presence` und
   `lock claim|release|status` nur als kleine Dateiverträge. Messenger ersetzt
   weder Ticket-Master noch Scheduler; Memory-Silos werden nie automatisch
   zusammengeführt.

## Sicherheitsgrenzen

- Ein Loader oder Redirect ist bevorzugt. Eine Projektion ist nur zulässig,
  wenn native Referenzen nicht funktionieren; sie enthält Quellhashes,
  Provenienz, `generated_at` und eine Driftkennung. Kontrollierte Regeneration
  erfolgt nur in ein neues Paket mit `capture --regenerate-projections`.
- Alle Profilpfade sind UTF-8-kodiert, relativ und plattformneutral. Exporte
  sind manifestiert und auf Includes/Excludes begrenzt.
- Secrets, Credentials und persönliche absolute Pfade werden fail closed
  abgewiesen oder bei explizitem `redact`-Modus protokolliert ersetzt.
- Bei vorhandenem Controlroom bleibt dieser Koordinationsautorität.
  `agents-bridge` ist dann ausschließlich Bootstrap-, Recovery- und
  Dateiadapter und dupliziert keine zentrale Runtime.

Verträge und Beispiele stehen in `references/contracts.de.md`,
`references/truth-topologies.md`, `references/inventory-contract.md` und
`references/migration-2-to-3.de.md`. Die englische Fassung ist `SKILL.en.md`.
