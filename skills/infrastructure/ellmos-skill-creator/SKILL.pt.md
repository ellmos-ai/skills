---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: "Cria ou revisa uma skill PARA ESTE ECOSSISTEMA: delega o ciclo genérico de entrevista/rascunho/avaliação ao plugin oficial skill-creator (Anthropic, Apache-2.0), mas aplica adicionalmente os requisitos ellmos que o plugin oficial não conhece — frontmatter próprio da casa (9 campos), regras de categoria/visibilidade, detecção neutra quanto a fornecedor/usuário/ellmos porém sensível a ellmos via grounding-seed, config.json incluído (incluindo o contrato de aprendizado) + connections.json, consciência de fornecedores/vendors (propor alternativas do estado da arte, incluindo componentes próprios da ellmos), uma seção de autoatualização E um conjunto reutilizável de arquivos de aprendizado/cobertura (user-usecases.json, usecase-gaps.json, known-providers-and-abilities.json, gap-closing-analysis.json — inspirados em evals.json do skill-creator e em A2A/AgentSkill, sem padrão paralelo). SEMPRE usar quando uma skill NOVA para este sistema deve ser criada ou uma existente deve ser adaptada à conformidade ellmos — também em \"crie uma skill\", \"monte uma skill para X\", \"use o skill-creator\", \"criar nova skill\", \"tornar esta skill conforme ellmos\", \"criar contrato de aprendizado/código de comportamento para uma skill\", \"verificar a cobertura de casos de uso de uma skill\". Para apenas ENCONTRAR/ROTEAR skills, use skill-finder; para auditoria da paisagem, use skill-explorer."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: df1b1afd8453bf4a4e39e0edf079608b4b5213e8b1378dcfe731c9e08930061f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.857126+00:00"
---
<img src="banner.png" width="100%" alt="ellmos-skill-creator banner">

# ellmos-skill-creator

## Origem e decisão (fork vs. desenvolvimento próprio)

**Decisão: desenvolvimento próprio, não fork.** Justificativa, para que não se perca:

- `skill-creator` (Anthropic, Marketplace `claude-plugins-official`) está licenciado sob **Apache-2.0**
  (texto da LICENSE lido e verificado no clone, 2026-08-24) — um fork seria juridicamente possível
  e já é o padrão estabelecido no repositório em outros pontos (`skills/third-party/grill-me`, `skills/third-party/grilling`).
- Um fork, porém, arrastaria toda a maquinaria de avaliação/benchmark do original
  (`agents/{analyzer,comparator,grader}.md`, `eval-viewer/`, 7 scripts, SKILL.md de 485 linhas) —
  capacidade que já existe e pode ser chamada diretamente (`Skill: skill-creator:skill-creator`).
  Segundo a regra 4 de `.PLUGINS/CLAUDE.md` ("verificar capacidades antes de reconstruir") e o padrão P10
  ("dois interruptores que ninguém compara"), isso seria uma duplicação, não uma extensão.
- A lacuna real é **puramente específica da ellmos** e basicamente desconhecida do original:
  frontmatter da casa (`templates/SKILL.md`), `docs/CONVENTIONS.md`, neutralidade quanto a fornecedor/usuário/ellmos
  com sensibilidade a ellmos, integração com `grounding-seed`, consciência de vendors, autoatualização.
- Esta skill **não contém texto da Anthropic** (formulação própria em todo o conteúdo) — portanto
  também não aciona a obrigação de atribuição da Apache-2.0 para modificações. Ela **compõe** o original,
  em vez de copiá-lo: isso é ao mesmo tempo o caminho juridicamente mais limpo e o de menor manutenção.

## Quando ativar

- "crie uma skill para X", "montar uma nova skill", "use o skill-creator"
- "torne esta skill conforme ellmos", "adaptar skill ao padrão da casa"
- Sempre que o **destino** for uma skill em `.AI/.SKILLS/skills/…` (ou seu clone canônico Plano-D) — não
  em pedidos gerais, alheios ao ecossistema ("crie qualquer skill do Claude sem relação com isto").

## Procedimento

### Passo 1 — Delegar entrevista/rascunho/avaliação

Chame o `Skill: skill-creator:skill-creator` oficial para: esclarecimento de intenção,
rascunho da estrutura do SKILL.md, casos de teste, ciclo de avaliação,
otimização da description (`scripts/improve_description.py`). **Não reinventar** — esta parte é
genérica e já está bem resolvida no original.

### Passo 2 — Montar o scaffold próprio da ellmos (obrigatório, aditivo ao formato original)

