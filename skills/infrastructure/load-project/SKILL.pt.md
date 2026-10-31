---
name: load-project
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-28
description: "No início de uma tarefa concreta de projeto ou quando o contexto não está claro: resolver o objetivo, carregar a hierarquia de regras aplicável, seguir as referências vinculantes e, antes do trabalho propriamente dito, elaborar um relatório de situação baseado em evidências."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [projekt, boot, kontext, regeln, locks, orientierung, onboarding]
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
  origin_path: "local-agent-skills/load-project/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ed68a6bc12f6305ac679b3e5f59590526e7ac96f05afeb08c77b00bd55bcdceb
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.834533+00:00"
---
<img src="banner.png" width="100%" alt="load-project banner">
# Carregar Projeto

## Finalidade

Use esta skill no início de uma tarefa concreta de projeto ou quando o contexto de trabalho
ficar pouco claro. O objetivo não é uma auditoria completa do repositório,
mas o menor contexto confiável com o qual seja possível continuar o trabalho com segurança.

## Configuração

A skill não exige nomes fixos de diretórios. Instalações locais podem definir
opcionalmente os seguintes valores nas suas regras gerais de agente ou em uma
configuração local do projeto:

- raízes de workspace conhecidas,
- ferramentas de arquivo preferidas,
- nomes de arquivos adicionais de boot ou de registro,
- verificadores de lock,
- funções e prioridades específicas do projeto.

Na ausência dessa configuração, a skill trabalha exclusivamente com o objetivo
indicado e com as regras do projeto que forem encontradas ali.

## Fluxo

### 1. Resolver o objetivo

1. Tomar como ponto de partida um caminho explícito, o nome do projeto ou a pasta de trabalho atual.
2. Determinar a raiz real do projeto ou do repositório.
3. Restringir resultados ambíguos com base na tarefa, nos documentos da raiz e nos limites do repositório; quando os objetivos forem materialmente diferentes, não adivinhar.

### 2. Carregar a hierarquia de regras

Ler do contexto geral para o específico:

1. regras globais de agente e de segurança,
2. regras do workspace ou do pipeline,
3. regras do projeto e do repositório,
4. instruções específicas da tarefa.

Regras mais específicas valem dentro do seu escopo; limites de segurança e de autorização de nível superior permanecem em vigor.

### 3. Ler os documentos da raiz por função

Nomes de arquivo são indicações, não uma norma fixa. Procure de forma direcionada
documentos com estas funções:

| Função | Conteúdo típico |
|---|---|
| Entrada | Finalidade, navegação, instrução de início |
| Regras | Forma de trabalho, idioma, segurança, convenções |
| Arquitetura | Componentes, fluxo de dados, limites |
| Status | Estado atual, problemas em aberto, última verificação |
| Tarefas | Próximo trabalho priorizado |
| Registro | Projetos, verificações ou publicações canônicos |
| Evidência | Testes, protocolos de verificação, notas de comprovação |
| Passagem | Trabalho em andamento, alterações alheias, próximo passo |

Carregue apenas as funções relevantes para a tarefa concreta.

### 4. Seguir referências vinculantes

Se uma regra lida indicar expressamente outros arquivos como leitura obrigatória,
carregue-os de forma direcionada. Encerre as cadeias de referência assim que elas
deixarem de fornecer contexto vinculante adicional para a tarefa.

### 5. Verificar estado e locks

- Verificar locks conforme a política local quanto a dono, escopo, carimbo de data/hora e critério de validade; sem uma regra de obsolescência definida, nunca declarar um lock obsoleto por conta própria,
- Estado do controle de versão e alterações alheias,
- Processos em execução ou checkpoints, quando relevante,
- Atualidade de registros, testes e informações de status.

Antes de qualquer alteração, registrar o estado inicial das áreas afetadas como linha de base de status/diff. Se não for possível atribuir com segurança as alterações existentes, considere-as de origem alheia por precaução e não as modifique.

Tratar instantâneos apenas como retratos do momento e verificá-los novamente antes de ações arriscadas.

### 6. Elaborar o relatório de situação

Antes da implementação, registrar de forma concisa:

```text
Ziel:
Projekt-Root:
Geltende Regeln:
Evidenzquellen:
Snapshot-Zeitpunkt:
Relevanter Ist-Zustand:
Locks oder fremde Änderungen:
Erfolgskriterium:
Nächster sicherer Schritt:
```

Citar as fontes apenas com a precisão necessária para permitir a verificação. Redigir segredos,
dados pessoais e conteúdos confidenciais e não os copiar para o relatório de situação.

Se a tarefa estiver clara e autorizada a partir disso, continuar diretamente com o trabalho.

## Limites

- Nenhuma busca ampla e irrestrita de arquivos como padrão.
- Não inventar regras ou registros ausentes.
- Não tratar uma mensagem de status antiga como evidência atual.
- Não sobrescrever alterações alheias.
- Não executar integração de projeto quando apenas o contexto para uma tarefa concreta deve ser carregado.

## Changelog

### 1.1.0 (2026-07-28)
- Removidas as vinculações fixas a usuário, workspace, ferramenta e provedor.
- Introduzida a identificação de documentos por função e a configuração local opcional.
- Operacionalizados a validade de locks, a proveniência de árvore suja, as evidências de instantâneo e os relatórios de situação redigidos.

### 1.0.0 (2026-06-17)
- Versão inicial local.
