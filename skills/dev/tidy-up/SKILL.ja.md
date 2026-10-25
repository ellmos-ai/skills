---
name: tidy-up
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-19
description: "プロジェクトフォルダに対する一回限りのタスク解決・ライター・メンテナーのパスで、セッションが作業していたフォルダ（サブフォルダを含む）が対象です — システム全体のスイープではありません。未解決の自明な/自律的なレジスタ項目を解決し、ドキュメントを測定された現状に更新し（プロジェクト内と、プロジェクトが置かれているパイプラインのルートの両方）、迷子/一時ファイルをごみ箱の原則に従って片付けます。/tidy-up、「プロジェクトを片付けて」、「続ける前にここをきれいにして」、プロジェクトでの作業セッションの終わり、または /work-autonomous + /goal 内の期限到来した自律タスクとして、このスキルを使用してください。"
# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [hygiene, maintenance, cleanup, documentation, tasksolver, writer, maintainer, autonomy, goal, work-autonomous, ticket-master]
language: ja
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: [work-autonomous, bilingual-doc-sync]
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 27510ce60a4dd2defe9ee4686aeae6378ce8aea2f2376b98163d1d1340960233
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="tidy-up banner">

# Tidy Up — アクティブなプロジェクトフォルダに対するタスク解決・ライター・メンテナーのパス

## 目的

プロジェクトでの作業セッションの終わりには、通常ささいなことが残ります。完了しても チェックされなかった TODO 項目、古い状態ではなく測定された現状を示していない README、もう誰も必要としないテストファイルの一握りなどです。`tidy-up` は、**一つの** プロジェクトフォルダについて、まさにそれを整理する**一回限りの、自己制限されたパス**です — セッションがすでに作業していたフォルダです。常時実行されるループではなく、システム全体のスイープでもありません。

このパスは、モデルが自ら順番に担う三つの役割から成ります。

1. **TASKSOLVER** — プロジェクトレジスタの未解決の自明な/自律的な項目を解決するか、正しく振り分ける。
2. **WRITER** — ドキュメントを測定された現状に更新する。プロジェクト内と、プロジェクトが置かれているパイプラインのルートの両方を対象とする。
3. **MAINTAINER** — 衛生管理：迷子/一時ファイルを回収する（ごみ箱の原則）、レジスタ/カタログを整備する、残った項目はチャットで言及するだけでなく書き留める。

**このスキルを構築する前に測定した結果：** このライブラリ（2026-08-19 時点）には、`tasksolver`/`writer`/`maintainer` という名前の独立したスキルや役割は**存在しません** — スキル名としても、別のスキル内の文書化された役割としても存在しません（`skills/**/SKILL.md` の全文検索では、無関係な名前 `privat-mail-writer` 以外に一致がありませんでした）。したがって三つの役割は、外部からオーケストレーションするのではなく、以下にセクションとして直接定義されています。今後、独立した `tasksolver`/`writer`/`maintainer` スキルが作られた場合、`tidy-up` はロジックを重複させ続けるのではなく、それらを参照して引き継ぐべきです（このスキルを更新するたびに確認が必要です）。

## スコープ — 「アクティブなプロジェクトフォルダ」とは何か？

- このコンテキストでセッションが作業したプロジェクトフォルダ。**すべてのサブフォルダを含む**。隣接するプロジェクトへの移動や、パイプライン全体、ましてや `.TOPICS/` 全体へのスイープは行わない。
- **一つの限定的な例外**：ドキュメント/レジスタの更新は、プロジェクトが置かれているパイプラインの**ルートレベル**にも触れてよい（例：パイプライン全体の概要表にあるこのプロジェクトのステータス行）— ただし、このプロジェクトに関係する行/セクションのみで、パイプラインルート全体を並べ替えてはならない。
- 「アクティブなプロジェクトフォルダ」が不明確な場合（例：セッションが複数のフォルダで作業した）、最も近い共通のプロジェクトルートを取る（README/TODO/CLAUDE.md のあるところ）— 迷ったら、広げすぎるより狭く捉える。

## 役割 1 — TASKSOLVER

目標：プロジェクトレジスタ（`TODO.md`/`AUFGABEN.txt`/同等のローカル慣習）を正しい最新の状態にする。

