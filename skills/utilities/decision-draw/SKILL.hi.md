---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "एक साथ जुड़े हुए खुले निर्णयों को सभी अनुशंसित विकल्पों के आधार पर एक ही सुसंगत, गद्य-आधारित समग्र अवधारणा में संघनित करता है। यह दिखाता है कि कार्यान्वयन के बाद उप-प्रणालियाँ ठोस रूप से एक-दूसरे में कैसे जुड़ती हैं, ताकि उपयोगकर्ता को दर्जनों अलग-अलग प्रश्नों से गुज़रने के लिए बाध्य न होना पड़े। उपयोगकर्ता चित्र को समग्र रूप में स्वीकृत करता है या लक्षित सुधार देता है, जिन्हें अपने-आप अलग-अलग निर्णयों में बदला जाता है और decision-briefing के चरण 4 के माध्यम से रजिस्टर में वापस लिखा जाता है। इस स्किल का उपयोग तब करें जब कहा जाए \"अगर हम सबसे सहमत हों तो पूरा चित्र कैसा दिखेगा\", \"मुझे समग्र चित्र बनाकर दिखाओ\", \"निर्णयों की समग्र अवधारणा\", \"decision draw\", /decision-draw, \"सिस्टम आपस में कैसे जुड़ते हैं\"। इसका उपयोग तब न करें जब प्रत्येक बिंदु के विकल्पों पर अलग-अलग चर्चा करनी हो -- यह decision-briefing करता है; निर्भरता ग्राफ़ के लिए न करें -- यह decision-path करता है; विकल्पों और पक्ष/विपक्ष वाले संरचित अलग-अलग ब्लॉकों के लिए न करें (निकटता से जुड़े समूहों के लिए भी नहीं) -- यह decision-shot करता है; किसी एक निर्णय की व्युत्पत्ति के लिए न करें -- यह decide करता है।"
visibility: public
language: hi
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
translator: "claude-sonnet-5-5"
translated_at: "2026-10-17T18:02:34.569514+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — समग्र चित्र और एक साथ जुड़े निर्णयों की स्वीकृति

> जब पाँच या दस निर्णय लंबित होते हैं, तो विकल्पों की छोटी-छोटी बारीकियों में उभरती हुई प्रणाली की दृष्टि आसानी से खो जाती है। decision-draw विकल्पों का वर्णन नहीं करता, बल्कि काम करते हुए पूरे तंत्र का वर्णन करता है: जब सभी अनुशंसाएँ स्वीकार कर ली जाएँ, तो सिस्टम एक-दूसरे के साथ कैसे काम करते हैं? उपयोगकर्ता चित्र को समग्र रूप में स्वीकृत करता है या लक्षित सुधार करता है।

---

## कब उपयोग करें

- कई परस्पर जुड़े निर्णयों ([decision-briefing](../decision-briefing/SKILL.md) या किसी निर्णय-प्रस्ताव से) को एक थकाऊ, अलग-अलग प्रश्नों की सूची के रूप में निपटाना न हो।
- उपयोगकर्ता निर्णय से पहले देखना चाहता है कि कार्यान्वयन के बाद रोज़मर्रा में घटक वास्तव में कैसे मिलकर काम करते हैं।
- निर्भरता ग्राफ़ ([decision-path](../decision-path/SKILL.md)) से निकटता से जुड़े निर्णयों का एक समूह पहचाना गया है, जिसे एक कार्यात्मक इकाई के रूप में स्वीकृत किया जा सकता है।
- ट्रिगर शब्द: `/decision-draw`, "अगर हम सबसे सहमत हों तो पूरा चित्र कैसा दिखेगा", "मुझे समग्र चित्र बनाकर दिखाओ", "निर्णयों की समग्र अवधारणा", "decision draw", "उसके बाद सिस्टम आपस में कैसे जुड़ते हैं", "समग्र स्वीकृति के लिए चित्र"।
- **न** उपयोग करें:
  - जब उपयोगकर्ता प्रत्येक प्रश्न के अलग-अलग विकल्पों को तौलकर अक्षर (A/B/C) से चुनना चाहता हो — यह [decision-briefing](../decision-briefing/SKILL.md) करता है।
  - टर्मिनल में केवल कारण-संबंध और अवरोधों के विश्लेषण के लिए — यह [decision-path](../decision-path/SKILL.md) करता है।
  - अलग-अलग प्रश्नों या निकटता से जुड़े समूहों के लिए 5-भाग वाले अलग ब्लॉकों (संदर्भ, प्रत्येक विकल्प के पक्ष/विपक्ष, अनुशंसा) में विकल्पों के पृथक मूल्यांकन के लिए — यह [decision-shot](../decision-shot/SKILL.md) करता है।
  - किसी एक खुले मूलभूत प्रश्न के पद्धतिगत विकास के लिए — यह [decide](../decide/SKILL.md) करता है।

