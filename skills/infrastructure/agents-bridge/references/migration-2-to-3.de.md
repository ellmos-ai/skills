# Migration von agents-bridge 2.x auf 3.0

Version 3 erweitert den bisherigen Boot-Loader-Vertrag zu einem portablen,
reversiblen Instanzpaket. Die alten Befehle `discover --project` und
`render --truth` bleiben als read-only Kompatibilität erhalten; sie erzeugen
noch kein v3-Profil.

## Vorgehen

1. Führe `discover --root <instanz>` aus und löse fehlende oder konkurrierende
   Autorität explizit. Setze genau einen Marker erst nach dieser Entscheidung.
2. Übertrage das alte `truth_sources`-Profil in
   `assets/bridge-profile.example.json`. Ergänze jede Anbieterfläche und alle
   Pointerkanten. Wähle die Hauptfläche bewusst; `CLAUDE.md` ist kein Default.
3. Lege den gemeinsamen Memory-Index und getrennte Silos mit Owner-/Zugriffs-
   und Merge-Regeln fest. Bestehende Silos werden nicht zusammengeführt.
4. Lege relative Roots für Messenger, Presence und Locks sowie Privacy-Includes
   und -Excludes fest.
5. Validiere und erfasse zuerst in ein neues Paket. Persönliche Inhalte bleiben
   lokal; veröffentliche nur synthetische oder redigierte Fixtures.
6. Prüfe `doctor` und `plan`, teste Restore auf einem leeren Ziel, `verify`,
   idempotenten zweiten Restore und `rollback`.
7. Ersetze installierte Kopien erst nach grünem kanonischem Release über den
   normalen Skill-Verteilweg.

## Inkompatibilitäten

- Profilschema ist jetzt `agents-bridge.profile.v3`.
- Absolute Profilpfade und nicht UTF-8-kodierte Inhalte sind unzulässig.
- Genau eine Hauptfläche muss als `primary` abgebildet sein.
- Projektionen benötigen Provenienz und Hashes; unmarkierte Kopien gelten nicht
  als gültige Projektion.
- Restore-Mutationen benötigen explizites `--apply --yes`, Backup-Verzeichnis
  und Receipt-Pfad.
