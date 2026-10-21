---
name: textproduction
version: 2.0.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-09-27
description: "Produção de texto assistida por IA em três subskills: textos gerais (post de blog, redes sociais, newsletter, copy, e-mail, relatório), histórias narrativas (roteiro, conto, RPG, construção de mundos) e comunicação de PR (comunicado de imprensa, documento de posicionamento) com compilador LaTeX-PDF local. Nenhum serviço externo é obrigatório."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: production
tags: [text, blogpost, social-media, newsletter, marketing, email, bericht, copy,
       story, drehbuch, rpg, weltenbau, pressemitteilung, positionspapier, pr, latex]
language: pt
status: active
visibility: public

dependencies:
  tools: [pr/press_compiler.py]
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/agents/_experts/textproduction/ + system/agents/_experts/press/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  origin_license: "MIT"
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: 0ecf524b5455a0991d20fb17dfd48892eaf544f75453f005c4bfa0dc63bdc03f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.977741+00:00"
---
<img src="banner.png" width="100%" alt="textproduction banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **English Translation** — Official English version of `textproduction`.

# Produção de Texto — Roteador (Deutsch)

Esta skill abrange todas as formas de produção textual. Ela encaminha para a
subskill adequada — leia a instrução detalhada na subpasta.

## Tabela de Roteamento

| Subskill | Exemplos de gatilho | Instrução detalhada |
|---|---|---|
| **text** | „Escreva um post de blog", „5 posts para LinkedIn", „Newsletter", „Descrição de produto", „E-mail formal", „Resuma X" | `text/WORKFLOW.md` |
| **storys** | „Escreva um roteiro", „Conto curto", „Criar aventura de RPG", „Ficha de personagem", „Construção de mundo" | `storys/WORKFLOW.md` |
| **pr** | „Redigir comunicado de imprensa", „Documento de posicionamento", „Pacote de PR", „Gerar PDF" | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## Fluxo de Trabalho e Procedimento

```
1. Nutzerwunsch → Routing-Tabelle oben → passenden Teilskill bestimmen.
2. Detail-Anleitung im Unterordner lesen (WORKFLOW.md).
3. Prompt-Muster auswaehlen, Platzhalter fuellen, Text generieren.
4. Qualitaetspruefung (je Teilskill angegeben).
```


## Observações

- **Neutro quanto ao usuário:** Nenhum dado pessoal, chave de API ou dado de conta na skill.
  A configuração (tom, limites de caracteres, dados de contato para PR) cabe ao usuário.
- **Ferramenta de PR:** `pr/press_compiler.py` compila comunicados de imprensa e documentos de posicionamento
  para PDF via LaTeX (pdflatex/xelatex). Configuração única: copiar `pr/config.example.json`
  para `pr/config.json` e preencher os dados de contato.
- Otimização opcional de estilo: DeepL Write (gratuito até 500.000 caracteres/mês).

## Histórico de Alterações

### 2.0.0 (2026-06-22)
- Reestruturação para o padrão de roteador: SKILL.md = ponto de entrada + tabela de roteamento.
- Três subskills: text/ (6 tipos de texto), storys/ (4 formatos narrativos),
  pr/ (comunicado de imprensa + documento de posicionamento + compilador LaTeX-PDF).
- press_compiler.py + templates LaTeX + config.example.json movidos de
  ai-media-editor/production/pr/ para cá (SSOT).
- Referências de skills relacionadas atualizadas para os caminhos internos das subskills.

### 1.0.0 (2026-06-22)
- Versão inicial. Extraída de ai-media-editor/production/text/WORKFLOW.md.
- Proveniência: BACH agents/_experts/textproduction/ (MIT).
