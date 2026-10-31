---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "يجمع القرارات المفتوحة المترابطة في تصوّر متماسك واحد قائم على النثر، استنادًا إلى جميع البدائل الموصى بها. يوضّح كيف تتشابك الأنظمة الفرعية فعليًا بعد التنفيذ، بدلًا من إجبار المستخدم على الإجابة عن عشرات الأسئلة المنفصلة. يقبل المستخدم الصورة في مجملها أو يقدّم تصحيحات موجّهة تُترجم تلقائيًا إلى قرارات فردية وتُعاد كتابتها في السجل عبر المرحلة 4 من decision-briefing. استخدم هذه المهارة عند عبارات مثل \"كيف يبدو الأمر كله إذا وافقنا على كل شيء\"، \"ارسم لي الصورة الكاملة\"، \"التصوّر الكلي للقرارات\"، \"decision draw\"، /decision-draw، \"كيف تتكامل الأنظمة معًا\". لا تستخدمها عندما يُراد مناقشة البدائل لكل نقطة على حدة — فذلك من اختصاص decision-briefing؛ ولا لرسم مخطط التبعيات — فذلك من اختصاص decision-path؛ ولا للكتل المنظمة المفردة ذات الخيارات والإيجابيات/السلبيات (حتى للمجموعات المترابطة بإحكام) — فذلك من اختصاص decision-shot؛ ولا لاستنباط قرار فردي واحد — فذلك من اختصاص decide."
visibility: public
language: ar
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: da661fa325502ab0dfae6d6655d70650457d6ac1ff27ca5f0ce6289c375ef2c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — الصورة الكلية وقبول القرارات المجمّعة

> عندما تكون هناك خمسة أو عشرة قرارات معلّقة، يسهل أن يضيع البصر في تفاصيل الخيارات الصغيرة عن النظام الذي يتشكّل. لا يصف decision-draw البدائل، بل الكل العامل: كيف تعمل الأنظمة معًا إذا قُبلت جميع التوصيات؟ يقبل المستخدم الصورة في مجملها أو يصحّح نقاطًا محددة.

---

## متى تُستخدم

- عندما تُراد عدة قرارات مترابطة (من [decision-briefing](../decision-briefing/SKILL.md) أو من قالب قرارات) ألّا تُعالج كقائمة متعبة من الأسئلة المفردة.
- عندما يرغب المستخدم، قبل الاعتماد، في رؤية كيف تتفاعل المكوّنات فعليًا في الاستخدام اليومي بعد التنفيذ.
- عندما حُدّدت من مخطط التبعيات ([decision-path](../decision-path/SKILL.md)) مجموعة من القرارات المقترنة بإحكام يمكن قبولها كوحدة وظيفية واحدة.
- كلمات التفعيل: `/decision-draw`، "كيف يبدو الأمر كله إذا وافقنا على كل شيء"، "ارسم لي الصورة الكاملة"، "التصوّر الكلي للقرارات"، "decision draw"، "كيف تتكامل الأنظمة بعد ذلك"، "صورة للقبول الشامل".
- **لا** تُستخدم:
  - عندما يريد المستخدم الموازنة بين الخيارات لكل سؤال واختيارها بالحرف (A/B/C) — فذلك من اختصاص [decision-briefing](../decision-briefing/SKILL.md).
  - للتحليل السببي والكشف عن الانسداد في الطرفية وحدها — فذلك من اختصاص [decision-path](../decision-path/SKILL.md).
  - للموازنة المعزولة للخيارات في كتل فردية من خمسة أجزاء (السياق، والإيجابيات/السلبيات لكل خيار، والتوصية) للأسئلة المفردة أو المجموعات المترابطة بإحكام — فذلك من اختصاص [decision-shot](../decision-shot/SKILL.md).
  - لاستنباط سؤال استراتيجي مفتوح واحد بالمنهج — فذلك من اختصاص [decide](../decide/SKILL.md).

---

## التمييز داخل عائلة القرارات

