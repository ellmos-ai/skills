---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "مهارة فوقية (Meta-skill) لتطوير ألعاب Roblox بشكل كامل باستخدام Rojo — نقطة الدخول التي تعرف المهارات المتخصصة الثلاث `/rojo` (المزامنة من نظام الملفات إلى Studio، وإعداد المشروع)، و`/rbx-studio` (المحرر، وMCP، والأصول، وفحص البرمجيات الخبيثة)، و`/game-design` (الأدوار، وسير العمل، ووثيقة تصميم اللعبة) وتوحّدها. استخدم هذه المهارة لأي مشروع لتطوير ألعاب Roblox: تخطيط لعبة Roblox أو بنائها أو إعدادها، وإنشاء هيكل مشروع جديد، وتحديد بنية الشيفرة (Main + وحدات المديرين، و_G.ClientState + HUD، والـ remotes في GameEnums)، وتجنّب مزالق Luau وRoblox، أو عندما يصعب تحديد أي مهارة متخصصة من مهارات Roblox تناسب المهمة — يتم التوجيه من هنا. كما تُفعَّل عند عبارات مثل \"تطوير لعبة Roblox\"، و\"بناء لعبة Roblox\"، و\"مشروع Roblox جديد\"، و\"بنية مشروع Luau\"، و\"كيف أنظّم شيفرة Roblox\"، و\"إعداد تطوير Roblox\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: ar
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-dev/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 0a489cbd24500517df731518ee92ae3d5881d249873c48d16af4a4d86f6b63a4
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="rbx-dev banner">

> **ملاحظة:** غير تابعة لشركة Roblox Corporation؛ "Roblox" علامة تجارية مملوكة لأصحابها. "rbx" هو الاختصار الشائع في المجتمع.

# Roblox-Dev — مهارة فوقية لتطوير ألعاب Roblox

## الغرض

نقطة الدخول المركزية لتطوير ألعاب Roblox بسير عمل قائم على Rojo وقابل للإصدار والتتبّع.
تجمع هذه المهارة المعرفة الشاملة — بنية المشروع، وأنماط الهندسة، وأهم مزالق Luau — وتوجّه الأسئلة المتخصصة إلى المهارات الفرعية الثلاث:

| المهارة الفرعية | الغرض منها |
| --- | --- |
| **`/rojo`** | المزامنة من نظام الملفات إلى Studio، و`default.project.json`، وrokit/Wally/Lune، وهيكل المشروع، ومشكلات المزامنة |
| **`/rbx-studio`** | تشغيل Studio، ووضع المشهد مقابل وضع الشيفرة، وStudio MCP، وخط أنابيب الأصول، **وفحص البرمجيات الخبيثة** |
| **`/game-design`** | الأدوار والمهام الفرعية، وسلاسل التطوير، ووثيقة تصميم اللعبة (KONZEPT.md)، وتعدد الوكلاء (Multi-Agent) |

> قاعدة التوجيه: إذا كان الأمر يتعلق بـ **المزامنة/البناء/الإعداد** ← `/rojo`. وإذا كان يتعلق بـ **المحرر/الأصول/الاختبار داخل Studio** ← `/rbx-studio`. وإذا كان يتعلق بـ **المفهوم/الأدوار/العملية** ← `/game-design`. أما **بنية الشيفرة، ومزالق Luau، أو سير العمل الكامل** ← ابقَ هنا.

## نظرة عامة على المكدس التقني

- **اللغة:** Luau (`.luau`، وليس `.lua`). الشيفرة بالإنجليزية، والتعليقات والوثائق والنصوص في الواجهة بالألمانية.
- **المزامنة:** Rojo عبر rokit (إصدارات أدوات مثبّتة). نظام الملفات هو مصدر الحقيقة.
- **الأدوات:** Rojo (المزامنة/البناء)، وLune (الاختبارات والنصوص خارج Studio)، وWally (الحزم)،
  واختياريًا Knit (إطار عمل للخدمات/وحدات التحكم، للمشاريع الجديدة)، وSelene (أداة فحص الشيفرة).
- **التحكم:** Roblox-Studio-MCP للفحص والاختبارات وإدراج الأصول بقيادة الذكاء الاصطناعي.

## بنية المشروع (القياسية)

```
ProjektName/
├── default.project.json     # Rojo-Mapping
├── rokit.toml               # gepinnte Tool-Versionen
├── wally.toml               # Package-Dependencies
├── KONZEPT.md               # Game Design Document
├── src/
│   ├── shared/              # → ReplicatedStorage(.ProjektName.shared)
│   │   ├── Config.luau      # zentrale Werte, States, Gameplay-Parameter
│   │   ├── GameEnums.luau   # Enums, Remote-Namen, Konstanten
│   │   └── *Defs.luau       # Datendefinitionen (Items, Einheiten, Level)
│   ├── server/              # → ServerScriptService(.ProjektName)
│   │   ├── Main.server.luau # EINZIGER Server-Entry-Point (Script)
│   │   └── *Manager.luau    # ModuleScripts, von Main per require() geladen
│   ├── client/              # → StarterPlayerScripts(.ProjektName)
│   │   └── GameClient.client.luau   # Client-Entry-Point (LocalScript)
│   └── gui/                 # → StarterGui(.ProjektName)
│       └── *HUD.client.luau # GUI-Aufbau + Heartbeat-Loop
└── assets/                  # optionale .rbxm/.rbxl (scriptfrei)
```