---

## निर्णय-परिवार में भेद

| स्किल | UX और फ़ोकस | विकल्पों के प्रति रुख | स्वीकृति का रूप |
|---|---|---|---|
| `decision-briefing` | अलग-अलग प्रश्नों में **विभाजित करता है** | सभी विकल्प A/B/C/D दिखाता है | अक्षर कोड (`1A 2C 3B`) |
| `decision-path` | कारण-संबंधों को **संरचित करता है** | ग्राफ़ में विकल्पों का मूल्यांकन करता है | टर्मिनल में निदान (ASCII) |
| `decision-draw` | **सुसंगत लक्ष्य-चित्र** (परस्पर जुड़े निर्णयों को एक साथ लाता है) | **केवल अनुशंसित विकल्प** का वर्णन करता है (विकल्पों के लिंक दिए जाते हैं) | समग्र स्वीकृति या सुधार वाक्य |
| `decision-shot` | **संरचित अलग ब्लॉक** (अलग प्रश्नों या निकट समूहों के लिए) | 2–4 पक्ष/विपक्ष बिंदुओं के साथ विकल्प दिखाता है | Executive Decision / अलग-अलग स्वीकृति |
| `decide` | एकल मामले को **विकसित करता है** | मूल्यांकन मैट्रिक्स (मानदंड) | विश्लेषणात्मक अनुशंसा |

> **केंद्रीय नियम:**
> `decision-draw` **केवल अनुशंसित विकल्प** का वर्णन करता है। अस्वीकृत विकल्प गायब नहीं हुए हैं — वे [decision-briefing](../decision-briefing/SKILL.md), [decision-shot](../decision-shot/SKILL.md) या लिंक किए गए टिकटों में प्रलेखित हैं और हेडर में लिंक किए जाते हैं। इस संदर्भ के बिना Draw उपयोगकर्ता का चुनाव आसान करने के बजाय उससे छीन लेता।

---

## अनिवार्य शैली-नियम: उपयोगकर्ता-पाठ में संक्षिप्त रूप और संख्याएँ नहीं

> **मानक उपयोगकर्ता-निर्देश (फ़ीडबैक 2026-09-13 / टिकट T-20260913-883789445):**
> *"decision draws मेरे लिए बहुत तकनीकी हैं, यह बिना संख्या के होना चाहिए; उन्हें तुम पृष्ठभूमि में जानते हो या पाठ तैयार करने के लिए इस्तेमाल करते हो [...]।"*

1. **उपयोगकर्ता को दिखने वाले पाठ में कोई तकनीकी संक्षिप्त रूप नहीं:**
   मनुष्य के लिए दिखने वाले सामान्य पाठ (बंडल, अवधारणा, परस्पर संयोजन, कार्यान्वयन, पूछताछ) में आंतरिक संक्षिप्त रूप (जैसे `BH-A`, `MD-A`, `HA-A`, `PRA`), टिकट नंबर (`T-2026...`), D-नंबर (`D-2026...`), सापेक्ष पथ, Git-हैश या मापे गए मान **नहीं** होते।
2. **प्रत्येक मद के लिए रोज़मर्रा की भाषा में 2–4 वाक्य, उत्तम पुरुष में:**
   बंडल की हर मद तीन चरणों के क्रम में लिखी जाती है:
   - *स्थिति:* वर्तमान प्रारंभिक स्थिति क्या है?
   - *"मैं करूँगा/करूँगी …":* मैं ठोस रूप से क्या योजना बना रहा/रही हूँ / मेरी कार्य-सिफ़ारिश क्या है?
   - *विकल्प-योजना:* यदि यह विफल हो जाए तो क्या होगा, या उसके बाद उपयोगकर्ता क्या तय करेगा?
   *(उदाहरण: "Hermes टास्क में केवल अंग्रेज़ी का समर्थन करता है। मैं इसे Hermes में इश्यू के रूप में दर्ज करूँगा/करूँगी और हम अपने लिए एक वैकल्पिक समाधान बनाएँगे। इस समय कुछ पुराने सत्र उपलब्ध हैं जो उपयोग करने योग्य नहीं हैं। मैं उन्हें फिर से उपयोग-योग्य बनाने की कोशिश करूँगा/करूँगी। अगर यह नहीं हो पाया, तो मैं तुम्हें 10 सत्रों में से एक यादृच्छिक नमूना दूँगा/दूँगी और उनका सारांश बताऊँगा/बताऊँगी — ताकि तुम तय कर सको कि उन्हें बचाना सार्थक है या नहीं।")*
