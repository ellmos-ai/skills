---
name: work-autonomous
version: 1.5.1
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-09
description: "自律ループの終了条件：可能な限り自律的に作業を続け、自律的に実行可能なタスクが残っていないことが裏付けられるまでループを終了しない。単なる「もうやることがない」という印象では不十分であり、まず新しいタスクを獲得しなければならない四段階の確認チェーン（think/decide、_CONTROL/_DECISIONS、Gardener/USMC、decision-avatar/BYUM）を発動させる。各チェーンステップは二値の結果ではなく found/empty/unavailable を報告する。「exhausted」は、すべてのソースが実際に照会可能だった場合にのみ成立する。少なくとも一つのソースが unavailable の場合、スキルは「exhausted」ではなく「blind」を報告し、未確認の事柄を主張しない。このスキルは /work-autonomous、/waafap、「自律的に作業を続けて、やることがなくなるまで」、/loop 内のゴール条件として、または、ループ／セッションを終了する前に本当に自律的な作業が残っていないかを確認したい場合に使用する。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: ja
status: active
visibility: public
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: a8ee248e73bb81d9af36df2f3e82719bed0f31e89005ab64c35f4e236b15600c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T22:17:49.701000+00:00"
---
<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — 自律的なタスクが残っていないと裏付けられるまでループを終了しない

## 目的

このスキルは二つのことを同時に行う:

1. **可能な限り自律的に作業を続ける** — 通常のセッション作業であり、特別なことは何もない。
2. **自律的に実行可能なタスクがもはや存在しないことが実証されるまで、ループを終了しない。** 「今はやることが見つからない」という疑念は**終了理由ではない**。それは、まず新しいタスクを**獲得**しようとする確認チェーンの**きっかけ**である。このチェーンが完全に結果なしに終わって初めて、終了が裏付けられたとみなされる。

**組み込みの `/goal` は意図的に持たない:** このスキルは単独で利用できる（例: 通常のセッション内で直接 `/work-autonomous` を呼び出す）。また、上位のループ構成の条件としても利用できる。`/loop` は通常どおり設定し、ゴールとしてこのスキルのみを挙げる。ゴールは意味的に次のようになる: *「もう自律的なタスクが残っていなければループを終了せよ。それまでは可能な限り自律的に作業を続けよ。」* このスキル自体は `/goal` 構造を呼び出さない。そのような構造が読み取れる、明確な終了信号を提供するだけである（後述の「終了信号」を参照）。

## 運用モデル — 二つのレベル

### レベル1 — 通常作業（各ティック）

#### TICKET-MASTER 受付ゲート（このレベルの他のすべてに優先）

**チケットシステム（`_TICKETS/`）がコンテキストに含まれている場合にのみ関係する** — チケットシステムのないセッションではこのゲートは単に省略され、このスキルはチケットシステムなしでも単独で利用可能なままである（上記「目的」を参照）。まず、`INBOX/` — まだチケット形式になっていない非公式な項目を含む — が完全に正式化され、トリアージ済みかどうかを確認する。そうでない場合、それ自体が発見された自律的作業としてカウントされる（正式化／トリアージは、ユーザーの判断を要しない事務作業である。下記の区別を参照）。処理し、ティックを終了する。レベル2には進まない。他のレベル1のソースと同様である。

**INBOX が開いている限り、`NO_WORK`、枯渇信号（`exhausted`/`blind`）、Guard-STOP、その他いかなる終了信号も発生してはならない。** 受付が完全にトリアージされて初めて、`ACTIONABLE`、ブロック解除済みの `BLOCKED`、期限到来の `WAITING`（下記）が確認され、その後必要に応じてレベル2が検討されうる。

*実例:* ループは `ACTIONABLE` の処理後に枯渇確認を開始したが、その間も新しい `INBOX` チケットが次々と到着しており、そのうち二件は優先度 P1 だった。このゲートがなければ、受付が開いたままなのに、ループは `exhausted`/`blind` を報告していたはずである。まさにこれをゲートが防ぐ。

