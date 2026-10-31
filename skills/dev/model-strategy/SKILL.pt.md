---
name: model-strategy
version: 3.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-10-11
description: "Estratégia multi-modelo baseada em papéis. O catálogo de modelos fica em um arquivo de configuração local em vez de no texto do skill -- papéis (Pensador/Decisor, Worker de longa duração, Gerador de rascunhos, Revisor/Aceitação, Escalonamento), esforço de raciocínio como eixo próprio, obrigatoriedade de aceitação para modelos de rascunho, troca de fornecedor para revisões independentes, cotas, fluxo de delegação e custo/qualidade de workers pequenos."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor, roles]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: cbce54cff40ed3f45c5e4bd4f96e9d402ba6e2b353668b20315bab1d8d648eac
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.907659+00:00"
---
<img src="banner.png" width="100%" alt="model-strategy banner">

# Estratégia de Troca de Modelos

> Estratégia multi-modelo baseada em papéis: configuração em vez de catálogo em texto, papéis em vez de uma tabela de pontuação rígida, aceitação obrigatória para rascunhos, troca de fornecedor para revisões independentes.

---

## 0. Configuração

**Modelos não pertencem a este texto.** Quais modelos, fornecedores e caminhos de chamada existem
no momento muda mais depressa do que um skill pode ser mantido de forma útil — e varia por
usuário. Este skill, portanto, descreve apenas **papéis e princípios**; o catálogo concreto vive em
um arquivo de configuração na pasta do skill.

### Ordem de carregamento

1. **Arquivo local** na pasta do skill: `models.local.json` ou `models.private.json` (ambos os padrões de nome já
   estão registrados como privados na `.gitignore` desta biblioteca,
   `skills/**/*.local.*` e `skills/**/*.private.*` — nunca publicar, nunca commitar).
   Se existir, esse é o catálogo válido.
2. **Arquivo de exemplo** `models.example.json` na mesma pasta — modelo neutro com marcadores de posição, que
   mostra o esquema. Serve apenas como modelo para criar o arquivo local próprio, não como catálogo
   para execuções reais.
3. **Levantamento ao vivo**, se ambos os arquivos faltarem ou estiverem incompletos: quais modelos
   o runtime atual oferece de fato (por exemplo, o enum `model` de uma ferramenta nativa de
   subagentes, `codex debug models --bundled`, ou uma lista de modelos própria do aplicativo)? Um modelo
   adivinhado é pior do que um levantado brevemente.

**Em caso de contradição, vale a medição ao vivo.** Um arquivo de configuração pode estar
desatualizado (um modelo foi desativado, renomeado ou substituído); uma medição recente no próprio
runtime vence qualquer fonte textual, inclusive a configuração local. Mencione a contradição
brevemente e atualize o arquivo de configuração depois, em vez de ignorá-la em silêncio.

**`deprecated: true` significa: nunca usar.** Uma entrada do catálogo marcada como `deprecated` permanece por
motivos de reconhecimento/histórico (para que um agente consiga situar uma menção antiga), mas não é
mais escolhida para nenhuma tarefa nova — nem como fallback.

### Esquema (ver `models.example.json`)

Cada entrada do catálogo contém: `id`, `provider`, `invoke` (padrão de chamada, sem caminhos reais
no exemplo), `effort_levels`, `roles` (ver seção 1), `strengths`, `weaknesses`, `guardrails`
(restrições de confiabilidade como "somente rascunho", "não escrever diretamente no sistema de arquivos",
"aceitação estrita" — ver seção 3), `budget_hint` (referência ao skill `budgetierung`),
`verified` (disponibilidade comprovada no próprio runtime, ver seção 5) e `deprecated`.

---

## 1. Papéis em vez de uma hierarquia rígida de modelos

A escolha de um modelo responde primeiro **qual papel** uma tarefa exige e só depois qual modelo
concreto preenche esse papel hoje da melhor/mais barata forma. Papéis são mais estáveis do que nomes
de modelos — um modelo é trocado, o papel permanece.

| Papel | Pergunta | Característica típica |
|---|---|---|
| **Pensador/Decisor** | arquitetura, estratégia, requisitos ambíguos, ponderação de alternativas | caro, usado de forma direcionada e não o tempo todo |
| **Worker de longa duração** | execução contínua ao longo de muitos passos: implementação, depuração, tarefas padrão | barato o suficiente para rodar continuamente |
| **Gerador de rascunhos** | primeira versão rápida (design, texto, código, estrutura, tradução) | rápido, mas sempre sujeito a aceitação (seção 3) |
| **Revisor/Aceitação** | verifica resultados de outros modelos | tem mais efeito quando é de um fornecedor diferente do criador (seção 4) |
| **Escalonamento** | chamado apenas para o passo individual mais difícil | nunca para a execução inteira, sempre com justificativa breve |

