---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "طرق إبداعية منظمة لتوليد الأفكار: SCAMPER، وقبعات التفكير الست، ورسم الخرائط الذهنية، والعصف الذهني العكسي، وTRIZ، والتوليد السريع للأفكار."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [brainstorm, creativity, ideation, scamper, six-hats, innovation]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/brainstorm.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 3974ca6cf14e2ee379fed97740da2cd90f141ba00af3f22de1ca0cec31ac342e
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="brainstorm banner">

# Brainstorm

> إبداع منظم من أجل الابتكار — SCAMPER، وSix Hats، وMind Mapping، وReverse Brainstorming، وTRIZ، وRapid Ideation

---

## متى تُستخدم؟

- الحاجة إلى أفكار جديدة
- الوقوع في طريق مسدود / تعطّل الإبداع
- البحث عن الابتكار
- حل مشكلة بطريقة إبداعية

**كلمات التشغيل:** brainstorm، ideen، kreativ، innovativ، ideenfindung، عصف ذهني، أفكار، إبداعي، ابتكاري، توليد الأفكار

---

## الطرق

### 1. SCAMPER

**Substitute، Combine، Adapt، Modify، Put to other use، Eliminate، Reverse**

تحسين الحلول القائمة بشكل منهجي:
- **S**ubstitute: ما الذي يمكن استبداله؟
- **C**ombine: ما الذي يمكن دمجه؟
- **A**dapt: ما الذي يمكن تكييفه؟
- **M**odify: ما الذي يمكن تعديله؟
- **P**ut to other use: ما استخدامات أخرى ممكنة له؟
- **E**liminate: ما الذي يمكن حذفه؟
- **R**everse: ما الذي يمكن عكسه؟

---

### 2. Six Thinking Hats (Edward de Bono)

التفكير في 6 وجهات نظر بشكل منهجي:

- **القبعة البيضاء — الحقائق:** ما المعلومات التي لدينا؟ وما الذي ينقصنا؟
- **القبعة الحمراء — العاطفة:** كيف تشعر حيال هذا؟ الحدس والإحساس الداخلي
- **القبعة السوداء — النقد:** ما الذي قد يسير بشكل خاطئ؟ المخاطر ونقاط الضعف
- **القبعة الصفراء — التفاؤل:** ما الفرص المتاحة؟ أفضل سيناريو
- **القبعة الخضراء — الإبداع:** أفكار جديدة؟ خارج الصندوق؟
- **القبعة الزرقاء — ميتا / مستوى أعلى:** التحكم في العملية، والتلخيص، والخطوات التالية

**العملية:** تعريف المشكلة (الأزرق) ← الحقائق (الأبيض) ← المشاعر (الأحمر) ← النقد (الأسود) ← الإيجابيات (الأصفر) ← أفكار جديدة (الأخضر) ← التلخيص (الأزرق)

---

### 3. Mind Mapping

تصوير الأفكار بشكل هرمي:
1. الموضوع المركزي
2. الفروع الرئيسية (3-7)
3. الفروع الفرعية لكل فئة
4. إضافة التفاصيل والأفكار
5. تحديد الروابط

---

### 4. Reverse Brainstorming

عكس المشكلة: "كيف نجعلها أسوأ؟"

1. عكس المشكلة
2. جمع الأفكار السيئة
3. عكسها = أفكار جيدة

مفيد بشكل خاص عندما يتعطل توليد الأفكار المباشر.

---

### 5. TRIZ (Theory of Inventive Problem Solving)

أهم 10 مبادئ للبرمجيات:
1. **Segmentation:** تقسيم النظام الأحادي إلى وحدات
2. **Extraction:** عزل الخاصية المزعجة
3. **Local Quality:** مكونات مختلفة وخصائص مختلفة
4. **Merging:** دمج الوظائف المتشابهة
5. **Universality:** عنصر واحد ووظائف متعددة
6. **Nesting:** تداخل المكونات
7. **Preliminary Action:** التحضير المسبق
8. **Feedback:** المراقبة والتكييف
9. **Self-Service:** النظام يخدم نفسه
10. **Asymmetry:** تصاميم غير متماثلة

---

### 6. Rapid Ideation

الكمية قبل الجودة — أكثر من 50 فكرة في 20 دقيقة.

**القواعد:**
- لا نقد أثناء توليد الأفكار
- الأفكار الجامحة مرحب بها
- البناء على أفكار الآخرين
- الكمية أولاً

**قائم على المؤقت:**
- الجولة 1 (5 دقائق): توليد حر للأفكار
- الجولة 2 (5 دقائق): التنويعات
- الجولة 3 (5 دقائق): التركيبات
- الجولة 4 (5 دقائق): أفكار متطرفة

---

## سير العمل

```
1. User Request
2. Ziel verstehen
3. Methode(n) waehlen
4. Ideen generieren (keine Kritik!)
5. Clustering
6. Feasibility/Impact Matrix
7. Top 5-10 Auswahl
8. Output + Empfehlung
```

---

## سجل التغييرات

### 1.0.0 (2026-03-15)
- نُقل من BACH v3.8.0

---

*نُقل من BACH v3.8.0 | نسخة مستقلة*

**انظر أيضاً:** [think](../think/SKILL.md) (التحليل، والسبب الجذري، وSWOT) | [decide](../decide/SKILL.md) (أطر اتخاذ القرار)
