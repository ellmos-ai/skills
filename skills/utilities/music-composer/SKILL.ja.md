---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "ストーリーライン JSON から、ローカルの波形合成（numpy + ffmpeg）により、動画に同期した背景音楽を作曲します。スタイル：Chiptune、Ambient、Electronic。決定的、オフライン、クラウドサービス不要。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: ja
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
translated_at: "2026-10-15T20:31:29.342138+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — ストーリーライン → スコア

動画のドラマ構成に沿った背景スコアを、完全にローカルで作曲します：
numpy による波形合成（オシレーター、ADSR、レイヤリング、ディレイリバーブ）＋ MP3 エンコードのための ffmpeg。
サンプルは使わず、MIDI ハードウェアも、クラウド API も使用しません。

## 使いどころ

- 動画／ポッドキャストに、ストーリーのビートをタイムスタンプに正確に合わせる背景音楽が必要な場合（オープニング、緊張の谷間、ドライブ区間、クライマックス、アウトロ）。
- 決定的で、何度でも再レンダリングできるスコアが必要な場合（同じシード → 同じ音声）。
- Chiptune、Ambient、Electronic のスタイルで問題ない場合。

## 使うべきでない場合（正直なジャンルの限界）

波形合成では、**Chiptune、Ambient、Electronic** の背景ベッドを生成できます。
内蔵シンセでは、**ポップ、ロック、クラシック、オーケストラの映画音楽**は生成できません。
ただし、アレンジはバックエンドに依存しません。同じ作曲を SoundFont、オーケストラ音源ライブラリ、または外部生成でレンダリングするには、下記の「波形合成を超えて」を参照してください。

## 手法：ストーリーライン → スコア

参照スコア（179.5 秒、ハ短調）と同じように再構成するには：

1. **ストーリーの幕を音楽のセクションに対応付ける。** 感情の状態を共有する幕は、1 つのセクションに統合します（参照：7 幕 → 5 セクション。幕 1〜3 は 1 つの 62 秒の静かなオープニングになった）。各セクションには、秒単位で正確な `start`/`end` を割り当てます。
2. **セクションごとに感情と強度を割り当てる。**
   - *感情* がコード進行を選ぶ（音階度数、短調の例）：`calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III · `driving` i–VII–VI–V · `epic` iv–V–VI–i（V はハーモニック・マイナーに基づく長三和音）。
   - *強度*（0〜1）は、テンポの感じ（BPM）、レイヤー数、音量ランプを左右します。レイヤーは次のしきい値で追加されます：パッドは常時 → まばらなベル（<0.3） → アルペジオ（≥0.25） → ベース（≥0.4） → リード（≥0.45） → ドラム（≥0.5） → ドライブ用の追加要素（≥0.65） → パッドのオクターブ重ね（≥0.85）。
3. **特別なイベントをタイムライン上に配置する。**
   - `damp`：ガウス分布による音量ダッキング — `1 - depth · exp(-((t-T)²)/(2σ²))`。参照：depth 0.5、σ 1 秒、T=84 秒の位置、話し言葉のビート「二つのデータベース。同じクラスター。」（約 1:24）。
   - `climax`：フルレイヤリング、ピーク音量、オクターブ重ねのパッドを強制する時間窓（参照：154〜170 秒 = 2:34〜2:50、2D→3D モーフィング時）。
   - `outro`：開始時点からドラム／ベース／リードが消え、ベルは 20 % までフェードダウンする（参照：170〜179.5 秒、エンドクレジットカード）。
4. **結合する。** セクション境界でのレイズドコサイン平滑化（約 2.5 秒）、全体のフェードイン／アウト、フィードバック・ディレイ・リバーブ（100 ms、減衰 0.25）、tanh ドライブ＋ピーク正規化で背景レベルに合わせる（計測された参照マスター：平均 ≈ −22 dB、最大 ≈ −1.6 dB）。
5. **ナレーションの後ろに留まる。** 「background」とマークされたセクションは、その音量ランプに上限を設けます。スコアは背景のベッドであり、リードではありません。

## 使い方

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```


出力：`score.wav`（ステレオ 16 ビット 44.1 kHz）、`score.mp3`（192k、ffmpeg が PATH に必要。なければ警告を出してスキップ）、`score.notes.json`（アレンジ／ノートログ：配置されたすべてのノートの時刻、レイヤー、MIDI ピッチ、長さ、ベロシティ）、および `score.mid` — 本物の**標準 MIDI ファイル**（タイプ 1：セクションごとに 1 つのテンポイベントを持つテンポトラック、スタイルごとの GM プログラムヒントを持つノートトラック、ドラムは GM チャンネル 10）。外部依存なしで書き出し。pretty_midi／mido は不要。

