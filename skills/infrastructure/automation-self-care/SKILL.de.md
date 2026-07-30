---
name: automation-self-care
version: 1.0.1
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-07-30
description: >
  Erstellt und betreibt ein anbieterneutrales Selbstpflege-Kernset für geplante
  LLM-Aufgaben und Desktop-App-Automationen. Verwenden, wenn ein Agent seinen
  nativen Scheduler ermitteln, wiederkehrende Prüfungen für Hygiene,
  Promptqualität, Häufigkeit, Last, Ressourcen, systemübergreifende Abstimmung,
  Berechtigungen und Laufzeit einrichten oder einen vorhandenen
  Automationsbestand mit Rollback, Readback und Löschschutz kontinuierlich
  verbessern soll. Auslöser sind unter anderem Automations-Selbstpflege,
  Scheduler-Aufgabenpflege, Pflege von Desktop-App-Automationen,
  Automationsbestands-Audit, selbstheilende Zeitpläne sowie Anfragen zur
  Wiederherstellung der ANTIGRAVITY-artigen Wartungsaufgabenfamilie,
  core-set-textautomations, basic-text-automations, textbased-automation-core,
  textbased-automation-drivers oder textbased-desktopapp-automations.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system]
language: de
status: active
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
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="automation-self-care banner">

# Automations-Selbstpflege

Erstelle aus einem anbieterneutralen Regelkreis einen nativen,
anbieterspezifischen Wartungsbestand. Bewahre die ursprüngliche Absicht der
ANTIGRAVITY-Aufgabenfamilie, verlange aber Nachweise, reversible Änderungen und
nativen Readback.

## Nicht verhandelbare Grenzen

- Behandle Ermittlung, Planung, Freigabe, Änderung und Readback als getrennte
  Phasen.
- Nutze die unterstützte Automations-API, den unterstützten Befehl oder die
  unterstützte Benutzeroberfläche der Zielanwendung. Unterstelle niemals, dass
  das Bearbeiten einer Speicherdatei den Live-Zustand der Anwendung verändert.
- Lies lokale Regeln, Sperren, Lösch- und Unterdrückungsprotokolle sowie
  vorhandene Zeitpläne, bevor du eine Aufgabe vorschlägst.
- Erfinde keine Scheduler-Unterstützung. Wenn Erstellen, Aktualisieren und
  Readback nicht belegt werden können, erstelle einen manuellen
  Installationsplan und halte vor jeder Änderung an.
- Nimm pro Pflegelauf höchstens eine unabhängig prüfbare Feinabstimmung vor.
- Verhindere, dass Pflegeaufgaben sich selbst deaktivieren oder ihre eigene
  Taktung unter die konfigurierte Wiederherstellungsuntergrenze absenken.
- Bewahre vorherigen Prompt, Zeitplan, Modell, Berechtigungen und
  Aktivierungszustand, damit jede Änderung zurückgerollt werden kann.
- Werte einen Lauf erst mit Ergebnisnachweis als erfolgreich, nicht schon bei
  Scheduler-Start oder Exit-Code 0.
- Kopiere niemals Geheimnisse, private Prompts oder personenbezogene Daten in
  eine gemeinsame Registry.

## Arbeitsablauf

### 1. Native Automationsoberfläche ermitteln

Inventarisiere den aktuellen Akteur, Anbieter, die App-Klasse,
Scheduler-Oberfläche, unterstützte Operationen, Zustandsdateien, Laufhistorie,
Nutzungsmetrik und Readback-Methode. Erfasse Fähigkeiten nach dem Profilvertrag
in [provider-adapter-contract.md](references/provider-adapter-contract.md).

Unterscheide native Desktop-App-Zeitpläne, CLI-/Headless-Ausführung,
Betriebssystem-Scheduler oder Service-Starter, allgemeine Scheduler-Dienste,
Workflow-Engines sowie nicht unterstützte oder ausschließlich über die
Benutzeroberfläche bedienbare Automationen. Setze das Vorhandensein einer
Konfigurationsdatei nicht mit einem unterstützten Änderungsweg gleich.

### 2. Automationsbestand erfassen

Erfasse für jede Aufgabe eine stabile lokale Kennung, Zweck,
Prompt-Fingerabdruck, Zeitplan, Aktivierungszustand, Modell, Berechtigungen,
Zielpfade, letztes Scheduler-Ereignis, letztes erfolgreiches Ergebnis und
aktuelle Zuständigkeit. Der Prompt-Inhalt bleibt lokal.

