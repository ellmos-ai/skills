# Gated Install/Uninstall, Vernetzung & Registrierung

## Grundsatz

**Nie automatisch installieren.** Immer: Staging → **manuelles Lesen & Beurteilen** → Skript-Triage
(unterstützend) → explizite Nutzer-Nummer → Promote. Die Sicherheitsbewertung ist primär das
**Lesen des Codes durch das Modell** — ein Skill wird ohnehin gelesen, um ihn zu beurteilen. Das
Skript ist nur eine schnelle, regex-basierte Vorpriorisierung mit bekannten Grenzen (keine Semantik,
kein Kontext, neue Obfuskation entgeht ihm). Der Skill installiert/deinstalliert erst, nachdem der
User die jeweilige Empfehlungsnummer bestätigt hat.

## Installations-Ablauf

1. **Staging (nicht nach ~/.claude!):**
   ```bash
   git clone --depth 1 <repo-url> "<staging-dir>/<name>"
   ```
   `--depth 1`, damit keine Historie mitkommt. Bei einzelnen Skill-Dateien stattdessen gezielt laden.

2. **Lesen & beurteilen (primär):** Das Modell liest die gestagten Dateien — SKILL.md, **alle**
   Skripte, `package.json` (pre/postinstall!), Hook-/Config-Dateien — und urteilt: Was tut der Code
   wirklich? Woher lädt er? Liest/schreibt er Secrets? Registriert er Hooks/Cron? Macht er Netzwerk?
   Dieses Lesen ist der eigentliche Sicherheits-Check und nicht delegierbar.

3. **Skript-Triage (unterstützend, nicht Ersatz):**
   ```bash
   PYTHONIOENCODING=utf-8 python scripts/scan_skill_security.py \
       "<staging>/<name>" --json "<staging>/<name>.scan.json"
   ```
   - `BLOCK` (CRITICAL/HIGH): starkes Warnsignal — die markierten Stellen gezielt nachlesen.
   - `REVIEW` (nur MEDIUM) / `PASS`: kein Freibrief — `PASS` heißt nur „keine bekannten Regex-Muster",
     **nicht** „sicher". Das Urteil aus Schritt 2 zählt.
   - Grenzen offenlegen: regex-basiert, blind für Semantik/Kontext/neue Obfuskation.
   - **Selbst-registrierende Hooks/Cron** werden als HIGH markiert (4-Augen-Prinzip): nur nach
     ausdrücklicher, gesonderter Bestätigung übernehmen.

4. **Promote (nach manuellem Urteil + Nummer):**
   ```bash
   cp -r "<staging-dir>/<name>/<skill-unterordner>" "$HOME/.claude/skills/<name>"
   ```
   Den tatsächlichen SKILL.md-Pfad im Repo finden (manche Repos legen Skills unter `skills/<name>/`).

5. **Abhängigkeiten:** benötigte CLIs/Pakete (npm/pip) dem User nennen; Installation nur auf Wunsch.

## Deinstallation

Nur nach expliziter Nummer:
```bash
rm -rf "$HOME/.claude/skills/<name>"
```
Vorher prüfen, dass es ein **user/external**-Skill ist — Plugin-Cache-Skills nicht löschen (kommen
beim Plugin-Update zurück; stattdessen Plugin deaktivieren).

## Vernetzung (an skill-explorer-Familien koppeln)

- War die Zielfamilie verlinkt (skill-explorer c2): neuen Skill mitvernetzen —
  ```bash
  PYTHONIOENCODING=utf-8 python scripts/inject_family_header.py \
      --family <f> --skills <neu> --router "<aktualisierter Wegweiser>" --inventory ~/.skill-inventory.json
  ```
  Vorher das Inventar neu erzeugen, damit der neue Skill als `editable` erkannt wird.
- Bei einem Umbrella (c1): den neuen Skill in dessen Routing-Tabelle ergänzen.
- Bei zugestimmter Löschung eines Mitglieds: dieses aus den Familien-Headern **und** dem Umbrella
  entfernen (`inject_family_header.py … --remove`), Umbrella-Tabelle bereinigen.

## Registrierung (extern vs. user-authored)

Strikt nach Herkunft trennen (Policy aus `the skill-sync script`):

| Herkunft | Master | `.AI/.SKILLS`-Library | Index | Provenance |
|----------|--------|------------------------|-------|------------|
| **Drittanbieter (installiert)** | `~/.claude/skills/<name>/` | **NEIN** (Policy: extern bleibt draußen) | Abschnitt „Externe Drittanbieter-Skills" in `the skill index` | Quell-Klon in `<staging-dir>\`; Codex-Mirror via Sync |
| **User-authored (selbst gebaut)** | `~/.claude/skills/<name>/` | **JA** via `LIB_CAT` + `the skill-sync script --apply` | passender Index-Abschnitt + `code-skill-index`-Katalog | provenance-Block im Frontmatter |

Beim externen Pfad **kein** `LIB_CAT`-Eintrag (sonst zöge der Sync ihn fälschlich in die Library).
Eine „nutzerneutrale Variante unter `.SKILLS`" gibt es nur für user-authored Skills — Drittanbieter-
Code wird nicht umgeschrieben/nutzerneutralisiert, nur referenziert.

> Nach Abschluss in der `skill-explorer/config.json` vermerken (installierter Skill, Familie,
> Vernetzung) und die Index-/Map-Dateien erweitern.
