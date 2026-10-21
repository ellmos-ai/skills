---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "Use quando o usuário quiser enviar o mesmo prompt para vários LLMs e comparar as respostas - sequencialmente (cronômetro, medição limpa por faixa) ou em paralelo (corrida real), com repetições opcionais por modelo, avaliadas pelo modelo inicial quanto a qualidade, correção, completude, fidelidade às instruções e latência (o tempo é apenas uma dimensão). Dispara com /compare-race, 'model race', 'vergleiche modelle', 'gleicher prompt an mehrere modelle', 'comparar modelos', 'mesmo prompt para vários modelos', 'corrida de modelos'."
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: pt
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — Skill de Ponteiro (Alemão)

> **Esta skill é um ponteiro puro. A fonte da verdade é o módulo.**

## Caminho do módulo

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

Repositório: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## Instrução ao agente

1. Leia o prompt de papel **`prompts/RACE-STARTER.de.md`** na pasta do módulo e siga-o.
   Você é o RACE-STARTER — e, por padrão, também o **Judge** (decisão do usuário
   2026-08-16).
2. Verifique a configuração (`compare-race config`; configuração do host em `~/.compare-race/`).
   Escolha o modo: `sequential` = cronômetro (medição individual limpa por faixa) ·
   `parallel` = corrida real. **O cronômetro é apenas uma imagem** — o tempo é uma
   dimensão entre qualidade, correção, completude, fidelidade às instruções e custo.
3. Inicie a corrida (`compare-race run --prompt-file …`); sem coma, siga o
   caminho manual por modelo via `compare-race record`.
4. Como Judge, preencha a rubrica em `RACE.md` da pasta da corrida — leia cada
   arquivo RUN você mesmo; aponte a parcialidade se o próprio modelo estiver participando.
5. Disciplina de eixos: atribua resultados somente quando exatamente um eixo variar
   (model = corrida · run = variância · time = deriva do modelo).

## Aviso de cota

As corridas consomem a cota de **cada** provedor envolvido (claude/codex/agy/kimi). Antes
de corridas grandes (muitas faixas × repetições), pergunte ao usuário.
