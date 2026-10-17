---
name: exposure-guidance
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "التعرّض التدريجي في اضطرابات القلق: تسلسل القلق، ومقياس SUDs، وتخطيط التعرّض ومرافقته. للتثقيف النفسي فقط، دون تنفيذ."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [exposition, angst, phobie, suds, graduiert, verhaltenstherapie]
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
  origin_path: "system/skills/therapie/exposition_begleitung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: cc2d8527c2aeecc0056fd3a0f28b717f4bab39d67c82f6a2fd2f67c5336fc667
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.188621+00:00"
---
<img src="banner.png" width="100%" alt="exposure-guidance banner">

# مرافقة التعرّض

> فهم تسلسل القلق ومقياس SUDs والتعرّض التدريجي والتعوّد: التخطيط والمرافقة — والتعرّض الفعلي بمعالج فقط

انظر: [ETHICS.md](../ETHICS.md)

---

## السياق

التعرّض (العلاج بالمواجهة) من أكثر طرق العلاج السلوكي فعالية في اضطرابات القلق والرهاب واضطرابات الوسواس القهري واضطراب ما بعد الصدمة.
ويستند إلى مبدأي التعوّد والانطفاء: فعند التعرّض المتكرر لموقف مثير للقلق، تنخفض الاستجابة القلقية مع مرور الوقت.

الأدلة: يُعدّ العلاج بالتعرّض المعيار الذهبي للعلاج في الرهاب النوعي والقلق الاجتماعي واضطراب الهلع ورهاب الأماكن المفتوحة (إرشادات NICE، Bandelow وآخرون 2014، الإرشادات الألمانية S3 لاضطرابات القلق). وتُعد أحجام التأثير فيه من بين الأعلى في أبحاث العلاج النفسي.

**مهم:** تدعم هذه المهارة **تخطيط** تمارين التعرّض، وتنقل فهم مبادئ عملها. أما **تنفيذ** التعرّض فيجب أن يتم تحت إشراف معالج مؤهل.
**لا تُطبّق أبدًا:** EMDR، والتعرّض المطوّل (PE)، والعلاج بالتعرّض السردي (NET)

---

## 1. فهم مبادئ العمل

### التعوّد

```
HABITUATION: Gewöhnung durch wiederholte Konfrontation

Angstlevel
100 |  *
    | * *
 80 |*   *
    |     *
 60 |      *
    |       *
 40 |        *
    |         *  *
 20 |          **  * *
    |                  * * * * * *
  0 |________________________________
    Zeit (während der Exposition)

Die Angst steigt zunächst an, erreicht einen Höhepunkt
und sinkt dann OHNE Flucht oder Vermeidung von selbst ab.

Entscheidende Erfahrung: "Die Angst geht vorbei, auch wenn
ich in der Situation bleibe."
```

### الانطفاء (التعلّم الجديد)

```
EXTINKTION: Neue Erfahrungen überschreiben alte Angst-Assoziationen

Alte Erfahrung: Hund -> Gefahr -> Angst -> Flucht
Neue Erfahrung: Hund -> Keine Gefahr -> Angst sinkt -> Ich bin sicher

Die alte Assoziation wird nicht gelöscht, sondern durch neue
Erfahrungen überlagert. Deshalb kann die Angst in bestimmten
Kontexten zurückkehren (Renewal, Reinstatement) — was NORMAL ist.
```

### لماذا يُبقي التجنّبُ المشكلةَ قائمة

```
DER VERMEIDUNGSTEUFELSKREIS:

Angstauslösende Situation
        |
        v
Angst steigt (unangenehm)
        |
        v
Vermeidung/Flucht
        |
        v
Kurzfristige Erleichterung (Angst sinkt sofort)
        |
        v
Langfristige Verstärkung der Angst
("Die Situation IST gefährlich, gut dass ich geflohen bin")
        |
        v
Nächstes Mal: Noch mehr Angst, noch mehr Vermeidung
```

---

## 2. مقياس SUDs

### الوحدات الذاتية للضيق (0-100)

