---
name: cloud-communication-protocols
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-25
language: pt
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [ping-pong, agent-beam, listeners, cross-machine, sync-yard, coordination]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: "Skill-guarda-chuva para protocolos de comunicação entre agentes baseados em nuvem em máquinas diferentes (Ping-Pong, agent-beam, Listener e protocolos futuros). Use quando o trabalho for coordenado entre máquinas por meio de uma pasta de sincronização compartilhada ou de um Message-Yard."

translated_from_sha256: 9f6c20f17b3f62f11b709c05cde26d3c28b48495a60ffaa26cf96a17af27a8ce
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.488602+00:00"
---
<img src="banner.png" width="100%" alt="cloud-communication-protocols banner">

# cloud-communication-protocols

Família de protocolos que permite a dois ou mais agentes em máquinas
diferentes coordenarem-se por meio de uma pasta compartilhada sincronizada
com a nuvem (o "Yard"), em vez de um canal direto. Este skill é o
**guarda-chuva**: ele reúne os protocolos, indica qual deles está
comprovado e bloqueia os que ainda são conceito.

## Quando usar

- O trabalho se estende por duas ou mais máquinas (verificação, configurações
  espelhadas, pilotos) e não há um canal direto de agente para agente.
- É necessário um vocabulário comum para tarefas, respostas, cadência e
  escalonamento entre essas máquinas.

## Protocolos desta família

### 1. Ping-Pong (comprovado, protocolo base)

Dois ou mais workers com varreduras agendadas em horários defasados
compensam a latência de sincronização da nuvem: cada lado varre o Yard em
busca de tarefas endereçadas a ele, executa, deixa a resposta e pode emitir
tarefas de acompanhamento para o outro lado.

Regras centrais: escrever apenas no próprio slot, comprovantes para cada
ação, idempotência, nenhum segredo no Yard (apenas chaves públicas,
fingerprints e caminhos), deltas de erro cooperativos, verificação por
readback sobre o log.

**Cadência: frequência de polling adaptativa.** O controle de cadência não
faz parte das regras de payload do protocolo base, mas toda implementação
precisa dele — um intervalo de polling fixo ou inunda um Yard vazio ou perde
trabalho novo. Dois mecanismos se aplicam e ambos devem ser tratados
explicitamente, não de forma implícita:

- **A — Autoajustável (padrão, sem entrada do operador; o padrão
  `cooldown`/backoff).** Tarefa nova encontrada → saltar diretamente
  para o intervalo mais rápido (por ex. 15 min). Execução vazia → resfriar
  em uma escada: 4 execuções vazias consecutivas → 30 min, mais 2 → 1 h,
  depois dobrar a cada nova série vazia (2 h, 4 h, 8 h) até um teto rígido
  (24 h, nunca mais). Persistir o contador de execuções vazias e o intervalo
  atual em um pequeno arquivo de estado no worker (não na memória da
  conversa), para que sobreviva a reinicializações; uma mudança de cadência
  significa apagar o job agendado antigo e criar um novo no novo intervalo,
  com o contador preservado. Esquema de referência completo, esquema do
  arquivo de estado e outros tipos de loop (burst, wake-assist): skill
  complementar **`cron-tuner`**.
- **B — Override instruído pelo par.** Cada lado pode definir explicitamente
  a cadência do outro no texto da tarefa — `CADENCE: match 15m`, para
  sincronizar em uma janela mais estreita, ou `CADENCE: pause 1h → 2h after 3
  empty`, para
  desacelerar um lado com trabalho de concentração previsível. Quem altera a
  cadência de um par confirma o novo intervalo no próximo delta (o readback
  também vale para os relógios).

Ambos os mecanismos alteram apenas o tempo de reação, nunca as regras do
protocolo base (disciplina de slot, comprovantes, nenhum segredo). Um canal
mútuo `WAKE: <Grund>` permite varreduras fora do ciclo como dica, nunca
como autoridade; apagar após a leitura.

Especificação completa e comprovantes de referência:
`dev-bricks/system-gap-master` → `docs/communications-protocols-skill.md`.

### 2. agent-beam (conceito, bloqueado)

Para trabalho urgente: um pacote composto de prompt + script inicial é
depositado no slot de destino, e um watcher na máquina de destino inicia com
ele uma execução de agente local — o agente "aterrissa" com a tarefa e o
script inicial e começa imediatamente.

Bloqueado: requer um contrato de confiança assinado para o script inicial,
uma etapa de quarentena/revisão e liberação explícita do operador antes de
qualquer ativação.

### 3. Listener / Ear-to-Ear-Listening (conceito, bloqueado)

Watchers observam gatilhos no Yard (chegada de arquivos, arquivos de flag,
alterações de registro) e iniciam agentes na outra máquina. "Ear-to-Ear": o
listener de um host observa a caixa de entrada do outro host.

Bloqueado: regras de debouncing, listas de permissão de gatilhos por slot e
um contrato de segurança são necessários antes de tudo.

## Invariantes comuns (todos os protocolos)

- O Yard é transporte, nunca área de trabalho e nunca armazenamento de
  segredos.
- Cada ação deixa um comprovante verificável; "concluído" sem artefato não
  está concluído.
- O tratamento de erros é cooperativo: deltas de erro com hipótese e teste
  de contraprova; segundas opiniões são bem-vindas.
- A ausência de um parceiro é tratada pela regra de vacância da plataforma
  (por ex. 48 h), não por escalonamento.

## Adicionando novos protocolos

Novos protocolos entram nesta família como subseções em
`communications-protocols-skill.md` (primeiro como conceito, com contrato de segurança
próprio e comprovantes antes de "comprovado"). Liste-os aqui com uma linha
cada: nome, estado (conceito/piloto/comprovado), finalidade.
