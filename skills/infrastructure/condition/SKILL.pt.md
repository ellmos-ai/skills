---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-28
description: "Linguagem de condição flexível para metas, prompts e tarefas. Traduz condições, momentos e dependências de ordem em gates verificáveis, de modo que uma subetapa só seja executada após uma liberação comprovada. Usar sempre com /condition, /if, /if-only, /when, /after, /and ou /or, bem como em formulações como \"somente quando\", \"assim que\", \"apenas se\", \"depois que\", \"aguarde até\", \"em seguida\" ou \"não antes de\". Usar também quando vários subobjetivos dependem uns dos outros ou quando uma meta contém uma liberação posterior."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
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
  origin_path: "condition/SKILL.md"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: d12d1a078138495fee061d4564ba1bc1e486e088023421c05cf21055a844a9c0
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.540007+00:00"
---
<img src="banner.png" width="100%" alt="condition banner">
# condition — Linguagem de condições para metas e prompts

## Ideia central

Condições em texto corrido são fáceis de deixar passar despercebidas. Por isso, traduzir cada condição relevante em um gate nomeado e verificável:

> Ao ler, generoso; ao comprovar, inflexível.

A entrada pode ser em linguagem natural e incompleta. A tradução interna, porém, precisa registrar de forma inequívoca:

1. qual condição deve estar cumprida,
2. qual subetapa está bloqueada,
3. qual consulta de ferramenta vale como comprovação,
4. se o não cumprimento significa adiamento ou proibição.

Bloquear apenas a subetapa afetada. Continuar o trabalho independente.

## Blocos da linguagem

| Expressão | Semântica | Exemplo |
| --- | --- | --- |
| `/condition <Bedingung> -> <Schritt>` | Gate canônico | `/condition Tests grün -> Release bauen` |
| `/if <Bedingung> -> <Schritt>` | Sinônimo de `/condition` | `/if Review abgeschlossen -> mergen` |
| `/when <Bedingung> -> <Schritt>` | Executar assim que a condição ocorrer | `/when Export fertig -> Bericht prüfen` |
| `/if-only <Bedingung> -> <Schritt>` | Somente se cumprida; caso contrário, não executar | `/if-only Backup belegt -> Altbestand löschen` |
| `/after <Dauer> -> <Schritt>` | Deslocamento temporal a partir do momento de definição | `/after 30 minutes -> Status prüfen` |
| `/and` | Todas as condições vinculadas devem valer | `/if Tests grün /and Review da -> mergen` |
| `/or` | Basta uma condição | `/if Freigabe da /or Notfallregel aktiv -> starten` |

Usar condições numeradas como `/condition 1 ...` e `/condition 2 ...` quando um prompt contiver vários gates. Com `/and` e `/or` combinados, não inventar uma precedência de operadores implícita: usar parênteses ou subcondições numeradas. Se o significado continuar ambíguo, perguntar antes de liberar uma etapa arriscada.

Tratar `/if-only` como proibição. Se a condição não puder ser comprovada, não executar a etapa. Em caso de formulação pouco clara e consequências irreversíveis, escolher a leitura mais rigorosa.

## Fluxo

### 1. Normalizar a condição

Traduzir a entrada em uma frase verificável. Converter tempos relativos em um momento absoluto com fuso horário no momento da definição.

| Entrada | Condição normalizada | Classe de comprovação |
| --- | --- | --- |
| `time 06:00` | Hora do sistema é no mínimo 06:00 no fuso acordado | Ferramenta de relógio/tempo |
| `after 2 hours` | Hora do sistema é no mínimo o momento da definição mais duas horas | Ferramenta de relógio/tempo |
| `wenn Worker A fertig ist` | Artefato de aceitação ou status da tarefa A indica conclusão | Ferramenta de tarefas/arquivos |
| `wenn Tests grün sind` | Execução de teste prescrita termina com sucesso | Ferramenta de processos/testes |
| `nach dem Push` | O remote de destino contém o commit previsto | Ferramenta de controle de versão |
| `wenn der User zustimmt` | Consentimento explícito consta na conversa | Entrada do usuário |