```
SUDS-SKALA (Subjektive Belastungsskala)

  0  Völlig entspannt, keine Angst
 10  Minimale Anspannung, kaum spürbar
 20  Leichte Unruhe, gut auszuhalten
 30  Deutlich unangenehm, aber kontrollierbar
 40  Merkliche Angst, noch handlungsfähig
 50  Mittlere Angst, anstrengend aber machbar
 60  Starke Angst, Vermeidungsimpuls deutlich
 70  Sehr starke Angst, schwer auszuhalten
 80  Intensive Angst, am Rand der Belastbarkeit
 90  Extreme Angst, Panikgefühl
100  Maximale Angst, schlimmste vorstellbare Belastung
```

### تطبيق مقياس SUDs

**قبل التعرّض:**
- تقدير القلق المتوقع في الموقف المخطَّط له (القيمة المتوقعة)

**أثناء التعرّض:**
- تقدير قيمة SUDs الحالية كل 5 دقائق
- توثيق مسار القلق (يرتفع، أو ينخفض، أو يتذبذب)

**بعد التعرّض:**
- ما أعلى قيمة لـ SUDs؟ وما القيمة النهائية؟ وما مدى سرعة تراجع القلق؟
- هل كان الأمر بالسوء الذي كان متوقعًا؟

---

## 3. إعداد تسلسل القلق

### المبدأ

يرتّب تسلسلُ القلق المواقفَ المثيرة للقلق من أدنى مستوى قلق إلى أعلاه.
يبدأ التعرّض بمواقف خفيفة ويتصاعد تدريجيًا.

### الإجراء

```
ANGST-HIERARCHIE ERSTELLEN

Schritt 1: Alle angstauslösenden Situationen sammeln
Schritt 2: Jede Situation mit SUDs-Wert (0-100) bewerten
Schritt 3: Von niedrig nach hoch ordnen
Schritt 4: Lücken füllen (möglichst 10er-Schritte)
```

### مثال: القلق من الكلاب

```
ANGST-HIERARCHIE: Hundephobie

SUDs | Situation
-----|--------------------------------------------------
 10  | Bild von einem Hund anschauen
 15  | Video von spielenden Hunden anschauen
 25  | Über eigene Erfahrungen mit Hunden sprechen
 30  | Einen kleinen Hund aus 10 Metern Entfernung beobachten
 40  | Einen kleinen Hund aus 5 Metern Entfernung beobachten
 50  | Neben einem angeleinten kleinen Hund stehen (2 Meter)
 55  | Einen kleinen angeleigten Hund berühren (Besitzer hält)
 60  | Einen mittelgroßen Hund aus 5 Metern beobachten
 65  | Neben einem angeleinten mittelgroßen Hund sitzen
 70  | Einen mittelgroßen Hund streicheln
 75  | An einem freilaufenden Hund vorbeigehen (Park)
 80  | Allein in einem Raum mit einem ruhigen Hund sein
 85  | Einen großen Hund streicheln
 90  | In einem Park mit mehreren freilaufenden Hunden sein
 95  | Einen Hund füttern
100  | Einen fremden Hund auf sich zulaufen lassen
```

### مثال: القلق الاجتماعي

```
ANGST-HIERARCHIE: Soziale Angst

SUDs | Situation
-----|--------------------------------------------------
 15  | Einen Fremden nach der Uhrzeit fragen
 20  | Im Supermarkt an der Kasse ein kurzes Gespräch führen
 30  | In einer kleinen Gruppe eine Frage stellen
 40  | Einen Bekannten anrufen
 45  | Blickkontakt halten während eines Gesprächs
 55  | Allein in ein Cafe gehen und dort essen
 60  | Einer Gruppe von 5 Personen etwas erzählen
 70  | Bei einer Feier auf einen Fremden zugehen
 75  | Im Restaurant Essen zurückschicken
 80  | Vor 10 Personen eine kurze Präsentation halten
 85  | In einer Diskussion eine abweichende Meinung vertreten
 90  | Vor 30 Personen einen Vortrag halten
 95  | Spontan eine Rede halten (Toast, Tischrede)
```

### نموذج للتعبئة

```
MEINE ANGST-HIERARCHIE

Angstthema: [...]

SUDs | Situation
-----|--------------------------------------------------
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
```

---

## 4. أنواع التعرّض

### التعرّض التدريجي (في الواقع)

**المبدأ:** المواجهة التدريجية للمواقف الواقعية، بدءًا من قيم SUDs المنخفضة.

