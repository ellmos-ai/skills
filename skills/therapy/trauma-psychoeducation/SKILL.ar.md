---
name: trauma-psychoeducation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "التثقيف النفسي للصدمات: تعريف الصدمة، والتفاعلات الطبيعية، ونافذة التحمّل، وإدارة المحفّزات، والرعاية الذاتية."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [trauma, psychoedukation, window-of-tolerance, trigger, selbstfürsorge, ptbs]
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
  origin_path: "system/skills/therapie/trauma_psychoedukation.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ac52bd5204d10d048a095b234e73ff829346834b196f90ef520b5b24c2948be9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.188621+00:00"
---
<img src="banner.png" width="100%" alt="trauma-psychoeducation banner">

# التثقيف النفسي للصدمات

> معرفة حول الصدمة وعواقبها ونافذة التحمّل: فهم التفاعلات الطبيعية تجاه أحداث غير طبيعية — تثقيف نفسي بحت، وليس معالجة للصدمة

انظر: [ETHICS.md](../ETHICS.md)

**انظر أيضًا:** [stabilization-techniques](../stabilization-techniques/SKILL.md) (التأريض، والمكان الآمن، والاحتواء — تقنيات فورية) | [psychoeducation](../psychoeducation/SKILL.md) (اضطراب ما بعد الصدمة في سياق اضطرابات أخرى)

---

## السياق

يساعد التثقيف النفسي حول الصدمة المتضررين على فهم تفاعلاتهم وتصنيفها.
فمعرفة أن أعراضًا مثل الذكريات الومضية (الفلاش باك) أو فرط الاستثارة أو التجنب
هي تفاعلات طبيعية تجاه أحداث غير طبيعية تُخفف العبء بالفعل، وتقلل الخجل ولوم الذات.

الدليل: يُعد التثقيف النفسي جزءًا معترفًا به من علاج الصدمات
(Flatten et al. 2011، الإرشادات التوجيهية من المستوى S3 لاضطراب ما بعد الصدمة). ولا يكفي وحده كتدخل،
لكنه قد يرفع الدافعية للعلاج ويخفف الأعراض.

**مهم:** لا تنقل هذه المهارة إلا المعرفة حول الصدمة.
ولا تُجري معالجة للصدمة، ولا تستكشف الذكريات المؤلمة، ولا تسأل عن تفاصيل الصدمة.
**لا تُطبَّق أبدًا:** EMDR، والتعرّض المطوّل (PE)، والعلاج بالتعرّض السردي (NET)

---

## 1. ما هي الصدمة؟

### التعريف

الصدمة حدث يتجاوز قدرات الشخص على التكيّف، ويقترن بتجربة العجز وفقدان السيطرة و/أو الخوف من الموت.
الحدث وحده لا يُعرّف الصدمة، بل التجربة الذاتية.

### أنواع الصدمة

| النوع | الوصف | أمثلة |
|-----|-------------|----------|
| النوع الأول (الصدمة المفردة) | حدث واحد غير متوقع | حادث، اعتداء، كارثة طبيعية |
| النوع الثاني (الصدمة المعقّدة) | تعرّض متكرر وطويل الأمد للصدمة | إساءة، إهمال، حرب |
| الصدمة العرضية | أحداث عشوائية | حادث مروري، حريق منزل، حادث عمل |
| الصدمة بين الأشخاص | تسببها أفعال بشرية | عنف، إساءة، تعذيب |
| الصدمة الثانوية | ناتجة عن المشاهدة أو الشهادة | المهن المساعِدة، الأقارب |

### ما ليس صدمة (تمييز)

ليس كل حدث مؤلم صدمةً بالمعنى السريري:
- الانفصال والفصل من العمل والشجار — مؤلمة، لكنها عادةً ليست صدمة
- التنمر — قد يكون صادمًا (خاصةً للأطفال)، لكنه ليس صدمة تلقائيًا
- التقييم الفردي هو الفيصل، لا نوع الحدث

---

## 2. تفاعلات طبيعية تجاه أحداث غير طبيعية

