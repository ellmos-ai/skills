---
name: budgetierung
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-10-03
updated: 2026-10-03
description: "Modelo de conta para o uso orçamentado de modelos caros ou escassos (Advisor, Revisor, modelos especializados, workers contínuos) em execuções longas de agentes. Começa com uma negociação conjunta entre usuário e modelo sobre os modelos disponíveis, os papéis e as cotas por janela de tempo, mantém uma conta de cada uso, executa um procedimento prévio de peça do quebra-cabeça antes de qualquer escalonamento e permite ajustes durante a execução. Usar quando aparecerem \"orçamento\", \"cota\", \"manter conta\", \"apenas uma vez por hora\", \"usar o revisor com moderação\", \"Fable/Codex/Sol/Astra/Luna/Advisor apenas de forma limitada\", \"/budgetierung\", e sempre que uma execução de Operator, de pesquisa ou de automação precisar combinar vários modelos com custos diferentes, mesmo que o usuário não mencione a palavra orçamento, mas defina limites de uso para modelos."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [budget, kontingent, modellwahl, eskalation, reviewer, advisor, operator, konto]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: ae8346a5144eac699936053f5ca7e12be53014cde4b7826264e2f5fd1e986b0c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
# Orçamentação — negociar, manter e ajustar cotas de modelos

## Para que serve

Execuções longas de agentes combinam hoje frequentemente vários modelos com preços e disponibilidade muito diferentes: um agente principal que pensa e decide, workers baratos e contínuos para a execução e poucos especialistas caros para revisões, auditorias ou avanços. Sem acordo prévio, ocorrem dois erros: os modelos caros são gastos em tarefas de rotina, ou nunca são usados por excesso de cautela. A conta torna o uso **visível e negociável**: o que é permitido fica definido antecipadamente, cada uso é registrado e o usuário pode reajustar a qualquer momento.

Modelos, preços e cotas mudam constantemente, porque surgem novos modelos, as assinaturas mudam e os projetos têm importâncias diferentes. Por isso, esta skill **não contém números fixos**, mas um procedimento para defini-los em conjunto, por uso e por projeto.

## Fase 1 — Negociação no início

Antes de delegar qualquer trabalho, esclarecer o orçamento com o usuário. O que ele já tiver definido não deve ser perguntado de novo; apenas as lacunas devem ser preenchidas, e o resultado deve ser confirmado uma vez, de forma breve.

1. **Levantar o que existe:** Quais modelos e acessos estão realmente disponíveis neste host? Verificar em vez de supor: arquivos de configuração, listas de modelos das CLIs, tipos de subagentes disponíveis. Anotar os nomes dos modelos exatamente como são chamados.
2. **Propor papéis:** Cada modelo recebe um papel:
   - *Pensador/Decisor* (agente principal),
   - *Worker contínuo* (execução, sem orçamento ou com orçamento amplo),
   - *Revisor/Auditor* (verificação independente, idealmente de outro fornecedor que o autor),
   - *Escalonamento* (subproblemas de alta complexidade, tentativas de avanço),
   - *Advisor/Consultor* (correção de rota do agente principal).
3. **Definir cotas:** Para cada recurso, um orçamento e uma janela de tempo, p. ex. „2 solicitações por hora“ ou „permanente, sem limite“. Esclarecer explicitamente:
   - **Expiração ou acúmulo?** Unidades não usadas normalmente expiram; registrar isso assim.
   - **Pools comuns ou separados?** Dois modelos dividem uma unidade (p. ex. „Fable *ou* Astra“)?
   - **O Advisor conta?** Chamadas ao Advisor são caras e fáceis de esquecer; se elas têm cota própria, pertencem a um pool ou estão fora do orçamento, deve constar na conta.
   - **Nível de esforço:** Em modelos com níveis de raciocínio, o nível faz parte do orçamento (xhigh ≠ low).
4. **Combinar o procedimento prévio** (Fase 3), salvo se o usuário quiser outra coisa.
5. **Criar a conta** (Fase 2) e informar ao usuário o caminho.

Forma breve de pergunta quando faltarem dados: uma pergunta com proposta, em vez de uma lista aberta, p. ex. „Sugestão: Sonnet como worker contínuo, revisão com Codex 1×/hora, Advisor apenas sob demanda — serve assim?“.

## Fase 2 — A conta

Um arquivo Markdown no projeto, p. ex. `_operator/KONTINGENT.md`, ou no local previsto pelas convenções do projeto. Modelo: [references/konto-vorlage.md](references/konto-vorlage.md).

A conta contém:
- **Bloco de regras:** as cotas negociadas como tabela (Recurso | chamada/nome do modelo exato | orçamento por janela | expira sim/não).
- **Registro de alterações das regras:** cada ajuste feito pelo usuário é acrescentado com data, sem sobrescrever. Assim fica rastreável sob qual regra um uso anterior foi registrado.
- **Tabela de lançamentos:** uma linha por uso de um recurso orçamentado, com número, horário real de início, **modelo realmente executado**, finalidade, procedimento prévio percorrido, caminho do resultado e próxima janela mais cedo.

