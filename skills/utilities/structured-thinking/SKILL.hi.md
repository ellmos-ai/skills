---
name: structured-thinking
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-05-19
description: "मेटा-स्किल: 3-चरणीय वर्कफ़्लो के रूप में संरचित चिंतन। विश्लेषण (think), विचार-मंथन (brainstorm) और निर्णय-लेना (decide) को एक सतत प्रक्रिया में संयोजित करता है।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [denken, analyse, kreativitaet, entscheidung, workflow, meta-skill]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'merged_from': ['utilities/think (v1.0.0)', 'utilities/brainstorm (v1.0.0)', 'utilities/decide (v1.0.0)'], 'local_changes_since_sync': False}
translated_from_sha256: e82ba03e100146dcafad229ee0d37103ce41774ddbb87ec965cabebcf2c88fef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="structured-thinking banner">

# संरचित चिंतन — विश्लेषण करना, विचार खोजना, निर्णय लेना

> संरचित चिंतन के लिए मेटा-वर्कफ़्लो: समस्या-विश्लेषण से लेकर रचनात्मक समाधानों और फिर सुदृढ़ निर्णय तक

---

## वर्कफ़्लो का अवलोकन

```
Problem/Frage
     |
     v
Phase 1: ANALYSIEREN (think)
  Divide & Conquer, Root Cause, Constraint Relaxation
     |
     v
Phase 2: IDEENFINDEN (brainstorm)
  SCAMPER, Six Hats, Reverse Brainstorming, Rapid Ideation
     |
     v
Phase 3: ENTSCHEIDEN (decide)
  Pro/Con, Weighted Scoring, Scenario Analysis, Eisenhower
     |
     v
Ergebnis + Begruendung
```

---

## चरण 1: विश्लेषण करना

लक्ष्य: समस्या को समझना, कारणों की पहचान करना, संरचना को पहचानना।

### दृष्टिकोण

| विधि | कब | प्रवाह |
|------|----|--------|
| **Divide & Conquer** | जटिल समस्या | समस्या → उप-समस्याएँ → अलग-अलग हल करें → संयोजित करें |
| **Root Cause (5x क्यों)** | लक्षण दिखता है, कारण अस्पष्ट | लक्षण → क्यों? → क्यों? → ... → कारण → समाधान |
| **Constraint Relaxation** | समस्या अनसुलझी लगती है | बाधाएँ ढीली करें → हल करें → बाधाएँ फिर से कसें |
| **सादृश्य-खोज** | नई प्रकार की समस्या | मिलती-जुलती ज्ञात समस्या खोजें → समाधान अनुकूलित करें |

### विश्लेषण-ढाँचे

| ढाँचा | उपयोग |
|-------|-------|
| **SWOT** | शक्तियाँ / कमज़ोरियाँ / अवसर / जोखिम |
| **Pareto** | 80/20 — सबसे बड़ा लाभ क्या देता है? |
| **Fishbone** | व्यवस्थित कारण-विश्लेषण (Ishikawa) |

### अनिश्चितता में अनुमान-नियम

1. सबसे बुरा परिदृश्य (Worst-Case) क्या है?
2. क्या यह उलटा जा सकता है?
3. कार्य न करने की लागत क्या है?

### जटिलता में अनुमान-नियम

1. सबसे सरल पहला कदम क्या है?
2. कोई विशेषज्ञ क्या करता?
3. 80% का समाधान क्या होगा?

---

## चरण 2: विचार खोजना

लक्ष्य: अधिकतम संभव समाधान-दृष्टिकोण उत्पन्न करना। गुणवत्ता से पहले मात्रा। इस चरण के दौरान कोई आलोचना नहीं।

### विधियाँ

**SCAMPER** — मौजूदा समाधानों को व्यवस्थित रूप से सुधारना:
- **S**ubstitute: क्या बदलें? | **C**ombine: क्या संयोजित करें? | **A**dapt: क्या अनुकूलित करें?
- **M**odify: क्या संशोधित करें? | **P**ut to other use: और किस काम में? | **E**liminate: क्या हटाएँ?
- **R**everse: क्या उलटें?

