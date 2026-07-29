---
name: headless
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-28
description: >
  Providerneutraler Modus für lange autonome Läufe: sichere Arbeit fortsetzen,
  Entscheidungen nach Evidenz und Konfidenz treffen und blockierte Punkte
  gebündelt zurückstellen, ohne neue Autorität zu erfinden.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [headless, autonomie, entscheidung, fortsetzung, checkpoint, autorität]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "local-agent-skills/headless/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Headless

## Zweck

Nutze diesen Skill, wenn die auftraggebende Person ausdrücklich einen längeren,
autonomen Lauf ohne laufende Rückfragen wünscht. Der Modus erhöht die
Ausdauer, nicht die Berechtigung.

Ein einzelner nicht ausführbarer Punkt darf unabhängige, sichere Restarbeit nicht
unnötig stoppen.

## Startbedingungen

Vor Beginn festhalten:

- konkretes Ziel und Erfolgskriterium,
- positiver und negativer Scope,
- verfügbare Zeit- oder Kostenbudgets,
- erlaubte Seiteneffekte,
- Projektregeln, Sperren und fremde Änderungen,
- Pfad oder Mechanismus für Checkpoints,
- optional ein zulässiges lokales Entscheidungsprofil.

Fehlt ein Entscheidungsprofil, werden nur explizite Regeln und sichere
Standardannahmen verwendet. Die Runtime darf keine Person imitieren.

## Entscheidungsstufen

| Stufe | Grundlage | Verhalten |
|---|---|---|
| hoch | explizite Regel oder mehrfach bestätigtes Muster | entscheiden; nur bei vorhandener Autorität ausführen |
| mittel | plausible, reversible Standardentscheidung | entscheiden, Annahme markieren, sicher fortsetzen |
| niedrig | neuartig, widersprüchlich oder ohne belastbaren Rahmen | nicht raten; zurückstellen oder eskalieren |

Konfidenz in die Entscheidung und Autorität zur Ausführung sind getrennte Achsen.

## Laufprotokoll

1. **Kontext laden.** Regeln, Zustand, Locks und Ziel prüfen.
2. **Arbeit zerlegen.** Unabhängige Pakete, Entscheidungspunkte und
   Freigabepunkte markieren. Werden mindestens zwei unabhängige Worker eingesetzt,
   das Auftrags- und Evidenzprotokoll des `orchestrator` anwenden, sofern es
   verfügbar ist.
3. **Sichere Arbeit ausführen.** Reversible, autorisierte Schritte fortsetzen.
4. **Entscheidungen behandeln.**
   - Mit zulässigem Profil: Verfahren des `decision-avatar` verwenden.
   - Ohne Profil: nur aus expliziten Projekt- oder Auftragsregeln ableiten.
5. **Nicht ausführbare Punkte parken.** Entscheidung oder Empfehlung festhalten,
   Ausführung aber nicht vorwegnehmen.
6. **Unabhängige Arbeit fortsetzen.** Ein geparkter Punkt blockiert nur seine
   echten Abhängigkeiten.
7. **Checkpoint schreiben.** Ziel, erledigte Schritte, Evidenz, Annahmen,
   geparkte Punkte und nächsten Schritt sichern.
8. **Abschluss prüfen.** Ergebnisse selbst verifizieren und offene Entscheidungen
   in einer kompakten Liste bündeln.

## Entscheidungsprotokoll

Für jede nicht triviale Annahme erfassen:

```text
ID:
Entscheidung:
Grundlage:
Konfidenz:
Ausgeführt: ja/nein
Evidenz:
Rücknahme oder Korrektur:
```

Agentenentscheidungen dürfen später nicht als Aussagen der auftraggebenden Person
behandelt werden.

## Paketlokale Stopps

Ein einzelnes Paket stoppen und parken, wenn es neue Autorität, eine irreversible
externe Aktion, unklare Regeln oder einen Konflikt benötigt. Danach prüfen, welche
anderen Pakete davon wirklich abhängig sind.

## Stop-Bedingungen des Gesamtlaufs

Der gesamte Lauf stoppt nur, wenn:

- keine sichere, unabhängige Arbeit mehr möglich ist,
- eine notwendige Entscheidung niedrige Konfidenz hat,
- alle verbleibenden Arbeitspakete neue externe oder irreversible Autorität
  erfordern,
- eine Sperre, ein Konflikt oder ein Sicherheitsrisiko den gesamten verbleibenden
  Scope betrifft,
- das vereinbarte Budget erreicht ist,
- der aktuelle Zustand nicht mehr zuverlässig gesichert werden kann.

## Abschlussformat

```text
Erreicht:
Verifiziert durch:
Annahmen:
Zurückgestellte Entscheidungen:
Nicht ausgeführte Seiteneffekte:
Nächster sinnvoller Schritt:
```

## Changelog

### 1.1.0 (2026-07-28)
- Persönliche Avatar-, Pfad-, Kommando- und Providerbindungen entfernt.
- Konfidenz und Ausführungsautorität getrennt.
- Fortsetzung unabhängiger Arbeit und gebündelte Eskalation präzisiert.
- Paketlokale Blocker ausdrücklich vom Stopp des Gesamtlaufs getrennt.

### 1.0.0 (2026-06-17)
- Lokale Ausgangsfassung.
