---
name: workflow-extract
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
description: "Constrói, a partir de um histórico de chat ou de prompts de automação existentes (por exemplo, de outro sistema de agentes), uma automação de fluxo de trabalho autossuficiente e neutra em relação ao usuário: um prompt recorrente ou skill de automação para Cron/Schedule/Loop. Alias: automations-extractor. Use este skill quando pedirem \"transforme isso numa automação\", \"isso precisa rodar regularmente/noturnamente\", \"extraia workflows destes históricos de chat/automações\", \"construa uma automação a partir desta sessão\", ou `/workflow-extract`. Complementa sistematicamente os blocos de automação ausentes (seleção por rotação, registro de checagens, idempotência, higiene de logs, portão de liberação, handoff de escalonamento, disciplina de relatório de monitoramento). Inclui também o modo de auditoria de frota: verificar frotas de automação existentes quanto a falhas silenciosas, redundância, desvios e lacunas (\"verifique minhas automações/tarefas agendadas/tarefas cron\"). Se, em vez disso, o objetivo for um skill invocável sob demanda (capacidade chamada sob comando), use o skill irmão skill-extractor."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [automation, workflow, extraction, cron, schedule, loop, transcript, meta, rotation]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: cbe4ff5879ea4348b27573d76c7464270a88ce752959a7681bc20e2bf90bf8df
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.188621+00:00"
---
<img src="banner.png" width="100%" alt="workflow-extract banner">
# Workflow-Extract — construir automações a partir de históricos de chat e automações de terceiros

## Finalidade

Alguns processos não pertencem a um skill carregado quando necessário, mas a uma
**automação que roda sozinha**: verificações noturnas, revisões rotativas de projetos,
execuções periódicas de manutenção. Este skill extrai esses workflows de dois tipos de
fonte — históricos de chat (um processo foi desenvolvido interativamente e deve rodar
futuramente sem supervisão) e prompts de automação existentes de outros sistemas (por
exemplo, automações do Codex, tarefas agendadas, fluxos do n8n) — e os transforma em
prompts ou skills de automação neutros em relação ao usuário e robustos.

A diferença em relação ao processo interativo: uma automação **não tem ninguém que corrija**.
Tudo o que o usuário interceptava na sessão precisa ser interceptado pela própria
automação. É exatamente para isso que existem os blocos em `automation-bausteine.md`.

## Procedimento

### 1. Esclarecer fonte e forma de destino

| Fonte | caso típico |
| --- | --- |
| Sessão atual / transcrição | O processo foi desenvolvido interativamente e deve continuar periodicamente |
| Automação de terceiros (arquivo de prompt, tarefa cron, fluxo do n8n) | Portabilização/abstração para outro sistema ou para a biblioteca |

Formas de destino (uma ou mais):

- **Prompt de automação:** texto de prompt autônomo e neutro em relação ao usuário,
  utilizável em qualquer agendador (automações do Codex, Claude `/schedule`/Cron,
  tarefa agendada, n8n).
- **Skill de workflow:** skill na biblioteca que descreve o processo, e o prompt de
  automação apenas o invoca/parametriza (preferível quando o mesmo processo deve valer para
  vários pipelines/sistemas — uma única fonte da verdade).
- **Command:** slash command enxuto para disparo manual do mesmo processo.

### 2. Extrair o núcleo do workflow

Da fonte, deve-se levantar:

- **Tarefa central:** o que é verificado/mantido/gerado? (uma frase)
- **Lógica de seleção:** a tarefa se aplica a um alvo fixo ou a uma rotação sobre um
  conjunto (um projeto por execução)?
- **Pré-condições:** o que deve ser lido/verificado antes do trabalho (documentos raiz,
  registros, locks)?
- **Obrigações de documentação:** para onde são gravados resultado, log e tarefas de
  acompanhamento?
- **Caminhos de aborto:** quando a execução termina em modo somente leitura ("nada a fazer"
  é um resultado válido)?

Nos históricos de chat, avaliar adicionalmente os ciclos de correção (ver
`../skill-extractor/transcript-quellen.md`): cada correção do usuário é candidata a uma
guarda que a automação precisará futuramente por conta própria.

### 3. Neutralizar

Seguindo as regras de `../skill-extractor/neutralisierung.md`: separar a mecânica da configuração e
mover caminhos/hosts/nomes de projetos para um bloco de configuração. Prompts de automação
precisam especialmente desse bloco, porque são copiados literalmente para os agendadores —
valores concretos devem estar em UM único lugar, no início do prompt.

### 4. Complementar os blocos de automação

Confrontar o núcleo extraído com a checklist em `automation-bausteine.md` e acrescentar os
blocos ausentes — em especial seleção por rotação com registro de checagens, idempotência,
higiene de logs, respeito a locks, saída somente leitura e relatório final. Um workflow sem
esses blocos funciona no teste e degenera na operação contínua (verificações duplicadas,
logs crescentes, colisões com agentes paralelos).

### 5. Definir cadência e orçamento

- **Acoplar a frequência à taxa de mudança:** uma checagem não precisa rodar com mais
  frequência do que muda o seu objeto. Experiência acumulada de conjuntos de automações
  mais antigos: muitas checagens inicialmente horárias foram reduzidas para diárias ou
  semanais — com seleção por rotação, mesmo uma cadência rara cobre todo o pipeline.
- **Janela noturna para o que é pesado**; checagens curtas e somente leitura podem ser
  mais frequentes.
- **Consciência de custo:** cada execução consome tokens/computação; uma execução que
  termina quase sempre em modo somente leitura deve identificar isso cedo (ler o registro
  ANTES da análise cara).