3. **दिशा-निर्देश के लिए सरल शीर्षक:**
   हर मद का एक समझने योग्य जर्मन शीर्षक होता है (जैसे *"अपने आप में मूल केंद्र के रूप में मॉडल-बैकएंड"*, *"Mac पर सुरक्षित Deploy-कुंजियाँ"*)। उपयोगकर्ता इसी शीर्षक के माध्यम से संवाद करता है या समग्र स्वीकृति देता है।
4. **तकनीकी मिलान केवल परिशिष्ट में:**
   सरल शीर्षक, आंतरिक संक्षिप्त रूप, टिकट-ID और रजिस्टर-स्थिति के बीच का अनुवाद **केवल** दस्तावेज़ के अंत में दी गई एक अंतिम परिशिष्ट-तालिका में होता है। वहीं — और केवल वहीं — स्वचालित पार्सर और रजिस्टर में वापस लिखने वाले घटक काम करते हैं।

---

## अनिवार्य संरचना (आठ भाग)

एक पूर्ण `decision-draw` बिना किसी अपवाद के इसी संरचना का पालन करता है:

### 1. बंडल और दायरा (सरल भाषा में)
बंडल की गई मदों का रोज़मर्रा की भाषा में अवलोकन (उत्तम पुरुष, प्रत्येक बिंदु के लिए 2–4 वाक्य, पाठ में कोई ID/संक्षिप्त रूप नहीं)।

### 2. अवधारणा
लक्षित अंतिम स्थिति, गद्य में एक सुसंगत प्रवाहपूर्ण पाठ के रूप में:
- यदि सभी सिफ़ारिशें ठीक इसी तरह लागू की जाएँ, तो कैसा सिस्टम-परिदृश्य या कार्यप्रवाह बनता है?
- विकल्पों की आमने-सामने तुलना नहीं, संभावनार्थ रूप में अगल-बगल की बातें ("यह भी किया जा सकता है") नहीं।
- स्पष्ट, सटीक निश्चयार्थ रूप: लक्षित अंतिम स्थिति में सिस्टम इस तरह काम करता है।

### 3. परस्पर संयोजन
Skill का कार्यात्मक केंद्र:
- तय किए गए हिस्से कार्यान्वयन के **बाद** वास्तव में एक-दूसरे में कैसे जुड़ते हैं?
- प्रस्तुति केवल घटकों की सूची के बजाय, अधिमानतः किसी ठोस एंड-टू-एंड प्रवाह के साथ।
- डेटा-प्रवाह, इंटरफ़ेस और ज़िम्मेदारियों को स्पष्ट और ठोस बनाता है।

### 4. कार्यान्वयन
साकार करने का ठोस क्रम:
- व्यवहार में वास्तव में क्या होता है?
- एज और निर्भरता का तर्क सीधे [decision-path](../decision-path/SKILL.md) से लिया जाता है।
- स्वतंत्र कार्य-धाराओं को ईमानदारी से समानांतर के रूप में दिखाया जाता है (कृत्रिम कारण-शृंखलाएँ न गढ़ें; एक बंडल में कई समानांतर धाराएँ हो सकती हैं)। क्रम केवल वहीं बताया जाता है जहाँ प्रमाणित निर्भरताएँ या समय-सीमाएँ मौजूद हों।
- Gate, माइग्रेशन-चरण और जाँचों का नाम बताता है।

### 5. यह चित्र क्या कवर नहीं करता
दिखावटी पूर्णता से सुरक्षा:
- कौन-से सीमांत प्रश्न, खुले बिंदु या 🔴-विश्वास-स्तर जानबूझकर बाहर रखे गए हैं?
- पड़ोसी सिस्टमों के साथ इंटरफ़ेस की सीमाएँ कहाँ हैं?
- जो चित्र अपनी सीमाओं के बारे में चुप रहता है, वह झूठी सुरक्षा की भावना पैदा करता है।

