# Textproduction › pr — PR-Kommunikation

> Teilskill von `textproduction`. Router: `../SKILL.md`.
>
> Dokumente: Pressemitteilung (LaTeX-PDF), Positionspapier (LaTeX-PDF),
> Pitch Deck, Social-Media-Kit. Das `press_compiler.py`-Skript generiert
> PDFs ohne externe Dienste (nur MiKTeX/TeX Live noetig).

---

## Uebersicht

| Dokument | Tool | Format |
|---|---|---|
| Pressemitteilung | `press_compiler.py` + LaTeX | PDF |
| Positionspapier | `press_compiler.py` + LaTeX | PDF |
| Pitch Deck | Gamma, Canva (optional) ☁️ | PDF / Web |
| Social-Media-Kit | Canva, Ideogram (optional) ☁️ | PNG / Zip |

---

## 1. Pressemitteilung (LaTeX-PDF)

### Voraussetzungen

```bash
# MiKTeX (Windows) oder TeX Live (Mac/Linux) installieren
# Pakete: geometry, fancyhdr, graphicx, hyperref, babel, xcolor, parskip

# Pruefen ob pdflatex verfuegbar:
pdflatex --version
```

### Konfiguration einrichten

```bash
# Einmalig: Beispiel-Config kopieren und Daten eintragen
cp config.example.json config.json
# Dann config.json mit eigenen Kontaktdaten befuellen
```

`config.json`-Felder:
```json
{
  "author":             "Vollstaendiger Name",
  "organization":       "Organisation / Unternehmen",
  "contact_email":      "kontakt@beispiel.de",
  "contact_phone":      "+49 ...",
  "logo_path":          "",
  "default_language":   "ngerman",
  "output_dir":         "press_output/",
  "latex_compiler":     "pdflatex",
  "fallback_compiler":  "xelatex"
}
```

### Pressemitteilung erstellen

```python
# Aus Python importieren (Pfad auf pr/-Verzeichnis zeigen):
import sys
sys.path.insert(0, '/pfad/zu/textproduction/pr')
from press_compiler import compile_document

pdf_path = compile_document(
    doc_type="pressemitteilung",
    title="Kurzer, praegnanter Titel (max. 10 Woerter)",
    body="""
\\textbf{Lead-Absatz:} Wer, Was, Wann, Wo, Warum -- die 5 W in 2 Saetzen.

Zweiter Absatz: Hintergrund und Details.

Dritter Absatz: Zitat.
\\begin{quote}
``Diese Entwicklung zeigt...'' -- Name, Rolle
\\end{quote}

Vierter Absatz: Ausblick / naechste Schritte.

\\textit{\\textbf{Ueber [Organisation]:}} Kurztext 2--3 Saetze (Boilerplate).
""",
    output_path="press_output/pm_2026-06-22.pdf"
)
print(f"PDF erstellt: {pdf_path}")
```

```bash
# Oder per CLI (Templates pruefen):
PYTHONIOENCODING=utf-8 python press_compiler.py --list-templates
```

### Aufbau einer Pressemitteilung

```
Headline:    Aktiv formuliert, max. 10 Woerter, Hauptaussage
Unterzeile:  Optional, ergaenzt die Headline

Lead:        5 W in 1-2 Saetzen (Wer? Was? Wann? Wo? Warum?)
Body:        Details, Kontext, Hintergrund (3-4 Absaetze)
Zitat:       1-2 direkte Zitate mit Name und Titel der Person
Boilerplate: "Ueber [Organisation]" -- standardisierter Abschlusstext
Kontakt:     Name, E-Mail, Telefon, Datum
```

---

## 2. Positionspapier (LaTeX-PDF)

```python
pdf_path = compile_document(
    doc_type="positionspapier",
    title="Titel des Positionspapiers",
    body="""
\\section{Ausgangslage}
Beschreibung des Problems oder Themas...

\\section{Position}
\\begin{itemize}
  \\item Kernforderung 1
  \\item Kernforderung 2
  \\item Kernforderung 3
\\end{itemize}

\\section{Begruendung}
Ausfuehrliche Argumentation...

\\section{Empfehlungen}
Konkrete Handlungsempfehlungen...
""",
    output_path="press_output/position_thema.pdf"
)
```

---

## 3. Pitch Deck ☁️

### Gamma (gamma.app)

```
1. gamma.app -> "New AI Presentation"
2. Thema eingeben + Anzahl Folien waehlen (7-12 empfohlen)
3. Generiertes Deck anpassen:
   - Slide-Reihenfolge per Drag & Drop
   - Text direkt bearbeiten
   - Bilder durch eigene ersetzen
4. Export: PDF oder Public Link
```

**Pitch-Deck-Struktur (klassisch):**
```
1. Titel + Tagline
2. Problem
3. Loesung
4. Wie es funktioniert (Produkt/Demo)
5. Markt & Chance
6. Geschaeftsmodell
7. Traction (was erreicht wurde)
8. Team
9. Was wir suchen (Call to Action)
```

### Canva ☁️ (canva.com)

```
1. "Presentations" -> Template waehlen oder leer starten
2. Markenfarben und -schriften einstellen (Brand Kit)
3. Folien nach Pitch-Deck-Struktur aufbauen
4. Export: PDF, PPTX oder Magic Presentation (Web)
```

---

## 4. Social-Media-Kit ☁️

### Canva Social Kit

```
1. Vorlage "Social Media Kit" suchen
2. Inhalte: Logo, Farben, Schrift, Key Message
3. Formate in einem Set:
   - Instagram Post 1080x1080
   - Instagram Story 1080x1920
   - LinkedIn Banner 1584x396
   - Twitter/X Header 1500x500
4. Als ZIP exportieren (alle Formate gleichzeitig)
```

### Ideogram fuer Custom-Grafiken ☁️

```
ideogram.ai -> Prompt + gewuenschtes Text-Overlay
Staerke: Text korrekt im Bild -> Zitate, Hashtags, Claims als Bild
```

---

## PR-Prompts fuer Texterstellung

### Pressemitteilung schreiben lassen

```
"Schreibe eine Pressemitteilung.

 Anlass: [BESCHREIBUNG, z.B. Produktlaunch / Kooperation / Studie]
 Organisation: [NAME]
 Hauptbotschaft: [Was ist die Kernaussage?]
 Datum: [DATUM]
 Zitat: [Person Name, Rolle + Zitat-Kernelement]

 Format: Lead (5W), 3 Body-Absaetze, 1 Zitat, Boilerplate, Kontaktblock.
 Tonalitaet: professionell, sachlich, aktiv formuliert."
```

### Presseverteiler-E-Mail

```
"Schreibe eine kurze Begleit-E-Mail zur Pressemitteilung [THEMA].
 Empfaenger: Redakteure [FACHGEBIET]
 Kernbotschaft in 2 Saetzen
 Warum relevant fuer deren Leser?
 Hinweis auf Ansprechpartner fuer Rueckfragen."
```