Um modelo pode acumular vários papéis (por exemplo, worker de longa duração e, às vezes, revisor).
Quais modelos preenchem quais papéis hoje consta na configuração (seção 0), não aqui. Sobre a
menor classe de worker (custo por tarefa, qualidade por tipo de tarefa), ver a seção 7.

### Orientação grosseira de dificuldade (não é uma tabela fixa)

Um cálculo de pontuação sobre dimensões fixas (clareza, complexidade, criatividade, contexto,
criticidade) pode servir como **orientação grosseira** para distinguir worker de longa duração de
pensador/escalonamento — não é um mecanismo vinculante que determine um modelo automaticamente:

```
SCORE = (10 - KLARHEIT) + KOMPLEXITAET + KREATIVITAET + KONTEXT + KRITIKALITAET   (je Dimension 0-10)
```

Pontuação baixa → worker de longa duração ou até um modelo local barato/sem tokens basta.
Pontuação alta (requisitos continuamente contraditórios, prova matemática, estatística com
consequências amplas) → pensador/escalonamento, geralmente seguido de revisão. Entre os extremos
fica o caso comum do worker de longa duração. O limiar concreto para escalonar depende do catálogo
atual (alguns usuários têm apenas dois papéis preenchidos, outros seis) e, por isso, não pertence a
uma tabela fixa neste texto.

---

## 2. Esforço de raciocínio como eixo próprio

O esforço de raciocínio (por exemplo `low`/`medium`/`high`/`xhigh`/`max`, ou uma escala mais fina ou diferente
por fornecedor) é um **eixo independente da escolha de modelo/papel**: primeiro escolha um modelo
tecnicamente adequado e disponível para o papel, depois ajuste sua profundidade de raciocínio à
dificuldade.

- Níveis baixos para rotina e subtarefas bem definidas.
- Níveis altos para ciência, demonstrações, decisões arquiteturais de grande alcance.
- Uma rota de amplitude (subtarefas paralelas e claramente separadas em vez de mais profundidade em
  uma só linha) apenas se o runtime atual oferecer um modo próprio para isso e a regra de confirmação/
  custo já vigente para fan-outs maiores ou de difícil cálculo estiver cumprida.

**Nenhum nível de esforço amplia direitos de escrita, custo, liberação ou publicação.**
Delegações permanecem dentro da autoridade existente (ver seção 5). Se um nível não estiver
disponível no runtime atual, isso deve ser dito e deve-se recorrer a um nível comprovadamente
disponível — sem reportar em silêncio o comportamento mais barato como sucesso.

Etapas individuais longas ou computacionalmente pesadas pertencem — independentemente do nível de
esforço — ao host de computação previsto para isso, não à máquina local interativa; o limiar para
isso é uma regra do ambiente, não uma regra da estratégia de modelos.

---

## 3. Aceitação obrigatória para modelos de rascunho

Modelos no papel **Gerador de rascunhos** entregam, por princípio, um rascunho, não uma entrega
final — independentemente de quão boa seja a primeira impressão. Isso não é uma desvalorização
geral de um modelo específico, mas uma propriedade do papel: primeiras versões rápidas são valiosas
porque são rápidas, e justamente por isso são mais sujeitas a erros.

Daí decorrem três regras fixas, independentemente do modelo concreto:

1. **Todo rascunho é verificado antes de ser aceito** — por um worker de longa duração ou um modelo
   revisor, nunca por simples confiança na qualidade do rascunho.
2. **Um modelo de rascunho preferencialmente não escreve diretamente no sistema-alvo** (sistema de
   arquivos de destino, banco de dados de produção, local publicado). Ele devolve o resultado; um
   modelo verificado o aplica. Essa salvaguarda consta concretamente na entrada do catálogo
   correspondente (`guardrails`), pois é implementada tecnicamente de forma diferente em cada ferramenta.
3. **Áreas tecnicamente restritas** (por exemplo LaTeX, textos jurídicos ou numéricos, código
   sensível à segurança) recebem uma aceitação **mais rigorosa** do que texto geral, mesmo quando o
   modelo de rascunho costuma se sair bem nelas.

---

## 4. Troca de fornecedor para revisões independentes

