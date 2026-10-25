---
name: research-agent
version: 0.2.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-08-22
description: "প্রজেক্ট-ফার্স্ট রিসার্চ পাইপলাইন, লাইভ গেট, সোর্স/PDF প্রমাণ, দাবির সীমা, কম্পিউট ও প্রকাশনা নিয়ন্ত্রণসহ; ঐচ্ছিক PubMed/arXiv স্ট্যান্ডার্ড-লাইব্রেরি সহায়ক অন্তর্ভুক্ত।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [research-pipeline, evidence, pdf-validation, publication-gates, pubmed, arxiv, literature-review, science]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e74f1bcd5fddbcf7f172c542aa7b2f9923b36a747d62029ad34864fa04df30c6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="research-agent banner">

> **জার্মান** — জার্মান ভাষায় অফিশিয়াল সংস্করণ / জার্মান ভাষায় অফিশিয়াল নথি।


# Research Agent (জার্মান)

এই সংস্করণটি প্যাকেজের মূল উৎস। `<OneDrive>/.TOPICS/.RESEARCH`-এর মধ্যে বর্তমান প্রজেক্ট ও রিসার্চ-পাইপলাইন কর্তৃত্বসম্পন্ন বলে গণ্য হবে; সঙ্গে দেওয়া PubMed/arXiv কোডটি কেবল একটি ঐচ্ছিক গবেষণা সরঞ্জাম।

## বাধ্যতামূলক কর্তৃত্ব-শৃঙ্খল

1. বর্তমান ব্যবহারকারীর অনুরোধ এবং বৈশ্বিক `AGENTS.md`-/`GPT.md`-/`CLAUDE.md`-নিয়মাবলি।
2. প্রজেক্ট-স্থানীয় বর্তমান ফাইল, লাইভ অবস্থা, লক, সিদ্ধান্ত ও রেজিস্টার। ক্রমাঙ্কিত ধারাবাহিকতা ও স্পষ্ট কারেন্ট-পয়েন্টার তাদের পূর্ববর্তীদের অগ্রাধিকার পাবে; আর্কাইভ ও দ্বন্দ্ব-কপি নীরবে বিকল্প কর্তৃত্বে পরিণত হবে না।
3. রিসার্চ-রুটের লাইভ পাইপলাইন: বিশেষত `CLAUDE.md`, `START*`, `MASTER*`, `POLICY*`, `PUBLIKATIONSVERFAHREN.md`, `QUALITY_RULES*`, বর্তমান স্ট্যাটাস/TODO-পয়েন্টার এবং `CHECKS-LOG.txt` ও `CHECKS-REG.md`।
4. এই স্কিল ও এর সাধারণ অনুসন্ধান-স্ক্রিপ্টসমূহ।

শুরুতে `~/.codex/GPT.md`, দুটি বৈশ্বিক `CLAUDE.md`-ফাইল, রিসার্চ-নিয়মাবলি এবং বর্তমান প্রজেক্ট-স্থানীয় `KONZEPT*`, পরিকল্পনা-, `TODO*`, `BEWEISNOTIZ*`, সিদ্ধান্ত-, প্রকাশনা ও গ্রন্থপঞ্জি-ফাইলগুলো পড়তে হবে। বিরোধের ক্ষেত্রে ফেইল-ক্লোজড নীতি প্রযোজ্য।

## লাইভ-গেট ও পরিবর্তন

- একটি বর্তমান, অপঠনযোগ্য `CHECKS-LOG.txt` একটি কঠোর শুধু-পঠন গেট।
- নির্বাচন বা পরিবর্তনের আগে: `CHECKS-REG.md`, প্রজেক্ট-রেজিস্টার, সিদ্ধান্ত, প্রয়োজে Fable-Plan, লক, দ্বন্দ্ব-কপি ও লাইভ অবস্থা যাচাই করুন।
- BACH/BYUM-হোল্ড ও মেয়াদোত্তীর্ণ হওয়ার বিষয় শুধুমাত্র `fc_get_time` দিয়ে প্রমাণ করুন।
- OneDrive-এ নেভিগেশন, পঠন, মেটাডেটা, চেকসাম, ক্লাউড-লক ও কার্যকরকরণের জন্য FileCommander ব্যবহার করুন। লেখার আগে সংকীর্ণভাবে লক করুন, অন্যের লক ও পরিবর্তন রক্ষা করুন, শেষে কেবল নিজের লকটি সরান।
- পণ্য/বিষয়গত সিদ্ধান্ত, কুলডাউন, অনুপস্থিত ক্যানোনিকাল ক্লোন, পুনরুৎপাদন গেট এবং ব্যবহৃত একবারের অনুমোদন স্বয়ংক্রিয়ভাবে এড়িয়ে যাবেন না।

## প্রমাণ, দাবি, কম্পিউট ও প্রকাশনার নিয়মাবলি