1. プロジェクトレジスタを特定する（ローカルの慣習は新しいファイルより優先される — 共通ルールの「残ったタスクは記録する、言及だけで済ませない」を参照）。
2. 未解決の各項目を個別に評価する：
   - **すでに完了**（例：直前に終わったセッションによって）→ 完了としてマークする／`DONE.md` またはローカルの完了慣習に移す。
   - **自明かつ自律的に解決可能**（ユーザーの判断/承認/データ/ハードウェア/セッションが不要。`work-autonomous` の区別表を参照）→ 今すぐ解決し、その後完了として振り分ける。
   - **自明でない、または自律的でない**→ 触らないが、正しく振り分けた状態で残す（より良い置き場所がある場合は黙って放置しない — 例：とっくに `USER/*` のチケットカテゴリに値する項目）。
3. 新しいタスクを作り出さない — `tidy-up` は既存の残りを解決するものであり、新しい議題を生み出すものではない。

## 役割 2 — WRITER

目標：ドキュメントは、記憶や期待ではなく、**測定された**状態を示す。

1. プロジェクト内：README/CHANGELOG/ステータス行を、実際のコード/フォルダの状況に照らして確認する（例：挙げられたファイルがまだ存在するか、挙げられたバージョン番号が正しいか、「作業中」の印が既に古くなっていないか）。
2. パイプラインのルート：このプロジェクトを掲載するレジスタ/ステータス表が存在する場合（例：`.TOPICS/<Pipeline>/ROADMAP.md`、`STATUS.md`、パイプラインの README 内のプロジェクト表）、まさにこのプロジェクトの行/セクションを更新する。
3. **キュレーションされた内容は決して置き換えず、測定して更新するのみ。** 表、変更履歴、丁寧に書かれたセクションは、形式と語調を保つ — 事実（数値、状態、ファイル名、バージョン）のみを修正する。セクションがキュレーションされているか不確かな場合は、既存の表現を上書きするより、注記を追加する方を選ぶ。
4. 更新で足りる場合は、ゼロから書き直さない。
5. **翻訳の追補**（2026-08-19 追記、ライブでのユーザー依頼）：プロジェクトに、**ポリシー P-006**（`.SYNC/_policies/library/P-006_sprachstufen.md`）によってその段階で必須とされる言語版が欠けている場合、または既存の版が明らかに古くなっている場合、ライター段階がそれを追補する。P-006 の要約：**コアセット（DE+EN）は**公開されたリポジトリ/カタログ登録オブジェクトすべてに**必須**（リポジトリ：`README.md` EN + `README_de.md`；スキル：`SKILL.md` DE + `SKILL.en.md`）。フル/ワールドセット（ES/ZH/JA/RU、もしくは +FR/HI/AR/BN/PT）が目標像だが、一度の大規模キャンペーンで `tidy-up` によって行うのではなく、**段階的に**追補する。**ツール：既存のスキル `bilingual-doc-sync` をオーケストレーション（呼び出し）する。そのロジックは複製しない** — 「欠けている版の追補」＋セクション対応の確認＋乖離の是正をすでに扱っている。`tidy-up` は、アクティブなプロジェクトフォルダについて、どのオブジェクトのどの（P-006 により欠けている必須）言語かという契機を与えるだけ。翻訳品質、構造の対応、基準言語のルールは `bilingual-doc-sync` の責任のまま。**P-006 と同じ制約：** 測定された現状までのみ翻訳し、内容を創作せず、本物の発音区別符号/ウムラウトを使い、リポジトリのクールダウン（最後のコミットから24時間未満）とアクティブなロックを尊重する — その場合、この項目は翻訳せずに残し、オープン項目として書き留める（役割 3）。無理に押し通さない。

## 役割 3 — MAINTAINER

目標：何も失わずに衛生管理を行う。

1. **迷子/一時ファイルの回収**（スクリプトの残骸、`*.tmp`、重複コピー、忘れられたデバッグ出力）— ごみ箱の原則：ローカルの `_archive/` フォルダに移す（なければ作成し、`.gitignore` に登録する）。**決して直接削除しない**。出所/目的が不明な発見物については、読み込んで目的を積極的に突き止める — 読まずに片付けない（慣習「外部変更の再認証」を参照）。
2. **レジスタ/カタログの整備：** プロジェクトがより大きなカタログ/レジストリ（スキルレジストリ、モジュールマニフェスト、パイプライン概要）の一部である場合、このプロジェクトのエントリがまだ正しいか確認する — レジストリ全体を作り直さず、この一つのエントリだけを対象にする。
3. **残った項目はチャットで言及せず書き留める：** このパスの最後に残るもの（自律的に解決できない項目、発見したが修正していない不具合、意図的に先送りしたもの）は、「残ったタスクは言及せず記録する」の規則に従って書き留める — まずは発見場所にローカルで（プロジェクトの TODO.md/AUFGABEN.txt の慣習）、なければ中央で（`ticket-master`/`TASKPLAN`）、いずれも文脈付き（何が、なぜ未解決か、次の一歩）。
4. **ロックを尊重する：** 変更の前に、プロジェクトフォルダにアクティブな `LOCK.txt`/`LOCK.<scope>.txt`/`LOCK.user.*` がないか確認する。`LOCK.user.*` は、影響を受ける領域について `tidy-up` を完全に停止させる — 回避せず、ロックされた領域の部分的な tidy-up も行わない。
5. **コミットとプッシュは、各プロジェクトのリポジトリ慣習に従ってのみ行う** — 計画用と開発用の領域が分かれている場合、変更は承認されたローカルのプロジェクトクローンで行い、計画用または投影用のコピーでは行わない。プロジェクトがそれを定めている場合、自分の変更は共通の慣習「すぐに自分でコミット＋プッシュ」に従って扱う。

