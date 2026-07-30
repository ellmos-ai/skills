---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: 将音频/视频文件转录为文本。使用 Whisper (openai-whisper) 或 Vosk (离线) 作为可选后端——两者均通过存在性检查检测。在没有后端的情况下：使用占位符模式和虚拟输出 (dry-run)。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [transkription, audio, speech-to-text, whisper, vosk, offline]
language: zh
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': [{'name': 'openai-whisper', 'optional': True, 'install': 'pip install openai-whisper', 'purpose': 'STT backend option 1 (cloud/local model)'}, {'name': 'vosk', 'optional': True, 'install': 'pip install vosk', 'purpose': 'STT backend option 2 (fully offline)'}]}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.\n'}
---

<img src="banner.png" width="100%" alt="transkription banner">

> **中文** — `transkription` 官方中文版本。


## 概述与目的

将音频/视频文件转换为文本——本地运行，无需强制云端访问。技能会自动检测是否安装了 Whisper 或 Vosk，并选择最佳可用后端。如果没有后端，它将在试运行（dry-run）模式下运行并返回占位符文本，因此工作流始终可用。

转录结果保存在本地 `transkription/store.db` 中，并可进行查询。

---

## 触发词

| 短语 | 操作 |
|---|---|
| "Transcribe this audio" | 转录音频文件 |
| "Transcribe [file]" | 转录指定文件 |
| "Show my transcripts" | 列出最新的转录记录 |
| "Search transcript [term]" | 在转录记录中进行全文搜索 |
| "Export transcript [ID]" | 将转录记录导出为 TXT |

---

## 工作流与步骤

1. **后端检查**：检查是否可以导入 `whisper` 或 `vosk`。
2. **文件检查**：输入文件必须存在（音频：wav, mp3, m4a, ogg, flac；视频：mp4, mkv, webm — 通过 ffmpeg 提取）。
3. **转录**：调用后端并获取原始文本。
4. **保存**：将结果及元数据（文件、时长、语言、后端、时间戳）存入 `store.db`。
5. **输出**：返回文本；可选导出为 `.txt`。

---

## CLI 入口点

```bash
# Transcribe file (Deutsch)
python transkription_core.py transcribe audio.wav

# With explicit language (Deutsch)
python transkription_core.py transcribe audio.mp3 --lang de

# Dry-run (no backend required) (Deutsch)
python transkription_core.py transcribe audio.wav --dry-run

# List transcripts (Deutsch)
python transkription_core.py list [--limit 20]

# Full-text search (Deutsch)
python transkription_core.py search "term"

# Export (Deutsch)
python transkription_core.py export <id> [--out file.txt]

# Backend check (Deutsch)
python transkription_core.py check

# Alternative store path (e.g. for tests) (Deutsch)
python transkription_core.py --store /tmp/test.db transcribe audio.wav --dry-run
```

---

## 存储

| 属性 | 值 |
|---|---|
| 类型 | SQLite |
| 路径（默认） | `skills/assist/transkription/store.db` |
| 覆盖 | `--store <path>` 或环境变量 `TRANSKRIPTION_STORE` |
| 表 | `transcripts` |

### 数据库表结构 `transcripts`

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,  -- UUID (short: 8 hex)
    file_path   TEXT NOT NULL,     -- original path of audio file
    file_name   TEXT NOT NULL,     -- filename (without path, for display)
    text        TEXT NOT NULL,     -- transcribed text
    language    TEXT,              -- language (e.g. "de", "en")
    backend     TEXT,              -- "whisper" | "vosk" | "dry-run"
    duration_s  REAL,              -- duration in seconds (if known)
    created_at  TEXT NOT NULL,     -- ISO-8601 timestamp
    tags        TEXT               -- comma-separated tags (optional)
);
```

---

## 行为与原则

- 在未安装后端的情况下，技能以 dry-run 模式工作（使用演示文本）。
- 优先选择 Whisper 而非 Vosk（德语质量更好）。
- Whisper 和 Vosk 之间的选择可以通过 `assist/prefs.json` 进行设置（`transkription_backend: "whisper"|"vosk"|"auto"`）。
- 用于视频提取的 ffmpeg 需要单独安装，未包含在本技能中。

---

## 隐私与安全

- **所有转录数据均保存在本地**——在未开启 Whisper 在线模式的情况下不会传输至云端。
- Whisper 可以在本地使用（tiny/base/medium 模型）或通过 OpenAI API 使用。默认使用本地模型。
- `store.db` 可能包含敏感的对话内容——**请勿提交到 Git**。
- 建议：将 `store.db` 添加至 `.gitignore`。

---

## 相关资源

- BACH `hub/_services/voice/voice_stt.py` — 后端模式（灵感来源，仅读）
- Skill `utilities/yt-transcriber` — YouTube 转录（独立技能，非重复：特定于 YT）
- `tools/module-installer/module_installer.py` — 注册表包含 whisper + vosk

---

## 变更日志

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初始创建 — 独立的 SQLite 存储，Whisper/Vosk 存在性检查 |