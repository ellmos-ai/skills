---
name: llm-text-hygiene
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-07-04
updated: 2026-09-27
description: "Remove vestígios de IA, resíduos de chat, marcadores de substituição e padrões de estilo de LLM dos textos finalizados e verifica se a divulgação de IA está completa e corretamente posicionada."
standalone: true
anthropic_compatible: true
category: utilities
tags: [ai-disclosure, text-hygiene, qa, llm-cleanup, style-review]
status: active
language: pt
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
translated_from_sha256: 9e9a71e433f72af2e2b03d70aac610a348e967e9eb518a2e46c0b9af694e8f5d
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.663587+00:00"
---
<img src="banner.png" width="100%" alt="llm-text-hygiene banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `llm-text-hygiene`.



# Higiene de Texto LLM — Remover Vestígios de IA de Textos Finalizados (Deutsch)

## Visão Geral & Finalidade

Textos produzidos com apoio de IA acumulam resíduos que permanecem invisíveis no rascunho e
só se tornam constrangedores no documento publicado: trechos da sessão de chat, instruções de
direção que caem fora da estrutura argumentativa, agradecimentos ao modelo de linguagem,
marcadores de substituição que sobraram, padrões de estilo LLM intrusivos — e uma
divulgação de IA que falta, está mal posicionada ou já não é verdadeira. Esta skill é a
passagem sistemática de limpeza que precede a publicação: verificar, limpar de forma
conservadora, corrigir a divulgação. **Ela nunca altera a substância** — remove o que não faz
parte da obra.

## Catálogo de Verificação

Cinco classes de achados, do inequívoco (corrigir diretamente) ao delicado (apenas sinalizar):

### 1. Resíduo de Chat e Instruções de Direção (inequívoco → remover/corrigir)

Frases que pertencem à GERAÇÃO do texto, não ao texto: „Wie besprochen lassen wir
diesen Teil im Paper, da …", „Hier ist der überarbeitete Abschnitt:", „Gerne ergänze
ich …", fragmentos de prompt que sobraram, comentários meta dirigidos ao solicitante.
**Princípio de reconhecimento:** a frase cai para fora da estrutura do texto e da
argumentação — ela se dirige a uma situação de conversa em vez de ao leitor. Ao remover,
verificar se algum conteúdo residual precisa ser preservado (transferir a justificativa para
nota de rodapé ou para o texto).

### 2. Marcadores de Substituição e Marcadores de Obra em Andamento (inequívoco → resolver)

`[TODO: …]`, `[Referenz einfügen]`, `XXX`, `<hier Beispiel>`, seções vazias com
título, „(Quelle?)". Resolver ou — se não for possível — transferir como tarefa aberta real
para o TODO do projeto e remover do entregável.

### 3. Agradecimentos a LLM e Antropomorfismos (inequívoco → remover)