### 6. स्वीकृति
उपयोगकर्ता के साथ संवाद:
- उपयोगकर्ता चित्र को समग्र रूप में जाँचता है।
- उत्तर विकल्प 1: **स्पष्ट समग्र स्वीकृति** ("ठीक है", "स्वीकृत", "इसी तरह लागू करें")। केवल इसी स्थिति में बंडल की सभी मदें निर्णीत के रूप में दर्ज किए जाते हैं।
- उत्तर विकल्प 2: **सादे शीर्षक या रोज़मर्रा की भाषा में सुधार** ("Mac-Deploy में बेहतर होगा कि Auto-Restart न हो", "VersicherungsManager को फ़िलहाल टाल दें")। इससे यह अलग-अलग निर्णयों में विभाजित हो जाता है; सभी असंशोधित मदें खुली रहती हैं।

### 7. वापसी-स्थानांतरण
उपयोगकर्ता के सुधारों का अलग-अलग निर्णयों में व्यवस्थित अनुवाद:
- **कोई स्वचालित सह-प्रविष्टि नहीं:** केवल स्पष्ट समग्र स्वीकृति पर ही अपरिवर्तित मदें दर्ज की जाती हैं। आंशिक सुधार समग्र स्वीकृति **नहीं** है!
- **सुधारों के समय अलगाव:** सुधार आने पर उसे अलग-अलग निर्णयों में विभाजित किया जाता है; बंडल की बाकी सभी मदें (स्रोत-रजिस्टर / टेम्पलेट में) कड़ाई से **खुले** रहते हैं, जब तक उपयोगकर्ता संशोधित चित्र को समग्र रूप में स्वीकार न कर ले या शेष मदों की अलग-अलग पुष्टि न कर दे।
- **वापसी-स्थानांतरण की अनिवार्य तालिका:** हर सुधार-प्रतिक्रिया अनिवार्य रूप से चार स्तंभों वाली एक संरचित मूल्यांकन तालिका बनाती है (मूल सुधार, प्रभावित संक्षिप्त नाम, डोमिनो-स्थिति, खुली अस्पष्टताएँ)।
- **लेखन का एकमात्र मार्ग चरण 4 के माध्यम से:** `decision-draw` का रजिस्टर में लिखने का **कोई** अपना मार्ग नहीं है। प्रविष्टि **केवल** [decision-briefing](../decision-briefing/SKILL.md) के चरण 4 की मानकीकृत प्रक्रिया से होती है।

### 8. परिशिष्ट: तकनीकी संदर्भ तालिका (केवल प्रविष्टि और ऑडिट के लिए)
दस्तावेज़ के अंत में एक संक्षिप्त तालिका, जिसमें:
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## उदाहरण (पायलट अंश: Ticket-Master 2026-09-13 — BACH और सिस्टम-समूह)

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

## व्यवहार के नियम

1. **अवधारणा में संभावनार्थ रूप नहीं:** पूरे सिस्टम का वर्णन ऐसे करें जैसे वह पहले ही साकार हो चुका हो। उपयोगकर्ता परिणाम के बारे में स्पष्टता चाहता है, सैद्धांतिक संभावनाएँ नहीं।
2. **कालक्रम से पहले कार्य-कारण:** *कार्यान्वयन* अनुभाग का क्रम [decision-path](../decision-path/SKILL.md) के निर्भरता-ग्राफ़ के स्तरों का अनुसरण करता है। स्वतंत्र धाराओं को ईमानदारी से समानांतर दिखाया जाता है और उन्हें कृत्रिम कारण-शृंखला में नहीं मोड़ा जाता।
3. **वापसी-स्थानांतरण में स्पष्ट डोमिनो-जाँच:** उपयोगकर्ता के सुधार को कभी भी अलग से दर्ज नहीं करना चाहिए, बिना यह जाँचे कि ग्राफ़ में आश्रित नोड अमान्य तो नहीं हो रहे या प्रभावित तो नहीं हो रहे।
4. **आंशिक सुधारों पर स्वचालित सह-प्रविष्टि नहीं:** केवल स्पष्ट समग्र स्वीकृति पर ही अपरिवर्तित मदें दर्ज की जाती हैं। प्रत्येक आंशिक सुधार में सभी अप्रभावित मदें कड़ाई से खुली रहती हैं, जब तक समग्र चित्र दोबारा स्वीकृत न हो या मदों की अलग-अलग पुष्टि न हो जाए।
5. **लेखन का एकमात्र मार्ग चरण 4 के माध्यम से:** `decision-draw` का रजिस्टर में लिखने का कोई अपना मार्ग नहीं है। प्रविष्टियाँ बिना किसी अपवाद के [decision-briefing](../decision-briefing/SKILL.md) के चरण 4 से होती हैं।
6. **रजिस्टर-अनुबंधों का सम्मान करें:** प्रविष्टियाँ हमेशा निर्णय-रजिस्टर के नियमों के अनुसार होती हैं (IDs का पुनःक्रमांकन नहीं, अद्वितीय प्रविष्टि-कोड, मानक लक्ष्य `DECIDED-AND-DONE.md`)।
7. **तकनीकी संख्याओं और संक्षिप्त नामों के बिना उपयोगकर्ता-पाठ:** मनुष्य के लिए दिखने वाले प्रवाही पाठ में कोई IDs, संक्षिप्त नाम, पथ या टिकट-संख्याएँ नहीं होतीं। प्रत्येक मद समझने योग्य उत्तम पुरुष रूप में लिखा जाता है; सभी पहचानकर्ता परिशिष्ट-तालिका में चले जाते हैं।