يُنشئ الهيكل الأساسي `/rojo` عبر `scaffold_roblox_project.sh`.

## أنماط الهندسة

**الخادم — Main + وحدات المديرين.** لكل مشروع سكربت **واحد** فقط: `Main.server.luau`. ينشئ مركزيًا مجلد الـ Remotes ويحمّل جميع وحدات الميزات عبر `require()`:
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
جميع ملفات الخادم الأخرى هي `.luau` (ModuleScripts).

**العميل — حالة مشتركة + HUD.** يكتب GameClient حالةً مشتركة، ويقرأها HUD في كل Heartbeat:
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**الـ Remotes — مركزيًا في GameEnums.** عرّف أسماء الـ Remotes مرة واحدة في `GameEnums.Remotes`؛ ينشئ الخادم الأحداث بناءً عليها، ويبحث العميل عنها بالأسماء نفسها. وبذلك لا توجد أي حالات عدم تطابق في النصوص بين الخادم والعميل.

## سير عمل اللعبة الكامل

1. **المفهوم** (`/game-design`): KONZEPT.md — النوع، ونقطة البيع الفريدة، و3–4 آليات أساسية، وتحقيق الدخل.
2. **الإعداد** (`/rojo`): إنشاء الهيكل الأساسي، وتحديد تعيين `default.project.json`.
3. **الخلفية**: Config ← GameEnums ← *Defs ← Main.server ← *Manager.
4. **الواجهة الأمامية**: GameClient ← HUD.
5. **اختبار اللعب بالنماذج الرمادية** (`/rbx-studio`): اللعب أولًا، مع Parts وأي مواد ذكاء اصطناعي عند الحاجة.
6. **ترقية الأصول** (`/rbx-studio`): أصول Creator Store، و**فحص البرمجيات الخبيثة**، وحفظ المشهد كـ .rbxl.
7. **الاختبار** (`/game-design`): ضمان الجودة + ناقد اللعب + اختبارات عمياء بالشخصيات، والتكرار.
8. **الإصدار** (`/game-design`، دور الأعمال): صفحة المتجر، وتحقيق الدخل، والعمليات المباشرة (Live-Ops).

## مزالق Luau/Roblox (قائمة مختصرة)

أكثر المزالق شيوعًا — القائمة الكاملة والمعلّقة:
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md).

- الفاصلة المنقوطة (Semicolon) بعد `task.wait(x)` عندما يتبعها كود آخر في السطر نفسه.
- `Model.Position` غير موجود ← `model:GetPivot().Position`.
- `#table` على القواميس = 0 ← احسب يدويًا.
- `mouse.Hit` قد يكون nil ← تحقّق قبل الاستخدام.
- استدعاءات DataStore **دائمًا** داخل `pcall`.
- `tick()` مهجور ← `os.clock()`؛ `SetPrimaryPartCFrame` ← `PivotTo`.
- أسماء الأحداث مركزيًا في `GameEnums.Remotes`؛ وأنشئ جميع الـ Remotes في `Main.server.luau`.
- لا توجد `require`s دائرية (وإلا حدث Deadlock).
- `require()` فقط على وحدات `.luau` (ModuleScripts)، وليس أبدًا على Scripts/LocalScripts.

## قائمة التحقق قبل كل Commit

- [ ] فواصل منقوطة (Semicolons) بعد `task.wait(...)` في العبارات المتعددة
- [ ] لا يوجد `Model.Position`، ولا `tick()`، ولا `SetPrimaryPartCFrame`
- [ ] DataStore داخل `pcall`، و`mouse.Hit` يُفحص مقابل nil
- [ ] أسماء الأحداث متطابقة بين الخادم والعميل (عبر GameEnums)
- [ ] جميع RemoteEvents منشأة في `Main.server.luau`
- [ ] لا توجد Requires دائرية
- [ ] أصول Marketplace مفحوصة (`/rbx-studio` ← فحص البرمجيات الخبيثة)، وحُفظت التقارير

## مصادر المعرفة

- **أحدث وثائق المحرك/المنشئين:** Context7 MCP — `resolve-library-id` ←
  `/websites/create_roblox_reference_engine` (واجهة برمجة المحرك) و`/roblox/creator-docs`
  (الدروس والأدلة)؛ والبديل <https://create.roblox.com/docs>.
- **خط أنابيب المرجع** (إن كان متاحًا على هذا النظام): `<your Roblox project pipeline>` —
  وتشمل خاصة `SKILL.md`، و`GUIDE.md`، و`LESSONS_LEARNED.md`، و`ROJO_FAQ.md`، و`ROBLOX_MCP_FAQ.md`،
  و`AGENT_ROLES.md`، و`_malware_reports/PATTERNS.md`، و`_knowledge/` (ذاكرة تخزين مؤقت محلية لواجهة البرمجة).

## سجل التغييرات

### 1.0.0 (2026-06-17)
- الإصدار الأولي. مهارة فوقية تشمل `/rojo`، و`/rbx-studio`، و`/game-design`؛ بنية المشروع،
  وأنماط الهندسة، ودروس Luau المستخلصة من خط أنابيب `.ROBLOX`، بصيغة محايدة للمستخدم.
