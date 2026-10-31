---
name: iterative-bundle-selection
version: 1.2.0
type: skill
author: Lukas Geiger
created: 2026-08-25
updated: 2026-08-25
description: "Reduzir listas grandes de candidatos gradualmente por meio de poças temáticas opcionais, etapas de filtragem e pacotes reembaralhados repetidamente. Usar quando o usuário quiser selecionar habilidades, tarefas, ideias, arquivos ou outras entradas em grupos, filtrá-las por características ou embaralhar apenas dentro de áreas temáticas comuns, sem descartar definitivamente as demais entradas."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, auswahl, datenreduktion, buendel, choice-overload, workflow]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'local_changes_since_sync': True}
translated_from_sha256: 947358cbebcf01dc7e4e4d15c4cf25da6fe10d5454a7e8fc0aa03788bf88f70f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.553407+00:00"
---
<img src="banner.png" width="100%" alt="iterative-bundle-selection banner">

# Seleção Iterativa de Pacotes

Reduzir conjuntos grandes de seleção com poucas decisões amplas, sem descartar prematuramente os candidatos não escolhidos.

## Princípio básico

1. Registrar todos os candidatos como um pool comum e nomeá-los de forma inequívoca.
2. Opcionalmente, definir poças temáticas e atribuir cada candidato a exatamente uma poça primária.
3. Aplicar os filtros desejados em sequência, globalmente ou dentro de poças individuais, mantendo seus resultados separados.
4. Dentro de cada poça ativa, embaralhar e formar pacotes de cinco candidatos por padrão.
5. Rotular os pacotes da primeira rodada de forma inequívoca por poça, com `THEMA-A`, `THEMA-B` …
6. Deixar o usuário selecionar pacotes inteiros.
7. Retirar os candidatos dos pacotes selecionados do pool aberto e encaminhá-los à próxima ação.
8. Devolver os candidatos dos pacotes não selecionados à sua respectiva poça.
9. Manter poças e filtros, embaralhar cada poça separadamente e usar rótulos com traço.
10. Continuar com rodadas adicionais até que o usuário pare ou o pool esteja vazio.

Um último pacote pode conter menos de cinco candidatos. Pacotes não selecionados significam "ainda em aberto", não "rejeitado".

## Fluxo de trabalho

### 1. Preparar o pool

- Remover duplicatas com base em nomes ou IDs estáveis.
- Excluir candidatos já selecionados ou concluídos.
- Marcar candidatos bloqueados, mas não excluí-los silenciosamente.
- Informar o tamanho do pool inicial.

### 2. Formar poças temáticas

Uma poça temática é um subpool delimitado. Candidatos de poças diferentes não são embaralhados entre si.

- Usar o método somente se o usuário solicitar poças temáticas ou se considerar explicitamente útil uma separação temática.
- Documentar as poças com ID estável, título, regra de atribuição e número de candidatos.
- Derivar as poças de instruções do usuário, categorias existentes ou características rastreáveis.
- Mostrar de forma transparente as atribuições derivadas automaticamente antes da primeira ação subsequente.
- Atribuir cada candidato, por padrão, a exatamente uma poça primária; não criar duplicatas silenciosas em várias poças.
- Manter candidatos ambíguos em `UNZU — Unzugeordnet` até que uma atribuição seja definida.
- Emitir uma poça com menos de cinco candidatos como pacote pequeno; nunca completá-la com outro tema.
- Os filtros podem valer globalmente para todas as poças ou localmente para uma poça nomeada.
- Candidatos filtrados mantêm sua atribuição de poça, para que retornem ao lugar correto ao serem reativados.
- Ao dividir, unir ou renomear uma poça, descartar e reformar apenas os pacotes afetados.

Exemplo:

```text
DEV  | Entwicklung     | 12 Kandidaten | DEV-A, DEV-B, DEV-C
MED  | Medien          |  7 Kandidaten | MED-A, MED-B
UNZU | Unzugeordnet    |  2 Kandidaten | UNZU-A
```

Em rodadas posteriores, indicar a profundidade da rodada pela letra do pacote: `DEV-A′`, `MED-B″`.

### 3. Aplicar etapas de filtragem

