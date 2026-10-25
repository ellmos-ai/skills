---
name: automation-self-care
version: 1.3.1
type: skill
author: Lukas Geiger + OpenAI + Google Gemini
created: 2026-07-28
updated: 2026-09-09
description: "Constrói e opera um conjunto central de autocuidado independente de fornecedor para tarefas de LLM agendadas e automações de aplicativos de desktop. Complementa o linting determinístico de políticas, a governança de locks e modelos, a verificação semântica de prompts, atualizações consistentes em múltiplas superfícies, mini-checks e higiene de arquivos de regras. Use quando um agente precisar descobrir seu agendador nativo ou melhorar continuamente uma frota de automações existente com rollback, readback e proteção contra exclusão. Acionado por automation self-care, manutenção de tarefas do agendador, manutenção de automações de aplicativos de desktop, auditoria de frota de automações, agendamentos auto-curativos, core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-governance-automations ou textbased-desktopapp-automations."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system, governance, token-governance, mini-check, policy-linter]
language: pt
status: active
visibility: public
aliases: [textbased-governance-automations-seed, tgas, textbasierte-governance-automationen-seed, textbased-governance-automations, textbasierte-governance-automationen, textbased-governance-automatisations-seed, core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
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
  local_changes_since_sync: true
translated_from_sha256: a4c4c991d5459d5b4fe3a7e80c0877791d79adbd1d9ff38b20798636c19cf5d0
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="automation-self-care banner">

# Autocuidado de Automações

Cria uma frota nativa de manutenção específica por fornecedor a partir de um
único ciclo de regras independente de fornecedor. Preserva a intenção original
da família de tarefas ANTIGRAVITY, mas exige evidências, alterações reversíveis
e readbacks nativos.

## Limites não negociáveis

- Tratar descoberta, planejamento, aprovação, mutação e readback como fases
  separadas.
- Usar a API de automação suportada, o comando ou a UI do aplicativo-alvo.
  Nunca presumir que editar um arquivo de armazenamento altera o estado do
  aplicativo em execução.
- Ler regras locais, locks, logs de exclusão/supressão e agendamentos
  existentes antes de propor qualquer tarefa.
- Não inventar suporte de agendador. Se Create/Update/Readback não puderem ser
  comprovados, criar um plano de instalação manual e parar antes da mutação.
- No máximo uma alteração de ajuste testável de forma independente por
  execução de cuidado.
- Proteger as tarefas de cuidado contra se desativarem ou reduzirem seu
  próprio intervalo abaixo do Recovery Floor configurado. Somente uma decisão
  explícita do usuário, um gate de segurança ou uma emergência comprovada pode
  autorizar uma pausa controlada.
- Manter IDs de tarefa estáveis e legíveis por máquina, independentemente dos
  títulos visíveis. Tratar um prefixo do aplicativo como proteção adicional de
  reconhecimento, nunca como identidade nem como substituto dos controles de
  recovery, supressão, rollback e readback.
- Preservar o prompt anterior, o agendamento, o modelo, as permissões e o
  status de ativação, para que toda mutação possa ser revertida.
- Considerar sucesso somente após evidência de resultado, não apenas após o
  início do agendador ou saída com código 0.
- Nunca copiar segredos, prompts privados ou dados pessoais para um registro
  compartilhado.
- Antes de qualquer mutação, executar um linter de políticas determinístico,
  nomeado no perfil do fornecedor. Resolver caminhos de projeto, scripts de
  verificação e políticas por meio de campos de adaptador ou placeholders
  neutros; não incluir caminhos de host, conta ou diretórios privados na skill
  pública.
- Verificar o mecanismo de lock autoritativo do sistema-alvo antes de ações
  sobre arquivos, agendador, commit ou push. Se a autoridade de lock for
  desconhecida, inacessível ou contraditória, aplicar fail-closed e somente
  leitura.
- Não alterar modelos com base em versões de produto codificadas de forma fixa
  nem em suposições de qualidade não comprovadas. Resolver os modelos
  permitidos e os padrões mínimos a partir da superfície atual do fornecedor e
  da política local válida. Rebaixamentos e promoções exigem a autoridade ali
  definida; em caso de dúvida, o modelo permanece inalterado.
- Não derivar ajustes de prompt apenas a partir de logs de execução. Antes da
  mutação, verificar semanticamente a proposta contra as políticas aplicáveis
  ao projeto-alvo e preservar os limites de segurança, pesquisa e aprovação.
- Tratar múltiplas superfícies de estado autoritativas como uma única
  transação: fazer snapshot dos estados anteriores, atualizar todos os alvos
  declarados, reler cada alvo e, em caso de sucesso parcial, reverter tudo por
  completo. Nunca assumir um número fixo nem uma estrutura de diretórios
  local como universal.
- Gravar relatórios de execução exclusivamente nos armazenamentos locais de
  evidência e status previstos para isso, nunca em arquivos de regras de
  agentes. Os nomes e localizações desses armazenamentos vêm do perfil do
  fornecedor.
- Manutenção pesada pode ser complementada por mini-checks estritamente
  limitados. Limite de tempo de execução, escopo de verificação, tarefa-mãe e
  caminho de escalonamento devem constar no perfil do fornecedor; um mini-check
  não pode executar reparo profundo.

## Fluxo

### 1. Descobrir a superfície nativa de automação

Inventariar o ator atual, o fornecedor, o `app_display_name` não sensível, a classe do aplicativo
a superfície do agendador, as operações suportadas, os
arquivos de estado, o histórico de execuções, a telemetria de uso e o método de
readback. Registrar as capacidades pelo contrato de perfil em
[provider-adapter-contract.md](references/provider-adapter-contract.md).

Distinguir agendamentos nativos de aplicativos de desktop, execução via CLI ou
headless, agendadores do sistema operacional ou iniciadores de serviço, serviço
de agendamento genérico, motor de fluxo de trabalho e automação não suportada
ou somente via UI. A existência de um arquivo de configuração não equivale a
um caminho de mutação suportado.

### 2. Inventariar a frota

Para cada tarefa, registrar um identificador local estável, papel semântico,
título visível, finalidade, impressão digital do prompt, agendamento, status de
ativação, modelo, raciocínio, permissões, caminhos-alvo, último evento do
agendador, último resultado bem-sucedido e proprietário atual. Manter o
conteúdo do prompt apenas localmente.

Conciliar semanticamente as tarefas existentes antes de propor uma nova
criação. Preferir primeiro o ID estável da tarefa, depois o ID nativo do
fornecedor, o papel semântico e o título legado conhecido. Um título visível
diferente não é prova de que uma nova tarefa seja necessária. Correspondências
ambíguas bloqueiam o plano, em vez de criar uma duplicata.

Verificar duas vezes a superfície ativa autoritativa antes de qualquer
mutação, caso o aplicativo possa reescrever o estado a partir da memória.

### 3. Projetar o conjunto central

Ler [core-set.md](references/core-set.md). Escolher entre:

- `compact`: cinco tarefas de cuidado que combinam frequência com
  distribuição de carga; ou
- `full`: nove tarefas focadas, de acordo com a família de
  manutenção original.

Gerar um plano independente de fornecedor:

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
python scripts/build_core_set.py --lint-plan automation-care-plan.json
```

O gerador nunca instala tarefas. Verificar cada capacidade `blocked`
e escolher horários locais sem colisão antes de aplicar o plano. Novos perfis
de fornecedor definem `app_display_name` explicitamente; a CI pode exigir isso
com `--strict-profile`. Títulos visíveis gerados usam
`<APP_DISPLAY_NAME> — <CARE_TITLE>`, enquanto os IDs de tarefa `automation-care.*` permanecem
inalterados. Um perfil Codex usa `CODEX`.

### 4. Instalação em etapas

Instalar pelo adaptador nativo do fornecedor:

1. Começar com higiene em modo somente leitura.
2. Acrescentar a proteção de recursos.
3. Acrescentar o ajuste de qualidade de prompt com rollback.
4. Acrescentar o ajuste de frequência e carga somente quando houver evidências
   de execução suficientes.
5. Acrescentar a coordenação entre sistemas por último.

Para uma migração apenas de título, atualizar no lugar a tarefa correspondente
semanticamente pela superfície nativa suportada. Reler o ID estável e todos os
campos que não são de título; qualquer variação operacional inesperada exige
rollback. Um segundo ciclo de plano/aplicação não deve relatar nenhuma
alteração nem criar outra tarefa.

Criar ou importar tarefas desativadas, a menos que o usuário tenha aprovado
explicitamente a instalação ativa. Para um piloto não supervisionado, exigir
primeiro um log de exclusão, um snapshot do estado anterior, uma evidência de
execução e um caminho de rollback.

### 5. Executar o ciclo de cuidado

Cada tarefa de cuidado segue:

```text
follow-up previous change
  -> collect current evidence
  -> classify one cause
  -> choose zero or one change
  -> mutate through native surface
  -> read back
  -> write receipt and next-check condition
```

Usar o catálogo de hipóteses e as regras de evidência de
[core-set.md](references/core-set.md). Causa desconhecida significa observar,
restringir permissões ou pausar com segurança; nunca adivinhar um reparo.

### 6. Coordenar entre atores

Manter o estado local do aplicativo como autoritativo. Compartilhar apenas
contratos de tarefa, cobertura, status, evidências e impressões digitais
sanitizadas. Revisões redundantes somente leitura são permitidas; mutações com
escritor único exigem um claim ou um lock nativo equivalente.

### 7. Sistemas sem hooks de eventos nativos (extensão Letter-Hooker)

Tratar limitação de tokens ou de assinatura como estado de capacidade, não
como ator quebrado. Devolver a cobertura delegada depois que o ator original
entregar uma evidência de sucesso.

## Saídas obrigatórias

Para cada execução de configuração ou de cuidado, relatar:

- a superfície nativa descoberta e as capacidades não suportadas;
- a topologia escolhida e as tarefas criadas, propostas ou ignoradas;
- a mutação exata e a releitura antes/depois;
- a evidência de resultado ou a janela de observação em aberto;
- o local do rollback e a condição de retorno;
- a atualização compartilhada de cobertura, caso exista um registro de
  coordenação.

## Exemplo

Usuário: "Configure agendamentos de autocuidado neste aplicativo de desktop."

Descobrir se o aplicativo consegue listar, criar, atualizar e verificar tarefas
agendadas. Gerar o plano compacto, explicitar as capacidades não suportadas e
então instalar apenas as tarefas aprovadas pela superfície nativa. Uma pasta
com um prompt de tarefa, mas sem registro ativo no agendador, não é uma
configuração concluída.

## Changelog

### 1.3.1 (2026-09-09)

- Os endurecimentos de autocuidado explicitamente solicitados nas versões 1.2
  e 1.3 foram consolidados de forma independente de fornecedor.
- Caminhos de host, conta e projetos privados foram removidos do guia público
  e substituídos por campos de adaptador ou placeholders neutros.
- A troca de modelos foi vinculada à capacidade atual do fornecedor, à política
  local e à autoridade comprovada; hierarquias de versão fixas e afirmações de
  qualidade não comprovadas foram removidas.
- Linting de políticas, verificação semântica de prompts, gate de lock,
  atualizações transacionais em múltiplas superfícies, higiene de arquivos de
  regras e mini-checks foram descritos como contratos portáteis.

### 1.3.0 (2026-09-09)

- Adicionados linting determinístico de políticas e verificação semântica de
  políticas.
- Garantidas a paridade entre múltiplas superfícies e a limpeza de estados
  contraditórios.

### 1.2.0 (2026-09-06)

- Adicionados governança de locks, proteção contra regressão de modelos,
  higiene de arquivos de regras e a arquitetura de mini-checks.

### 1.1.0 (2026-08-30)

- Adicionados `app_display_name` independente de fornecedor e o formato de
  título visível `<APP_DISPLAY_NAME> — <CARE_TITLE>`, incluindo `CODEX — ...` por meio do
  perfil de adaptador Codex.
- Adicionados linting de plano, conciliação por ID estável/semântica e
  proteção contra duplicatas.
- Esclarecido que a nomenclatura se aplica além do Recovery Floor e que
  migrações apenas de título devem preservar toda impressão digital que não
  seja de título.

### 1.0.1 (2026-07-30)

- Adicionados aliases independentes de fornecedor para automações de texto e
  automações de aplicativos de desktop.

### 1.0.0 (2026-07-28)

- A família original de manutenção ANTIGRAVITY, o ciclo de regras F1-F6 e
  ajustes posteriores específicos de fornecedor foram consolidados em uma skill
  de conjunto central neutra.