Prüfe die maßgebliche Live-Oberfläche vor einer Änderung zweimal, wenn die App
den Zustand aus dem Speicher zurückschreiben kann.

### 3. Kernset entwerfen

Lies [core-set.md](references/core-set.md). Wähle:

- `compact`: fünf Pflegeaufgaben, die Häufigkeit und Lastverteilung kombinieren;
  oder
- `full`: neun fokussierte Aufgaben entsprechend der ursprünglichen
  Wartungsfamilie.

Erzeuge einen anbieterneutralen Plan:

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
```

Der Generator installiert niemals Aufgaben. Prüfe jede als `blocked`
gekennzeichnete Fähigkeit und wähle kollisionsfreie lokale Zeiten, bevor du den
Plan anwendest.

### 4. Installation vorbereiten

Installiere über den nativen Anbieteradapter:

1. Beginne mit Hygiene im Nur-Lese-Modus.
2. Ergänze Ressourcenschutz.
3. Ergänze Promptqualitäts-Abstimmung mit Rollback.
4. Ergänze Häufigkeits- und Lastabstimmung erst, wenn genügend Laufnachweise
   vorliegen.
5. Ergänze systemübergreifende Koordination zuletzt.

Erstelle neue oder importierte Aufgaben deaktiviert, sofern der Nutzer die
aktive Installation nicht ausdrücklich freigegeben hat. Verlange für einen
unbeaufsichtigten Pilotbetrieb zuerst ein Löschprotokoll, einen
Vorher-Zustandssnapshot, einen Laufbeleg und einen Rollback-Pfad.

### 5. Pflegeregelkreis ausführen

Jede Pflegeaufgabe folgt diesem Ablauf:

```text
vorherige Änderung nachverfolgen
  -> aktuelle Nachweise sammeln
  -> eine Ursache klassifizieren
  -> keine oder genau eine Änderung wählen
  -> über die native Oberfläche ändern
  -> Readback durchführen
  -> Beleg und Bedingung für die nächste Prüfung schreiben
```

Nutze den Hypothesenkatalog und die Nachweisregeln in
[core-set.md](references/core-set.md). Bei unbekannter Ursache beobachten,
Berechtigungen einschränken oder sicher pausieren; niemals eine Reparatur
erraten.

### 6. Akteure koordinieren

Der lokale App-Zustand bleibt maßgeblich. Teile nur Aufgabenverträge, Abdeckung,
Status, Belege und bereinigte Fingerabdrücke. Redundante Nur-Lese-Prüfungen sind
zulässig; Änderungen mit genau einem Schreiber benötigen einen Claim oder eine
gleichwertige native Sperre.

### 7. Systeme ohne native Event-Hooks (Letter-Hooker-Erweiterung)

Behandle Token- oder Abonnementbegrenzungen als Kapazitätszustand, nicht als
defekten Akteur. Übergib delegierte Abdeckung zurück, sobald der ursprüngliche
Akteur einen erfolgreichen Beleg erzeugt.

## Erforderliche Ausgaben

Berichte für jeden Einrichtungs- oder Pflegelauf:

- ermittelte native Oberfläche und nicht unterstützte Fähigkeiten;
- gewählte Topologie sowie erstellte, vorgeschlagene oder übersprungene
  Aufgaben;
- genaue Änderung und Readback des Vorher-/Nachher-Zustands;
- Ergebnisnachweis oder offenes Beobachtungsfenster;
- Rollback-Ort und Rückkehrbedingung;
- aktualisierte gemeinsame Abdeckung, sofern eine Koordinations-Registry
  existiert.

## Beispiel

Nutzer: „Richte in dieser Desktop-App selbstpflegende Zeitpläne ein.“

Ermittle, ob die App geplante Aufgaben auflisten, erstellen, aktualisieren und
verifizieren kann. Erzeuge den kompakten Plan, zeige nicht unterstützte
Fähigkeiten und installiere anschließend nur die freigegebenen Aufgaben über die
native Oberfläche. Ein Ordner mit einem Aufgaben-Prompt ohne Live-Registrierung
im Scheduler ist keine abgeschlossene Einrichtung.

## Änderungsprotokoll

### 1.0.1 (2026-07-30)

- Anbieterneutrale Aliasse für Textautomationen und
  Desktop-App-Automationen ergänzt.

### 1.0.0 (2026-07-28)

- Die ursprüngliche ANTIGRAVITY-Wartungsfamilie, der F1-F6-Regelkreis und
  spätere anbieterspezifische Anpassungen zu einem neutralen Kernset-Skill
  zusammengeführt.
