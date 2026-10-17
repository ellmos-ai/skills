---
name: semantic-persona-routing
version: 1.1.0
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-09-03
description: "Cria e usa um grafo de roteamento semântico neutro quanto ao provedor, composto por personas, funções coordenadoras, especialistas e endpoints de skills ativos. Use quando um LLM precisar encaminhar uma solicitação de uma função líder, passando por um especialista, até um skill, extrair um roteador de personas portável de um sistema de agentes existente, combinar um mapa semântico de domínio com um registro lexical de skills, ou tornar visíveis conexões ausentes entre função e skill, em vez de recorrer silenciosamente a um substituto. Os gatilhos incluem roteamento semântico de personas, persona-umbrella, roteador de funções, roteamento boss-agent para especialista e skill, exportação de funções de agentes ou reutilização de personas entre vários provedores de LLM."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [persona, persona-authoring, semantic-routing, agents, experts, skills, umbrella, provider-neutral]
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
translated_from_sha256: 0b19c395645de38c2550f550de6a95670df63c86a2f555252d221c67f85b2dc3
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:53.391636+00:00"
---
<img src="banner.png" width="100%" alt="semantic-persona-routing banner">

# Roteamento Semântico de Personas

Roteie primeiro por capacidade e aplique a personalidade depois. Crie um mapa
portável que separe a escolha semântica de funções, a busca determinística de
endpoints e o carregamento específico de cada provedor.

## Modelo de Roteamento

```text
Anfrage
  -> semantische Domäne oder koordinierende Rolle
  -> Expertenfähigkeit
  -> ausdrücklich angegebener oder live aufgelöster Skill-Endpunkt
  -> optionales Persona-Overlay
  -> Anbieteradapter lädt und führt aus
```

Uma persona controla o estilo de comunicação, as prioridades e os padrões de
interação. Ela não concede ferramentas, permissões nem capacidades de domínio.
Uma função coordena, um especialista delimita o domínio, e um skill é o endpoint
executável.

## Criar o Mapa de Roteamento

Use metadados explícitos como fonte autoritativa e a similaridade lexical apenas
para encontrar candidatos:

```bash
python scripts/build_routing_map.py \
  --roles-dir path/to/roles \
  --personas-dir path/to/personas \
  --skills-dir path/to/skills \
  --out routing-map.json
```

O builder entende campos comuns do `SKILL.md`, como `type`,
`orchestrates.experts`, `parent_agents`, `skills`, descrições e
proveniência. Ele gera um mapa de execução sem que o sistema de origem precise
estar instalado. Leia [routing-map-schema.md](references/routing-map-schema.md) antes de
estender o formato.

Cada ID de skill exportado é único. Se vários arquivos de origem declararem o
mesmo ID estável, o builder escolhe de forma determinística o caminho relativo de
origem lexicograficamente primeiro e registra um problema `duplicate-skill-id`; nunca
emite duas entradas de skill com o mesmo ID. Referências declaradas a skills de
especialistas e personas só são normalizadas para um ID limpo se esse ID existir no
registro exportado. Referências malformadas, desconhecidas e normalizadas
permanecem visíveis em `issues`; referências desconhecidas ou inválidas
nunca se tornam endpoints nem vínculos de compatibilidade de personas.

Não promova `candidate_skills` automaticamente. Confirme-os primeiro por meio de um
resolvedor de skills ativo ou de metadados da origem.

## Criar e Colocar Personas

O núcleo gera mapas; ele não inventa personas. Quem quiser usar as próprias
personas deve colocá-las **ao lado do skill** e reconstruir o mapa:

```text
semantic-persona-routing/
  personas/<persona-id>.md          # eine Datei je Persona
  roles/<rolle>/SKILL.md            # koordinierende Rollen und Experten
  routing-map.json                  # erzeugte Karte
  config.json                       # host-lokal, nie veröffentlicht
```

O builder lê funções exclusivamente de arquivos `SKILL.md`; personas, de
qualquer arquivo Markdown com frontmatter. Copie
[templates/persona.template.md](templates/persona.template.md) para
`personas/<persona-id>.md` e preencha o contrato:

| Campo | Significado |
|---|---|
| `name`, `type: persona` | ID estável da persona e tipo |
| `persona.display_name`, `short_name`, `gender`, `role`, `default_prompt` | Exibição, nome curto, forma de tratamento, função em uma frase, frase de invocação do provedor |
| `parent_agents` | funções coordenadoras às quais a persona está associada |
| `skills` | **Nomes de skills, nunca caminhos** — somente estes são resolvidos para endpoints |
| `optional_skills` | skills vinculados ao host; se ausentes, permanecem como `GAP` visível |

Uma persona não pode conceder nem substituir ferramentas, permissões, decisões de
segurança, bloqueios ou decisões do usuário; ela é uma camada sobre a função e os
skills.

