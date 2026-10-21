---
name: using-blender
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-06-20
updated: 2026-06-20
description: "Habilidade geral de fluxo de trabalho com Blender para agentes de IA que trabalham com .blend, .fbx, .obj, .glb, glTF, materiais, inspeção de cenas, automação com bpy, execuções em lote headless do Blender, validação de exportação/reimportação, pré-visualizações e controle opcional via Blender MCP. Use quando uma tarefa pedir para abrir, inspecionar, criar, automatizar, converter, otimizar, renderizar ou verificar arquivos do Blender ou de ativos 3D de forma independente do usuário."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
dependencies: {'tools': ['blender'], 'services': [], 'protocols': [], 'python': []}
category: game-dev
tags: [blender, bpy, 3d, assets, fbx, glb, gltf, mcp]
language: pt
status: active
visibility: public
provenance: {'origin': 'custom', 'origin_path': 'skills/game-dev/using-blender', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: 7bfddc52a5ef221e1ec94d0aae4bbc1095390df9b944341075b64321ab8782ff
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="using-blender banner">

> **Português** — Versão oficial em português.


> **English Translation** — Official English version of `using-blender`.


# Usando o Blender

## Regra central

Trabalhe com o Blender em três modos, conforme a tarefa:

1. **Modo GUI:** abrir o Blender com interface visível quando o usuário quiser ver, avaliar ou editar manualmente um ativo.
2. **Modo headless:** usar `blender --background --python <script.py>` quando forem solicitadas exportação, reimportação, processamento em lote ou verificação determinística.
3. **Modo MCP:** usar somente quando um addon do Blender em execução estiver conectado de forma intencional e for necessário controle da cena em tempo real. Antes, verificar a situação de segurança e licença.

## Fluxo padrão

1. Esclarecer o objetivo: visualizar, criar, converter, otimizar, renderizar ou verificar.
2. Ler os arquivos existentes: manifesto, README, formatos de exportação e resultados de verificação já disponíveis, primeiro.
3. Determinar o caminho do Blender: `blender` no PATH, configuração específica do projeto ou caminho do usuário. Não gravar caminhos locais privados em documentação publicável.
4. Para automação, usar um pequeno script `bpy` que torne explícitos as entradas, as saídas e os erros.
5. Após cada exportação, executar pelo menos uma verificação de reimportação ou carregamento antes de considerar o resultado utilizável.
6. Documentar os artefatos de forma concisa: origem, formatos de exportação, versão da ferramenta, status da verificação e limitações conhecidas.

## Regras de exportação e verificação

- Para uso geral na web/pré-visualização, preferir `.glb`.
- Para game engines e intercâmbio com DCC, oferecer adicionalmente `.fbx` ou `.obj/.mtl` quando o fluxo de destino exigir.
- Em roundtrips, sempre verificar: o arquivo existe, não está vazio, pode ser reimportado e os nomes esperados de objetos/materiais estão presentes.
- Para ativos grandes, coletar métricas: quantidade de malhas, materiais, bounding box, tamanho do arquivo e, opcionalmente, contagem de triângulos.
- Para verificações de renderização, usar pré-visualização em resolução baixa antes de iniciar renders custosos em Cycles ou Full HD.

## Regras de segurança

- Código `bpy` é Python local com acesso ao sistema de arquivos. Executar apenas scripts escritos por você mesmo ou auditados.
- Não ativar addons de Blender de terceiros, downloaders de ativos nem servidores de telemetria sem verificação de licença e de privacidade.
- Em servidores MCP com uma ferramenta `execute_python` genérica, limitar previamente escopo, rede, diretório de trabalho e timeout.
- Para ativos de marketplace ou externos, verificar a licença separadamente. A capacidade técnica de carregamento não substitui os direitos de uso.

## Opções de MCP

Para controle em tempo real, leia [references/blender-mcp-review.md](references/blender-mcp-review.md) quando um servidor Blender MCP for selecionado, instalado ou avaliado.

## Registro de alterações

### 1.0.0 (2026-06-20)
- Habilidade inicial e independente do usuário para Blender, com roteamento para GUI, headless e MCP.

## Verificar o resultado sem abrir a GUI

Para ativos há um gate de segundo plano pronto, que entrega **quatro renders e métricas mensuráveis**
em uma única execução (rotação, pivô, peças flutuantes):

```powershell
blender.exe --background --factory-startup `
  --python "<OneDrive>\.TOPICS\.ROBLOX\_tools\verify_asset_visual.py" -- `
  --fbx "<asset.fbx>" --out "<ordner>" --json
```

Sem GUI, sem necessidade de foco. Detalhes e limites (entre outros: o servidor MCP `ellmos-blender-use`
**não** consegue renderizar): `.ROBLOX\BLENDER_ASSET_CHANNELS.md`.
Fluxo de trabalho mais detalhado: habilidade `build-assets-with-blender`.
