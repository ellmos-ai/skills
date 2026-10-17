---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "নতুন সফটওয়্যার প্রকল্প অনবোর্ডিংয়ের আদর্শ পদ্ধতি: বৈশিষ্ট্য বিশ্লেষণ, কোড গুণমান পর্যালোচনা, অনবোর্ডিং চেকলিস্ট এবং টাস্ক তৈরি।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 8e49954ab15704af930d6a8e717a5fd9c0109ed1378a2421998d889d8e90d359
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:50.098377+00:00"
---
<img src="banner.png" width="100%" alt="project-onboarding banner">

# নতুন সফটওয়্যার প্রকল্পের জন্য স্ট্যান্ডার্ড অনবোর্ডিং পদ্ধতি

**সংস্করণ:** 1.0
**হালনাগাদ:** 2026-03-12

---

## সারসংক্ষেপ

এই পদ্ধতি নির্ধারণ করে যে নতুন আবিষ্কৃত সফটওয়্যার ফোল্ডারগুলিকে একটি টাস্ক-ম্যানেজমেন্ট সিস্টেমে যুক্ত করার আগে কোন ধাপগুলি সম্পন্ন করতে হবে।

```
┌─────────────────────────────────────────────────────────┐
│           STANDARDAUFNAHMEVERFAHREN                     │
├─────────────────────────────────────────────────────────┤
│  1. Feature-Analyse erstellen                           │
│  2. Code-Qualitaetspruefung (Standard-Tests)            │
│  3. AUFGABEN.txt erstellen                              │
│  4. In Task-Management uebernehmen                      │
└─────────────────────────────────────────────────────────┘
```

---

## ধাপ 1: বৈশিষ্ট্য বিশ্লেষণ

**উদ্দেশ্য:** টুলটি, তার কার্যাবলি এবং উন্নয়নের অবস্থা বোঝা।

**ফাইল তৈরি করুন:** `Feature_Analyse_<ToolName>.md`

### টেমপ্লেট

```markdown
# Feature-Analyse: <ToolName>

## Kurzbeschreibung
Ein kurzer Satz der beschreibt was das Tool macht.

---

## Highlights

| Feature | Beschreibung |
|---------|-------------|
| **Feature 1** | Beschreibung |
| **Feature 2** | Beschreibung |

---

## Bewertung der Ausbaustufe

### Aktueller Stand: **<Status> (<X>%)**

Moegliche Status:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Kategorie | Bewertung (1-5) | Details |
|-----------|:---------------:|---------|
| **Funktionsumfang** | 3 | |
| **UI/UX** | 3 | |
| **Stabilitaet** | 3 | |
| **Dokumentation** | 3 | |

---

## Empfohlene Erweiterungen

### Prioritaet: Hoch
1. ...

### Prioritaet: Mittel
2. ...

### Prioritaet: Niedrig
3. ...

---

## Technische Details

Framework:      <Framework>
Dateigroesse:   <X> Zeilen Python
Hauptdatei:     <main.py>

---
*Analyse erstellt: <Datum>*
```

---

## ধাপ 2: কোড গুণমান পরীক্ষা

**উদ্দেশ্য:** প্রযুক্তিগত গুণমান নিশ্চিত করা এবং পরিচিত সমস্যাগুলি চিহ্নিত করা।

### সুপারিশকৃত পরীক্ষা

| পরীক্ষা | টুল | বিবরণ |
|---------|-----|-------|
| **এনকোডিং** | এনকোডিং-চেকার (যেমন `chardet`, `file`) | UTF-8 নিশ্চিত করুন |
| **পদ্ধতি বিশ্লেষণ** | লিন্টার (যেমন `pylint`, `flake8`) | বড় পদ্ধতি খুঁজুন |
| **ইনডেন্টেশন** | ফরম্যাটার (যেমন `black`, `autopep8`) | সামঞ্জস্য পরীক্ষা করুন |
| **ইম্পোর্ট** | ইম্পোর্ট-চেকার (যেমন `isort`, `pylint`) | অব্যবহৃত ইম্পোর্ট খুঁজুন |

### পরীক্ষার বিষয়সমূহ

- [ ] সব .py ফাইল UTF-8 এনকোড করা?
- [ ] কোনো অস্বাভাবিক বড় পদ্ধতি নেই (>100 লাইন)?
- [ ] সামঞ্জস্যপূর্ণ ইনডেন্টেশন (স্পেস বনাম ট্যাব)?
- [ ] অব্যবহৃত ইম্পোর্ট সরানো হয়েছে?
- [ ] ডকস্ট্রিং আছে?

