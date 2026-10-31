---
name: research-agent
version: 0.2.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-08-22
description: "خط أنابيب بحث يبدأ من المشروع مع بوابات مباشرة وأدلة من المصدر وPDF وحدود للادعاءات وضوابط للحوسبة والنشر؛ يتضمن مساعدًا اختياريًا لـ PubMed/arXiv بمكتبة قياسية فقط."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [research-pipeline, evidence, pdf-validation, publication-gates, pubmed, arxiv, literature-review, science]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e74f1bcd5fddbcf7f172c542aa7b2f9923b36a747d62029ad34864fa04df30c6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:53.391636+00:00"
---
<img src="banner.png" width="100%" alt="research-agent banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# Research Agent (Deutsch)

تمثل هذه النسخة أصل الحزمة المركزي. ضمن `<OneDrive>/.TOPICS/.RESEARCH` يُعد خط أنابيب المشروع والبحث الحالي السلطة المعتمدة؛ أما شيفرة PubMed/arXiv المرفقة فهي أداة بحث اختيارية فقط.

## سلسلة السلطة الملزمة

1. طلب المستخدم الحالي وقواعد `AGENTS.md`-/`GPT.md`-/`CLAUDE.md` العامة.
2. الملفات الحالية المحلية للمشروع، والحالة المباشرة، وأقفال الملفات، والقرارات، والسجلات. تتقدم المتابعات المرقمة والمؤشرات الحالية الصريحة على أسلافها؛ ولا تُعامل الأرشيفات ونسخ التعارض دون تصريح كسلطة بديلة.
3. خط الأنابيب المباشر في جذر البحث: ولا سيما `CLAUDE.md` و`START*` و`MASTER*` و`POLICY*` و`PUBLIKATIONSVERFAHREN.md` و`QUALITY_RULES*`، ومؤشرات الحالة/المهام الحالية، إضافةً إلى `CHECKS-LOG.txt` و`CHECKS-REG.md`.
4. هذه المهارة وسكربتات البحث العامة التابعة لها.

في البداية يجب قراءة `~/.codex/GPT.md`، والملفان العامان `CLAUDE.md`، وقواعد البحث، وملفات `KONZEPT*` والخطة و`TODO*` و`BEWEISNOTIZ*` والقرارات والنشر وقوائم المراجع الحالية الخاصة بالمشروع. عند وجود تعارضات يُعتمد مبدأ الإغلاق عند الفشل (fail-closed).

## البوابات المباشرة والتعديلات

- يُعد ملف `CHECKS-LOG.txt` الحالي غير القابل للقراءة بوابةً صارمة للقراءة فقط.
- قبل الاختيار أو التعديل: التحقق من `CHECKS-REG.md` وسجل المشروع والقرارات وخطة Fable عند وجودها والأقفال ونسخ التعارض والحالة المباشرة.
- إثبات حالات الإيقاف والانتهاء الخاصة بـ BACH/BYUM حصريًا عبر `fc_get_time`.
- في OneDrive يُستخدم FileCommander للتنقل والقراءة والبيانات الوصفية والمجاميع الاختبارية وأقفال السحابة والتنفيذ. قبل الكتابة يُطبَّق قفل ضيق، وتُحفظ الأقفال والتغييرات التي يملكها الآخرون، وفي النهاية تُزال فقط القفلة الخاصة بالعملية نفسها.
- لا تُتجاوز بشكل مستقل قرارات المنتج أو القرارات الموضوعية، ولا فترات التهدئة، ولا النسخ المرجعية المفقودة، ولا بوابات إعادة الإنتاج، ولا الموافقات لمرة واحدة التي استُهلكت.

## قواعد الأدلة والادعاءات والحوسبة والنشر

- تُستخدم نتائج `.WISSEN` المحلية مبكرًا، ثم تُتحقق الادعاءات العلمية لاحقًا من المصادر الأولية. يجب ربط الجملة أو القسم أو الصفحة والشروط المسبقة والتطبيع ونوع الكائن بدقة، وتأريخ الاستعلامات المتقلبة.
- لا تُعد ملفات PDF مصادر إلا بعد التحقق من `%PDF-`، ورقم الصفحة القابل للقراءة واستخراج النص، وSHA-256. لا تُحتسب ملفات HTML ولا CAPTCHA ولا صفحات 404 ولا الملفات النائبة.
- يُفصل القياس والأدلة طويلة الأمد وعدم اليقين وخيار البحث؛ ولا تُرفع بروكسي أو فحص أولي أو مراجعة أو تشغيل جزئي إلى مستوى ادعاء علمي.
- تستخدم المخرجات الألمانية الموجهة للمستخدم النهائي حروف العلة (Umlaute) الصحيحة. تُراجع النسختان الإنجليزية والألمانية، وتُراجع النسخة المدمجة فقط عندما تسمح بها خط الأنابيب الحالي: البنية وقائمة المراجع والبناء والاستخراج والترميز.
- تُنفذ الحوسبة حصريًا وفق عقد `.COMPUTE` المباشر/عقد المشروع وقواعد التموضع (Placement). لا تُشغَّل تشغيلات طويلة على الحاسوب المحمول، ولا تُعاد المحاولات، ولا تُستأنف العمليات، ولا تُغيَّر قوائم الانتظار، ولا تُعاد التشغيلات الأحادية المستهلكة دون سلطة صريحة. مهلة التنفيذ أو خطأ البنية التحتية ليس نتيجة سلبية رياضية.
- الرفع والنشر العام والتقديم وحجز السجل والإصدار بوابات منفصلة للمستخدم. التحضير والتجربة الجافة ليسا نشرًا.
- لا يُعد الإنجاز مكتملًا إلا بعد تنفيذ الاختبارات والبناءات المطلوبة، وإعادة قراءة الملفات الناتجة، وتحديث سجلات المشروع والجذر، وعند الاقتضاء ذاكرة الأتمتة والتسليم، وإزالة الأقفال المؤقتة الخاصة بالعملية. وتُذكر البوابات المتبقية صراحةً.

## مساعد الأدبيات الاختياري

تستخدم وحدات Python التالية المكتبة القياسية فقط (`urllib` و`xml` و`json`). تدعم البحث والمراجعة، لكنها لا تحل محل أي من فحوصات السلطة أو الأدلة المذكورة أعلاه.

## Architecture

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


## Usage as Python Library

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


## Usage as CLI

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```


## Data Sources

| Source | API | Rate Limit | Access |
|--------|-----|------------|--------|
| PubMed | NCBI E-utilities | 3/s (without key), 10/s (with key) | Free |
| arXiv | Atom REST API | None documented | Free |

قابل للتوسيع: تنفذ المصادر الجديدة الفئة المجردة `Source` من `sources/base.py`.

## Extension

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


## BACH Notes

> ذو صلة فقط عند الاستخدام ضمن BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```


## سجل التغييرات

### 0.2.0 (2026-08-22)
- تثبيت سلطة المشروع وخط الأنابيب قبل سكربتات البحث العامة
- إضافة البوابات المباشرة وقواعد OneDrive/الأقفال ومؤشرات الحالة الحالية
- إضافة أدلة المصادر الأولية وPDF وحدود الادعاءات وفحوص ثنائية اللغة
- تثبيت بوابات الحوسبة والرفع والسجل والإغلاق بمبدأ الإغلاق عند الفشل

### 0.1.0 (2026-03-12)
- الترحيل من MODULAR_AGENTS/ResearchAgent إلى مكتبة المهارات
- مصدرا PubMed وarXiv
- سير عمل QuickSearch وLiteratureReview