- স্থানীয় `.WISSEN`-ফলাফল প্রথম দিকে ব্যবহার করুন, এরপর বৈজ্ঞানিক বক্তব্য প্রাথমিক উৎসের সাথে যাচাই করুন। বাক্য/অনুচ্ছেদ/পৃষ্ঠা, পূর্বশর্ত, স্বাভাবিকীকরণ ও অবজেক্ট-টাইপ নির্দিষ্টভাবে যুক্ত করুন; পরিবর্তনশীল অনুসন্ধানের তারিখ লিখুন।
- PDF কেবল `%PDF-`, পঠনযোগ্য পৃষ্ঠা-সংখ্যা/টেক্সট-নিষ্কাশন এবং SHA-256 সহ উৎস হিসেবে নথিভুক্ত করুন। HTML, CAPTCHA, 404 ও প্লেসহোল্ডার ফাইল গণনায় আসবে না।
- পরিমাপ, দীর্ঘমেয়াদি প্রমাণ, অনিশ্চয়তা ও গবেষণা-বিকল্পকে আলাদা রাখুন; কোনো প্রক্সি, প্রি-ফ্লাইট, রিভিউ বা আংশিক রানকে বৈজ্ঞানিক দাবিতে উন্নীত করবেন না।
- জার্মান এন্ড-ইউজার আর্টিফ্যাক্টে প্রকৃত উমলাউট (ä, ö, ü, ß) ব্যবহার করুন। EN/DE এবং কেবল তখনই একটি সম্মিলিত আর্টিফ্যাক্ট যাচাই করুন যখন বর্তমান পাইপলাইন তা অনুমতি দেয়: গঠন, গ্রন্থপঞ্জি, বিল্ড, নিষ্কাশন ও এনকোডিং।
- কম্পিউট কেবল লাইভ `.COMPUTE`-/প্রজেক্ট-চুক্তি ও প্লেসমেন্ট-নিয়ম অনুযায়ী। সুস্পষ্ট কর্তৃত্ব ছাড়া দীর্ঘ ল্যাপটপ-রান, পুনরায় চেষ্টা, ধারাবাহিকীকরণ, কিউ-পরিবর্তন বা ব্যবহৃত একবারের রান করবেন না। টাইমআউট/ইনফ্রা-ত্রুটি গাণিতিক নেতিবাচক ফলাফল নয়।
- আপলোড, পাবলিক-সুইচ, সাবমিট, রেজিস্ট্রি-বুকিং ও রিলিজ আলাদা ব্যবহারকারী-গেট। প্রস্তুতি ও ড্রাই-রান প্রকাশনা নয়।
- সমাপ্তি কেবল প্রয়োজনীয় টেস্ট/বিল্ড, আর্টিফ্যাক্ট-রিডব্যাক, প্রজেক্ট ও রুট-রেজিস্টার, প্রয়োজে অটোমেশন-মেমরি/হ্যান্ডঅফ এবং নিজস্ব অস্থায়ী লক অপসারণের পরে হবে। অবশিষ্ট গেটগুলো স্পষ্টভাবে উল্লেখ করুন।

## ঐচ্ছিক সাহিত্য-সহায়ক

নিম্নোক্ত Python-মডিউলগুলো শুধুমাত্র স্ট্যান্ডার্ড লাইব্রেরি ব্যবহার করে (`urllib`, `xml`, `json`)। এগুলো অনুসন্ধান ও রিভিউয়ে সহায়তা করে, তবে উপরের কোনো কর্তৃত্ব বা প্রমাণ-যাচাইয়ের স্থলাভিষিক্ত নয়।

## আর্কিটেকচার

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

## Python লাইব্রেরি হিসেবে ব্যবহার

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

## CLI হিসেবে ব্যবহার

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## ডেটা উৎস

| উৎস | API | হার সীমা | অ্যাক্সেস |
|--------|-----|------------|--------|
| PubMed | NCBI E-utilities | 3/সেকেন্ড (কী ছাড়া), 10/সেকেন্ড (কী সহ) | বিনামূল্যে |
| arXiv | Atom REST API | কোনো নথিভুক্ত সীমা নেই | বিনামূল্যে |

সম্প্রসারণযোগ্য: নতুন উৎসগুলো `sources/base.py` থেকে `Source` ABC বাস্তবায়ন করে।

## সম্প্রসারণ

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

## BACH-নোট

> কেবল BACH-এর মধ্যে ব্যবহার করা হলে প্রাসঙ্গিক।

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## পরিবর্তন-লগ

### 0.2.0 (2026-08-22)
- সাধারণ অনুসন্ধান-স্ক্রিপ্টের আগে প্রজেক্ট ও পাইপলাইনের কর্তৃত্ব প্রতিষ্ঠিত
- লাইভ-গেট, OneDrive/লক-নিয়ম ও কারেন্ট-পয়েন্টার যুক্ত
- প্রাথমিক উৎস/PDF প্রমাণ, দাবির সীমা ও দ্বিভাষিক যাচাই যুক্ত
- কম্পিউট, আপলোড, রেজিস্টার ও ক্লোজআউট গেট ফেইল-ক্লোজড হিসেবে নির্ধারিত

### 0.1.0 (2026-03-12)
- MODULAR_AGENTS/ResearchAgent থেকে স্কিল লাইব্রেরিতে স্থানান্তর
- PubMed + arXiv উৎস
- QuickSearch + LiteratureReview ওয়ার্কফ্লো
