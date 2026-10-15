---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Operação do Roblox Studio para desenvolvimento de jogos — o editor visual no qual a cena 3D é construída, testada e publicada. Use esta skill para: noções básicas do Studio (Explorer, Workspace, teste de jogo, salvar o lugar como .rbxl), a interação com o Rojo (Connect, modo cena-vs-código), controle por IA do Studio via Roblox-Studio-MCP (execute_luau, insert_from_creator_store, generate_material, screen_capture, Play/Stop, leitura do Console), o fluxo completo do pipeline de assets (Creator Store → limpeza → kit → cena → .rbxl → o Rojo o traz à vida) e, acima de tudo, a verificação de malware OBRIGATÓRIA para assets do marketplace. Também acione para \"incorporar um asset da Store\", \"Studio MCP não funciona\", \"studios: []\", \"gerar material\", \"salvar cena\", \"este asset do Roblox é seguro\", \"scripts desaparecem após Play\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: pt
status: active
visibility: public
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 9d0fca2a40692abba63ce104ab8f69627490f5cd4adf2ead8a6da3ad00f4d7b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.532187+00:00"
---
<img src="banner.png" width="100%" alt="rbx-studio banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **Nota:** Não afiliado à Roblox Corporation; "Roblox" é uma marca registrada de seus proprietários. "rbx" é a abreviação comum da comunidade.

# Roblox Studio — Editor, Teste, Assets, MCP (Deutsch)

## Visão geral e finalidade

O Roblox Studio é o editor oficial: construa a cena 3D, teste o jogo no modo de jogo, insira assets da Creator Store e publique o lugar. Em um fluxo de trabalho com Rojo, o Studio é responsável pela **cena** (Workspace, Terrain, modelos posicionados) e pelo **teste** — o **código** chega via Rojo a partir do sistema de arquivos (veja a skill `/rojo`).

Esta skill cobre: noções básicas do Studio, a separação limpa entre trabalho de cena e de código, controle por IA via Roblox-Studio-MCP e o fluxo de assets, incluindo a **verificação obrigatória de malware** para cada asset do marketplace.

## Noções básicas

- **Explorer** — árvore de todas as instâncias (Workspace, ServerScriptService, ReplicatedStorage, …). Com o Rojo ativo, as áreas mapeadas são preenchidas ao vivo a partir do sistema de arquivos.
- **Teste de jogo (Play-Test)** — o botão verde Play (ou F5) inicia uma sessão local de servidor+cliente. Após cada início, **verifique o console Output em busca de erros** — o reflexo de depuração mais importante.
- **Salvar lugar** — Arquivo → Salvar como → `.rbxl` (binário) ou `.rbxlx` (XML, comparável por diff). O lugar salvo contém a **cena**. O código fica no sistema de arquivos, não no lugar.

## O fluxo crítico: modo cena vs. modo código

Ao conectar, o Rojo sobrescreve todas as áreas de script mapeadas com o conteúdo do sistema de arquivos. A `Workspace` (cena 3D) **não** é mapeada e permanece intacta. Disso decorre a regra mais importante do trabalho diário — nunca misture os dois modos:

**Modo A — editar a cena (Rojo DESLIGADO):**
1. Pare o servidor Rojo (`taskkill //F //IM rojo.exe` ou Ctrl+C).
2. Abra o lugar no Studio, posicione assets, construa o mundo, organize.
3. Arquivo → Salvar → a `.rbxl` agora contém a nova cena.

**Modo B — testar o código (Rojo LIGADO):**
1. Abra o mesmo lugar no Studio.
2. Inicie `rojo serve` → no plugin Rojo do Studio → Connect.
3. Pressione Play e teste. O Rojo sincroniza os scripts; o Workspace vem da `.rbxl`.
4. Enquanto o Rojo estiver em execução, **não** salve (caso contrário, o estado do Rojo congela na `.rbxl`).

Assim, o trabalho de cena (Studio) e o de código (editor + Rojo) podem ocorrer em paralelo e sem conflitos — artistas constroem cenas, desenvolvedores escrevem código.

## Roblox-Studio-MCP — a IA controla o Studio

O Roblox-Studio-MCP permite que Claude/Gemini/Codex controlem diretamente uma instância **em execução** do Studio: executar código, inspecionar, Play/Stop, ler o Console, inserir assets. Ele **não** substitui o Rojo — ele o complementa: Rojo para alterações persistentes de código, MCP para inspeção, testes, inserção de assets e geração de materiais.

```
Editor + Rojo  ──(persistenter Code-Sync)──►  Studio (laufend)  ◄──(Inspektion/Test/Insert)──  MCP ◄── KI
```


### Ferramentas MCP disponíveis (típicas)

| Ferramenta | Finalidade |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | listar instâncias abertas / selecionar a ativa |
| `search_game_tree` / `inspect_instance` | pesquisar a hierarquia / ler propriedades |
| `execute_luau` | executar código Luau diretamente no Studio |
| `script_read` / `script_grep` / `script_search` | analisar scripts |
| `multi_edit` | alterar várias instâncias/scripts em lote |
| `start_stop_play` | controlar Play/Stop |
| `get_console_output` | ler o log Output |
| `screen_capture` | captura de tela da cena |
| `insert_from_creator_store` | inserir um asset da Creator Store |
| `generate_material` | gerar um material/textura por IA (MaterialVariant) |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | simular entrada |

### Configuração (neutra quanto ao usuário)

