---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "Utiliser lorsque l'utilisateur souhaite envoyer le même prompt à plusieurs LLM et comparer les réponses — séquentiellement (chronomètre, mesure propre par voie) ou en parallèle (course réelle), avec répétitions optionnelles par modèle, évalué par le modèle de départ selon la qualité, l'exactitude, l'exhaustivité, la fidélité aux instructions et la latence (le temps n'est qu'une dimension). Déclenché par /compare-race, « model race », « compare les modèles », « envoie le même prompt à plusieurs modèles »."
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: fr
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.411669+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — Skill pointeur (allemand)

> **Ce skill est un pur pointeur. La source de vérité est le module.**

## Chemin du module

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

Dépôt : [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## Instruction pour l'agent

1. Lis le prompt de rôle **`prompts/RACE-STARTER.de.md`** dans le dossier du module et suis-le.
   Tu es le RACE-STARTER — et par défaut aussi le **Judge** (décision de l'utilisateur
   du 2026-08-16).
2. Vérifie la configuration (`compare-race config` ; configuration de l'hôte sous `~/.compare-race/`).
   Choisis le mode : `sequential` = chronomètre (mesure individuelle propre par voie) ·
   `parallel` = course réelle. **Le chronomètre n'est qu'une image** — le temps est une dimension parmi la qualité, l'exactitude, l'exhaustivité, la fidélité aux instructions et le coût.
3. Lance la course (`compare-race run --prompt-file …`) ; sans le module coma, passe par la voie
   manuelle par modèle via `compare-race record`.
4. En tant que Judge, remplis la grille dans `RACE.md` du dossier de course — lis toi-même chaque fichier RUN ; signale tout parti pris si ton propre modèle participe à la course.
5. Discipline des axes : n'attribue une cause que si un seul axe varie
   (model = course · run = variance · time = dérive du modèle).

## Avertissement de quota

Les courses consomment le quota de **chacun** des contingents impliqués (claude/codex/agy/kimi). Avant
les grandes courses (nombreuses voies × répétitions), demande confirmation à l'utilisateur.
