# versionctl Build-Report — 2026-06-20

Modus: Implementierung Etappen 5, 6, 8 (funktionaler Kern).
Kein Skill geändert, keine bestehenden Dateien überschrieben.

## Neue Dateien

```
versionctl.py                            # CLI (Etappe 5)
templates/SKILL.md                       # (Etappe 6)
templates/PROMPT.md                      # (Etappe 6)
templates/WORKFLOW.md                    # (Etappe 6)
templates/AGENT.md                       # (Etappe 6)
registry/components.json                 # (Etappe 8) — 52 Komponenten (öffentliche Skills, gitignorierte private Skills ausgeschlossen)
registry/forks.json                      # (Etappe 8) — leer, befuellt ab Etappe 7
registry/branches.json                   # (Etappe 8) — leer
registry/releases.json                   # (Etappe 8) — leer
registry/deployments.json               # (Etappe 8) — leer
testing/test_versionctl.py              # 22 pytest-Tests
_reports/inventory-2026-06-20.json      # von versionctl inventory erzeugt
```

## Geänderte Dateien

```
UMSETZUNGSPLAN.md    # Etappe 5, 6, 8 als IMPLEMENTIERT markiert
CHANGELOG.md         # Eintrag für 2026-06-20 hinzugefügt
```

## versionctl-Befehle (real getestet gegen Bestand)

### registry-generate

```
Registry geschrieben: registry/components.json  (52 Komponenten)
Angelegt: registry/forks.json
Angelegt: registry/branches.json
Angelegt: registry/releases.json
Angelegt: registry/deployments.json
```

Nur öffentliche, von Git getrackte Skills werden einbezogen.
Gitignorierte Skills (gemäß `.gitignore`) werden durch `git ls-files`-Filter automatisch
ausgeschlossen und erscheinen weder in der Registry noch im Inventory.

### status (nach registry-generate)

```
OK: 52  |  NEU: 0  |  DRIFT: 0  |  Nur-Registry: 0
Registry ist aktuell.
```

### validate

Reale Befunde (korrekt erkannt, keine false positives):

- `skills/dev/dev-soft-agent/SKILL.md`: type: agent — nicht in skill-v1-Schema erlaubt
- `skills/dev/update-cli-docs/SKILL.md`: 5 CONVENTIONS-Pflichtfelder fehlen (version, type, author, created, updated)

Total: 2 Skills mit Befunden, 6 Fehler.
(Gitignorierte Skills werden nicht validiert.)

### inventory

```
Inventory geschrieben: inventory-2026-06-20.json  (52 Skills)
```

## Tests

```
22 passed in 3.24s  (testing/test_versionctl.py)
24 passed in 4.71s  (testing/test_skill_sync.py — Regression-Check)
```

Abdeckung: Schema-Validation positiv+negativ, Drift-Erkennung, Registry-Reproduzierbarkeit,
Dry-Run, Pfad-Leak-Check, Inventory-Privatsicherheit.

## Leak-Grep

Geprüfte Dateien: `registry/components.json`, `_reports/inventory-2026-06-20.json`.
Muster: Windows- und Unix-Benutzerpfade, Tailscale-IP, SSH-Login-Präfix.

**Ergebnis: 0 Treffer.** Keine absoluten Systempfade in generierten Dateien.

## Reproduzierbarkeit

- Komponenten-Daten (`components`-Array) sind bei mehrfachem Aufruf von `registry-generate`
  byte-identisch (stabile Sort-Reihenfolge nach `path`, keine volatilen Timestamps in Komponentenfeldern).
- `summary.generated_at` variiert naturgemäß; das ist by design.
- Test `test_registry_generate_reproducibel` verifiziert dies automatisch.

## Offene Etappen

| Etappe | Thema | Status |
|--------|-------|--------|
| 0–4 | Freeze, Inventur, Klassifikation, Schema, Schatten-Registry | ✅ erledigt (Vorsession) |
| 5 | versionctl CLI | ✅ 2026-06-20 |
| 6 | Templates | ✅ 2026-06-20 |
| 7 | Fork-Modell Schattenmodus | offen |
| 8 | Produktive Registry | ✅ 2026-06-20 |
| 9 | Drift-Reports | offen |
| 10 | Bump-Befehle | offen |
| 11 | Privacy-Gate | offen |
| 12 | Export-Adapter | offen |
| 13–16 | Release, Branch-Ops, BACH-Integration, PromptBoard | offen |

## Validierungsbefunde (echte Registry-Lücken, offen)

Die folgenden Skills haben reale Qualitätsprobleme, die außerhalb des versionctl-Scopes liegen:

1. `type: agent` in `dev-soft-agent` — Typ existiert nicht im skill-v1-Schema.
   Optionen: (a) Schema erweitern um `agent`, (b) Skill auf `service` oder `tool` umstellen.
2. `update-cli-docs/SKILL.md` ohne Pflichtfelder — Frontmatter unvollständig.
