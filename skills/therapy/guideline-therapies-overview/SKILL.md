---
name: guideline-therapies-overview
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Vergleich der vier in Deutschland zugelassenen Richtlinienverfahren: Verhaltenstherapie, Tiefenpsychologisch fundierte Psychotherapie, Psychoanalyse, Systemische Therapie — Orientierungshilfe.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [richtlinienverfahren, verhaltenstherapie, tiefenpsychologie, psychoanalyse, systemische-therapie, orientierung]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/richtlinienverfahren_ueberblick.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Richtlinienverfahren Ueberblick

> Vergleich der vier in Deutschland zugelassenen Richtlinienverfahren: Verhaltenstherapie, Tiefenpsychologisch fundierte Psychotherapie, Psychoanalyse, Systemische Therapie — Orientierungshilfe

Siehe: [ETHICS.md](../ETHICS.md)

---

## Kontext

In Deutschland gibt es vier anerkannte Richtlinienverfahren, deren Kosten von
gesetzlichen Krankenkassen uebernommen werden. Viele Menschen wissen nicht,
welches Verfahren fuer sie geeignet sein koennte. Dieser Skill bietet einen
psychoedukativen Ueberblick zur Orientierung.

Rechtsgrundlage: Die Richtlinienverfahren werden vom Gemeinsamen Bundesausschuss
(G-BA) auf Basis wissenschaftlicher Evidenz zugelassen.
- Verhaltenstherapie (VT): Richtlinienverfahren seit 1987
- Tiefenpsychologisch fundierte Psychotherapie (TP): seit 1967
- Analytische Psychotherapie (AP): seit 1967
- Systemische Therapie (ST): seit 2019 (Erwachsene) / 2024 (Kinder & Jugendliche)

**Hinweis:** Dies ist eine Orientierungshilfe, keine Therapieempfehlung.
**Niemals implementieren:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Die vier Richtlinienverfahren im Ueberblick

| Merkmal | VT | TP | AP | ST |
|---------|----|----|----|----|
| **Grundidee** | Verhalten und Denkmuster aendern | Unbewusste Konflikte verstehen | Tiefe Persoenlichkeitsveraenderung | Beziehungen und Systeme veraendern |
| **Zeitfokus** | Gegenwart und Zukunft | Vergangenheit und Gegenwart | Vergangenheit (Kindheit) | Gegenwart und Beziehungen |
| **Sitzungen** | 12-80 Std. | 12-100 Std. | 80-300 Std. | 12-48 Std. |
| **Frequenz** | 1x/Woche | 1x/Woche | 2-3x/Woche | 1x/Woche oder seltener |
| **Setting** | Meist Einzeln | Meist Einzeln | Einzeln (Couch) | Einzeln, Paar, Familie |

---

## 2. Verhaltenstherapie (VT)

### Grundannahmen
- Verhalten wird gelernt und kann umgelernt werden
- Denkmuster beeinflussen Gefuehle und Verhalten (kognitive Wende, Beck)
- Veraenderung geschieht durch aktives Ueben und neue Erfahrungen

### Wann besonders geeignet?
- Angststoerungen, Phobien, Panikattacken
- Depressionen
- Zwangsstoerungen, PTBS, Essstoerungen

---

## 3. Tiefenpsychologisch fundierte Psychotherapie (TP)

### Grundannahmen
- Unbewusste Konflikte beeinflussen unser Erleben und Verhalten
- Fruehere Beziehungserfahrungen praegen aktuelle Muster
- Einsicht in unbewusste Zusammenhaenge foerdert Veraenderung

### Wann besonders geeignet?
- Depressionen (besonders chronische)
- Beziehungsprobleme mit wiederkehrenden Mustern
- Persoenlichkeitsstoerungen, psychosomatische Beschwerden

---

## 4. Analytische Psychotherapie (Psychoanalyse, AP)

### Grundannahmen
- Tief verwurzelte unbewusste Konflikte aus der fruehen Kindheit beeinflussen das gesamte Erleben
- Umfassende Persoenlichkeitsveraenderung ist moeglich durch tiefes Verstehen

### Wann besonders geeignet?
- Tiefgreifende Persoenlichkeitsprobleme
- Chronische, wiederkehrende Probleme
- Wenn kuerzere Verfahren nicht ausreichend geholfen haben

---

## 5. Systemische Therapie (ST)

### Grundannahmen
- Probleme entstehen und bestehen in Beziehungssystemen
- Veraenderung bei einem Mitglied veraendert das ganze System
- Jeder Mensch hat Ressourcen und Loesungskompetenzen

### Wann besonders geeignet?
- Familien- und Paarkonflikte
- Kinder- und Jugendprobleme (im Familiensystem)
- Bei Wunsch nach kuerzerer Therapie

---

## 6. Praktische Orientierung

### Entscheidungshilfe (KEINE Empfehlung, nur Orientierung)

| Ich moechte... | Eher passendes Verfahren |
|----------------|-------------------------|
| Konkrete Werkzeuge gegen Aengste | VT |
| Verstehen, warum ich immer wieder in gleiche Muster falle | TP |
| Mich grundlegend besser kennenlernen | AP |
| Beziehungsprobleme im System verstehen | ST |
| Schnell praktische Hilfe | VT oder ST |

### Therapeutische Beziehung

Forschung zeigt konsistent: Der wichtigste Wirkfaktor ist die therapeutische
Beziehung (Wampold 2015). Das "richtige" Verfahren ist weniger wichtig als
der "richtige" Therapeut.

---

## 7. Praktische Informationen (Deutschland)

### Therapeutensuche
- Terminservicestelle: 116 117
- Therapeutensuche der Kassenaerztlichen Vereinigung
- Psychotherapeutenkammer des Bundeslandes

---

## Ethik und Grenzen

**Ein KI-Assistent darf:**
- Die vier Richtlinienverfahren sachlich vorstellen und vergleichen
- Orientierungshilfe geben (keine Empfehlung)
- Praktische Informationen zur Therapeutensuche geben
- Reflexionsfragen stellen zur Selbstklaerung

**Ein KI-Assistent darf NICHT:**
- Ein bestimmtes Verfahren empfehlen
- Von einem Verfahren abraten
- Diagnosen stellen oder Indikationen ableiten
- Therapeuten bewerten oder empfehlen
- Laufende Therapien kommentieren oder infrage stellen

**Bei Anzeichen akuter Krise IMMER verweisen auf:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Psychiatrischer Notdienst: 112
- Krisenchat: krisenchat.de

---

## Quellenangaben

- Wampold, B. E. (2015). *The Great Psychotherapy Debate.* Routledge.
- Leichsenring, F. & Rabung, S. (2011). Long-term psychodynamic psychotherapy in complex mental disorders. *British Journal of Psychiatry*, 199(1), 15-22.
- von Sydow, K. et al. (2010). *Die Wirksamkeit der Systemischen Therapie/Familientherapie.* Hogrefe.
- G-BA Psychotherapie-Richtlinie

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
*Quellen: G-BA Richtlinien, Wampold (2015), Leichsenring & Rabung (2011), von Sydow et al. (2010) — Keine professionelle Therapie*