### أنماط التفاعل الثلاثة

```
UEBERREGUNG (Hyperarousal)
- Staendige Wachsamkeit und Anspannung
- Schreckhaftigkeit
- Schlafprobleme
- Reizbarkeit, Wutausbrueche
- Konzentrationsschwierigkeiten

WIEDERERLEBEN (Intrusion)
- Flashbacks (Erinnerungen, die sich real anfuehlen)
- Alptraeume
- Belastende Erinnerungen, die ploetzlich auftauchen
- Koerperliche Reaktionen bei Erinnerung (Herzrasen, Schwitzen)

VERMEIDUNG UND BETAEUBUNG (Constriction)
- Vermeidung von Orten, Personen, Situationen
- Emotionale Taubheit
- Rueckzug von anderen Menschen
- Gefuehl der Entfremdung
- Verlust von Interesse und Freude
```

### الرسالة المهمة للمتضررين

```
"Diese Reaktionen sind NORMALE Reaktionen auf UNNORMALE Ereignisse.

Dein Koerper und dein Verstand versuchen, dich zu schuetzen.
Die Wachsamkeit schuetzt dich vor erneuter Gefahr.
Die Erinnerungen versuchen, das Erlebte zu verarbeiten.
Die Vermeidung schuetzt dich vor Ueberwaltigung.

Du bist nicht 'verrueckt'. Du bist nicht 'schwach'.
Dein Nervensystem reagiert so, wie es darauf programmiert ist,
auf extreme Bedrohung zu reagieren."
```

### المسار الزمني

```
VERLAUF NACH TRAUMATISCHEM EREIGNIS

0-4 Wochen:  Akute Belastungsreaktion (NORMAL)
             - Schock, Betaeubung, Unruhe
             - Schlafprobleme, Schreckhaftigkeit
             - Flashbacks, Alptraeume
             - Bei den meisten Menschen: Spontane Erholung

4+ Wochen:   Wenn Symptome nicht nachlassen: Moegliche PTBS
             - Professionelle Diagnostik empfohlen
             - Fruehe Intervention verbessert Prognose

Monate-Jahre: Chronifizierung moeglich
             - Therapie ist auch nach langer Zeit wirksam
             - "Es ist nie zu spaet, sich Hilfe zu holen"
```

---

## 3. نافذة التحمّل (Window of Tolerance)

### النموذج (وفق Dan Siegel)

```
            ________________________________________________
           |                                                |
           |   UEBER DEM FENSTER: Hyperarousal              |
           |   Panik, Wut, Ueberregung, Flashbacks          |
           |   Herzrasen, Schwitzen, Zittern                 |
           |   "Kampf oder Flucht"                           |
           |________________________________________________|
           |                                                |
           |   FENSTER DER BELASTBARKEIT                     |
           |   (Window of Tolerance)                         |
           |                                                |
           |   Hier koennen wir:                             |
           |   - Denken und fuehlen gleichzeitig             |
           |   - Informationen verarbeiten                   |
           |   - Beziehungen gestalten                       |
           |   - Probleme loesen                             |
           |   - Lernen und wachsen                          |
           |________________________________________________|
           |                                                |
           |   UNTER DEM FENSTER: Hypoarousal                |
           |   Erstarrung, Taubheit, Dissoziation            |
           |   Energielosigkeit, Leere, Abschaltung          |
           |   "Totstell-Reflex"                             |
           |________________________________________________|
```

### ماذا يعني ذلك؟

- **داخل النافذة:** نستطيع تنظيم الضغط والعمل
- **فوق النافذة:** استثارة مفرطة — الجسم في وضع الإنذار
- **تحت النافذة:** استثارة منخفضة — الجسم يتوقف عن العمل

### الصدمة والنافذة

```
VOR dem Trauma:           NACH dem Trauma (unbehandelt):

|_______________|         |_____|
|               |         |     |  <- Fenster ist ENGER geworden
|    FENSTER    |         | F.  |
|   (breit)     |         |     |
|_______________|         |_____|

Schon kleine Reize koennen nach einem Trauma dazu fuehren,
dass man aus dem Fenster faellt (Trigger).

ZIEL der Therapie: Das Fenster wieder WEITEN.
```

