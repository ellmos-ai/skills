---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "إعادة هيكلة تسلسلات المجلدات المتداخلة إلى بنى مسطحة قابلة للقراءة الآلية. قائمة على Bash مع منطق دمج ذكي."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [ordner, flattening, filesystem, bash, reorganisation, cleanup]
language: ar
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/ordner-flattening.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ecd288c18790f209ab63e3b72bc81cf748f957b27068f37a9a4999740f4392b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.612725+00:00"
---
<img src="banner.png" width="100%" alt="folder-flattening banner">

# سير العمل: تسطيح المجلدات

الهدف: نقل بنى المجلدات المتداخلة إلى بنية مسطحة قابلة للقراءة الآلية.
الميزة: لا حاجة إلى التنقل بالنقر، بل البحث عبر قاعدة البيانات (Verzeichnis.db).
الازدواجية مسموحة إذا كانت منطقية من حيث الموضوع.

---

## نظرة عامة على المراحل

| المرحلة | ما الذي يحدث | قسم السكربت |
|---------|-------------|-----------------|
| 1 | التسطيح: نقل جميع المجلدات الفرعية إلى مستوى واحد | `phase_flatten` |
| 2 | الاختصار: اختصار أسماء المسارات الطويلة إلى الجزء الأخير، والدمج عند التعارض | `phase_shorten` |
| 3 | التنظيف: حل الشرطات السفلية المتعددة (`___`) وإزالة `_` اللاحقة | `phase_cleanup_underscores` |
| 4 | التجميع: مجلدات الأرقام ومجلدات CD والأسماء القصيرة في مجلدات تجميعية | `phase_group_problematic` |
| 5 | تحليل الثلاثيات: مجموعات ثلاثية متحركة، وأقصر اسم كهدف للدمج | `phase_tripel_merge` |
| 6 | دمج تنسيقات الوسائط: تجميع المجلدات حسب نوع الملف (قالب) | `phase_media_merge` |
| 7 | التنظيف النهائي: حذف المجلدات الفارغة | `phase_cleanup_empty` |

---

## القواعد المهمة

### مطابقة تحليل الثلاثيات
- **سلسلة جزئية**: `Aufklaerung` في `Aufklaerungsbroschueren` -> يُدمج في `Aufklaerung`
- **الجمع/تحويل الحروف المتحركة**: `Raum` = `Raeume`، `Teil` = `Teile`، `Buch` = `Buecher`
- **الكلمة الأولى**: `Autismus ADHS` تطابق `Autismus Beruf` (البداية نفسها)

### الحد الأدنى للطول
- اسم من كلمة واحدة بدون مسافات: **8 أحرف على الأقل** (يمنع `Hand` و`Haus` و`Form`)
- مع مسافات (مثل `ICF Katalog`): **من 3 أحرف مقبول**
- وبذلك تبقى `ICF` و`ASS Frauen` وغيرها مسموحة

### إعادة التشغيل بعد الدمج
بعد كل عملية دمج تُعاد تحميل قائمة المجلدات ويُعاد التشغيل من هدف الدمج.
فمثلاً يجمع `Autismus` كل الإضافات قبل المتابعة.

---

## دمج تنسيقات الوسائط (نظام القوالب)

تستخدم المرحلة 6 مصفوفة قوالب `MEDIA_TYPES`. يحدد كل إدخال:
- المجلد الهدف (ببادئة `_`)
- امتدادات الملفات التي تنتمي إلى هذا النوع

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Bilder|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Erweiterbar:
    # "_Tabellen|xlsx|xls|csv|ods"
    # "_Prasentationen|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

تُنقل فقط المجلدات التي تحتوي **حصرياً** على ملفات من نوع واحد.
تُتخطى المجلدات التي تحتوي على مجلدات فرعية.

### إضافة نوع وسائط جديد

أضف ببساطة سطراً جديداً إلى مصفوفة `MEDIA_TYPES`:
```bash
"_Zielordner|ext1|ext2|ext3"
```

---

## التنفيذ

```bash
# Kompletter Durchlauf:
cd /pfad/zum/zielverzeichnis
bash ordner_flattening_komplett.sh

# Oder einzelne Phasen:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## القيم التجريبية لجلسة 26.01.2026

- البداية: 206 مجلدات + 252 ملفاً منفرداً، نحو 5600 مجلد فرعي متداخل
- بعد التسطيح: نحو 2200 مجلد على مستوى واحد
- بعد الاختصار والتنظيف: نحو 2005 مجلدات
- بعد التجميع (الأرقام، الأقراص المدمجة): نحو 2005 -> أُنشئت مجلدات تجميعية
- بعد الثلاثيات v1: نحو 1561 مجلداً
- بعد الثلاثيات v2 (قاعدة 8 أحرف): تخفيض إضافي
- مرحلة تنسيقات الوسائط: دُمجت مجلدات الصوت والفيديو والصور
