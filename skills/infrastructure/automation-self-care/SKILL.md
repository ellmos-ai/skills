---
name: automation-self-care
version: 1.1.0
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-08-30
description: >
  Baut und betreibt ein anbieterneutrales Self-Care-Kernset für geplante
  LLM-Aufgaben und Desktop-App-Automationen. Nutzen, wenn ein Agent seinen
  nativen Scheduler entdecken, wiederkehrende Hygiene-, Prompt-Qualitäts-,
  Frequenz-, Last-, Ressourcen-, Cross-System-, Berechtigungs- und
  Laufzeit-Checks installieren oder eine bestehende Automations-Flotte mit
  Rollback, Readback und Löschschutz kontinuierlich verbessern soll. Löst
  aus bei automation self-care, Scheduler-Task-Pflege, Desktop-App-
  Automations-Wartung, Automations-Flotten-Audit, selbstheilende
  Zeitpläne, Anfragen zur Wiederherstellung der ANTIGRAVITY-artigen
  Wartungs-Task-Familie, core-set-textautomations, basic-text-automations,
  textbased-automation-core, textbased-automation-drivers oder
  textbased-desktopapp-automations.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system]
language: de
status: active
visibility: public
aliases: [core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="automation-self-care banner">

# Automation Self-Care

Erstellt eine native, anbieterspezifische Wartungs-Flotte aus einer einzigen
anbieterneutralen Regelschleife. Bewahrt die ursprüngliche Absicht der
ANTIGRAVITY-Task-Familie, verlangt dabei aber Belege, reversible Änderungen
und native Readbacks.

## Nicht verhandelbare Grenzen

- Discovery, Planung, Freigabe, Mutation und Readback als getrennte Phasen
  behandeln.
- Die unterstützte Automations-API, den Befehl oder die UI der Ziel-App
  nutzen. Niemals annehmen, dass das Bearbeiten einer Speicherdatei den
  Live-App-State ändert.
- Lokale Regeln, Locks, Lösch-/Suppression-Logs und bestehende Zeitpläne
  lesen, bevor ein Task vorgeschlagen wird.
- Keine Scheduler-Unterstützung erfinden. Kann Create/Update/Readback nicht
  belegt werden, einen manuellen Installationsplan erstellen und vor der
  Mutation anhalten.
- Höchstens eine unabhängig testbare Tuning-Änderung je Care-Lauf.
- Die Care-Tasks davor schützen, sich selbst zu deaktivieren oder ihren
  eigenen Takt unter den konfigurierten Recovery Floor zu senken. Nur eine
  ausdrückliche Nutzerentscheidung, ein Sicherheitsgate oder ein belegter
  Notfall darf eine kontrollierte Pause autorisieren.
- Stabile maschinelle Task-IDs unabhängig von sichtbaren Titeln halten. Ein
  App-Präfix als zusätzlichen Erkennbarkeits-Schutz behandeln, niemals als
  Identität oder als Ersatz für Recovery-, Suppression-, Rollback- und
  Readback-Kontrollen.
- Den vorherigen Prompt, Zeitplan, Modell, Berechtigungen und Aktiv-Status
  bewahren, damit jede Mutation zurückgerollt werden kann.
- Erfolg erst nach Ergebnis-Beleg zählen, nicht bloß nach Scheduler-Start
  oder Exit 0.
- Niemals Geheimnisse, private Prompts oder personenbezogene Daten in eine
  geteilte Registry kopieren.

## Ablauf

### 1. Die native Automationsoberfläche entdecken

Den aktuellen Akteur, Anbieter, nicht-sensitiven `app_display_name`,
App-Klasse, Scheduler-Oberfläche, unterstützte Operationen, State-Dateien,
Lauf-Historie, Nutzungstelemetrie und Readback-Methode inventarisieren.
Fähigkeiten über den Profilvertrag in
[provider-adapter-contract.md](references/provider-adapter-contract.md)
festhalten.

Native Desktop-App-Zeitpläne, CLI-/Headless-Ausführung, OS-Scheduler oder
Service-Starter, allgemeinen Scheduler-Dienst, Workflow-Engine und nicht
unterstützte oder nur-UI-Automation unterscheiden. Die Existenz einer
Konfigurationsdatei nicht mit einem unterstützten Mutationspfad
gleichsetzen.

### 2. Die Flotte inventarisieren

Für jeden Task einen stabilen lokalen Identifier, semantische Rolle,
sichtbaren Titel, Zweck, Prompt-Fingerprint, Zeitplan, Aktiv-Status, Modell,
Reasoning, Berechtigungen, Zielpfade, letztes Scheduler-Ereignis, letztes
erfolgreiches Ergebnis und aktuellen Owner erfassen. Prompt-Inhalt lokal
halten.

Bestehende Tasks semantisch abgleichen, bevor eine Neuanlage vorgeschlagen
wird. Zuerst stabile Task-ID, dann anbieter-native ID, semantische Rolle und
bekannter Legacy-Titel bevorzugen. Ein abweichender sichtbarer Titel ist
kein Beleg dafür, dass ein neuer Task nötig ist. Mehrdeutige Treffer
blockieren den Plan, statt ein Duplikat anzulegen.

Die maßgebliche Live-Oberfläche vor jeder Mutation zweimal prüfen, wenn die
App State aus dem Gedächtnis neu schreiben kann.

### 3. Das Core-Set entwerfen

[core-set.md](references/core-set.md) lesen. Wählen zwischen:

- `compact`: fünf Care-Tasks, die Frequenz mit Lastverteilung kombinieren;
  oder
- `full`: neun fokussierte Tasks entsprechend der ursprünglichen
  Wartungs-Familie.

Einen anbieterneutralen Plan erzeugen:

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
python scripts/build_core_set.py --lint-plan automation-care-plan.json
```

Der Generator installiert niemals Tasks. Jede `blocked`-Fähigkeit prüfen und
kollisionsfreie lokale Zeiten wählen, bevor der Plan angewendet wird. Neue
Anbieter-Profile setzen `app_display_name` ausdrücklich; CI kann das mit
`--strict-profile` erzwingen. Erzeugte sichtbare Titel nutzen
`<APP_DISPLAY_NAME> — <CARE_TITLE>`, während `automation-care.*`-Task-IDs
unverändert bleiben. Ein Codex-Profil nutzt `CODEX`.

### 4. Installation stufenweise

Über den nativen Anbieter-Adapter installieren:

1. Mit Hygiene im Read-only-Modus beginnen.
2. Ressourcenschutz ergänzen.
3. Prompt-Qualitäts-Tuning mit Rollback ergänzen.
4. Frequenz- und Lasttuning erst ergänzen, wenn genug Lauf-Belege
   vorliegen.
5. Cross-System-Koordination zuletzt ergänzen.

Für eine reine Titel-Migration den semantisch gematchten Task über die
unterstützte native Oberfläche in-place aktualisieren. Die stabile ID und
alle Nicht-Titel-Felder zurücklesen; jedes unerwartete operative Delta
verlangt Rollback. Ein zweiter Plan-/Apply-Zyklus muss keine Änderung
melden und darf keinen weiteren Task anlegen.

Neue oder importierte Tasks deaktiviert anlegen, sofern der Nutzer die
aktive Installation nicht ausdrücklich freigegeben hat. Für einen
unbeaufsichtigten Pilotlauf zuerst ein Löschlog, einen
Vorher-State-Snapshot, einen Laufbeleg und einen Rollback-Pfad verlangen.

### 5. Die Care-Schleife ausführen

Jeder Care-Task folgt:

```text
follow-up previous change
  -> collect current evidence
  -> classify one cause
  -> choose zero or one change
  -> mutate through native surface
  -> read back
  -> write receipt and next-check condition
```

Den Hypothesen-Katalog und die Belegregeln in
[core-set.md](references/core-set.md) nutzen. Unbekannte Ursache bedeutet
beobachten, Berechtigungen einschränken oder sicher pausieren; niemals eine
Reparatur raten.

### 6. Über Akteure hinweg koordinieren

Lokalen App-State als maßgeblich behalten. Nur Task-Verträge, Abdeckung,
Status, Belege und bereinigte Fingerprints teilen. Redundante Read-only-
Reviews sind erlaubt; Single-Writer-Mutationen brauchen einen Claim oder
einen gleichwertigen nativen Lock.

### 7. Systeme ohne native Event-Hooks (Letter-Hooker-Erweiterung)


Token- oder Abo-Limitierung als Kapazitätszustand behandeln, nicht als
kaputten Akteur. Delegierte Abdeckung zurückgeben, nachdem der ursprüngliche
Akteur einen erfolgreichen Beleg liefert.

## Pflicht-Ausgaben

Für jeden Setup- oder Care-Lauf berichten:

- entdeckte native Oberfläche und nicht unterstützte Fähigkeiten;
- gewählte Topologie und angelegte, vorgeschlagene oder übersprungene
  Tasks;
- exakte Mutation und Vorher-/Nachher-Readback;
- Ergebnis-Beleg oder offenes Beobachtungsfenster;
- Rollback-Ort und Rückkehrbedingung;
- geteiltes Abdeckungs-Update, falls eine Koordinations-Registry existiert.

## Beispiel

Nutzer: "Richte selbst-wartende Zeitpläne in dieser Desktop-App ein."

Entdecken, ob die App geplante Tasks auflisten, anlegen, aktualisieren und
verifizieren kann. Den kompakten Plan erzeugen, nicht unterstützte
Fähigkeiten darlegen, dann nur die freigegebenen Tasks über die native
Oberfläche installieren. Ein Ordner mit einem Task-Prompt ohne
Live-Scheduler-Registrierung ist kein abgeschlossenes Setup.

## Changelog

### 1.1.0 (2026-08-30)

- Anbieterneutrales `app_display_name` und das sichtbare Titelformat
  `<APP_DISPLAY_NAME> — <CARE_TITLE>` ergänzt, inklusive `CODEX — ...` über
  das Codex-Adapter-Profil.
- Plan-Linting, Stabile-ID-/Semantik-Abgleich und Duplikat-Schutz ergänzt.
- Klargestellt, dass Naming zusätzlich zum Recovery Floor gilt und dass
  reine Titel-Migrationen jeden Nicht-Titel-Fingerprint bewahren müssen.

### 1.0.1 (2026-07-30)

- Anbieterneutrale Text-Automations- und Desktop-App-Automations-Aliase
  ergänzt.

### 1.0.0 (2026-07-28)

- Die ursprüngliche ANTIGRAVITY-Wartungsfamilie, die F1-F6-Regelschleife und
  spätere anbieterspezifische Anpassungen zu einem neutralen
  Core-Set-Skill konsolidiert.
