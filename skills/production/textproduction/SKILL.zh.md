---
language: zh
---

> **中文** — 针对该技能的官方完整中文文档: `textproduction`.



> **English** — Offizielle English-Version / Documento Oficial en English.


> **English Translation** — Official English version of `textproduction`.


# Textproduction — Router (English)

Dieser Skill deckt alle textlichen Produktionsformen ab. Er leitet an den
passenden Teilskill weiter — lies die Detail-Anleitung im Unterordner.

## Routing-Tabelle

| Teilskill | Trigger-Beispiele | Detail-Anleitung |
|---|---|---|
| **text** | „Schreib einen Blogpost", „5 LinkedIn-Posts", „Newsletter", „Produktbeschreibung", „Formelle E-Mail", „Fasse X zusammen" | `text/WORKFLOW.md` |
| **storys** | „Schreib ein Drehbuch", „Kurzgeschichte", „RPG-Abenteuer erstellen", „Character Sheet", „Weltenbau" | `storys/WORKFLOW.md` |
| **pr** | „Pressemitteilung verfassen", „Positionspapier", „PR-Paket", „PDF generieren" | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## 工作流程与执行步骤 & Execution Steps

```
1. Nutzerwunsch → Routing-Tabelle oben → passenden Teilskill bestimmen.
2. Detail-Anleitung im Unterordner lesen (WORKFLOW.md).
3. Prompt-Muster auswaehlen, Platzhalter fuellen, Text generieren.
4. Qualitaetspruefung (je Teilskill angegeben).
```

## Hinweise

- **Userneutral:** Keine persoenlichen Daten, API-Keys oder Kontodaten im Skill.
  Konfiguration (Tonalitaet, Zeichenlimits, Kontaktdaten fuer PR) obliegt dem Nutzer.
- **PR-Tool:** `pr/press_compiler.py` kompiliert Pressemitteilungen und Positionspapiere
  zu PDF via LaTeX (pdflatex/xelatex). Setup einmalig: `pr/config.example.json`
  nach `pr/config.json` kopieren und Kontaktdaten eintragen.
- Optionale Stiloptimierung: DeepL Write (kostenlos bis 500.000 Zeichen/Monat).

## 变更日志与历史

### 2.0.0 (2026-06-22)
- Umstrukturierung auf Router-Muster: SKILL.md = Einstieg + Routing-Tabelle.
- Drei Teilskills: text/ (6 Texttypen), storys/ (4 narrative Formate),
  pr/ (Pressemitteilung + Positionspapier + LaTeX-PDF-Compiler).
- press_compiler.py + LaTeX-Templates + config.example.json aus
  ai-media-editor/production/pr/ hierher verschoben (SSOT).
- Verwandte-Skills-Verweise auf interne Teilskill-Pfade aktualisiert.

### 1.0.0 (2026-06-22)
- Initiale Version. Herausgeloest aus ai-media-editor/production/text/WORKFLOW.md.
- Provenance: BACH agents/_experts/textproduction/ (MIT).