Uma revisão é mais significativa quando criador e revisor **não usam o mesmo fornecedor nem o mesmo
modelo** — caso contrário, podem compartilhar os mesmos pontos cegos.

- **Padrões de revisão:**

  | Padrão | Como funciona | Quando usar |
  |---|---|---|
  | **Consultor de sessão** | o usuário configura um revisor na sessão em andamento; o agente o chama de forma direcionada | padrão para prova/arquitetura |
  | **Orquestrador como revisor** | o modelo mais forte/coordenador revisa a saída de um subagente worker | o orquestrador já é mais capaz que o worker |
  | **Agente adversário / troca de fornecedor** | modelo A (fornecedor 1) trabalha, modelo B (fornecedor 2) verifica de forma adversarial | verificação independente, duas perspectivas, maior poder de conclusão |
  | **Recomendação em vez de execução própria** | o agente recomenda explicitamente: "executar esta tarefa com o papel Escalonamento + Revisão" | a sessão atual é fraca demais para o passo |

- **Quando usar revisão:** demonstrações matemáticas, decisões arquiteturais com consequências de
  longo prazo, metodologia estatística/desenho de estudo, bugs complexos após vários ciclos de
  depuração sem sucesso, qualquer rascunho da seção 3.
- **Quando não é preciso revisão:** código de rotina, conteúdo, formatação; tarefas bem definidas e
  pouco críticas dentro de um procedimento já verificado.
- **Fraquezas documentadas ficam na configuração, não aqui** — por exemplo, "o modelo X é inadequado
  para revisões matemáticas" pertence como entrada `weaknesses` ao catálogo, pois muda com o modelo, não com o skill.

---

## 5. Direitos decorrem da tarefa, não do modelo

Deliberadamente **não existe uma matriz de permissões por nome de modelo** (qual modelo pode apagar,
qual pode executar comandos de sistema). Essa matriz sugeriria que os direitos são uma propriedade do
modelo — mas são uma propriedade da **tarefa e da autoridade concedida**:

- O que um agente pode ler, escrever, apagar ou executar decorre do sandbox atual do runtime, do
  escopo da tarefa e de eventual liberação do usuário — não de um modelo caro ou barato estar
  respondendo naquele momento.
- As salvaguardas do catálogo (campo `guardrails`) são **indicações de confiabilidade**, não ampliação
  nem restrição de direitos: "somente rascunho" diz o quanto o resultado é confiável, não o que seria
  tecnicamente permitido.
- Uma delegação (a um subagente, a um agente externo, a outro modelo) permanece dentro da autoridade
  da execução que delega. Ela não amplia nada.

### Escalonamento e desescalonamento (padrões, não nomes de modelos)

- **Para cima (o papel passa a Pensador/Escalonamento):** decisão arquitetural exigida, vários
  sistemas precisam ser integrados, requisitos contraditórios/pouco claros, planejamento estratégico
  necessário, bug crítico após vários ciclos sem sucesso.
- **Lateral (outro papel, mesmo nível):** pesquisa fora da área, revisão independente, ferramenta
  especializada de outro fornecedor.
- **Para baixo (desescalonamento):** conceito definido → worker de longa duração assume a
  implementação; tarefa trivial/repetitiva → um modelo mais barato assume; tarefa puramente textual
  sem acesso a ferramentas → um modelo local/sem tokens assume, se disponível no acervo e comprovado
  (`verified: true` no catálogo).

### Regra de transparência na troca de modelo

**Uma troca silenciosa de modelo em relação à formação configurada deve ser comunicada.** Se um runtime
escolhe por conta própria (cota, disponibilidade, padrão interno) um modelo diferente do definido em
`models.local.json`/`models.private.json`, isso não é um erro, mas deve ser declarado de forma transparente — não
reportado em silêncio como sucesso da estratégia planejada. Isso vale independentemente de quais dois
modelos estejam envolvidos concretamente; versões anteriores deste skill citavam aqui um par específico de
modelos como precedente — a regra passou a ser deliberadamente neutra, porque não deve depender de uma
única troca de modelo.

---

## 6. Cotas, fluxo e recorte de papéis — referências em vez de duplicação

Este skill responde **qual papel** e **com que cuidado (esforço, revisão)**. Duas questões vizinhas
deliberadamente não são respondidas aqui, para evitar manutenção duplicada:

- **"Com que frequência posso usar um modelo caro/escasso?"** → skill `budgetierung`: negociação de cotas por
  janela de tempo, conta corrente em execução, pré-procedimento de peças do quebra-cabeça antes de
  escalonar. `budget_hint` no catálogo aponta exatamente para lá.
