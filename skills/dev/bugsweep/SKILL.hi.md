---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: "कोडबेस-आधारित लक्ष्य मान, दोगुना-वृद्धि (doubling escalation), क्षेत्र-ट्रैकिंग और अंतिम सत्यापन के साथ व्यवस्थित बग स्वीप। /bugsweep पर या जब भी उपयोगकर्ता व्यवस्थित बग जाँच या स्वीप करने को कहे, इसका उपयोग करें।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 72c943e5f956ae19c2e36d0478108228b95866bb77faaadf3dca77a686d9f972
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="bugsweep banner">

# /bugsweep — व्यवस्थित बग-स्वीप वर्कफ़्लो

अभिसारी (konvergierend) रोक-मानदंड के साथ पुनरावृत्त बग-खोज। कोडबेस के आकार के अनुसार स्केल होता है, सतही खोज का संदेह होने पर बढ़ता है, और क्षेत्र-ट्रैकिंग के माध्यम से दोहराव को रोकता है।

## 1. मूल दर की गणना

```
LOC = produktive Quellzeilen (src/, lib/ — ohne Tests, Configs, Docs, generated)
x = max(1, ceil(LOC / 1500))
Grundrate = x * 3
```

| LOC | x | Grundrate |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

उपयोगकर्ता को सूचित करें: "Codebasis: {LOC} LOC → Grundrate = {Grundrate} saubere Suchläufe."

## 2. खोज-लूप

```
zähler = 0
ziel = Grundrate
je_bug_gefunden = False
geprüft = []  # (bereich_name, typ: code|aufgabe)

LOOP:
  bereich = wähle_neuen_bereich()  # Siehe Bereichs-Regeln
  geprüft.append(bereich)
  
  Führe gründliche Bug-Suche durch
  
  IF Bug gefunden:
    je_bug_gefunden = True
    Fix nach bugfix-protocol (Phase 4+5)
    Review: siehe Modell-Regel (neuere Modellklassen: kein externer Review nötig)
    Commit + Push
    zähler = 0  # RESET
  ELSE:
    zähler += 1
    Melde: "✓ Sauber: {bereich} — {zähler}/{ziel}"
  
  IF zähler >= ziel:
    IF NOT je_bug_gefunden:
      # Verdoppelungs-Eskalation: kein einziger Bug → zu oberflächlich?
      ziel = Grundrate * 2
      je_bug_gefunden = True  # Eskalation nur EINMAL
      Melde: "⚠ Kein Bug in {Grundrate} Läufen → Ziel verdoppelt auf {ziel}."
      CONTINUE LOOP
    ELSE:
      GOTO Abschluss-Verifikation
```

### खोज-लूप के व्यावहारिक संकेत (स्वीप से सीखे गए)

- **गैर-Git रिपॉज़िटरी:** जहाँ `git` मौजूद नहीं है (जैसे क्लाउड-सिंक्रोनाइज़्ड प्रोजेक्ट फ़ोल्डर), वहाँ **संस्करणित बैकअप** "Commit + Push" की जगह लेता है: पहले फ़िक्स से पहले `datei_<ts>.bak` बनाएँ। **ध्यान दें — फ़िक्स-पूर्व बैकअप कार्य की सुरक्षा नहीं है:** अंतिम फ़िक्स के बाद एक ताज़ा `_FINAL_` बैकअप लें, अन्यथा सिंक में गड़बड़ी होने पर पूरा फ़िक्स-कार्य खो जाएगा।
- **कई पहले से ज्ञात बग:** यदि शुरुआत में ही N बग ज्ञात हों (जैसे पिछले लूप से), तो "प्रति बग: फ़िक्स → रिव्यू → Commit → Reset" अव्यावहारिक है। तब ज्ञात बगों को एक ही फ़िक्स-ब्लॉक में निपटाएँ (अंत में संयुक्त रिव्यू) और मूल दर/खोज-लूप को पहले नए खोजे गए बग से गिनें। Reset-तर्क स्वीप के दौरान नए मिले बगों पर लागू रहता है।
- **एक ही बग कई स्थानों पर:** एक मिली त्रुटि (जैसे गलत Regex, टूटी फ़ॉर्मैट-धारणा) अक्सर अन्य स्थानों पर नकल होकर मौजूद रहती है। हर फ़िक्स के बाद खोज से जाँचें कि वही पैटर्न कहीं और तो नहीं है — यह एक अलग और उपयोगी "क्षेत्र" है।

## 3. क्षेत्र-नियम (Anti-Gaming)

एक "क्षेत्र" या तो एक **Code-Fokus** है या एक **Aufgabe** (कोड का उद्देश्य)।

### Code-Fokus
- रनों के बीच **विस्तारित** (अधिक फ़ाइलें) या **स्थानांतरित** (दूसरा भाग) किया जा सकता है
- चयन पिछले रन के बिल्कुल समान नहीं होना चाहिए
- उदाहरण OK: रन 1 = `maintenance.py`, रन 5 = `maintenance.py + orchestrator.py` (विस्तारित)
- उदाहरण NICHT OK: रन 1 = `maintenance.py`, रन 5 = `maintenance.py` (समान)

### कार्य (उद्देश्य)
- **अधिक सूक्ष्म** (उप-फ़ंक्शन जाँचें) या **व्यापक** (संबंधित फ़ंक्शन) हो सकता है
- बिल्कुल वही कार्य नहीं होना चाहिए
- उदाहरण OK: रन 1 = "Thread-Safety im Watchdog", रन 5 = "Thread-Safety Tray gesamt" (व्यापक)
- उदाहरण OK: रन 1 = "Prozesserkennung", रन 5 = "Store-Marker-Matching in Prozesserkennung" (सूक्ष्म)
- उदाहरण NICHT OK: रन 1 = "Thread-Safety im Watchdog", रन 5 = "Thread-Safety im Watchdog" (समान)