Complemente o SKILL.md gerado pelo original com os nove campos da casa de
`.SKILLS/templates/SKILL.md` (ou `AGENT.md`/`WORKFLOW.md`/`PROMPT.md` conforme o tipo),
leia antes `.SKILLS/docs/CONVENTIONS.md` para as pastas de categoria, a regra flat (<5 arquivos
planos), a convenção de versão (SemVer: MAJOR/MINOR/PATCH) e os conjuntos multilíngues
(núcleo: DE+EN obrigatório). **`visibility` sempre começa em `private-only`** — a publicação
é uma decisão posterior e verificada do usuário (`.AI/VISIBILITY-POLICY.md`), nunca o padrão.
Esses campos são puramente **aditivos** ao formato Anthropic (chaves YAML extras ao lado de
`name`/`description`) — toda skill assim gerada continua totalmente
`anthropic_compatible: true`.

### Passo 3 — Impor os princípios: neutra quanto a fornecedor, neutra quanto ao usuário, neutra quanto à ellmos mas sensível a ellmos

Texto completo e padrões de código: `references/ELLMOS-PRINCIPLES.md`. Resumo: a skill gerada
deve **funcionar sozinha** (traz tudo o que precisa) e **ao mesmo tempo**
usar componentes da ellmos assim que estiverem disponíveis — ela decide isso sozinha em tempo de execução,
nunca de forma fixa. Esse é exatamente o padrão que `grounding-seed` já fornece
(README: "cultivated landscape, not wildflower" / "viable alone, more productive
together") — **nenhum segundo mecanismo de detecção é inventado**; esta skill direciona
as skills produzidas de forma consistente para `grounding_seed.detect_ecosystem()`.

### Passo 4 — Incluir config.json + connections.json

`grounding-seed` já é importável como pacote Python (verificado em 2026-08-24:
`import grounding_seed` resolve com sucesso na árvore de código-fonte do `grounding-seed` clonado localmente,
clone Plano-D) — é o **ponto de encaixe canônico**; não inventar um arquivo novo. Para cada
skill produzida com necessidade externa (programas, serviços, fornecedores):

- **`config.json`** — configurações próprias da skill (modelo: `templates/skill-config.template.json`).
  `grounding_seed.store.LocalStore(root)` usa este nome de arquivo por padrão para seu armazenamento de papéis —
  uma skill produzida pode, portanto, usar seu próprio `config.json` como backend `LocalStore` OU mantê-lo
  separado, caso precise, além de papéis, de configurações puramente comportamentais (então uma segunda instância de `LocalStore(root, filename="connections.json")`).
- **`connections.json`** — os encaixes externos **efetivamente resolvidos** (qual programa/serviço
  foi encontrado, desde quando, com qual origem) — modelo: `templates/skill-connections.template.json`, esquema `ellmos.source-resolver.user-config.v1`
  (idêntico a `source-resolver`; conforme o README do grounding-seed, escolhido deliberadamente para que uma
  futura migração para o `source-resolver` real seja sem perdas — ver `migration.py` ali).

Detalhes, CLI e exemplo de código: `references/ELLMOS-PRINCIPLES.md` seção "Docking".

### Passo 5 — Incluir a consciência de fornecedores/vendors

Texto completo: `references/VENDOR-AWARENESS.md`. Resumo: a skill produzida recebe
uma seção "Fornecedores & alternativas" que (a) cita o(s) fornecedor(es) do estado da arte para o tema
(p. ex., ElevenLabs para TTS), (b) pelo menos um fornecedor substituto, (c) lista **componentes próprios da ellmos
explicitamente como candidatos de mesmo nível** quando cobrirem o tema
(p. ex., `ellmos-voice-io` em vez de, ou além de, ElevenLabs) — e, diante de uma necessidade clara do usuário,
**propõe** instalação/troca, em vez de pressupô-las silenciosamente. Base
para "o que está disponível no sistema": `grounding_seed.scan.scan_resources([...])`
(verifica `shutil.which`) mais `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` para candidatos ellmos.

### Passo 6 — Criar a autoatualização

Texto completo: `references/SELF-UPDATE.md`. Resumo: cada skill produzida recebe
uma seção "Autoatualização" que (a) sugere periodicamente uma breve pesquisa na web
para se manter no estado da arte, (b) conhece skills/fluxos relacionados e nomeia
novas alternativas que possam servir melhor, (c) mantém um pequeno JSON de aprendizado
(modelo: `templates/skill-connections.template.json`, campo `notizen`/`gelernt`), que pode ser transferido para
o componente de memória da ellmos (USMC/Gardener), se disponível, em vez de crescer localmente —
também aqui: detectar em vez de fixar de forma rígida (`grounding_seed.detect_ecosystem()`).

### Passo 6b — Criar o contrato de aprendizado + cobertura de casos de uso (padrão reutilizável)

Texto completo: `references/LEARNING-CONTRACT-AND-COVERAGE.md`. Resumo: não só esta
skill, mas **cada skill que ela produz** recebe um pequeno conjunto reutilizável de arquivos de
aprendizado/cobertura — verificado contra padrões estabelecidos, sem padrão paralelo:

- `evals/evals.json` — **reutilizar**, não duplicar: já é o padrão do skill-creator para
  casos de teste elaborados pelo autor.
- `user-usecases.json` — casos de uso efetivamente trazidos pelo usuário, com a mesma forma
  de `evals.json` (modelo: `templates/user-usecases.template.json`).
- `usecase-gaps.json` — comparação: quais casos de uso do usuário não foram testados/cobertos
  (modelo: `templates/usecase-gaps.template.json`).
- `known-providers-and-abilities.json` — espaço de candidatos de fornecedores conhecidos por papel,
  campos inspirados em A2A/`AgentSkill` (id/name/description/tags), não inventados
  (modelo: `templates/known-providers-and-abilities.template.json`).
- `gap-closing-analysis.json` — caminhos estruturais de fechamento para cada lacuna (módulo ellmos,
  bundle ellmos, módulo de terceiros, reconstrução) — não duplica `grading.json.eval_feedback`
  (modelo: `templates/gap-closing-analysis.template.json`).
- Campo `config.json` em `lernvertrag` — código de comportamento (escolher a melhor opção, **o usuário é o rei**, nunca instalar por conta própria, intervalo de atualização) — deliberadamente como extensão de
  `config.json`, não como um sétimo arquivo.

Esquemas: `.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json` — a mesma convenção da casa de `skill-v1.schema.json`.
`grounding-seed` foi verificado para este conjunto de arquivos e deliberadamente **não** foi estendido
(justificativa em `LEARNING-CONTRACT-AND-COVERAGE.md`) — apenas `connections.json` permanece como parte dele.

### Passo 7 — Registrar, testar, commitar

- Escolher a pasta de categoria segundo `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md`; em caso de dúvida, perguntar a `skill-finder`
  ou `controlcenter_find_skill` se uma família já existe.
- Executar `testing/` (privacy_gate + testes de metadados) antes de commitar.
- Os arquivos de registro (`registry/components.json`, `SKILLS-MAP.md`, `llms.txt`) **não devem ser editados à mão** —
  são gerados (`build_public_registry.py`, `build_skills_map.py`, `catalog.py`). Se uma sessão alheia, ainda não commitada,
  estiver ativa no clone canônico, NÃO regenerar globalmente (isso misturaria alterações alheias e próprias
  em um mesmo arquivo) — em vez disso, commitar isoladamente a nova pasta da skill e deixar a regeneração do registro
  para a próxima execução limpa (`skill-register-care`).
- `git commit -- skills/<kategorie>/<name>/` — apenas os próprios caminhos novos.

## Compatibilidade com o formato Anthropic

Todos os campos adicionais são extensões puramente YAML ao lado de `name`/`description` — um Claude Code padrão, fora
deste ecossistema, continua lendo apenas `name`/`description` e ignora o restante.
`config.json`/`connections.json` são recursos empacotados opcionais (como previsto em
`docs/CONVENTIONS.md`), não uma dependência obrigatória — uma skill sem eles funciona sem alterações.

## Skills relacionadas

- `skill-creator:skill-creator` — ciclo genérico de entrevista/avaliação (delegado, passo 1).
- `skill-finder` — roteador para skills próprias já existentes (verificar ANTES de construir: isso já existe?).
- `skill-explorer` — auditoria da paisagem + pesquisa na web por novas skills/plugins (nível meta:
  o *acervo* de skills; esta skill aqui, em vez disso, torna cada skill *produzida individualmente* consciente de fornecedores).
- `skill-family-care`, `skill-register-care` — manutenção após a construção.
- `grounding-seed` (módulo, `.AI/.MODULES/.CONTROL/grounding-seed`) — a lógica efetiva de encaixe/autoprovisionamento,
  aqui apenas referenciada, não duplicada.

## Changelog

### 0.2.0 (2026-08-24)
- Complemento (ticket T-20260824-218233618, ampliação de escopo): padrão reutilizável de
  aprendizado/cobertura por skill produzida adicionado — `user-usecases.json`,
  `usecase-gaps.json`, `known-providers-and-abilities.json`,
  `gap-closing-analysis.json` (novos esquemas da casa em `.SKILLS/schemas/`) mais o
  campo de contrato de aprendizado em `config.json`. `evals/evals.json` (skill-creator) deliberadamente
  reutilizado em vez de duplicado. `grounding-seed` verificado — nenhuma extensão
  necessária (justificativa em `references/LEARNING-CONTRACT-AND-COVERAGE.md`), portanto
  nenhum ticket de acompanhamento. Nomes de campos para catálogos de fornecedores inspirados no protocolo A2A (`AgentSkill`)
  em vez de vocabulário próprio.

### 0.1.0 (2026-08-24)
- Versão inicial. Decisão de desenvolvimento próprio em vez de fork tomada e justificada (ticket
  T-20260824-218233618). Delega a criação genérica de skills ao
  `skill-creator:skill-creator`, acrescenta o scaffold da casa, os princípios ellmos,
  a integração `grounding-seed` (config.json/connections.json), a consciência de vendors e a
  autoatualização.