| المهارة | تجربة الاستخدام والتركيز | الموقف من الخيارات | شكل القبول |
|---|---|---|---|
| `decision-briefing` | **تُفكّك** إلى أسئلة مفردة | تعرض جميع الخيارات A/B/C/D | رموز بالحروف (`1A 2C 3B`) |
| `decision-path` | **تُنظّم** العلاقات السببية | تقيّم الخيارات داخل المخطط | تشخيص في الطرفية (ASCII) |
| `decision-draw` | **صورة متماسكة للهدف** (تجمع القرارات المترابطة) | تصف **الخيار الموصى به فقط** (والبدائل مرتبطة) | قبول شامل أو جملة تصحيح |
| `decision-shot` | **كتل منظمة مفردة** (للأسئلة الفردية أو المجموعات المحكمة) | تعرض الخيارات مع 2–4 نقاط إيجابية/سلبية | قرار تنفيذي / قبول فردي |
| `decide` | **تستنبط** الحالة الفردية | مصفوفة تقييم (معايير) | توصية تحليلية |

> **القاعدة المركزية:**
> `decision-draw` يصف **الخيار الموصى به فقط**. البدائل المرفوضة لم تختفِ — فهي موثّقة في [decision-briefing](../decision-briefing/SKILL.md) أو [decision-shot](../decision-shot/SKILL.md) أو التذاكر المرتبطة، وتُربط في الترويسة. فالتصوير بدون هذا المرجع يحرم المستخدم من الاختيار بدلًا من تيسيره.

---

## قاعدة الأسلوب الملزمة: نصوص للمستخدم بلا رموز وأرقام

> **التوجيه الأساسي للمستخدم (ملاحظة 2026-09-13 / التذكرة T-20260913-883789445):**
> *«صور القرارات الشاملة تبدو لي تقنية أكثر من اللازم، يجب أن تكون بلا أرقام، أنت تعرفها في الخلفية أو تستعملها لكتابة النص [...].»*

1. **لا رموز تقنية في النص الظاهر للمستخدم:**
   في النص الظاهر المخصص للإنسان (الحزمة، المفهوم، التفاعل، التنفيذ، الاستعلام) **لا** توجد رموز داخلية (مثل `BH-A` و`MD-A` و`HA-A` و`PRA`)، ولا أرقام تذاكر (`T-2026...`)، ولا أرقام قرارات D (`D-2026...`)، ولا مسارات نسبية، ولا معرّفات Git، ولا قيم قياس.
2. **لكل بند 2–4 جمل بلغة يومية بصيغة المتكلم:**
   يُصاغ كل بند في الحزمة وفق ثلاثية:
   - *الوضع:* ما الحالة الراهنة؟
   - *«أنا أفعل …»:* ما الخطة الملموسة / ما التوصية العملية؟
   - *الاحتياط:* ماذا يحدث إذا فشل ذلك، أو ماذا يقرّر المستخدم بعده؟
   *(مثال: «يدعم Hermes المهام بالإنجليزية فقط. أبلّغ Hermes عن ذلك كمشكلة، ونبني لنا حلًا مؤقتًا. توجد حاليًا جلسات قديمة غير قابلة للاستخدام. أحاول إعادتها للعمل. إن لم ينجح ذلك، أعطيك عينة عشوائية من 10 جلسات وألخّصها — حتى تقرر إن كان الإنقاذ مفيدًا.»)*
3. **عناوين واضحة بالألمانية للتوجيه:**
   يحمل كل بند عنوانًا مفهومًا (مثل *„Modell-Backend als eigenes Herzstück“*، *„Sichere Deploy-Schlüssel auf dem Mac“*). يتفاعل المستخدم عبر هذا العنوان أو يعطي قبولًا شاملًا.
4. **الربط التقني حصرًا في الملحق:**
   يتم الربط بين العنوان الواضح والرمز الداخلي ومعرّف التذكرة وحالة السجل **حصرًا في جدول ملحق ختامي** في نهاية المستند — وهناك فقط تعمل أدوات التحليل الآلي وإعادة الكتابة في السجل.

---

## البنية الملزمة (ثمانية أجزاء)

يتبع `decision-draw` الكامل هذه البنية دون استثناء:

### 1. الحزمة والنطاق (بلغة واضحة)
عرض موجز للبنود المجمّعة بلغة يومية (بصيغة المتكلم، 2–4 جمل لكل نقطة، دون معرّفات أو رموز في النص).

