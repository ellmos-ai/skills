---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: "このエコシステム向けにスキルを作成または改訂する。汎用的なインタビュー・草案・評価ループは公式の skill-creator プラグイン（Anthropic、Apache-2.0）に委譲するが、公式プラグインが知らない ellmos 固有の要件を追加で適用する — ハウスのフロントマター（9 フィールド）、カテゴリ／可視性ルール、grounding-seed による、プロバイダー・ユーザー・ellmos に対して中立でありながら ellmos には敏感な検出、同梱の config.json（学習契約を含む）と connections.json、ベンダー認識（ellmos 独自コンポーネントを含む最新の代替案の提案）、自己更新セクション、そして再利用可能な学習・カバレッジファイル群（user-usecases.json、usecase-gaps.json、known-providers-and-abilities.json、gap-closing-analysis.json — skill-creator の evals.json と A2A/AgentSkill に倣い、並行する標準ではない）。このシステム向けに新しいスキルを作る場合、または既存スキルを ellmos 準拠に改修する場合は、必ずこれを使用する — 「スキルを作成して」「X のスキルを作って」「skill-creator を使って」「新しいスキルを作成」「このスキルを ellmos 準拠にして」「スキルの学習契約／行動規範を作成」「スキルのユースケースカバレッジを確認」などの場合も含む。スキルの単なる検索・ルーティングには skill-finder を、ランドスケープ監査には skill-explorer を使う。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: ja
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 1e6dace03eb8afc639fa08debace08a61441912a22399c11a49f7fe6e7dc3ecb
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="ellmos-skill-creator banner">

# ellmos-skill-creator

## 由来と決定（フォーク対自作）

**決定：フォークではなく自作。** 失われないよう根拠を記す：

- `skill-creator`（Anthropic、マーケットプレイス `claude-plugins-official`）は **Apache-2.0** でライセンスされている（クローン内の LICENSE 本文を読んで確認、2026-08-24）。ライセンス上、フォークは法的に問題なく可能であり、リポジトリ内の他の箇所では、フォークが既に確立されたパターンでもある（`skills/third-party/grilling`）。
- ただしフォークすると、原本の評価・ベンチマークの仕組み全体（`agents/{analyzer,comparator,grader}.md`、`eval-viewer/`、7 本のスクリプト、485 行の SKILL.md）も持ち込むことになる — これは既に存在し直接呼び出せる機能である（`Skill: skill-creator:skill-creator`）。`.PLUGINS/CLAUDE.md` のルール 4「作り直す前に機能を確認する」と、パターン P10「誰も比較していない二つのスイッチ」に従えば、それは拡張ではなく重複になる。
- 本当の欠落は **ellmos 固有** のもので、原本には基本的に存在しない：ハウスのフロントマター（`templates/SKILL.md`）、`docs/CONVENTIONS.md`、プロバイダー・ユーザー・ellmos に対する中立性と ellmos への敏感性、`grounding-seed` との連携、ベンダー認識、自己更新。
- このスキルには **Anthropic の文章を含めない**（終始独自の表現）。そのため改変に伴う Apache-2.0 の帰属表示義務も生じない。原本を **複製するのではなく構成して利用する**。これは法的に最もクリーンで、保守負担も最小の方法でもある。

## 起動条件

- 「X のスキルを作って」「新しいスキルを作成」「skill-creator を使って」
- 「このスキルを ellmos 準拠にして」「スキルをハウス基準に改修」
- **出力先**がこのエコシステム（`.AI/.SKILLS/skills/…`、もしくはその正規の Plan-D クローン）内のスキルである場合は常に。このエコシステムと無関係な一般的依頼（「このエコシステムに関係のない Claude スキルを何か作って」）では使わない。

## 手順

### ステップ 1 — インタビュー・草案・評価を委譲する

`Skill: skill-creator:skill-creator` を呼び出して、意図の明確化、SKILL.md 構造の草案、テストケース、評価ループ、description の最適化（`scripts/improve_description.py`）を任せる。**作り直さないこと** — この部分は汎用的で、原本で既によく解決されている。

### ステップ 2 — ellmos ハウス足場を設定する（必須、原本形式への追加）

原本が生成した SKILL.md に、`.SKILLS/templates/SKILL.md` の 9 つのハウスフィールドを追加する（種類に応じて `AGENT.md`／`WORKFLOW.md`／`PROMPT.md` を使う）。事前に `.SKILLS/docs/CONVENTIONS.md` を読み、カテゴリフォルダ、フラット規則（5 ファイル未満はフラット）、バージョン規約（SemVer：MAJOR/MINOR/PATCH）、多言語セット（Core：DE+EN 必須）を確認する。**`visibility` は常に `private-only` から開始する** — 公開は後で行う、確認済みのユーザー判断（`.AI/VISIBILITY-POLICY.md`）であり、デフォルトではない。これらのフィールドは Anthropic 形式に対して **追加的** な項目（`name`／`description` の横の追加 YAML キー）であり、そのように生成されたすべてのスキルは完全に `anthropic_compatible: true` のままである。