### 6. Testar e implantar

1. **Ensaio:** executar uma vez, interativamente, o prompt final (como se fosse o
   agendador) e verificar: termina de forma limpa? Grava registro/log corretamente?
   Permanece dentro do escopo?
2. **Teste de caso-limite:** simular uma execução em que não há nada a fazer — ela deve
   terminar em modo somente leitura com um breve registro, e não "inventar trabalho".
3. **Implantar:** cadastrar no agendador de destino; na forma de skill, além disso, gravar
   na biblioteca e fazer o deploy.
4. **Observar o caminho de falha:** após as primeiras 2–3 execuções reais, conferir log e
   registro — automações falham com mais frequência por desvio de caminho (o alvo foi
   movido) e por arquivos de log que crescem sem controle.

## Modo de auditoria de frota: verificar uma frota de automações em operação

Para "verifique minhas automações": não extrair, e sim ajudar a operar o ACERVO existente.
Pela fonte de automações do sistema alvo (arquivos de prompt/configuração, agendamentos,
logs/memórias de execução), verificar sistematicamente:

1. **Detecção de falha silenciosa/no-op:** a automação ainda roda, mas não faz mais nada?
   (ler as memórias/logs das últimas execuções: só execuções vazias, erros, caminhos mortos?)
2. **Redundância + retorno:** as automações se sobrepõem em escopo? O retorno (saída,
   achados corrigidos) ainda compensa o consumo (tokens, execuções)?
3. **Desvio:** os caminhos dos prompts, as convenções e os agendamentos ainda correspondem
   à realidade? (alvos movidos, políticas alteradas, cadência alta demais para a taxa de
   mudança.)
4. **Comparação com o catálogo:** falta alguma automação que deveria existir (lacunas na
   grade de padrões)? Sugestões somente com portão de liberação (bloco 12), nunca ativá-las
   por conta própria.
5. **Relatório de achados:** uma linha por automação (manter | ajustar | pausar |
   unificar | excluir) + justificativa; alterações feitas por conta própria somente após
   liberação.

## Modo em lote: triar acervos de automações ou muitas transcrições

Para "verifique todas as automações do sistema X em busca de workflows abstraíveis" ou
"extraia candidatos a automação de históricos de chat antigos":

1. **Redução de dados como no skill-extractor** (map-reduce com subagentes, padrão
   `swarm-operations`): por lote, um subagente que informa, para cada fonte: tarefa central |
   padrão (por exemplo, checagem de rotação, checagem de saúde, mineração de ideias) |
   elementos singulares | abstraível de forma neutra em relação ao usuário? | já coberto por
   um skill existente?
2. **Padrões antes de casos isolados:** quando muitas fontes compartilham o mesmo esqueleto
   (por exemplo, 40 checagens de rotação), o ESQUELETO vira um skill e os casos individuais
   viram parametrizações — não 40 skills separados.
3. **Deduplicar contra o conjunto existente de skills/commands**, e então apresentar ao
   usuário uma lista numerada de candidatos antes da construção em massa.

## Exemplo

```text
User: „Wir haben heute die Zitationsprüfung für ein Paper durchgespielt —
das soll ab jetzt wöchentlich über alle Paper laufen."

1. Zielform: Automations-Prompt für den Scheduler + Verweis auf rotation-check.
2. Kern: Zitate eines Papers gegen Originalquellen prüfen (Web/Datenbank),
   Korrekturen einpflegen, bei Änderungen Folgeaufgabe „Neu-Upload" in TODO.md.
3. Neutralisieren: Pipeline-Root, Registry-/Log-Pfade → Konfigurationsblock.
4. Bausteine ergänzen: Rotations-Auswahl (ein Paper pro Lauf), Registry lesen VOR
   Auswahl, Read-only-Exit („alle Quellen ok"), Log-Hygiene, Abschlussbericht.
5. Takt: wöchentlich reicht (Papers ändern sich langsam); Trockenlauf + Leerlauf-Test,
   dann in den Scheduler.
```

## Sinais de alerta

| Pensamento | Realidade |
| --- | --- |
| "O processo rodou na sessão, então também roda como automação" | Sem usuário faltam todas as correções — a checklist de blocos é obrigatória. |
| "De hora em hora não faz mal" | Faz: tokens, crescimento de log, risco de colisão. Acople a cadência à taxa de mudança. |
| "Vou criar uma automação própria para cada variante" | Esqueleto comum como skill, variantes como parâmetros. |
| "Não encontrei nada — então procuro outro trabalho" | Saída somente leitura com registro é o resultado correto de uma execução vazia. |

## Skills relacionados

- `skill-extractor` — mesma extração, cujo alvo é um skill invocável; compartilha a
  neutralização e as fontes de transcrição (documentadas lá).
- `rotation-check` — o esqueleto padrão para checagens rotativas de pipeline (o tipo de
  automação mais comum); referenciar como bloco em vez de reinventar.
- `swarm-operations` — padrão de enxame para triagem em lote.

## Changelog

### 1.1.0 (2026-07-03)
- Modo de auditoria de frota (verificar uma frota de automações em operação: falhas
  silenciosas, redundância, desvio, lacunas) — integrado em vez de ser um skill próprio
  (decisão de deduplicação).
- Três novos blocos em automation-bausteine.md: portão de liberação por arquivos sentinela (12),
  escalonamento graduado com artefato de handoff (13), disciplina de relatório para monitores (14).

### 1.0.0 (2026-07-03)
- Versão inicial. Surgiu da abstração do acervo de automações do Codex
  (77 automações, padrão dominante de checagem por rotação) em blocos neutros em relação ao usuário.
