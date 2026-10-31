---
name: research-agent
version: 0.2.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-08-22
description: "प्रोजेक्ट-प्रथम Research पाइपलाइन, जिसमें लाइव गेट्स, स्रोत/PDF साक्ष्य, दावा-सीमाएँ, कंप्यूट और प्रकाशन नियंत्रण शामिल हैं; इसमें एक वैकल्पिक PubMed/arXiv स्टैंडर्ड-लाइब्रेरी सहायक भी है।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [research-pipeline, evidence, pdf-validation, publication-gates, pubmed, arxiv, literature-review, science]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e74f1bcd5fddbcf7f172c542aa7b2f9923b36a747d62029ad34864fa04df30c6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="research-agent banner">

> **जर्मन** — आधिकारिक जर्मन संस्करण / जर्मन में आधिकारिक दस्तावेज़।


# Research Agent (जर्मन)

यह संस्करण केंद्रीय पैकेज-मूल है। `<OneDrive>/.TOPICS/.RESEARCH` के भीतर वर्तमान प्रोजेक्ट- और Research-पाइपलाइन अधिकार मानी जाती है; साथ दिया गया PubMed/arXiv कोड केवल एक वैकल्पिक शोध उपकरण है।

## बाध्यकारी अधिकार-श्रृंखला

1. वर्तमान उपयोगकर्ता-आदेश और वैश्विक `AGENTS.md`-/`GPT.md`-/`CLAUDE.md`- नियम।
2. प्रोजेक्ट-स्थानीय वर्तमान फ़ाइलें, लाइव स्थिति, लॉक, निर्णय और रजिस्टर। क्रमांकित निरंतरताएँ और स्पष्ट करंट-पॉइंटर अपने पूर्ववर्तियों से पहले आते हैं; आर्काइव और विवाद प्रतियाँ चुपचाप प्रतिस्थापन अधिकार नहीं बनतीं।
3. Research-रूट में लाइव पाइपलाइन: विशेष रूप से `CLAUDE.md`, `START*`, `MASTER*`, `POLICY*`, `PUBLIKATIONSVERFAHREN.md`, `QUALITY_RULES*`, वर्तमान स्थिति-/TODO-पॉइंटर तथा `CHECKS-LOG.txt` और `CHECKS-REG.md`।
4. यह स्किल और उसके सामान्य खोज स्क्रिप्ट।

शुरुआत में `~/.codex/GPT.md`, दोनों वैश्विक `CLAUDE.md`-फ़ाइलें, Research-नियम और वर्तमान प्रोजेक्ट-स्थानीय `KONZEPT*`, योजना-, `TODO*`, `BEWEISNOTIZ*`, निर्णय-, प्रकाशन- और बिब्लियोग्राफी-फ़ाइलें पढ़ी जानी चाहिए। विरोधाभास होने पर fail-closed लागू होता है।

## लाइव-गेट्स और म्यूटेशन

- एक वर्तमान अपठनीय `CHECKS-LOG.txt` एक कठोर केवल-पठन गेट है।
- चयन या बदलाव से पहले: `CHECKS-REG.md`, प्रोजेक्ट-रजिस्टर, निर्णय, यदि उपलब्ध हो तो Fable-Plan, लॉक, विवाद प्रतियाँ और लाइव स्थिति जाँचें।
- BACH/BYUM-होल्ड और उनकी समय-सीमा केवल `fc_get_time` से सिद्ध करें।
- OneDrive FileCommander का उपयोग नेविगेशन, रीड, मेटाडेटा, चेकसम, क्लाउड-लॉक और निष्पादन के लिए करें। लिखने से पहले सीमित लॉक लगाएँ, दूसरों के लॉक और परिवर्तनों की रक्षा करें, और अंत में केवल अपना लॉक हटाएँ।
- प्रोडक्ट-/विषय-निर्णय, कूलडाउन, गायब कैनोनिकल क्लोन, पुनरुत्पादन गेट्स और उपभोग हो चुकी एक-बार की स्वीकृतियों को स्वायत्त रूप से बायपास न करें।

## साक्ष्य, दावा, कंप्यूट और प्रकाशन नियम

