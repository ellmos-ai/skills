---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "يوسّع automation-self-care بوظائف Letter Hooks وبوتلودر التحقق المسبق (Preflight) وقواعد اجتياز المستندات وإثراء سياق المطالبات ذاتي الإصلاح لوكلاء الذكاء الاصطناعي وواجهات سطر الأوامر التي لا تملك خطافات دورة حياة JSON أصلية تعتمد على الأحداث (مثل Antigravity / Gemini CLI). استخدمه عندما يحتاج أحد الوكلاء إلى حقن قواعد التحقق المسبق، أو البحث في Memory/Gardener قبل بدء العمل، أو فرض استراتيجيات قراءة مستندات الدليل (CLAUDE.md / AGENTS.md)، أو توجيه مهام Sidecar ديناميكيًا إلى المهارات وبروتوكولات الأمان."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: ar
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: [agy_kontext_and_workflow_loader.py]
provenance:
  origin: "fork of automation-self-care"
  origin_path: "skills/infrastructure/automation-self-care"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: cb03d9a06cc52ced2695c952c855b3d57c168dc5b0a9ad1c412e72da13de1765
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="letter-hooker banner">

# Letter-Hooker (محرك التحقق المسبق والحوكمة على مستوى المطالبة)

تُوسّع مهارة **Letter-Hooker** `automation-self-care` لأطر عمل وكلاء الذكاء الاصطناعي (مثل **Antigravity / Gemini CLI**) التي لا تملك محملات أصلية لخطافات دورة الحياة JSON المعتمدة على الأحداث (مثل `~/.claude/settings.json` أو `~/.codex/hooks.json`).

وبدلًا من الاعتماد على خطافات سلبية تعمل مع كل ضغطة مفتاح، يشغّل `letter-hooker` **بوتلودر تحقق مسبق نشطًا على مستوى المطالبة وحلقة حقن Letter Hook** عبر المهام المجدولة وسكربتات المشرف (`agy_kontext_and_workflow_loader.py`).

---

## الإمكانات الأساسية

1. **بوتلودر التحقق المسبق وقواعد اجتياز المستندات**:
   - **البحث الصاعد والنازل**: يفرض على الوكلاء تعليمات صارمة للتحقق من `AGENTS.md` و`CLAUDE.md` و`START.md` و`RULES.md` و`README.md` في مستوى مجلد العمل الحالي. فإن غابت، يُجتاز المسار صعودًا حتى يُعثر عليها، ثم يُفحص النزول.
   - **التحقق المسبق من Memory وGardener**: استعلام تحقق مسبق إلزامي إلى `gardener` و`memoryhooker` قبل تنفيذ أي تغييرات مدمّرة أو معقدة.

2. **كتالوج Letter Hooks والروابط المرجعية**:
   - ملفات تعليمات `.md` معيارية موجودة ضمن `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/`.
   - يحقن روابط `file://` صريحة مباشرة في نص مطالبة `sidecar.json`، بحيث يقرأ الوكلاء عند الاستدعاء بروتوكولات الأمان وسير العمل الدقيقة.

3. **قائمة الكلمات المفتاحية اليومية وإثراء المطالبات ذاتي الإصلاح**:
   - يحافظ على `STICHWORTLISTE.json` يومية من المهام النشطة/الاحتياطية.
   - يحلل سجلات التنفيذ (`AUTOMATIONS-MEMORY.md`) بحثًا عن أنماط الأخطاء (السياق المفقود، وغياب إرشادات سير العمل، والمسارات غير الصالحة) ويعدّل مطالبات المهام ديناميكيًا.

4. **توجيه المهارات والشخصيات**:
   - يفحص الكلمات المفتاحية للمهام ويربطها بـ `.SKILLS` المناسبة (مثل `infrastructure/condition` و`semantic-persona-routing` و`orchestrator` و`think` و`decide`).

---

## Letter Hooks المهمة

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](hooks/path_validation_and_authority.md)

---

## تكامل سير العمل

```bash
# Letter-Hooker-Wartungs-Engine ausführen
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **فحص الملفات الجانبية (Sidecars)**: قراءة جميع نصوص مطالبات `sidecar.json` في `~/.gemini/config/sidecars/`.
2. **تحديث قائمة الكلمات المفتاحية**: استخراج المصطلحات المتخصصة وحفظها في `.SYNC/STICHWORTLISTE.json`.
3. **حقن Letter Hooks**: إلحاق قواعد البوتلودر وروابط `file://` المرجعية بالمطالبات.
4. **تسجيل النتائج**: تدوين التحديثات في `ANTIGRAVITY-LOG.txt` و`ANTIGRAVITY-REGISTRY.md`.
