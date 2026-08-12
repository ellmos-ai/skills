---
name: software-in-worten
version: 1.0.0
type: method
author: ellmos (aus einem Entwurfsgespräch von Lukas Geiger, 2026-08-02)
created: 2026-08-02
description: >
  Übersetzt zwischen Benutzeroberfläche und Text — in beide Richtungen. Aus einer
  beschriebenen Oberfläche wird ein Skill; aus einem Skill wird eine Oberfläche. Nutzen,
  wenn eine Anwendung entworfen wird und der Ablauf noch unklar ist, wenn ein bestehendes
  Werkzeug als Skill verfügbar gemacht werden soll, wenn Oberfläche und Agentenzugang
  auseinanderdriften, oder wenn ein Skill zu lang wird und niemand weiß warum.
category: dev
tags: [design, ui, skills, methodik, uebersetzung, entwurf]
language: de
status: stable
standalone: true
---

# Software in Worten

## Der Gedanke

Menschen entwerfen **visuell**: *Wie will ich das bedienen?* Agenten lesen **Text**.
Solange beides getrennt entsteht, driftet es auseinander — die Oberfläche kann etwas, das
der Skill nicht kennt, und umgekehrt.

Beides ist aber dasselbe, nur in verschiedenen Aggregatzuständen. Es gibt eine
Übersetzung, und wer sie kennt, arbeitet in beide Richtungen:

> **Aus Worten eine Oberfläche entwerfen. Und eine Oberfläche zurück in Worte bringen.**

---

## Die Übersetzungstabelle

| In der Oberfläche | Was es bedeutet | In Text |
|---|---|---|
| **Mauszeiger** | *ich kann auswählen* — der Raum des Möglichen | die Menge der Optionen an dieser Stelle |
| **Markieren** | *das will ich haben* | eine Auswahl, ein Wert |
| **Klick** | *ich entscheide mich, ich will dahin* | **der Prompt** — die Antwort des Nutzers |
| **Feld, Schalter, Einstellung** | eine Entscheidung, die bleibt | **Config** |
| **Einstellungen der ganzen Software** | Entscheidungen, die überall gelten | **Policies** |
| **Formular, Eingabemaske** | eine Sammlung zusammengehöriger Entscheidungen | **Template** |
| **Knopf, der etwas startet** | *jetzt passiert etwas* | **Skill** oder **Workflow** wird ausgelöst |
| **Was danach abläuft** | die Schrittfolge | Anweisungen im Skill — oder ein **Skript** |
| **Fortschrittsanzeige** | *es läuft, und wie weit* | Statusmeldungen im Ablauf |
| **Erfolgsmeldung, Ergebnisansicht** | *das kam heraus* | die Rückgabe — in der Oberfläche nur schöner gesetzt |
| **Projekt** | ein abgegrenzter Arbeitsstand | ein **Ordner** — und weil er selbst in einem Ordner liegt, Teil der Software |
| **Ansicht, Tab, Bereich** | ein Zustand, in dem man gerade ist | ein Schritt im Ablaufbaum |

**Die zentrale Zeile ist der Klick.** Ein Klick ist nichts anderes als das, was ein Nutzer
im Gespräch sagen würde — nur schneller. **Der Klick ist der Prompt.** Und auf einen Prompt
folgt eine Reaktion: eine neue Frage, eine neue Ansicht, ein neuer Zustand.

---

## Der Ablauf ist ein Baum

Jede Anwendung ist eine Folge von Entscheidungen, zwischen denen etwas passiert:

```
Voraussetzungen geklärt?   →  Referenzen · Kandidatenliste · Nummern · Reihenfolge
        ↓
Einverständnis des Nutzers →  START
        ↓
Will er mitlesen?          →  ja: Mitleseansicht öffnen
Will er Zwischenmeldungen? →  ja: bei jedem Ereignis melden (durch, abgelehnt, Status)
        ↓
        [ AUSFÜHRUNG — oft ausgelagert an andere Software ]
        ↓
Rückgabe kommt zurück      →  auswerten
        ↓
Was will er wissen?        →  das Ergebnis in seinen Begriffen:
                              „bestellt bei X, 40 Minuten, 30 Euro"
```

**Drei Teile, immer dieselben:**

1. **Entscheidungen** — wenn-dann, bis alles Nötige beisammen ist
2. **Ausführung** — häufig gar nicht im eigenen Werkzeug, sondern ausgelagert
3. **Rückmeldung** — das Ergebnis zurück an den Menschen, in seiner Sprache

Der dritte Teil wird beim Entwurf am häufigsten unterschätzt. **Kommunikation läuft über
die Sinne** — als Text, als Bild, als Ton. Eine Oberfläche gestaltet das aus; ein Skill
beschreibt, *was* gemeldet wird und *wann*.

