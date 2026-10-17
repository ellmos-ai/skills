---
name: think
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "समस्या समाधान और विश्लेषण: जटिल समस्याओं के लिए संरचित विचार प्रक्रियाएँ। Divide & Conquer, Root Cause Analysis, SWOT, Pareto और निर्णय-ह्यूरिस्टिक्स।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: eb79ba4bdf7216c7845cd999ef2c905d4611f252d2c4b8f42404058645b37fc7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.512215+00:00"
---
<img src="banner.png" width="100%" alt="think banner">

# Think — समस्या समाधान और विश्लेषण

> जटिल समस्याओं के लिए संरचित विचार प्रक्रियाएँ

---

## समस्या समाधान के दृष्टिकोण

### 1. Divide & Conquer

```
Problem -> Teilprobleme -> Loese einzeln -> Kombiniere
```

### 2. Root Cause Analysis

```
Symptom -> Warum? -> Warum? -> Warum? -> Ursache -> Loesung
```

### 3. Constraint Relaxation

```
Unloesbares Problem -> Constraints lockern -> Loesen -> Constraints wieder anziehen
```

### 4. एनालॉजी-खोज

```
Neues Problem -> Aehnliches bekanntes Problem -> Loesung adaptieren
```

---

## विश्लेषण पद्धतियाँ

| पद्धति | उपयोग |
|---------|-----------|
| **SWOT** | शक्तियाँ/कमजोरियाँ/अवसर/जोखिम |
| **Pro/Contra** | निर्णय लेना |
| **Pareto** | 80/20 प्राथमिकीकरण |
| **Fishbone** | कारण विश्लेषण |

---

## निर्णय-ह्यूरिस्टिक्स

### अनिश्चितता में

```
1. Was ist das Worst-Case-Szenario?
2. Ist es reversibel?
3. Was kostet Nicht-Handeln?
```

### जटिलता में

```
1. Was ist der einfachste erste Schritt?
2. Was wuerde ein Experte tun?
3. Was waere die 80%-Loesung?
```

---

## Changelog

### 1.0.0 (2026-03-15)
- BACH v3.8.0 से पोर्ट किया गया

---

*BACH v3.8.0 से पोर्ट किया गया | Standalone-संस्करण*

**इसे भी देखें:** [brainstorm](../brainstorm/SKILL.md) (रचनात्मक पद्धतियाँ, विचार-संग्रह) | [decide](../decide/SKILL.md) (निर्णय फ्रेमवर्क)