決定性：同じストーリーライン＋同じ `seed` → バイト単位で同一の WAV。

## Storyline-JSON リファレンス

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

- `duration`（必須、秒）、`sections`（必須、1 以上、ソート済み、重複なし、全体の長さの範囲内）。
- セクションのフィールド：`start`、`end`（必須）；`emotion` ∈ calm | tense | alive | driving | epic | outro；`intensity` 0〜1（感情ごとの既定値）；`bpm`（既定値：グローバルの `bpm`）；`melody`（任意の MIDI リスト、循環。指定がない場合は、シード付きのランダムウォークを音階音で生成）。
- `key`：音名（C、C#、Db、…）、`mode`：minor | major。
- `style`：chiptune | ambient | electronic（下記参照）。
- イベント `damp`：`time`（秒）、`depth` 0〜1、`width` = 秒単位の σ。
- フェード／クロスフェード／ピーク／ドライブ／リバーブの既定値は上記のとおり。すべて任意。

完全に計算済みの例（参照動画の再現）：[`example-storyline.json`](example-storyline.json) — 179.5 秒のスコアをレンダリングします。これは原本のマスターレベルに相当します（平均 ≈ −22 dB、最大 ≈ −1.6 dB）。

## スタイルプリセット

| スタイル | リード | ベース／アルペジオ | ドラム | 特徴 |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | トライアングル・ベース、速い square アルペジオ | ノイズベースのキック／ハイハット／スネア | レトロゲーム機風、アルペジオ主体（参照スタイル） |
| `ambient` | 柔らかい triangle/sine | ゆっくりしたアルペジオ、ロングアタックのパッド | 強度 ≥ 0.75 から初めて | 控えめ、ベル中心、広がりのあるリバーブ感 |
| `electronic` | sawtooth + detune + sub | パワフルなベース、saw アルペジオ | フルキット | 推進力のある EDM 寄りのベッド |

## 波形合成を超えて：より良いサウンドバックエンド

前述のジャンルの上限は、**作曲ではなくサウンドバックエンドによるもの**です。
ストーリーライン→スコアの手法は、バックエンドに依存しないアレンジを生成します。付属の numpy シンセは、無料でオフラインに使える標準レンダラーにすぎません。
各実行では、標準 MIDI ファイル（`<out>.mid`）も追加で書き出されます。これを、より良い楽器でレンダリングしてください：

- **パス A — SoundFont（推奨：ローカル、無料、クラウド不要）。**
  FluidSynth をインストール（fluidsynth.org、Windows の場合：`winget install FluidSynth`）し、無料の GM SoundFont（S. Christian Collins 作の GeneralUser GS、または MuseScore_General.sf2）も用意します。その後：
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → ffmpeg で MP3 へ。
  これにより、ポップ／ロックのバンドサウンド、ピアノ、シンプルなストリングスが使えるようになります。
- **パス B — オーケストラ／映画音楽。** 無料のオーケストラ音源ライブラリ：VSCO 2 Community Edition、Soni Musicae、Salamander Grand Piano。より良いストリングス／金管、よりドラマチック。率直な注意点：アーティキュレーションと人間味づけ（ベロシティの変化、レガート、ダイナミクスカーブ）は、サンプルセットそのものより重要です。また、本格的な映画音楽のような壮大さには、さらにアレンジの成熟が必要で、バックエンドだけでは不十分です。
- **パス C — 外部 AI 生成（Suno ほか）。** 可能ではあるものの、プライバシーや権利に関する問題が生じます。必ずユーザーの明示的な同意を得た場合にのみ使用し、決して標準としては用いないでください。

**計画済みですが、まだ実装されていません**：エンジンに `humanize` オプションを追加する予定です（ノートごとのベロシティ／タイミングのゆらぎ）。これにより、サンプルベースのレンダリングが機械的に聞こえるのを防ぎます（エンジンの docstring に TODO として記載）。

## 制限事項

- 英語とドイツ語のストーリーラインのコメントは問題ありません。キーと値は英語で固定です。
- 非常に短い長さ（約 10 秒未満）でも動作しますが、ドラマ構成が圧縮されます（フェードとクロスフェードは、自動的に全長の 20 % ／最も短いセクションの 50 % に制限されます）。
- ノートログ（`*.notes.json`）は分析しやすいデータセットです。`*.mid` ファイルは DAW／SoundFont レンダラー向けの交換フォーマットです（GM プログラム番号は大まかなスタイルの目安です。好みに応じて再割り当ててください）。
