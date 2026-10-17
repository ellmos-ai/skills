---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "根据故事线 JSON，通过本地波形合成（numpy + ffmpeg）创作与视频同步的背景音乐。风格：Chiptune、Ambient、Electronic。确定性、离线，无云服务。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: zh
status: stable
visibility: public
dependencies:
  tools: [ffmpeg]
  services: []
  protocols: []
  python: [numpy]
provenance:
  origin: local-reconstruction
  origin_license: MIT
  notes: >
    Verfahren rekonstruiert aus einem video-synchronisierten Score, komponiert
    für ein 179,5-s-Erklärvideo (5 Musikabschnitte aus 7 Story-Akten
    gemappt). Kanonische Engine: ai-media-editor-Repo, tools/compose_music.py
    (github.com/ellmos-ai/ai-media-editor). Eine eigenständige Kopie liegt
    hier für Offline-Nutzung bei.
translated_from_sha256: 4920ef9c05d0ed853c0ddf7723ca56bac953af15b025feb2f32bdbc8c446fc23
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — 故事线 → 乐谱

完全在本地创作一份背景乐谱，使其遵循视频的戏剧弧线：numpy 波形合成（振荡器、ADSR、分层、延迟混响）加 ffmpeg 进行 MP3 编码。没有采样、没有 MIDI 硬件、没有云 API。

## 何时使用

- 视频/播客需要背景音乐，并且故事节拍要精确对齐时间戳（开场、紧张低谷、驱动段落、高潮、结尾）。
- 需要确定性、可重新渲染的乐谱（相同种子 → 相同音频）。
- 可以接受 Chiptune、Ambient 或 Electronic 风格。

## 何时不要使用（诚实的风格边界）

波形合成可以提供 **Chiptune、Ambient 和 Electronic** 的背景铺底。它无法用内置合成器提供 **流行、摇滚、古典或管弦乐电影配乐**——但编曲与后端无关：参见下方“超越波形合成”，了解如何通过 SoundFont、管弦乐音库或外部生成渲染同一份作品。

## 方法：故事线 → 乐谱

按参考乐谱（179.5 秒，c 小调）的重建方式：

1. **将故事章节映射到音乐段落。** 共享同一情绪状态的章节合并为一个段落（参考：7 个章节 → 5 个段落；第 1–3 章构成一个 62 秒的平静开场）。每个段落以秒为单位给出精确的 `start`/`end`。
2. **为每个段落分配情绪与强度。**
   - *情绪* 决定和弦进行（音阶级数，小调示例）：
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i（V 为和声小调的大三和弦）。
   - *强度*（0–1）驱动速度感（BPM）、层数和音量渐变。各层在阈值处加入：铺底始终存在 → 稀疏钟声（<0.3）→ 琶音（≥0.25）→ 低音（≥0.4）→ 主旋律（≥0.45）→ 鼓（≥0.5）→ 驱动增强（≥0.65）→ 铺底八度加倍（≥0.85）。
3. **在时间轴上放置特殊事件。**
   - `damp`：高斯音量压低 — `1 - depth · exp(-((t-T)²)/(2σ²))`。参考：深度 0.5，σ 1 秒，位于 T=84 秒，对应旁白节拍“Two databases. Same cluster.”（约 1:24）。
   - `climax`：强制全层、峰值音量、八度加倍铺底的时间窗口（参考：154–170 秒 = 2:34–2:50，即 2D→3D 变形处）。
   - `outro`：从其开始时刻起，鼓/低音/主旋律移除（不再演奏），钟声淡至 20%（参考：170–179.5 秒，片尾字幕卡）。
4. **拼接。** 段落边界处进行升余弦平滑（约 2.5 秒），全局淡入/淡出，反馈延迟混响（100 ms，衰减 0.25），双曲正切驱动 + 峰值归一化至背景电平（实测参考母带：均值 ≈ −22 dB，最大值 ≈ −1.6 dB）。
5. **退居旁白之下，作为背景。** 标记为“background”的段落限制其音量渐变；乐谱是铺底，而非主奏。

## 用法

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

输出：`score.wav`（立体声 16 位 44.1 kHz）、`score.mp3`（192k，需要 ffmpeg 在 PATH 中；否则带警告跳过）、`score.notes.json`（编曲/音符日志：每个放置音符的时间、层、MIDI 音高、时值、力度）以及 `score.mid`——真正的 **标准 MIDI 文件**（类型 1：速度轨，每个段落一个速度事件；音符轨，每种风格附带 GM 音色提示；鼓位于 GM 通道 10）。以无依赖方式编写；无需 pretty_midi/mido。

确定性：相同故事线 + 相同 `seed` → 字节级一致的 WAV。

