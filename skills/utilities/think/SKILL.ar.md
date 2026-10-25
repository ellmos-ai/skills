---
name: think
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "حل المشكلات والتحليل: عمليات تفكير منظّمة للمشكلات المعقّدة. التقسيم والغلبة، وتحليل السبب الجذري، وSWOT، وباريتو، والاستدلالات الإرشادية لاتخاذ القرار."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: eb79ba4bdf7216c7845cd999ef2c905d4611f252d2c4b8f42404058645b37fc7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.645381+00:00"
---
<img src="banner.png" width="100%" alt="think banner">

# Think — حل المشكلات والتحليل

> عمليات تفكير منظّمة للمشكلات المعقّدة

---

## نُهج حل المشكلات

### 1. التقسيم والغلبة

```
Problem -> Teilprobleme -> Loese einzeln -> Kombiniere
```

### 2. تحليل السبب الجذري

```
Symptom -> Warum? -> Warum? -> Warum? -> Ursache -> Loesung
```

### 3. تخفيف القيود

```
Unloesbares Problem -> Constraints lockern -> Loesen -> Constraints wieder anziehen
```

### 4. البحث بالتشابه

```
Neues Problem -> Aehnliches bekanntes Problem -> Loesung adaptieren
```

---

## طرق التحليل

| الطريقة | التطبيق |
|---------|-----------|
| **SWOT** | نقاط القوة/نقاط الضعف/الفرص/المخاطر |
| **المؤيِّد/المعارِض** | اتخاذ القرار |
| **باريتو** | ترتيب الأولويات 80/20 |
| **مخطط عظم السمكة** | تحليل الأسباب |

---

## الاستدلالات الإرشادية لاتخاذ القرار

### عند عدم اليقين

```
1. Was ist das Worst-Case-Szenario?
2. Ist es reversibel?
3. Was kostet Nicht-Handeln?
```

### عند التعقيد

```
1. Was ist der einfachste erste Schritt?
2. Was wuerde ein Experte tun?
3. Was waere die 80%-Loesung?
```

---

## سجل التغييرات

### 1.0.0 (2026-03-15)
- نُقل من BACH v3.8.0

---

*نُقل من BACH v3.8.0 | النسخة المستقلة*

**انظر أيضًا:** [brainstorm](../brainstorm/SKILL.md) (طرق الإبداع، توليد الأفكار) | [decide](../decide/SKILL.md) (أطر اتخاذ القرار)
