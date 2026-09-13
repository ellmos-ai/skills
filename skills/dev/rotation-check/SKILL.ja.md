---
name: rotation-check
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-30
description: >
  回転型パイプラインチェックの標準フレームワーク：1 回の実行につき集合（プロジェクト、フォルダ、リポジトリ）の中から
  正確に 1 つの対象を選択（最も長くチェックされていないものを優先）し、チェックを実行、結果をレジストリと履歴ログに記録します。
  多数のプロジェクトに分散して定期チェックを行う場合（「すべての X を Y について定期チェックする」）、重複チェックを回避したい場合、
  レジストリ／CHECKS-LOG 構造を作成・使用する場合、またはパイプライン全体に定期品質ラウンド（ソース、スタイル、健全性、監査）を
  公平に分配したい場合にこのスキルを使用します。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [automation, check, rotation, registry, pipeline, log, audit, wartung]
language: ja
status: active

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
---

<img src="banner.png" width="100%" alt="rotation-check banner">
# 回転チェック — 1 実行 1 対象、公平なカバー率、記憶機構

## 目的

多数のプロジェクトを含むパイプラインを定期的に検証（ソース、スタイル、健全性、セキュリティ、翻訳など）したい場合、分配の問題に直面します：1 回の実行ですべてのプロジェクトをチェックするのはコストが高すぎ、記憶機構がなければ毎回ランダムに同じプロジェクトをチェックしてしまいます。回転パターンは両方を解決します：**1 回の実行につき正確に 1 つの対象、選択基準は「最も長くチェックされていないもの」、レジストリを記憶機構として使用。** これにより、頻度の低い実行サイクル（日次/週次）であっても、数週間かけてパイプライン全体を証明可能かつ重複なしでカバーできます。

複数のプロジェクトパイプラインにわたるプロダクション自動化群のバックボーンとして実証されています。

## 構成要素

### 1. パイプラインごとに 2 つのファイル（初回作成）

| ファイル | 内容 | 性質 |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | チェックごとに 1 行のコンパクトな記録：対象、日付、チェック種別、結果、次のステップ | 状態概要 —— 対象選択の「前」に必ず読み込む |
| `CHECKS-LOG.txt` | 実行ごとの詳細/証拠を含む短い履歴エントリ | 誌面 —— 追記のみ (append-only) |

両ファイルはパイプラインのルート（個別プロジェクト内ではなく）に配置し、1 回の実行で一括読み込みできるようにします。レジストリの行フォーマット：

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. 選択ルール

1. レジストリとログの読み込み（選択の**前**に必須 —— そうしないと重複チェックが発生）。
2. 候補：**この**チェック種別について一度もチェックされていない、または最も長くチェックされていない対象。
3. 回避/スキップ：対象が最近**密接に関連する**チェックによって変更された場合（例：ソースチェックの直後に引用チェックを行っても効果が薄い）、または現在ロック/編集中の場合（ロックを尊重）。
   **兄弟クールダウン（Sibling Cooldown）：** 同じ対象集合に対して複数の関連チェックが動作している場合（例：同一パイプラインの開発、バグ調査、レビュー）、兄弟チェックによって変更された対象を一定期間（経験値：約 24 時間）再選択しないクールダウン期間を設定します —— 衝突や矛盾する並行変更を防ぎます。
4. 例外的な優先選択は正当な理由がある場合のみ（例：前回のチェック以降の重大な改修） —— 理由をログに明記します。

### 3. チェックの実行 — Read-only 出口付き

選択された**1 つ**の対象に対して実際のチェック（自由定義：ソースチェック、スタイルチェック、セキュリティ監査など）を適用します。2 つの有効な結果：

- **指摘事項あり（Finding）：** スコープに収まるものは修正し、大きな作業はプロジェクトローカルの TODO/タスクファイルに次回作業として記録します（チェック自体がすべてを解決する必要はありません）。
- **作業なし（Nothing to do）：** 簡潔に記録して終了します。何もない空振り実行は結果であり、失敗ではありません —— 「何か見つけるため」にスコープを無理に拡大しないでください。

### 4. 記録とドキュメント化

- レジストリ行を追加（コンパクト）、ログエントリを記述（詳細/証拠）。
- **ログの整理：** レジストリ/ログが肥大化した場合（経験値：数百万行）、古い状態を `_archiv/` に移動し、新しいファイルを作成、ヘッダーで以前のファイルを参照（パス + 日付）します。
- **パスのずれ（Path Drift）：** 予想されるパスが存在しない場合（対象の移動/名前変更）、新規作成**せず** —— パイプラインの正当な状態ファイル/レジストリを修正し、無効なパスを失敗ログに記録します。

### 5. 実行サイクル

検証対象の変更頻度に実行周期を合わせます：安定したコードベースに対する回転チェックは週次実行が適しています（1 実行 1 対象 ≈ ~12 対象の場合、四半期でパイプライン全体をカバー）；変化の激しいチェック（例：アクティブな開発作業）は日次で実行します。実践的経験：当初の時次チェックはほぼすべて日次/週次に削減されました —— カバー率は維持され、コストは削減されました。

## プロンプトテンプレート（スケジューラ／自動化用）

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und was bei Befund zu tun ist; Folgearbeiten in
die projektlokale TODO-Datei>.

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registry-Zeile in <REGISTRY> (Ziel, Datum, Checktyp, Ergebnis, nächster
Schritt) + Verlaufseintrag in <LOG>. Bei Überlänge: alten Stand nach _archiv/ und
frische Datei mit Verweis.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```

## レッドフラグ（注意すべき考え）

| 考え | 現実 |
| --- | --- |
| 「面白そうなプロジェクトを適当に選ぼう」 | レジストリのみに基づいて選択してください —— そうしないとお気に入り偏差や死角が発生します。 |
| 「レジストリはチェック後に読もう」 | 事前に読んでください。レジストリはプロトコルだけでなく、選択基準でもあります。 |
| 「1 回の実行で複数の対象を処理した方が効率的」 | 1 実行 1 対象により、実行を短時間、べき等、かつ中断可能に保ちます。量は回転によって達成されます。 |
| 「指摘なしの実行は無駄だった」 | 記録された空振り実行は記憶を更新します —— それがシステムの価値の半分を占めます。 |

## 関連スキル

- `workflow-extract` — セッション／外部自動化から自動化を構築；この骨架を標準コンポーネントとして利用。
- `pipeline-optimizer` — パイプラインの構造的再構築用（Rotation-Check が保守を行い、Optimizer が刷新を行う）。

## 変更履歴

### 1.1.0 (2026-07-03)
- 選択ルールに兄弟クールダウンを追加（同一対象集合に対する関連チェック間の衝突防止；自動化資産の全量分類からの知見）。

### 1.0.0 (2026-07-03)
- 初版。Codex 自動化資産から抽象化（77 の自動化のうち約 40 で回転パターンを適用：CHECKED-REGISTRY/CHECKS-LOG を持つ研究/ソフトウェア/Roblox チェック）。
