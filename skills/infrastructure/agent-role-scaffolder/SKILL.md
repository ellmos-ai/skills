---
name: agent-role-scaffolder
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-25
updated: 2026-08-25
description: >
  Baut und prüft neue Agentenrollen im ellmos-Ökosystem: native Claude-Code-
  Subagenten (dauerhafte Rollendefinition) und Companion-Worker (SendMessage-
  wiederverwendete Instanz für eine Ticket-/Aufgabenserie). Formalisiert das
  bislang unformalisierte eigene Wissen aus dem laufenden Bau von Agentenrollen
  (ati-agent, bueroassistent, versicherungs-agent u. a.) zu einem
  wiederverwendbaren Scaffold-plus-Verify-Ablauf. Nutze diesen Skill, wenn eine
  neue Rolle entstehen soll ("neue Agentenrolle bauen", "Subagent anlegen",
  "Companion-Worker starten") oder eine bestehende gegen die Haus-Konventionen
  geprüft werden soll ("ist dieser Agent richtig aufgesetzt?").
visibility: public
language: de
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
---

# agent-role-scaffolder

<!-- FAMILY-ROUTER:Agenten-Orchestrierung START -->
> **Familie Agenten-Orchestrierung — Wegweiser:** Modell wählen/staffeln ->
> `model-strategy`; Orchestrierungsmuster wählen -> `choose-your-orchestrator`;
> Schwarmoperationen (5 Grundmuster + 2 Modi) -> `swarm-operations`; Aufgabe
> zerlegen/delegieren/abnehmen -> `orchestrator`; anbieterübergreifende
> Nachrichten/Presence/Locks -> `agents-bridge`; **eine neue Rolle bauen oder
> prüfen -> dieser Skill (agent-role-scaffolder)**.
<!-- FAMILY-ROUTER:Agenten-Orchestrierung END -->

## Zweck

Dieses Ökosystem hat bereits eine reife Familie von Orchestrierungs-Skills
(`model-strategy`, `swarm-operations`, `orchestrator`, `choose-your-orchestrator`,
`agents-bridge`) — aber **keinen davon für die Frage "wie entsteht eine neue
Rolle richtig".** Diese Lücke füllt `agent-role-scaffolder`. Er dupliziert die
genannten Skills nicht, sondern **routet zu ihnen**, sobald Staffelung,
Orchestrierungsmuster oder Cross-Provider-Messaging gebraucht werden.

**Herkunft:** User-Entscheid M5 aus Ticket `T-20260825-935905816`
(Marketplace-Vollsichtung): Verdikt (b) — eigenes Agenten-Bau-Wissen war
vorhanden, aber unformalisiert. Das offizielle Claude-Code-Plugin
`agent-sdk-dev` (claude-plugins-official, Apache-2.0) diente als
**strukturelles Vorbild**: eine scaffolding-Kommando-Datei plus zwei
themenspezifische Verifier-Subagenten mit Checkliste und einem
PASS/PASS-WITH-WARNINGS/FAIL-Berichtsformat. Übernommen wurde die **Form**
(Scaffold-Frage-Katalog → Aufbau → Verifikations-Checkliste mit
strukturiertem Bericht), nicht der Text und nicht der Gegenstand — jenes
Plugin baut rohe Claude-Agent-SDK-Apps (Python/TypeScript), dieser Skill
baut **ellmos-eigene Agentenrollen** (Subagent-Definitionen und
Companion-Worker). Das Original ist NICHT installiert; es liegt read-only im
lokalen Marketplace-Cache und wurde nur gelesen (`.PLUGINS/CLAUDE.md`
Regel 5: Ideen frei, Formulierungen nicht). Register-Eintrag:
`.AI/.PLUGINS/PLUGIN-REGISTER.md`, Status `zitiert`.

## Zwei Bauwege — beide gehören hierher

Im ellmos-Ökosystem entstehen neue Rollen auf zwei strukturell verschiedenen
Wegen, die nicht verwechselt werden dürfen (analog zur TS/Python-Trennung
des Vorbild-Plugins — hier aber entlang der tatsächlichen Systemgrenze):

| | **Nativer Subagent** | **Companion-Worker** |
|---|---|---|
| Was entsteht | eine dauerhafte Rollendefinition (`~/.claude/agents/<name>.md`, per `Agent`-Tool startbar) | eine ad-hoc benannte, per `SendMessage` wiederverwendete Instanz für EINE Aufgabenserie |
| Lebensdauer | dauerhaft, wiederverwendbar über Sitzungen hinweg | für die Dauer einer Ticket-/Themenserie, danach verworfen |
| Beispiele im Bestand | `ati-agent`, `bueroassistent`, `versicherungs-agent`, `gesundheitsassistent`, `persoenlicher-assistent`, `production`, `research-agent`, `reflection-agent`, `test-agent`, `entwickler-agent` | dieses Session-Modell selbst (z. B. `skillcreator-bau`, `policyreg-decisions`, `workflowhooker-ausbau` — benannte Worker im Ticket-System) |
| Lebenszyklus-Schicht | Claude-Code-eigene Agent-Registry | **COMA** (`.MODULES/.ORCHESTRATION/coma`) — sofern prozessübergreifend gestartet, nicht nur Tool-intern |
| Bauanleitung hier | `references/subagent-role-scaffold.md` | `references/companion-worker-scaffold.md` |

