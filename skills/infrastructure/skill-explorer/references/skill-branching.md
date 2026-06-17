# Branch-Mechanismus — Drittanbieter-/read-only-Skills anpassen

## Zweck / Wann branchen

Wenn ein Plugin-Skill oder importierter Drittanbieter-Skill angepasst werden soll, ist direktes
Editieren verboten (eiserne Regel „Survey ≠ Mutation"). Der **Branch** ist der sanktionierte Ausweg:
eine vollständige Kopie des Originals, die dann bearbeitet wird. Typische Anlässe:

- Trigger-Text auf eigene Projekte zuschneiden
- Ressourcenpfade auf lokale Verzeichnisse anpassen
- Verhalten in einem Schritt ändern, ohne das ursprüngliche Skill-Paket zu berühren

## Prinzip: copy-then-edit

Das Original bleibt **zu jeder Zeit unangetastet und read-only**. Alle Änderungen erfolgen
ausschließlich am Branch (der Kopie). Dadurch bleibt die eiserne Regel wahr — der Branch ist
kein Widerspruch, sondern die explizit vorgesehene Alternative.

## Namenskonvention

| Fall | Verzeichnisname |
|------|-----------------|
| Allgemeine Anpassung | `<original>-fork` (Default) |
| Thematisch benannter Grund | `<original>-<grund-in-kebab-case>` |

Beispiele: `deep-research-fork`, `skill-finder-roblox`.

## Ablauf

1. **Original-Verzeichnis kopieren** (inkl. `LICENSE`-Datei und aller Assets):
   ```bash
   cp -r ~/.claude/plugins/<plugin>/skills/<original>/ ~/.claude/skills/<original>-fork/
   ```
   Bei Skills aus einem externen Staging-Verzeichnis entsprechend anpassen.

2. **Branch-Frontmatter-Block setzen** (in der kopierten `SKILL.md`, im `provenance`-Abschnitt,
   die alten Felder ersetzen):
   ```yaml
   provenance:
     origin: "branch"
     branched_from: "<original-skill-name>"
     branch_source_path: "~/.claude/plugins/.../skills/<original>/"
     origin_repo: "<repo des originals oder null>"
     origin_version: "<version des originals zum branch-zeitpunkt oder null>"
     branch_date: "YYYY-MM-DD"
     branch_author: "<bearbeiter>"
     branch_reason: "<grund>"
     last_sync_from_origin: null
   ```

3. **Nur die Kopie anpassen** — SKILL.md, Skripte, Vorlagen nach Bedarf; das Original-Verzeichnis
   bleibt wie kopiert (nie zurückschreiben).

4. **Supersession — Original ablösen:** Damit nicht zwei nahezu identische Skills gleichzeitig laden
   und kollidieren, eine der folgenden Maßnahmen wählen:
   - **Deregistrierung:** Original-`SKILL.md` zu `CONTENT.md` umbenennen (die Runtime lädt nur
     `SKILL.md`; der Skill bleibt per Read-Tool nutzbar, feuert aber nicht mehr bei Trigger-Beschreibungen).
   - **Router umzeigen:** Falls ein Familien-Router existiert, diesen auf den Branch zeigen lassen
     (`inject_family_header.py` oder manuelle Anpassung der Routing-Tabelle).
   Welche Variante passt, hängt davon ab, ob das Original-Plugin als Datei zugänglich ist (dann
   Deregistrierung) oder nur über den Familien-Router gesteuert wird.

## Lizenz & Sichtbarkeit

- Die `LICENSE`-Datei des Originals **mit in den Branch kopieren und unverändert erhalten**.
  Attribution-Hinweise in Kommentaren oder `ATTRIBUTION.md` beibehalten.
- **Drittanbieter-Branches bleiben privat** — sie gehen nicht in die öffentliche `.AI/.SKILLS`-
  Library und werden nicht per `skill_sync.py` dorthin deployed. Dies ist konsistent mit der
  bestehenden Policy: „Drittanbieter-Code wird nicht in die Library gezogen" (vgl. `install-uninstall.md`).
- Nur rein user-authored Skills (kein Drittanbieter-Anteil) gehen in die Library.

## Upstream-Abgleich

Das Feld `last_sync_from_origin` im Branch-Frontmatter merkt, wann zuletzt gegen das Original
abgeglichen wurde. Bei Updates des Original-Skills:

1. Diff zwischen Original-Version-zum-Branch-Zeitpunkt und aktueller Original-Version erzeugen.
2. Relevante Upstream-Änderungen manuell in den Branch mergen/rebasen.
3. `last_sync_from_origin` auf das aktuelle Datum setzen.

Ein automatisches Rebase gibt es nicht — der Abgleich ist immer manuell und bewusst.

## Persistenz

Den Branch in `config.json` unter einem `branches`-Eintrag vermerken, damit `skill-explorer`
ihn bei Re-Runs kennt und keinen zweiten Branch anlegt (Idempotenz):

```json
"branches": {
  "<original>-fork": {
    "branched_from": "<original>",
    "branch_date": "YYYY-MM-DD",
    "branch_reason": "<grund>",
    "superseded_original": true
  }
}
```

Vorlage für das Frontmatter: `assets/branch-header.example.md`.
