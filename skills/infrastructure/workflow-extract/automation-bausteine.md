# Automations-Bausteine — Checkliste für unbeaufsichtigte Workflows

Jede extrahierte Automatisierung gegen diese Liste halten. Die Bausteine stammen aus der
Analyse eines gewachsenen Bestands von Praxis-Automationen; fehlende Bausteine sind dort
die häufigsten Ursachen für Degeneration im Dauerbetrieb.

## 1. Rotations-Auswahl (bei Menge von Zielen)

Wenn die Automatisierung über eine Menge von Projekten/Ordnern/Objekten läuft: pro Lauf
GENAU EIN Ziel wählen, bevorzugt das am längsten ungeprüfte. Vorteile: kurze Läufe,
gleichmäßige Abdeckung, seltener Takt reicht. Details und Registry-Format: Skill
`rotation-check`.

## 2. Check-Registry + Log (Gedächtnis der Automation)

Ohne Gedächtnis prüft die Automation dasselbe Ziel doppelt und übersieht andere.

- **Registry** (kompakt, eine Zeile pro Check): Ziel | Datum | Checktyp | Ergebnis |
  nächster sinnvoller Schritt. VOR der Zielauswahl lesen.
- **Log** (Verlauf mit Details/Evidenz): kurzer Eintrag pro Lauf, auch bei Leerlauf.
- Eng verwandte Checktypen zählen mit: Wurde das Ziel gerade von einem verwandten Check
  angefasst, ausweichen oder read-only enden.

## 3. Vorbedingungen / Pflichtlektüre

Root-Dokumente der Ziel-Pipeline VOR der Arbeit lesen (Policies, Status, Namenskonventionen).
Als expliziten VORBEREITUNG-Block an den Prompt-Anfang — eine Automation, die Konventionen
nicht kennt, produziert Parallel-Standards.

## 4. Lock-/Koordinations-Respekt

Vor Schreibzugriffen prüfen, ob das Ziel gesperrt ist (Lock-Dateien, Claims, laufende
Pipelines anderer Agenten). Bei Sperre: ausweichen oder read-only enden — nie warten/blockieren.

## 5. Read-only-Exit („nichts zu tun" ist ein Ergebnis)

Expliziter Abbruchpfad: Wenn kein Handlungsbedarf, kurz dokumentieren und enden. Ohne diesen
Baustein „erfindet" die Automation Arbeit oder weitet ihren Scope aus. Formulierung im Prompt:
„Wenn keine Arbeit anfällt, dokumentiere kurz das geprüfte Ziel und beende den Lauf."

## 6. Idempotenz + Scope-Begrenzung

- Ein wiederholter Lauf über dasselbe Ziel darf nichts verschlimmern (keine doppelten
  Einträge, keine erneuten Umbenennungen).
- Scope hart begrenzen: „genau ein Projekt", „nur Dateien unter X", „keine neuen
  Ordnerstrukturen anlegen".
- Bei totem Pfad/verschobenem Ziel: nicht neu anlegen, sondern über die maßgebliche
  Registry/Statusdatei korrigieren und den Fehlpfad in ein Failure-Log schreiben.

## 7. Log-Hygiene (Cut-and-Archive)

Registry/Log wachsen unbegrenzt. Regel einbauen: Ab Überlänge (Erfahrungswert: wenn die Datei
unübersichtlich wird bzw. mehrere hundert Zeilen) alten Stand nach `_archiv/` verschieben,
frische Datei anlegen, im Kopf auf den Vorgänger verweisen (Pfad + Datum).

## 8. Dokumentationspflichten + Folgeaufgaben

Ergebnisse gehören an die Orte, wo Menschen/Agenten sie finden: projektlokale TODO/AUFGABEN
für Folgearbeiten, Pipeline-Registry für den Checkstand. Die Automation erledigt nicht alles
selbst — sie darf Aufgaben hinterlassen (z. B. „erneuter Upload nötig" in TODO.md).

## 9. Abschlussbericht

Kurzer strukturierter Schlussblock pro Lauf: Ziel | getan | Ergebnis | hinterlassene
Folgeaufgaben. Das ist die Schnittstelle für Monitoring und für den User, der Läufe
stichprobenartig kontrolliert.

## 10. Memory-/State-Regel (harness-spezifisch)

Wenn der Ziel-Scheduler ein Automations-Memory unterstützt, am Prompt-Ende festlegen, wohin
es geschrieben wird (mit Fallback-Pfad, falls Umgebungsvariable fehlt) und DASS es vor der
finalen Antwort geschrieben wird — sonst geht Lauf-zu-Lauf-Wissen verloren.

## 11. Encoding-/Sprach-Konventionen

Sprach- und Encoding-Regeln des Zielsystems explizit in den Prompt (z. B. „deutsche
End-User-Texte mit echten Umlauten: ä ö ü ß, nicht ae/oe/ue") — Automationen ohne diese
Zeile driften bei jedem Lauf ein Stück.

## Minimal-Gerüst (Vorlage)

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für diesen
<CHECKTYP> noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft, weiche aus oder beende read-only.

<KERNAUFGABE — was konkret geprüft/gepflegt wird und was bei Befund zu tun ist>

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registriere den Check kompakt in <REGISTRY> (Ziel, Datum, Checktyp,
Ergebnis, nächster Schritt) und schreibe einen kurzen Verlaufseintrag in <LOG>.
Folgearbeiten in die projektlokale <TODO-DATEI>. Werden <REGISTRY>/<LOG> zu lang:
alten Stand nach _archiv/ verschieben, frische Datei mit Verweis anlegen.

GUARDS: Respektiere Locks/Claims. Genau ein Ziel pro Lauf. Keine neuen
Ordnerstrukturen; tote Pfade über <STATUS-REGISTRY> korrigieren und in
<FAILURE-LOG> protokollieren.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```
