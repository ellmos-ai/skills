---
name: paveman
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-20
description: "Detecta pedidos para encurtar um arquivo de regras ou de memória (\"encurta meu CLAUDE.md\", \"MEMORY.md está muito longo\", \"comprime a documentação sem alterar a parte técnica\", \"este arquivo de regras é cortado pelo limite de caracteres\") e usa para isso o módulo paveman — uma ferramenta CLI determinística, sem modelo, para encurtar prosa em arquivos Markdown/texto, com execução de simulação como padrão, reversão e um validador rigoroso de proteção para caminhos, títulos e código. Use esta skill em frases como \"encurta <Datei>\", \"este arquivo está longo demais/está sendo cortado\", \"shrink this rule file\", \"comprime sem alterar o conteúdo\" ou quando um arquivo de regras ou de memória claramente atinge um limite de caracteres ou de linhas."
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [kürzen, kompression, regeldatei, gedächtnis, deterministisch, dry-run, rollback, dokumentation]
language: pt
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [paveman]
  services: []
  protocols: []
  python: []
  modules: [paveman]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: cb1c7bfcbc7a4592a1df4a844c4e3d2a5f5da3f268d81b246c0ce05024927bc1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:10.711777+00:00"
---
<img src="banner.png" width="100%" alt="paveman banner">

# Paveman — Encurtar de forma determinística arquivos de regras e de memória

> Wrapper de skill fino e neutro quanto ao usuário, em torno do módulo `paveman`, disponibilizado separadamente.
> A skill identifica quando a ferramenta é adequada e descreve seu fluxo seguro. Ela não pressupõe
> uma máquina específica, um caminho de instalação fixo nem um perfil pessoal.

## Quando esta skill se aplica

Os gatilhos são frases do usuário que querem encurtar um **arquivo existente de regras, convenções ou memória**
sem alterar seu conteúdo técnico:

- "Encurta `<Datei>`" / "este arquivo está longo demais" / "é cortado em X caracteres ou linhas"
- "Comprime a documentação sem alterar a parte técnica ou o código"
- "MEMORY.md ou CLAUDE.md ficou cheio demais"
- "Deixa este arquivo de regras mais curto, mas mantém o significado"
- Qualquer variante que se refira a **encurtar um arquivo existente**, não a **escrever algo novo** e não a
  **traduzir** (veja a delimitação abaixo)

**Não** é esta skill:

- **`knappform`** — altera a forma como o próprio modelo se expressa na conversa em andamento
  (estilo de comunicação do LLM, baseado em modelo, sem acesso a arquivos). `paveman`, por outro lado, altera
  o conteúdo de um arquivo existente de forma determinística e sem chamada ao modelo. Ambos podem
  coexistir; são técnica e funcionalmente separados.
- **`bilingual-doc-sync`** — completa versões de idioma que faltam. `paveman` encurta uma versão
  e não traduz nada.
- **`llm-text-hygiene`** — remove vestígios de IA ou restos de chat dos textos. Essa finalidade é diferente
  de encurtar.
- Escrever ou inventar conteúdo novo — `paveman` encurta apenas o que já existe.

## O que o módulo faz

`paveman` é um encurtador de prosa determinístico e baseado em regras para arquivos Markdown e de texto:
sem chamada a modelo, sem tokens e sem envio pela rede. A forma de disponibilização pode variar de sistema
para sistema; o que vale é a versão do módulo ou pacote autorizada naquele ambiente.

| Flag | Efeito |
|---|---|
| *(sem flag)* | **Execução de simulação (padrão).** Mostra o diff e a economia de caracteres, sem gravar nada. |
| `--apply` | Grava de fato; antes disso é criada automaticamente uma cópia de segurança. |
| `--rollback` | Restaura a última cópia de segurança. |
| `--locker` | Informa desvios de caminho ou de títulos apenas como aviso, em vez de erro. |
| `--kontext N` | Define o número de linhas de contexto do diff. |

O **validador de proteção é executado em cada chamada**. Blocos de código, caminhos e títulos não podem
ser alterados. No modo padrão, um desvio impede a gravação, em vez de apenas ser informado.

## Fluxo — sempre nesta ordem

1. **Primeiro a simulação.** Execute `paveman <Datei>` sem `--apply`. Mostre ao usuário a economia de
   caracteres, o diff e o status do validador ("OK" ou a mensagem de erro concreta).
2. **Gravar somente com liberação explícita.** Só então execute `paveman <Datei> --apply`;
   nunca mude automaticamente da simulação para a gravação.
3. **Mencione `--rollback` antes de gravar.** O usuário deve saber de antemão como desfazer um
   resultado indesejado.
4. **Leve a sério os erros do validador.** Não use `--locker` apenas para contornar um erro.
   Verifique antes se o desvio é de fato inofensivo; o modo mais brando exige uma decisão consciente do usuário.
5. **Respeite o conteúdo curado.** Uma ferramenta baseada em regras não reconhece de forma confiável se uma
   formulação é intencionalmente detalhada. Em caso de dúvida, revise com cuidado o diff da simulação.

## Pré-requisito — verificar a disponibilidade do módulo

1. Use `paveman --help` para verificar se a CLI está disponível no ambiente atual.
2. Se o comando não existir, determine o caminho de módulo ou pacote autorizado para este sistema. Não invente
   estrutura de caminho local, nome de pacote nem repositório.
3. Se nenhuma fonte autorizada puder ser localizada, informe o pré-requisito ausente como um ponto de
   configuração próprio, em vez de executar a skill às cegas ou criar um módulo paralelo.
4. Após uma instalação, execute primeiro novamente `paveman --help` e depois uma simulação inofensiva; um
   teste de gravação real continua dependendo de liberação.

## Exemplos

```text
User: „Kürze meine CLAUDE.md, sie wird beim Sessionstart abgeschnitten.“

→ `paveman CLAUDE.md` (Trockenlauf)
→ Ergebnis: „12.400 → 9.800 Zeichen (-21 %), Validator: OK.“
→ Diff zeigen und auf `--rollback` hinweisen.
→ Nutzer bestätigt.
→ `paveman CLAUDE.md --apply`
```

```text
User: „MEMORY.md ist zu voll, kürze sie bitte.“

→ Trockenlauf: „893 → 893 Zeichen, keine Regel griff — der Text ist bereits knapp.“
→ Kein `--apply` empfehlen; den fehlenden Mehrwert ehrlich melden.
```


## Changelog

### 1.0.1 (2026-08-20)

- Wrapper público totalmente desvinculado de nomes de máquinas, caminhos locais de checkout, dados de instalação,
  referências privadas de tickets e resultados de testes locais.
- Acrescentado contrato neutro quanto ao usuário para disponibilidade e instalação, e corrigidos os caracteres
  alemães com umlaut.

### 1.0.0 (2026-08-19)

- Primeira versão pública do wrapper com simulação, etapa de liberação, reversão e limites do validador.
- Delimitação em relação a `knappform`, `bilingual-doc-sync` e `llm-text-hygiene`.
