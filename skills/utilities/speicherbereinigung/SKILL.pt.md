---
name: speicherbereinigung
version: 1.0.0
type: skill
author: Lukas Geiger und OpenAI Codex
created: 2026-08-04
updated: 2026-08-05
description: "Limpeza de armazenamento baseada em evidências no Windows, com modo de emergência controlado, medição da ocupação física, perícia de processos e origem, e medidas reversíveis contra preenchedores recorrentes de armazenamento."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: utilities
tags: [windows, storage, cleanup, forensics, onedrive, pagefile, logs]
language: pt
status: active
visibility: public
dependencies:
  tools: [powershell]
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: "~/.codex/skills/speicherbereinigung"
  origin_version: null
  origin_repo: null
  last_sync_from_origin: 2026-08-05
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6d44ad70bc2f7abc4086474c001d33a6727d9bb6f9793333d804ad3af4907661
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="speicherbereinigung banner">

# Limpeza de Armazenamento

## Finalidade e resultado

Esta skill recupera espaço de armazenamento de forma controlada no Windows e impede
que o mesmo caminho de preenchimento volte a ocupar o disco imediatamente. Ela
funciona em três fases: liberação de emergência, perícia da causa e limitação
duradoura.

Cada mutação segue o mesmo protocolo (em português: Achado -> Decisão -> execução limitada -> releitura -> medição):

`Fund -> Entscheidung -> begrenzte Ausführung -> Readback -> Messung`

Se o usuário não indicar um objetivo maior, a tarefa só é considerada concluída
quando o volume do sistema informar novamente pelo menos 50 GB de espaço livre
após a última mutação. O primeiro limiar de emergência, de 10 GB adicionais,
encerra apenas o estado agudo, não a tarefa como um todo.

## Quando ativar

Use esta skill em casos de:

- disco do sistema com pouco espaço ou perda recorrente de espaço;
- logs, caches, arquivos de paginação, arquivos, builds ou gerações de backup incomumente grandes;
- clones duplicados, gerações de backup ou cópias locais de nuvem;
- eventos de esgotamento de recursos ou processos com crescimento intenso de commit;
- suspeita de que agendadores, observadores ou clientes de sincronização estejam
  regenerando dados.

## Regras de segurança

- Antes de cada mutação, determine o espaço livre, o volume, o estado dos
  processos, bloqueios, pontos de reparse e o caminho absoluto resolvido do alvo.
- Em ações recursivas, verifique que o alvo está dentro da raiz explicitamente
  escolhida. Nunca use variáveis ou curingas como alvos de exclusão não verificados.
- Não exclua raízes de volume, de usuário, de repositório, de nuvem ou de projeto.
- Preserve fontes ativas, trabalho não confirmado, segredos, cópias de conflito,
  bloqueios de terceiros, `.git` e a única cópia de recuperação.
- Prefira a Lixeira, quarentena, compactação ou desidratação na nuvem. A exclusão
  irreversível só é permitida para um item exatamente identificado e regenerável;
  documente caminho, tamanho e recuperação.
- Altere arquivo de paginação, hibernação, serviços ou limites do sistema somente
  com os privilégios necessários, um plano de reversão e verificação completa por
  releitura. `Zugriff
  verweigert` (Acesso negado) não é uma medida bem-sucedida.
- Nunca exclua objetos da nuvem do OneDrive para liberar armazenamento local.
  Exclusão na nuvem e desidratação local são operações diferentes.

## Fase 1: Liberação de emergência

### 1. Linha de base

Registre no mínimo:

```powershell
Get-PSDrive -Name C | Select-Object Used, Free
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID, Size, FreeSpace
Get-Process | Sort-Object PrivateMemorySize64 -Descending |
  Select-Object -First 15 Name, Id, PrivateMemorySize64, WorkingSet64
```

Anote o horário, o valor inicial e o alvo. Diferencie `PrivateMemory` ou
commit de `WorkingSet`: um processo pode mostrar pouca RAM no working set
e, ainda assim, ocupar muito o arquivo de paginação.

### 2. Inventário limitado

Comece por raízes locais conhecidas e janelas de alteração recentes. Não faça uma
busca recursiva cega em todos os diretórios de nuvem ou de usuário. Candidatos
adequados são:

- caches de modelos, pacotes e builds claramente regeneráveis;
- saídas antigas de builds concluídos;
- logs de aplicação rotacionáveis;
- gerações de arquivo ou backup verificadas;
- cópias locais de nuvem totalmente sincronizadas.

O tamanho lógico do arquivo não é a ocupação física em arquivos esparsos,
compactados ou espaços reservados da nuvem. Use a alocação NTFS (`GetCompressedFileSizeW`),
`compact` ou uma ferramenta equivalente e compare o espaço livre antes e
depois.

### 3. Tratar um item

Trate exatamente um item por etapa de medição. Depois verifique:

- quantos bytes foram realmente recuperados;
- erros, identificadores abertos e bloqueios remanescentes;
- se a fonte protegida continua intacta;
- se é possível recuperar ou regenerar o item;
- se algum processo o recria imediatamente.

O modo de emergência só termina após a comprovação de 10 GB adicionais. Depois
disso, o processo passa diretamente para a perícia.

