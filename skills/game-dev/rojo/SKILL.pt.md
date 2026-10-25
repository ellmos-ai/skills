---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Operar o Rojo — a ferramenta de sincronização do sistema de arquivos com o Roblox Studio para o desenvolvimento profissional em Roblox no VS Code / Claude Code, em vez do editor do Studio. Use esta skill sempre que o Rojo estiver envolvido: `rojo serve`/`rojo build`, escrever ou depurar `default.project.json`, rokit/rokit.toml e versões de ferramentas (Rojo, Lune, Wally), mapeamento de caminhos aninhado vs. plano (ReplicatedStorage.Project.shared), problemas de connect/porta/sincronização, ou quando for preciso criar a estrutura base de um projeto Roblox. Acione também com \"rojo connect não funciona\", \"os scripts acabam no lugar errado no Studio\", \"como mapear src/ para o Studio\", \"porta 34872 em uso\", \"ModuleScript vs Script no Rojo\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: pt
status: active
visibility: public
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rojo/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 2901142af2c1b72480d9cfaea5111557a8c6003c6b51aefa4bab02a0e168b742
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="rojo banner">

# Rojo — Sistema de arquivos → Sincronização com o Roblox Studio

## Finalidade

O Rojo conecta um projeto normal no sistema de arquivos (arquivos `.luau` em `src/`, versionados com Git)
ao Roblox Studio. Você escreve o código no editor de sua escolha (VS Code, Claude Code), e o Rojo
o sincroniza ao vivo com uma instância em execução do Studio. Assim, o código Roblox fica versionável,
comparável por diff e editável com ferramentas reais — em vez de viver no editor de scripts integrado do Studio.

Use esta skill para tudo que envolve a configuração do Rojo, o mapeamento `default.project.json`, a
cadeia de ferramentas (rokit/Wally/Lune) e problemas típicos de sincronização.

## Modelo mental

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**Regra central:** o sistema de arquivos é a fonte da verdade. A cada connect, o Rojo sobrescreve as áreas
mapeadas do Studio com o conteúdo do sistema de arquivos. Por isso, **nunca** edite código no Studio (será perdido na próxima
sincronização), edite apenas no editor. O `Workspace` (cena 3D, terreno) **não** é mapeado pelo Rojo e
permanece intacto — veja a skill `/rbx-studio` para o fluxo cena-vs-código.

## Extensões de arquivo → tipo Roblox (convenção do Rojo)

O Rojo deriva o tipo da instância a partir da extensão. Esta é a fonte de erro mais comum:

| Arquivo            | Tipo Roblox   | `require()`-ável | Função                    |
| ------------------ | ------------- | --------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **sim**         | Módulo de lógica, definições |
| `Foo.server.luau`  | Script        | não             | Ponto de entrada do servidor |
| `Foo.client.luau`  | LocalScript   | não             | Ponto de entrada do cliente |
| `init.luau`        | torna-se o próprio nó de pasta | sim | transforma a pasta em ModuleScript |

> Regra prática: **apenas os pontos de entrada** são `.server.luau`/`.client.luau`. Tudo o que é carregado via
> `require()` **deve** ser um ModuleScript `.luau`. `require()` em um
> Script/LocalScript gera "Attempted to call require with invalid argument(s)".

## Comandos da CLI

```bash
rojo serve default.project.json     # Live-Sync-Server starten (Standard-Port 34872)
rojo serve                          # nutzt default.project.json automatisch
rojo build default.project.json -o game.rbxlx   # einmaliger Build → Place-Datei (XML)
rojo build default.project.json -o game.rbxl    # Build → Place-Datei (binär)
rojo plugin install                 # Rojo-Studio-Plugin installieren (einmalig)
rojo --version                      # installierte Version prüfen
```

Após `rojo serve`: no Studio, abra o plugin do Rojo → **Connect** (localhost:34872).
`rojo build` não exige o Studio em execução — ideal para CI, testes de fumaça e releases.

## `default.project.json` — o mapeamento

Este arquivo mapeia caminhos do sistema de arquivos para a hierarquia do DataModel do Roblox. Chaves:

- `name` — nome do projeto (exibição)
- `$className` — classe Roblox do nó (`DataModel`, `ServerScriptService`, `Folder`, …)
- `$path` — caminho do sistema de arquivos sincronizado sob esse nó (relativo à raiz do projeto)

Um modelo padrão pronto para uso está em [`assets/default.project.json`](assets/default.project.json).

### Plano vs. aninhado — a decisão mais importante

Seu código precisa corresponder ao mapeamento. Duas variantes:

**Plano** — o conteúdo de `src/server` vai diretamente para `ServerScriptService`:
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
→ o código referencia, por exemplo, `ReplicatedStorage.Config`, `ReplicatedStorage.GameEnums`.

**Aninhado** — o conteúdo vai para `ServerScriptService.ProjektName`:
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
→ o código referencia `ReplicatedStorage.ProjektName.shared.Config` etc.

Ambas são válidas. Decida-se por **uma** variante para todo o projeto e mantenha cada
caminho `require`/`WaitForChild` consistente com ela. Sintoma de incompatibilidade: `WaitForChild(...)`
fica travado indefinidamente (Infinite yield), porque o nó esperado está em outro lugar.

