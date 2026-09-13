---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: Use when the user wants to send the same prompt to several LLMs and compare the answers - sequentially (stopwatch, clean per-lane timing) or in parallel (true race), with optional repetitions per model, judged by the starting model across quality, correctness, completeness, instruction fidelity and latency (time is only one dimension). Triggers on /compare-race, 'model race', 'compare models', 'same prompt to several models'.
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: en
status: active
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Execution layer for compare-race run (spawn/polling/file protocol)', 'note': 'Optional. Without coma the model-manual path applies: run each lane yourself and file it with compare-race record.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.en.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — pointer skill (English)

> **This skill is a pure pointer. The module is the source of truth.**

## Module path

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

Repo: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## Instruction to the agent

1. Read the role prompt **`prompts/RACE-STARTER.en.md`** in the module folder and
   follow it. You are the RACE-STARTER — and by default also the **judge** (user
   decision 2026-08-16).
2. Check the config (`compare-race config`; host config under `~/.compare-race/`).
   Pick the mode: `sequential` = stopwatch (clean per-lane timing) · `parallel` =
   true race. **The stopwatch is only a picture** — time is one dimension beside
   quality, correctness, completeness, instruction fidelity and cost.
3. Start the race (`compare-race run --prompt-file …`); without coma take the
   model-manual path via `compare-race record`.
4. As the judge, fill the rubric in the race folder's `RACE.md` — read every RUN
   file yourself; name your bias if your own model runs a lane.
5. Axis discipline: attribute only when exactly one axis varies
   (model = the race · run = variance · time = model drift).

## Quota warning

Races cost on **every** participating quota (claude/codex/agy/kimi). Ask the user
before large races (many lanes × repetitions).
