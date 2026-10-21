---
name: choose-your-orchestrator
version: 1.1.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-10-03
description: "複雑なマルチエージェント作業の前に、ユーザーとともに適切で限定されたオーケストレーションを選択し、コンパクトなセッション契約を作成します。/choose-your-orchestrator が呼び出された場合、Orchestrator・スウォーム・モデルルーティング・ユーザー嗜好モデルの組み合わせが不明確な場合、またはモデルスロット、並列性、spawn深度、書き込み境界、受け入れ、エスカレーションを明示的に定める必要があるエージェントプログラムの前に、このスキルを使用してください。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestrierung, multi-agent, delegation, routing, budget, matruschka, session-vertrag]
aliases: [choose-your-orchestrator]
language: ja
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar, budgetierung]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 0b3feaa40d5c9d5310977fbc0e9c92572c1504e201baad19e7b73c7b64e4e846
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.485190+00:00"
---
<img src="banner.png" width="100%" alt="choose-your-orchestrator banner">

# Choose Your Orchestrator

## 目的

複雑なマルチエージェント作業の前に前提条件を明確にし、既存スキルの最小限の有効な組み合わせを推奨し、拘束力のあるセッション・オーケストレーション契約を出力します。選択したスキルは現在のランタイムのスキル機構で読み込み、そのライブの指示に従ってください。その手順をこのスキルにコピーしないでください。

委譲によって権限が拡大されることは決してありません。公開、送信、削除、支払い、本番環境への変更などの外部的または不可逆的な操作は、現在の依頼で明示的に承認されていない限り、ユーザーの承認を必要とします。

## 構成要素

| 構成要素 | 契約における役割 | 役割ではないこと |
|---|---|---|
| `orchestrator` | 作業パッケージ、スコープ、証拠、受け入れ | モデル選択やスウォーム・パターンの考案 |
| `swarm-operations` | スウォーム・パターン、コストゲート、任意のMatruschka段階化 | 個別タスクを人工的に並列化すること |
| `model-strategy` | ライブ利用可能性に基づく能力・モデル別ルート | 固定のモデルバージョンや権限の指定 |
| `clutch` | 任意の外部ルーティング提案 | ディスパッチやスコープに対する唯一の権限 |
| `decision-avatar` | 可逆的な不確実性に対する任意の承認済み嗜好シグナル | ユーザー承認の代替や権限の拡大 |
| `budgetierung` | 高価なモデル/レビュアー/アドバイザー向けに、時間枠ごとに交渉された枠。予算口座と事前手続きをエスカレーションの前に扱う | モデルの専門的選択（それは`model-strategy`が行う）や枠の独断的な決定 |

`clutch route "<kurze Aufgabenbeschreibung>" --json`は、`clutch`が実際に利用可能な場合にのみ使用してください。JSON応答は提案として扱い、利用可能なランタイム・スロット、予算、プロジェクト規則、ユーザー境界と照合してください。`clutch`が利用できない、または出力が読めない場合は、`model-strategy`とランタイムのライブ能力を使用してください。現在のモデル名やバージョンを契約にハードコードしないでください。

## 推奨ダイアログ

### 1. タスクの分類

目的、タスク種別、成功基準、除外スコープ、現在の権限、既存のロック、独立した作業パッケージを特定します。まず、下の表から最小限の適切なルート提案を選択してください。

### 2. 契約の提案

次を含むコンパクトな草案を提示します。

1. 構成要素と役割、
2. モデル/予算スロット（数時間にわたる実行や、利用枠が限られた、または高価なモデルの場合は`budgetierung`で交渉し、予算口座として管理する）、
3. 最大並列性とspawn深度、
4. 書き込み境界とロック、
5. 受け入れと証拠、
6. エスカレーションとユーザーへの質問、
7. 権限の境界。

具体的な値を推奨し、最も重要なトレードオフを1文で示してください。結果を実質的に変える決定についてのみ質問してください。未解決の質問は、明確に区別された最大3つのグループにまとめ、推奨オプションを各グループの先頭に置いてください。すべての項目が明示的に確定している場合は、再度質問しないでください。

### 3. 確認または縮小

実質的な予算、書き込み、または権限の問題が未解決の間は、マルチエージェントのディスパッチを開始しないでください。並列性の利点のみが不明な場合は、単独実行に縮小してください。明示的に承認された依頼は、実質的なユーザー決定が欠けていなければ、安全なデフォルトで開始してかまいません。

### 4. 契約の出力

確定した契約をチャットに出力します。`usmc`のコマンドが利用可能な場合は、まずそのヘルプを確認し、さらにそこに文書化されたNote/Writeコマンドを通じて、プライバシーに配慮したセッションノートを書き込んでください。サブコマンドを作り出さず、生のプロンプト、機密情報、非公開の内容を保存しないでください。利用可能なUSMCの書き込み手段がない場合は、チャット内の契約が権威を持ちます。