## 故事线 JSON 参考

```json
{
  "title": "my-score",
  "duration": 179.5,
  "bpm": 100,
  "key": "C",
  "mode": "minor",
  "style": "chiptune",
  "seed": 42,
  "fade_in": 3.0,
  "fade_out": 5.0,
  "crossfade": 2.5,
  "peak": 0.85,
  "drive": 2.0,
  "reverb": {"delay_ms": 100, "decay": 0.25},
  "sections": [
    {"start": 0.0, "end": 62.0, "emotion": "calm", "intensity": 0.18, "bpm": 60,
     "comment": "optional note"},
    {"start": 62.0, "end": 88.0, "emotion": "tense", "intensity": 0.4, "bpm": 72}
  ],
  "events": [
    {"type": "damp", "time": 84.0, "depth": 0.5, "width": 1.0},
    {"type": "climax", "start": 154.0, "end": 170.0},
    {"type": "outro", "start": 170.0}
  ]
}
```

- `duration`（必填，秒），`sections`（必填，≥1，已排序、无重叠、位于时长之内）。
- 段落字段：`start`、`end`（必填）；`emotion` ∈ calm | tense | alive | driving | epic | outro；`intensity` 0–1（按情绪取默认值）；`bpm`（默认：全局 `bpm`）；`melody`（可选 MIDI 列表，循环使用；否则在音阶音上生成一个由种子决定的随机游走）。
- `key`：音名（C、C#、Db 等），`mode`：minor | major。
- `style`：chiptune | ambient | electronic（见下文）。
- 事件 `damp`：`time`（秒）、`depth` 0–1、`width` = 以秒为单位的 σ。
- 淡入淡出/交叉淡化/峰值/驱动/混响的默认值如上所示；全部为可选。

完整的已计算示例（参考视频的重建）：[`example-storyline.json`](example-storyline.json)——渲染一份 179.5 秒的乐谱，与原片的母带电平相符（均值 ≈ −22 dB，最大值 ≈ −1.6 dB）。

## 风格预设

| 风格 | 主旋律 | 低音/琶音 | 鼓 | 特点 |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | triangle 低音，快速 square 琶音 | 基于噪声的底鼓/踩镲/军鼓 | 复古主机风，琶音驱动（参考风格） |
| `ambient` | 柔和的 triangle/sine | 慢速琶音，长起音铺底 | 仅在强度 ≥ 0.75 时出现 | 稀疏、以钟声为主，宽广混响感 |
| `electronic` | sawtooth + detune + sub | 有力的低音，saw 琶音 | 完整鼓组 | 接近 EDM 的驱动型铺底 |

## 超越波形合成：更好的声音后端

上述风格上限是**声音后端，而非作品本身**。故事线→乐谱的方法生成与后端无关的编曲；随附的 numpy 合成器只是免费的离线默认渲染器。每次运行还会额外写出一个标准 MIDI 文件（`<out>.mid`）——可用更好的乐器渲染：

- **路径 A——SoundFont（推荐：本地、免费、无云）。** 安装 FluidSynth（fluidsynth.org，Windows：`winget install FluidSynth`），再加上一个免费的 GM SoundFont（GeneralUser GS，作者 S. Christian Collins，或 MuseScore_General.sf2）。然后：`fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → 通过 ffmpeg 转为 MP3。这可解锁流行/摇滚乐队音色、钢琴和简单弦乐。
- **路径 B——管弦乐/电影。** 免费管弦乐音库：VSCO 2 Community Edition、Soni Musicae、Salamander Grand Piano。弦乐/铜管更好，更具史诗感。诚实提示：演奏法和人性化（力度变化、连奏、动态曲线）比采样集本身更重要；真正的电影配乐史诗感还需要编曲成熟度——仅靠一个后端是不够的。
- **路径 C——外部 AI 生成（Suno 等）。** 可行，但会引发数据隐私与权利归属问题——仅在用户明确同意后使用，绝不作为默认。

计划中但**尚未实现**：引擎中的 `humanize` 选项（每个音符的力度/时序抖动），使基于采样的渲染不会听起来机械（已在引擎文档字符串中标记为 TODO）。

## 限制

- 英文和德文的故事线注释均无问题；键名/值固定为英文。
- 非常短的时长（< 约 10 秒）可以工作，但会压缩戏剧结构（淡入淡出和交叉淡化会自动限制在时长的 20% / 最短段落的 50%）。
- 音符日志（`*.notes.json`）是便于分析的数据集；`*.mid` 文件是面向 DAW/SoundFont 渲染器的交换格式（GM 音色编号只是粗略的风格提示——可按喜好重新映射）。
