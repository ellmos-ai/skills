---
name: video-transcriber
version: 1.2.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-08-24
description: "Obter transcrições de vídeo (legendas) e metadados de fontes de vídeo online e exibi-los como Markdown, JSON ou texto simples. Atualmente suportado: YouTube. Dá preferência a legendas criadas manualmente e recorre às geradas automaticamente quando necessário."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: caf55e3434119acd935dad208f5461f7a08e72d34b595314abd52b58469cd299
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.778562+00:00"
---
<img src="banner.png" width="100%" alt="video-transcriber banner">

# Transcritor de vídeo

Obtém transcrições (legendas) e metadados (título, canal, data, visualizações,
descrição) de vídeos online. Dá preferência a legendas criadas manualmente, com
recurso às geradas automaticamente. Saída em Markdown, JSON ou texto simples.

Se o caminho primário (`youtube-transcript-api`) não retornar nada, entra automaticamente um
segundo caminho através dos metadados do yt-dlp. Ele lê exclusivamente a faixa de
legendas que a plataforma já entrega para reprodução — **sem download de vídeo ou
áudio**. Qual caminho foi usado consta no campo `source` da saída JSON e no stderr.

Para cada idioma desejado, o recurso de fallback prioriza faixas manuais exatas e
de idioma base antes das automáticas exatas e de idioma base; faixas arbitrárias
vêm só depois. Uma faixa JSON3 ilegível não interrompe a busca, enquanto houver
outra candidata disponível.

Fonte atualmente suportada: **YouTube** (youtube.com, youtu.be, youtube-nocookie.com).

Para vídeos, use esta ferramenta em vez de resumir o conteúdo manualmente —
a transcrição é a fonte confiável.

> **Aviso:** Esta ferramenta não é afiliada ao YouTube ou ao Google e não é
> suportada nem endossada por eles. O uso é de responsabilidade própria. Os
> usuários são responsáveis por cumprir os termos de uso da respectiva
> plataforma e o direito autoral aplicável. Não contornar DRM, paywalls ou
> restrições de acesso; nenhuma coleta de dados em massa; nenhuma republicação
> de transcrições protegidas sem consentimento dos detentores de direitos.

## Dependências e licenças

```bash
pip install youtube-transcript-api   # Transkripte (Pflicht) — MIT-Lizenz
pip install yt-dlp                   # Metadaten (optional, Fallback: noembed) — Unlicense (Public Domain)
```

## Uso

> **Nota para Windows:** Defina sempre `PYTHONIOENCODING=utf-8`, caso contrário os
> acentos e caracteres especiais quebram na saída (codificação cp1252).

```bash
# Standard: Markdown mit Timestamps
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Ausgabeformat waehlen
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# In Datei speichern
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# Sprachen bevorzugen (Default: de en)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### Opções

| Opção | Efeito |
|-------|--------|
| `--format markdown\|json\|plain` | Formato de saída (padrão: markdown) |
| `--output, -o <datei>` | Grava em arquivo em vez de stdout |
| `--lang <codes...>` | Idiomas de legenda preferidos (padrão: de en) |
| `--meta-only` | Somente metadados, sem transcrição |
| `--transcript-only` | Somente transcrição, sem metadados |
| `--no-timestamps` | Transcrição sem marcas de tempo |
| `--no-meta` | Mais rápido: pula os metadados do yt-dlp |
| `--allow-empty-transcript` | Considera transcrição vazia como sucesso (saída 0 em vez de 3) |

### Códigos de saída

Uma transcrição vazia **não** é sucesso. Antes da 1.2.0, esse caso terminava com
saída 0: o arquivo de saída era gravado, o array de segmentos estava vazio, e
qualquer automação chamadora considerava isso bem-sucedido. Essa falha silenciosa
é exatamente o defeito que a 1.2.0 elimina.

| Código | Significado |
|--------|-------------|
| `0` | Sucesso — transcrição presente, ou `--meta-only`, ou `--allow-empty-transcript` |
| `1` | URL/ID de vídeo inválido |
| `2` | Erro de chamada (atribuído pelo argparse, p. ex. opção desconhecida) |
| `3` | Nenhuma transcrição obtida — ambos os caminhos vazios |

`2` fica reservado ao argparse, para que um erro de digitação na chamada
continue distinguível de um vídeo sem legendas.

```bash
# In Skripten
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o out.md || {
  code=$?
  [ "$code" -eq 3 ] && echo "Video hat keine Untertitel" || echo "Fehler: $code"
}
```

### Como biblioteca Python

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)

# Immer pruefen -- fetch_transcript wirft nicht, es meldet:
if not transcript["segments"]:
    raise RuntimeError(transcript["error"])
print(transcript["source"])  # "youtube_transcript_api" oder "yt-dlp"
```