- **"Como decomponho a tarefa, delego pacotes de trabalho e aceito os resultados?"** → skill
  `orchestrator` (protocolo para decompor, delegar e aceitar) ou skill `choose-your-orchestrator` (quando a forma de
  orquestração adequada ainda precisa ser negociada — contrato de sessão para slots de modelo,
  paralelismo, profundidade de spawn, limites de escrita, aceitação, escalonamento).

---

## 7. Workers pequenos (classe Haiku): qualidade e custo por tarefa

Medição de 2026-10 (Haiku 5.5, `claude-haiku-5-5`; família na época Fable 5.1, Opus 5.5, Sonnet 5.5,
Haiku 5.5; cerca de 30 execuções, comparadas com Sonnet 5.5). Preços por milhão de tokens (posição de
2026-10-06): Haiku 5.5 $0,10/$0,50 (até 100 mil de prompt), Sonnet 5.5 $2/$10, Opus 5.5 $4/$20 — por token ≈ 1/20
de Sonnet, 1/40 de Opus. Preços e conclusões envelhecem com os modelos: em caso de divergência, vale a
medição recente (seção 0).

**Armadilha de eficiência: barato por token ≠ barato por tarefa.** Um subagente Haiku no harness do
Claude Code custa ~180–360 mil tokens por tarefa, mesmo para um arquivo de 193 linhas. A carga base
(~45–65 mil tokens por turno) vem do harness (listas de skills/agentes/MCP, hooks de início), não do
`CLAUDE.md` do projeto (repetição após encurtar o arquivo de regras: 186 mil → 182 mil). Contramedidas:

- **Agrupar:** várias subtarefas por worker, para que a carga base seja paga uma só vez; nunca um
  subagente por documento.
- **Worker headless simples** para tarefas em massa com entrada fixa: `claude -p --model haiku
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' --disable-slash-commands --tools Read,Write`
  → medido $0,018 je README-Übersetzung (gleiches Tokenprofil: Sonnet ≈ $0,35, Opus ≈ $0,66).
  `--bare` (sem `CLAUDE.md` e hooks) economiza mais, mas exige uma chave de API. Para volumes muito grandes,
  API/lote em vez de subagente.
- **Resultado como arquivo mais uma mensagem de 3–5 linhas**, poucas chamadas de ferramenta.

**Qualidade por tipo de tarefa (medida):**

| Tipo de tarefa | Resultado |
|---|---|
| Verificação de fidelidade antigo → novo (enxame de verificação) | muito bom; encontrou 2 erros críticos que autor e script de verificação não viram; ~6 % de falsos alarmes |
| Revisão de código de um único arquivo | bom; 8 achados reais contra 6 do modelo de comparação, em um segundo arquivo 4 achados extras; cada achado precisa de contraverificação |
| Tradução (por ex. READMEs DE→EN) | bom (~9/10); paridade completa; termos técnicos oscilam entre execuções → glossário; rótulos de UI/placeholders precisam de contexto |
| Conferência documentação↔código | bom; sem falsos alarmes nas amostras |
| Mapeamento de duplicatas | utilizável; ~85–90 % de recall contra o modelo de comparação, ~1 falso alarme por seção |
| Correção pequena e bem especificada com teste | bom |
| Mecânica (testes no worktree, rebase, PR, panorama de situação) | bom; relata honestamente instabilidade e bloqueios, não contorna guardas |

**Recomendações:**

1. Traduções em massa (docs, READMEs, strings i18n): muito adequadas, com arquivo de glossário, regra
   de paridade 1:1 e amostragem por um modelo mais forte; agrupar muitos documentos por worker ou usar o
   worker headless simples ou a API em lote — nunca um subagente por documento.
2. Enxames de verificação (fidelidade antigo→novo, doc↔código, antes/depois, existência de links/caminhos):
   o melhor uso — um segundo leitor independente que percebe o que escapa ao autor.
3. Atualizar a base documental no padrão *modelo pequeno mapeia → worker de longa duração escreve →
   modelo pequeno verifica → pensador aceita*; nunca deixar o modelo pequeno reescrever sozinho textos normativos.
4. Pré-revisão de código por arquivo e pequenas correções bem especificadas com teste.
5. Mecânica: execuções de teste, releituras, análise de logs, panoramas via `git grep`.
6. **Não** para decisões de arquitetura, merge e segurança, arquivos de regras normativas e grandes
   sínteses entre arquivos.
