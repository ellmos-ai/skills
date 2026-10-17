---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "يخطط الملفات أو يعكسها أو يتحقق منها أو يستعيدها أو يؤرشفها صراحةً عبر نواة mac-backup الآمنة عند الفشل (fail-closed). استخدمه لمهام النسخ الاحتياطي عبر المضيفات الخاصة بالمستخدم؛ لا تستخدمه للمزامنة السحابية العامة أو لنسخ الملفات العرضي."
visibility: public
language: ar
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# Backup

استخدم واجهة سطر الأوامر `mac-backup` المثبتة بوصفها التنفيذ الوحيد للنقل. لا تُعِد بناء التدفق
باستخدام `scp` أو `rsync` أو SSHFS أو إجراءات Explorer أو الحذف المرتجل.

## توجيه الطلب

- يعني طلب "Backup" أو "نسخ احتياطي" العادي `mirror`؛ ويبقى المصدر دون مساس.
- يعني `archive` تنظيف المصدر، وهو نية مدمّرة مستقلة. لا تستنتجه أبدًا من "backup" أو "نسخ احتياطي" أو "copy" أو "نسخ" أو "free some space" أو "تحرير مساحة".
- يكتب `restore` إلى هدف جديد، ولا يستبدل أبدًا بصمت.
- إذا لم يكن هناك ملف JSON للمهمة مُدقَّق، فأعدّ اقتراحًا للمهمة وتوقف قبل `init-target` أو النقل.

## التنفيذ

1. اقرأ المهمة ونفّذ `mac-backup plan <job> --json`.
2. تحقّق من تطابق فئة المصدر المُعادة وعدد الملفات وعدد البايتات ومعرّف وحدة التخزين الهدف وحالة التشفير وبصمة المضيف مع الطلب ومع إثبات الجهاز الحالي.
3. بالنسبة إلى Mirror، نفّذ `mac-backup mirror <job> --json` ثم `mac-backup verify <job> --json`.
4. بالنسبة إلى Restore، استخدم هدفًا جديدًا ومطلقًا، وتحقّق من الملفات المستعادة عبر نتيجة الـ manifest الخاصة بالأمر.
5. بالنسبة إلى Archive، مرّر `--confirm-delete` فقط عندما يطلب المستخدم إزالة المصدر صراحةً وتسمّي الخطة المُدقَّقة هذا المصدر تحديدًا. يُعد الحظر الناتج عن السياسة النتيجة الصحيحة؛ ولا تتجاوز أبدًا `target_encryption_required`،
   أو `source_class_unknown_cleanup_blocked`، أو `onedrive_dehydrate_not_implemented`، أو قفلًا، أو عدم تطابق الهوية، أو مرساةً مفقودة.

يُعد `init-target` إعدادًا ذا امتيازات، وليس تنفيذًا روتينيًا. ويتطلب إثباتًا مستقلًا من نظام التشغيل لمعرّف وحدة التخزين وحالة التشفير؛ والقيمة المنسوخة من المهمة المقترحة ليست إثباتًا.

لا تدّعِ أبدًا أن الـ Mirror نسخة احتياطية كاملة قبل أن ينجح كل من التحقق من الهدف واختبار استعادة فعلي. أبقِ الأسرار وملفات المهام الحقيقية والمراسي المحلية وأسماء ملفات المستخدم خارج التذاكر وGit وOneDrive.

## سجل التغييرات

### 1.0.0 (2026-08-24)
- أُدرجت نسخة محايدة من نسخة `~/.claude/skills/backup/` الأصلية للنشر ضمن المكتبة المصنّفة. سبب فجوة المزامنة: كانت المهارة منشورة لكنها لم تكن تملك مدخل مصدر تحت `skills/<category>/`، لذلك أبلغ `skill_sync.py status` عنها بوصفها `NUR-ZIEL` (الهدف فقط)، ولم ترَها `catalog.py`/`build_public_registry.py` (اللتان تفحصان `skills/` فقط)، ولذلك لم تتمكن أبدًا من الوصول إلى السجل العام أو `SKILLS-MAP.md`، بغض النظر عن كيفية تعديل نسخة النشر.