Os dois caminhos podem ser chamados separadamente: `fetch_transcript_primary()` (somente
`youtube-transcript-api`) e `fetch_transcript_ytdlp()` (somente o caminho alternativo).
`fetch_transcript()` os encadeia e garante os campos `segments`,
`language`, `is_generated`, `full_text`, `source` e, em caso de erro, `error`.

## Casos de uso típicos

- Pesquisa: tornar o conteúdo de vídeos citável como texto
- Análise de fontes: examinar argumentação e metáforas em palestras
- Resumos: usar a transcrição como base confiável, em vez de alucinação

## Limitações

- Só funciona se o vídeo tiver legendas (manuais ou automáticas)
- Legendas automáticas podem conter erros de reconhecimento
- Sem download de áudio, sem reconhecimento de fala próprio — mesmo o caminho
  alternativo baixa apenas a faixa de legendas, nunca vídeo ou áudio
- O caminho alternativo exige uma faixa JSON3; se a plataforma entregar apenas
  outros formatos, a execução termina com saída 3 em vez de uma saída parcial

## Changelog

### 1.2.0 (2026-08-24)
- **Semântica de saída:** transcrição vazia termina com saída `3` em vez de
  silenciosamente com `0`. URL inválida agora retorna `1` como constante nomeada. `--meta-only` permanece
  bem-sucedido, pois ali não se espera transcrição.
- **Nova opção `--allow-empty-transcript`:** considera deliberadamente uma transcrição vazia
  como sucesso — para chamadores que tratam as legendas como opcionais.
- **Fallback de legendas via yt-dlp:** entra assim que o caminho primário não retorna
  segmentos (não apenas em caso de exceção). Usa `extract_info(download=False)` e lê somente a URL
  da legenda — sem vídeo, sem áudio, sem contornar restrições de acesso.
- **Seleção de idioma reforçada:** `de-orig`/`de-DE` são encontrados para `--lang de`
  (correspondência por idioma base). Legendas manuais continuam antes das automáticas.
- **Campo `source`** no resultado: `youtube_transcript_api` ou `yt-dlp`.
- Testes de regressão: 29 testes com respostas simuladas (UTF-8, os três
  formatos de saída, códigos de saída, seleção de idioma, parsing de JSON3).

### 1.1.0 (2026-06-20)
- Renomeado de `yt-transcriber` → `video-transcriber` (diretriz de marca do YouTube:
  "yt" é uma abreviação explicitamente proibida; recomendação: RECHTSCHECK_2026-06-20.md)
- Script: `yt_transcriber.py` → `video_transcriber.py`
- Aviso legal e licenças de dependências adicionados (responsabilidade do usuário, ToS, sem endosso)
- YouTube agora apenas como indicação descritiva da fonte, não como parte do nome/marca
- Wrapper de compatibilidade retroativa `yt_transcriber.py` mantido no caminho antigo

### 1.0.0 (2026-06-12)
- SKILL.md adicionado (a ferramenta já existia como script + README)
- Script v1.0.0: transcrição + metadados, 3 formatos de saída, preferências de idioma