O MCP roda como um servidor incluído com o Studio, frequentemente conectado por meio de um wrapper fino de filtragem JSON (ele filtra banners que não são JSON e que alguns clientes não conseguem interpretar):

- Lote MCP (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- wrapper opcional: `<your roblox-mcp wrapper>`
  (se presente neste sistema; compartilhado por Claude/Codex/Gemini)
- Configurações do cliente: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

Entrada de exemplo (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "node",
      "args": ["<your roblox-mcp wrapper>",
               "cmd.exe", "/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```


### Problemas comuns do MCP

| Sintoma | Significado / correção |
| --- | --- |
| `studios: []` ou `Not connected to WS host` | não necessariamente "quebrado": envie `initialize` → aguarde 2–3 s → `list_roblox_studios`; caso contrário, reinicie o Studio |
| `Error: connection closed: initialized request` | o Studio não está aberto — inicie o Studio, carregue o lugar e tente novamente |
| scripts escritos via MCP desaparecem após Play/Stop | edições de código via MCP não são persistentes — para alterações duradouras de código use o **Rojo** |
| valor via `require()` na VM do plugin está incorreto | a VM do plugin tem seu próprio cache de require — para verificar, leia `.Source` diretamente ou verifique o log do servidor após Play |

## Pipeline de assets (Creator Store → jogo)

Primeiro o greybox (jogabilidade), depois os assets (antes do lançamento). A sequência comprovada:

```
STORE DURCHSUCHEN   → z. B. "medieval" → mehrere Kandidaten laden
AUSSORTIEREN        → stilfremde/hässliche raus, 5–8 passende behalten
BEREINIGEN          → ALLE Scripts entfernen (Malware!), nur Geometrie/Meshes behalten
KIT / SET BAUEN     → aus Basis-Assets Varianten ableiten (gleiche Materials/Proportionen)
SZENE BAUEN (Studio)→ Assets zur Kulisse zusammensetzen (Dorf, Arena, Park)
ALS .RBXL SPEICHERN → die Kulisse ist die "Bühne"
ROJO BELEBT ES      → Scripts/Gameplay/HUD kommen per Rojo dazu; Workspace bleibt unangetastet
```


**Técnica de variantes ("kit modular"):** Pegue um bom asset base e derive um conjunto inteiro a partir dele (casa → torre, celeiro, ferraria, ruína). Todos compartilham materiais, cores e proporções → uma aparência consistente com esforço mínimo, da forma como estúdios profissionais fazem.

**Fontes de assets (prioridade):** Creator Store (gratuita, enorme, **verificação de malware obrigatória**) → materiais por IA (`generate_material`) → malhas próprias (Blender → .fbx) → pacotes de assets comprados.

## OBRIGATÓRIO: verificação de malware para assets do marketplace

Os assets da Creator Store podem conter scripts maliciosos ofuscados (backdoors, código remoto, ganchos de redes de bots). Verifique **cada** asset importado antes do uso e remova todos os scripts — mantenha apenas geometria/malhas.

- Referência de padrões: [`references/malware-patterns.md`](references/malware-patterns.md) — os 8 padrões de ofuscação conhecidos (payload de atributo invertido, script de sistema falso, remoto `require()`, `loadstring`, `string.char`, `getfenv/setfenv`, Values ocultos, execução atrasada).
- Verificador: [`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — execute-o no Studio via `execute_luau` (ou a Barra de Comandos); ele verifica uma instância contra todos os padrões e relata os achados.

**Sinais de alerta imediatos:** um script grande em um modelo puramente decorativo · strings invertidas em atributos · `require(<number>)` · `loadstring` · `HttpService` em um asset que não precisa de rede. Na dúvida: exclua o script. Documente os achados (por exemplo, `_malware_reports/YYYY-MM-DD_*.md` no pipeline de referência).

## Armadilhas importantes de Luau/Studio (trecho)

As mais comuns que causam problemas no Studio — a lista completa é mantida pela skill `/rbx-dev`:

- `Model.Position` não existe → `model:GetPivot().Position`.
- `tick()` está obsoleto → `os.clock()` / `workspace:GetServerTimeNow()`.
- `SetPrimaryPartCFrame()` obsoleto → `model:PivotTo(cf)`.
- Chamadas de DataStore **sempre** em `pcall`.
- Baseplate + piso procedural na mesma altura → Z-fighting (cintilação): remova o baseplate ou eleve o piso em +0,1 studs.
- Fique atento ao orçamento de partes (~50–80 partes por sala gerada proceduralmente).

## Leitura adicional

- Skills irmãs: `/rojo` (sincronização, configuração do projeto), `/game-design` (papéis, fluxos de trabalho, GDD), skill meta `/rbx-dev` (padrões de arquitetura + todas as lições de Luau).
- Documentação do motor/Creator: Context7 MCP (`/websites/create_roblox_reference_engine`, `/roblox/creator-docs`) ou <https://create.roblox.com/docs>.
- Pipeline de referência (se presente): `<your Roblox project pipeline>` (`ROBLOX_MCP_FAQ.md`, `ASSET_PIPELINE.md`, `_malware_reports/PATTERNS.md`).

## Registro de alterações

### 1.0.0 (2026-06-17)
- Versão inicial. Destilada do pipeline `.ROBLOX` (ROBLOX_MCP_FAQ, ASSET_PIPELINE, PATTERNS, LESSONS_LEARNED), escrita de forma neutra quanto ao usuário.
