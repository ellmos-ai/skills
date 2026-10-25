---
name: exposure-guidance
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "ग्रेडेड एक्सपोज़र (क्रमिक संपर्क) चिंता विकारों में: चिंता पदानुक्रम, SUDs स्केल, एक्सपोज़र नियोजन और साथ देना। केवल मनोशिक्षा, कोई क्रियान्वयन नहीं।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [exposition, angst, phobie, suds, graduiert, verhaltenstherapie]
language: hi
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

# एक्सपोज़र सहायता

> चिंता पदानुक्रम, SUDs स्केल, ग्रेडेड एक्सपोज़र और हैबिचुएशन को समझना: नियोजन और सहायता — वास्तविक एक्सपोज़र केवल थेरेपिस्ट के साथ

देखें: [ETHICS.md](../ETHICS.md)

---

## संदर्भ

एक्सपोज़र (कॉन्फ्रंटेशन थेरेपी) चिंता विकारों, फोबिया, ओसीडी और PTSD में व्यवहार चिकित्सा की सबसे प्रभावी विधियों में से एक है।
यह हैबिचुएशन और एक्सटिंक्शन के सिद्धांतों पर आधारित है: जब कोई व्यक्ति चिंता उत्पन्न करने वाली स्थिति के बार-बार संपर्क में आता है, तो समय के साथ चिंता की प्रतिक्रिया घटती है।

साक्ष्य: विशिष्ट फोबिया, सामाजिक चिंता, पैनिक डिसऑर्डर और एगोराफोबिया के लिए एक्सपोज़र थेरेपी स्वर्ण-मानक उपचार है (NICE Guidelines, Bandelow et al. 2014, S3-Leitlinie Angststörungen)। इसके प्रभाव-आकार मनोचिकित्सा अनुसंधान में सबसे उच्च में से हैं।

**महत्वपूर्ण:** यह स्किल एक्सपोज़र अभ्यासों की योजना बनाने में सहायता करता है और क्रियाविधि की समझ देता है। एक्सपोज़र का क्रियान्वयन किसी योग्य थेरेपिस्ट के मार्गदर्शन में ही होना चाहिए।
**कभी लागू न करें:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. क्रियाविधि को समझना

### हैबिचुएशन

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

### एक्सटिंक्शन (नया सीखना)

```
EXTINKTION: Neue Erfahrungen überschreiben alte Angst-Assoziationen

Alte Erfahrung: Hund -> Gefahr -> Angst -> Flucht
Neue Erfahrung: Hund -> Keine Gefahr -> Angst sinkt -> Ich bin sicher

Die alte Assoziation wird nicht gelöscht, sondern durch neue
Erfahrungen überlagert. Deshalb kann die Angst in bestimmten
Kontexten zurückkehren (Renewal, Reinstatement) — was NORMAL ist.
```

### बचाव क्यों समस्या को बनाए रखता है

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

## 2. SUDs स्केल

### Subjective Units of Distress (0-100)

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

### SUDs स्केल का उपयोग

**एक्सपोज़र से पहले:**
- नियोजित स्थिति में अनुमानित चिंता (अपेक्षित मान)

**एक्सपोज़र के दौरान:**
- हर 5 मिनट पर वर्तमान SUDs मान का आकलन करें
- दर्ज करें कि स्थिति कैसे बदल रही है (बढ़ रही है, घट रही है, उतार-चढ़ाव कर रही है)

**एक्सपोज़र के बाद:**
- उच्चतम SUDs मान? अंतिम मान? चिंता कितनी जल्दी कम हुई?
- क्या यह उतना ही कठिन था जितना अपेक्षित था?

---

## 3. चिंता पदानुक्रम बनाना

### सिद्धांत

चिंता पदानुक्रम चिंता उत्पन्न करने वाली स्थितियों को निम्नतम से उच्चतम चिंता स्तर तक क्रमबद्ध करता है।
एक्सपोज़र हल्की स्थितियों से शुरू होकर धीरे-धीरे बढ़ता है।

### प्रक्रिया

```
ANGST-HIERARCHIE ERSTELLEN

Schritt 1: Alle angstauslösenden Situationen sammeln
Schritt 2: Jede Situation mit SUDs-Wert (0-100) bewerten
Schritt 3: Von niedrig nach hoch ordnen
Schritt 4: Lücken füllen (möglichst 10er-Schritte)
```

### उदाहरण: कुत्तों का डर

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

### उदाहरण: सामाजिक चिंता

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

### भरने योग्य टेम्पलेट

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

## 4. एक्सपोज़र के प्रकार

### ग्रेडेड एक्सपोज़र (In Vivo)

**सिद्धांत:** वास्तविक स्थितियों से क्रमिक सामना, कम SUDs मानों से शुरू करते हुए।

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

