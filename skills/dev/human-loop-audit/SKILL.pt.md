---
name: human-loop-audit
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: "Procedimento interativo de auditoria em zíper para uma série de aplicativos/objetos de teste: o usuário testa ao vivo e dá feedback curto no chat, enquanto o agente já inicia o próximo objeto E avalia em paralelo o feedback do anterior (registrar de forma estruturada, delegar imediatamente as ordens de reparo a workers) — em vez de esperar sequencialmente. Use esta skill com \"human-loop-audit\", \"vamos testar os apps em zíper\", \"eu testo, você avalia e repara\", ou quando uma série de GUIs/produtos deve ser testada em conjunto com o usuário e as constatações devem gerar reparos imediatamente. O encerramento é uma lista estruturada de constatações por objeto (Funciona/Defeito/Desejo) mais a lista dos reparos já iniciados."
# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [audit, usertest, human-in-the-loop, gui-test, reissverschluss, delegation, feedback]
language: pt
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: b65128841e358d7ba0f7a3892feea4ef776f3b6e3021109bb89010a6243e82d5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.764372+00:00"
---
<img src="banner.png" width="100%" alt="human-loop-audit banner">

# Human-Loop-Audit

> **Não confundir com `reissverschluss-merge`:** O nome compartilha a imagem do "zíper", mas `reissverschluss-merge` é um **procedimento de merge no Git** (mesclar, trecho a trecho, dois branches de código). `human-loop-audit` aqui não tem nada a ver com Git — é um **procedimento de teste/auditoria com o usuário**. Ambas as skills usam o zíper apenas como a mesma ideia básica (dois fios entrelaçados dente a dente, não fio por fio, um após o outro).

## Finalidade e divisão de papéis

O tempo do usuário é o **gargalo serial**: somente ele pode operar um app ao vivo e dizer em segundos se ele funciona corretamente. Todo o resto — abrir objetos, registrar o feedback de forma estruturada, disparar reparos — fica a cargo do agente, e isso acontece **enquanto** o usuário já está no próximo objeto, não depois. O agente atua ao mesmo tempo como operador do cockpit e avaliador.

**O cerne é a sobreposição, não a ordem em si:** um "abrir app → esperar → avaliar → abrir o próximo app" puramente sequencial desperdiça o tempo de espera em que o usuário está testando. O Human-Loop-Audit aproveita exatamente essa janela.

## Fluxo

1. **"start"** do usuário → o agente abre o **primeiro** objeto de teste. Basta iniciar o processo (por exemplo `Start-Process <exe>` ou o comando de inicialização correspondente do objeto) — **não é necessário assumir a área de trabalho**, o usuário opera sozinho. Confirmar brevemente que está aberto.
2. **O usuário testa e escreve o feedback no chat** — tópicos curtos bastam; não reformular nada que altere o sentido.
3. **Assim que o feedback chega, duas coisas acontecem em paralelo, não em sequência:**
   - O agente **abre imediatamente o próximo objeto de teste**, para que o usuário possa continuar testando sem tempo de espera.
   - **Ao mesmo tempo**, o agente avalia o feedback recebido: registra a constatação de cada objeto de forma estruturada (**Funciona** / **Defeito** / **Desejo**, com uma breve descrição) e, em caso de defeito ou desejo claro, **delega imediatamente uma ordem de reparo a um worker** (não acumular e encomendar "depois" — o reparo deve rodar enquanto o usuário continua testando).
4. **Repetir** até que todos os objetos tenham sido testados (voltar aos passos 2/3 para cada objeto seguinte).
5. **Encerramento:** apresentar ao usuário a lista de constatações (Funciona/Defeito/Desejo por objeto) + a lista dos reparos iniciados (worker/ordem/status).

## Estrutura das constatações (por objeto de teste)

| Objeto | Status | Constatação | Reparo delegado a |
|---|---|---|---|
| `<App/Objekt-Name>` | Funciona / Defeito / Desejo | tópico curto, sem alterar a formulação do usuário | nome do worker/sessão, se delegado |

Um objeto pode receber várias linhas (várias constatações). Nada é resumido silenciosamente — o encerramento deve ser lido a partir desta tabela, não de memória.

## Delimitação em relação a skills afins

- **`reissverschluss-merge`** (ver observação acima) — procedimento puro de merge no Git, sem sobreposição de conteúdo apesar da mesma imagem do nome.
- Ciclos de teste por ondas/envio à loja, mais restritos, com fases adicionais fixas (revisão de assets, planilhas de submissão, reescrita de IDs) e implementação **sequencial** ("a implementação dos pontos ocorre separadamente") existem como procedimentos locais de projeto. `human-loop-audit` é deliberadamente o procedimento **genérico** para séries **quaisquer** de apps/GUIs e delega reparos **imediatamente e em paralelo**, não como uma etapa posterior separada.
- **`bugsweep` / `bugfix-protocol`** — o trabalho de reparo propriamente dito, delegado por `human-loop-audit`; esta skill não repara nada por conta própria.

## Armadilhas

- **Não esperar a avaliação antes de abrir o próximo objeto** — um "esperar, depois avaliar, depois abrir o próximo" puramente sequencial desperdiça justamente a sobreposição que define esta skill.
- **Registrar o feedback de forma estruturada imediatamente**, em vez de acumulá-lo no histórico do chat — em caso de queda da sessão ele se perderia.
- **Não iniciar objetos às cegas** quando se sabe que um deles é instável — verificar brevemente se ele inicia antes de o usuário ficar diante dele ao vivo.
- **Delegação imediata, não reunida no final** — caso contrário o reparo só começa quando o usuário já terminou os testes, e a vantagem de tempo do procedimento se perde.

## Exemplos de gatilho

- "human-loop-audit"
- "Vamos testar os apps em zíper."
- "Eu testo, você avalia e repara."
- "start" (após anúncio prévio de um Human-Loop-Audit, como sinal de início para o passo 1)

## Changelog

### 1.0.0 (2026-08-18)
- Versão inicial. Procedimento adotado a partir de uma definição do usuário de 2026-08-18: auditoria em zíper com avaliação paralela + delegação imediata de reparos, delimitada em relação a `reissverschluss-merge` (merge no Git, mesma imagem do nome, sem relação) e a ciclos de teste por ondas mais restritos, locais do projeto (implementação sequencial em vez de paralela).
