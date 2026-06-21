---
name: trampelpfadanalyse
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-06-21
updated: 2026-06-21
description: >
  Fehleranalyse in Pipeline- und Steuerdatei-Abläufen: prüfen, ob eine Konvention
  oder ein Verfahren für ein LLM überhaupt sichtbar und auffindbar ist. Empirischer
  Baseline → Intervention → Retest-Vergleich mit naiven Subagenten (eigene isolierte
  Sandbox-Kopien, gleicher Testfall, quantitative Erfolgsmessung). Nutze diesen Skill,
  wenn Agenten eine Regel/README/Konvention wiederholt ignorieren oder falsch
  navigieren und du messen willst, ob eine Doku-Änderung das Verhalten tatsächlich
  ändert. Triggert bei "wird die Konvention überhaupt gesehen", "warum hält sich
  kein Agent an die Regel", "Doku-Schild messbar wirksam machen", "Trampelpfadanalyse".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [workflow, fehleranalyse, llm-ux, doku-audit, baseline-retest, naive-subagent, empirisch, pipeline, steuerdatei]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/system/trampelpfadanalyse.md"
  origin_version: "2.0"
  origin_repo: "github.com/ellmos-ai/swarm-ai"
  last_sync_from_origin: "2026-06-21"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Trampelpfadanalyse — LLM-sichtbare Konventionen empirisch herstellen

Eine Methode, um Fehler in Pipeline- und Steuerdatei-Abläufen aufzudecken, die nicht
durch falschen Code entstehen, sondern dadurch, dass eine **Konvention für ein LLM
unsichtbar** ist. Statt zu raten, ob eine README oder Regel "klar genug" ist, wird
empirisch gemessen: naive Subagenten ohne Vorwissen werden auf den Ablauf losgelassen,
ihr Verhalten wird zur **Baseline**, eine gezielte Doku-Änderung ("Schild") ist die
**Intervention**, und frische naive Subagenten liefern den **Retest**. Der Diff zur
Baseline ist die Erfolgsmessung.

Der Name kommt vom Trampelpfad (engl. *desire path*): dort, wo Menschen tatsächlich
laufen statt auf dem angelegten Weg, gehört ein Weg hin. Analog zeigen die Pfade naiver
LLMs, wo Doku/Leitplanken tatsächlich gebraucht werden — nicht dort, wo wir sie vermuten.

## Wann diesen Skill nutzen

- Agenten ignorieren wiederholt eine Regel/Konvention, obwohl sie dokumentiert ist.
- Du willst wissen, ob ein Verfahren für ein LLM **sichtbar/auffindbar** ist, bevor du
  weitere Doku schreibst ("redet hier jemand gegen eine Wand?").
- Nach einer Umstrukturierung (neue Verzeichnisse, Umbenennungen): Finden Agenten noch
  die Einstiegspunkte?
- Du hast eine Doku-Änderung gemacht und willst **belegen**, dass sie wirkt — nicht nur
  hoffen.
- Onboarding-Test vor dem Einbinden neuer LLM-Partner in eine Pipeline.

Nicht hierfür: reine Code-Bugs (→ systematisches Debugging), oder die Auswahl von
Schwarm-Koordinationsmustern für eine Produktivaufgabe (→ siehe `swarm-operations`).
Dieser Skill nutzt einen Schwarm naiver Agenten ausschließlich als **Messinstrument**.

## Kernidee in einem Satz

Behandle Dokumentation wie UX: was zählt, ist nicht was du geschrieben hast, sondern
was ein unvoreingenommener Nutzer (hier: ein naiver Agent) damit tatsächlich tut —
und das misst man, ändert man, und misst man erneut.

---

## Der Prozess: 5 Schritte

```
1. BASELINE        naive Subagenten → Ist-Verhalten messen (quantitativ)
2. PFAD-ANALYSE    wo genau scheitert es? welche Doku-Stelle führt fehl?
3. INTERVENTION    "Schild" aufstellen (README/Konvention prominenter)
4. RETEST          FRISCHE naive Subagenten, gleicher Testfall
5. DIFF            Retest vs. Baseline → Erfolgsmessung + ehrliche Einordnung
```

### Schritt 1 — Baseline: Ist-Verhalten naiv messen

Formuliere zuerst die **Problemlage als prüfbare Frage**, z. B. "Legt ein Agent ein
Log an der konventionsgemäßen Stelle an?" oder "Findet ein Agent den Einstiegspunkt
der Pipeline?".

Setze dann naive Subagenten auf:

