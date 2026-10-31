---
name: security-tech-stack-check
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "Prüft den gemessenen Tech-Stack anhand aktueller primärer Sicherheitshinweise, trennt Betroffenheit von Unsicherheit und führt nur eng autorisierte, konfigurierte Korrekturen mit Readback aus."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, advisories, vulnerabilities, patching, tech-stack]
language: de
status: active
visibility: public
dependencies: {'tools': ['web'], 'services': [], 'protocols': [tech-detect], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# Security Tech Stack Check (STSC)

## Eintritt und Quellen

Prüfe nur autorisierte Assets aus einem aktuellen `tech-detect`-Techshot oder einer gleichwertig belegten Bestandsquelle. Nutze **jetzt** Websuche/verbundene Quellen für Herstelleradvisories und Patchnotes; ergänze [NVD CVE API](https://nvd.nist.gov/developers/vulnerabilities), [CISA KEV](https://github.com/cisagov/kev-data) zur Priorisierung tatsächlich ausgenutzter CVEs, [OSV API](https://google.github.io/osv.dev/api/) für eindeutig identifizierte Paketökosysteme und bei eigenen Repos die vorhandenen `github-health`-/Dependabot- und `codex-security`-Fähigkeiten. Quellen-URL, Abrufzeit UTC, Veröffentlichungs-/Änderungszeit und konkrete Produktkennung dokumentieren. Wenn eine Quelle nicht lesbar ist, `unknown`, nicht „kein Befund“ melden. Keine Skripte aus Feeds ausführen.

## Komponentengenaue Prüfung

1. Exakte Installation und Versionsbeleg aus dem Techshot wählen; Aliasse und mehrere Installationen getrennt behandeln. `unknown`/`uncertain` ist keine CVE-Betroffenheit.
2. Hersteller/Produkt, betroffene Versionsgrenze einschließlich Inklusiv-/Exklusiv-Ende, Betriebssystem/Architektur, optionale Konfiguration/Exposition und Hersteller-Patchstatus prüfen. NVD-CPE-Knoten können kombinierte Bedingungen haben; einfacher Namenssubstring oder „kleiner als neueste Version“ genügt nicht.
3. Je CVE/Installation `affected`, `not-affected` oder `undetermined` mit Begründung und Quellen ausgeben. KEV beweist bekannte Ausnutzung **des CVE**, nicht die Betroffenheit dieses Hosts. Priorität getrennt nach Ausnutzung, Exposition, Schwere und verfügbarem Fix angeben.
4. Privaten Bericht mit Techshot-SHA, Quellenstand, Lücken, konkreter Empfehlung, Wartungsfenster, Tests, Rollback und Verantwortlichem erstellen. Routinebefunde knapp halten, ungeklärte kritische Fälle sichtbar eskalieren.

## `config.json`-gesteuerter Fixmodus

Standard ist **Bericht ohne Änderung**. Der private, nicht in ein öffentliches Repo eingecheckte Konfigurationsvertrag enthält mindestens `schema: ellmos.stsc-config.v1`, `mode: report|apply`, `asset_id`, Host/Owner, Techshot-SHA, konkrete `actions[]` mit `action_id`, `component_id`, Ist-/Zielversion, Herstellerbeleg, erlaubtem lokalen Werkzeug/Argumenten, `authority_ref`, Wartungsfenster, Backup/Restoreweg und Nachprüfung. Das Profil oder eine Entscheidung kann bestehende Autorität belegen; bloße Profil-Vermutung oder eine selbst geschriebene Freitext-„Genehmigung“ nicht. Pro Asset und Aktion Lock, Rechte, aktuelle Version und Entscheidungsreichweite erneut lesen.

Bei `mode=apply` darf ein Agent die **exakt konfigurierte** Aktion über den vorhandenen nativen Paketmanager, Projektinstaller oder Konfigurationsworkflow ausführen, wenn Autorität und alle Vorbedingungen aktuell belegt sind. Keine aus dem Advisory kopierten Kommandos, kein pauschales `latest`, keine Shellverkettung, keine Erhöhung von Rechten und keine andere Anlage. Ist der Rollback nicht belastbar, eine Aktion außerhalb des erlaubten Scopes oder die Version unklar: `HOLD` mit engem technischen Grund; ein vorhandener gültiger Standing-Entscheid muss nicht künstlich neu angefragt werden. Vorher Snapshot/Hashes, danach tatsächliche Versions-/Funktions-/Sicherheitsnachprüfung, unveränderlichen Aktions-Receipt und gegebenenfalls Restore-Receipt schreiben. Ein Dry-run ist keine ausgeführte Reparatur.

Der öffentliche Skill speichert keine Host-Defaults, Keys oder Live-Config und führt selbst keinen Feed-Code aus. Geprüfte Quellenverträge: [NVD](https://nvd.nist.gov/developers/vulnerabilities), [CISA KEV-Daten](https://github.com/cisagov/kev-data), [OSV](https://google.github.io/osv.dev/api/), am 2026-10-25 gelesen. Herstellerhinweise bleiben für den konkreten Fix maßgeblich.

## Changelog

### 1.0.0 (2026-10-25)

- Primärquellen-Prüfung, Betroffenheitsgrenze und konfigurationsgebundener Reparaturablauf.
