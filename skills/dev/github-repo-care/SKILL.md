---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: >
  Protokoll für das sichere Erstellen, Veröffentlichen und Pflegen von GitHub-Repositories:
  lokale Regeln und Sperren prüfen, .gitignore vor dem ersten Add setzen, Privacy-Checks
  durchführen, README/i18n/Banner/Metadaten vorbereiten, Release-Tag und GitHub-Release
  verifizieren sowie Organisationsprofile, llms.txt und Registry-Links aktualisieren.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: de
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.codex/skills/github-repo-care/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-06-18"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="github-repo-care banner">

# GitHub Repo Care — Repository sauber veröffentlichen und pflegen

## Wann dieser Skill greift

Nutze diesen Skill, wenn ein GitHub-Repository neu erstellt, veröffentlicht, gereleaset, auditiert oder nachträglich gepflegt werden soll. Er ist besonders wichtig vor dem ersten öffentlichen Push, bei Release-Tags, bei Änderungen an Repository-Metadaten, bei Organisationsprofilen und bei Privacy-Checks.

Greift nicht für reine Code-Implementierung ohne GitHub-Veröffentlichung. In diesem Fall erst den passenden Entwicklungs- oder Debugging-Skill verwenden und diesen Skill erst beim Publikationsschritt aktivieren.

## Kernregel

Bereite das Repository vor dem ersten öffentlichen Push vor. Eine korrekte `.gitignore`, ein sauberer Privacy-Gate, Lizenz, README, Metadaten und Release-Story sind vor öffentlicher Historie deutlich einfacher als danach.

## Ablauf

1. **Lokale Regeln lesen.** Prüfe `AGENTS.md`, `CLAUDE.md`, `START.md`, Release-Policy, Naming-Policy und Lock-Policy, sofern vorhanden.
2. **Sperren prüfen.** Wenn `LOCK.txt` oder eine passende `LOCK.*.txt` aktiv ist, diesen Scope nicht ändern.
3. **Repository-Namen festlegen.** Namen, Organisation, Sichtbarkeit, Lizenz und Zweck in einem Satz festhalten.
4. **`.gitignore` vor `git add` anlegen.** Secrets, lokale Daten, Datenbanken, Build-Ausgaben, virtuelle Umgebungen, Caches, IDE-Dateien und private Notizen ausschließen.
5. **Public-Basics ergänzen.** Typisch: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `llms.txt` und CI.
6. **README für Entdeckung schreiben.** Erste Bildschirmhöhe: Zweck, Installation, Nutzung, Privacy-Modell, Projektstruktur, Lizenz und kanonischer Repo-Name.
7. **Visuelle Signale setzen.** Banner, Logo oder Screenshot ergänzen, wenn sie den Nutzen erkennbarer machen. Keine generische Dekoration, wenn ein echtes Produktbild oder klares Konzeptbild möglich ist.
8. **Mehrsprachigkeit bewusst planen.** Minimum: Englisch plus Projektsprache. Für nutzernahe Module bevorzugt: Deutsch, Englisch, Spanisch, vereinfachtes Chinesisch, Japanisch und Russisch.
9. **Tests und Smokes ausführen.** Lokal verifizieren, bevor Erfolg behauptet oder ein Release erstellt wird.
10. **Privacy-Gate ausführen.** Staged/tracked Set prüfen: Secrets, lokale Pfade, PII, `.env`, Datenbanken, private Dokumente, generierte Artefakte und Mojibake.
11. **Committen und pushen.** Nur nach bestandenem Gate committen. Danach GitHub-Repo anlegen oder verbinden, pushen und Remote-Status prüfen.
12. **Metadaten setzen.** Beschreibung, Topics, Homepage, Sichtbarkeit und Branch-Default prüfen.
13. **Release erstellen.** Tag und GitHub-Release anlegen; CI für Branch und Tag prüfen.
14. **Discovery-Flächen aktualisieren.** Organisationsprofil, `llms.txt`, zentrale Registries, lokale Modulindizes und Ökosystem-READMEs verlinken.
15. **Abschluss prüfen.** Remote README, Release-Seite, Topics, CI und Links kontrollieren.

## Privacy-Gate

Suche im gestagten oder getrackten Set, nicht nur im sichtbaren Arbeitsbaum.

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

Bei öffentlichen Modulen zusätzlich ein `RELEASE_GATE.md` oder äquivalentes Gate dokumentieren: Datum, geprüfte Befehle, Ergebnis, Restwarnungen und bewusste Ausnahmen. Wenn ein Secret jemals committed wurde, reicht Löschen aus `HEAD` nicht; das Secret muss rotiert werden.

## GitHub-Metadaten

Nach dem Push Metadaten und Release explizit setzen.

```bash
gh repo edit ORG/REPO --description "Kurze konkrete Beschreibung" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

Danach verifizieren:

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

Wenn CI nach einem Release rot ist, gilt das Repository noch nicht als sauber veröffentlicht. Bei einem gerade erstellten Initialrelease ist es akzeptabel, den frischen Tag sofort und bewusst auf den korrigierten Commit zu verschieben.

## Häufige Fehler

| Fehler | Korrektur |
|---|---|
| `.gitignore` wird erst nach `git add` erstellt | Erst unstage, Ignore-Regeln korrigieren, dann erneut adden |
| README ist einsprachig, obwohl UI oder Skill mehrsprachig ist | Sprachlinks oder lokalisierte READMEs ergänzen |
| Kein Banner, keine Topics, keine Beschreibung | Discovery-Assets vor Ankündigung ergänzen |
| Release-Tag existiert, aber CI ist rot | CI fixen und neuen Run prüfen |
| Organisations-README aktualisiert, aber `llms.txt` vergessen | Beide menschlichen und maschinenlesbaren Flächen aktualisieren |
| Lokaler Pfad steht in öffentlicher Doku | Durch relative Pfade oder generische Beispiele ersetzen |
| Public Repo enthält Testdatenbank oder Notebook-Inbox | Datei aus Tracking entfernen, Ignore-Regel ergänzen, Gate erneut laufen lassen |

## Abschluss-Checkliste

- [ ] Lokale Regeln und Sperren geprüft.
- [ ] `.gitignore` existierte vor dem ersten Add.
- [ ] Public-Dokumente, Lizenz, Security, Contributing, Changelog und `llms.txt` vorhanden.
- [ ] README enthält Repo-Name, Zweck, Installation, Nutzung, Privacy und Lizenz.
- [ ] i18n-Erwartung erfüllt.
- [ ] Banner, Logo oder Screenshot vorhanden, sofern sinnvoll.
- [ ] Tests und Smokes bestanden.
- [ ] Privacy-, Pfad-, Secret-, Datenbank- und Mojibake-Scans sauber.
- [ ] GitHub-Beschreibung, Topics, Tag, Release und CI verifiziert.
- [ ] Organisationsprofil, Registry und Ökosystem-Links aktualisiert.

## Changelog

### 1.0.0 (2026-06-18)
- Initiale Version als Repository-Pflege- und Veröffentlichungsprotokoll erstellt.