- Executar os filtros de forma opcional e na ordem indicada pelo usuário.
- Registrar cada filtro com ID estável, modo, regra e número de resultados.
- Realizar comparações de texto, por padrão, sem diferenciar maiúsculas de minúsculas.
- `exclude` remove os resultados apenas do pool ativo e os coloca no pool de filtrados.
- `include` mantém apenas os resultados no pool ativo; os não correspondentes passam ao pool de filtrados.
- Se o modo não for indicado e o usuário disser que o pool deve ser filtrado ou limpo, usar `exclude` e informar essa suposição.
- Após cada etapa, informar o tamanho de entrada, o número de resultados e o tamanho restante.
- Nunca excluir candidatos filtrados nem marcá-los como rejeitados; o usuário pode desativar filtros individuais depois.

Exemplo:

```text
F1 | exclude | Name enthält "aws"         | 13 Treffer
F2 | exclude | Name enthält "hyperframes" | 8 Treffer
Aktiver Pool: 44 | Filterpool: 21
```

Se um filtro mudar, descartar todos os pacotes existentes do pool ativo e só então reembaralhar.

### 4. Formar a rodada

- Embaralhar realmente os candidatos; não apenas renomear a antiga estrutura de pacotes.
- Usar, sempre que possível, cinco candidatos por pacote.
- Embaralhar entre si apenas candidatos da mesma poça temática.
- Não duplicar nem perder candidatos.
- Quando candidatos dependerem uns dos outros, marcar a dependência em vez de omiti-la.

Formato de saída:

```text
Bündel DEV-A: dev-1, dev-2, dev-3, dev-4, dev-5
Bündel MED-A: media-1, media-2, media-3
```

Sem poças temáticas, continuar usando os rótulos simples `A`, `B`, `C` …

### 5. Processar a seleção

- Aceitar respostas como `A, D und F`.
- Antes de uma ação subsequente, listar novamente por completo os candidatos incluídos.
- Verificar bloqueios, pré-requisitos ou simulações (dry-runs) necessários por candidato.
- Registrar como selecionados ou concluídos os candidatos bem-sucedidos.
- Devolver ao pool restante os candidatos bloqueados ou que falharam.

### 6. Reagrupar o pool restante

- Remover definitivamente apenas os candidatos que realmente tiveram sucesso.
- Devolver todos os demais candidatos às suas poças anteriores e embaralhá-los separadamente ali.
- Reaplicar os filtros ativos ao pool restante antes de cada novo embaralhamento.
- Rotular a próxima rodada com traço: `DEV-A′`, depois `DEV-A″` etc.
- Informar o pool total, o pool de filtrados, o tamanho do pool ativo e o tamanho de cada poça.

## Regras de proteção

- Nunca interpretar a não seleção como rejeição definitiva.
- Nunca descartar silenciosamente os resultados de filtros; eles permanecem recuperáveis no pool de filtrados.
- Nunca ultrapassar os limites das poças ao embaralhar.
- Não duplicar nem mover candidatos entre poças ao redistribuí-los, a menos que o usuário altere a divisão.
- Não perder candidatos por causa de uma combinação desfavorável de pacotes.
- Não forçar candidatos bloqueados; eles permanecem em aberto.
- Em ações subsequentes irreversíveis ou de alto risco, pedir confirmação de cada candidato individualmente.
- Se necessário, documentar uma chave de embaralhamento reproduzível; caso contrário, basta uma nova distribuição rastreável.
- O método reduz a complexidade da seleção, mas não substitui a avaliação técnica de candidatos individuais.

## Delimitação

- `decide` avalia uma decisão concreta com critérios e frameworks.
- `decision-briefing` coordena várias questões de decisão diferentes.
- `iterative-bundle-selection` reduz um grande pool de candidatos semelhantes por meio de escolhas repetidas em grupo e reembaralhamento.

## Encerramento

O procedimento termina quando o pool estiver vazio, quando o usuário pedir expressamente para parar ou quando restarem apenas candidatos que exijam decisão individual. Em seguida, apresentar um breve balanço com selecionados, em aberto e bloqueados.

## Registro de alterações

### 1.2.0 (2026-08-25)

- Adicionadas poças temáticas opcionais como divisores do pool.
- Definidos embaralhamento vinculado a poças, filtros locais, rótulos inequívocos de pacotes e tratamento de `UNZU`.

### 1.1.0 (2026-08-25)

- Adicionadas etapas reversíveis de filtragem `include` e `exclude` antes do reembaralhamento.
- Definidos registro de filtros, pool de filtrados e recálculo de pacotes existentes.

### 1.0.0 (2026-08-25)

- Registrados pacotes iterativos de cinco, rodadas com traço, pool restante e devolução de bloqueados como procedimento independente de redução de dados e decisão.