### 2. المفهوم
الحالة المستهدفة كنص متصل قائم على النثر:
- ما المشهد النظامي أو سير العمل الذي ينشأ إذا نُفّذت كل التوصيات كما هي؟
- بلا مقابلة للخيارات، وبلا جمل شرطية متوازية («يمكن أيضًا …»).
- صيغة خبرية واضحة ودقيقة: هكذا يعمل النظام في الحالة المستهدفة.

### 3. التفاعل
المحور الوظيفي للمهارة:
- كيف تتشابك الأجزاء المقررة **بعد** التنفيذ فعليًا؟
- يُفضّل العرض وفق سير شامل ملموس من البداية إلى النهاية بدلًا من قائمة مكوّنات مجرّدة.
- يوضح تدفقات البيانات والواجهات والمسؤوليات.

### 4. التنفيذ
ترتيب التحقيق الفعلي:
- ماذا يحدث فعليًا في الممارسة؟
- يأخذ منطق الحواف والتبعيات مباشرة من [decision-path](../decision-path/SKILL.md).
- تُعرض المسارات المستقلة كمتوازية بصدق (لا تُختلق سلاسل سببية مصطنعة؛ قد تتكوّن الحزمة من عدة مسارات متوازية). لا تُذكر ترتيبات إلا حيث توجد تبعيات أو مواعيد موثّقة.
- يسمّي البوابات وخطوات الترحيل والفحوص.

### 5. ما لا تغطيه هذه الصورة
حماية من الاكتمال الوهمي:
- ما المسائل الهامشية أو النقاط المفتوحة أو درجات الثقة 🔴 التي تُستبعد عمدًا؟
- أين تقع حدود الواجهات مع الأنظمة المجاورة؟
- الصورة التي تُخفي حوافها تخلق أمانًا كاذبًا.

### 6. القبول
التفاعل مع المستخدم:
- يتحقق المستخدم من الصورة في مجملها.
- الخيار الأول: **قبول شامل صريح** («مناسب»، «موافق»، «نفّذها هكذا»). عندها فقط تُسجَّل جميع بنود الحزمة كمقررة.
- الخيار الثاني: **تصحيح بالعنوان الواضح أو بلغة يومية** («عند نشر الحاسوب لا إعادة تشغيل تلقائية»، «نؤجّل VersicherungsManager أولًا»). يؤدي ذلك إلى تفكيك القرارات الفردية، وتبقى جميع البنود غير المصحَّحة مفتوحة.

### 7. النقل العكسي
الترجمة المنهجية لتصحيحات المستخدم إلى قرارات فردية:
- **لا تسجيل تلقائي مع الآخرين:** لا تُسجَّل البنود غير المتغيرة إلا عند قبول شامل صريح. التصحيح الجزئي **ليس** قبولًا شاملًا!
- **العزل عند التصحيح:** عند ورود تصحيح يُفكَّك إلى قرارات فردية، وتبقى جميع البنود الأخرى في الحزمة **مفتوحة** بصرامة (في سجل المصدر / القالب) حتى يقبل المستخدم الصورة المصحَّحة في مجملها أو يؤكد البنود المتبقية فرادى.
- **جدول النقل العكسي الإلزامي:** كل ردّ تصحيح يُنتج حتمًا جدول تقييم منظّمًا بأربعة أعمدة (التصحيح الأصلي، الرموز المتأثرة، حالة التأثير المتتالي، الغموض المفتوح).
- **مسار الكتابة الحصري عبر المرحلة 4:** لا يملك `decision-draw` مسار كتابة خاصًا به في السجل. يتم التسجيل **حصرًا** عبر الإجراء الموحّد في المرحلة 4 من [decision-briefing](../decision-briefing/SKILL.md).

### 8. الملحق: جدول مرجعي تقني (للتسجيل والتدقيق فقط)
جدول مختصر في نهاية المستند يتضمن:
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## مثال (مقتطف تجريبي: التذكرة الرئيسية 2026-09-13 — BACH ومنظومة الأنظمة)

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## قواعد عملية

