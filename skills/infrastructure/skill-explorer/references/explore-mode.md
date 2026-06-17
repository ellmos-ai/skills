# Explore-Modus — Skills & Plugins im Web finden, prüfen, integrieren

Der nach-außen-gerichtete Modus von `skill-explorer`: recherchiert zu einem Thema, welche
Skills/Plugins es draußen gibt, vergleicht sie in Familien, simuliert ihre Wirkung auf den eigenen
Bestand und installiert/deinstalliert — **immer erst nach manueller Sicherheitsbeurteilung und
expliziter, nummerierter Freigabe**.

## Workflow

1. **Thema fassen** — Thema + Sprache klären. Recherche **zweisprachig**: Muttersprache des Users
   **und** Englisch.
2. **Mehrquellen-Recherche** (`references/research-method.md`): allgemeines Web, GitHub, Reddit — je
   in beiden Sprachen. Je Kandidat die **drei Kategorien** erfassen: (1) Fähigkeiten/Features,
   (2) Abhängigkeiten/Kosten, (3) Ressourcen/Alleinstellungsmerkmale.
3. **Clustern & vergleichen** in Familien (Taxonomie wie im Audit-Modus, `references/clustering.md`).
4. **Wirkungs-Simulation** (`references/integration-sim.md`): wenn ein früherer Audit/`config.json`
   vorliegt, simulieren, wie ein neuer Skill eine bestehende Familie verändert
   (verbessern/verschlechtern/unabhängiger machen).
5. **Nummerierte Empfehlungen** (global, wie im Audit-Modus): **(a)** „Skill X entfernen, dafür A
   installieren", **(b)** „Skill Z bringt einzigartige Fähigkeiten — bei Bedarf installieren".

## Sicherheit: primär manuell, Skript unterstützt

Die Sicherheitsbeurteilung ist **primär das Lesen des Codes durch das Modell** — um einen Skill zu
bewerten, muss man ihn ohnehin lesen (SKILL.md, **alle** Skripte, `package.json`, Hooks). Das Skript
`scripts/scan_skill_security.py` ist nur eine **unterstützende, regex-basierte Triage** mit klaren
Grenzen (keine Semantik/Kontext, neue Obfuskation entgeht ihm; `PASS` ≠ sicher, `BLOCK` ≠ zwingend
bösartig). Ablauf je bestätigter Installation (Details: `references/install-uninstall.md`):

1. **Staging** in einen lokalen Staging-Ordner klonen (nicht direkt ins Skill-Verzeichnis).
2. **Lesen & beurteilen (primär):** Modell liest die gestagten Dateien und urteilt.
3. **Skript-Triage (unterstützend):** scan ausführen, markierte Stellen nachlesen, Grenzen offenlegen.
4. **Promote** erst nach manuellem Urteil **und** expliziter Nutzer-Nummer.
5. **Hooks/Cron** (4-Augen-Prinzip) nur nach gesonderter Bestätigung.

## Vernetzen, aufräumen, registrieren

- War die Zielfamilie verlinkt (c2): neuen Skill mitvernetzen (`inject_family_header.py`); bei
  Umbrella (c1) in dessen Routing ergänzen. Bei zugestimmter Löschung: Mitglied aus Headern + Umbrella
  entfernen (`--remove`).
- **Registrierung nach Herkunft** (`references/install-uninstall.md`): user-authored Skills → voller
  Pfad inkl. Library; **Drittanbieter** → externer Pfad (lokales Deployment + Index-Eintrag „extern" +
  Staging-Quelle), **nicht** in die publizierte Library.

## Orchestrierung (modell-neutral)

Quellen (Web/GitHub/Reddit) × Sprachen sind unabhängige Suchpfade — wenn die Plattform günstigere
Subagenten bietet, je Quelle/Sprache einen beauftragen, Roh-Funde einsammeln, als Orchestrator
konsolidieren/prüfen. Sonst sequenziell selbst.
