---
name: video-transcriber
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-06-20
description: 从在线视频源获取视频逐字稿（字幕）和元数据，并以 Markdown、JSON 或纯文本形式输出。目前支持：YouTube。优先使用手动创建的字幕，备用自动生成的字幕。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="video-transcriber banner">

> **中文** — `video-transcriber` 官方中文版本。


# Video Transcriber (中文)

从在线视频源获取逐字稿（字幕）和元数据（标题、频道、日期、观看次数、描述）。优先使用手动创建的字幕，备用自动生成的字幕。输出格式为 Markdown、JSON 或纯文本。

目前支持的来源：**YouTube**（youtube.com, youtu.be, youtube-nocookie.com）。

对于视频，请使用此工具，而不是手动总结内容 —— 逐字稿是可靠的来源。

> **声明：** 本工具与 YouTube 或 Google 无关，未经其认可或赞助。使用由用户自行承担责任。用户全权负责遵守相应平台的服务条款和适用的版权法。禁止规避 DRM、付费墙或访问限制。禁止大规模抓取。未经版权所有人同意，禁止重新分发受版权保护的逐字稿。

## 依赖与许可证

```bash
pip install youtube-transcript-api   # 逐字稿（必需） — MIT 许可证
pip install yt-dlp                   # 元数据（可选，回退：noembed） — Unlicense（公有领域）
```

## 使用方法

> **Windows 注意：** 请务必设置 `PYTHONIOENCODING=utf-8`，否则输出中的变音符号和特殊字符可能会损坏（cp1252 编码）。

```bash
# 默认：带时间戳的 Markdown
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 选择输出格式
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# 保存到文件
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# 偏好语言（默认：de en）
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### 选项

| 选项 | 效果 |
|------|------|
| `--format markdown\|json\|plain` | 输出格式（默认：markdown） |
| `--output, -o <file>` | 写入文件而不是 stdout |
| `--lang <codes...>` | 偏好的字幕语言（默认：de en） |
| `--meta-only` | 仅元数据，无逐字稿 |
| `--transcript-only` | 仅逐字稿，无元数据 |
| `--no-timestamps` | 不带时间戳的逐字稿 |
| `--no-meta` | 更快：跳过 yt-dlp 元数据 |

### 作为 Python 库

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)
```

## 典型应用场景

- 研究：使视频内容可以作为文本进行引用
- 来源分析：在演讲中研究论证/隐喻
- 摘要：逐字稿作为可靠的基础，而不是幻觉

## 限制

- 仅在视频具有字幕（手动或自动）时有效
- 自动字幕可能包含识别错误
- 无音频下载，无内置语音识别

## 变更日志

### 1.1.0 (2026-06-20)
- 从 `yt-transcriber` 重命名为 `video-transcriber`（YouTube 品牌政策："yt" 是明确禁止的缩写；参阅 RECHTSCHECK_2026-06-20.md）
- 脚本：`yt_transcriber.py` → `video_transcriber.py`
- 添加了免责声明和依赖许可证（用户责任、服务条款、无背书）
- YouTube 仅作为来源进行描述性提及，不作为名称/品牌组件
- 在旧路径中保留了向下兼容的包装器 `yt_transcriber.py`

### 1.0.0 (2026-06-12)
- 添加了 SKILL.md（该工具已作为脚本 + README 存在）
- 脚本 v1.0.0：逐字稿 + 元数据，3 种输出格式，语言偏好
