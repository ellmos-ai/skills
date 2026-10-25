---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "تشغيل Rojo — أداة مزامنة من نظام الملفات إلى Roblox Studio لتطوير Roblox الاحترافي في VS Code / Claude Code بدلًا من محرّر Studio. استخدم هذه المهارة كلما كان Rojo معنيًا: `rojo serve`/`rojo build`، وكتابة `default.project.json` أو تصحيحه، وrokit/rokit.toml وإصدارات الأدوات (Rojo وLune وWally)، وربط المسارات المتداخلة مقابل المسطحة (ReplicatedStorage.Project.shared)، ومشكلات connect/port/sync، أو عندما يلزم إنشاء هيكل مشروع Roblox. كما تُفعَّل عند عبارات مثل \"rojo connect not working\"، و\"scripts end up in the wrong place in Studio\"، و\"how do I map src/ to Studio\"، و\"port 34872 in use\"، و\"ModuleScript vs Script in Rojo\"، وعبارات عربية مثل \"الاتصال عبر rojo connect لا يعمل\"، و\"تظهر السكربتات في المكان الخطأ داخل Studio\"، و\"كيف أربط src/ بـ Studio\"، و\"المنفذ 34872 مستخدم\"، و\"ModuleScript مقابل Script في Rojo\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: ar
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rojo/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 2901142af2c1b72480d9cfaea5111557a8c6003c6b51aefa4bab02a0e168b742
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="rojo banner">

# Rojo — مزامنة من نظام الملفات إلى Roblox Studio

## الغرض

يربط Rojo مشروع نظام ملفات عاديًا (ملفات `.luau` في `src/`، مُدارة بالإصدارات عبر Git)
مع Roblox Studio. تكتب الشيفرة في المحرّر الذي تفضّله (VS Code، وClaude Code)، ويزامنها Rojo مباشرةً
إلى نسخة Studio قيد التشغيل. بهذا تصبح شيفرة Roblox قابلة للإصدار والمقارنة والتحرير بأدوات حقيقية،
بدلًا من أن تعيش في محرّر النصوص المدمج في Studio.

استخدم هذه المهارة لكل ما يتعلق بإعداد Rojo، وبمخطط ربط `default.project.json`، وبسلسلة الأدوات
(rokit وWally وLune)، وبمشكلات المزامنة الشائعة.

## النموذج الذهني

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**القاعدة الأساسية:** نظام الملفات هو مصدر الحقيقة. يستبدل Rojo عند كل اتصال محتوى مناطق Studio المربوطة
بمحتوى نظام الملفات. لذلك لا تعدّل الشيفرة **أبدًا** داخل Studio (فهذا يضيع عند المزامنة التالية)، بل
في المحرّر فقط. أما `Workspace` (مشهد ثلاثي الأبعاد، والتضاريس) ف**لا** يربطه Rojo
ويبقى كما هو — راجع مهارة `/rbx-studio` لسير عمل المشهد مقابل الشيفرة.

## امتدادات الملفات ← نوع Roblox (اصطلاح Rojo)

يستنتج Rojo نوع النسخة من الامتداد. وهذا أكثر مصادر الخطأ شيوعًا:

| الملف              | نوع Roblox    | قابل لـ `require()` | الدور                     |
| ------------------ | ------------- | --------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **نعم**         | وحدة منطق، وتعريفات       |
| `Foo.server.luau`  | Script        | لا              | نقطة دخول الخادم          |
| `Foo.client.luau`  | LocalScript   | لا              | نقطة دخول العميل          |
| `init.luau`        | يصبح عقدة المجلد نفسها | نعم | يجعل المجلد ModuleScript |

> قاعدة عامة: **نقاط الدخول فقط** هي `.server.luau`/`.client.luau`. وكل ما يُحمَّل عبر
> `require()` **يجب** أن يكون `.luau` من نوع ModuleScript. استدعاء `require()` على
> Script/LocalScript يطلق الخطأ "Attempted to call require with invalid argument(s)".

## أوامر CLI