その後は通常どおり、さらに自律的に実行可能な作業を探し（下記の区別を参照）、それを処理する。オープンな `ACTIONABLE` チケット、ブロック解除された `BLOCKED` チケット、期限の来た `WAITING` チケット、ユーザー依存のないプロジェクト内のオープンな `TODO.md`/`AUFGABEN.txt` 項目、ローカルポリシーに従った期限の来た定期／衛生チェック、前回のセッションから開始されたが完了していない作業（USMC `working`）、**アクティブなプロジェクトの期限の来た `tidy-up` 実行**（追補 1.3.0、2026-08-19 — スキル `tidy-up` を参照: セッションが作業していたプロジェクトフォルダ向けの Tasksolver+Writer+Maintainer 実行。期限は `tidy-up` 自身が独自の軽量な USMC ログで確認する。該当セクション「work-autonomous との関係」を参照）。

→ **発見して処理済み:** 結果を簡潔に報告し、ティックを終了する。ループは通常どおり続行する。レベル2には進まない。目に見える作業がある限り、四つの高コストな確認ステップはいずれも必要ない。

### レベル2 — 枯渇確認（「やることがない」という疑いがある場合のみ）

レベル1が自律的な作業を**何も**見つけなくなって初めて、疑いが生じる。この疑いだけでは不十分である。ここで**必ず**次のチェーンが実行され、新しいタスクを**獲得**する。

#### 自己認識（チェーンの前に、後ではなく）

何かを照会する前に、スキルは判定のためにどのソースが必要かを宣言する。四つの必要項目（`grounding_seed.self_knowledge.Need`、`grounding-seed` がインストールされている場合。そうでなければ、同じリストは単なる宣言として、ライブラリ接続なしに扱われる）:

