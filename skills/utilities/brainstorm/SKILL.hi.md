---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "रचनात्मक तरीकों से विचार-उत्पादन की संरचित पद्धतियाँ: SCAMPER, Six Thinking Hats, Mind Mapping, Reverse Brainstorming, TRIZ, और Rapid Ideation।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [brainstorm, creativity, ideation, scamper, six-hats, innovation]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/brainstorm.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 3974ca6cf14e2ee379fed97740da2cd90f141ba00af3f22de1ca0cec31ac342e
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="brainstorm banner">

# Brainstorm

> नवाचार के लिए संरचित रचनात्मकता — SCAMPER, Six Hats, Mind Mapping, Reverse Brainstorming, TRIZ, Rapid Ideation

---

## कब उपयोग करें?

- नए विचारों की आवश्यकता है
- अटकाव / रचनात्मकता में रुकावट
- नवाचार की खोज है
- समस्या को रचनात्मक ढंग से हल करना है

**ट्रिगर-शब्द:** brainstorm, ideen, kreativ, innovativ, ideenfindung, विचार, रचनात्मक, नवाचार, विचार-उत्पादन

---

## विधियाँ

### 1. SCAMPER

**Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse**

मौजूदा समाधानों को व्यवस्थित रूप से बेहतर बनाना:
- **S**ubstitute: क्या बदला जा सकता है?
- **C**ombine: क्या जोड़ा जा सकता है?
- **A**dapt: क्या अनुकूलित किया जा सकता है?
- **M**odify: क्या संशोधित किया जा सकता है?
- **P**ut to other use: इसे और किस काम में लिया जा सकता है?
- **E**liminate: क्या हटाया जा सकता है?
- **R**everse: क्या उलटा किया जा सकता है?

---

### 2. Six Thinking Hats (Edward de Bono)

6 दृष्टिकोणों से व्यवस्थित रूप से सोचना:

- **White Hat — तथ्य:** हमारे पास कौन-सी जानकारी है? क्या कमी है?
- **Red Hat — भावना:** यह कैसा महसूस होता है? अंतर्ज्ञान, मन की भावना
- **Black Hat — आलोचना:** क्या गलत हो सकता है? जोखिम, कमज़ोरियाँ
- **Yellow Hat — आशावाद:** अवसर क्या हैं? सर्वोत्तम स्थिति
- **Green Hat — रचनात्मकता:** नए विचार? out-of-the-box?
- **Blue Hat — मेटा:** प्रक्रिया-नियंत्रण, सारांश, अगले कदम

**प्रक्रिया:** समस्या परिभाषित करें (Blue) -> तथ्य (White) -> भावनाएँ (Red) -> आलोचना (Black) -> सकारात्मक पहलू (Yellow) -> नए विचार (Green) -> सारांश (Blue)

---

### 3. Mind Mapping

विचारों को पदानुक्रम में दृश्य रूप देना:
1. केंद्रीय विषय
2. मुख्य शाखाएँ (3-7)
3. प्रत्येक श्रेणी के लिए उप-शाखाएँ
4. विवरण और विचार जोड़ें
5. संबंध पहचानें

---

### 4. Reverse Brainstorming

समस्या को उलटना: "हम इसे और बुरा कैसे बनाएँ?"

1. समस्या को उलटें
2. बुरे विचार इकट्ठा करें
3. उलटने पर = अच्छे विचार

सीधे विचार-उत्पादन के रुकने पर विशेष रूप से उपयोगी।

---

### 5. TRIZ (Theory of Inventive Problem Solving)

सॉफ़्टवेयर के लिए शीर्ष 10 सिद्धांत:
1. **Segmentation:** मोनोलिथ को मॉड्यूल में बाँटें
2. **Extraction:** बाधक गुण को अलग करें
3. **Local Quality:** अलग घटक, अलग गुण
4. **Merging:** समान कार्यों को मिलाएँ
5. **Universality:** एक तत्व, कई कार्य
6. **Nesting:** घटकों को एक-दूसरे में रखें
7. **Preliminary Action:** पहले से तैयारी
8. **Feedback:** निगरानी और समायोजन
9. **Self-Service:** प्रणाली स्वयं अपना रखरखाव करे
10. **Asymmetry:** असममित डिज़ाइन

---

### 6. Rapid Ideation

गुणवत्ता से पहले मात्रा — 20 मिनट में 50+ विचार।

**नियम:**
- Ideation के दौरान कोई आलोचना नहीं
- जंगली विचार स्वागत योग्य हैं
- दूसरों के विचारों पर आगे बढ़ें
- पहले मात्रा

**टाइमर-आधारित:**
- राउंड 1 (5 मिनट): खुला Ideation
- राउंड 2 (5 मिनट): विविधताएँ
- राउंड 3 (5 मिनट): संयोजन
- राउंड 4 (5 मिनट): अतिवादी विचार

---

## Workflow

```
1. User Request
2. Ziel verstehen
3. Methode(n) waehlen
4. Ideen generieren (keine Kritik!)
5. Clustering
6. Feasibility/Impact Matrix
7. Top 5-10 Auswahl
8. Output + Empfehlung
```

---

## Changelog

### 1.0.0 (2026-03-15)
- BACH v3.8.0 से पोर्ट किया गया

---

*BACH v3.8.0 से पोर्ट किया गया | Standalone-Version*

**यह भी देखें:** [think](../think/SKILL.md) (विश्लेषण, Root Cause, SWOT) | [decide](../decide/SKILL.md) (निर्णय-फ़्रेमवर्क)