### नामकरण
- क्षेत्र को खोज से पहले नामित करना अनिवार्य है (बाद में असाइन करना नहीं)
- प्रारूप: `"{Name}" ({typ}: code|aufgabe)`

## 4. अंतिम सत्यापन

जब zähler >= ziel और je_bug_gefunden:

**चरण A — bugfix-protocol Phase 5:**
- [ ] पूर्ण टेस्ट-सूट हरा (`pytest`)
- [ ] **बदले गए निष्पादन-पथ को कम से कम एक बार वास्तव में चलाएँ** — केवल टेस्ट नहीं। उस कोड पर हरे यूनिट-टेस्ट जो बदले गए स्थान को कभी नहीं बुलाते, केवल भ्रामक सुरक्षा हैं। वास्तव में बदला गया पथ चलाएँ (Dry-Run, Smoke-Lauf, CLI-Aufruf) और Tracebacks / Signatur- / Namensfehler जाँचें। `py_compile` या केवल Import केवल सिंटैक्स जाँचता है — यह नहीं कि पथ चलता है।
- [ ] **हर फ़िक्स को कम से कम एक टेस्ट छुए** — जो फ़िक्स उस बदली हुई शाखा को वास्तव में ट्रिगर करने वाले टेस्ट के बिना है, वह अजाँचा माना जाता है (ऑर्केस्ट्रेशन/नेटवर्क पथों के लिए Mock + Dry-Run संयोजित करें)।
- [ ] Type-Check (यदि कॉन्फ़िगर हो)
- [ ] Lint (यदि कॉन्फ़िगर हो)
- [ ] सत्र-फ़िक्स के Edge Cases जाँचे गए

**चरण B — समीक्षा (मॉडल-नियम):**
- **नए मॉडल-वर्ग (जैसे Claude 5 / Fable-Klasse):** बाहरी Advisor-/दूसरे-मॉडल-समीक्षा आवश्यक नहीं।
  चरण A (टेस्ट + वास्तविक Smoke-Lauf) ही सत्यापन है। वास्तविक अनिश्चितता में वैकल्पिक रूप से
  एक ताज़ा Review-Subagent — परंतु उसकी खोजों को बग मानने से पहले अनुभवजन्य रूप से जाँचें
  (अपरिवर्तित कोड के विरुद्ध टेस्ट)। 
  पृष्ठभूमि (स्वीप-अनुभव 2026-06-11): दूसरा समीक्षक उपलब्ध नहीं था, प्रतिस्थापन Subagent ने 1 खोज दी (विश्वास 85), जो टेस्ट से गैर-बग सिद्ध हुई — बाहरी समीक्षा ने परिणाम नहीं बदला।
- **पुराने मॉडल:** Advisor के साथ अंतिम चर्चा (फ़ॉलबैक: दूसरा मॉडल समीक्षक के रूप में); Advisor पुष्टि करता है या कमियाँ खोजता है।

**सत्यापन में बग मिलने पर:**
→ Fix + Test + Commit
→ RESET: zähler = 0, ziel = Grundrate (ताज़ा, दोगुना नहीं)
→ खोज-लूप पर वापस (geprüft-Liste रहती है, je_bug_gefunden = True)

**स्वच्छ सत्यापन पर:**
→ समाप्त। Commit + Push। प्रोटोकॉल आउटपुट करें।

## 5. प्रोटोकॉल (अंत में)

```markdown
## Bug-Sweep Ergebnis

- **Codebasis:** {LOC} LOC
- **Grundrate:** {Grundrate} (eskaliert: {ziel})
- **Geprüfte Bereiche:** {len(geprüft)}
- **Bugs gefunden:** {anzahl}
- **Resets:** {anzahl_resets}
- **Verdoppelung ausgelöst:** ja/nein
- **Fixes:**
  - {titel} — {commit_hash}
  - ...
- **Finale Test-Suite:** {passed}/{total} grün
- **Review-Verdict:** Selbstverifikation (neuere Modellklasse) / Advisor bestätigt / Lücken benannt
```

## यह वर्कफ़्लो कब उपयोग करें

- फ़ीचर-विकास के बाद (गुणवत्ता आश्वासन)
- रिलीज़ से पहले (स्वीकृति-स्वीप)
- आवधिक हाइजीन-जाँच के रूप में
- जब उपयोगकर्ता `/bugsweep` टाइप करे

## अन्य Skills के साथ अंतःक्रिया

- **bugfix-protocol:** हर मिले बग के लिए फ़िक्स-प्रक्रिया (Phase 4+5)
- **systematic-debugging:** स्वीप के भीतर कठिनाई से पुनरुत्पादित होने वाले बगों के लिए
- **code-review:** इसे कार्य-क्षेत्र के रूप में उपयोग किया जा सकता है

---

## Changelog

### 1.1.0 (2026-06-13)
- चरण B के लिए मॉडल-नियम वापस पोर्ट किया गया (स्थानीय Skill-इंस्टॉलेशन से, स्थिति 2026-06-11): नए मॉडल-वर्ग टेस्ट + वास्तविक Smoke-Lauf से स्वयं सत्यापित करते हैं, बाहरी समीक्षा आवश्यक नहीं; प्रोटोकॉल-फ़ील्ड "Review-Verdict" तदनुसार विस्तारित

### 1.0.0 (2026-06-13)
- Skill-लाइब्रेरी में पहला प्रकाशन (स्थानीय Skill-इंस्टॉलेशन से लिया गया, स्थिति 2026-06-01)
