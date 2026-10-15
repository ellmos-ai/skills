---
name: dev-cycle
version: 1.2.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-08-22
description: "8-चरणीय विकास चक्र: फ़ीचर अनुरोध, वर्तमान स्थिति, कार्यात्मक योजना, फ़्रंटएंड, बैकएंड योजना, बैकएंड कोड, परीक्षण, उपयोग-मामले। व्यवस्थित सॉफ़्टवेयर विकास के लिए पुनरावृत्तिमूलक ढाँचा।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 3d82b648971c28906aeabf5b953a28ac162897503581e5cb5a6af8d9f0b1ae8f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.873368+00:00"
---
<img src="banner.png" width="100%" alt="dev-cycle banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# विकास चक्र (Dev Cycle) (Deutsch)

> **लक्ष्य:** फ़ीचर अनुरोध से सत्यापित प्रणाली तक एक संरचित प्रक्रिया।
> हर विकास इन 8 चरणों से होकर गुजरता है।

> 📐 **परिशिष्ट:** `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` —
> मनुष्य के लिए पठनीय „सॉफ़्टवेयर विकास का सर्किट आरेख" (HTML, ब्राउज़र में खोलें):
> चरणों, नियंत्रण लूपों, भूमिकाओं, प्रक्रिया शृंखलाओं और परीक्षण-गेटों का शोधित समग्र मानचित्र
> (वेब-शोध 08/2026), जिसमें यह 8-चरणीय चक्र समाहित होता है।

---

## अवलोकन और उद्देश्य

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                           |
  +--------------------------------------------------------------+
  |                                                                |
  |  Phase 1   Feature Requests (functional requirements)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 2   Check Current State (What already exists?)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 3   Functional Planning                                 |
  |            (Workflows, Agents, Experts, Skills, Services)      |
  |     |                                                          |
  |     v                                                          |
  |  Phase 4   Implement Functional Frontend                       |
  |            (Skill files, workflow markdown, agent profiles)     |
  |     |                                                          |
  |     v                                                          |
  |  Phase 5   Plan and Align Backend                              |
  |            (CLI handlers, DB schema, API endpoints)            |
  |     |                                                          |
  |     v                                                          |
  |  Phase 6   Implement Backend Tasks                             |
  |            (Python code, tools, DB migrations)                 |
  |     |                                                          |
  |     v                                                          |
  |  Phase 7   Test Execution, Review Gate and Bugfixes           |
  |            (B/O/E tests, bugfix protocol, code review)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 8   Functional and Feature Test: USE CASES              |
  |            (End-to-end validation from user perspective)        |
  |                                                                |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
  - Shift-Left: tests are DESIGNED early (phases 1/3/5) and WRITTEN
    with the code (phase 6) - phase 7 only EXECUTES them
