# Rollen & Workflows — ausführliche Beschreibungen

Generisches Rollenmodell für (Roblox-)Spieleentwicklung. Eine Person oder ein Agent kann
mehrere Rollen übernehmen; entscheidend ist, dass die **Teilaufgaben** abgedeckt und
Entwicklung/Test getrennt sind.

---

## Entwicklungs-Rollen

### Creative Director — WAS, WARUM, für WEN
- Game Design Document (KONZEPT.md) schreiben und pflegen.
- Spielmechaniken entwerfen und balancen.
- Roadmap/Backlog priorisieren, Sprints planen.
- Story, Lore, Dialoge, Rollen verfassen.
- UX-Flow definieren: Onboarding, Spieler-Journey, Retention.
- Feature-Wünsche zu umsetzbaren Spezifikationen konkretisieren.
- *Fähigkeiten:* Game Design, Mechanik-Entwurf, Balancing, Story, Produktion, Priorisierung, UX.

### Engineer — WIE (technisch gebaut)
- Backend: Server-Scripts, Manager-Module, Game-Loop, Persistenz.
- Client: Input, State-Sync, Event-Handling.
- GUI-Code: HUD-Aufbau, Heartbeat-Loop, Benachrichtigungen.
- DevOps: Rojo-Config, Build-System, MCP-Anbindung, Deployment.
- Bugfixing nach Tester-Feedback.
- *Fähigkeiten:* Luau (Server/Client), Rojo, Netzwerk/Remotes, Datenbank, GUI-Code, Build.

### Artist — wie die Welt aussieht
- Prozedurale oder handgebaute Welt-/Level-Generierung.
- Atmosphäre, Beleuchtung, Farbpaletten.
- Partikel-Effekte (Feuer, Rauch, Magie, Wetter).
- Level-Design: Raum-Layouts, Spielflächen, Sichtlinien.
- Asset-Scout: Creator Store durchsuchen, **auf Malware prüfen**, bereinigen, einbinden, recyceln.
- *Fähigkeiten:* Level-Layout, Partikel, Beleuchtung, Atmosphäre, Asset-Beschaffung & -Bereinigung.

### Polish / Audio — wie es sich anfühlt und klingt
- Sound-Effekte und Ambient-Soundscapes.
- Animationen: Bewegung, Kampf, Idle, Emotes.
- UI/UX-Feinschliff: Layout, Farbschema, Lesbarkeit, Accessibility.
- "Juice": Screen-Shake, Slow-Motion, Hit-Stop, Treffer-Feedback.
- Feedback-Systeme (visuell + Audio bei jeder Aktion), Tutorial/Onboarding-Umsetzung.
- *Fähigkeiten:* SFX/Musik/Ambient, Animation, UI/UX, Juice/Polish, Spieler-Feedback.

### Business — nach außen
- Store-Beschreibung + Tags, Icon/Thumbnail.
- Monetarisierung: Gamepasses, Developer Products, Battle-Pass-Seasons.
- Analytics auswerten (Retention, Monetarisierung, Spielzeit), Konkurrenzanalyse.
- Social Media / DevLog, Community-Management.
- *Fähigkeiten:* Store-Page, Thumbnails, Monetarisierungs-Design, Analytics, Community.

## Test-Rollen (streng von Entwicklung getrennt)

### QA-Tester — ist es technisch korrekt?
- Bug-Scans: Code lesen, Logikfehler, API-Missbrauch.
- Playtests: Features durchklicken, Console prüfen.
- Reproduzierbare Bug-Reports schreiben.
- Regressionstests nach Fixes.
- Performance-Checks (Part-Count, Lag, Memory).

### Spielkritiker — macht es Spaß?
- Bewertung aus reiner Spielerperspektive: Ist es FUN? Verständlich? Fair?
- First-Impression-Review (erste 5 Min) und Long-Term-Review (nach 30–60 Min).
- Dimensionen: Gameplay, Grafik, Sound, Wiederspielwert, Monetarisierung.
- Konkrete, priorisierte Verbesserungsvorschläge — darf hart und ehrlich sein.

---

## Chains (Reihenfolgen)

| Chain | Ablauf | Zweck |
| --- | --- | --- |
| Standard-Feature | CreativeDir → Engineer → Artist → Polish → QA → Spielkritiker → CreativeDir | neues Feature end-to-end |
| Quick-Fix | QA → Engineer → QA | gemeldeten Bug schließen |
| Asset | Artist (Suche) → Artist (Malware-Scan) → Artist (Einbinden) → QA (visuell) | Store-Asset sicher integrieren |
| Polish | Spielkritiker → Polish → Artist → Spielkritiker | Spielgefühl verbessern |
| Mensch-im-Loop | [Agenten-Chain] → Mensch-Tester → CreativeDir → [Chain] | Qualitäts-Gate durch Menschen |

**Regeln über allen Chains:**
1. Entwicklung und Test sind immer verschiedene Akteure.
2. Persona-Tests laufen blind (Tester kennt die Design-Absicht nicht).
3. Der Spielkritiker ist ehrlich und hart, nicht gefällig.
4. Der Artist prüft eingebrachte Assets **immer** auf Malware.
5. Abbruch: Zeitbudget erreicht oder Qualitätsziel erfüllt.
6. Jede Iteration erzeugt ein Changelog + kurzen Testbericht.

---

## Persona-Achsen für Blind-Playtests

Variiere die Test-Personas entlang dieser Achsen, um die reale Spielerbreite abzudecken:
Alter · Geschlecht · Gaming-Erfahrung (Casual/Core/Hardcore) · Plattform (PC/Mobile/Tablet/Konsole)
· Interessen/Genre-Vorlieben · Aufmerksamkeitsspanne · Sprache · Zugänglichkeit (Sehkraft, Motorik)
· Sozialtyp (Solo/Coop/Kompetitiv). Drei kontrastierende Personas pro Test reichen meist, um
Verständlichkeits- und Fairness-Probleme früh zu finden.
