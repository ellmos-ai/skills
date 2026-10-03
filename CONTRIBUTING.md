# Contributing to ellmos-skills / Mitwirken an ellmos-skills

Welcome! We welcome contributions to `ellmos-skills` (`ellmos-ai/skills` - Portable AI skill library for Claude Code, Codex, AGY, BACH, and local-first LLM agents from [ellmos-ai](https://github.com/ellmos-ai) under the [open-bricks](https://github.com/open-bricks) umbrella). To ensure deterministic agent tool executions, air-gapped process isolation, strict privacy boundary defense, and seamless cross-platform multi-host resilience, all contributions must adhere to the standards, quality gates, and operational invariants specified below.

---

## English

### 1. General Principles & Quality Gates
1. **100% Local-First & Zero Egress (`INV-LOCAL-01`)**: All catalog generators, static validation gates, privacy boundary verifiers, and indexing tools operate strictly offline using the Python standard library. Zero outbound network sockets, zero telemetry, and zero phone-home tracking.
2. **Fail-Closed Privacy Boundary Gate (`INV-PRIVACY-02`)**: Automated privacy validation (`testing/privacy_gate.py`) strictly enforces the exclusion of private user paths, personal tokens, credentials, host-specific identifiers, and unapproved private skill categories.
3. **Non-Elevation & RunAsInvoker (`INV-UNPRIV-03`)**: All CLI runners, test suites, generator scripts, and skill execution steps execute strictly in unprivileged user space. Administrative elevation (UAC/root/sudo) is strictly prohibited.
4. **Deterministic Frontmatter & Schema Integrity (`INV-SCHEMA-04`)**: YAML frontmatter across all skills strictly conforms to `docs/CONVENTIONS.md` and schema validation rules (`name`, `description`, `category`, `tags`, etc.).
5. **Portable & Self-Contained Skill Anatomy (`INV-ISOLATION-05`)**: Skills package their own playbooks, references, and scripts cleanly without implicit host dependencies or unversioned couplings.
6. **Multi-Agent Runtime Portability (`INV-PORTABLE-06`)**: Skills are verified across major agent runtimes including Claude Code, OpenAI Codex, Google Antigravity / Gemini, BACH, and local Ollama runtimes.
7. **Public/Private Boundary Isolation (`INV-DISCOVERY-07`)**: The public catalog (`registry/components.json`) exposes only verified non-sensitive discovery fields, keeping internal maintenance profiles isolated.
8. **Multi-OS Parity & Platform Independence (`INV-PLATFORM-08`)**: All features, scripts, and skills must pass automated testing across Linux, Windows, macOS, and Python 3.10 through 3.13.
9. **Multi-Host Cloud Sync & Lock Resilience (`INV-SYNC-09`)**: Hardened `.gitignore` and cooperative lock protocols prevent cloud sync races, conflict copies, and data corruption across distributed workstations.
10. **48h Security Response & Triage Commitment (`INV-SLA-10`)**: We commit to a 48h initial acknowledgment SLA and a 5-business-day triage commitment for security disclosures pursuant to [SECURITY.md](SECURITY.md).
11. **Version Freeze Discipline (`T-20260920-167562623`)**: Package version `1.4.4` is strictly frozen across `pyproject.toml`, manifests, and badges. Do not bump the version string. Document all advancements under `## [Unreleased]` in `CHANGELOG.md`.
12. **Statutory Limitation of Liability (§ 521 BGB)**: This open-source repository is provided free of charge under the MIT License. In accordance with statutory German law for gratuitous services (§ 521 BGB - *Gefälligkeitsrecht*), the author and maintainers are liable only for intent (*Vorsatz*) and gross negligence (*grobe Fahrlässigkeit*).

### 2. Local Development Workflow (Plan D)
```bash
# Clone the repository (canonical Plan D local repository checkout)
git clone https://github.com/ellmos-ai/skills.git
cd skills

# Run full pytest test suite
pytest -ra -v

# Run fast static code analysis
ruff check .

# Validate privacy boundary gate
python testing/privacy_gate.py

# Verify bytecode compilation across testing and skills
python -m compileall -q testing skills

# Check git diff and whitespace cleanliness
git diff --check

# Verify version freeze compliance (must return 0 matches)
git diff -G"version = "
```

### 3. Submission Protocol
- File an issue before embarking on large structural refactorings or new top-level skill domains.
- Ensure all 10 governance invariants (`INV-LOCAL-01` to `INV-SLA-10`) are strictly satisfied.
- Keep credentials, API keys, personal configs, and private overlays strictly outside the repository.
- Pull requests must target the `master` branch.

### 4. License
By contributing to `ellmos-skills`, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

## Deutsch

### 1. Grundsätze & Qualitäts-Tore
1. **100% Local-First & Zero Egress (`INV-LOCAL-01`)**: Alle Katalog-Generatoren, Validierungs-Gates, Privacy-Prüfer und Indizierungswerkzeuge arbeiten standardmäßig zu 100% offline ausschließlich mit Modulen der Python-Standardbibliothek. Keine Telemetrie, keine externen Netzwerk-Sockets, kein Phone-Home.
2. **Fail-Closed Privacy Boundary Gate (`INV-PRIVACY-02`)**: Das automatisierte Privacy-Gate (`testing/privacy_gate.py`) erzwingt strikt den Ausschluss von nutzerspezifischen Pfaden, persönlichen Tokens, Zugangsdaten, Host-Token-Mustern und unautorisierten privaten Skill-Bereichen.
3. **Unprivilegierte Ausführung (`INV-UNPRIV-03` / `RunAsInvoker`)**: Sämtliche Testläufe, Generatoren, Skripte und Skill-Aktionen laufen strikt im unprivilegierten Standard-Benutzerkontext. Administrative Elevationen (UAC/root/sudo) sind verboten.
4. **Deterministisches Frontmatter & Schema-Integrität (`INV-SCHEMA-04`)**: YAML-Frontmatter aller Skills entspricht ausnahmslos `docs/CONVENTIONS.md` und den Schema-Vorgaben (`name`, `description`, `category`, `tags` usw.).
5. **Portable & Selbständige Skill-Anatomie (`INV-ISOLATION-05`)**: Skills kapseln ihre Handlungsanweisungen, Referenzen und Skripte sauber ohne implizite Host-Abhängigkeiten oder unversionierte Kopplungen.
6. **Multi-Agenten-Laufzeit-Portabilität (`INV-PORTABLE-06`)**: Skills sind verifiziert für führende Agenten-Laufzeiten wie Claude Code, OpenAI Codex, Google Antigravity / Gemini, BACH sowie lokale Ollama-Modelle.
7. **Isolation der Öffentlich/Privat-Grenze (`INV-DISCOVERY-07`)**: Der öffentliche Katalog (`registry/components.json`) exponiert nur geprüfte, unkritische Metadaten; interne Wartungsprofile bleiben vollständig isoliert.
8. **Plattformunabhängigkeit & Multi-OS-Parität (`INV-PLATFORM-08`)**: Alle Skripte und Skills müssen die automatisierte GitHub Actions CI-Matrix unter Linux, Windows, macOS und Python 3.10 bis 3.13 fehlerfrei bestehen.
9. **Multi-Host Cloud-Sync & Lock-Resilienz (`INV-SYNC-09`)**: Gehärtete `.gitignore`-Muster und kooperative Lock-Protokolle verhindern Cloud-Synchronisations-Races, Konfliktkopien und Datenkorruption über verteilte Arbeitsstationen.
10. **48h Sicherheits-Reaktions- & Triage-Zusage (`INV-SLA-10`)**: Verbindliche Zusage einer 48h-Erstbestätigung und 5-Werktage-Triage für gemeldete Sicherheitsvorfälle gemäß [SECURITY.md](SECURITY.md).
11. **Version-Freeze-Disziplin (`T-20260920-167562623`)**: Paketversion `1.4.4` ist über alle Manifeste, Badges und Konfigurationen hinweg strikt eingefroren. Kein Versions-Bump. Alle Neuerungen werden unter `## [Unreleased]` in `CHANGELOG.md` dokumentiert.
12. **Gesetzlicher Haftungsausschluss (§ 521 BGB - Gefälligkeitsrecht)**: Dieses Open-Source-Projekt wird unentgeltlich unter der MIT-Lizenz bereitgestellt. Gemäß § 521 BGB haften Autor und Betreuer bei unentgeltlicher Leistung nur für Vorsatz und grobe Fahrlässigkeit.

### 2. Lokaler Entwicklungs-Workflow (Plan D)
```bash
# Repository klonen (kanonischer Plan D lokaler Checkout)
git clone https://github.com/ellmos-ai/skills.git
cd skills

# Vollständige Pytest-Testsuite ausführen
pytest -ra -v

# Statische Code-Prüfung ausführen
ruff check .

# Privacy-Gate validieren
python testing/privacy_gate.py

# Bytecode-Kompilierung prüfen
python -m compileall -q testing skills

# Git-Diff- und Whitespace-Sauberkeit prüfen
git diff --check

# Versions-Freeze prüfen (muss 0 Treffer liefern)
git diff -G"version = "
```

### 3. Einreichungsprotokoll
- Bei größeren strukturellen Änderungen bitte vorab ein GitHub Issue zur Abstimmung eröffnen.
- Sicherstellen, dass alle 10 Invarianten (`INV-LOCAL-01` bis `INV-SLA-10`) erfüllt sind.
- Keine API-Keys, Host-spezifischen Daten oder privaten Overlays im Repository ablegen.
- Pull Requests müssen auf den `master`-Branch zielen.

### 4. Lizenz
Mit dem Einreichen von Beiträgen zu `ellmos-skills` erklären Sie sich damit einverstanden, dass Ihre Beiträge unter der [MIT-Lizenz](LICENSE) lizenziert werden.