## ルーティング表

| タスク種別 | 推奨 | デフォルトの分割 |
|---|---|---|
| 監査 / スイープ | `orchestrator` + `swarm-operations`。能力クラスが異なる場合は`model-strategy` | 独立した領域、小さな`parallel-chunks`または`specialist`のグループ、中央でのマージ |
| 構築プログラム | `orchestrator` + `model-strategy`。本当に独立したストランドに限りスウォーム | チーフが計画と受け入れを行い、ワーカーは互いに素な領域で構築 |
| 単独構築 | 単独実行。ルートに`model-strategy`または`clutch`を任意で使用 | スウォームや階層のオーバーヘッドなし |
| チケット運用 | チケットシステムが主導。`orchestrator`が作業契約と証拠を補完 | 既存のルーター/スコア体制を置き換えず、チケットのライフサイクルを尊重する |

## 安全なデフォルト

ユーザー、ランタイム、またはプロジェクト規則がより厳格な値を定めていない限り、次の値を使用してください。

- 同時にアクティブなワーカーは最大2つ。まず1つから始め、2つ目の効果を実証する。
- Matruschkaはオフ、最大spawn深度は`0`。
- 明示的な承認がない限り、ワーカー自身によるサブエージェントは作らない。
- リポジトリまたは明確に区切られた領域ごとに書き込み者は1人。
- 書き込みの前に、互いに素なファイルのClaimとプロジェクト標準のロックを確保する。
- チーフ/オーケストレーターは、成果物、差分、テストを自ら確認する。
- 完了報告は、証拠の受け入れを経てから有効とする。
- 不可逆または外部の操作はユーザーの承認を必要とする。
- 不確実性は個別の中断を多数送るのではなく、まとめて報告する。

Matruschkaは、ユーザーが明示的に確認し、契約が階層ごとにモデル/能力クラス、アクティブなスロット上限、許可される下位タスク、最大深度を明記している場合にのみ有効化してください。存在するエージェントではなく、アクティブなエージェントを数えてください。その場合でも、領域ごとに書き込み者は必ず1人のままです。

## 契約の形式

```text
SESSION-ORCHESTRIERUNGSVERTRAG
Ziel und Typ: <Ergebnis; Audit/Bauprogramm/Einzelbau/Ticket-Betrieb>
Bausteine: <geladene Skills und optionale Router>
Chef: <Planung, Denkarbeit, Integration, Evidenzabnahme>
Worker-Slots: <Rolle/Fähigkeitsklasse je Slot; Budgetgrenze; Budget/Konto: <budgetierung-Konto, Pfad>>
Parallelität: <maximal aktiv>; Spawn-Tiefe: <0..N>; Matruschka: <aus/an>
Schreibgrenzen: <ein Schreiber je Bereich; Claims; Locks; negative Scopes>
Abnahme: <Artefakte, Tests, Diffs, Quellen; wer prüft>
Eskalation: <Stopps; höchstens drei gebündelte Nutzerfragen>
Autorität: <zulässige Aktionen; extern/irreversibel user-gegatet>
Persistenz: <Chat autoritativ; USMC-Notiz ja/nein und privacy-neutral>
```

## 例

```text
Auftrag: Drei unabhängige Komponenten prüfen und einen Fix integrieren.
Empfehlung: orchestrator + swarm-operations; zwei aktive Read-only-Reviewer,
danach genau ein Integrationsschreiber. Matruschka aus, Tiefe 0. Der Chef prüft
Fundstellen, Diff und Gesamttests. Push oder Veröffentlichung nur im ausdrücklich
autorisierten Scope.
Offene Frage: Ist die zweite parallele Review-Spur den zusätzlichen Verbrauch wert?
Empfehlung: ja, weil die Komponenten unabhängig sind.
```

## 停止条件

スコープが重なる、ロックが不明確、ランタイムが推奨スロットを提供しない、予算が確認されていない、または受け入れを独立して証明できない場合は、オーケストレーションを停止または縮小してください。新たな製品、プライバシー、権限の決定を推測するのではなく、ユーザーに質問してください。

## 変更履歴

### 1.1.0 (2026-10-03)
- `budgetierung`を、交渉されたモデル枠/アカウントのための構成要素として追加（構成要素の表、契約ダイアログのモデル/予算スロット、契約形式のワーカースロット行）。

### 1.0.0 (2026-08-20)
- 推奨ダイアログ、ルーティング表、コンパクトなセッション契約を導入。
- 並列性、Matruschka、書き込み境界、証拠、外部操作の安全なデフォルトを定義。
- `clutch`の任意統合と、固定のモデル結合や権限拡大なしの承認済み嗜好モデルを記述。
