# <Spielname> — KONZEPT (Game Design Document)

## Vision
<1–2 Sätze: Was ist das Spiel, und warum spielt man es?>

## Genre / Vorbild
<z. B. Sci-Fi Base Builder; Vorbild: Clash of Clans im Alien-Setting>

## Zielgruppe
<Alter, Plattform-Schwerpunkt (Mobile/PC), Spielertyp>

## Kern-Mechaniken (max. 3–4)
1.
2.
3.

## Gameplay-Loop
<Was tut der Spieler Minute für Minute? Welche Schleife hält ihn dabei?>

## Spielmodi / Zeitformate
<falls relevant — z. B. Classic / Ranked / Creative; Bullet / Blitz / Rapid>

## USP
<Was macht dieses Spiel anders/besser als bestehende im Genre?>

## Monetarisierung
- Gamepasses:
- Developer Products:
- Battle Pass / Seasons:
- Shop / UGC:
<Regel: Monetarisierung soll Gameplay unterstützen, nicht blockieren.>

## Technik / Architektur
- Stack: Rojo / rokit (Rojo, Lune, Wally), Framework (z. B. Knit)
- Mapping: flach | verschachtelt
- Grobe Code-Struktur: shared (Config, GameEnums, *Defs) · server (Main + *Manager) · client · gui

## Live-Ops-Plan
<Update-Rhythmus (Ziel: alle 2–4 Wochen), geplante Events/Seasons>

## Nächste Schritte
- [ ] Backend: Config → GameEnums → *Defs → Main.server → *Manager
- [ ] Frontend: GameClient → HUD
- [ ] Greybox-Playtest (Gameplay zuerst)
- [ ] Asset-Upgrade (Creator Store, Malware-Scan)
- [ ] Persona-Blindtests
- [ ] Store-Seite + Monetarisierung

## Bekannte Bugs / Offene Punkte
-