### ステップ 3 — 原則を適用する：プロバイダー中立、ユーザー中立、ellmos 中立だが ellmos には敏感

全文とコードパターン：`references/ELLMOS-PRINCIPLES.md`。要約すると、生成されたスキルは **単独で動作できる**（必要なものを全て同梱する）と同時に、ellmos コンポーネントが存在すればそれらも利用する — その判断は実行時にスキル自身が行い、決してハードコードしない。これは `grounding-seed` が既に提供しているパターンそのもの（README：「野の花ではなく、手入れされた景観」／「単独でも機能し、一緒ならより生産的」）であり、**第二の検出機構は発明しない**。このスキルは、生成したスキルを `grounding_seed.detect_ecosystem()` へ一貫して誘導する。

### ステップ 4 — config.json と connections.json を同梱する

`grounding-seed` は既に Python パッケージとしてインポート可能である（2026-08-24 に検証：`import grounding_seed` はローカルにクローンされた `grounding-seed` のソースツリーで正常に解決される、Plan-D クローン）。これは **正規の接続点** であり、新しいファイルを発明しない。外部依存（プログラム、サービス、プロバイダー）を持つ生成スキルごとに：

- **`config.json`** — スキル固有の設定（テンプレート：`templates/skill-config.template.json`）。`grounding_seed.store.LocalStore(root)` は標準でこのファイル名をロール格納に使う。したがって生成されたスキルは、自身の `config.json` を `LocalStore` のバックエンドとして使うこともできるし、ロール以外に純粋な振る舞い設定も必要な場合は、別個に（その場合は二つ目の `LocalStore(root, filename="connections.json")` インスタンスとして）保持することもできる。
- **`connections.json`** — 実際に **解決された** 外部接続点（どのプログラム／サービスが見つかったか、いつから、どの出所か）。テンプレート：`templates/skill-connections.template.json`、スキーマ `ellmos.source-resolver.user-config.v1`（`source-resolver` と同一。grounding-seed の README によれば、後で実際の `source-resolver` へ損失なく移行できるよう意図的にこの形にした — 同 README の `migration.py` を参照）。

詳細、CLI、コード例：`references/ELLMOS-PRINCIPLES.md` の「Docking」セクション。

### ステップ 5 — プロバイダー／ベンダー認識を組み込む

全文：`references/VENDOR-AWARENESS.md`。要約すると、生成されたスキルには「プロバイダーと代替」セクションを持たせ、(a) そのテーマの最先端プロバイダーを挙げる（例：TTS なら ElevenLabs）、(b) 少なくとも一つの代替プロバイダーを挙げる、(c) テーマをカバーする **ellmos 独自コンポーネントも同等の候補として明示的に** 挙げる（例：ElevenLabs の代わりに、またはそれと並べて `ellmos-voice-io`）。そして、ユーザーの要件に合う場合は、導入や乗り換えを暗黙に前提とせず **提案する**。「このシステムに何があるか」の根拠は `grounding_seed.scan.scan_resources([...])`（`shutil.which` を確認）と、ellmos 候補のための `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` である。

### ステップ 6 — 自己更新を設定する

全文：`references/SELF-UPDATE.md`。要約すると、生成されたスキルごとに「自己更新」セクションを持たせ、(a) 最先端を保つため定期的に短い Web 調査を提案する、(b) 関連するスキル・ワークフローを把握し、より適合しうる新しい代替案を挙げる、(c) 小さな学習 JSON を保持する（テンプレート：`templates/skill-connections.template.json`、フィールド `notizen`／`gelernt`）。ellmos のメモリコンポーネント（USMC/Gardener）が存在する場合は、ローカルで肥大化させる代わりにそちらへ外部化できる。ここでも、ハードコードではなく検出する（`grounding_seed.detect_ecosystem()`）。

### ステップ 6b — 学習契約とユースケースカバレッジを設定する（再利用可能パターン）

全文：`references/LEARNING-CONTRACT-AND-COVERAGE.md`。要約すると、このスキル自身だけでなく、**このスキルが生成するすべてのスキル** に、小さく再利用可能な学習・カバレッジのファイル群を持たせる。確立された標準に照らして検証済みで、並行標準ではない：

