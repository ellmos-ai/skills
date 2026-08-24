# Selbstaktualisierung für produzierte Skills

Ein Skill, der einmal gebaut und nie wieder angeschaut wird, veraltet lautlos —
neue Anbieter entstehen, bessere Alternativ-Skills/Workflows tauchen auf, alte
Annahmen stimmen nicht mehr. Jeder produzierte Skill bekommt deshalb einen
Abschnitt **"Selbstaktualisierung"**, gesteuert von drei Kräften zugleich:
**Modell** (das den Skill gerade ausführt), **Nutzer** (der Feedback gibt) und
**mitgelieferte Speicher-JSONs** (die das zwischen Läufen festhalten).

## Was der Abschnitt enthalten muss

1. **Periodischer Web-Recherche-Vorschlag:** kein automatischer Hintergrundlauf
   (das wäre eine unbeaufsichtigte Massenautomation, siehe `~/CLAUDE.md`
   "24-Stunden-Protokoll"), sondern ein **Vorschlag im laufenden Gespräch**, wenn
   der letzte Update-Check (siehe `letzter_check` in der Lern-JSON) älter als eine
   sinnvolle Frist ist (Richtwert: 30–90 Tage, themenabhängig — ein TTS-Anbietermarkt
   bewegt sich schneller als ein Steuerformular).
2. **Alternativen-Kenntnis:** der Skill kennt verwandte eigene Skills/Workflows
   (`skill-finder`/`controlcenter_find_skill` befragen) und benennt explizit, wenn
   einer davon für den konkreten Fall besser passen könnte als er selbst — das ist
   kein Makel, sondern korrektes Routing.
3. **Lern-JSON statt Gedächtnisverlust:** Erkenntnisse aus Nutzerfeedback und
   Recherchen werden **strukturiert** festgehalten (Vorlage:
   `../templates/skill-connections.template.json`, Feld `gelernt`), nicht nur im
   Fließtext der SKILL.md verstreut. Jeder Eintrag trägt Datum + Quelle.
4. **Auslagerbar, wenn vorhanden:** Ist eine ellmos-Memory-Komponente da (USMC,
   Gardener), wird dorthin geschrieben (`usmc lesson`/`usmc fact` bzw. Gardener
   `put(..., type="memory")`) statt die lokale JSON unbegrenzt wachsen zu lassen —
   erkannt über dasselbe `try/except`-Muster wie in `ELLMOS-PRINCIPLES.md`. Ist
   nichts vorhanden, bleibt die lokale JSON die alleinige Quelle — das ist der
   "allein lauffähig"-Fall, kein Fehler.

## Muster (kurz)

```markdown
## Selbstaktualisierung

- Letzter Anbieter-Check: siehe `connections.json` -> `gelernt[-1].datum`.
  Älter als 60 Tage? Vor der nächsten Ausführung eine kurze Websuche vorschlagen
  ("Gilt <Anbieter X> noch als Referenz für <Thema>, oder gibt es Neueres?").
- Verwandte Skills: `skill-finder` fragen, ob es inzwischen einen passenderen
  Skill gibt, bevor dieser hier stur weiterläuft.
- Neue Erkenntnis? In `connections.json` unter `gelernt` anhängen
  (`{"datum": "...", "quelle": "...", "erkenntnis": "..."}`), bei vorhandener
  ellmos-Memory-Komponente zusätzlich dorthin auslagern.
```

## Warum kein eigener Scheduler

Dieser Abschnitt beschreibt **wie der Skill sich selbst prüft, wenn er läuft**,
nicht **wann er automatisch läuft**. Ein eigener Cron-/Scheduler-Mechanismus pro
Skill wäre eine Wildwuchs-Automation ohne zentrale Aufsicht — dafür existieren
bereits `ellmos-scheduler`/Loop-Werkzeuge (`workflow-extract`-Skill). Ein
produzierter Skill schlägt seine Aktualisierung vor, er terminiert sie nicht selbst.
