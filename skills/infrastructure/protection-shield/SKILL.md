---
name: protection-shield
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "Koordiniert begrenzte defensive Sofortmaßnahmen und wiederkehrende Serverlog-/Stack-Prüfungen mit Assetautorität, Beweissicherung, Readback und Rollback."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [defense, incident-response, server, logs, monitoring]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [tech-detect, security-tech-stack-check], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# Protection Shield

## Akuter defensiver Einsatz

Nur für eigene oder ausdrücklich autorisierte Systeme, Netze und Server. Zuerst Asset-ID, Owner, Ausführungsautorität, laufende Sperren, Auswirkungsradius und vorhandenen Notfall-/Rollbackweg feststellen. Ein Alarm oder eine Auffälligkeit allein ist keine Freigabe für produktive Netzänderungen. Keine Gegenangriffe, kein Zugriff auf fremde Assets und kein unautorisierter Port- oder Dienstescan.

1. **Lage sichern:** Uhrzeit UTC, betroffene Dienste, aktuelle Konfiguration und begrenzte relevante Logauszüge/Hashes aufnehmen; Geheimnisse redigieren, Originale privat erhalten. Symptome, bestätigte Kompromittierung und Hypothesen getrennt führen.
2. **Bestehende Autorität prüfen:** Projekt-Runbook, Standing-Entscheid, privates Assetprofil und konkrete `config.json`-Aktion lesen. Ohne gültige Deckung nur lesend analysieren und die tatsächlich nötige Restentscheidung als Ticket routen. Technische Blocker an Worker statt pauschal an den Nutzer.
3. **Maßnahme eingrenzen:** etwa einen eigenen Dienst über den vorhandenen Service-Manager stoppen, eine konkret exponierte Regel im vorhandenen Firewall-Workflow ändern, Zugang über die dafür bestimmte Rotation sperren oder einen Patch über `security-tech-stack-check` ausführen. Exakter Zielhost, Regel/Dienst, erwartete Wirkung, Zeitfenster und Rückweg müssen gebunden sein. Keine pauschalen Netzsperren und keine Admin-Erhöhung durch den Skill.
4. **Ausführen und verifizieren:** nur mit vorhandenen nativen Tools und gültigem Asset-/Aktionsscope; vorher/nachher Zustand, Exitcode, Funktionsprobe, Logwirkung und Nebenwirkung protokollieren. Bei Fehlschlag nach Runbook zurückrollen und Restore separat messen. Eine konfigurierte Absicht ist noch keine wirksame Abwehr.

## Wiederkehrende Prüfung

Ein privates Profil benennt nur erlaubte Logpfade/API-Leser, Techshot-Stand, Assetliste, Lookback, Filter, Zeitplan, Retention und Eskalationsziel. Den **vorhandenen** Scheduler/Logdienst anbinden statt einen zweiten Daemon zu installieren. Jeder Lauf liest nur den begrenzten Zeitraum und die benannten Quellen, dedupliziert Ereignisse, vergleicht Stackstände über `tech-detect` und relevante aktuelle Hersteller-/CISA-Hinweise über `security-tech-stack-check`. Quelle, UTC-Fenster, Parserfehler, fehlende Rechte und Abdeckung in den Receipt; Routineerfolge nicht als Alarm aufblasen. Ein geplanter Lauf ist erst nach einem tatsächlichen Scheduler- und Ergebnis-Readback aktiv.

Für den begrenzten Logabruf vorhandene Leser nutzen: etwa `Get-WinEvent -FilterHashtable` mit konkretem Log und Startzeit, `journalctl --since ... --until ... -u <eigener Dienst>` oder den projektspezifischen Serverlog-Leser. Keine pauschale Suche durch sämtliche Logverzeichnisse. Für den Zeitplan an den vorhandenen Windows Task Scheduler, systemd-Timer oder launchd-Job des Assets anschließen und anschließend dessen registrierte Definition, letzten Lauf, Exitstatus und Ergebnisdatei lesen. Ohne diese vier Belege ist die periodische Abwehr nur geplant.

Priorisierung: bestätigte aktuelle Exposition und belastbarer Sicherheitsbefund vor allgemeinen Versionsunterschieden. `unknown` bleibt offen. Incident-Runbooks, Logschutz und Assetrechte des Projekts haben Vorrang; dieser Skill erfindet keine globale Firewall-Policy oder dauerhafte Freigabe.

## Changelog

### 1.0.0 (2026-10-25)

- Enger defensiver Sofort- und periodischer Prüfablauf ohne automatische Produktivaktivierung.