### ফলাফল নথিভুক্ত করুন

"QUALITAETSPRUEFUNG" (গুণমান পরীক্ষা) অধীনে AUFGABEN.txt-এ সমস্যাগুলি লিখুন।

---

## ধাপ 3: AUFGABEN.txt তৈরি

**উদ্দেশ্য:** খোলা কাজগুলি কাঠামোবদ্ধভাবে লিপিবদ্ধ করা।

**ফাইল তৈরি করুন:** প্রকল্প ফোল্ডারে `AUFGABEN.txt`

### টেমপ্লেট

```
AUFGABEN - <ToolName> V<Version>
==============================
Status: <Status>
Stand: <Datum>

OFFENE AUFGABEN:
[ ] <Aufgabe 1> - Aufwand: <NIEDRIG|MITTEL|HOCH>
[ ] <Aufgabe 2> - Aufwand: <NIEDRIG|MITTEL|HOCH>

---
ERLEDIGT (Archiv):
- <Erledigte Aufgabe> (<Version>, <Datum>)
```

### স্ট্যাটাস মান

| স্ট্যাটাস | অর্থ |
|----------|------|
| NEU ENTDECKT (নতুন আবিষ্কৃত) | এখনো বিশ্লেষণ করা হয়নি |
| ANALYSE NOETIG (বিশ্লেষণ প্রয়োজন) | বৈশিষ্ট্য বিশ্লেষণ চলছে |
| QUALITAETSPRUEFUNG (গুণমান পরীক্ষা) | কোড পরীক্ষা চলছে |
| VALIDIERT & BEREIT (যাচাইকৃত ও প্রস্তুত) | বৈশিষ্ট্যের জন্য প্রস্তুত |
| MVP | ন্যূনতম কার্যকর পণ্য |
| NUR KOMPILIEREN (শুধু কম্পাইল) | শুধু কম্পাইল প্রয়োজন |
| GESPERRT (লক করা) | ব্যবহারকারীর পরীক্ষা/সিদ্ধান্তের অপেক্ষায় |

---

## ধাপ 4: টাস্ক-ম্যানেজমেন্ট ইন্টিগ্রেশন

ধাপ 1-3 সম্পন্ন হওয়ার পর:

1. **কাজ স্থানান্তর:** AUFGABEN.txt-এর এন্ট্রিগুলি টাস্ক/ইস্যু হিসেবে তৈরি করুন
2. **পরীক্ষা:** সব কাজ কি সঠিকভাবে শ্রেণিবদ্ধ হয়েছে?
3. **শ্রেণিবিন্যাস:** প্রকল্পটিকে উপযুক্ত বিভাগে রাখুন (Single-Tool, Suite, Library ইত্যাদি)

### স্বয়ংক্রিয় অনবোর্ডিং টাস্ক

নতুন প্রকল্পের জন্য নিম্নলিখিত আদর্শ টাস্কগুলি তৈরি করুন:

| টাস্ক | কাজ | প্রচেষ্টা |
|-------|-----|----------|
| onb_1 | বৈশিষ্ট্য বিশ্লেষণ তৈরি | মাঝারি |
| onb_2 | কোড গুণমান পরীক্ষা | কম |
| onb_3 | AUFGABEN.txt তৈরি | কম |

টাস্কগুলির নির্ভরতা রয়েছে: onb_2 নির্ভর করে onb_1-এর উপর, onb_3 নির্ভর করে onb_2-এর উপর।

---

## দ্রুত চেকলিস্ট

```
[ ] 1. Feature_Analyse_<Name>.md erstellt
[ ] 2. Code-Qualitaetspruefung durchgefuehrt (Linter, Encoding, Imports)
[ ] 3. AUFGABEN.txt erstellt mit Status
[ ] 4. Tasks in Task-Management uebernommen
```

---

## উদাহরণ: নতুন টুল "MyTool"

```bash
# 1. Feature-Analyse
# -> Feature_Analyse_MyTool.md erstellen (siehe Template)

# 2. Code-Qualitaet
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Encoding pruefen

# 3. AUFGABEN.txt
# -> Im Tool-Ordner erstellen mit Status "QUALITAETSPRUEFUNG"

# 4. Tasks anlegen
# -> Eintraege aus AUFGABEN.txt als Issues/Tickets erfassen
```

---

*তৈরি: 2026-01-10 | পোর্ট করা: 2026-03-12*
