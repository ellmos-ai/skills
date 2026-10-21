---
name: game-design
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Como o desenvolvimento de jogos funciona como processo — funções, subtarefas, fluxos de trabalho e descrições de funções, especialmente (mas não só) para Roblox. Use esta skill quando se tratar da ORGANIZAÇÃO do desenvolvimento de jogos e não de código concreto: Quais funções existem (Creative Director, Engineer, Artist, Polish/Audio, Business, QA-Tester, Game Critic)? Quem faz qual subtarefa? Como é uma cadeia de desenvolvimento (conceito → backend → frontend → polimento → teste)? Como se escreve um Game Design Document / KONZEPT.md? Como vários agentes (de IA) dividem um jogo? Também acione com \"planejar um novo jogo\", \"criar Game Design Document\", \"de quais funções preciso para o meu jogo\", \"fluxo de desenvolvimento de um jogo\", \"quem testa o jogo\", \"estruturar uma ideia de jogo\", \"gênero/monetização no Roblox\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [game-design, roblox, rollen, workflow, gdd, konzept, monetarisierung, qa, gamedev]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/game-design/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: e21ae8c9208280a65f748fd252d86404a38bd12ad05bb53c5f6b0531c56b0720
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.297618+00:00"
---
<img src="banner.png" width="100%" alt="game-design banner">

# Game Design — Funções, Subtarefas & Fluxos de Trabalho

## Finalidade

O desenvolvimento de jogos é trabalho em equipe a partir de disciplinas claramente separadas — mesmo quando uma única pessoa ou um agente de IA assume várias delas. Esta skill fornece o **modelo organizacional**: quais funções existem, quais subtarefas fazem parte delas, em que ordem interagem e como um jogo é registrado como conceito (GDD). Para o *como técnico*, veja `/rojo` (Sync), `/rbx-studio` (Editor/Assets) e a metaskill `/rbx-dev` (Arquitetura).

Use esta skill ao planejar um novo jogo, ao dividir o trabalho (também entre vários agentes de IA) e ao escrever/revisar um Game Design Document.

## As Funções (5 de desenvolvimento + 2 de teste)

Uma divisão de funções compacta e comprovada. Descrições completas com todas as subtarefas:
[`references/roles-and-workflows.md`](references/roles-and-workflows.md).

| Função | Foco | Subtarefas principais |
| --- | --- | --- |
| **Creative Director** | O QUE & POR QUE & PARA QUEM | GDD/KONZEPT, projetar e balancear mecânicas, priorização/Sprints, história, fluxo de UX |
| **Engineer** | COMO (técnico) | Código de servidor/cliente/compartilhado, game loop, rede/Remotes, DevOps (Rojo, build), correção de bugs |
| **Artist** | como o mundo se parece | Construção de mundo/níveis, iluminação & atmosfera, partículas, obtenção de assets (incl. verificação de malware) |
| **Polish / Audio** | como ele se sente & soa | SFX/música/ambiente, animações, polimento de UI/UX, "Juice" (screen-shake, hit-stop), feedback |
| **Business** | para fora | Página na loja, ícone/miniatura, monetização (Gamepass/Products/Pass), analytics, comunidade |
| **QA-Tester** | tecnicamente correto? | Varreduras de bugs no código, playtests + verificação do console, relatórios reproduzíveis, regressão, desempenho |
| **Spielkritiker** | é divertido? | Primeira/longa impressão do ponto de vista do jogador, avaliação honesta (diversão, clareza, justiça), sugestões |

**Regra básica:** Desenvolvimento e teste são funções **separadas** — idealmente pessoas ou agentes
distintos. Quem escreve o código não o testa de forma objetiva. O crítico de jogos pode ser duro.

## Fluxos de Trabalho (cadeias de desenvolvimento)

O trabalho flui como uma cadeia de função para função. Os padrões mais importantes:

**Cadeia padrão de funcionalidade:**
```
Creative Director (plant Feature) → Engineer (Backend) → Artist (Frontend/Assets)
→ Polish/Audio (Sound + Feinschliff) → QA-Tester (technischer Test)
→ Spielkritiker (Spielerperspektive) → Creative Director (Feedback → nächste Iteration)
```

**Cadeia de correção rápida:** QA-Tester (bug) → Engineer (correção) → QA-Tester (verificado).

**Cadeia de assets:** Artist (busca na loja) → Artist (verificação de malware) → Artist (integração) → QA (visual).