```

---

## चरण 1: फ़ीचर अनुरोध (कार्यात्मक आवश्यकताएँ)

**क्या:** कार्यात्मक आवश्यकताओं को एकत्र करना और सूत्रबद्ध करना।

**इनपुट:**
- उपयोगकर्ता की इच्छाएँ, विचार, समस्याएँ
- साथी सुझाव (LLM सहायक)
- उपयोग-मामलों से अंतर्दृष्टि (प्रतिक्रिया लूप!)

**आउटपुट:**
- कार्य-प्रणाली में कार्य (जैसे issue, ticket या TODO सूची के रूप में)
- आवश्यकताएँ बताती हैं कि क्या चाहिए, न कि कैसे
- प्रत्येक आवश्यकता के साथ परीक्षण-योग्य स्वीकृति मानदंड हों (Shift-Left: ये
  चरण 8 के उपयोग-मामले और स्वीकृति सूची बन जाते हैं)

**नियम:**
- आवश्यकताएँ हमेशा कार्यात्मक रूप में लिखें ("उपयोगकर्ता X कर सकता है")
- तकनीकी रूप में नहीं ("X के लिए REST endpoint लागू करें")
- उपयोग-मामलों को आवश्यकता का स्रोत बनाएँ (चरण 8 -> चरण 1)

---

## चरण 2: वर्तमान स्थिति की जाँच

**क्या:** मौजूदा कार्यक्षमता की सूची बनाना।

**चेकलिस्ट:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**आउटपुट:**
- क्या मौजूद है, क्या गायब है, और क्या विस्तार की आवश्यकता है, इसका दस्तावेज़
- दोहराव से बचाव

---

## चरण 3: कार्यात्मक योजना

**क्या:** कार्यात्मक स्तर पर योजना बनाना - तुरंत कोड न लिखें।

**योजना स्तर:**

| स्तर | प्रश्न | कलाकृति |
|-------|----------|----------|
| Workflow | समन्वय कब/कैसे होता है? | workflows/*.md |
| Agent | कौन निष्पादित करता है? | agents/*.txt |
| Expert | किसके पास डोमेन ज्ञान है? | experts/*/ |
| Skill | क्या किया जाता है? | skills/*.md |
| Service | तकनीकी रूप से कैसे किया जाता है? | services/*/ |

**नियम:**
- पहले कार्यात्मक सोचें, फिर तकनीकी
- Shift-Left: हर योजना स्तर के लिए उसकी जाँच की भी योजना बनाएँ — आवश्यकता →
  स्वीकृति मानदंड, service/interface → integration test, unit → unit test
  (परीक्षण-स्तर और तकनीक का चयन: [software-testing](../software-testing/SKILL.md))
- Workflows प्रक्रियाओं का वर्णन करें, कार्यान्वयन विवरण का नहीं
- हर agent की स्पष्ट प्रोफ़ाइल होनी चाहिए
- Services उपयोगकर्ता डेटा के बिना काम करने चाहिए

---

## चरण 4: कार्यात्मक फ़्रंटएंड लागू करना

**क्या:** skill फ़ाइलें, workflow markdown, agent प्रोफ़ाइल बनाना।

यहाँ "फ़्रंटएंड" कार्यात्मक विवरण की परत है:
- Workflow फ़ाइलें (.md)
- Agent प्रोफ़ाइल (.txt)
- Expert ज्ञान
- Service विवरण
- सहायता फ़ाइलें

**आउटपुट:**
- सभी कार्यात्मक विवरण मौजूद हों
- एक LLM साथी workflow को पढ़कर समझ सके
- कार्यात्मक परत पूरी तरह दस्तावेज़ित हो

---

## चरण 5: बैकएंड की योजना और संरेखण

**क्या:** तकनीकी आर्किटेक्चर को कार्यात्मक फ़्रंटएंड के साथ संरेखित करना।

**योजना क्षेत्र:**

| क्षेत्र | प्रश्न | स्थान |
|------|----------|----------|
| CLI Handlers | कौन-से commands? | handlers/*.py |
| DB Schema | कौन-सी tables/columns? | schema/*.sql |
| API Endpoints | कौन-से GUI endpoints? | server.py |
| Tools | कौन-सी Python scripts? | tools/*.py |

**आउटपुट:**
- कार्यात्मक फ़्रंटएंड के साथ संरेखित तकनीकी योजना
- DB schema डिज़ाइन
- CLI command संरचना

---

## चरण 6: बैकएंड कार्य लागू करना

**क्या:** Python कोड, DB migrations, CLI handlers लिखना।

**चेकलिस्ट (प्रति कार्य):**
```
  [ ] Unit tests written (TDD: test before code) and green locally?
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## चरण 7: परीक्षण निष्पादन, समीक्षा गेट और बगफ़िक्स

**क्या:** तकनीकी शुद्धता सुनिश्चित करना। परीक्षण चरण 1/3/5 में डिज़ाइन किए गए थे और
चरण 6 में लिखे गए (Shift-Left) — चरण 7 उन्हें चरणबद्ध, अवरोधक गेटों में निष्पादित करता है:
हर commit पर तेज़ परीक्षण, महंगे परीक्षण (पूर्ण regression, E2E, load) रात्रि में या रिलीज़ से पहले।
गेट मैपिंग और परीक्षण चयन: [software-testing](../software-testing/SKILL.md).

**परीक्षण प्रकार (B/O/E):**

| प्रकार | दृष्टिकोण | विवरण |
|------|-------------|-------------|
| B-Tests | बाहरी/स्वचालित | स्वचालित परीक्षण, CI/CD |
| O-Tests | कार्यात्मक (Input->Output) | मैन्युअल कार्यात्मक सत्यापन |
| E-Tests | व्यक्तिपरक/अनुभव | UX मूल्यांकन, एर्गोनॉमिक्स |

**समीक्षा गेट (चरण 8 से पहले):**
- दूसरी जोड़ी आँखों द्वारा कोड समीक्षा (peer, reviewer agent, या advisor)
- कुछ भी बिना समीक्षा के उपयोग-मामला सत्यापन में न जाए
- समीक्षा निष्कर्ष परिवर्तन अनुरोधों के रूप में चरण 6 पर लौटें

**बग पर:**
- bugfix protocol लागू करें
- 20-मिनट नियम का पालन करें (20 मिनट बाद दृष्टिकोण बदलें)
- सीखे गए सबक दस्तावेज़ित करें

---

## चरण 8: कार्यात्मक और फ़ीचर परीक्षण - उपयोग-मामले

**क्या:** उपयोगकर्ता के दृष्टिकोण से अंत-से-अंत सत्यापन।

**उपयोग-मामले दोनों उद्देश्य पूरे करते हैं:**
1. **फ़ीचर संकेतक** - क्या वांछित है? क्या संभव होना चाहिए?
2. **परीक्षण परिदृश्य** - क्या यह वास्तव में A से Z तक काम करता है?

**उपयोग-मामला प्रारूप:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**प्रतिक्रिया लूप:**
- विफल उपयोग-मामले -> चरण 1 में नए कार्य
- सफल उपयोग-मामले -> सत्यापित फ़ीचर
- नए उपयोग-मामले विचार -> कार्य के रूप में दर्ज करें

---

## सारांश: चक्र

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