## Cadeia de ferramentas via rokit

[rokit](https://github.com/rojo-rbx/rokit) é o gerenciador de cadeia de ferramentas. Um `rokit.toml` no
projeto (ou pasta-mãe) fixa versões exatas das ferramentas → builds reproduzíveis em todas as máquinas. Se ele faltar, aparece `Failed to find tool 'rojo' in any project manifest file`.

`rokit.toml` padrão (veja [`assets/rokit.toml`](assets/rokit.toml)):
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> Observação de versão: 7.4.4 é a versão fixada de forma consistente no pipeline de referência.
> Projetos mais novos podem usar 7.6.x — antes disso, verifique com `rojo build` contra o projeto,
> pois o formato do projeto pode mudar entre versões principais.

Após clonar/configurar: `rokit install` instala todas as ferramentas fixadas.

- **Lune** — executor de Luau fora do Studio (testes unitários, scripts de build, processamento de assets).
- **Wally** — gerenciador de pacotes: `wally install` → `Packages/` → no Studio em
  `ReplicatedStorage.Packages`. As dependências ficam em `wally.toml` (veja
  [`assets/wally.toml`](assets/wally.toml)), por exemplo o framework `sleitnick/knit@1.7.0`.

## Criar um novo projeto

O script [`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) gera uma estrutura completa de Rojo (project.json, rokit.toml, wally.toml, `src/{shared,server,client,gui}/`
com arquivos iniciais, stub de KONZEPT):

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # flaches Mapping (Default)
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # verschachteltes Mapping
```

Depois: `cd MeinSpiel && rokit install && rojo serve`.

## Solução de problemas

| Sintoma | Causa | Solução |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | nenhum `rokit.toml` | criar `rokit.toml` com o pin do Rojo no projeto/pasta-mãe, `rokit install` |
| `require` gera "invalid argument(s)" | `require()` em um Script/LocalScript | apenas ModuleScripts `.luau` podem ser usados com require; verifique a extensão |
| Porta 34872 ocupada (`os error 10048`) | um processo antigo do Rojo está em execução | `tasklist \| grep -i rojo` → `taskkill //PID <PID> //F`, depois `rojo serve` de novo |
| Scripts vão para o lugar errado no Studio | mapeamento plano em vez de aninhado (ou o contrário) | ajustar `default.project.json` aos caminhos do código (veja acima) |
| `WaitForChild` fica travado | o nó esperado não existe / erro no servidor antes da criação | **verificar primeiro o console do servidor** em busca de erros; conferir o mapeamento e a ordem de criação |
| A sincronização não ocorre após renomear um arquivo | o Rojo não detecta o rename imediatamente | parar o servidor (Ctrl+C) e iniciá-lo de novo; no Studio, Disconnect→Reconnect |
| A alteração no Studio some após reconectar | edição no Studio em vez de no sistema de arquivos | alterar o código **somente** no editor; o Rojo sobrescreve as áreas mapeadas |

### Limitações conhecidas do Rojo

1. **Sem sincronização de terreno/workspace** — construa a cena 3D e o terreno no Studio ou gere-os por código.
2. **Sem merge de `.rbxl`** — os arquivos de place são binários e não podem ser mesclados pelo git. Nunca os use como fonte primária.
3. **Sem sincronização ao vivo no modo Play** — alterações feitas durante o Play são descartadas ao parar.
4. **Conversão de caminhos no Git Bash** — `/c/...` pode ser convertido para `C:/...` e quebrar os caminhos do Rojo; na dúvida, use caminhos relativos ou caminhos nativos do Windows.

## Linting (Selene)

Projetos Luau para Roblox costumam ser verificados com **Selene** (`selene.toml` na raiz,
`std = "roblox"`). Libere globais como `_G` via `global_usage = "allow"` se o projeto
as usar para estado compartilhado do cliente. Execute o Selene a partir do diretório com a definição da API do Roblox
(`roblox.yml`).

## Leitura complementar

- Skills irmãs: `/rbx-studio` (operação do Studio, MCP, assets), `/game-design`
  (funções, fluxos de trabalho, GDD), metaskill `/rbx-dev` (reúne as três + padrões de arquitetura).
- Documentação atual de engine/Rojo: Context7 MCP (`resolve-library-id` →
  `/websites/create_roblox_reference_engine`, `/roblox/creator-docs`) ou
  <https://rojo.space/docs/>.
- Se disponível neste sistema, há um pipeline de referência rico em projetos em
  `<your Roblox project pipeline>` (incluindo `ROJO_FAQ.md`, `SKILL.md`).

## Changelog

### 1.0.0 (2026-06-17)
- Versão inicial. Destilada do pipeline `.ROBLOX` (ROJO_FAQ, ROJO_START, _template),
  redigida de forma neutra quanto ao usuário.

## Skills relacionadas

- `roblox-team-lock` — reivindicações de arquivos, Studio e MCP quando vários agentes trabalham no mesmo projeto. Leia primeiro, depois reivindique, depois trabalhe, depois libere.