## 自己制限

`tidy-up` は**一回のパスであり、ループではない**。役割 3 の後、スキルは短い要約（何を解決し、何を更新し、何を片付け、何を未解決として書き留めたか）で終わり、呼び出し元のセッションに戻る。同じプロジェクトでその直後に再度 `/tidy-up` を呼ぶのは許されるが、自動的に意味があるわけではない — 以下の期限判定を参照。

## work-autonomous との関係

`tidy-up` の実行は、`work-autonomous` のレベル 1（通常の、目に見える作業 — 期限の来た `tidy-up` 実行がある間は、高コストなレベル 2 の使い尽くし確認に移る理由はない）の意味で**自律的に実行可能なタスクとして扱う**。実際には、`/work-autonomous` が `/tidy-up` と一緒に `/goal` 内で使われる場合、期限の来た `tidy-up` 項目も（`work-autonomous` の区別表に従って自律的に実行可能であれば）解決されるまで、ゴールは完了とはみなされない。ユーザーの判断を必要とする `tidy-up` 項目は、他の `USER/*` 依存のタスクと同様に、自律的とはみなされない。

**期限判定**（`tidy-up` の実行はいつ「期限が来た」か？）：

1. セッションは、このセッションのコンテキストで、すでに具体的なプロジェクトフォルダで作業している（単なる調査/読み取りのみで変更がない場合は、片付けるものがないので不可）。
2. このプロジェクトに限定した、直近の記録済み `tidy-up` 実行以降、クールダウンが過ぎている（既定：そのプロジェクトのセッション終了ごとに 1 回 — 新しい変更がないまま、同じセッション内で複数回実行しない）。
3. プロジェクトフォルダを塞いでいるアクティブな `LOCK.user.*` がない（役割 3、項目 4 を参照）。

直近の実行の記録（`work-autonomous` のガードパターンに倣うが、意図的にもっと簡素 — `tidy-up` には四段階の連鎖は不要で、プロジェクトごとにタイムスタンプが一つあればよい）：

```bash
usmc --agent <agent> note "tidy-up: project=<projekt-pfad-oder-slug> at=<ISO-Zeit> result=<done|nothing-to-do>" \
  --type context --priority 2 --tags "tidy-up-log,<projekt-slug>"
```

新しい実行の前に、同じタグを `tidy-up-log,<projekt-slug>` でフィルタした `usmc --agent <agent> working --limit 20` から読み、基準 2 を確認する。

`/goal` の構造（存在する場合、または構築される場合 — `work-autonomous` 自体は `/goal` を呼び出さない。該当セクション「意図的に組み込まない `/goal`」を参照）は、この期限判定を、`work-autonomous` 自身の中断シグナルを読むのと同じように読む：`tidy-up` の実行が期限到来かつ自律的に実行可能であれば、ゴールはまだ完了していない — `work-autonomous` 自身の四段階の連鎖がすでに「使い尽くした」と報告していても、である。

`work-autonomous` スキル自体への、最小限に侵襲的な対応する追加項目（レベル 1、新しい情報源「アクティブなプロジェクトの期限到来 tidy-up 実行」）がこの拡張の一部であり、該当箇所の変更履歴の項目を参照。

## 関連スキル

