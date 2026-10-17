---
name: software-testing
version: 1.0.1
type: knowledge-protocol
author: Lukas Geiger
created: 2026-08-22
updated: 2026-08-22
description: "सॉफ़्टवेयर प्रोजेक्ट के लिए टेस्ट-रणनीति सलाहकार — स्थिति और SDLC-/CI-चरण के अनुसार सही परीक्षण-स्तर (Unit/Integration/System/Abnahme), परीक्षण-प्रकार (funktional, nicht-funktional, änderungsbezogen) और परीक्षण-डिज़ाइन विधियाँ (Äquivalenzklassen, Grenzwerte, Entscheidungstabellen, explorativ) चुनता है, जिसमें Testpyramide, CI/CD-Gates, Shift-Left और Best Practices शामिल हैं। जब भी Tests लिखने, योजना बनाने, प्राथमिकता तय करने या मूल्यांकन करने हों — जैसे \"schreibe Tests\", \"Teststrategie\", \"Testplan\", \"Testkonzept\", \"was/wie soll ich testen\", \"welche Tests fehlen\", \"Testabdeckung verbessern\", \"QA aufsetzen\", \"QA सेटअप करो\", \"टेस्ट लिखो\", \"टेस्ट रणनीति\", \"टेस्ट प्लान\", Regression/Smoke/Sanity/Last/Stress/Security-Tests से जुड़े प्रश्न या Test-Pipeline सेट करते समय — यह Skill हमेशा उपयोग करें, भले ही \"Test\" केवल संयोग से आए। सीमांकन — TDD-लूप के लिए स्वयं superpowers:test-driven-development, Bug-Diagnose के लिए bugfix-protocol, और व्यवस्थित Bug-Suche के लिए bugsweep का उपयोग करें।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [testing, teststrategie, qa, unit-test, integration, regression, testpyramide, shift-left, ci-cd, istqb]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'claude-code-recherche', 'origin_version': '1.0.0', 'created_from': 'Online-Recherche 2026-08-22 (ISTQB-Systematik, Testpyramide, Agile Testing Quadrants, moderne Verfahren); Quellen siehe testarten-katalog.md'}
translated_from_sha256: 85a9672454c8df2d2e0dfd1a87d5468a7ebc030e45a1fa2843f361bba80c8b80
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T03:22:33.152218+00:00"
---
<img src="banner.png" width="100%" alt="software-testing banner">

# सॉफ़्टवेयर-टेस्टिंग: टेस्ट-रणनीति और टेस्ट-चयन

यह Skill इस प्रश्न का उत्तर देता है — **„मुझे यहाँ, अभी, किसके लिए कौन-से Tests चाहिए?"** —
अंदाज़े से नहीं, बल्कि व्यवस्थित रूप से। यह निर्णय-तर्क देता है; सभी परीक्षण-प्रकारों, विधियों और
परिभाषाओं की पूरी सूची उसी फ़ोल्डर में `testarten-katalog.md` में है (विस्तृत प्रश्नों के लिए वहीं देखें)।

---

## 1. क्रमबद्ध ढाँचा: तीन आयामों में सोचें

Tests की योजना बनाने या लिखने से पहले कार्य को तीन अक्षों (ISTQB) पर रखें।
जो केवल „Tests की एक सूची" रखता है, वह अक्षों को मिला देता है और अधूरी योजना बनाता है:

| अक्ष | प्रश्न | रूप |
|---|---|---|
| **टेस्ट-स्तर** | किस स्तर पर? | Unit → Integration → System → Abnahme |
| **टेस्ट-प्रकार** | कौन-सा गुण? | funktional / nicht-funktional / strukturbezogen / änderungsbezogen |
| **टेस्ट-विधि** | Testfälle कैसे बनते हैं? | Black-Box / White-Box / erfahrungsbasiert |

इसके आर-पार: **statisch** (Reviews, statische Analyse — बिना चलाए, सबसे जल्दी और सस्ती दोष-खोज) बनाम **dynamisch** (कोड चलाया जाता है)।

---

## 2. स्थिति-राउटर: वर्तमान स्थिति क्या है?

ठोस स्थिति के अनुसार प्रवेश-बिंदु चुनें:

