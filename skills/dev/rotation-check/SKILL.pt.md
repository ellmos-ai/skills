---
name: rotation-check
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
description: "Esqueleto padrão para verificações rotativas de pipeline: a cada execução, escolher exatamente um alvo de um conjunto (projetos, pastas, repositórios) — preferencialmente o que está há mais tempo sem verificação —, realizar a verificação e registrar o resultado em um registro de verificações e em um log de histórico. Use esta skill quando uma verificação recorrente deve ser distribuída por muitos projetos („verifique regularmente todos os X quanto a Y\"), quando uma automação precisa evitar verificações duplicadas, quando uma estrutura de registro de verificações / CHECKS-LOG é criada ou utilizada, ou quando uma rodada periódica de qualidade (verificação de fontes, verificação de estilo, verificação de saúde, auditoria) deve ser distribuída de forma justa por um pipeline."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [automation, check, rotation, registry, pipeline, log, audit, wartung]
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
translated_from_sha256: b723f4d120407b938e8a8fdc10c5a6a7d6d4a8fe1fed2cf79b836daf0b729244
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="rotation-check banner">
# Rotation-Check — um alvo por execução, cobertura justa, memória

## Finalidade

Quem quer verificar periodicamente um pipeline com muitos projetos (fontes, estilo, saúde,
segurança, traduções, …) enfrenta um problema de distribuição: verificar todos os projetos a
cada execução é caro; sem memória, cada execução verifica por acaso o mesmo. O padrão de
rotação resolve os dois: **exatamente um alvo por execução, seleção por „há mais tempo sem
verificação", registro como memória.** Assim, mesmo uma cadência rara (diária/semanal) cobre
todo o pipeline ao longo de semanas — comprovável e sem trabalho duplicado.

Comprovado como base de um acervo crescido de automações produtivas em vários pipelines de
projetos.

## Componentes

### 1. Dois arquivos por pipeline (criar uma vez)

| Arquivo | Conteúdo | Caráter |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | uma linha compacta por verificação: alvo, data, tipo de verificação, resultado, próximo passo | Visão geral do estado — é lido ANTES de cada seleção de alvo |
| `CHECKS-LOG.txt` | breve entrada de histórico por execução com detalhes/evidências | Diário — somente acréscimo |

Ambos ficam na raiz do pipeline (não no projeto individual), para que uma execução possa
ler os dois com uma única leitura. Formato de linha do registro:

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. Regra de seleção

1. Ler registro e log (obrigatório, ANTES da seleção — senão há verificação duplicada).
2. Candidatos: alvos que, para ESTE tipo de verificação, nunca foram verificados ou não são
   verificados há mais tempo.
3. Desviar se o alvo foi tocado recentemente por uma verificação **intimamente relacionada**
   (por exemplo, uma verificação de citações logo após a verificação de fontes não traz nada)
   ou se está bloqueado/em edição no momento (respeitar os locks).
   **Período de carência entre irmãs:** Quando várias verificações relacionadas atuam sobre o
   mesmo conjunto de alvos (por exemplo, desenvolvimento, busca de bugs e revisão do mesmo
   pipeline), combinar um período de carência (valor empírico: ~24 h) durante o qual um alvo
   trabalhado por uma verificação irmã não é escolhido novamente — evita colisões e alterações
   paralelas contraditórias.
4. Priorizar fora da ordem apenas com um bom motivo (por exemplo, grande revisão desde a
   última verificação) — mencionar o motivo no log.

### 3. Realizar a verificação — com saída somente leitura

Aplicar a verificação em si (livremente definível: verificação de fontes, verificação de
estilo, auditoria de segurança, …) ao ÚNICO alvo escolhido. Dois desfechos válidos:

- **Achado:** corrigir o que cabe no escopo; o que for maior entra como tarefa de
  acompanhamento no arquivo TODO/AUFGABEN local do projeto (a verificação não precisa resolver
  tudo sozinha).
- **Nada a fazer:** documentar brevemente e encerrar. Uma execução ociosa é um resultado,
  não um fracasso — jamais ampliar o escopo para „ter encontrado algo".

### 4. Documentar

- Acrescentar a linha ao registro (compacta), escrever a entrada no log (detalhes/evidências).
- **Higiene do log:** quando registro/log ficarem confusos (valor empírico: várias centenas de
  linhas), mover o estado antigo para `_archiv/`, criar um arquivo novo e referenciar no
  cabeçalho o antecessor (caminho + data).
- **Desvio de caminho:** se um caminho esperado não existir (alvo movido/renomeado), NÃO criar
  de novo — corrigir pelo arquivo de estado/registro oficial do pipeline e registrar o caminho
  incorreto em um log de falhas.

### 5. Cadência

Acoplar a frequência à taxa de mudança do que está sendo verificado: verificações rotativas
sobre acervos estáveis funcionam bem semanalmente (um alvo por execução ≈ pipeline inteiro por
trimestre com cerca de 12 alvos); verificações de ritmo acelerado (por exemplo, sobre trabalho
ativo) diariamente. Experiência prática: verificações inicialmente horárias foram quase todas
reduzidas para diárias/semanais — a cobertura se manteve, os custos caíram.

## Modelo de prompt (para agendador/automação)

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und was bei Befund zu tun ist; Folgearbeiten in
die projektlokale TODO-Datei>.

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registry-Zeile in <REGISTRY> (Ziel, Datum, Checktyp, Ergebnis, nächster
Schritt) + Verlaufseintrag in <LOG>. Bei Überlänge: alten Stand nach _archiv/ und
frische Datei mit Verweis.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```

## Sinais de alerta

| Pensamento | Realidade |
| --- | --- |
| „Eu simplesmente escolho um projeto interessante" | A seleção só pelo registro — caso contrário há viés para projetos favoritos e pontos cegos. |
| „Leio o registro depois da verificação" | Antes. Ele é o critério de seleção, não apenas o protocolo. |
| „Vários alvos por execução rendem mais" | Um alvo mantém as execuções curtas, idempotentes e interrompíveis; o volume vem da rotação. |
| „A execução ociosa foi em vão" | Uma execução ociosa documentada atualiza a memória — isso é metade do valor do sistema. |

## Skills relacionadas

- `workflow-extract` — constrói automações a partir de sessões/automações de terceiros; usa este
  esqueleto como componente padrão.
- `pipeline-optimizer` — para a reestruturação de um pipeline (o Rotation-Check mantém, o
  Optimizer renova).

## Changelog

### 1.1.0 (2026-07-03)
- Período de carência entre irmãs adicionado como regra de seleção (anticolisão entre
  verificações relacionadas sobre o mesmo conjunto de alvos; achado da classificação completa do
  acervo de automações).

### 1.0.0 (2026-07-03)
- Versão inicial. Abstraída do acervo de automações do Codex (padrão de rotação em
  ~40 de 77 automações: verificações de pesquisa/software/Roblox com CHECKED-REGISTRY/CHECKS-LOG).