```bash
rojo serve default.project.json     # Live-Sync-Server starten (Standard-Port 34872)
rojo serve                          # nutzt default.project.json automatisch
rojo build default.project.json -o game.rbxlx   # einmaliger Build → Place-Datei (XML)
rojo build default.project.json -o game.rbxl    # Build → Place-Datei (binär)
rojo plugin install                 # Rojo-Studio-Plugin installieren (einmalig)
rojo --version                      # installierte Version prüfen
```

بعد `rojo serve`: افتح إضافة Rojo في Studio ← **Connect** (localhost:34872).
لا يحتاج `rojo build` إلى تشغيل Studio — وهو مثالي لـ CI واختبارات الدخان والإصدارات.

## `default.project.json` — المخطط

يربط هذا الملف مسارات نظام الملفات بتسلسل Datamodel في Roblox. المفاتيح:

- `name` — اسم المشروع (للعرض)
- `$className` — فئة Roblox للعقدة (`DataModel`، `ServerScriptService`، `Folder`، …)
- `$path` — مسار نظام الملفات الذي يُزامَن تحت هذه العقدة (نسبةً إلى جذر المشروع)

يوجد قالب قياسي جاهز للاستخدام في [`assets/default.project.json`](assets/default.project.json).

### مسطّح مقابل متداخل — أهم قرار

يجب أن تتطابق شيفرتك مع المخطط. هناك متغيران:

**مسطّح** — يُوضع محتوى `src/server` مباشرةً داخل `ServerScriptService`:
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
← تشير الشيفرة مثلًا إلى `ReplicatedStorage.Config`، و`ReplicatedStorage.GameEnums`.

**متداخل** — يُوضع المحتوى داخل `ServerScriptService.ProjektName`:
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
← تشير الشيفرة إلى `ReplicatedStorage.ProjektName.shared.Config` وهكذا.

كلاهما صالح. اختر على مستوى المشروع **واحدًا** منهما والتزم بتوافق كل مسار `require`/`WaitForChild` معه.
العَرَض عند عدم التطابق: يتعلق `WaitForChild(...)` إلى ما لا نهاية (Infinite yield)، لأن العقدة المتوقعة موجودة في موضع آخر.

## سلسلة الأدوات عبر rokit