**Faustregel:** Braucht die Fähigkeit einen eigenen, über viele Sitzungen
hinweg wiederverwendbaren Namen mit fester Trigger-Beschreibung (z. B. „immer
wenn es um Steuerbelege geht") → nativer Subagent. Ist es eine begrenzte,
aber inhaltlich zusammenhängende Serie von Aufgaben, die ein Koordinator
gerade delegiert (Ticket-Kette, Themenwechsel) → Companion-Worker.

## Ablauf

1. **Bauweg wählen** (Tabelle oben) — im Zweifel den User fragen, nicht raten.
2. **Scaffold-Fragen durchgehen** (siehe passende `references/*.md`) — analog
   zum Vorbild-Plugin nacheinander, nicht alle auf einmal: Zweck/Auslöser,
   Werkzeugbedarf (`Tools:`), Modellwahl (→ **Schritt 3**), Koordinations-Bedarf
   (Boss-Agent mit Experten oder Einzelrolle?).
3. **Modellwahl NICHT hier entscheiden — an `model-strategy` delegieren.**
   Score-basierte Auswahl, Cross-Agent-Delegation, Advisor-Pairing,
   Eskalationstrigger sind dort bereits gelöst; hier nur der Verweis. Faustregel
   aus dem Bestand: Subagenten erben **nicht pauschal** das Hauptmodell (siehe
   Feedback-Memory `feedback_subagenten_modellstaffelung`).
4. **Orchestrierungsmuster prüfen**, falls die neue Rolle mit mehreren anderen
   zusammenarbeiten soll — `choose-your-orchestrator` wählt das Muster,
   `swarm-operations` liefert die 5 Grundmuster + 2 Modi, `orchestrator` das
   Zerlegen/Delegieren/Abnehmen-Protokoll.
5. **Team-/Messaging-Konventionen einhalten** (`references/
   model-staffing-and-messaging.md`): `SendMessage` für Cross-Agent-
   Kommunikation, Ticket-Claim-per-Dateiname bei Ticket-Delegation, „verweisen
   statt wiederholen" beim Beauftragen (zentrale Regeln nicht im Prompt
   nacherzählen, nur das Aufgabenspezifische).
6. **Verifizieren** — die passende Checkliste in der gewählten
   `references/*.md`-Datei abarbeiten, Bericht im Format
   `PASS / PASS MIT WARNUNGEN / FAIL` erstellen (Struktur siehe unten).
7. **Bei Bedarf katalogisieren** — eine dauerhafte neue Rolle gehört ins
   passende Register (`~/.claude/agents/`, ggf. Plugin-Bündelung); ein
   Companion-Worker braucht kein Register-Eintrag, nur eine klare erste
   Aufgabenübergabe.

## Verifikations-Berichtsformat (für beide Bauwege)

Struktur bewusst vom Vorbild-Plugin übernommen (Form, nicht Wortlaut) — vier
Abschnitte, knapp:

- **Status:** PASS | PASS MIT WARNUNGEN | FAIL
- **Kritische Punkte:** was die Rolle unbrauchbar macht (fehlende Trigger-
  Beschreibung, `Tools:` zu weit/zu eng, Modell nicht per `model-strategy`
  begründet, keine Abgrenzung zu einer bestehenden Rolle geprüft)
- **Warnungen:** suboptimal, aber funktionsfähig (z. B. Hauptmodell geerbt
  statt gestaffelt, kein Rotationskriterium für einen langlebigen
  Companion-Worker)
- **Bestandene Prüfungen + Empfehlungen:** was passt, was als Nächstes

## Verwandte Skills

- `model-strategy` — Modellwahl/-staffelung (Schritt 3, hier nur referenziert).
- `swarm-operations` — Schwarmmuster für Mehrfach-Rollen-Zusammenarbeit.
- `choose-your-orchestrator` — wählt das passende Orchestrierungsmuster.
- `orchestrator` — Protokoll für Zerlegen/Delegieren/Abnehmen.
- `agents-bridge` — Cross-Provider-Messaging/Presence/Locks, falls die neue
  Rolle über Claude Code hinaus mit Codex/Gemini/Kimi kommunizieren muss.
- `skill-explorer` — prüft, ob eine Fähigkeit schon existiert, BEVOR eine neue
  Rolle gebaut wird (Duplikatsvermeidung).

## Changelog

### 1.0.0 (2026-08-25)
- Erstfassung. Gebaut nach User-Entscheid M5 (`T-20260825-935905816`) über
  `ellmos-skill-creator`. Formalisiert Companion-Worker-Muster (Primärquelle:
  `_control-center/_TICKETS/README.md`, Abschnitt „Leitprinzip
  (Kontext-Ökonomie)"), COMA-Lebenszyklus (Primärquelle:
  `.MODULES/.ORCHESTRATION/coma/README.md`), und das beobachtete
  „Boss-Agent koordiniert Experten"-Muster bestehender Rollen. Routet bewusst
  zu `model-strategy`/`swarm-operations`/`orchestrator`/
  `choose-your-orchestrator`/`agents-bridge` statt sie zu duplizieren.
  Vorbild `agent-sdk-dev` (claude-plugins-official) NICHT installiert, nur
  gelesen und strukturell zitiert (`.PLUGINS/CLAUDE.md` Regel 5).