- स्थानीय `.WISSEN`-खोजें जल्दी उपयोग करें, फिर वैज्ञानिक कथनों को प्राथमिक स्रोतों से सत्यापित करें। वाक्य/खंड/पृष्ठ, पूर्वापेक्षाएँ, सामान्यीकरण और ऑब्जेक्ट-प्रकार को सटीक रूप से बाँधें; अस्थिर क्वेरी की तिथि दर्ज करें।
- PDF को केवल `%PDF-` के अनुसार, पठनीय पृष्ठ-संख्या/टेक्स्ट-एक्सट्रैक्शन और SHA-256 के साथ स्रोत के रूप में दर्ज करें। HTML-, CAPTCHA-, 404- और प्लेसहोल्डर फ़ाइलें गिनी नहीं जातीं।
- माप, दीर्घकालिक साक्ष्य, अनिश्चितता और शोध-विकल्प को अलग रखें; किसी प्रॉक्सी, प्रीफ़्लाइट, समीक्षा या आंशिक रन को वैज्ञानिक दावे तक न बढ़ाएँ।
- जर्मन अंतिम-उपयोगकर्ता आर्टिफ़ैक्ट वास्तविक Umlaute (ä, ö, ü) का उपयोग करते हैं। EN/DE और संयुक्त आर्टिफ़ैक्ट की जाँच केवल तभी करें जब वर्तमान पाइपलाइन इसकी अनुमति दे: संरचना, बिब्लियोग्राफी, बिल्ड, एक्सट्रैक्शन और एन्कोडिंग।
- कंप्यूट केवल लाइव `.COMPUTE`-/प्रोजेक्ट-अनुबंध और प्लेसमेंट-नियमों के अनुसार। बिना स्पष्ट अधिकार के लंबे लैपटॉप-रन, रिट्राई, निरंतरताएँ, क्यू-परिवर्तन या उपभोग हो चुके एक-बार के रन न करें। टाइमआउट/इन्फ्रा-त्रुटियाँ गणितीय नकारात्मक परिणाम नहीं हैं।
- अपलोड, पब्लिक-स्विच, सबमिट, रजिस्ट्री-बुकिंग और रिलीज़ अलग-अलग उपयोगकर्ता-गेट हैं। तैयारी और ड्राई-रन प्रकाशन नहीं हैं।
- समापन तभी जब आवश्यक टेस्ट/बिल्ड, आर्टिफ़ैक्ट-रीडबैक, प्रोजेक्ट- और रूट-रजिस्टर, यदि आवश्यक हो तो ऑटोमेशन-मेमोरी/हैंडऑफ़ और अपने अस्थायी लॉक हटाना पूरे हों। शेष गेट स्पष्ट रूप से बताएँ।

## वैकल्पिक साहित्य सहायक

निम्नलिखित Python मॉड्यूल केवल स्टैंडर्ड-लाइब्रेरी का उपयोग करते हैं (`urllib`, `xml`, `json`)। ये खोज और समीक्षा में सहायता करते हैं, पर ऊपर की किसी भी अधिकार- या साक्ष्य-जाँच का स्थान नहीं लेते।

## आर्किटेक्चर

```
ResearchAgent (Orchestrator)
  sources/          Data sources (PubMed, arXiv)
    base.py         Article/SearchResult dataclasses, Source ABC
    pubmed.py       NCBI E-utilities (esearch + efetch)
    arxiv.py        arXiv Atom API
  workflows/        Research workflows
    quick_search.py Quick search across multiple sources
    literature_review.py  4-phase literature review
```

## Python लाइब्रेरी के रूप में उपयोग

```python
from scripts.agent import ResearchAgent

agent = ResearchAgent()

# Quick search (Deutsch)
result = agent.search("machine learning diagnostics", max_results=10)
print(result)

# Structured literature review (Deutsch)
plan = agent.create_review_plan("transformer architectures", years=3)
print(plan.total_articles, "articles found")

# Save result (Deutsch)
agent.save_result(result, "research_ml.md", fmt="markdown")
```

## CLI के रूप में उपयोग

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## डेटा स्रोत

| स्रोत | API | दर सीमा | पहुँच |
|--------|-----|------------|--------|
| PubMed | NCBI E-utilities | 3/सेकंड (कुंजी के बिना), 10/सेकंड (कुंजी के साथ) | निःशुल्क |
| arXiv | Atom REST API | कोई दस्तावेज़ित सीमा नहीं | निःशुल्क |

विस्तार योग्य: नए स्रोत `Source` ABC को लागू करते हैं, जो `sources/base.py` में है।

## विस्तार

```python
from scripts.sources.base import Source, SearchResult

class MySource(Source):
    @property
    def name(self) -> str:
        return "my-source"

    def search(self, query, max_results=10, **kwargs):
        # Implement API query
        ...

    def get_article(self, article_id):
        ...

    def is_available(self) -> bool:
        return True
```

## BACH नोट्स

> केवल तब प्रासंगिक जब BACH के भीतर उपयोग हो।

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## परिवर्तन लॉग

### 0.2.0 (2026-08-22)
- प्रोजेक्ट- और पाइपलाइन-अधिकार को सामान्य खोज स्क्रिप्ट से पहले स्थापित किया गया
- लाइव-गेट्स, OneDrive-/लॉक-नियम और करंट-पॉइंटर जोड़े गए
- प्राथमिक-स्रोत/PDF प्रमाण, दावा-सीमाएँ और द्विभाषी जाँचें जोड़ी गईं
- कंप्यूट-, अपलोड-, रजिस्टर- और समापन-गेट्स को fail-closed रूप में दर्ज किया गया

### 0.1.0 (2026-03-12)
- MODULAR_AGENTS/ResearchAgent से skill library में माइग्रेशन
- PubMed + arXiv स्रोत
- QuickSearch + LiteratureReview वर्कफ़्लो