Agradecimentos ao ChatGPT/Claude/Gemini & Cia. não pertencem à seção de agradecimentos —
ferramentas não são agradecidas; seu uso é declarado na divulgação de IA. Remover também:
formulações antropomórficas sobre a ferramenta („die KI schlug freundlicherweise vor").

### 4. Divulgação de IA (verificar → corrigir)

- **Está presente?** Se o documento foi produzido com apoio de IA e a venue/projeto exige ou
  prevê uma divulgação: a seção existe?
- **Está correta?** Descreve o uso real (nem subestimado, nem exagerado)? Utiliza o esquema
  de divulgação do projeto/da venue, caso exista um definido (p. ex., níveis graduados)?
- **Está bem posicionada?** No local usual da venue (Métodos/entorno de Agradecimentos/
  seção própria), idêntica em todas as versões linguísticas.

### 5. Padrões de Estilo LLM (delicado → corrigir apenas casos claros, sinalizar o resto)

Transições formulaicas („Zusammenfassend lässt sich sagen", „Es ist wichtig zu betonen"),
inflação de enumerações onde deveria haver texto corrido, cadeias „nicht nur … sondern auch",
densidade de travessões, expressões de hedging, no inglês os marcadores conhecidos (entre
outros „delve", „tapestry", „it's worth noting"). **Cuidado:** o estilo é território do autor —
suavizar apenas a formulaicidade inequívoca e entregar todo o restante como lista de achados
ao autor, em vez de reescrever o texto. Soar humano não é o objetivo desta skill; o objetivo
é um texto sem corpos estranhos.

## Procedimento

1. **Definir o escopo:** quais entregáveis (arquivos), quais versões linguísticas? As alterações
   SEMPRE sincronizadas em todas as versões (conferência: `bilingual-doc-sync`).
2. **Varredura mecânica:** busca de texto integral pelos padrões de sinal (tabela abaixo) —
   barata, encontra de forma confiável as classes 2/3 e partes da 1.
3. **Passagem de leitura:** ler o documento ao longo da estrutura argumentativa — os achados
   da classe 1 só são reconhecidos estruturalmente (a frase se dirige à conversa em vez de ao
   leitor). Verificar especialmente: início/fim de seções, agradecimentos, introdução/conclusão
   (é aí que o resíduo aparece primeiro).
4. **Limpar:** corrigir diretamente as classes 1–3 (de forma conservadora, preservando a
   substância), corrigir a classe 4, emitir a classe 5 como lista de achados; suavizar
   diretamente apenas os casos inequívocos.
5. **Documentar:** o que foi encontrado/alterado/apenas sinalizado — em trabalhos com obrigação
   de versionamento, registrar se será necessária uma nova versão/reenvio.
6. **Periodicamente sobre um acervo:** combinar com `rotation-check` (um documento/projeto
   por execução, registro como memória).

**Ferramenta opcional para a classe 5 e a divulgação de IA:** mediante pedido explícito do
usuário — nunca automaticamente — pode-se usar [`pasta-press`](https://github.com/ellmos-ai/pasta-press)
(repositório público, 100% local via Ollama) para o refinamento de estilo:
`pastapress process <datei>` ou `pastapress text "…"`. Limite dos Red Flags acima:
esta skill não faz polimento por si mesma — pasta-press não substitui a passagem de leitura, e a
limpeza de marcadores (classes 1–4) continua sendo uma decisão de verificação desta skill,
independentemente de o pasta-press ser usado.

## Padrões de Sinal para a Varredura Mecânica

| Classe | Padrão de busca (DE) | Padrão de busca (EN) |
| --- | --- | --- |
| Resíduo de chat | „wie besprochen", „wie gewünscht", „hier ist", „gerne", „im Chat", „wie du sagtest", „lassen wir" | "as discussed", "as requested", "here is the", "I have added", "per your" |
| Marcador de substituição | `TODO`, `XXX`, `[…einfügen]`, `<…>`, „Quelle?" | `TBD`, `[insert`, `placeholder`, `citation needed` |
| Agradecimento a LLM | „Dank an ChatGPT/Claude/Gemini", „mithilfe von KI erstellt" (fora da divulgação) | "thanks to ChatGPT/Claude", "grateful to the AI" |
| Marcador de estilo | „zusammenfassend lässt sich", „es ist wichtig zu betonen", „nicht nur … sondern auch" | "delve", "tapestry", "it's worth noting", "in conclusion" |

A tabela é um ponto de partida, não um substituto para o filtro: os padrões geram candidatos, e a
decisão é tomada no contexto (passos 3–4). Para a higiene puramente mecânica de caracteres
(varredura de emojis, caracteres de controle, umlauts quebrados), usar as ferramentas existentes —
danos de codificação são território de `encoding-fix`, não desta skill.

## Exemplo & Aplicação

```text
Auftrag: „Prüf das Paper vor dem Upload auf KI-Rückstände."

1. Scope: paper_de.tex + paper_en.tex.
2. Scan: 1× "as discussed" (EN, Abschnitt 4), 1× "[TODO: Referenz Smith]" (beide),
   Danksagung erwähnt "wertvolle Hilfe von Claude".
3. Lese-Pass: In der Einleitung ein Satz, der den Reviewer direkt adressiert
   („Diesen Einwand behandeln wir wie gewünscht in 3.2") → Regieanweisung.
4. Fixes: Regieanweisung gestrichen (Inhalt steckte schon in 3.2), TODO als Aufgabe
   in TODO.md überführt + Platzhalter entfernt, LLM-Dank gestrichen, stattdessen
   AI-Disclosure-Abschnitt auf tatsächlichen Einsatz präzisiert — alles in DE und EN.
5. Vermerk: inhaltliche Änderung → neue Paperversion nötig, in TODO.md eingetragen.
```

## Red Flags

| Pensamento | Realidade |
| --- | --- |
| „Vou deixar o texto mais fluente logo" | Substância e voz pertencem ao autor — a skill remove corpos estranhos, ela não faz polimento. |
| „Achei marcadores de estilo → apagar" | A classe 5 é sinalizada, não reescrita automaticamente; suavizar apenas a formulaicidade inequívoca. |
| „A versão alemã basta" | O resíduo frequentemente aparece em APENAS uma versão — sempre verificar e manter sincronizadas todas as versões linguísticas. |
| „Tirar a divulgação, aí fica limpo" | Ao contrário: remover o agradecimento a LLM e INSERIR a divulgação correta — ocultar não é higiene. |

## Skills & Ferramentas Relacionadas

- `encoding-fix` — Reparação de bytes/codificação (mojibake); esta skill atua no nível do conteúdo.
- `bilingual-doc-sync` — Sincronização das versões linguísticas, nas quais as correções são incorporadas.
- `rotation-check` — Estrutura para a execução periódica sobre um acervo de documentos.
- `textproduction` — Geração de texto (esta skill é o QA posterior).
- [`pasta-press`](https://github.com/ellmos-ai/pasta-press) — ferramenta externa e pública
  (não é uma skill desta biblioteca): prensa de texto local com IA via Ollama para refinamento de
  estilo, tradução e remoção de marcadores. Opcional para a classe 5, apenas mediante pedido do
  usuário — esta skill não faz polimento por si mesma (ver Red Flags e Procedimento).

## Registro de Alterações

### 1.1.0 (2026-09-27)
- `pasta-press` (repositório público `ellmos-ai/pasta-press`) incluído como ferramenta opcional para a
  classe 5 (padrões de estilo) e para o refinamento da divulgação de IA — apenas mediante pedido do
  usuário; a limpeza de marcadores continua sendo uma decisão de verificação desta skill. Seção
  „Skills Relacionadas" ampliada para „Skills & Ferramentas Relacionadas". Todas as sete versões
  linguísticas atualizadas de forma sincronizada; `SKILL.fr.md` era, de fato, texto alemão não traduzido
  sob uma capa francesa — agora foi revisado como uma tradução francesa real.

### 1.0.0 (2026-07-04)
- Versão inicial. Abstraída da automação do Codex „research-llm-muster-check"
  (partes de chat em artigos, agradecimentos a LLM, divulgação de IA) e generalizada para textos
  de entregáveis arbitrários; catálogo de verificação ampliado com marcadores de substituição,
  padrões de estilo e tabela de sinais para a varredura.