**Caminhos:** o skill não informa caminhos do host. `config.example.json` mostra o
padrão (`ellmos.skill-config.v1`, `einstellungen.paths` com marcadores como
`<HOME>/<ONEDRIVE>/<TOPICS>`); a cópia local do host se chama `config.json`, é
preservada no deploy e nunca é incluída no repositório.

**Limpar o catálogo:** uma biblioteca de skills com arquivos arquivados ou cópias
de referência gera muitos problemas `duplicate-skill-id`. `--skills-layout catalog` aceita
apenas `<kategorie>/<name>/SKILL.md` e ignora pastas com prefixo `_`
(`_archive`, `_reference`, `_templates`):

```bash
python scripts/build_routing_map.py \
  --roles-dir roles --personas-dir personas \
  --skills-dir path/to/skills --skills-layout catalog \
  --out routing-map.json
```

## Rotear uma Solicitação

### 0. Oferecer as Personas Existentes

Se houver personas ao lado do skill (`personas/`), liste-as na invocação
com nome de exibição, função e skills e roteie para a adequada; se a solicitação
não mencionar uma persona, escolha-a apenas no passo 4. O formato do comprovante de
roteamento permanece inalterado.

### 1. Escolher Semanticamente a Função Coordenadora

Compare a solicitação com nomes de funções, descrições e casos de uso. Prefira a
função mais específica capaz de coordenar toda a solicitação. Quando a confiança
for baixa, mantenha vários candidatos visíveis; pergunte ao usuário somente se a
escolha alterar substancialmente o resultado.

### 2. Escolher os Especialistas Dentro da Função

Use apenas especialistas vinculados à função coordenadora escolhida, a menos que a
solicitação envolva claramente várias funções. Uma solicitação direta a um
especialista pode pular a função coordenadora na execução, mas mantém essa
vinculação na explicação da rota.

### 3. Resolver os Endpoints Executáveis

Resolva nesta ordem:

1. `endpoint_skills` a partir de metadados explícitos da origem ou de proveniência exata;
2. um resolvedor externo atual de skills ou um localizador local de skills;
3. `candidate_skills` verificados;
4. uma `GAP` visível, quando nenhum endpoint existir.

Nunca roteie para um nome de especialista como se ele fosse um skill instalado. Um
endpoint ausente é uma lacuna de portabilidade, não permissão para inventar um
endpoint.

Leia [endpoint-resolution.md](references/endpoint-resolution.md) ao conectar um registro ativo,
um localizador lexical ou um carregador de skills específico de um provedor.

### 4. Aplicar a Camada de Persona

Escolha uma persona associada à função ou ao especialista selecionado. Se várias
personas forem adequadas, prefira a que tenha limites e estilo declarados
compatíveis com a tarefa. Não aplique persona alguma quando nenhuma estiver
explicitamente vinculada.

As instruções de persona não podem substituir regras de segurança, bloqueios,
decisões do usuário, limites profissionais ou permissões de ferramentas.

### 5. Carregar e Executar

Use o mecanismo nativo de carregamento de skills ou agentes do provedor. Antes da
execução, carregue as instruções dos skills ativos selecionados. Mantenha o roteador
enxuto; a execução pertence ao worker ou ao agente atual com os skills carregados.

## Comprovante de Roteamento

Retorne ou registre o seguinte:

```text
ROLE: <koordinierende Rolle oder direct>
EXPERT: <Experte oder n/a>
SKILLS: <verifizierte aktive Endpunkte>
PERSONA: <Overlay oder none>
RESOLUTION: explicit | provenance | live-resolver | verified-candidate | GAP
CONFIDENCE: high | medium | low
WHY: <ein kurzer Grund>
GAPS: <fehlende Endpunkte oder Warnungen vor veralteten Karten>
```

Recrie o mapa quando as funções de origem ou o conjunto de skills mudarem. Um
resolvedor ativo pode sobrepor um mapa desatualizado quanto à disponibilidade de
endpoints, mas não deve reescrever silenciosamente a taxonomia semântica de funções.

## Exemplo

Solicitação: "Organize meus recibos e prepare o resumo para o ano fiscal."

O roteador escolhe uma coordenação de escritório, em seguida o especialista em
impostos, resolve o skill de impostos instalado e, por fim, aplica uma persona de
impostos cuidadosa explicitamente vinculada. Se o especialista em impostos existir,
mas não houver um skill de impostos portável, ele registra `GAP` e
continua apenas por um caminho substituto explicitamente configurado.

## Registro de Alterações

### 1.1.0 (2026-09-03)

- Criar e colocar personas: convenção de armazenamento ao lado do skill, contrato
  de frontmatter, modelo neutro `templates/persona.template.md`, convenção de caminhos com
  `config.example.json`, comportamento de invocação (oferecer personas existentes) e
  `--skills-layout catalog` contra IDs de skill duplicados de cópias de arquivo e
  referência.

### 1.0.0 (2026-07-28)

- Extraída a cadeia neutra quanto ao provedor de funções, especialistas e skills
  de um roteador de domínio já testado, com criação portável de mapas e lacunas de
  endpoint visíveis.
