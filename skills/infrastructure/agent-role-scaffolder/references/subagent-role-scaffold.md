# Nativer Subagent — Scaffold + Verifikation

Bauweg für eine dauerhafte, über Sitzungen hinweg wiederverwendbare
Agentenrolle (Claude-Code-Agent-Registry, per `Agent`-Tool startbar).

## Beobachtetes Muster im Bestand

Die vorhandenen Rollen (`ati-agent`, `bueroassistent`, `gesundheitsassistent`,
`persoenlicher-assistent`, `versicherungs-agent`, `production`, `research-agent`,
`reflection-agent`, `test-agent`, `entwickler-agent`, u. a.) folgen erkennbar
zwei Kompositionsformen, keine dritte erfinden ohne Grund:

1. **Boss-Agent + Experten-Koordination.** Kurzformel in der Beschreibung:
   „Boss-Agent für <Domäne>. Nutze diesen Skill wenn: (1) ..., (2) ..., (3) ....
   Koordiniert Experten: <Rolle A>, <Rolle B>." Beispiel-Domänen im Bestand:
   Büro/Steuer (`bueroassistent` → Steuer-Agent, Förderplaner), Gesundheit
   (`gesundheitsassistent` → Gesundheitsverwalter, Psycho-Berater), Alltag
   (`persoenlicher-assistent` → Haushaltsmanagement). Dieses Muster passt,
   wenn eine Domäne mehrere Teilfähigkeiten hat, die eine Rolle bündelt statt
   sie einzeln aufzurufen.
2. **Einzelrolle mit klarer Alleinzuständigkeit.** Kurzformel: „<Funktion> für
   <System>." + Tools-Einschränkung. Beispiel: `reflection-agent`
   („Selbstreflexions-Agent für BACH. Analysiert Session-Performance ..."),
   `test-agent` („Systematisches Testen von BACH ... Orchestrator für Test-
   und Vergleichs-Workflows"). Passt, wenn die Rolle eine einzelne,
   abgrenzbare Verantwortung hat.

## Scaffold-Fragen (nacheinander, nicht alle auf einmal)

1. **Auslöser:** Bei welchen konkreten Formulierungen/Situationen soll diese
   Rolle greifen? Mindestens 2-3 Beispielsätze, wie im Bestand üblich (siehe
   `claude-code-guide`-Eintrag: „Can Claude...", „Does Claude...", „How do
   I..." als Auslöser-Beispiele in der Beschreibung selbst).
2. **Domäne oder Einzelfunktion?** Siehe die zwei Kompositionsformen oben —
   erst hier entscheiden, nicht vorher.
3. **Werkzeugbedarf (`Tools:`):** so eng wie möglich, so weit wie nötig.
   Beobachtete Werte im Bestand reichen von stark eingeschränkt (`bgb`:
   `Read, Grep` — reiner Textanalyse-Agent) bis `All tools` (Boss-Agenten mit
   Datei-/Prozess-Bedarf). **Nicht standardmäßig `All tools` vergeben** —
   das ist eine bewusste Entscheidung, keine Vorgabe.
4. **Modellwahl** — hier NICHT selbst entscheiden. Siehe
   `../references/model-staffing-and-messaging.md` bzw. den Skill
   `model-strategy` direkt. Score-basierte Auswahl, nicht raten.
5. **Abgrenzung prüfen:** Existiert schon eine Rolle mit ähnlichem Zuschnitt?
   `/skill-finder` bzw. `controlcenter_find_skill` befragen (Duplikat-
   Vermeidung, `.PLUGINS/CLAUDE.md` Regel 4 gilt sinngemäß auch für Rollen).

## Verifikations-Checkliste (Format siehe SKILL.md)

**Kritische Punkte (verhindern Funktion):**
- Beschreibung ohne konkrete Auslöser-Beispiele — die Rolle wird vom Router
  nie zuverlässig getroffen.
- `Tools:` fehlt oder ist widersprüchlich zur beschriebenen Aufgabe (z. B.
  eine Rolle, die schreiben soll, aber nur `Read` hat).
- Modellwahl weder begründet noch an `model-strategy` delegiert.
- Keine Abgrenzungsprüfung gegen bestehende Rollen durchgeführt.

**Warnungen (funktionsfähig, aber suboptimal):**
- `All tools` vergeben, obwohl die Aufgabe erkennbar enger ist.
- Boss-Agent-Muster gewählt, obwohl nur eine einzelne Teilfähigkeit gebraucht
  wird (unnötige Koordinationsebene).
- Keine Sprache/keine deutschen Umlaute in der Beschreibung, obwohl der
  Rest des Systems durchgängig Deutsch führt (Kern-Sprachregel).

**Bestandene Prüfungen:**
- Klare, mit Beispielen belegte Auslöser-Beschreibung.
- `Tools:` passend zum tatsächlichen Bedarf.
- Modellwahl über `model-strategy` begründet oder explizit dokumentiert,
  warum nicht.
- Abgrenzung gegen bestehende Rollen geprüft und im Bericht vermerkt.
