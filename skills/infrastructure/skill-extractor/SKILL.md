---
name: skill-extractor
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
description: >
  Extrahiert aus einem Chatverlauf (aktuelle Session oder Transkript-Dateien) einen
  wiederverwendbaren Skill — oder verbessert einen sehr ähnlichen existierenden Skill,
  statt ein Duplikat zu erzeugen. Nutze diesen Skill bei „mach daraus einen Skill",
  „das sollten wir als Skill festhalten", „extrahiere Skills aus diesem/alten Chatverläufen",
  „diese Arbeitsweise wiederverwendbar machen", oder bei `/skill-extract`. Deckt auch
  Bulk-Läufe über viele alte Transkripte ab (mit Datenreduktion über Subagenten).
  Für wiederkehrende AUTOMATISIERUNGEN (Cron/Schedule/Loop) stattdessen den
  Schwester-Skill workflow-extract nutzen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, extraction, transcript, chatverlauf, meta, dedup, neutralisierung, workflow]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Skill-Extractor — aus Chatverläufen Skills gewinnen

## Zweck

Wertvolle Arbeitsweisen entstehen in Sessions: Ein Problem wurde mühsam gelöst, der User hat
mehrfach korrigiert, am Ende steht ein funktionierender Ablauf — und beim nächsten Mal fängt
der Agent wieder bei null an. Dieser Skill destilliert aus einem Chatverlauf das, was sich zu
konservieren lohnt, und macht daraus einen Skill nach den Konventionen der lokalen
Skill-Bibliothek. Kernprinzip: **Erweitern vor Neuanlegen** — existiert ein sehr ähnlicher
Skill, wird der verbessert statt ein Duplikat erzeugt.

Abgrenzung: Ergebnis ist hier ein **abrufbarer Skill** (Fähigkeit/Verfahren, das ein Agent bei
Bedarf lädt). Soll aus dem Verlauf eine **selbstlaufende Automatisierung** werden (wiederkehrender
Prompt, Cron, Schedule), den Schwester-Skill `workflow-extract` nutzen.

## Ablauf

### 1. Quelle bestimmen

Drei Eingabeformen:

| Quelle | Zugang |
| --- | --- |
| **Aktuelle Session** | Konversationskontext direkt nutzen — keine Dateien nötig |
| **Einzelne Transkripte** | Dateien lesen; Fundorte und Parsing: `transcript-quellen.md` |
| **Bulk (viele alte Verläufe)** | Erst Datenreduktion über Subagenten, dann Extraktion: Abschnitt „Bulk-Modus" |

### 2. Extraktionswürdiges finden

Nicht jede Session enthält einen Skill. Suche nach diesen Signalen — sie zeigen, wo Wissen
steckt, das teuer erworben wurde und wieder gebraucht wird:

- **Wiederholung:** Derselbe Ablauf kam ≥2-mal vor (in dieser oder über mehrere Sessions).
- **Korrekturschleifen:** Der User hat den Agenten mehrfach nachjustiert, bis es stimmte —
  die Endfassung ist das Destillat, die Korrekturen sind die Begründungen („warum so").
- **Explizite Marker:** „merk dir das", „so machen wir das immer", „beim nächsten Mal direkt so".
- **Werkzeugketten:** Eine nicht-offensichtliche Abfolge von Tools/Befehlen, die funktioniert hat
  (inklusive der Sackgassen, die vermieden werden sollen).
- **Entscheidungsregeln:** Kriterien, nach denen zwischen Alternativen gewählt wurde.

Halte pro Kandidat fest: Auslöser (wann braucht man das), Ablauf (Schritte), Begründungen
(warum so und nicht anders), Fallstricke (was schiefging), Ergebnisform.

### 3. Dedup-Gate: Erweitern vor Neuanlegen

Bevor irgendetwas geschrieben wird, die bestehende Landschaft prüfen:

1. Kandidaten-Stichwörter gegen die Skill-Verzeichnisse suchen (Deployment-Ordner des Agenten,
   z. B. `~/.claude/skills/`, und — falls vorhanden — die kuratierte Skill-Bibliothek als Quelle
   der Wahrheit; ebenso registrierte Plugin-Skills).
2. Die 2–3 nächstliegenden Skills wirklich **lesen**, nicht nur Namen vergleichen.
3. Entscheiden:

| Befund | Aktion |
| --- | --- |
| Kandidat ist im Kern schon abgedeckt | **Erweitern:** fehlende Elemente in den bestehenden Skill einarbeiten (neue Sektion, neue Technik, neuer Fallstrick), Version MINOR erhöhen, Changelog-Eintrag |
| Teilüberlappung, aber anderer Kern | **Neuer Skill** mit Querverweis („Verwandte Skills") auf die Nachbarn — keine Inhalte duplizieren, sondern verweisen |
| Nichts Vergleichbares | **Neuer Skill** |

Faustregel: Wenn mehr als die Hälfte des Kandidaten in einem bestehenden Skill steckt, wird
erweitert. Ein Skill-Bestand voller Fast-Zwillinge ist schlechter als ein gepflegter Skill.

### 4. Neutralisieren

Der Rohstoff ist voller session-spezifischer Details. Vor dem Schreiben nach den Regeln in
`neutralisierung.md` abstrahieren: Mechanik (allgemeingültig) von Konfiguration (user-/system-
spezifisch) trennen, konkrete Pfade/Hosts/Namen durch Platzhalter oder einen klar markierten
Konfigurationsblock ersetzen. Ziel: Der Skill funktioniert für andere User, andere Systeme,
andere Projekte.

### 5. Skill schreiben

- **Format:** Konventionen der Ziel-Bibliothek beachten (Frontmatter, Namensschema, Sprache,
  Changelog). In dieser Bibliothek: `docs/CONVENTIONS.md` (vollständiger YAML-Header,
  kebab-case-Name, Deutsch primär, Semantic Versioning).
- **Description „pushy" formulieren:** Die description ist der Trigger-Mechanismus. Sowohl WAS
  der Skill tut als auch WANN er greifen soll (typische User-Formulierungen) hineinschreiben —
  Skills werden eher zu selten als zu oft ausgelöst.
- **Warum vor Was:** Begründungen aus den Korrekturschleifen in den Skill übernehmen. Ein Skill,
  der nur Schritte auflistet, wird beim ersten Sonderfall falsch angewandt; einer, der erklärt
  warum, lässt sich übertragen.
- **Fallstricke dokumentieren:** Die Sackgassen aus der Session sind Gold — als „Red Flags"- oder
  „Fallstricke"-Abschnitt aufnehmen.
- **Schlank halten:** Unter ~300 Zeilen; Detailmaterial in Referenzdateien auslagern, auf die die
  SKILL.md verweist.

### 6. Command-Wrapper (optional)

Wenn der Skill regelmäßig direkt aufgerufen werden soll, einen Slash-Command anlegen (bei
Claude Code: kurze Markdown-Datei in `~/.claude/commands/<name>.md`, die auf den Skill zeigt
und Argumente durchreicht). Konvention: Command = dünner Einstieg, Inhalt lebt im Skill.

### 7. Registrieren und testen

- In der Bibliothek ablegen (richtige Kategorie) und ins Deployment ausrollen (hier:
  `python skill_sync.py deploy <name>` — Erstinstallation braucht den expliziten Namen).
- Trigger-Test: 2–3 realistische Prompts formulieren, die den Skill auslösen sollten, und prüfen,
  ob die description greift.
- Für einen vollen Eval-Loop (Testfälle, Baseline-Vergleich, Beschreibungs-Optimierung) den
  `skill-creator` nutzen, falls installiert — dieser Skill hier ist der Extraktor, nicht das Testlabor.
- Index-/Routing-Pflege: Skill-Finder-/Index-Skills aktualisieren, falls vorhanden
  (hier: `code-skill-index`, `skill-finder`-Routing-Tabelle).

## Bulk-Modus: viele alte Chatverläufe

Transkripte sind groß (oft >100k Tokens); niemals alle roh in einen Kontext laden.
Map-Reduce über Subagenten (Muster: `swarm-operations`-Skill, Aufgabenschwarm):

1. **Inventar:** Transkript-Dateien auflisten (Fundorte: `transcript-quellen.md`), nach Projekt/
   Zeitraum bündeln. Bei sehr großen Beständen zuerst mit vorhandenen Kollektoren/Extraktoren
   reduzieren (z. B. Prompt-Listener-/Studien-Datensätze, die nur User-Prompts enthalten) —
   User-Prompts + Korrekturen tragen das meiste Signal.
2. **Map:** Pro Bündel ein Subagent mit engem Auftrag: „Lies diese Transkripte, melde
   Skill-Kandidaten als Kompaktliste (Auslöser, Ablauf, Begründungen, Fallstricke, Beleg-Session)"
   — nur die Destillate zurückgeben, nie Rohtext.
3. **Reduce:** Kandidatenlisten zusammenführen, clustern, Duplikate mergen. Häufigkeit zählt:
   Ein Muster, das in 5 Sessions auftaucht, ist ein stärkerer Kandidat als ein einmaliger Trick.
4. **Gate + Bau:** Für die Top-Kandidaten Schritte 3–7 des Normalablaufs durchlaufen.
   Dem User vor dem Massenbau eine nummerierte Kandidatenliste zur Auswahl vorlegen —
   Bulk-Extraktion erzeugt sonst Skill-Müll.

## Beispiel

```text
User: „Wir haben jetzt dreimal PDF-Rechnungen nach demselben Schema geparst —
mach daraus einen Skill."

1. Quelle: aktuelle Session. Signal: Wiederholung (3×) + Korrektur („Beträge immer
   als Dezimalzahl mit Punkt, nicht Komma").
2. Dedup-Gate: Suche findet `pdf`-Skill (generisch, Erzeugung/Extraktion) — Kern
   überlappt nicht (hier: Rechnungs-Schema + Validierungsregeln) → neuer Skill
   `invoice-parsing` mit Querverweis auf `pdf`.
3. Neutralisieren: konkreter Ablageordner und Firmenname → Konfigurationsblock.
4. Skill schreiben: Schema-Tabelle, die Komma/Punkt-Korrektur als Fallstrick,
   Changelog 1.0.0. Trigger-Test mit „lies diese Rechnung ein".
```

## Red Flags

| Gedanke | Realität |
| --- | --- |
| „Ich lege schnell einen neuen Skill an" | Dedup-Gate zuerst — Erweitern vor Neuanlegen. |
| „Die Pfade lasse ich drin, ist ja für dieses System" | Neutralisieren ist Pflicht; Konkretes gehört in einen Konfigurationsblock. |
| „Der Verlauf ist lang, ich fasse aus dem Gedächtnis zusammen" | Signale (Korrekturen, Marker) gezielt heraussuchen — das Gedächtnis glättet genau die Stellen, die den Skill wertvoll machen. |
| „Jede Session ergibt einen Skill" | Ohne Wiederholungs-/Korrektur-/Marker-Signal: kein Skill. |

## Verwandte Skills

- `workflow-extract` — gleiche Extraktion, aber Ziel ist eine selbstlaufende Automatisierung.
- `skill-explorer` — Audit/Aufräumen der Skill-Landschaft (nutzt das Dedup-Gate in groß).
- `skill-creator` (Plugin) — Eval-Loop und Beschreibungs-Optimierung für fertige Skills.
- `swarm-operations` — Schwarm-Muster für den Bulk-Modus.

## Changelog

### 1.0.0 (2026-07-03)
- Initiale Version. Entstanden aus dem Auftrag, Codex-Automatisierungen und Chatverläufe
  systematisch zu Skills zu abstrahieren.