7. Regras de eficiência: agrupar tarefas por worker, resultado como arquivo mais mensagem de 3–5 linhas,
   poucas chamadas de ferramenta; nunca aceitar resultados sem verificação (a seção 3 também vale aqui).

**Regra de uso:** o modelo é uma ferramenta de rascunho e verificação (papel *Gerador de rascunhos* ou
segundo leitor no enxame de verificação, seção 1) — não uma instância de aceitação nem um worker padrão
de longa duração. O trabalho produtivo passa pelo worker de longa duração da configuração; a classe
pequena apenas por instrução explícita do usuário. Tarefas em massa com entrada fixa passam
preferencialmente pela API (lote, ≈ $0,001 por README), não como subagente no harness.

---

## Changelog

### 3.1.0 (2026-10-11) — Workers pequenos (classe Haiku) medidos
- Nova seção 7: Haiku 5.5 como worker, medição de 2026-10 (qualidade por tipo de tarefa, preços, recomendações)
- Armadilha de eficiência documentada: subagente ~180–360 mil tokens por tarefa (carga base do harness
  ~45–65 mil por turno); contramedidas: agrupar, worker headless simples ($0,018 por tradução de README), API/lote para tarefas em massa
- Regra de uso: classe pequena somente por instrução explícita, trabalho produtivo pelo worker de longa duração
- Lista de esquema na seção 0 complementada com `verified` (campo já estava em uso em `models.example.json` e
  na seção 5)

### 3.0.0 (2026-10-03) — Breaking: catálogo de modelos externalizado
- Catálogo de modelos removido do texto do skill e transferido para `models.example.json` (versionado, neutro)
  mais um arquivo de configuração local, não publicado (`models.local.json` /
  `models.private.json`, já registrado como privado via `.gitignore`)
- Ordem de carregamento documentada: arquivo local → arquivo de exemplo → levantamento ao vivo; em caso
  de contradição vence a medição ao vivo; `deprecated: true` nunca é usado
- Hierarquia rígida de modelos nível 1 a 4 e tabela fixa pontuação→modelo substituídas por cinco papéis
  (Pensador/Decisor, Worker de longa duração, Gerador de rascunhos, Revisor/Aceitação, Escalonamento);
  a pontuação permanece apenas como orientação grosseira
- Aceitação obrigatória para modelos de rascunho como seção própria (dever de verificação, sem direitos
  de escrita diretos no sistema-alvo, aceitação mais rigorosa em áreas tecnicamente restritas)
- Troca de fornecedor para revisões independentes como princípio, em vez de recomendação fixa de um par de modelos
- Matriz de permissões por nome de modelo removida — direitos decorrem da tarefa/autoridade, não do modelo;
  salvaguardas são indicações de confiabilidade, não cláusula de direitos
- Caminho de chamada concreto do companion 1.0.4, cadeia fixa de escalonamento Ollama/Haiku e a regra de
  precedência Fable/Opus 4.8 removidos ou convertidos na regra neutra "troca silenciosa de modelo deve ser comunicada"
- Cotas remetidas ao skill `budgetierung`, fluxo de delegação/recorte de papéis às `orchestrator` e
  `choose-your-orchestrator` em vez de manutenção duplicada

### 2.2.0 (2026-09-02)
- Esforço de raciocínio incluído como eixo ortogonal à escolha de modelo (`xhigh`, `max` direcionado,
  `ultracode` orientado à amplitude)
- Limiar de computação local e limites de runtime, custo e autoridade esclarecidos

### 2.1.0 (2026-07-02)
- REGRA DE PRECEDÊNCIA: um modelo específico substitui outro em todas as recomendações de nível 4/revisor/
  prova (decisão do usuário; neutralizada na 3.0.0)
- Aviso de troca silenciosa de modelo incluído

### 2.0.0 (2026-06-12)
- Delegação entre agentes: agentes externos e um modelo local como destinos de roteamento
- Pareamento de consultores: 4 padrões (consultor de sessão, orquestrador como revisor, agente adversário,
  recomendação do usuário)
- Matriz de alcançabilidade: iniciável por subagente vs. somente usuário documentada
- Escalonamento lateral para agentes externos (pesquisa, revisão)
- Limiares de pontuação ampliados

### 1.0.0 (2026-03-15)
- Portado do BACH v3.8.0 (ing-strategie v2.0.0)

---

*Portado do BACH v3.8.0 | Baseado em papéis desde 3.0.0*