| 役割 | チェーンステップ | 内容 |
|---|---|---|
| `decisions.ledger` | 2 | 中央の決定レジスタ |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide`（ステップ 1）は意図的に宣言されたソース「ではない」。** これはモデル自身の分析ステップであり、到達可能か否かがありうる外部システムではない。この区別の意味では常に「利用可能」である。ステップ 2〜4 のみが `unavailable` になりうる。

純粋な所在確認（found/unavailable、まだ内容確認なし）のための任意でテスト可能なツールとして、このスキルフォルダ内に `scripts/exhaustion_check.py` がある。これは `grounding_seed.resolve()` + `status_from_resolution()` を `decisions.ledger`/`user.model` に使用する（そこには実在の `source-resolver` プロバイダーが存在する）。`memory.organic`/`memory.curated` については、**常に** CLI 到達性（PATH 上の `gardener`/`usmc`）で直接確認する。これら二つの役割には 2026-08-15 まで登録済みの `source-resolver` プロバイダーがなかった。リゾルバー経由で照会すると、Gardener/USMC が実際にインストールされているかどうかに関係なく、`unavailable` を報告するだけだっただろう。`grounding-seed` がインストールされているか否かに関係なく、同じように動作する。

**更新 2026-08-25（K3=C、`T-20260825-342866657`）:** この欠落は解消された。`source-resolver` が `memory.organic`（Gardener）と `memory.curated`（USMC）の両方を、このスクリプトがこれまで独自にハードコードしていた同じ CLI 存在チェック（`shutil.which("gardener")`/`shutil.which("usmc")`）を伴うステージ 1 の役割として登録するようになった。そのため `exhaustion_check.py` は直ちには書き換えられていない（機能の喪失はなく、既存のチェックは正しいまま）。次回のスキル保守の実行時に、ステップ 3 を `source_resolver.resolve("memory.organic"/"memory.curated")` に切り替えてよい。ステップ 2（`decisions.ledger`）と同様であり、CLI チェックを二重に保守しないためである。

#### 四つのチェーンステップ — それぞれ found | empty | unavailable を報告する

各ステップは二段階で実行される。まず**所在確認**（到達可能な場所をそもそも把握しているか？）、次に、所在が確認できた場合のみ**内容確認**（モデルが自身のツールで、そこに新しいものがあるかを実際に読んで確認する）。所在を確認できなかったソースは決して内容確認されない。それは `unavailable` としてカウントされ、`empty` としてはカウントされない。

1. **`/think` + `/decide`** を次の問いに適用する: 「本当に自律的に実行可能な作業はもう残っていないのか、それとも何かを見落としているのか？」 構造化された分析であり、直感ではない。found/empty/unavailable のステータスはない（上記参照、ソースではないため）。
2. **`decisions.ledger`** — 所在確認は、インストールされていれば `source_resolver.resolve("decisions.ledger")` / `grounding_seed.resolve(...)` 経由。そうでなければ既知のフォールバックパス（`_control-center/_CONTROL/_DECISIONS/`、`TO-DECIDE-USER*.txt` チェーン、ホスト固有の `TO-DECIDE-USER-<HOST>.txt`、`DECIDED-AND-DONE.md`）。所在確認できた → 内容を読む: 最近、以前ブロックされていた、または承認待ちだった作業をいま解除する決定が下されたか？ ヒットあり → `found`。読んだが新しいものなし → `empty`。所在確認不能（リゾルバーがなく、かつフォールバックパスも存在しない）→ `unavailable`。
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — 二つの別個のソース、一つのチェーンステップ。所在確認: PATH 上の CLI（`gardener`/`usmc`）、上記の自己認識を参照。到達可能 → 内容を読む（`find()`/`recall()`、もしくは `usmc facts|lessons|working|context`）: 未解決のワーキングメモリ項目、未完了のフォローアップを持つ教訓、見落とされているが実行可能な作業を示唆する事実。まさにここに、以前のセッションが未完成の項目（`RESUME:` フィールド、オープンな `note` エントリ）を残す。ヒットあり → `found`。読んだが新しいものなし → `empty`。PATH 上に CLI がない → `unavailable`。
4. **`user.model` (decision-avatar/BYUM)** — 所在確認は `decisions.ledger` と同様（リゾルバーまたはフォールバックパス `_control-center/_CONTROL/_USER-MIND/`）。所在確認できた → 内容を確認: ユーザーがこの場所で特定の行動を自律的に処理してほしいと望んでいた、実証された傾向があるか？ 十分な確信度（🟢/🟡）の場合のみ `found` として数える。🔴 は `empty` として数える。これは獲得されたタスクとしてではなく、下記の「ユーザーのみの残り」ステップのための未解決項目としてである。所在確認できない → `unavailable`。

**「Exhausted」は、ALLE VIER ソース（ステップ 2〜4、三つのステップ、四つの役割）が実際に照会できた場合にのみ報告してよい。つまり `found` または `empty` で、一つも `unavailable` がない場合に限る。** これは `grounding_seed.self_knowledge.GroundingReport.all_answerable()` に対応する。少なくとも一つの役割が `unavailable` の場合、「exhausted」は適用されず、代わりに独自の信号「blind」（下記の終了信号を参照）が適用される。ループは（どのみち照会できないので）それでも終了するが、確認できなかったことを確認したと主張しなくなる。

いずれかのステップで新しい作業が見つかった場合は、レベル1に戻り、作業を処理し、ガード状態（下記）を「exhausted」/「blind」ではなく「found」に設定する。

### 特殊ケース：ユーザー依存の残りのみ

チェーンが**自律的な**タスクをもはや見つけないが、`USER/*` チケットまたは未決定の `_DECISIONS` 項目が未解決のままである場合、それでも**自律性のための停止**である。ただし意味は「やることがない」ではなく「*自律的に*やることがない」である。これらの項目は `ticket-master` の自律ループのルールに従い、**まとめて**提示される（一つの一括提示であり、個別の問い合わせは行わない）。終了信号は、この場合を本当の空っぽの状態から明示的に区別する。

## 区別 — 何が「自律的に実行可能」とみなされるか？

参照: `ticket-master` のカテゴリ（`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`）。

| ケース | 自律的か？ | 根拠 |
|---|---|---|
| `INBOX/`（非公式な項目を含む）、TICKET-MASTER 配下（トリアージ前） | **はい、優先** | 正式化／トリアージは、ユーザーの判断を要しない事務作業である。`ACTIONABLE`/`BLOCKED`/`WAITING` より前に行われ、それまではあらゆる終了信号をブロックする（上記の受付ゲートを参照）。 |
| `ACTIONABLE` チケット | **はい** | ブロッカーなし、ユーザー依存なし。定義上そうである。 |
| `BLOCKED/*`（host-receipt, foreign-state, lock, quota, dependency） | いいえ、ブロッカーが**実証的に**解消されるまで | 定期的な再確認は許可されている（自律ループ）。「存在する」は証明としては不十分であり、根拠が必要。 |
| `WAITING/*`（scheduled, review-due, marker）で期限／マーカーの前 | いいえ | 時間依存。 |
| `WAITING/*`、期限／マーカーの到来後 | **はい** | 条件が満たされた → `ACTIONABLE` へ移行する。 |
| `USER/*`（decision, data, freigabe, hardware, session） | **決して自律的ではない** | 必ずユーザーの判断／データ／承認／ハードウェア／セッションが必要。上記のようにまとめて提示する。 |
| `PARKED/*`（skip, backlog, until-trigger） | いいえ、明示的な指示／トリガーがない限り | 意図的に保留されており、自動の再確認はない。 |
| 承認／決定の記録がない、オープンな `TODO.md`/`AUFGABEN.txt` 項目 | **はい** | プロジェクトレジスタ、通常の作業。 |
| 期限の来た定期／衛生チェック（クールダウン経過、ロックなし） | **はい** | ローカルポリシーに従う通常のメンテナンス作業。 |
| `LOCK.user.*` によりロックされた領域 | **決して** | ユーザーロック。ユーザーのみが解除できる。LOCK-SYSTEM を参照。 |
| ポリシー承認のない不可逆／外部に作用するステップ（Zenodo-Upload、審査済み・保護されたブランチへの Push、ラップトップの閾値を超えるサーバー支出の決定、プレビューなしの完全削除） | **いいえ** | 技術的に実行可能であっても、承認／決定が必要。 |
| GUI／ログインでのみ開始可能なセッション（例: Claude Desktop のタスク、対話的ログイン、物理的なハードウェア操作） | **決して** | 「ユーザーのみが開始できるセッション」であり、どのループも引き継げない。 |

経験則: 自律的とは、ユーザーの判断、承認、データ、ハードウェア、またはセッションなしで完了でき、かつ、文書化されたポリシー承認なしには不可逆／外部に作用する行為を必要としないものである。

## 無限ループ防止ガード（必須）

**問題:** ブレーキがなければ、四段階のチェーンは、前回の結果なしの実行から何も変わっていなくても、毎回の再確認でフルに実行されてしまう。高コストで無意味である。特にスキルが繰り返し呼び出される場合（ループ、スケジュールされたタスク、短時間の手動の再呼び出し）に問題になる。

**状態は USMC に永続化される**（このシステムではプロセス状態はそこに属する。Markdown ファイルには置かない）:

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**フィンガープリントは二つの要素から成る。状況と到達可能性である:**

1. **状況要素**（従来どおり）: オープンな `ACTIONABLE` チケットの数／ID、`_DECISIONS` チェーン（`TO-DECIDE-USER*.txt`、`DECIDED-AND-DONE.md`）の mtime、前回のチェーン実行以降の新しい USMC-`working` エントリの数。
2. **可用性要素（新規、1.2.0 以降必須）:** 自己認識チェック（`exhaustion_check.availability_fingerprint_component()`）で、ちょうどいま `unavailable` と報告された役割のソート済みタプル。例: `("memory.organic",)` または `()`。

**なぜ二つ目の要素が必須なのか。「そうでないとガードが欠落を継承する」:** これがないと、フィンガープリント（要素 1）は、とりわけ `_DECISIONS` チェーンの mtime に依存する。そのチェーンがあるシステムに完全に欠けている場合、フィンガープリントのこの部分は永久に一定になる。一度誤って設定された `exhausted`/`blind` は、その後 `source-resolver` がインストールされたり `_control-center/_CONTROL/_DECISIONS/` が作成されたりしても、決して再確認されない。可用性要素はまさにこれを解決する。どの役割が unavailable かが変わると（ソースが加わるか失われると）、フィンガープリントは自動的に変わる。ガードは次の呼び出しでそれを検出し、チェーンを再実行する。これはグラウンディング・メタファー（T-20260815-371628859）の意味での「移植」である。環境の変化が新しい検索を引き起こし、誰もガードを手動でリセットする必要がない。

**各チェーン実行の前の手順:**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result in ("exhausted", "blind")
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:      # Lage- UND Verfügbarkeits-Baustein
       → Kette NICHT erneut fahren.
       → guard.result == "exhausted":
           Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                    Kein neuer Trigger. STOP (Guard aktiv, exhausted unchanged since …)."
       → guard.result == "blind":
           Melden: "Weiterhin blind (Quellen nicht verfügbar) — unverändert seit {guard.timestamp}.
                    STOP (Guard aktiv, blind unchanged since …)."
sonst:
       → Kette vollständig fahren (Selbstkenntnis-Prüfung + alle vier Kettenschritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|blind|found).
       → alle vier Quellen befragbar UND alle empty → exhausted → STOP (belegt).
       → mindestens eine Quelle unavailable → blind → STOP (nicht belegt, nur unerreichbar).
       → mindestens eine Quelle liefert einen Treffer → found → zurück zu Ebene 1, Arbeit erledigen.
```

全四ソースが照会可能で、いずれもヒットを返さなかった、完全に実行された単一のチェーン実行は、「もう自律的なタスクはない」の証拠として十分である（チケットの仕様: 「すべてのステップが結果なしのままになって初めて」。ここで「結果なし」とは明示的に `empty` を意味し、`unavailable` ではない）。ガードは判定そのものを妨げるのではなく、密な後続呼び出しでの**反復的な、変化のない再判定**のみを防ぐ。しかも `exhausted` と `blind` で別々に、決して取り違えずに。

`GUARD_INTERVAL` は設定可能（デフォルト 15 分）である。非常に動きの少ない環境（新しいチケット／決定がまれ）では長めに、非常に活発な環境では短めに選んでよい。

## 終了信号

各実行は、**一つ**の明確な、grep 可能な行で終わる。これにより、周囲の `/loop` や将来の `/goal` 構造が、そこから続行すべきかどうかを読み取れる:

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE` は、上位のループが次のティックを開始すべき唯一の信号である。すべての `STOP` 変種は確定した終了であり、どのケースが該当するかの理由を含む。

**`exhausted` と `blind` の違いはユーザーにとって本質的であり、見た目だけの問題ではない:**
`exhausted` は「確認すべきものはすべて確認した。作業は完了している」を意味する。`blind` は「そもそも確認するためのインフラが欠けている。これは作業の状態ではなく、欠落である」を意味する。
両方を同じように扱う（どちらの場合もループは終了する）`/loop`/`/goal` 構造は、それらをユーザーに同じ形で「報告」してはならない。さもないと、T-20260815-205101335 が要求した情報そのものが消えてしまう。

## 他のスキルとの関係

- **`think`/`decide`** — チェーンステップ 1 で構造化された分析／判断を提供する。ここではビルディングブロックとして呼び出され、新たに作り直されることはない。
- **`decision-avatar`**（このスキル、ユーザー非依存）— チェーンステップ 4 を提供する。具体的で認可されたプロファイルがあるシステムでは、これは `user-model` + `build-your-users-mind` に対応する。
- **`orchestrator`** — サブエージェントへの委任方法と、その完了報告の確認方法を定める。`work-autonomous` は、そもそも探索をいつやめるかを定める。両者は組み合わせ可能である（オーケストレーターは、レベル 1 で処理された作業の一部として現れうる）。
- **`bugsweep`** — 別の、自己制限的な探索プロトコルの例（四ステップのチェーンではなく、倍増によるエスカレーション）。`work-autonomous` はより汎用的である。コードをバグについて確認するだけでなく、自律的作業のあらゆるソースを確認する。
- **チケットカテゴリ（`ticket-master`）** — 「自律的に実行可能」の語彙（上記の区別の表を参照）と、自律ループのテンプレート（BLOCKED の再確認、USER のまとめ、WAITING の期限引き寄せ、PARKED の停滞）を提供する。
- **`tidy-up`**（1.3.0 以降）— レベル 1 の追加ソースを提供する。現在作業中のプロジェクトフォルダに対する一回限りの Tasksolver+Writer+Maintainer 実行である。自身の期限は自分で確認する（軽量な USMC ログを使用し、ここにあるような四ステップのガードはない）。`work-autonomous` はそれを複数のレベル 1 ソースの一つとしてのみ呼び出し、そのロジックを複製しない。

## 実行例

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Selbstkenntnis + Kette 1–4 läuft.
        → Schritt 2 (decisions.ledger): verortet, DECIDED-AND-DONE.md hat einen neuen Eintrag
          seit 10 Min. → found, daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar. Voll ausgestattetes System (Gardener, USMC, _DECISIONS, BYUM alle da).
        → Ebene 2: alle vier Quellen verortet UND befragt, alle vier empty.
        → Guard: result=exhausted, fingerprint=FP1 (Lage + Verfügbarkeit ()), timestamp=T1.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since T1)

Gegenbeispiel — System OHNE Gardener/USMC (der Kernfall aus T-20260815-205101335):
Tick 1: Nichts sichtbar. Selbstkenntnis-Prüfung: decisions.ledger verortet (leer, empty),
        memory.organic/memory.curated NICHT verortet (CLI fehlt) → unavailable,
        user.model verortet (empty).
        → nicht alle vier Quellen befragbar → KEIN exhausted.
        → Guard: result=blind, fingerprint=FP2 (Verfügbarkeit ("memory.curated","memory.organic")).
        → WORK-AUTONOMOUS: STOP (blind, 2/4 Quellen nicht verfuegbar: memory.organic, memory.curated)
Tick 2 (Nutzer installiert grounding-seed + usmc auf diesem System):
        → Selbstkenntnis-Prüfung: memory.curated jetzt verortet (CLI auf PATH) → Verfügbarkeits-
          Baustein ändert sich zu ("memory.organic",) → fingerprint(jetzt) != FP2.
        → Guard erkennt Änderung, Kette läuft neu (Verpflanzung) — ohne dass jemand den Guard
          manuell zurückgesetzt hätte.
```


## 変更履歴

### 1.5.1 (2026-09-09)
- T-20260909-282509082: `decisions.ledger` と `user.model` の文書化されたフォールバックは、実証された Control-Center の移行（`_CONTROL/_DECISIONS` と `_CONTROL/_USER-MIND` への）に従う。リゾルバーの優先順位と fail-closed の動作は変更されていない。

### 1.5.0 (2026-09-09)
- P-018: 重要な新規作成され、永続的に保存された作業レポート、ハンドオフ、レシートは `session: <session-id> | <agent>@<host> | YYYY-MM-DD` で終わる。ソースの優先順位は次のとおり: 明示的な実行時／CLI の指定、`unbekannt` より前の、権威あるプロバイダー環境／フックより前。値は決して推測せず、サブエージェントは親セッションを使用する。通常のチャット、ソースファイル、ポリシー、`CLAUDE.md`、README、旧ファイルは、一括または遡及的なスタンプ付与の対象外のまま。

### 1.4.0 (2026-09-03)
- チケット T-20260902-729068782 からの最小限の追加: レベル 1 に新しい **TICKET-MASTER 受付ゲート** を追加（`ACTIONABLE`/`BLOCKED`/`WAITING` より優先）。チケットシステムがコンテキストの一部である場合にのみ関係する。`INBOX/`（非公式な項目を含む）が完全にトリアージされるまで、`NO_WORK`、枯渇信号、Guard-STOP は発生してはならない。実例: ループは、`INBOX` がまだオープンな項目（二件の P1 チケットを含む）を保持している間に枯渇確認を開始した。既存の四ステップの枯渇チェーン、ガード、TICKET-MASTER 以外での利用可能性は変更せず保持した。このゲートはレベル 1 にのみ作用し、TICKET-MASTER 配下でのみ作用する。
- 新しい、テスト済みのヘルパー関数 `scripts/exhaustion_check.py::intake_gate_blocks_stop()` と、`tests/test_exhaustion_check.py` での回帰テスト（振る舞いベース: INBOX が開いている間はゲートがブロックし、INBOX が空なら解放する）。

### 1.3.0 (2026-08-19)
- チケット T-20260819-461890468 からの最小限の追加（新スキル `tidy-up`）: レベル 1 に、独立した追加ソースを追加する。「アクティブなプロジェクトの期限の来た `tidy-up` 実行」（Tasksolver+Writer+Maintainer 実行、スキル `tidy-up` を参照）。新しいチェーンステップや、レベル 2／ガード／終了信号の変更はない。`tidy-up` は独自の期限を軽量な USMC ログで自ら確認し、ここでは既存のソース（チケット、TODO/AUFGABEN、定期チェック、USMC `working`）と同様に、もう一つのレベル 1 ソースとして参照される。これにより `tidy-up` の項目は、`/work-autonomous` + `/tidy-up` を組み合わせる `/goal` 構造の意味で、自律的に実行すべきタスクとしてカウントされる（チケットの中核のユースケース）。四ステップの枯渇チェーンやガードへの介入はなく、レベル 2 は変更されていない。

### 1.2.0 (2026-08-15)
- チケット T-20260815-205101335 からの改修（検証依頼: 「グラウンディング・メタファーと組み合わせて、そこで解決策が成り立つか確認せよ」。納品されたスキルへの所見: 三点では成り立ったが、「照会して空だった」と「そもそも照会できなかった」の区別では成り立たなかった。チェーンは、Gardener/USMC/`_DECISIONS` がないシステムでも `STOP (exhausted)` を報告していたが、それを確認したことは一度もなかった。`grounding-seed` の最初の実際の適用例。チケット T-20260815-371628859）。
- **自己認識を追加:** チェーンの前に、固定された四つの場所を盲目的に探すのではなく、宣言された四つの必要項目（`decisions.ledger`、`memory.organic`、`memory.curated`、`user.model`）を確認する。
- **各チェーンステップ（2〜4）は found | empty | unavailable を報告する**（二値の結果ではなく）。二段階: まず所在確認（`decisions.ledger`/`user.model` は `grounding-seed`/`source-resolver` を経由、`memory.organic`/`memory.curated` は、まだ `source-resolver` プロバイダーを持たないため直接の CLI チェック）、内容確認は所在確認が成功した場合のみ。
- **`exhausted` は、四つのソースがすべて実際に照会可能だった場合にのみ適用される**（すべて found/empty、unavailable なし）。少なくとも一つのソースが到達不能だった場合のための、新しい区別可能な信号 `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)`。ループは終了するが、検査済みの結果とはもう主張しない。
- **ガードのフィンガープリントに可用性要素を追加**（現在 unavailable の役割のソート済みタプル）。「ガードが欠落を継承する」という後続の所見に対処する。この要素がないと、`exhausted`/`blind` が誤って設定されると、`_DECISIONS` チェーンが完全に欠けている場合、永久に有効なままになる（その場合、従来のフィンガープリント要素は一定になる）。この要素があれば、新たに利用可能になったソースは、自動的に再実行のチェーンを引き起こす（グラウンディング・メタファーの意味での「移植」）。
- 新しい、テスト済みのヘルパースクリプト `scripts/exhaustion_check.py`（+ `tests/test_exhaustion_check.py`、11 件のテスト、`grounding-seed` がインストールされている場合とされていない場合の両方の動作モードを確認）。自己認識／所在確認のチェックを決定的に提供するため、スキルが毎回の実行でそれを推測し直す必要がない。任意であることに変わりはない。このスキルは引き続き、モデルが自身のツールで従うプロトコルである。
- 依存関係: `grounding_seed.self_knowledge.assess()`/`status_from_resolution()` は `grounding-seed` 0.2.0 以降。0.1.0 の古い `grounding-seed` 版には分類の誤りがあった（`not_found` が誤って `empty` とされていた）。これは、ここで修正された区別をまさに曖昧にしてしまうものだった。`grounding-seed` がインストールされていない場合、文書化されたフォールバックは同一に動作する。

### 1.1.0 (2026-08-15)
- チケット T-20260815-385400870 からの参照の改修: ステップ 2（決定レジスタ）は、ハードワイヤードする代わりに、役割 `decisions.ledger`（`source_resolver.resolve(...)`、モジュール `source-resolver`）を経由して所在を解決するようになった。リゾルバーがインストールされていない場合は、従来のパスへの文書化されたフォールバックがある。機能の振る舞いは変更されていない。

### 1.0.0 (2026-08-15)
- チケット T-20260815-522639345 からの初版: 二層の運用モデル、四ステップの確認チェーン、`ticket-master` カテゴリに基づく区別の表、無限ループに対する USMC に支えられたガード、`/loop`/`/goal` 構造のための明確な終了信号。
