# Audit-Modus — Bestand sichten & konsolidieren

Der nach-innen-gerichtete Modus von `skill-explorer`: sichtet **alle** vorhandenen Skills, clustert
sie in Familien, erhebt je Skill Fähigkeiten/Abhängigkeiten/Ressourcen und liefert pro Familie einen
Teilbericht mit **global durchnummerierten** Empfehlungen. Zweiphasig: Phase 1 nur Report (read-only),
Phase 2 führt nur nach Zahlen-Bestätigung aus.

## Eiserne Regel: Survey ≠ Mutation

**Clustern und berichten** über *alle* sichtbaren Skills (inkl. Plugin-/Drittanbieter-Skills),
aber **editieren** ausschließlich **user-eigene** Skills (`source: user`, `editable: true`).
Plugin-Cache-Skills (`plugin`) werden bei Updates überschrieben, Drittanbieter (`external`) sind
„Nur-Ziel" — beide nie mit Headern verändern oder löschen. Im Report als *read-only* kennzeichnen.

## Phase 1 — Erheben, Clustern, Berichten (read-only)

1. **Inventar (Skript):** deterministisch erheben, nicht jede Datei manuell lesen:
   ```bash
   PYTHONIOENCODING=utf-8 python scripts/inventory_skills.py --include-plugins \
       --out ~/.skill-inventory.json --pretty
   ```
   Liefert je Skill `name`, `source`, `editable`, `category`, `tags`, `description`, `dependencies`
   (tools/services/protocols/python), `resources` (scripts/references/assets) und H2-Überschriften.
2. **Clustern:** Familien aus den bestehenden Quellen seeden (`references/clustering.md`).
3. **Pro Familie Teilbericht** nach `references/report-format.md`: Mitglieder + Profil, dann
   Analyse — *Wann welcher Skill?* · *Gut gekoppelt?* · *Duplikate?* · *Ungleich gute Workflows?*
   (gleiche Fähigkeit, aber einer bringt Ressourcen mit, der andere nur Abhängigkeiten/Prosa → der
   ressourcenreichere bevorzugen).
4. **Konsolidierte, global durchnummerierte Entscheidungsliste** über alle Familien (`report-format.md`).
   Empfehlungstypen: **(a)** Redundanz ablösen, **(b)** Workflow-Skill aus n,o,p bauen, **(c)**
   Familien-Maßnahme: **c1** Umbrella anlegen · **c2** Familie per Header-Router verlinken · **c3** beides.
   Plus separat adressierbar: **[R]** Register erweitern, **[F]** Skill-Finder ausgründen,
   **[P1]/[P2]** Pflege-Subskills (siehe `references/family-care.md`, `references/skill-finder.md`).

## Phase 2 — Ausführen (nur nach Zahlen-Bestätigung)

- **c2 Header-Router** (nur `editable`-Skills, idempotent, Block im Body, sauber entfernbar):
  ```bash
  PYTHONIOENCODING=utf-8 python scripts/inject_family_header.py \
      --family <name> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
  # Entfernen: zusätzlich --remove
  ```
- **c1 Umbrella / [F] Finder / [P1]/[P2] Pflege:** Subskill aus der jeweiligen Vorlage in `assets/`
  ausgründen (Installer-Prinzip) und registrieren (`references/family-care.md`).
- **(a)/(b):** Workflow-Skill bauen bzw. Ablösung vorbereiten (Löschung erst nach expliziter Nummer;
  Drittanbieter/Plugin nie löschen).

Nach jeder Änderung registrieren und `config.json` aktualisieren (`references/config.md`).

## Orchestrierung (modell-neutral)

Familien-Teilberichte sind unabhängig — wenn die Plattform günstigere Subagenten bietet als der
Orchestrator selbst, je Familie einen Subagenten mit der Inventar-Teilmenge beauftragen und als
Orchestrator nur konsolidieren/prüfen (Spezialist-Schwarm). Sonst sequenziell selbst.
