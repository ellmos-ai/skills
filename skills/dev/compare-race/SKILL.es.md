---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "Úsalo cuando el usuario quiera enviar el mismo prompt a varios LLM y comparar las respuestas: de forma secuencial (cronómetro, temporización limpia por carril) o en paralelo (carrera real), con repeticiones opcionales por modelo, evaluado por el modelo de inicio según calidad, corrección, completitud, fidelidad a las instrucciones y latencia (el tiempo es solo una dimensión). Se activa con /compare-race, 'model race', 'compara modelos', 'envía el mismo prompt a varios modelos'."
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: es
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.395008+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — Skill de puntero (alemán)

> **Este skill es un puntero puro. La fuente de verdad es el módulo.**

## Ruta del módulo

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

Repositorio: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## Instrucción para el agente

1. Lee el prompt de rol **`prompts/RACE-STARTER.de.md`** en la carpeta del módulo y sigue sus indicaciones.
   Eres el RACE-STARTER y, por defecto, también el **Judge** (decisión del usuario
   del 2026-08-16).
2. Revisa la configuración (`compare-race config`; configuración del host en `~/.compare-race/`).
   Elige el modo: `sequential` = cronómetro (medición individual limpia por carril) ·
   `parallel` = carrera real. **El cronómetro es solo una imagen**: el tiempo es una dimensión
   junto a la calidad, la corrección, la completitud, la fidelidad a las instrucciones y el coste.
3. Inicia la carrera (`compare-race run --prompt-file …`); sin el módulo coma, sigue el
   camino manual por modelo a través de `compare-race record`.
4. Como Judge, completa la rúbrica en `RACE.md` de la carpeta de la carrera; lee tú mismo
   cada archivo RUN; indica el sesgo si tu propio modelo participa en la carrera.
5. Disciplina de ejes: atribuye resultados solo cuando varía exactamente un eje
   (model = carrera · run = variación · time = deriva del modelo).

## Advertencia de cuota

Las carreras consumen cuota en **cada** contingente implicado (claude/codex/agy/kimi). Antes
de carreras grandes (muchos carriles × repeticiones), pregunta al usuario.