### फ्लडिंग (उद्दीपक अतिप्रवाह)

**सिद्धांत:** लंबे समय तक अत्यधिक चिंता उत्पन्न करने वाली स्थितियों (उच्च SUDs मान) का सीधा सामना।

```
FLOODING:

- Sehr wirksam, aber belastender als graduierte Exposition
- Nur unter therapeutischer Anleitung
- Voraussetzung: Gute therapeutische Beziehung und Vorbereitung
- Nicht bei unkontrollierbaren Panikattacken oder Dissoziation
- NICHT durch einen KI-Assistenten anleiten — nur erklären
```

### इन सेंसू एक्सपोज़र (कल्पना में)

**सिद्धांत:** कल्पना में चिंता उत्पन्न करने वाली स्थितियों का अनुभव करना।

```
EXPOSITION IN SENSU:

- Hilfreich als Vorbereitung auf reale Exposition
- Bei Situationen, die nicht leicht reproduzierbar sind
- Bei starker Vermeidung als Einstieg
- Ein KI-Assistent kann bei der Planung helfen, aber die Durchführung
  sollte therapeutisch begleitet sein
```

### इंटेरोसेप्टिव एक्सपोज़र

**सिद्धांत:** शारीरिक चिंता लक्षणों को जानबूझकर उत्पन्न करना
(जैसे गतिविधि से दिल की धड़कन तेज़ होना, घूमने से चक्कर आना)।

```
INTEROZEPTIVE EXPOSITION (bei Panikattacken):

- Durch Körperübungen: Hyperventilation, Strohhalm-Atmen,
  Kopfdrehen, Treppensteigen
- Ziel: Lernen, dass körperliche Symptome ungefährlich sind
- NUR unter therapeutischer Anleitung
```

---

## 5. सहायता-युक्त एक्सपोज़र नियोजन

### तैयारी प्रोटोकॉल

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

### एक्सपोज़र के बाद की समीक्षा प्रोटोकॉल

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

## 6. सुरक्षा निर्देश और रोकने के मानदंड

### एक्सपोज़र की पूर्व-शर्तें

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

### रोकने के मानदंड

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

### सुरक्षा व्यवहारों की पहचान

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

## नैतिकता और सीमाएँ

**एक AI सहायक यह कर सकता है:**
- एक्सपोज़र के सिद्धांत समझाना (मनोशिक्षा)
- चिंता पदानुक्रम साथ मिलकर बनाना
- SUDs स्केल समझाना और उपयोग करना
- एक्सपोज़र नियोजन में सहायता करना (प्रोटोकॉल भरना)
- एक्सपोज़र के बाद की समीक्षा दर्ज करना
- सुरक्षा संबंधी निर्देश देना
- प्रेरित करना और सामान्य बनाना ("एक्सपोज़र के दौरान चिंता वांछनीय और सामान्य है")

**एक AI सहायक यह नहीं कर सकता:**
- एक्सपोज़र स्वतंत्र रूप से करना या उसका मार्गदर्शन करना
- फ्लडिंग का मार्गदर्शन करना (केवल थेरेपिस्ट)
- इंटेरोसेप्टिव एक्सपोज़र का मार्गदर्शन करना (केवल थेरेपिस्ट)
- PTSD में Prolonged Exposure करना
- गंभीर डिसोसिएशन में एक्सपोज़र की सहायता करना
- एक्सपोज़र के लिए दबाव डालना ("तुम्हें इसका सामना करना ही होगा")
- परिणामों की गारंटी देना
- निदान करना या चिकित्सा योजना बनाना
- दवाओं से संबंधित सिफारिशें देना

**विशेष रूप से सख्त सीमा:** AI सहायक योजना बनाता और समझाता है। वास्तविक एक्सपोज़र किसी योग्य थेरेपिस्ट के मार्गदर्शन में होता है। क्रियान्वयन से जुड़े हर अनुरोध पर: विशेषज्ञ से संपर्क करने का सुझाव दें। पेशेवर सहायता के बिना एक्सपोज़र री-ट्रॉमेटाइज़ कर सकता है या चिंता बढ़ा सकता है।

**तीव्र संकट के संकेत होने पर हमेशा इनसे संपर्क करने का सुझाव दें:**
- टेलीफ़ोन सीलसॉर्गे: 0800 111 0 111 / 0800 111 0 222
- मनोचिकित्सीय आपातकालीन सेवा: 112
- Krisenchat: krisenchat.de

---

*BACH v3.8.0 से पोर्ट किया गया | स्टैंडअलोन संस्करण*
*स्रोत: Foa & Kozak (1986), Craske et al. (2014), Bandelow et al. (2014), S3-Leitlinie Angststörungen (2014) — कोई पेशेवर थेरेपी नहीं*
