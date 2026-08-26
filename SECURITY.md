# Security Policy

[English](#english) · [Deutsch](#deutsch)

---

## English

### Supported Versions

We actively support the latest release of `ellmos-ai/skills` on the default branch (`master`).

| Version | Supported | Notes |
| ------- | --------- | ----- |
| 1.3.x   | Yes       | Current active release line |
| < 1.3.0 | No        | Please upgrade to the latest version |

---

### Local-First & Zero-Egress Guarantees

`ellmos-ai/skills` is an offline-first, portable AI skill library designed for Claude Code, Codex, AGY/Gemini, BACH, and other local-first agent runtimes:

1. **Zero-Egress by Default**: Public skills contain pure Markdown (`SKILL.md`), YAML frontmatter, and local automation scripts. No telemetry, background tracking, or unsolicited outbound network requests are embedded in canonical public skills.
2. **Fail-Closed Privacy Boundary**: Automated privacy gates (`testing/privacy_gate.py` and `testing/test_public_private_boundary.py`) run in CI to ensure that personal data, host-scoped device names, private tokens (API keys, tokens), and internal directories are strictly prevented from entering tracked public repositories.
3. **Non-Elevation (User-Mode Execution)**: All skills and utility scripts operate entirely within unprivileged user space. Administrator or root privileges are never required or requested.
4. **Deterministic Frontmatter & Schema Validation**: Skill definitions are validated against strict YAML frontmatter schemas (`docs/CONVENTIONS.md`), preventing malicious instruction injection or untracked state manipulation.

### Gitless Projections

The repository privacy gate derives its file authority from Git. A gitless
archive or enriched projection must therefore delegate explicitly to a trusted
canonical checkout instead of guessing from the files physically present:

```bash
python testing/privacy_gate.py --canonical-repo <path-to-canonical-checkout>
```

Without that explicit checkout, the gate fails closed with a non-zero exit
code. The canonical path is never embedded in the public script.

---

### Reporting a Vulnerability

If you discover a potential security issue, sensitive information leakage, or vulnerability:

1. **Do NOT open a public issue.**
2. Send an email to **[security@ellmos.ai](mailto:security@ellmos.ai)** with a copy to **[support@lukasgeiger.com](mailto:support@lukasgeiger.com)**.
3. Include:
   - Description of the vulnerability or finding.
   - Affected skill(s) or script path(s).
   - Minimal reproduction steps or proof-of-concept.
   - Potential impact assessment.
4. Alternatively, use [GitHub Security Advisories](https://github.com/ellmos-ai/skills/security/advisories) to submit a private report.

We will acknowledge receipt within 48 hours and provide remediation updates.

---

## Deutsch

### Unterstützte Versionen

Wir unterstützen aktiv die neueste Version von `ellmos-ai/skills` auf dem Standard-Branch (`master`).

| Version | Unterstützt | Hinweise |
| ------- | ----------- | -------- |
| 1.3.x   | Ja          | Aktuelle Release-Linie |
| < 1.3.0 | Nein        | Bitte auf die neueste Version aktualisieren |

---

### Local-First- & Zero-Egress-Garantien

`ellmos-ai/skills` ist eine Offline-First-, portable KI-Skill-Bibliothek für Claude Code, Codex, AGY/Gemini, BACH und andere Local-First-Agenten-Laufzeiten:

1. **Zero-Egress standardmäßig**: Öffentliche Skills bestehen aus reinem Markdown (`SKILL.md`), YAML-Frontmatter und lokalen Automationsskripten. Es gibt keinerlei Telemetrie, Hintergrund-Tracking oder unaufgeforderte ausgehende Netzwerkverbindungen in kanonischen öffentlichen Skills.
2. **Fail-Closed Privacy-Boundary**: Automatisierte Privacy-Gates (`testing/privacy_gate.py` und `testing/test_public_private_boundary.py`) stellen in der CI sicher, dass keine personenbezogenen Daten, gerätespezifischen Hostnamen, privaten Tokens (API-Keys) oder internen Verzeichnisse in öffentliche Repositories gelangen.
3. **Non-Elevation (User-Mode-Betrieb)**: Alle Skills und Utility-Skripte laufen vollständig im unprivilegierten Benutzerbereich. Administrator- oder Root-Rechte werden zu keinem Zeitpunkt benötigt oder angefordert.
4. **Deterministische Frontmatter- & Schema-Validierung**: Skill-Definitionen werden gegen strikte YAML-Frontmatter-Schemas validiert (`docs/CONVENTIONS.md`), um fehlerhafte oder unsichere Instruktionsstrukturen auszuschließen.

### Gitlose Projektionen

Das Privacy-Gate leitet seine Dateiautorität aus Git ab. Ein gitloses Archiv
oder eine angereicherte Projektion muss deshalb ausdrücklich an einen
vertrauenswürdigen kanonischen Checkout delegieren, statt aus den physisch
vorhandenen Dateien zu raten:

```bash
python testing/privacy_gate.py --canonical-repo <pfad-zum-kanonischen-checkout>
```

Ohne diesen expliziten Checkout bricht das Gate fail-closed mit einem
Exitcode ungleich null ab. Der kanonische Pfad ist nicht im öffentlichen
Skript fest verdrahtet.

---

### Sicherheitslücke melden

Wenn Sie ein mögliches Sicherheitsproblem, ein Datenleck oder eine Schwachstelle entdecken:

1. **Eröffnen Sie bitte KEIN öffentliches Issue.**
2. Senden Sie eine E-Mail an **[security@ellmos.ai](mailto:security@ellmos.ai)** mit Kopie an **[support@lukasgeiger.com](mailto:support@lukasgeiger.com)**.
3. Bitte fügen Sie folgende Angaben bei:
   - Beschreibung der Sicherheitslücke bzw. des Fundes.
   - Betroffene(r) Skill(s) oder Skriptpfad(e).
   - Minimale Schritte zur Reproduktion (Proof-of-Concept).
   - Einschätzung der potenziellen Auswirkungen.
4. Alternativ können Sie private Sicherheitsberichte über [GitHub Security Advisories](https://github.com/ellmos-ai/skills/security/advisories) einreichen.

Wir bestätigen den Eingang innerhalb von 48 Stunden und halten Sie über Sicherheits-Updates auf dem Laufenden.