```
ABLAUF GRADUIERTER EXPOSITION:

1. Angst-Hierarchie erstellen (siehe oben)
2. Mit der leichtesten Situation beginnen (SUDs 20-30)
3. In der Situation BLEIBEN, bis die Angst nachlässt
   (mindestens 50% Reduktion oder SUDs < 25)
4. Übung mehrfach wiederholen, bis die Situation
   routinemäßig bewältigbar ist
5. Nächste Stufe der Hierarchie angehen
6. Weiter bis zur Spitze
```

### الإغراق (الإغمار بالمثير)

**المبدأ:** المواجهة المباشرة للمواقف شديدة الإثارة للقلق (قيم SUDs مرتفعة) لفترة أطول.

```
FLOODING:

- Sehr wirksam, aber belastender als graduierte Exposition
- Nur unter therapeutischer Anleitung
- Voraussetzung: Gute therapeutische Beziehung und Vorbereitung
- Nicht bei unkontrollierbaren Panikattacken oder Dissoziation
- NICHT durch einen KI-Assistenten anleiten — nur erklären
```

### التعرّض في المخيلة (في التصوّر)

**المبدأ:** عيش المواقف المثيرة للقلق في التصوّر.

```
EXPOSITION IN SENSU:

- Hilfreich als Vorbereitung auf reale Exposition
- Bei Situationen, die nicht leicht reproduzierbar sind
- Bei starker Vermeidung als Einstieg
- Ein KI-Assistent kann bei der Planung helfen, aber die Durchführung
  sollte therapeutisch begleitet sein
```

### التعرّض الاستبطاني (الحشوي)

**المبدأ:** استحضار أعراض القلق الجسدية عمدًا (مثلًا خفقان القلب بالحركة، أو الدوار بالدوران).

```
INTEROZEPTIVE EXPOSITION (bei Panikattacken):

- Durch Körperübungen: Hyperventilation, Strohhalm-Atmen,
  Kopfdrehen, Treppensteigen
- Ziel: Lernen, dass körperliche Symptome ungefährlich sind
- NUR unter therapeutischer Anleitung
```

---

## 5. تخطيط التعرّض المصحوب

### بروتوكول الإعداد

```
EXPOSITIONS-PLANUNGSPROTOKOLL

Datum: [...]
Therapeut informiert: [ ] Ja  [ ] Nein (PFLICHT!)

Angstthema: [...]
Gewährte Situation: [...]
Erwarteter SUDs-Wert: [...]
Stufe in der Hierarchie: [...]

Was genau werde ich tun: [...]
Wo: [...]
Wann: [...]
Wie lange: [...]
Allein oder begleitet: [...]

Meine größte Befürchtung: [...]
Was realistisch passieren wird: [...]

Notfallplan (falls SUDs > 90 oder Dissoziation):
1. Grounding (5-4-3-2-1)
2. Atemübung (Box-Breathing)
3. [Vertrauensperson anrufen]: Tel. [...]
4. Situation ordentlich verlassen (kein panisches Flüchten)
```

### بروتوكول ما بعد التعرّض

```
EXPOSITIONS-NACHBEREITUNG

Datum: [...]
Situation: [...]

SUDs vorher (Erwartung): [...]
SUDs höchster Wert während: [...]
SUDs am Ende: [...]

Wie lange in der Situation geblieben: [...]
Habituation eingetreten: [ ] Ja  [ ] Teilweise  [ ] Nein

Was habe ich gelernt: [...]
War es so schlimm wie befürchtet: [ ] Schlimmer  [ ] Wie erwartet  [ ] Weniger schlimm

Was möchte ich beim nächsten Mal anders machen: [...]
Nächste Stufe: [...]
```

---

## 6. تحذيرات السلامة ومعايير الإيقاف

### متطلبات التعرّض

```
CHECKLISTE VOR EXPOSITIONSBEGINN:

[ ] Qualifizierter Therapeut ist einbezogen
[ ] Ausreichende Stabilisierung vorhanden
[ ] Angst-Hierarchie ist erstellt und besprochen
[ ] Notfallplan ist vorbereitet
[ ] Person versteht das Wirkprinzip (Habituation)
[ ] Keine akute Suizidalität
[ ] Keine unkontrollierte psychotische Symptomatik
[ ] Keine schwere dissoziative Störung (ohne therapeutische Begleitung)
[ ] Keine akute Substanzintoxikation
[ ] Person hat freiwillig zugestimmt (keine Zwangsexposition!)
```

