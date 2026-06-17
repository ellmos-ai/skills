# Familien-Pflege, Register-Handling & Registrierung

## Register-Handling (kein Duplikat anlegen!)

Ein Skill-Register existiert auf diesem System bereits in drei verzahnten Artefakten:

- `~/.claude/skills/code-skill-index/` — Kategorie-Kataloge (`references/catalog-*.md`).
- `<skill register: index>` — der versionierte Index (Master-Liste, je System ladbar).
- `<skill register: family/cross-reference map>` — die Quervergleichs-/Routing-Map (Familien + „welcher statt welchem").

**Default-Maßnahme = diese drei erweitern**, niemals ein viertes Register anlegen. Konkret bei
neuen/geänderten Familien:
- neue/aktualisierte Familie als Abschnitt in `the family map` ergänzen,
- neuen Skill als Zeile in `the skill index` (passender Index-Abschnitt) + Datum im Kopf,
- passenden `code-skill-index`-Katalog (`references/catalog-<kategorie>.md`) ergänzen.

Nur falls *gar kein* Register existierte (fremdes System), eines aus
`assets/skill-register-template.md` anlegen.

## Pflege-Subskill ausgründen (P1 / P2)

Auf Wunsch des Users wird ein eigenständiger Pflege-Skill erzeugt — ausgegründet aus diesem Skill,
damit die Pflege ohne den vollen Audit-Lauf möglich ist.

**P1 — Familien-Pflege** (`skill-family-care`):
- Zweck: hält die Familien aktuell — neue Skills der richtigen Familie zuordnen, Header-Router bei
  Familienänderung nachziehen (per `inject_family_header.py`), verwaiste Router entfernen.
- Inhalt: schlanker SKILL.md, der `inventory_skills.py` + `inject_family_header.py` aus
  `skill-explorer` referenziert (nicht kopiert) und die Familienliste aus `the family map` als Quelle nimmt.
- Trigger: „Familien pflegen", „neuen Skill einer Familie zuordnen", „Router aktualisieren".

**P2 — Register-Pflege** (`skill-register-care`):
- Zweck: hält `code-skill-index` + `the skill index` + `the family map` konsistent (Drift-Check:
  Inventar gegen Index, fehlende/zu viele Einträge melden, Counts korrigieren, Stand-Datum setzen).
- Inhalt: SKILL.md mit Drift-Check-Prozedur; nutzt `inventory_skills.py` als Ist-Stand.
- Trigger: „Skill-Register pflegen", „Index aktualisieren", „Register-Drift prüfen".

Beide werden — falls bestätigt — wie unten registriert. Vor dem Anlegen prüfen, ob ein gleichwertiger
Pflege-Skill schon existiert (keine Duplikate).

## Registrierungs-Ablauf (für jeden neu erzeugten user-Skill)

Gilt für Umbrella-Skills (c1), Workflow-Skills (b) und Pflege-Subskills (P1/P2). Reihenfolge:

1. **Master** — Skill unter `~/.claude/skills/<name>/` anlegen (SKILL.md + ggf. references/scripts/assets).
2. **Kategorie-Mapping** — in `<your skill-sync script>` im `LIB_CAT`-Block eine Zeile
   `[<name>]=<kategorie>` ergänzen (sonst überspringt der Sync den Skill mit „keine Kategorie-Zuordnung").
   Meta-/Skill-Management-Skills → `infrastructure`.
3. **Sync** — `bash <your skill-sync script> --check` (Erwartung: erkannt, `Kein-Kategorie: 0`),
   dann `--apply` → erzeugt die Library-Kopie unter `<skills library>/skills/<kategorie>/` und den Codex-Mirror.
   Falls die Kategorie neu ist, das Library-Verzeichnis vorher anlegen (`mkdir -p`), da `cp` keine
   Zwischenordner erstellt.
4. **Index** — `the skill index` (neue Zeile + Kopf-Datum) und `code-skill-index`-Katalog ergänzen.
5. **Verifikation** — `--check` zeigt nichts Neues mehr; SKILL.md am Master vorhanden; Skripte `bash -n`/
   Smoke-getestet.

> Wichtig: Nur **user-authored** Skills gehen in die `.AI/.SKILLS`-Library. Installierte
> Drittanbieter-Skills folgen dem externen Pfad (siehe den Explore-Modus → `references/install-uninstall.md`).