[rokit](https://github.com/rojo-rbx/rokit) هو مدير سلسلة الأدوات. يثبّت ملف `rokit.toml` داخل
المشروع (أو مجلد أبٍ له) إصدارات أدوات دقيقة ← بناءات قابلة للتكرار على كل الأجهزة. وإذا غاب الملف، يظهر `Failed to find tool 'rojo' in any project manifest file`.

`rokit.toml` القياسي (راجع [`assets/rokit.toml`](assets/rokit.toml)):
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> ملاحظة حول الإصدار: الإصدار 7.4.4 هو المثبّت باستمرار في خط الأنابيب المرجعي. قد تنتقل المشاريع الأحدث إلى 7.6.x — لكن تحقق منه أولًا بـ `rojo build` على المشروع،
> لأن صيغة المشروع قد تتغير بين الإصدارات الرئيسية.

بعد النسخ/الإعداد: يسحب `rokit install` جميع الأدوات المثبّتة.

- **Lune** — مشغّل Luau خارج Studio (اختبارات الوحدة، وسكربتات البناء، ومعالجة الأصول).
- **Wally** — مدير الحزم: `wally install` ← `Packages/` ← في Studio ضمن
  `ReplicatedStorage.Packages`. تُخزَّن التبعيات في `wally.toml` (راجع
  [`assets/wally.toml`](assets/wally.toml))، مثل إطار العمل `sleitnick/knit@1.7.0`.

## إنشاء مشروع جديد

ينشئ السكربت [`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) هيكل Rojo كاملًا (project.json، وrokit.toml، وwally.toml، و`src/{shared,server,client,gui}/`
مع ملفات بداية، وقالب KONZEPT):

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # flaches Mapping (Default)
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # verschachteltes Mapping
```

ثم: `cd MeinSpiel && rokit install && rojo serve`.

## استكشاف الأخطاء وإصلاحها

| العَرَض | السبب | الحل |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | لا يوجد `rokit.toml` | أنشئ `rokit.toml` مع تثبيت Rojo في المشروع/مجلد الأب، ثم `rokit install` |
| `require` يطلق "invalid argument(s)" | `require()` على Script/LocalScript | فقط `.luau` من نوع ModuleScript قابل لـ require؛ تحقق من الامتداد |
| المنفذ 34872 مشغول (`os error 10048`) | عملية Rojo قديمة لا تزال تعمل | `tasklist \| grep -i rojo` ← `taskkill //PID <PID> //F`، ثم أعد `rojo serve` |
| تقع السكربتات في الموضع الخطأ في Studio | مخطط مسطّح بدلًا من متداخل (أو العكس) | عدّل `default.project.json` ليطابق مسارات الشيفرة (راجع أعلاه) |
| `WaitForChild` يتعلق إلى ما لا نهاية | العقدة المتوقعة غير موجودة / خطأ في الخادم قبل الإنشاء | **تحقق أولًا من Server-Console بحثًا عن الأخطاء**؛ وراجع المخطط وترتيب الإنشاء |
| لا تحدث المزامنة بعد إعادة تسمية ملف | لا يكتشف Rojo إعادة التسمية فورًا | أوقف الخادم (Ctrl+C) وأعد تشغيله، وفي Studio: Disconnect ثم Reconnect |
| تختفي تغييرات Studio بعد إعادة الاتصال | تعديل في Studio بدلًا من تعديل نظام الملفات | عدّل الشيفرة **فقط** في المحرّر؛ يستبدل Rojo المناطق المربوطة |

### حدود Rojo المعروفة

1. **لا مزامنة للتضاريس/مساحة العمل** — ابنِ المشهد ثلاثي الأبعاد والتضاريس في Studio أو وَلِّدْهما بالشيفرة.
2. **لا دمج `.rbxl`** — ملفات Place ثنائية، ولا يمكن دمجها عبر git. لا تعتمد عليها كمصدر أساسي أبدًا.
3. **لا مزامنة حية في وضع اللعب** — تُلغى التغييرات التي تحدث أثناء اللعب عند الإيقاف.
4. **ترجمة المسارات في Git Bash** — قد تُترجم `/c/...` إلى `C:/...` فتتعطل مسارات Rojo؛ عند الشك استخدم مسارات نسبية أو مسارات Windows الأصلية.

## التدقيق اللغوي (Selene)

تُدقَّق مشاريع Roblox Luau عادةً بأداة **Selene** (`selene.toml` في الجذر،
`std = "roblox"`). اسمح بالمتغيرات العامة مثل `_G` عبر `global_usage = "allow"` عندما يستخدم المشروع
حالة عميل مشتركة. شغّل Selene من الدليل الذي يحوي تعريف واجهة برمجة Roblox
(`roblox.yml`).

## للاطلاع

- المهارات الشقيقة: `/rbx-studio` (تشغيل Studio، وMCP، والأصول)،
  `/game-design` (الأدوار، وسير العمل، وGDD)، والمهارة الفوقية `/rbx-dev` (تجمع الثلاث مع أنماط المعمارية).
- وثائق المحرك وRojo الحديثة: Context7 MCP (`resolve-library-id` ←
  `/websites/create_roblox_reference_engine`، `/roblox/creator-docs`) أو
  <https://rojo.space/docs/>.
- إن كان متاحًا على هذا النظام، توجد خط أنابيب مرجعي غني بالمشاريع تحت
  `<your Roblox project pipeline>` (منها `ROJO_FAQ.md`، و`SKILL.md`).

## سجل التغييرات

### 1.0.0 (2026-06-17)
- الإصدار الأولي. مستخلص من خط أنابيب `.ROBLOX` (ROJO_FAQ، وROJO_START، والقالب _template)،
  صيغ بشكل محايد للمستخدم.

## المهارات ذات الصلة

- `roblox-team-lock` — مطالبات الملفات وStudio وMCP عندما يعمل عدة وكلاء على المشروع نفسه. اقرأ أولًا، ثم احجزها، ثم اعمل، ثم حرّرها.