### معايير الإيقاف

```
EXPOSITION ABBRECHEN, WENN:

- Dissoziation auftritt (Person "ist weg", reagiert nicht)
- Panikattacke mit Kontrollverlust
- Person will ausdrücklich abbrechen (Autonomie respektieren!)
- Körperliche Symptome: Brustschmerz, Atemnot, Ohnmacht
- Suizidgedanken während der Exposition
- Die Situation objektiv unsicher wird

BEI ABBRUCH:
1. Grounding und Stabilisierung (5-4-3-2-1, Atemübung)
2. Sicherstellen, dass die Person orientiert und stabil ist
3. Erfahrung besprechen (was ist passiert, was wurde gelernt)
4. Keinen Vorwurf machen ("Du hättest bleiben sollen")
5. Nächsten Schritt mit Therapeut planen
```

### التعرّف على سلوكيات الأمان

```
SICHERHEITSVERHALTEN (Safety Behaviors):

Sicherheitsverhalten sind Strategien, die die Angst kurzfristig senken,
aber das Lernen verhindern:

| Sicherheitsverhalten | Problem |
|---------------------|---------|
| Ablenkung während Exposition | Verhindert volle Konfrontation |
| Handy griffbereit halten | "Ich habe es nur geschafft, weil..." |
| Begleitperson dabei | Lernt nicht, es allein zu schaffen |
| Beruhigungstablette vorher | Erfolg wird Tablette zugeschrieben |
| Nur kurz in Situation bleiben | Habituation hat keine Zeit |
| Fluchtweg im Kopf planen | Aufmerksamkeit nicht bei Erfahrung |

Ziel: Sicherheitsverhalten schrittweise reduzieren,
damit die volle Lernerfahrung möglich wird.
Aber: Nicht zu früh wegnehmen — in Absprache mit Therapeut.
```

---

## الأخلاقيات والحدود

**يحق لمساعد الذكاء الاصطناعي:**
- شرح مبادئ التعرّض (التثقيف النفسي)
- إعداد تسلسل القلق معًا
- شرح مقياس SUDs واستخدامه
- دعم تخطيط التعرّض (تعبئة البروتوكولات)
- توثيق ما بعد التعرّض
- تقديم تحذيرات السلامة
- التحفيز والتطبيع ("القلق أثناء التعرّض متوقع وطبيعي")

**لا يحق لمساعد الذكاء الاصطناعي:**
- تنفيذ التعرّض أو توجيهه بشكل مستقل
- توجيه الإغراق (للمعالج فقط)
- توجيه التعرّض الداخلي (للمعالج فقط)
- إجراء التعرّض المطوّل لاضطراب ما بعد الصدمة
- مرافقة التعرّض مع تفكك شديد
- الضغط للدخول في التعرّض ("يجب أن تواجه هذا")
- ضمان النتائج
- تشخيص الحالات أو وضع خطة علاجية
- تقديم توصيات تتعلق بالأدوية

**حدّ صارم بشكل خاص:** يخطط مساعد الذكاء الاصطناعي ويشرح فقط. أما التعرّض الفعلي فيتم تحت إشراف معالج مؤهل. وعند أي طلب يتعلق بالتنفيذ: يُحال المستخدم إلى مختص. فالتعرّض دون مرافقة مهنية قد يؤدي إلى إعادة الصدمة أو تفاقم القلق.

**عند ظهور علامات أزمة حادة أحِل دائمًا إلى:**
- Telefonseelsorge (الخط الألماني لمساندة النفس): 0800 111 0 111 / 0800 111 0 222
- خدمة الطوارئ الطبية النفسية: 112
- Krisenchat: krisenchat.de

---

*منقول عن BACH v3.8.0 | النسخة المستقلة*
*المصادر: Foa & Kozak (1986)، Craske وآخرون (2014)، Bandelow وآخرون (2014)، الإرشادات الألمانية S3 لاضطرابات القلق (2014) — ليس علاجًا نفسيًا مهنيًا*
