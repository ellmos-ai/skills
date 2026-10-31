---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "إطار عمل لاتخاذ القرارات المنظم: مصفوفة المزايا والعيوب، والتقييم الموزون، وشجرة القرار، وتحليل السيناريوهات، ومصفوفة أيزنهاور."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 1627b5e5d34c9cc5009de91ad5ce32eb203984c0416d715513c7f2489e5ca4f6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.257940+00:00"
---
<img src="banner.png" width="100%" alt="decide banner">

# Decide — اتخاذ القرار المنظم

> قرارات عقلانية من خلال أطر عمل منظمة وأساليب تقييم

---

## متى يُستخدم؟

- الاختيار بين خيارات متعددة
- الحاجة إلى قائمة مزايا وعيوب
- قرار متعدد المعايير
- الشعور بعدم اليقين في قرارات مهمة

**كلمات التشغيل:** يقرر، يختار، يقارن، يقيّم، يزن الأمور

---

## أطر العمل

### 1. مصفوفة المزايا والعيوب (بسيطة)

قرارات سريعة بين خيارين.

```
PRO A:                    CON A:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

PRO B:                    CON B:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

Empfehlung: [A/B] weil [Begruendung]
```

---

### 2. التقييم الموزون (معقد)

قرارات متعددة المعايير مع ترجيح.

| المعيار | الوزن | الخيار أ | تقييم أ | الخيار ب | تقييم ب |
|-----------|---------|----------|---------|----------|---------|
| المعيار 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| المعيار 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| المجموع | 100% | - | X.XX | - | X.XX |

**العملية:**
1. جمع المعايير
2. تحديد الأوزان (المجموع = 100%)
3. تقييم الخيارات (مقياس من 1 إلى 10)
4. حساب النتائج (التقييم × الوزن)
5. المقارنة والتوصية

---

### 3. شجرة القرار (متسلسلة)

قرارات ذات مسارات واضحة من نوع «إذا... فإن...»:
1. تحديد السؤال الابتدائي
2. التفرع الأول (المعيار الأهم)
3. المستوى التالي (المعيار الثاني في الأهمية)
4. وصولاً إلى الخيار النهائي

---

### 4. تحليل السيناريوهات (عدم اليقين)

```
Best Case (X% Wahrscheinlichkeit):
  Ergebnis: +Y Punkte -> Erwartungswert: +Z

Realistic Case (X%):
  Ergebnis: +Y -> Erwartungswert: +Z

Worst Case (X%):
  Ergebnis: -Y -> Erwartungswert: -Z

Gesamt-Erwartungswert: [Summe]
```

---

### 5. مصفوفة أيزنهاور (تحديد الأولويات)

```
              DRINGEND        NICHT DRINGEND
WICHTIG       1. TUN          2. PLANEN
NICHT WICHTIG 3. DELEGIEREN   4. ELIMINIEREN
```

---

## قائمة التحقق من الجودة

قبل التوصية النهائية، تحقّق مما يلي:
- [ ] هل حُددت جميع المعايير ذات الصلة؟
- [ ] هل رُوعيت قيم المستخدم؟
- [ ] هل فُكّر في الآثار طويلة المدى؟
- [ ] هل حُددت المخاطر وقُيّمت؟
- [ ] هل أُجري فحص للتحيزات؟
- [ ] هل جرى التحقق من إمكانية الرجوع عن القرار؟

---

## أفضل الممارسات

### تحديد المعايير
- أن تكون محددة وقابلة للقياس
- ألا تكون كثيرة (من 3 إلى 7 مثالياً)
- أن تكون مستقلة بعضها عن بعض

### الترجيح
- المجموع = 100%
- يكون المعيار الأهم 25% على الأقل
- لا تقل أي أوزان عن 5%

### التوصية
- أن تكون واضحة ومعللة
- ذكر البدائل
- تسمية المخاطر
- مراعاة إمكانية الرجوع

---

## سير العمل

```
1. User Request
2. Entscheidung verstehen
3. Optionen identifizieren (2-5)
4. Framework waehlen
5. Kriterien sammeln
6. Framework anwenden
7. Bias-Check (optional)
8. Empfehlung aussprechen
9. Reasoning dokumentieren
```

---

## سجل التغييرات

### 1.0.0 (2026-03-15)
- نُقل من BACH v3.8.0

---

*نُقل من BACH v3.8.0 | النسخة المستقلة*

**انظر أيضاً:** [think](../think/SKILL.md) (التحليل، والسبب الجذري، وتحليل SWOT) | [brainstorm](../brainstorm/SKILL.md) (أساليب الإبداع، وتوليد الأفكار) | [decision-shot](../decision-shot/SKILL.md) (تكثيف مخرجات هذا التحليل في صيغة تنفيذية موجزة تتضمن التوصية ورابطاً إلى النسخة الكاملة)