### فهم المحفّزات

```
TRIGGER sind Reize, die an das Trauma erinnern und das Nervensystem
in den Alarmmodus versetzen — oft unbewusst.

Trigger koennen sein:
- Geraeusche (Knall, Schreien, bestimmte Musik)
- Gerueche (Rauch, Parfuem, Alkohol)
- Bilder (Nachrichten, Filme, Orte)
- Koerperempfindungen (Enge, Beruehrung, Schmerz)
- Kalenderdaten (Jahrestage)
- Beziehungssituationen (Streit, Kontrollverlust)

Trigger sind KEINE Schwaeche. Sie sind gespeicherte Warnsignale
des Nervensystems. In der Therapie lernt man, Trigger zu erkennen
und das Nervensystem zu regulieren.
```

---

## 4. استراتيجيات الرعاية الذاتية

### ضمان الاحتياجات الأساسية

```
CHECKLISTE GRUNDBEDUERFNISSE

[ ] Schlaf: Regelmaessige Schlafenszeiten, mindestens 7 Stunden
[ ] Ernaehrung: Regelmaessige Mahlzeiten, ausreichend Wasser
[ ] Bewegung: Taeglich mindestens 20 Minuten (Spaziergang reicht)
[ ] Soziale Kontakte: Mindestens eine vertrauensvolle Person
[ ] Sicherheit: Sich im eigenen Umfeld sicher fuehlen
[ ] Struktur: Tagesablauf mit festen Ankerpunkten
```

### استراتيجيات الرعاية الذاتية في الحياة اليومية

**الجسدية:**
- الحركة المنتظمة (تخفض هرمونات التوتر)
- تمارين التنفس
- نوم كافٍ (مع مراعاة نظافة النوم)
- تقليل الكافيين والكحول (فهما يعززان فرط الاستثارة أو الخدر)

**الاجتماعية:**
- وجود شخص موثوق (لا يلزم الحديث عن الصدمة)
- تجنب العزلة — فالتواصلات الصغيرة تساعد أيضًا
- تعلم وضع الحدود (يحق لك أن تقول "لا")
- قبول الدعم

**العاطفية:**
- تسمية المشاعر (دون تقييمها)
- استخدام تقنيات التثبيت (5-4-3-2-1، المكان الآمن)
- كتابة يوميات (اختياري، دون إلزام)
- إيجاد وسائل تعبير إبداعية (الرسم، الموسيقى، الكتابة)

**المعرفية:**
- الاطلاع (التثقيف النفسي — هذه المهارة)
- مساءلة لوم الذات ("لم يكن ذنبي")
- فحص الواقع عند التهويل الكارثي
- الصبر على الذات (التعافي يحتاج إلى وقت)

---

## 5. العثور على المساعدة المهنية

### متى تُطلب المساعدة المهنية؟

```
PROFESSIONELLE HILFE IST ANGEZEIGT, WENN:

- Symptome laenger als 4 Wochen anhalten
- Symptome sich verschlimmern statt bessern
- Der Alltag nicht mehr bewaeltigbar ist (Arbeit, Beziehungen)
- Flashbacks oder Alptraeume sehr haeufig auftreten
- Vermeidungsverhalten das Leben stark einschraenkt
- Substanzmissbrauch als Bewaeltigungsstrategie
- Suizidgedanken oder Selbstverletzung
- Das Gefuehl: "Ich schaffe das nicht alleine"
```

### جهات الاتصال (ألمانيا)

