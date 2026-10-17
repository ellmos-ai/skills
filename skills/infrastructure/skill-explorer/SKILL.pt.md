---
name: skill-explorer
version: 1.1.1
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-08-24
description: "Gerencia a sua própria paisagem de skills: faz levantamento e compara skills existentes (modo Audit), pesquisa na web novos skills/plugins (modo Explore) e atua ao mesmo tempo como instalador que gera subskills enxutos (Skill-Finder, umbrella de família, skills de manutenção) em vez de carregar um monólito. Use esta skill para \"comparar/auditar skills\", \"quais skills estão duplicados\", \"formar famílias de skills\", \"limpar/consolidar skills\", \"manter o registro de skills\", \"encontrar skills/plugins para o tema X\", \"instalar novos skills\", \"navegar pelo marketplace de skills\" ou para `/skill-explorer`. Entrega um subrelatório por família e uma lista de decisões numerada globalmente; instala/desinstala somente após uma verificação de segurança e aprovação explícita."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: pt
status: active
visibility: public
dependencies: {'tools': ['git'], 'services': ['websearch'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/skill-explorer/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 290cc943766331f12d02c48949c72ba33065d7b80c835a1d9a3edfa08a17bf21
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="skill-explorer banner">

# Skill-Explorer — Gerenciar a paisagem de skills (Audit · Explore · Instalador)

## Objetivo

Com o crescimento do acervo de skills surgem duplicações, recursos não utilizados e situações pouco claras do tipo "qual skill usar em vez de qual" — e continuamente há novos skills/plugins disponíveis. `skill-explorer` reúne três papéis em uma só ferramenta:

| Papel | O que faz | Detalhe |
| --- | --- | --- |
| **Modo Audit** (para dentro) | examina todos os skills, agrupa-os em famílias, levanta capacidades/dependências/recursos, gera um subrelatório por família + recomendações numeradas | `references/audit-mode.md` |
| **Modo Explore** (para fora) | pesquisa na web (Web/GitHub/Reddit, bilíngue) novos skills/plugins sobre um tema, compara, instala somente com aprovação prévia | `references/explore-mode.md` |
| **Instalador** | *gera* subskills enxutos em vez de um monólito — Skill-Finder, umbrella de família, skills de manutenção | abaixo + `references/family-care.md` |

Chamada: `/skill-explorer` (Audit como padrão) ou "… encontrar para o tema X" (Explore). Ambos os modos compartilham a taxonomia (`references/clustering.md`), o formato de relatório (`references/report-format.md`) e o esquema de numeração, para que o usuário possa responder com uma única lista de números.

## Princípio do instalador e persistência

Em vez de crescer como monólito, `skill-explorer` *gera*, quando necessário, subskills enxutos e carregáveis individualmente — assim nunca é preciso carregar um skill único excessivamente longo:

- **Skill-Finder** ([F]) — localizador/roteador ativo, análogo a um "porteiro" do tipo "using-superpowers", que antes de cada tarefa lê o registro e encaminha para a família adequada (`references/skill-finder.md`, modelo `assets/skill-finder-template.md`).
- **Umbrella de família** (c1) — meta-skill que conhece uma família inteira (`assets/family-umbrella-template.md`).
- **Skills de manutenção** ([P1] famílias, [P2] registro) — mantêm famílias/registro atualizados (`references/family-care.md`).

As decisões são persistidas em `~/.claude/skills/skill-explorer/config.json` (`references/config.md`, modelo `assets/config.example.json`): ler no início (famílias/roteadores/subskills gerados conhecidos), atualizar após a execução — assim uma nova execução não cria nada em duplicata.

## Mecanismo de branch (adaptar terceiros)

Um skill somente leitura (plugin, importado de terceiros) pode ser adaptado sem alterar o original: o diretório original é copiado integralmente (**Branch**); depois, somente a cópia é editada. O branch traz quatro informações obrigatórias: referência ao original, data do branch, responsável e motivo. Assim que o branch substitui o original, o original é desregistrado do runtime (`SKILL.md` → `CONTENT.md`) ou o roteador da família passa a apontar para o branch, para que dois skills quase idênticos não entrem em conflito. Branches de terceiros permanecem **privados** — não entram na biblioteca pública `.AI/.SKILLS`. Detalhe: `references/skill-branching.md`.

## Fluxo

1. **Escolher o modo:** examinar/organizar o acervo → modo Audit. Pesquisar/instalar a partir de fora → modo Explore. (O Explore pode partir de um Audit/`config.json` anterior.)
2. **Modo Audit** (`references/audit-mode.md`): inventário (script) → agrupamento em famílias → subrelatórios → **uma única lista de decisões numerada globalmente** (a/b/c1/c2/c3, além de R/F/P1/P2).
3. **Modo Explore** (`references/explore-mode.md`): pesquisa bilíngue em múltiplas fontes → 3 categorias por candidato → simulação de impacto → recomendações numeradas de instalação/remoção.
4. **Executar** somente após a confirmação numérica do usuário; registrar a criação/alteração de skills e atualizar `config.json`.

## Regras de ferro

- **Levantamento ≠ mutação:** agrupar tudo, mas editar apenas skills **próprios do usuário**; skills de plugin/terceiros são somente leitura (nunca cabeçalho/exclusão). Quem quiser adaptar um skill de terceiros cria, em vez disso, um **branch** (cópia em fork) — o original permanece intocado e a adaptação ocorre somente na cópia (→ `references/skill-branching.md`).
- **Ampliar o registro, não duplicar:** se existe um registro de skills (índice + mapa de famílias + skill índice), amplie-o em vez de criar um quarto.
- **Segurança principalmente manual:** antes de qualquer instalação, o modelo lê o próprio skill e julga; `scripts/scan_skill_security.py` é apenas triagem de apoio, com limites conhecidos. Nunca instalar automaticamente.
- **Registro conforme a origem:** autoria do usuário → biblioteca; terceiros → caminho externo, **não** biblioteca.

## Orquestração (neutra quanto ao modelo)

Subrelatórios de família ou fontes/idiomas são caminhos de trabalho independentes. Se a plataforma oferecer subagentes mais baratos do que o próprio orquestrador, delegue um subagente por família/fonte e atue como orquestrador apenas para consolidar/verificar (enxame de especialistas). Caso contrário, faça sequencialmente por conta própria.

## Recursos

- **Modos:** `references/audit-mode.md`, `references/explore-mode.md`
- **Compartilhados:** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **Audit:** `references/family-care.md`, `references/skill-finder.md`
- **Explore:** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **Branch:** `references/skill-branching.md`
- **Scripts:** `scripts/inventory_skills.py` (inventário), `scripts/inject_family_header.py` (roteador de cabeçalhos),
  `scripts/scan_skill_security.py` (triagem de segurança)
- **Modelos:** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`,
  `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## Histórico de alterações

### 1.1.1 (2026-08-24)
- O auxiliar de inventário agora também aceita mapeamentos `dependencies` antigos, serializados em uma única linha, e trata valores corrompidos de forma tolerante a falhas, em vez de interromper toda a auditoria. Sua mensagem de conclusão também passou a ser compatível com consoles do Windows.

### 1.1.0 (2026-06-17)
- Mecanismo de branch acrescentado: skills de terceiros/somente leitura podem ser adaptados por meio de cópia em fork (branch) — com referência ao original, data, responsável e motivo; o original permanece intocado. A regra de ferro "Levantamento ≠ mutação" foi ampliada com a saída por branch. Nova seção `## Branch-Mechanismus` (no corpo do documento, intitulada «Mecanismo de branch (adaptar terceiros)»). Novos: `references/skill-branching.md`, `assets/branch-header.example.md`.

### 1.0.0 (2026-06-17)
- Versão inicial. Reúne auditoria do acervo (agrupamento em famílias, decisões numeradas) e pesquisa na web (instalação somente com aprovação prévia e triagem de segurança) em um único instalador que gera subskills enxutos.
