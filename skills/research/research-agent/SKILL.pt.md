---
name: research-agent
version: 0.2.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-08-22
description: "Pipeline de pesquisa com prioridade ao projeto, com gates ao vivo, evidências de fonte/PDF, limites de afirmações, controles de computação e publicação; inclui um auxiliar opcional de PubMed/arXiv com biblioteca padrão."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [research-pipeline, evidence, pdf-validation, publication-gates, pubmed, arxiv, literature-review, science]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e74f1bcd5fddbcf7f172c542aa7b2f9923b36a747d62029ad34864fa04df30c6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
---
<img src="banner.png" width="100%" alt="research-agent banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# Research Agent (Deutsch)

Esta versão é a origem central do pacote. Dentro de `<OneDrive>/.TOPICS/.RESEARCH`, o projeto atual e a pipeline de pesquisa atual valem como autoridade; o código PubMed/arXiv incluído é apenas uma ferramenta opcional de pesquisa.

## Cadeia de autoridade vinculante

1. Pedido atual do usuário e regras globais de `AGENTS.md`, `GPT.md` e `CLAUDE.md`.
2. Arquivos atuais locais do projeto, estado ao vivo, locks, decisões e registros. Continuações numeradas e ponteiros atuais explícitos têm precedência sobre seus predecessores; arquivos e cópias em conflito não devem tornar-se silenciosamente autoridade substituta.
3. Pipeline ao vivo na raiz de pesquisa: em especial `CLAUDE.md`, `START*`, `MASTER*`, `POLICY*`, `PUBLIKATIONSVERFAHREN.md`, `QUALITY_RULES*`, ponteiros atuais de status/TODO, bem como `CHECKS-LOG.txt` e `CHECKS-REG.md`.
4. Esta skill e seus scripts genéricos de busca.

No início, devem ser lidos `~/.codex/GPT.md`, os dois arquivos globais `CLAUDE.md`, as regras de pesquisa e os arquivos atuais locais do projeto `KONZEPT*`, de plano, `TODO*`, `BEWEISNOTIZ*`, decisão, publicação e bibliografia. Em caso de contradição, aplica-se fail-closed.

## Gates ao vivo e mutações

- Um `CHECKS-LOG.txt` atual ilegível é um gate rígido somente leitura.
- Antes de seleção ou alteração: verificar `CHECKS-REG.md`, registro do projeto, decisões, quando houver plano Fable, locks, cópias de conflito e estado ao vivo.
- Holds e expiração de BACH/BYUM devem ser comprovados exclusivamente com `fc_get_time`.
- No OneDrive, usar FileCommander para navegação, leituras, metadados, checksums, locks de nuvem e execução. Antes de gravações, aplicar lock restrito, preservar locks e alterações alheias, e ao final remover apenas o próprio lock.
- Decisões de produto/de domínio, cooldowns, clones canônicos ausentes, gates de reprodução e liberações únicas já consumidas não devem ser contornados de forma autônoma.

## Regras de evidência, afirmação, computação e publicação

- Usar cedo os achados locais de `.WISSEN`; depois, verificar afirmações científicas em fontes primárias. Vincular exatamente frase/seção/página, pressupostos, normalização e tipo de objeto; datar consultas voláteis.
- PDFs só contam como fontes após `%PDF-`, número de página legível/extração de texto e SHA-256. Arquivos HTML, CAPTCHA, 404 e de placeholder não contam.
- Separar medição, evidência de longo prazo, incerteza e opção de pesquisa; não elevar proxy, preflight, revisão ou execução parcial a afirmação científica.
- Artefatos finais em alemão devem usar umlauts reais. Verificar EN/DE e só verificar um artefato combinado se a pipeline atual o permitir: estrutura, bibliografia, build, extração e codificação.
- Computação exclusivamente conforme o contrato ao vivo de `.COMPUTE`/projeto e as regras de placement. Sem execuções longas em laptop, retries, continuações, alterações de fila ou execuções únicas já consumidas sem autoridade explícita. Timeout/falha de infraestrutura não é resultado matemático negativo.
- Upload, troca para público, submissão, registro e release são gates de usuário separados. Preparação e dry-run não são publicação.
- Encerramento somente após testes/builds necessários, releitura de artefatos, registros do projeto e da raiz, quando aplicável, memória de automação/handoff, e remoção dos próprios locks temporários. Gates restantes devem ser declarados explicitamente.

## Auxiliar opcional de literatura

Os módulos Python a seguir usam exclusivamente a biblioteca padrão (`urllib`, `xml`, `json`). Eles apoiam busca e revisão, mas não substituem nenhuma das verificações de autoridade ou evidência acima.

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

| Fonte | API | Limite de taxa | Acesso |
|--------|-----|------------|--------|
| PubMed | NCBI E-utilities | 3/s (sem chave), 10/s (com chave) | Gratuito |
| arXiv | Atom REST API | Nenhum documentado | Gratuito |

Extensível: novas fontes implementam a ABC `Source` de `sources/base.py`.

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

> Relevante apenas quando usado dentro do BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```


## Änderungsprotokoll

### 0.2.0 (2026-08-22)
- Autoridade de projeto e pipeline ancorada antes dos scripts genéricos de busca
- Gates ao vivo, regras de OneDrive/locks e ponteiros atuais incluídos
- Comprovantes de fonte primária/PDF, limites de afirmação e verificações bilíngues acrescentados
- Gates de computação, upload, registro e encerramento fixados de forma fail-closed

### 0.1.0 (2026-03-12)
- Migração de MODULAR_AGENTS/ResearchAgent para a biblioteca de skills
- Fontes PubMed + arXiv
- Fluxos QuickSearch + LiteratureReview