---

## Die Zwischenebene: das Blueprint

Zwischen „beschrieben" und „gebaut" fehlt eine Stufe. Sie heißt **Blueprint** und ist
**Text, dessen Anordnung dem Bild entspricht** — ein Screen, den man lesen kann:

```
 Worauf hast du Hunger?   [ Burger                        ]
 Wohin liefern?           [ Dorfstraße 1, 16321 Bernau    ]
 Höchstbetrag             [ 35 ] €   ⓘ Endbetrag an der Haustür
 Modus                    (•) Lieferung  ( ) Tisch  ( ) Abholung

 Kandidaten (ziehen zum Umsortieren)            ↻ neu suchen
 ┌────────────────────────────────────────────────────┐
 │ ≡ 1  Burger House Dorfstadt      ★ Favorit   offen │
 │ ≡ 2  Pizzeria Roma                            offen │
 └────────────────────────────────────────────────────┘

 [ Trockenlauf ansehen ]   [ Wirklich anrufen → 4 Anrufe, ~0,20 € ]
```

**Warum diese Stufe so viel bringt:**

Ein Blueprint ist **gleichzeitig lesbar und ansehbar**. Der Mensch sieht sein Bild wieder,
der Agent sieht Felder, Typen und Reihenfolge. Es entsteht in Minuten, kostet nichts und
lässt sich im Gespräch korrigieren — anders als eine gebaute Oberfläche.

**Und aus dem Blueprint fällt der Skill fast von selbst:**

> **Was muss der Agent können, wissen und tun — in welcher Reihenfolge —
> um dieses Blueprint auszufüllen?**

Jedes Feld wird eine Frage. Die Anordnung wird die Reihenfolge. Was vorbelegt ist, wird
nicht gefragt. Was als Knopf dasteht, wird ein Schritt. Danach reichert man an, was der
Agent zusätzlich wissen muss — Fachwissen, Grenzen, Fallstricke.

**Drei Stufen also:** Beschreibung → **Blueprint** → Skill *(und von dort ebenso gut in
eine gebaute Oberfläche)*.

## Richtung 1: Aus Worten eine Oberfläche

**Wenn zuerst der Ablauf beschrieben wurde.**

1. **Entscheidungen sammeln.** Jede Stelle, an der etwas festgelegt wird. Dabei sortieren:
   - **Pflicht** — ohne das geht es nicht weiter → **Muss-Feld**
   - **Ableitbar** — kann aus Kontext oder Bestand kommen → **vorbelegtes Feld** mit
     Korrekturmöglichkeit
   - **Optional** — verbessert das Ergebnis → **zugeklappter Bereich**
   - **Gate** — unumkehrbar, kostet Geld, erreicht Menschen → **Bestätigungsschritt**
2. **Zusammengehöriges bündeln** → eine Maske, ein Template.
3. **Den Baum in Ansichten schneiden.** Ein Zustand = eine Ansicht.
4. **Rückmeldungen entwerfen.** Was wird wann gemeldet? Fortschritt, Zwischenstand,
   Ergebnis.
5. **Was durchgehend gilt, einmal festlegen** — Farbe, Typografie, Schnitt, Bewegung.
   Das sind Policies für die Oberfläche.

**Der Gewinn:** Ein Formular, das aus einem Gesprächsablauf entsteht, ist fast immer
schlanker als eines vom Reißbrett. Man merkt beim Formulieren, welche Frage überflüssig ist.

## Richtung 2: Aus einer Oberfläche Worte

**Wenn die Anwendung schon existiert oder beschrieben ist.**

1. **Jeden Klick als Frage formulieren.** Was fragt dieser Knopf den Nutzer eigentlich?
2. **Jedes Feld als Config-Eintrag** — mit Vorgabewert, Typ und Hilfetext.
3. **Jede Ansicht als Schritt** im Ablauf.
4. **Jede Meldung als Rückgabe** — was wird berichtet, in welchen Worten?
5. **Prüfen, was die Oberfläche implizit weiß** — Reihenfolgen, Sperren, Abhängigkeiten,
   die nirgends stehen, sondern nur im Layout stecken. **Das ist der Teil, der beim
   Übersetzen am leichtesten verlorengeht.**

### Warum diese Richtung schwerer ist — und wie man sie trotzdem geht

Richtung 1 fällt leicht, Richtung 2 fühlt sich zäh an. Das hat einen Grund:

> **Ein Skill ist Zeit. Ein Screen ist Fläche.**
> Erst dies, dann jenes — gegen alles gleichzeitig sichtbar.

Man übersetzt also nicht Zeile für Zeile, sondern **schneidet einen Ablauf in Flächen**.
Die Schnittkante ist immer dieselbe:

**Ein Screen entsteht dort, wo der Ablauf auf einen Menschen wartet.**

Alles zwischen zwei Wartepunkten läuft von selbst — das wird **kein** Screen, sondern
höchstens eine Fortschrittsanzeige. Wer für jeden Schritt eine Ansicht baut, baut ein
Klickgefängnis.

**Und die wenn-dann-Ketten?** Sie werden nicht alle sichtbar. Vier Fälle:

| Art der Bedingung | Was daraus wird |
|---|---|
| **Der Mensch legt sie fest** („höchstens 35 €") | ein **Feld** — vor dem Start |
| **Das System prüft sie** („Preis über Limit") | ein **Ergebnis** — danach, mit Begründung |
| **Sie ändert, was der Mensch sieht** („kein Treffer") | ein **Zustand** desselben Screens, kein neuer |
| **Sie ist reine Mechanik** (Wiederholungen, Zeitüberschreitungen, Formatprüfung) | **gar nichts** — sie bleibt unsichtbar |

**Der vierte Fall ist der häufigste.** Die meisten Verzweigungen eines Skripts gehören nie
auf einen Bildschirm. Wer sie trotzdem zeigt, verwechselt Ablaufdiagramm mit Oberfläche.

**Praktisch in vier Schritten:**

1. **Wartepunkte markieren** — jede Stelle, an der ein Mensch entscheidet, bestätigt oder
   etwas eingibt. Das sind die Screens, und es sind meist überraschend wenige.
2. **Rückwärts einsammeln** — was muss vor diesem Wartepunkt bekannt sein? Diese Werte
   sind die Felder des Screens.
3. **Vorwärts einsammeln** — was passiert danach, und was davon muss der Mensch erfahren?
   Das ist die Rückmeldung.
4. **Den Rest weglassen** — alles, was weder Eingabe noch Meldung ist, bleibt unsichtbar.

---

## Der Gradient: Skill ↔ Skript

```
weit von der Software                                    nah an der Software
   Skill trägt alles                                    Skript trägt alles
        │                                                       │
   ausführlicher Text          ────────────►         knappe Bedienungsanleitung
   jeder Schritt erklärt                             „ruf dies auf, dann jenes"
   funktioniert ohne Werkzeug                        funktioniert nur mit Werkzeug
```

**Je mehr ein Vorgang automatisiert ist, desto weniger muss der Skill erklären.**
Er wird kürzer und konkreter — irgendwann ist er kaum mehr als eine Bedienung für die
Skripte: *wann nimmt man dieses Werkzeug, was gibt man hinein, woran erkennt man, dass es
geklappt hat.*

Zwei Umkehrschlüsse, die im Alltag helfen:

- **Wird ein Skill zu lang, fehlt ein Skript.** Länge ist ein Signal: Was sich wiederholt
  und mechanisch ist, gehört automatisiert.
- **Wird ein Skript unverständlich, fehlt ein Skill.** Ein Werkzeug ohne Text darüber ist
  nur für den benutzbar, der es gebaut hat.

---

## Die gemeinsame Währung

**Jede Einstellung existiert dreifach** — als Config-Wert, als Frage im Skill, als Feld in
der Oberfläche. Damit sie nicht auseinanderlaufen, wird die Darstellung **einmal**
beschrieben und von allen dreien gelesen:

```yaml
field: sample.method
label: "Ziehungsverfahren"                       # Oberfläche
question: "Wie soll gezogen werden — zufällig, geschichtet oder alle?"   # Skill
type: choice
options: [random, stratified, census]
default: random
help: "Geschichtet nur, wenn die Merkmale in der Grundlage stehen."
locked: false        # true = nicht abschaltbar, erscheint in keiner Oberfläche
```

**Was `locked` ist, taucht nirgends als Option auf.** Manche Dinge sind keine Einstellung,
sondern Teil des Gerüsts.

---

## Wann dieser Skill hilft

- Eine Anwendung wird entworfen und der Ablauf ist noch unklar → **Richtung 1**
- Ein bestehendes Werkzeug soll für Agenten nutzbar werden → **Richtung 2**
- Oberfläche und Agentenzugang driften auseinander → **gemeinsame Währung** einführen
- Ein Skill wird zu lang und niemand weiß warum → **Gradient** prüfen
- Ein Entwurfsgespräch soll festgehalten werden, bevor es verfliegt → Tabelle + Baum

## Verwandtes

`condition` übersetzt Bedingungen, Zeitpunkte und Reihenfolgen in prüfbare Gates
(`/if`, `/when`, `/after`, `/and`, `/or`) — dieselbe Bewegung für den Sonderfall Ablaufsteuerung.
`skill-extractor` gewinnt Skills aus Gesprächsverläufen. `plugin-system` macht eigene
Skripte auffindbar.