**Cadeia de polimento:** Spielkritiker (fraqueza) → Polish/Audio → Artist → Spielkritiker (nova verificação).

**Humano no loop:** [cadeia de agentes] → testador humano → Creative Director (feedback) → [cadeia].

Cada iteração deve deixar um changelog curto. Condição de parada: orçamento de tempo atingido **ou** meta de qualidade cumprida.

### Testes baseados em personas

Um jogo só sobrevive se jogadores muito diferentes conseguirem usá-lo. Teste, portanto (também
simulado por agentes), a partir de várias **personas** em vez de apenas do seu próprio ponto de
vista — variando por idade, experiência, plataforma (PC/Mobile/Tablet/Console), capacidade de atenção,
idioma e acessibilidade. Exemplos: uma criança casual de 9 anos num tablet, que só quer apertar botões;
um jogador core de 12 anos no PC, que procura a meta; um iniciante de 60+ anos que precisa de botões
grandes. Os testes com personas devem ser **cegos** (o testador não conhece a intenção do design).

## Game Design Document (KONZEPT.md)

Registre cada jogo num GDD conciso — modelo:
[`assets/KONZEPT_template.md`](assets/KONZEPT_template.md). Estrutura mínima:

- **Visão** — 1–2 frases: o que é o jogo?
- **Gênero / Referência** — classificação + títulos de referência.
- **Mecânicas centrais** — **no máx. 3–4** (o foco força a qualidade).
- **Game loop** — o ciclo minuto a minuto do jogador.
- **Modos de jogo / formatos de tempo** — se relevante.
- **Monetização** — Gamepasses, Developer Products, Battle Pass, loja.
- **Técnica** — stack (Rojo/frameworks), arquitetura geral.
- **Próximos passos** — checklist de implementação.
- **Bugs conhecidos / pontos em aberto**.

## Divisão de trabalho entre múltiplos agentes

Vários agentes de IA (ou humano+IA) podem dividir um jogo — dois modos:

- **Enxame** — mesma tarefa, áreas diferentes (ex.: três agentes balanceiam cada um um sistema).
- **Equipe** — funções diferentes, coordenadas entre si (Engineer + Artist + Polish em paralelo em
  uma funcionalidade, coordenados pelo Creative Director).

Comprovado na prática: desenvolvimento e teste **nunca** para o mesmo agente; fixar prompts de função
por papel (prompt de sistema = descrição da função); cada iteração da cadeia termina com changelog +
relatório de testes; o humano permanece como portão de qualidade.

## Contexto de mercado específico do Roblox (orientação)

Conhecimento da plataforma que ancora o trabalho conceitual para o Roblox (sem garantia, apenas regras práticas):

- **Gêneros lucrativos:** Simulator, RPG, Tycoon, Horror, Obby — escalas e esforços muito diferentes.
- **Nichos pouco atendidos (mais risco, menos concorrência):** estratégia/RTS-Lite de verdade,
  jogos esportivos de alta qualidade, Cozy/Life-Sim, quebra-cabeças/escape cooperativos, Auto-Battler.
- **Regras de ouro de monetização:** (1) LiveOps é obrigatório (atualizações a cada 2–4 semanas),
  (2) a monetização deve *apoiar* a jogabilidade, não bloqueá-la, (3) design social (trocas,
  cooperação) é infraestrutura, (4) Mobile-First (50 %+ jogam pelo celular), (5) aptidão para criadores
  de conteúdo (YouTube/TikTok) é marketing.

> Para números de mercado atuais e confiáveis, pesquise em vez de estimar — os pontos acima são
> heurísticas estáveis, não dados ao vivo.

## Leitura complementar

- Skills irmãs: `/rojo`, `/rbx-studio`; metaskill `/rbx-dev` (padrões de arquitetura,
  estrutura de projeto, lições de Luau).
- Pipeline de referência (se existir): `<your Roblox project pipeline>` (`AGENT_ROLES.md`, `GUIDE.md`,
  `IDEAS.md`, análises de mercado).

## Changelog

### 1.0.0 (2026-06-17)
- Versão inicial. Framework genérico de funções/fluxos de trabalho, destilado de `.ROBLOX/AGENT_ROLES.md`
  & `GUIDE.md`, neutro em relação ao usuário (sem portfólio específico de projeto).

## Skills Relacionadas

- `roblox-team-lock` — Reivindicações de arquivos, Studio e MCP, assim que vários agentes trabalham no mesmo projeto. Ler primeiro, reivindicar depois, trabalhar, depois liberar.