1. **لا صيغة شرطية في المفهوم:** صِف النظام الكامل كما لو كان منفّذًا فعلًا. يريد المستخدم وضوح النتيجة لا احتمالات نظرية.
2. **السببية قبل التسلسل الزمني:** يتبع الترتيب في قسم *التنفيذ* مستويات مخطط التبعيات من [decision-path](../decision-path/SKILL.md). تُعرض المسارات المستقلة كمتوازية بصدق ولا تُلوى إلى سلسلة سببية مصطنعة.
3. **فحص التأثير المتتالي الإلزامي في النقل العكسي:** لا يُسجَّل تصحيح للمستخدم منفردًا دون التحقق مما إذا كانت العُقد التابعة في المخطط تتأثر أو تفقد صلاحيتها.
4. **لا تسجيل تلقائي مع تصحيحات جزئية:** لا تُسجَّل البنود غير المتغيرة إلا عند قبول شامل صريح. عند كل تصحيح جزئي تبقى جميع البنود غير المتأثرة مفتوحة بصرامة حتى تُعاد الموافقة على الصورة الكاملة أو تُؤكَّد البنود فرادى.
5. **مسار الكتابة الحصري عبر المرحلة 4:** لا يملك `decision-draw` مسار كتابة خاصًا به في السجل. تتم التسجيلات حصرًا عبر المرحلة 4 من [decision-briefing](../decision-briefing/SKILL.md).
6. **احترم عقود السجل:** تتم التسجيلات دائمًا وفق قواعد سجل القرارات (لا إعادة ترقيم للمعرّفات، رموز تسجيل فريدة، الهدف الأساسي `DECIDED-AND-DONE.md`).
7. **نصوص للمستخدم بلا أرقام ولا رموز تقنية:** في النص الظاهر للإنسان لا توجد معرّفات أو رموز أو مسارات أو أرقام تذاكر. يُصاغ كل بند بلغة يومية بصيغة المتكلم، وتنتقل جميع المعرّفات إلى جدول الملحق.

---

## مصدر الجلسة

عند حفظ تصوّر قرارات كمستند تصوّر دائم، ينتهي بـ:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- أولوية المصدر: صراحةً وقت التشغيل أو سطر الأوامر، ثم بيئة المزوّد الموثوقة أو الخطاف، وإلا `unbekannt`.
- يرث الوكلاء الفرعيون معرّف جلسة الجلسة الأم.
- لا تحصل القوالب النصية البحتة على ختم.

---

## سجل التغييرات

### 1.1.0 (2026-09-18)
- تثبيت قاعدة الأسلوب للنصوص الموجّهة للمستخدم (T-20260913-883789445، توجيه المستخدم 2026-09-13):
  - لا رموز تقنية، ولا أرقام تذاكر أو قرارات D، ولا مسارات أو قيم قياس في النص الظاهر للمستخدم.
  - 2–4 جمل بلغة يومية بصيغة المتكلم (الوضع، «أنا أفعل …»، الاحتياط) لكل بند.
  - عناوين واضحة لتحديد البنود وقبولها.
  - نقل الربط التقني (الرمز، معرّف التذكرة، حالة السجل) حصرًا إلى جدول الملحق الختامي (القسم 8).

### 1.0.1 (2026-09-13)
- تدقيق بعد المراجعة:
  - تشديد عقد النقل العكسي: لا تسجيل تلقائي مع التصحيحات الجزئية؛ تبقى البنود غير المتأثرة مفتوحة بصرامة حتى القبول الشامل.
  - إدخال جدول إلزامي للنقل العكسي بأربعة أعمدة (التصحيح الأصلي، الرموز المتأثرة، حالة التأثير المتتالي، الغموض المفتوح).
  - عرض تعدد المطابقات في المثال (يحرّك تصحيح واحد للمستخدم `MD-A` و`CF-A` معًا).
  - تثبيت مسار الكتابة الحصري عبر المرحلة 4 لـ `decision-briefing` في العقد والمثال.
  - تصحيح افتراض السلسلة السببية في المثال: عرض البنود المستقلة كأربعة مسارات متوازية بصدق (المخرج أ).
  - توضيح التمييز عن `decision-shot` عبر شكل المخرج (كتل منظمة مع إيجابيات/سلبيات مقابل صورة متماسكة للهدف مع قبول شامل).

### 1.0.0 (2026-09-13)
- الصياغة الأولى استنادًا إلى طلب المستخدم T-20260913-107991667.
- البنية الملزمة من سبعة أجزاء (الحزمة، المفهوم، التفاعل، التنفيذ، الحدود، القبول، النقل العكسي).
- منطق التجميع استنادًا إلى `decision-path` وجسر الكتابة إلى السجل عبر المرحلة 4 لـ `decision-briefing`.