चक्र एक लूप है: उपयोग-मामले फ़ीचर सत्यापित करते हैं और साथ ही
नई आवश्यकताएँ उत्पन्न करते हैं।

---

## नियंत्रण लूप (Regelkreise)

8-चरणीय चक्र बाहरी नियंत्रण लूप है। इसके भीतर तेज़ लूप एक साथ चलते हैं — लूप में जितना भीतर स्थित हो,
उसकी टैक्ट उतनी तेज़ और सुधार उतना सस्ता:

| लूप | टैक्ट | चक्र में स्थान |
|------|--------------------|--------------------|
| TDD (Red–Green–Refactor) | सेकंड–मिनट | चरण 6 के भीतर |
| परीक्षण निष्पादन / CI गेट | प्रति commit < 10 मिनट | चरण 7 → विफल होने पर चरण 6 |
| समीक्षा गेट (4 आँखें) | घंटे | चरण 7 और चरण 8 के बीच |
| बगफ़िक्स लूप | घंटे | चरण 7 → चरण 6 (bugfix protocol) |
| उपयोग-मामला लूप | प्रति चक्र | चरण 8 → चरण 1 |
| संचालन प्रतिक्रिया | निरंतर | निगरानी/घटनाएँ → चरण 1 |

सामान्य नियम: commit से प्रतिक्रिया तक का समय 10 मिनट से कम रखें — धीमा लूप बायपास हो जाता है।
समय सहित सभी लूपों का दृश्य मानचित्र: संलग्न
`SCHALTPLAN-SOFTWAREENTWICKLUNG.html`, शीट BL-2.

---

## चरण-विशिष्ट skills

| चरण | विशेषीकृत skill | ट्रिगर |
|-------|-------------------|--------------------|
| चरण 1-3 | Project bootstrapper (यदि उपलब्ध हो) | नई परियोजना बनाना (greenfield) |
| चरण 2 | [project-onboarding](../project-onboarding/SKILL.en.md) | मौजूदा परियोजना अपनाना |
| चरण 2-3 | [docs-analysis](../docs-analysis/SKILL.en.md) | आवश्यकता दस्तावेज़ों की कोड से जाँच |
| चरण 5-6 | [pipeline-optimizer](../pipeline-optimizer/SKILL.en.md) | मौजूदा संरचनाओं का नवीनीकरण |
| चरण 7 | [bugfix-protocol](../bugfix-protocol/SKILL.en.md) | व्यवस्थित 6-चरणीय डिबगिंग |
| चरण 7-8 | [bugsweep](../bugsweep/SKILL.en.md) | रिलीज़ से पहले अभिसरणशील बग सफ़ाई |
| चरण 1, 3, 7 | [software-testing](../software-testing/SKILL.md) | परीक्षण स्तर, प्रकार और डिज़ाइन तकनीकें चुनें; CI/CD गेट मैपिंग |
| चरण 8 के बाद | [github-repo-care](../github-repo-care/SKILL.en.md) | रिलीज़: रिपॉज़िटरी प्रकाशित और रखरखाव करें |

यदि आपके skill संग्रह में skill सूची है, तो आगे के चरण-विशिष्ट skills के लिए उसमें खोजें।

---

## परिवर्तन लॉग

### 1.2.0 (2026-08-22)
- Shift-Left स्थापित (परिशिष्ट-सर्किट आरेख के साथ शोध-मिलान): स्वीकृति मानदंड चरण-1 आउटपुट के रूप में,
  हर योजना स्तर पर चरण 3 में परीक्षण डिज़ाइन, Unit-Tests (TDD) चरण-6 चेकलिस्ट का पहला बिंदु; चरण 7 का नाम
  „Test Execution, Review Gate and Bugfixes" रखा गया — परीक्षण वहाँ निष्पादित होते हैं, केवल लिखे नहीं जाते
- समीक्षा गेट (4-आँखें सिद्धांत) चरण 8 से पहले स्पष्ट चरण के रूप में
- नया खंड „Control Loops (Regelkreise)" टैक्ट समय सहित (TDD, CI, समीक्षा,
  बगफ़िक्स, उपयोग-मामला, संचालन)
- चरण-skill तालिका विस्तारित: software-testing (चरण 1/3/7), github-repo-care
  (चरण 8 के बाद); चरण 3 और चरण 7 में software-testing के संदर्भ

### 1.1.1 (2026-08-22)
- परिशिष्ट `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (मनुष्य के लिए पठनीय समग्र मानचित्र: चरण,
  नियंत्रण लूप, भूमिकाएँ, प्रक्रिया शृंखलाएँ, परीक्षण-गेट — वेब-शोध 08/2026 का संश्लेषण)
  और फ़ाइल के शीर्ष पर संदर्भ

### 1.1.0 (2026-06-13)
- नई "Phase-specific skills" तालिका, जिसमें project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol और bugsweep के संदर्भ हैं

### 1.0.0 (2026-03-12)
- BACH से पोर्ट किया गया (dev-zyklus v1.0.0)

---

*निर्मित: 2026-01-28 | पोर्ट किया गया: 2026-03-12*
