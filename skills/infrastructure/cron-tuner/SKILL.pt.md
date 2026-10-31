---
name: cron-tuner
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-23
language: pt
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [cadence, scheduler, cooldown, backoff, self-tuning, cron]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: "Loop de regulação de cadência auto-ajustável para varreduras recorrentes de agentes. Use quando uma varredura agendada deve acelerar seu intervalo quando há atividade e desacelerar quando há silêncio, sem intervenção do operador."

translated_from_sha256: 4872af1b0af7126a6e61179a521bfde60be8ab195522e48cf612f260b65b139c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.220923+00:00"
---
<img src="banner.png" width="100%" alt="cron-tuner banner">

# cron-tuner — loop de regulação de cadência auto-ajustável

Um loop de regulação **auto-ajustável** para trabalho recorrente guiado por cronograma (cron jobs, tarefas agendadas, temporizadores). Em vez de um intervalo fixo, o job ajusta sua própria cadência: acelera quando há trabalho e desacelera quando há silêncio. Neutro quanto a host e plataforma; o padrão funciona com qualquer agendador.

## Quando usar

- Uma varredura recorrente (monitoramento de caixa de correio, varredura de sync-yard, polling de fila) deve reagir rapidamente durante um "Match" ativo e permanecer econômica em períodos ociosos.
- O ajuste deve ser **auditável** (um arquivo de estado) em vez de implícito em uma conversa ou na cabeça de uma pessoa.

## Conceitos

- **Loop de regulação**: medir → decidir → agir → persistir. Cada execução termina gravando seu estado; cada execução começa lendo-o.
- **Ativação**: novo trabalho encontrado → saltar diretamente para o intervalo mais rápido.
- **Escada de cooldown**: execuções vazias descem uma escada; cada degrau só se aplica quando o intervalo realmente muda.
- **Teto**: nunca relaxar além de um intervalo máximo definido.

## Esquema de referência

| Condição | Novo intervalo |
|---|---|
| novo trabalho encontrado | o mais rápido (ex.: 15 min) |
| 4 execuções vazias consecutivas | 30 min |
| 6 execuções vazias consecutivas | 1 h |
| cada execução vazia adicional | dobrar (2 h, 4 h, 8 h) |
| Teto | 24 h (nunca mais alto) |

Ajuste os limiares à carga de trabalho; mantenha a duplicação simples e o teto explícito.

## Arquivo de estado (obrigatório)

Um pequeno arquivo JSON por worker, ex.: `cron-tuner-state.json`:

```json
{
  "empty_runs": 0,
  "interval_minutes": 15,
  "note": "cron-tuner state"
}
```

Regras:

1. **Arquivo, não memória.** O contador deve sobreviver à compactação de contexto, a reinícios de sessão e a trocas de operador, e deve ser visível para humanos e outros agentes. Não rastreie a cadência no histórico da conversa.
2. **Reescrever somente na mudança.** Persista o estado a cada execução, mas substitua o job agendado somente quando o intervalo realmente mudar.
3. **Novo job = novo cronograma, mesmo estado.** Uma mudança de cadência significa excluir o job antigo e criar um novo com o novo intervalo; o contador continua.

## Regras operacionais

- **O trabalho decide, não o humor.** Somente chegadas observadas alteram a cadência — nunca expectativas ou estimativas.
- **Deslocamentos anti-manada.** Evite as marcas de hora cheia e meia hora para o intervalo mais rápido (ex.: minutos 7/22/37/52), para que frotas não disparem em sincronia.
- **Fail-safe:** se um sistema parceiro silenciar, vale a regra normal de vacância/ausência — o regulador nunca escala para enxurradas de polling.
- **Evidências:** toda mudança de cadência é registrada com motivo, intervalo antigo e novo.

## Extensibilidade (registro dos tipos de loop)

A skill é o lar de outros tipos de loop auto-ajustáveis ao longo do tempo:

- **cooldown** (este esquema: silêncio → mais lento)
- **backoff** (erro → mais lento, sucesso → mais rápido)
- **burst** (pico de chegadas → modo rápido temporário com fim explícito)
- **wake-assist** (mensagem externa de despertar → execução imediata fora do ciclo)

Novos tipos de loop recebem aqui uma subseção própria mais seu próprio esquema de arquivo de estado.