- **`work-autonomous`** — 上記を参照。`tidy-up` は `work-autonomous` のレベル 1 が処理する情報源の一つであり、その使い尽くし確認の代わりにはならない。
- **`bilingual-doc-sync`** — 翻訳追補のため、ライター段階（役割 2）によってオーケストレーションされる（上記参照）。複製はしない。`tidy-up` は P-006 により何が欠けているかだけを決め、`bilingual-doc-sync` はどのように翻訳・同期するかを決める。
- **`bugsweep`** — 倍増エスカレーションを伴う体系的なバグ検索。目的が異なる（欠陥を見つけるのであり、レジスタ/ドキュメント/衛生管理を維持するのではない）。重なる場合（バグ検索の発見がレジスタに入る）、`tidy-up` はレジスタの整備のみを担い、バグ検索自体は行わない。
- **`dev-cycle`** — 新機能開発のための八段階の枠組み。`tidy-up` は開発枠組みではなく、すでに行われた作業の後の締めくくり/衛生管理のパスである。
- **`folder-flattening`** — 入れ子のフォルダ階層を再構成する。`tidy-up` は既存の構造の中でファイルを片付けるものであり、構造そのものは変えない。

## 例

```
User: "/tidy-up"
(Session hat gerade am autorisierten lokalen Checkout von `beispiel-projekt` gearbeitet)

→ TASKSOLVER: TODO.md gelesen — 2 Punkte bereits durch die Sitzung erledigt (nach DONE.md
  verschoben), 1 trivialer Punkt ("README-Tippfehler in Zeile 12") autonom geloest, 1 Punkt
  braucht Nutzerentscheidung (unveraendert stehen gelassen).
→ WRITER: README-Versionsangabe war 1.2.0, tatsaechlich 1.3.0 (package.json) — korrigiert.
  Pipeline-Root-Statustabelle: Zeile fuer "beispiel-projekt" von "in Arbeit" auf "aktiv" gesetzt.
→ MAINTAINER: 3 Debug-Skripte im Projektroot gefunden, nach _archive/ verschoben (Zweck geprueft:
  einmalige Testskripte, nicht mehr referenziert). Skill-Registry-Eintrag geprueft: stimmt.
  1 offener Punkt (Nutzerentscheidung) in AUFGABEN.txt belassen, dort bereits korrekt einsortiert.
→ USMC-Log geschrieben: tidy-up: project=beispiel-projekt at=2026-08-19T14:30 result=done
→ Zusammenfassung an Nutzer: 3 geloest, 2 Doku-Stellen aktualisiert, 3 Dateien archiviert, 1 Punkt
  offen (Nutzerentscheidung noetig).
```

```
Kombiniert mit /goal + /work-autonomous:

/goal "Projekt X fertigstellen" mit /work-autonomous + /tidy-up als Bedingungen
→ work-autonomous Ebene 1 findet: ACTIONABLE-Ticket erledigt, dann kein weiteres Ticket mehr,
  ABER tidy-up-Faelligkeitskriterium erfuellt (Session hat an Projekt X gearbeitet, kein
  protokollierter Lauf seit Sitzungsbeginn, kein LOCK.user aktiv) → tidy-up-Durchlauf ausgefuehrt.
→ Erst NACHDEM tidy-up "done" meldet UND work-autonomous Ebene 2 "exhausted" meldet, gilt das
  Goal als abgeschlossen.
```


## 変更履歴

### 1.1.0 (2026-08-19)
- チケット T-20260819-461890468 に対してライブで追加されたユーザーの補足を反映（ユーザーの原文：「bis zu einer uebersetzung nachzuziehen die noch nicht existiert soll auch zum skill gehoeren」）：役割 2（WRITER）に、**ポリシー P-006**（言語段階：コアセット DE+EN は必須、フル/ワールドは段階的に）に基づく翻訳追補の五つ目の項目を追加。ツールは既存のスキル `bilingual-doc-sync` — 複製ではなくオーケストレーションする。フロントマターの依存関係と「関連スキル」の項目を追加。

### 1.0.0 (2026-08-19)
- チケット T-20260819-461890468 からの初版。ライブラリ全体の全文検索で、独立した `tasksolver`/`writer`/`maintainer` スキルが存在しないことを確認したため（存在すればオーケストレーションし、複製はしなかった）、三つの役割（タスク解決/ライター/メンテナー）をスキル内のセクションとして定義。スコープをアクティブなプロジェクトフォルダとパイプラインルートのステータス行に限定。ゴール統合：`tidy-up` の実行を `work-autonomous` レベル 1 の情報源として扱い、独自の簡素な USMC 期限判定ログを持つ（`work-autonomous` 自体の四段階ガードは持たない — `tidy-up` には構造が単純すぎるため）。`work-autonomous` 1.3.0 に、最小限に侵襲的な対応する追加項目を追加（該当箇所の変更履歴を参照）。