---

## सेशन-प्रोवेनेंस

जब किसी Decision-Draw को स्थायी अवधारणा-दस्तावेज़ के रूप में सहेजा जाता है, तो वह इसके साथ समाप्त होता है:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- स्रोत की प्राथमिकता: पहले स्पष्ट रनटाइम/CLI-जानकारी, उसके बाद प्रामाणिक प्रोवाइडर-परिवेश या हुक, अन्यथा `unbekannt`।
- सबएजेंट अपने पैरेंट सेशन की सेशन-ID विरासत में लेते हैं।
- केवल चैट-टेम्पलेट्स पर कोई स्टैम्प नहीं लगाया जाता।

---

## चेंजलॉग

### 1.1.0 (2026-09-18)
- उपयोगकर्ता-अनुकूल निर्णय-पाठ के लिए शैली-नियम स्थापित किया गया (T-20260913-883789445, उपयोगकर्ता-निर्देश 2026-09-13):
  - उपयोगकर्ता को दिखने वाले पाठ में कोई तकनीकी संक्षिप्त रूप, टिकट-/D-नंबर, पथ या मापे गए मान नहीं।
  - प्रत्येक मद के लिए उत्तम पुरुष में 2–4 वाक्य रोज़मर्रा की भाषा में (स्थिति, „मैं करूँगा/करूँगी …“, विकल्प-योजना)।
  - पहचान और स्वीकृति के लिए स्पष्ट, सरल भाषा में शीर्षक।
  - तकनीकी मिलान (संक्षिप्त रूप, टिकट-ID, रजिस्टर-स्थिति) कठोरता से अंत की परिशिष्ट-तालिका (अनुभाग 8) में स्थानांतरित किया गया।

### 1.0.1 (2026-09-13)
- समीक्षा के बाद का संशोधन:
  - वापसी-स्थानांतरण अनुबंध को अधिक सटीक बनाया गया: आंशिक सुधारों में स्वचालित सह-प्रविष्टि नहीं; अप्रभावित मदें समग्र स्वीकृति तक कठोरता से खुली रहती हैं।
  - 4 स्तंभों वाली वापसी-स्थानांतरण की अनिवार्य तालिका (मूल सुधार, प्रभावित संक्षिप्त रूप, डोमिनो-स्थिति, खुली अस्पष्टताएँ) जोड़ी गई।
  - उदाहरण में एकाधिक मिलान दर्शाया गया (एक उपयोगकर्ता-सुधार `MD-A` और `CF-A` को एक साथ प्रभावित करता है)।
  - अनुबंध और उदाहरण में `decision-briefing` चरण 4 के माध्यम से ही लिखने का एकमात्र मार्ग स्थापित किया गया।
  - उदाहरण में कारण-श्रृंखला की गलत धारणा ठीक की गई: स्वतंत्र मदों को ईमानदारी से चार समानांतर कार्य-धाराओं के रूप में दिखाया गया (समाधान a)।
  - `decision-shot` से अंतर को आउटपुट-प्रारूप के आधार पर स्पष्ट किया गया (पक्ष/विपक्ष सहित संरचित अलग-अलग ब्लॉक बनाम समग्र स्वीकृति सहित सुसंगत लक्ष्य-चित्र)।

### 1.0.0 (2026-09-13)
- उपयोगकर्ता-आदेश T-20260913-107991667 के आधार पर पहला संस्करण।
- सात भागों वाली बाध्यकारी संरचना (बंडल, अवधारणा, पारस्परिक क्रिया, कार्यान्वयन, सीमाएँ, स्वीकृति, वापसी-स्थानांतरण)।
- `decision-path` पर आधारित बंडलिंग-तर्क और `decision-briefing` चरण 4 तक वापस लिखने का सेतु।
