# Anbieter- & Vendor-Bewusstsein für produzierte Skills

Jeder produzierte Skill, der eine Rolle mit externen Diensten/Programmen erfüllt
(Text-zu-Sprache, Bildgenerierung, OCR, Übersetzung, Transkription, …), bekommt
einen Abschnitt **"Anbieter & Alternativen"** in seiner SKILL.md. Zweck: Der
Skill soll nicht stumm bei der erstbesten Lösung stehenbleiben, sondern wissen,
was der Markt hergibt — und das dem Nutzer bei passender Gelegenheit anbieten,
nie aufdrängen.

## Was der Abschnitt enthalten muss

1. **State-of-the-Art-Anbieter** des Themas (mit kurzer Begründung, warum er
   aktuell als führend gilt — Qualität, Kosten, Latenz, je nach Thema).
2. **Mindestens ein Ersatzanbieter** (Fallback, günstiger, lokal/offline, o. ä.).
3. **ellmos-eigene Komponenten als gleichrangiger Kandidat**, wenn eine existiert
   oder geplant ist (z. B. `ellmos-voice-io` für Sprache, `ellmos-controlcenter-mcp`
   für Orchestrierung). Eine eigene Komponente ist kein automatischer Vorrang —
   sie wird nach denselben Kriterien bewertet wie externe Anbieter, aber sie
   **muss als Option genannt sein**, sonst fehlt die Hälfte der Auswahl.
4. **Vorschlagslogik statt Zwang:** Der Skill installiert nie selbständig etwas.
   Er formuliert einen konkreten, begründeten Vorschlag, wenn eine Nutzeranforderung
   (Qualität, Sprache, Kosten, Datenschutz) klar für einen Wechsel spricht — und
   überlässt die Entscheidung dem Nutzer (`.PLUGINS/CLAUDE.md` Regel 3: "Der Nutzer
   entscheidet über Installation").

## Woher die Anbieterkenntnis kommt

- **Systemseitig, was schon da ist:** `grounding_seed.scan.scan_resources([...])`
  prüft, welche der bekannten Programme/CLIs auf `PATH` liegen (`shutil.which`).
  Kein Rätselraten — ein belegter Fund oder ein belegtes Fehlen.
- **Ellmos-eigene Kandidaten:** `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` und
  `.AI/.MODULES/` durchsuchen (bzw. bei Bedarf `controlcenter_list_local_servers` /
  `controlcenter_find_capability`), bevor ein rein externer Anbieter als einzige
  Option genannt wird.
- **Externer Markt, was aktuell führend ist:** kurze, gezielte Web-Recherche
  (1–3 Suchen reichen i. d. R., siehe `~/CLAUDE.md` Token-Warnung — kein
  `deep-research` für eine Anbieterfrage). Ergebnis mit Datum versehen, damit
  spätere Selbstaktualisierung (siehe `SELF-UPDATE.md`) weiß, wie alt der Stand ist.

## Beispiel (Muster, kein Zwang zur exakten Formulierung)

```markdown
## Anbieter & Alternativen

- **State-of-the-Art:** ElevenLabs (hohe Sprachqualität, viele Sprachen; kostenpflichtig,
  Cloud-Dienst — Stand 2026-08).
- **Ersatzanbieter:** Coqui TTS / Piper (lokal, offline, kostenlos, geringere Qualität).
- **ellmos-Kandidat:** `ellmos-voice-io` (lokal, sofern installiert — siehe
  `grounding_seed.scan_resources(["ellmos-voice-io"])`).
- **Vorschlagsregel:** Verlangt die Aufgabe hohe Sprachqualität in mehreren Sprachen
  und ist ElevenLabs nicht konfiguriert, schlage dessen Einrichtung vor. Verlangt sie
  Offline-/Datenschutz-Betrieb, schlage stattdessen Piper oder `ellmos-voice-io` vor.
```