Importante:
- **Registrar o modelo realmente usado, não o pretendido.** As CLIs recorrem ao modelo padrão quando não há indicação explícita do modelo. Por isso, definir sempre o modelo explicitamente e, em caso de dúvida, comprová-lo pela configuração ou pela resposta. Se depois se descobrir que outro modelo foi executado, **reclassificar** o lançamento e registrar o erro.
- **Horário de início a partir de um comprovante** (arquivo de carimbo de tempo, log), não estimado.
- **Usos fora do orçamento** (disparados pelo usuário ou expressamente liberados) devem ser registrados mesmo assim, com a observação „nenhuma unidade lançada“, para que o quadro fique completo.
- Workers contínuos sem limite não precisam de lançamento individual. Basta uma linha dizendo que estão em execução e em que trabalham.

## Fase 3 — Procedimento prévio antes de qualquer escalonamento

Unidades caras existem para exceções. Antes de lançar uma:

1. **Definir a peça do quebra-cabeça:** O que exatamente falta? Quais propriedades a solução, a fonte ou o resultado da verificação deveria ter? Por escrito, em poucas linhas.
2. **Procurar barato:** Web, bases de dados especializadas, acervo do projeto, com workers contínuos.
3. **Ferramentas de ideias:** p. ex. `/idea-mining`, depois `/skill-finder`, caso exista uma skill para a tarefa.
4. **Só então lançar**, e registrar na conta quais etapas foram percorridas. Se uma etapa não se encaixar tecnicamente (p. ex. busca de ideias, quando se procura uma *verificação*), registrar o motivo em vez de executá-la pro forma.

Uma cota que expira **não é motivo** para consumi-la. Por outro lado, a economia mal entendida também é um erro: se uma aprovação independente for necessária para o próximo passo (p. ex. registro de reivindicações com troca de fornecedor), esse é exatamente o caso excepcional para o qual o orçamento existe.

## Fase 4 — Ajustes durante a execução

O usuário pode alterar as regras a qualquer momento: novos modelos, mais ou menos unidades, um Advisor que passa a contar a partir de agora. Nesse caso:
- incluir a nova regra no bloco de regras com data e manter a antiga,
- verificar se os lançamentos anteriores devem ser classificados de outra forma sob a nova regra, e registrar isso,
- verificar se existe uma tarefa aberta adequada para o novo recurso e, se houver, utilizá-la. Se não houver, o recurso pode permanecer sem uso até surgir necessidade: uma cota é uma moldura, não uma incumbência. O usuário pode ter superestimado a necessidade, e ocupar-se por ocupar também custa,
- confirmar ao usuário em uma frase o que passa a valer.

Se o próprio modelo propuser um ajuste (p. ex. porque um recurso permanece sem uso de forma constante ou surge um gargalo), deve apresentá-lo como proposta com justificativa. A decisão cabe ao usuário.

## Fase 5 — Encerramento

Ao final de uma execução ou bloco, incluir no relatório ao usuário uma linha sobre o consumo: quais unidades foram usadas, para quê e com qual resultado, e o que expirou sem uso. A conta permanece no projeto; uma sessão posterior a lê primeiro.

## Exemplo

O usuário diz: „Trabalhe como Operator, use workers Sonnet, use Fable ou Codex apenas uma vez por hora e mantenha uma conta.“ Depois: „Sol pode revisar duas vezes por hora, Luna permanentemente, o Advisor recebe uma cota extra.“

→ A Fase 1 confirma brevemente os papéis, a Fase 2 cria a conta com a primeira regra. Na segunda mensagem, a Fase 4 completa o bloco de regras e constata que duas auditorias anteriores com „Codex“, sem indicação de modelo, na verdade foram executadas pelo modelo padrão. Por isso, os lançamentos são reclassificados. Para Luna há agora uma tarefa de exploração aberta adequada, então ela é utilizada; sem uma tarefa desse tipo, permaneceria sem uso.

## Skills relacionadas

- `operator` — modelo de papéis Operator/Worker, no qual esta conta é incorporada.
- `model-strategy` — quando qual modelo é adequado; esta skill regula *quanto* deles se usa.
- `idea-mining`, `skill-finder` — blocos de construção do procedimento prévio.
- `advisor-skill` — consultoria seletiva; suas chamadas pertencem à conta.
- `orchestrator` — pacotes de trabalho, perfis (paralelismo), aceitação.
- `choose-your-orchestrator` — contrato de sessão, no qual esta conta é registrada nos slots de orçamento.

## Changelog

### 1.0.0 (2026-10-03)
- Versão inicial: negociação, conta, procedimento prévio, ajustes durante a execução, encerramento.