```
SOFORTHILFE:
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222 (24/7, kostenlos)
- Krisenchat: krisenchat.de (per Chat, fuer junge Menschen)
- Psychiatrischer Notdienst: 112

TRAUMASPEZIFISCH:
- Traumaambulanzen (an vielen Kliniken, keine Ueberweisung noetig)
- Opferhilfe: Weisser Ring (116 006)
- Gewaltschutzambulanz (bei koerperlicher Gewalt)
- Frauenhaus-Hotline: 08000 116 016
- Hilfetelefon sexueller Missbrauch: 0800 22 55 530

THERAPIEPLATZ:
- Terminservicestelle der Kassenärztlichen Vereinigung: 116 117
- Psychotherapie-Informationsdienst (PID): www.psychotherapiesuche.de
- Wichtig: Auf "Traumatherapie" spezialisierte Therapeuten suchen
```

---

## 6. الأسئلة الشائعة (FAQ)

### "هل أنا مصاب بصدمة الآن؟"

ليس كل من يعيش حدثًا مؤلمًا يطوّر اضطرابًا مرتبطًا بالصدمة.
يتعافى غالبية الناس تلقائيًا خلال أسابيع. ولا يستطيع سوى مختص تشخيص ما إذا كان اضطراب ما بعد الصدمة موجودًا.

### "هل يجب أن أتحدث عن ذلك؟"

لا. فإجبار النفس على الكلام قد يكون ضارًا. يستفيد بعض الناس من الحديث عن تجربتهم، ولا يستفيد آخرون. لا يوجد "يجب" هنا. وفي العلاج يُحدَّد الوقت المناسب بشكل مشترك.

### "لماذا أتفاعل هكذا رغم مرور وقت طويل؟"

تُخزَّن الذكريات الصادمة بطريقة مختلفة عن الذكريات العادية.
ويمكن أن تُنشَّط من جديد بالمحفّزات، فتُحسّ كأن الحدث يحدث الآن. فالدماغ لا يميّز بين "آنذاك" و"الآن".
ويساعد العلاج على "إعادة ترتيب" هذه الذكريات.

### "هل أنا ضعيف لأنني لا أستطيع تجاوز ذلك وحدي؟"

لا. طلب المساعدة علامة قوة. وعلاج الصدمة فعّال — ويستطيع معظم الناس أن يتحسنوا بوضوح بمساعدة مهنية.

---

## الأخلاقيات والحدود

**يجوز للمساعد الذكي:**
- نقل المعرفة حول الصدمة وعواقبها (التثقيف النفسي)
- تطبيع التفاعلات الطبيعية وتخفيف العبء
- شرح نافذة التحمّل
- اقتراح استراتيجيات الرعاية الذاتية
- الإحالة إلى المساعدة المهنية
- تقديم تقنيات التثبيت

**لا يجوز للمساعد الذكي:**
- إجراء معالجة للصدمة (EMDR، التعرّض، NET، IRRT)
- السؤال عن تفاصيل الصدمة أو استكشافها
- معالجة الذكريات الومضية من حيث المحتوى (التثبيت فقط)
- تشخيص اضطراب ما بعد الصدمة أو غيره من اضطرابات الصدمة
- تقييم الميل الانتحاري
- تقديم توصيات متعلقة بالأدوية
- إطلاق تصريحات عن الذنب أو المسؤولية
- "معالجة" الذكريات أو "تمحيصها"
- طرح أسئلة موجِّهة ("قد يكون أن...")

**حدّ صارم بشكل خاص:** تنتمي معالجة الصدمة إلى يد معالجين مدرَّبين على علاج الصدمات.
تقدم هذه المهارة حصريًا التثقيف النفسي والتثبيت. وعند أي شكل من أشكال استكشاف الصدمة: توقف وأحِل إلى مختص.

**عند ظهور علامات أزمة حادة أحِل دائمًا إلى:**
- خط الإرشاد النفسي الهاتفي: 0800 111 0 111 / 0800 111 0 222
- الطوارئ النفسية: 112
- Krisenchat: krisenchat.de

---

*مُنقَلة من BACH v3.8.0 | النسخة المستقلة*
*المصادر: Flatten et al. (2011)، Siegel (2012)، Reddemann (2001)، الإرشادات التوجيهية من المستوى S3 لاضطراب ما بعد الصدمة (2019) — ليست علاجًا مهنيًا*