| स्थिति | कार्यप्रणाली |
|---|---|
| **नया Feature बनाना** | कोड से पहले स्वीकृति-मानदंड (Abnahmekriterien) स्पष्ट करें (ATDD/BDD-सोच)। Implementierung के साथ-साथ Unit-Tests (Äquivalenzklassen + Grenzwerte)। नए इंटरफ़ेस (Schnittstellen) के लिए Integrationstest। केवल एक E2E-Happy-Path, इससे अधिक नहीं। |
| **Bug ठीक करना** | पहले Bug को दोहराने वाला Test (लाल), फिर Fix (हरा) = **Re-Test**। उसके बाद वातावरण का **Regression**। स्वयं का निदान → `bugfix-protocol`। |
| **Refactoring** | कोई नया Feature-Test नहीं — मौजूदा Suite ही सुरक्षा-जाल है। पहले जाँचें कि Suite व्यवहार को वास्तव में कवर करती है या नहीं (आवश्यकता होने पर लक्षण-परीक्षण (Charakterisierungstests) जोड़ें)। Coverage/Mutation को कमी-सूचक के रूप में देखें। |
| **बिना Tests वाला Legacy-Code** | हर Funktion के Unit-Tests से शुरू न करें। पहले System-/API-स्तर पर वर्तमान व्यवहार के Charakterisierungstests लगाएँ, फिर जब किसी हिस्से को छूएँ तो Unit-Tests जोड़ें। |
| **API / Microservices** | Service-स्तर के API-Tests पर ज़ोर (पिरामिड का मध्य-स्तर)। अलग Teams/Deployments होने पर: साझा Staging-Integrationstests के बजाय **Contract Testing** (जैसे Pact)। |
| **Release की तैयारी** | क्रम: Smoke (Build स्थिर है?) → पूर्ण Regression → nicht-funktionale Tests (Last, Security) → UAT/Abnahme → Release-Kandidat पर Smoke। |
| **Performance की चिंता** | पहले मापने योग्य लक्ष्य तय करें (जैसे „P95 < 300 ms, 1,000 Nutzer पर"), नहीं तो कोई Test परिणाम नहीं दे सकता। Lasttest = सामान्य भार, Stresstest = टूटने का बिंदु + पुनर्प्राप्ति। उत्पादन-सदृश वातावरण अनिवार्य। |
| **Test-Pipeline सेट करना** | अनुभाग 4 के CI/CD-Gates लागू करें; हर Commit पर Unit + Lint से शुरू करें, फिर चरणबद्ध विस्तार करें। |
| **Teststrategie/Testkonzept लिखना** | तीन आयामों + चरण-मैपिंग (अनुभाग 4) + जोखिम-आधारित प्राथमिकता (अनुभाग 6, बिंदु 10) के अनुसार संरचना। |

---

## 3. टेस्ट-स्तर: परीक्षण-वस्तु, लक्ष्य, समय

| स्तर | जाँचता है | कब | सामान्य नियम |
|---|---|---|---|
| **Unit/Komponente** | एक Funktion/Klasse अलग से (Mocks/Stubs) | Implementierung के दौरान, हर Commit | पिरामिड का चौड़ा आधार; तेज़ (< सेकंड), निर्धारक (deterministisch) |
| **Integration** | परस्पर-क्रिया, Schnittstellen, DB-Anbindung | Unit-Tests के बाद, हर Merge पर | क्रमिक एकीकरण (Top-Down/Bottom-Up), बड़े सिस्टम में कभी Big Bang नहीं |
| **System** | तकनीकी आवश्यकताओं के विरुद्ध पूरा सिस्टम | जैसे ही एकीकृत Build उपलब्ध हो | funktional और nicht-funktional दोनों; स्वतंत्र Tester मूल्यवान |
| **Abnahme** | व्यावसायिक अपेक्षा, वास्तविक उपयोग | Go-Live से पहले अंतिम स्तर | व्यावसायिक विभाग (Fachbereich) द्वारा UAT; परिचालन (Backup/Deploy/Monitoring) न भूलें; आवश्यकता हो तो Alpha/Beta |

**Testpyramide** एक मात्रात्मक अनुपात के रूप में: बहुत सारे Unit-, लक्षित Integrations-/API-, और कम E2E-Tests
(लगभग 70/20/10 एक प्रारंभिक नियम — वास्तविक दोष-स्रोत के अनुसार समायोजित करें)। उल्टा पिरामिड
(बहुत सारे UI-Tests) = धीमा + flaky → इससे बचें।

---

## 4. चरण-मैपिंग: कब किसकी जाँच?

### CI/CD-Gates (आधुनिक मानक मैपिंग)

| Pipeline-चरण | Gate |
|---|---|
| हर Commit | Unit-Tests, Linter, statische Analyse (सेकंड–मिनट) |
| Pull Request | Code-Review, SAST/SCA, लक्षित Komponententests |
| Merge | Integrations-/API-/Contract-Tests, Testumgebung पर Smoke |
| Nightly / Pre-Release | पूर्ण Regression, E2E, Performance-/Lasttests, DAST |
| Release-Kandidat | Staging पर Smoke, UAT, Abnahme |
| Produktion (Shift-Right) | Monitoring/Observability, Canary/Blue-Green, Feature Flags, आवश्यकता हो तो Chaos-Experimente |

**समय-बजट और रोक-नियम (व्यवहार से लिए गए अनुमानित मान):**

- **Commit से Feedback < 10 मिनट** तेज़ पथ के लिए (Lint + Unit + महत्वपूर्ण Integrationstests); Staging तक पूरी pipeline **< 30–45 मिनट**; पूर्ण Regression nightly या Release से पहले। जो लूप इससे धीमा चले, उसे लोग बायपास कर देते हैं।
- **रोकने वाला बनाम सूचना देने वाला:** Unit-, Integrations- और Smoke-Gates हमेशा रोकते हैं (लाल होने पर कोई Merge/Deploy नहीं)। Nightly-चरण (Regression, Last, DAST) Ticket/Fix के माध्यम से सूचित करते हैं, पर हर Commit को नहीं रोकते। Prod-Deploy के बाद: Smoke + Monitoring — लाल होने पर Rollback + Incident।
- **हस्तांतरण-बिंदु:** Commit (git push) Inner Loop (स्थानीय: TDD, Unit, तेज़ पुनरावृत्ति) को Outer Loop (साझा pipeline के Gates के साथ) से अलग करता है। जिसे Inner Loop में खिसकाया जा सके, वहीं सबसे सस्ते में पकड़ा जाता है (Shift-Left)।

### क्लासिक (V-Modell): Spezifizieren के समय Tests का डिज़ाइन

Anforderungen↔Abnahmetest · Systemdesign↔Systemtest · Architektur↔Integrationstest ·
Code↔Unit-Test। मूल विचार: किसी स्तर के Tests **उसकी संबंधित Spezifikation बनाते समय** डिज़ाइन किए जाते हैं — अंत में नहीं। Anforderungen/Designs के Reviews (statisches Testen) सबसे जल्दी दोष-खोज हैं।

### Agile Testing Quadrants (Sprint-योजना का ग्रिड)

Q1 Unit/TDD + Q2 Story-Tests/BDD लगातार चलते हैं और दोषों को **रोकते** हैं;
Q3 explorativ/Usability/UAT + Q4 Performance/Security तब उत्पाद का **मूल्यांकन** करते हैं, जब पर्याप्त उत्पाद बन जाए। विवरण सूची में।

---

## 5. टेस्ट-डिज़ाइन विधि चुनें

| यदि परीक्षण-आधार (Testbasis) … | … तो विधि |
|---|---|
| इनपुट-क्षेत्र/मान-समूह हों | **Äquivalenzklassen** (हर वर्ग का एक प्रतिनिधि) + **Grenzwertanalyse** (हर सीमा पर और ठीक उसके पार: 5–50 के लिए 4, 5, 50, 51 परखें) — लगभग हर Unit-Test की मूल सुविधा |
| जटिल व्यावसायिक नियम/शर्त-संयोजन हों | **Entscheidungstabellentest** |
| अवस्थाएँ और संक्रमण हों (Workflow, Session, डिवाइस (Gerät)) | **Zustandsübergangstest** (निषिद्ध संक्रमण भी परखें) |
| उपयोगकर्ता-प्रवाह का वर्णन हो | **Use-Case-/Szenariotest** जिसमें त्रुटि- और अपवाद-पथ शामिल हों |
| कोड हो और Coverage मापना हो | **Anweisungs-/Zweigüberdeckung** — कमी-सूचक के रूप में, लक्ष्य के रूप में नहीं (100 % Coverage ≠ सही) |
| अस्पष्ट/अधूरा हो या समय कम हो | **Exploratives Testen** (Charter के साथ समय-सीमित सत्र) + **Error Guessing** (शून्य, खाली स्ट्रिंग, विशेष अक्षर, Zeitzonen, Race Conditions) |

पहले व्यवस्थित विधियाँ, फिर अनुभव-आधारित विधियाँ जानबूझकर **पूरक** के रूप में — वे वह पकड़ती हैं जो स्क्रिप्ट छोड़ देती हैं।

---

## 6. Best Practices (Tests की योजना/Review करते समय सूची)

1. **Shift-Left:** Anforderungsphase से Reviews + statische Analyse — दोष जितनी देर से मिले, उतना महँगा (Boehm के बाद प्रचलित नियम; दिशा निर्विवाद है, सटीक गुणक विवादित हैं)।
2. **Testpyramide का सम्मान** — E2E-Tests संयमित, Unit-आधार चौड़ा।
3. **जो दोहराया जाता है उसे स्वचालित करें** (Smoke, Regression, API, Unit) और उसे CI/CD-Gates में स्थापित करें; मैनुअल क्षमता explorativ + Usability के लिए सुरक्षित रखें।
4. **टेस्ट केस व्यवस्थित रूप से डिज़ाइन करें** (अनुभाग 5), अंधाधुंध नहीं।
5. **nicht-funktionale Anforderungen को मापने योग्य बनाएँ** — संख्यात्मक लक्ष्य के बिना कोई उपयोगी Performanz-/Lasttest नहीं।
6. **Re-Test ≠ Regression:** पहले Fix की पुष्टि, फिर दुष्प्रभाव। क्रम Smoke → Sanity/Re-Test → Regression।
7. **Flaky Tests को तुरंत संभालें** — अलग-थलग (Quarantäne) करें, कारण ठीक करें या हटाएँ; अस्थिर Suites pipeline पर भरोसा नष्ट कर देती हैं।
8. **Testdaten/-umgebungen प्रबंधित करें:** पुनरुत्पादनीय (Container/IaC), उत्पादन-सदृश, अनामीकृत या synthetische डेटा।
9. **Test-गुणवत्ता स्वयं मापें:** Coverage कमी-सूचक के रूप में; जहाँ Coverage-संख्याएँ भ्रम दे सकती हों, वहाँ **Mutation Testing**।
10. **जोखिम-आधारित प्राथमिकता:** परीक्षण की गहराई विफलता-प्रभाव × दोष-संभावना के अनुसार — समान रूप से नहीं।
11. **गुणवत्ता टीम का कार्य है** (Whole-Team-Approach): Tester को Anforderungen में जल्दी शामिल करें; BDD/ATDD को Fachbereich के साथ साझा माध्यम बनाएँ।
12. **Shift-Right न भूलें:** Monitoring, Canary, Feature Flags; परिपक्व Observability के बाद ही Chaos Engineering।

---

## 7. आधुनिक विधियाँ — कब अतिरिक्त रूप से लगाएँ

| विधि | कब लगाएँ … |
|---|---|
| **Contract Testing** (Pact) | अलग Deployments/Teams वाले Microservices |
| **Mutation Testing** (Stryker, PIT, mutmut) | मौजूदा Testsuite की गुणवत्ता आँकनी हो |
| **Property-Based Testing** (Hypothesis, fast-check) | Invarianten मौजूद हों („sortiert ist idempotent") और सीमांत मामलों (Randfälle) का डर हो |
| **Fuzzing** | Parser, Deserialisierung, सुरक्षा-संवेदनशील इनपुट (Eingaben) |
| **Chaos Engineering** | वितरित सिस्टम + परिपक्व Observability + साफ़ Rollbacks |

---

## पड़ोसी Skills (दोहराएँ नहीं)

- **`superpowers:test-driven-development`** — कोड लिखते समय ठोस Red-Green-Refactor-लूप।
- **`bugfix-protocol`** — किसी ठोस Bug का 6-चरणीय निदान।
- **`bugsweep`** — किसी कोडबेस (Codebasis) पर व्यवस्थित Bug-खोज।
- **`dev-cycle`** — 8-चरणीय संपूर्ण चक्र (v1.2.0 से: चरण 1/3/5 में Tests डिज़ाइन होते हैं, चरण 6 में लिखे जाते हैं, चरण 7 में चलाए जाते हैं; यह Skill भरता है कि कौन-से Tests कहाँ चलने चाहिए)।

## संदर्भ

पूरी सूची (सभी टेस्ट-स्तर, गैर-कार्यात्मक विस्तृत तालिका सहित सभी टेस्ट-प्रकार, सभी डिज़ाइन-विधियाँ, Agile Quadrants, statisch/dynamisch, V-Modell, स्रोत):
→ `testarten-katalog.md` (उसी फ़ोल्डर में)

दृश्य समग्र मानचित्र — चरण, नियंत्रण-लूप, भूमिकाएँ और Test-Gates „सॉफ़्टवेयर-विकास का सर्किट-आरेख" के रूप में (शीट BL-5 = Test-एकीकरण, BL-2 = नियंत्रण-लूप के समय-चक्र):
→ `../dev-cycle/SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (ब्राउज़र में खोलें)

---

## परिवर्तन-लॉग

### 1.0.1 (2026-08-22)
- CI/CD-Gates के लिए समय-बजट और रोक-नियम जोड़े गए (< 10 मिनट Fast Path, < 30–45 मिनट pipeline; रोकने बनाम सूचना देने वाले; Prod लाल होने पर Rollback) तथा Commit को Inner/Outer Loop का हस्तांतरण-बिंदु बनाया गया
- dev-cycle Skill की Schaltplan-Beilage का संदर्भ जोड़ा गया; dev-cycle की सीमांकन उसके v1.2.0 (Shift-Left: डिज़ाइन 1/3/5, लेखन 6, निष्पादन 7) के अनुसार समायोजित

### 1.0.0 (2026-08-22)
- ऑनलाइन शोध से प्रारंभिक संस्करण (ISTQB-व्यवस्था, Testpyramide, Agile Testing Quadrants, CI/CD-Gates, आधुनिक विधियाँ)