Se não houver um caminho objetivo de comprovação, dizê-lo abertamente. Nenhum gate deve ser formulado de modo que só possa ser fechado por suposição.

### 2. Registrar o estado do gate

Se houver um armazenamento persistente de gates, tarefas ou memória disponível, armazenar pelo menos estes campos:

```text
id
condition
blocks
mode = wait | only
proof_method
status = open | met | dropped
created_at
evidence
```

Se não existir armazenamento persistente, manter o estado visível no objetivo atual, no plano de tarefas ou no documento de transferência. Só afirmar que um gate sobrevive às sessões se o armazenamento usado for de fato durável.

Um adaptador de runtime existente pode usar outros nomes de comando. Funcionalmente, ele precisa de: `open`, `list`, `meet` e `drop`, ou operações equivalentes.

### 3. Reordenar o trabalho

Um gate aberto não bloqueia a tarefa inteira. Executar todas as etapas independentes e, antes de cada etapa dependente, verificar novamente o estado do gate.

Não fazer polling ativo em loops curtos de agente. Para esperas mais longas, usar um agendador, um job em segundo plano ou um evento que sinalize uma única vez quando ocorrer. Após o sinal de despertar, comprovar mesmo assim a condição real novamente com a ferramenta prevista.

### 4. Verificar com rigor e fechar

Executar primeiro a consulta da ferramenta e só então fechar o gate com evidência concreta. Exemplos de comprovações adequadas:

- Tempo: carimbo de tempo medido com fuso horário,
- Arquivo: caminho, metadados ou hash do artefato esperado,
- Testes: comando executado, código de saída e resumo relevante,
- Repositório: branch, ID do commit e conferência com o remote,
- Processo ou tarefa: ID estável e status final medido,
- Consentimento: resposta inequívoca do usuário no contexto atual.

Uma estimativa, um estado apenas esperado ou a mera afirmação de outro worker não bastam quando deveria haver uma comprovação independente disponível.

Se um gate se tornar obsoleto por mudança na tarefa, marcá-lo como `dropped` com justificativa. Em `/or`, fechar ou descartar também as alternativas que não são mais necessárias, para que não restem gates zumbis.

### 5. Escalar

Quando todas as etapas independentes estiverem concluídas:

1. verificar se o trabalho preparatório que bloqueia pode ser feito ativamente dentro da tarefa,
2. se for apenas uma condição de espera, usar um agendador ou job em segundo plano adequado,
3. se depender de uma decisão do usuário ou de uma dependência externa, transferir com o gate aberto e um estado intermediário claro.

Não derivar permissão adicional de uma condição. Um gate cumprido apenas altera a ordem; não amplia o escopo autorizado da tarefa.

## Exemplos

### Meta com condição temporal

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

A verificação dos dados pode acontecer antes. A publicação permanece bloqueada até que uma consulta atual de horário comprove no mínimo 16:00.

### Prompt com várias condições

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

Comprovar os dois gates separadamente. Só depois fazer o merge.

### Proibição em vez de adiamento

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

Sem backup comprovado, não excluir nada, e mencionar a proibição pendente no relatório final.

## Armadilhas

- Repetir a condição apenas no texto corrido, em vez de mantê-la como estado.
- Pausar uma meta inteira quando apenas uma subetapa está bloqueada.
- Armazenar tempo relativo sem momento de definição e sem fuso horário.
- Substituir a comprovação por ferramenta por uma suposição ou autodeclaração.
- Tratar `/if-only` como simples espera.
- Deixar gates alternativos desnecessários abertos após `/or`.
- Incluir nomes de provedores, modelos, usuários ou hosts na mecânica geral.
- Tratar um caminho local de runtime como pré-requisito da própria linguagem.

## Changelog

### 1.1.0 (2026-07-28)

- Formulado de modo neutro quanto a provedor, usuário e sistema, para runtimes de skill compartilhados.
- Uso em metas e prompts explicitado.
- Runtime descrito como adaptador intercambiável; caminhos locais fixos e nomes de modelos removidos.
- Esclarecidas as ligações ambíguas `/and`/`/or`, os estados duráveis e os limites de autorização.

### 1.0.0 (2026-07-25)

- Primeira versão com `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and` e `/or`.