- `evals/evals.json` — **再利用し、複製しない**：作者が設計したテストケースについては、既に skill-creator の標準である。
- `user-usecases.json` — ユーザーが実際に持ち込んだユースケース。`evals.json` と同形式（テンプレート：`templates/user-usecases.template.json`）。
- `usecase-gaps.json` — 照合：どのユーザーのユースケースが未テスト／未カバーか（テンプレート：`templates/usecase-gaps.template.json`）。
- `known-providers-and-abilities.json` — 役割ごとの既知プロバイダーの候補空間。フィールドは A2A/`AgentSkill`（id/name/description/tags）に倣い、発明しない（テンプレート：`templates/known-providers-and-abilities.template.json`）。
- `gap-closing-analysis.json` — ギャップごとの構造的な解消経路（ellmos モジュール、ellmos バンドル、外部モジュール、新規作成）。`grading.json.eval_feedback` の重複ではない（テンプレート：`templates/gap-closing-analysis.template.json`）。
- `config.json` のフィールド `lernvertrag` — 行動規範（最良の選択肢を選ぶ、**ユーザーが王**、決して独断でインストールしない、更新間隔）。`config.json` の拡張として意図的に入れており、7 つ目のファイルではない。

スキーマ：`.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json` — `skill-v1.schema.json` と同じハウス規約。`grounding-seed` はこのファイル群のために確認したが、意図的に **拡張しなかった**（理由は `LEARNING-CONTRACT-AND-COVERAGE.md`）。`connections.json` のみがその担当である。

### ステップ 7 — 登録、テスト、コミット

- `.SKILLS/CLAUDE.md`／`SKILLS-MAP.md` に従ってカテゴリフォルダを選ぶ。判断に迷う場合は、ファミリーが既に存在するかを `skill-finder` か `controlcenter_find_skill` で確認する。
- コミット前に `testing/`（privacy_gate とメタデータテスト）を実行する。
- レジストリファイル（`registry/components.json`、`SKILLS-MAP.md`、`llms.txt`）は **手で編集しない** — それらは生成される（`build_public_registry.py`、`build_skills_map.py`、`catalog.py`）。正規クローンで他者の未コミットのセッションが進行中であれば、グローバルに再生成しない（他者の変更と自分の変更が一つのファイルに混ざる）。代わりに新しいスキルフォルダだけを単独でコミットし、レジストリの再生成は次のクリーンな実行（`skill-register-care`）に任せる。
- `git commit -- skills/<kategorie>/<name>/` — 自分の新規パスのみ。

## Anthropic 形式との互換性

すべての追加フィールドは `name`／`description` の横に置かれた純粋な YAML 拡張である。このエコシステムを持たない標準の Claude Code は、引き続き `name`／`description` のみを読み、残りは無視する。`config.json`／`connections.json` は（`docs/CONVENTIONS.md` で想定されているとおり）任意のバンドル済みリソースであり、必須の依存ではない — それらがなくてもスキルは変わらず動作する。

## 関連スキル

- `skill-creator:skill-creator` — 汎用のインタビュー・評価ループ（委譲先、ステップ 1）。
- `skill-finder` — 既存の自前スキルのルーター（構築の前に確認：既にあるか？）。
- `skill-explorer` — ランドスケープ監査と、新しいスキル／プラグインの Web 調査（メタレベル：当方のスキルの *在庫*。このスキルは代わりに、生成された *個々の* スキルをプロバイダー認識させる）。
- `skill-family-care`、`skill-register-care` — 構築後の保守。
- `grounding-seed`（モジュール、`.AI/.MODULES/.CONTROL/grounding-seed`）— 実際の接続・自己供給のロジック。ここでは参照のみで、複製はしない。

## 変更履歴

### 0.2.0 (2026-08-24)
- 追補（チケット T-20260824-218233618、スコープ拡張）：生成された各スキルに再利用可能な学習・カバレッジのパターンを追加 — `user-usecases.json`、`usecase-gaps.json`、`known-providers-and-abilities.json`、`gap-closing-analysis.json`（新しいハウススキーマは `.SKILLS/schemas/`）に加え、`config.json` への学習契約フィールド。`evals/evals.json`（skill-creator）は複製ではなく意図的に再利用。`grounding-seed` を確認 — 拡張は不要（理由は `references/LEARNING-CONTRACT-AND-COVERAGE.md`）のため、フォローアップのチケットはなし。プロバイダーカタログのフィールド名は独自語彙を作らず、A2A プロトコル（`AgentSkill`）に倣った。

### 0.1.0 (2026-08-24)
- 初版。フォークではなく自作とする決定を行い、その根拠を記録（チケット T-20260824-218233618）。汎用のスキル作成は `skill-creator:skill-creator` に委譲し、ハウス足場、ellmos 原則、`grounding-seed` との接続（config.json/connections.json）、ベンダー認識、自己更新を追加。