**Six Thinking Hats** (de Bono) — 6 दृष्टिकोण क्रमशः:
1. नीला: प्रक्रिया-नियंत्रण ("प्रश्न क्या है?")
2. सफ़ेद: तथ्य ("हम क्या जानते हैं?")
3. लाल: भावना ("क्या सही लगता है?")
4. काला: आलोचना ("क्या गलत हो सकता है?")
5. पीला: आशावाद ("अवसर क्या हैं?")
6. हरा: रचनात्मकता ("कौन-से नए विचार हैं?")

**Reverse Brainstorming** — समस्या को उलटना:
1. "हम इसे और बुरा कैसे बनाएँ?"
2. बुरे विचार इकट्ठा करें
3. उलटें = अच्छे विचार

**Rapid Ideation** — 20 मिनट में 50+ विचार:
- राउंड 1 (5 मिनट): खुला विचार-मंथन
- राउंड 2 (5 मिनट): भिन्नताएँ
- राउंड 3 (5 मिनट): संयोजन
- राउंड 4 (5 मिनट): चरम विचार

### आइडिएशन के बाद

1. क्लस्टरिंग: मिलते-जुलते विचारों को समूहबद्ध करें
2. Feasibility/Impact Matrix: व्यवहार्यता बनाम प्रभाव का मूल्यांकन करें
3. चरण 3 के लिए शीर्ष 5-10 का चयन करें

---

## चरण 3: निर्णय लेना

लक्ष्य: पारदर्शी तर्क के साथ सर्वोत्तम विकल्प चुनना।

### ढाँचे का चयन

| स्थिति | ढाँचा |
|--------|-------|
| 2 विकल्प, त्वरित निर्णय | **Pro/Con Matrix** |
| 3+ विकल्प, कई मानदंड | **Weighted Scoring** |
| क्रमिक यदि-तो निर्णय | **Decision Tree** |
| उच्च अनिश्चितता | **Scenario Analysis** |
| कार्यों को प्राथमिकता देना | **Eisenhower Matrix** |

### Weighted Scoring (मुख्य विधि)

1. मानदंड इकट्ठा करें (3-7, विशिष्ट और मापने योग्य)
2. भार तय करें (योग = 100%, सबसे महत्वपूर्ण >= 25%)
3. विकल्पों का मूल्यांकन करें (1-10 पैमाना)
4. स्कोर की गणना करें (मूल्यांकन x भार)
5. तुलना करें और अनुशंसा करें

### Scenario Analysis

```
Best Case (X%):      Ergebnis → Erwartungswert
Realistic Case (X%): Ergebnis → Erwartungswert
Worst Case (X%):     Ergebnis → Erwartungswert
Gesamt-Erwartungswert: [Summe]
```

### Eisenhower Matrix

```
              DRINGEND        NICHT DRINGEND
WICHTIG       1. TUN          2. PLANEN
NICHT WICHTIG 3. DELEGIEREN   4. ELIMINIEREN
```

### अंतिम अनुशंसा से पहले गुणवत्ता जाँच-सूची

- [ ] क्या सभी प्रासंगिक मानदंड पहचाने गए?
- [ ] क्या उपयोगकर्ता के मूल्यों पर विचार किया गया?
- [ ] क्या दीर्घकालिक प्रभावों पर विचार किया गया?
- [ ] क्या जोखिम पहचाने और मूल्यांकित किए गए?
- [ ] क्या Bias-जाँच की गई?
- [ ] क्या उलटने की क्षमता जाँची गई?

---

## स्थिति-संवेदी चयन

| स्थिति | अनुशंसित चरण |
|--------|--------------|
| "मेरे सामने एक समस्या है" | चरण 1 (विश्लेषण) → आवश्यकतानुसार चरण 2+3 |
| "मुझे विचार चाहिए" | चरण 2 (विचार खोजना) |
| "मुझे निर्णय लेना है" | चरण 3 (निर्णय) |
| "मैं अटक गया हूँ" | चरण 2 (Reverse Brainstorming) |
| "मुझे किस चीज़ को प्राथमिकता देनी चाहिए?" | चरण 3 (Eisenhower) |
| "जटिल समस्या को समझना" | चरण 1 (Divide & Conquer + SWOT) |

---

## परिवर्तन-लॉग

### 1.0.0 (2026-05-19)
- think, brainstorm और decide से मेटा-स्किल के रूप में निर्मित

---

*मेटा-स्किल | विस्तृत संदर्भ: [think](../think/SKILL.md), [brainstorm](../brainstorm/SKILL.md), [decide](../decide/SKILL.md)*