- **Naiv heißt:** kein Projekt-Gedächtnis, keine Skills, keine Vorab-Hinweise — der
  Agent kennt nur den Einstiegspfad und den Auftrag. So misst du **reine Auffindbarkeit
  über die vorhandene Doku**, nicht das Vorwissen des Agenten.
- **Isolierte Sandbox-Kopien:** Jeder Probe-Agent arbeitet auf einer eigenen Kopie des
  betroffenen Ordners/Ablaufs, damit sich die Proben nicht gegenseitig beeinflussen und
  der echte Stand unverändert bleibt.
- **Gleicher Testfall, mehrere Wiederholungen:** Variabilität ist real. Eine Probe ist
  ein Anekdote; n Wiederholungen (z. B. 3, oder bei Bedarf mehr) ergeben eine Quote.
- **Günstiges, "naives" Modell** ist ausreichend und realistisch — es soll nicht klug
  raten, sondern zeigen, wohin die Doku einen durchschnittlichen Agenten führt.

Minimaler Probe-Prompt (Platzhalter anpassen):

```
Du erkundest <SYSTEM>. Es liegt unter: <PFAD>.
AUFTRAG: <konkreter Auftrag>.
REGELN:
1. Du weißt NUR den Pfad oben, sonst nichts.
2. Erkunde, um den Auftrag zu erfüllen. Max. <N> Schritte.
3. Berichte am Ende: BESUCHTE_VERZEICHNISSE, GELESENE_DATEIEN,
   AUFTRAG_ERFÜLLT (ja/nein), HILFREICHSTE_DATEI.
```

**Festhalten als Baseline-Metriken** (immer quantitativ, nie "fühlt sich besser an"):

| Metrik | Bedeutung |
|---|---|
| Erfolgsquote | wie oft wurde der Auftrag konventionsgemäß erfüllt (z. B. 0/3) |
| Falschverhalten | wie oft die falsche Stelle/Methode (z. B. 3/3 Sammel-Log statt per-Eintrag) |
| Pfade bis Ziel | wie viele Schritte/Umwege bis zum Ziel |
| Blind Spots | welche relevante Datei/Stelle niemand öffnet |

### Schritt 2 — Pfad-Analyse: wo scheitert es real?

Werte die Probe-Berichte gemeinsam aus (eine "Heatmap" über besuchte Stellen reicht):

- Welche Datei wird **häufig** gelesen (HOT)? Wenn dort die Orientierung fehlt, ist das
  der wirksamste Ort für ein Schild.
- Welche relevante Stelle wird **nie** geöffnet (COLD / Blind Spot)? Sie ist faktisch
  unsichtbar — egal wie gut ihr Inhalt ist.
- Wo dreht ein Agent **Schleifen** oder greift an der Konvention vorbei (Sackgasse,
  Umgehung)? Das markiert die konkrete Doku-Lücke.

Befund-Tabelle:

| Befund | Bedeutung | Maßnahme (→ Schritt 3) |
|---|---|---|
| HOT + keine Orientierung | viel Traffic, kein Wegweiser | Schild genau dort platzieren |
| WARM + Fehler | Agenten kommen hin, straucheln | Beispiel/Klarstellung ergänzen |
| COLD | Stelle wird nie gefunden | von einer HOT-Datei aus verlinken |
| Umgehung | Konvention wird übergangen | Hinweis an den Ort der Umgehung |

Ergebnis von Schritt 2: **eine konkrete, lokalisierte Hypothese** — "Agenten lesen X,
aber X erwähnt die Konvention nicht; deshalb landen sie bei Y."

### Schritt 3 — Intervention: ein Schild aufstellen

Stelle **genau ein** Schild auf (eine Variable pro Durchgang, sonst ist der Diff nicht
interpretierbar). Typische Schilder:

- Die Konvention **dort** prominent platzieren, wo der HOT-Pfad ohnehin vorbeikommt
  (z. B. ein kurzer, expliziter Hinweis ganz oben in der meistgelesenen README/Steuerdatei).
- Eine **Schnellnavigations-Tabelle** am Anfang der zentralen Architektur-/Übersichtsdatei,
  die auf bisherige Blind Spots zeigt.
- Einen **Wegweiser/Verweis** von einer HOT-Datei zu einer COLD-Stelle.
- Optional eine **Leitplanke** (z. B. ein PreToolUse-Hinweis) für gefährliche oder
  konventionswidrige Aktionen.

Halte das Schild kurz und unübersehbar — Agenten überfliegen, sie lesen selten lang.

### Schritt 4 — Retest mit FRISCHEN naiven Subagenten

Wiederhole Schritt 1 **identisch** — gleicher Auftrag, gleiche Wiederholungszahl,
gleiches Modell, gleiche Naiv-Bedingung — aber auf Sandbox-Kopien **mit** dem neuen
Schild. Wichtig:

- **Frische** Agenten ohne Erinnerung an den Baseline-Lauf (sonst misst du Lernen statt
  Auffindbarkeit).
- **Nur das Schild** unterscheidet sich vom Baseline-Setup.

### Schritt 5 — Diff zur Baseline + ehrliche Erfolgsmessung

Stelle Retest und Baseline direkt gegenüber:

| Metrik | Baseline | Nach Schild | Δ |
|---|---|---|---|
| Erfolgsquote | z. B. 0/3 | z. B. 3/3 | +3 |
| Falschverhalten | z. B. 3/3 | z. B. 0/3 | −3 |
| Blind Spots | z. B. 1 | z. B. 0 | −1 |

Einordnung — und hier nicht schönen:

- **Wirkt** (Falschverhalten geht messbar zurück): Schild behalten, dokumentieren.
- **Wirkt nicht** (kaum Δ): Schild war am falschen Ort oder zu unauffällig → zurück zu
  Schritt 2/3, anderes Schild, erneut messen.
- **Grenzen offen benennen:** kleine n sind Indizien, keine Beweise; ein naiver Agent
  ist ein Modell für "durchschnittlich uninformiert", nicht für jeden realen Nutzer;
  False Positives/Negatives bei der Erfolgsbewertung explizit prüfen (was genau zählte
  als "erfüllt"?).

---

## Mini-Fallbeispiel (real, mit echten Zahlen)

Problemlage: Eine Ticket-Pipeline schrieb vor, dass triviale Erledigungen je **ein**
eigenes Per-Ticket-Log bekommen — Agenten legten aber stattdessen alles in **ein
Sammel-Log**.

- **Schritt 1 (Baseline):** 3 naive Subagenten, gleicher Auftrag → **3/3 nutzten das
  Sammel-Log** (Konvention nicht befolgt).
- **Schritt 2 (Pfad-Analyse):** Die meistgelesene README erwähnte die Per-Ticket-Regel
  nicht an sichtbarer Stelle → der naive Pfad führte zum Sammel-Log.
- **Schritt 3 (Intervention):** Ein kurzes, explizites "Schild" zur Logging-Konvention
  prominent in der README platziert.
- **Schritt 4 (Retest):** 3 frische naive Subagenten, identischer Auftrag.
- **Schritt 5 (Diff):** **3/3 falsch → 0/3 falsch**, alle drei legten ein korrektes
  Per-Ticket-Log an. (Dokumentiert in Ticket T-20260621-44.)

Lehre: Die Konvention war nicht "zu schwach formuliert" — sie war am gelesenen Pfad
**unsichtbar**. Das Schild am richtigen Ort, empirisch verifiziert, löste das Problem.

---

## Quelle und verwandte Methoden

Diese Methode stammt aus der Trampelpfadanalyse v2.0 (Schwarm als empirisches
Messinstrument für LLM-Verhalten). Die ursprünglichen Referenzergebnisse eines
Großversuchs (100 naive Proben) sind als Beleg der Quelle dokumentiert: größter Blind
Spot war ein Hilfe-Verzeichnis, das **0/100** Agenten besuchten (trotz vieler
Hilfe-Dateien), und die Aufgabe "neuen Skill erstellen" gelang **0%**, weil niemand das
Templates-Verzeichnis fand — beides klassische Sichtbarkeits-, keine Inhaltsprobleme.

## Siehe auch

- `swarm-operations` (dev) — Katalog der Schwarm-**Koordinationsmuster** für
  Produktivaufgaben; führt die Trampelpfadanalyse dort nur als Konzept-Abschnitt.
  Dieser Skill ist die anwendbare **Prozess**-Variante mit Baseline→Retest-Loop.
- `pipeline-optimizer` (dev) — 6-Schritte-Renovierung von Pipelines; der Retest mit
  frischen Subagenten dort entspricht Schritt 4–5 hier.
- `bugfix-protocol` / systematisches Debugging — für echte Code-Bugs statt
  Sichtbarkeitsprobleme.

## Changelog

### 0.1.0 (2026-06-21)
- Initiale Portierung aus der Trampelpfadanalyse v2.0 (Quelle: swarm-ai/BACH).
- Auf den anwendbaren 5-Schritte-Prozess fokussiert (Baseline → Pfad-Analyse →
  Intervention → Retest → Diff); Schwarm-Koordinationsmuster bewusst ausgelassen
  (bleiben bei `swarm-operations`). Nutzerneutral mit Platzhaltern; reales Mini-Beispiel.