## Fase 2: Determinar forensicamente os processos de preenchimento e a origem

### 1. Esgotamento de recursos e arquivo de paginação

Leia evidências atuais e históricas em conjunto:

```powershell
Get-CimInstance Win32_ComputerSystem |
  Select-Object AutomaticManagedPagefile
Get-CimInstance Win32_PageFileUsage |
  Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage
Get-WinEvent -FilterHashtable @{LogName='System'; Id=2004} -MaxEvents 20
```

O evento 2004 do Windows Resource Exhaustion Detector contém os processos com o
maior commit no momento do evento. Associe PID, nome do processo, carimbo de
data/hora e bytes aos processos atuais. Um grande `pagefile.sys`, sozinho, não
prova que o próprio arquivo é a causa; procura-se o processo que disparou o commit.

### 2. Crescimento de arquivos

Agrupe arquivos novos ou alterados por:

- hora de criação e de alteração;
- caminho pai e extensão;
- proprietário ou processo gerador;
- taxa diária em arquivos e em bytes fisicamente ocupados.

Examine com atenção os diretórios de log, cache, sincronização, backup, build,
download e sessão. Uma retenção de sete dias é inadequada quando um cliente grava
vários gigabytes por dia e o volume é pequeno.

### 3. Automações

Verifique o agendador de tarefas, serviços, observadores e programas de
inicialização quanto a frequência, retenção e êxito:

```powershell
Get-ScheduledTask | Where-Object State -ne 'Disabled'
Get-ScheduledTaskInfo -TaskName '<task-name>'
```

Verifique separadamente ação, gatilho, intervalo de repetição, último código de
retorno e próxima execução. Uma tarefa existente não prova que a retenção ou a
frequência controlam o crescimento real.

## Fase 3: Limitação duradoura

Escolha a menor medida eficaz e reversível:

- executar a rotação de logs com mais frequência e definir adicionalmente um
  limite de tamanho;
- reiniciar de forma controlada um cliente que esteja gerando muito e medir seu commit;
- limitar o histórico de rolagem do terminal ou o log de depuração a um valor adequado;
- remover caches antigos e regeneráveis e observar se são recriados automaticamente;
- desidratar conteúdo da nuvem já verificado com "Liberar espaço";
- ajustar a frequência do agendador e a retenção à taxa diária medida;
- alterar arquivo de paginação ou hibernação somente de forma administrativa, com
  plano de reinicialização e reversão.

Para o Windows Terminal, um histórico de rolagem padrão limitado pode, por
exemplo, ter a seguinte aparência:

```json
{
  "profiles": {
    "defaults": {
      "historySize": 2000
    }
  }
}
```

Preserve as configurações existentes e valide o arquivo JSON após a alteração.

### Controle específico do OneDrive

Antes de desidratar, o estado de sincronização e os envios pendentes devem estar
verificados. Use um gerenciador de arquivos compatível com filtros de nuvem ou o
comando "Liberar espaço" do Explorador. A desidratação não pode excluir o
conteúdo da nuvem.

Verifique separadamente a área de logs locais do OneDrive em
`$env:LOCALAPPDATA\Microsoft\OneDrive\logs`. Se uma subárea gerar gigabytes por dia, combine retenção
baseada em tempo com um limite rígido de tamanho e uma execução planejada com
frequência suficiente. Proteja arquivos muito recentes ou abertos e verifique,
após a execução, tanto o status da tarefa quanto o tamanho restante.

## Verificação final e relatório

Após a última mutação:

1. Aguarde o término das operações assíncronas de nuvem ou de exclusão.
2. Leia novamente o espaço livre e o commit dos processos.
3. Confira por releitura as configurações alteradas, as tarefas e os tamanhos dos logs.
4. Execute um teste rápido: ocorre novamente geração excessiva de armazenamento
   dentro da janela de observação?
5. Relate o valor inicial, cada item e sua decisão, os bytes fisicamente
   recuperados, os processos de preenchimento, os ajustes duradouros, as
   reversões, os riscos remanescentes e o valor final.

Não afirme limpeza, limitação de processos ou alcance da meta de 50 GB sem a
releitura atual correspondente.

## Limites conhecidos

- Sem privilégios administrativos, alterações de arquivo de paginação, hibernação
  ou serviços podem permanecer bloqueadas. Documente a etapa exata que falta.
- Eventos históricos de processos comprovam um preenchedor anterior; para a
  situação atual, também são necessários dados de processos e de crescimento de arquivos.
- Um plano de backup não é um backup. Transferência ou exclusão exige identidade
  atual do destino, manifesto ou hash, comprovação de restauração e montagem.
- Em caso de propriedade incerta, trabalho ativo de terceiros ou destino
  desconhecido, aplica-se a decisão `nichts` (nada).

## Registro de alterações

### 1.0.0 (2026-08-05)

- Primeira versão portátil para a biblioteca central de skills.
- Adicionadas perícia de esgotamento de recursos, de arquivo de paginação e de processos.
- Ocupação física NTFS e desidratação do OneDrive claramente separadas.
- Adicionada rotação de logs do OneDrive com limite de tempo e de tamanho.
- Definidos critérios rígidos de emergência e de conclusão, com releitura.
