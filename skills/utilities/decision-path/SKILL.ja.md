---
name: decision-path
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "未決定の決定のリストから、ターミナル向けの構造化された ASCII 依存関係グラフ（最大 100 列）を生成します。各ノードを 5 つの固定基準で評価します。妥当性、推奨、ユーザーの典型的なやり方との適合（方向性と decision-avatar の信頼度を分けて評価）、整合性、矛盾です。エッジには関係の種類と根拠ステータスを付与します。ブロッカー、ゲート解除、順序、相反する推奨を容赦なく明らかにします。次のような依頼のときにこのスキルを使用してください。「どの決定が互いに依存しているか」「決定の依存関係グラフ」「決定経路を可視化」「決定間の矛盾を確認」「決定の順序」、/decision-path。決定をまず洗い出す目的には使用しないこと（それは decision-briefing の役割です）。推奨される全体構想を承認用にまとめる目的には使用しないこと（それは decision-draw の役割です）。選択肢と賛否を備えたコンパクトな 5 項目の単独ブロックには使用しないこと（それは decision-shot の役割です）。フレームワークを用いた個別事案の検討には使用しないこと（それは decide の役割です）。"
visibility: public
language: ja
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, abhaengigkeiten, ascii-graph, decision-path, visualisierung, routing, widerspruchs-erkennung]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-draw, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: 68422f7ca7043f158883734f79aadf21f8830b6238588a896255dccd8abc952a
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="decision-path banner">

# decision-path — 未決定事項の ASCII 依存関係グラフ

> 決定は真空の中で行われるわけではありません。単独で見れば妥当に思える案が、
> 後続作業をブロックしたり、未完成の前段階を必要としたり、既存の保護契約を
> 無効にしたりすることは少なくありません。decision-path は、因果関係、順序、
> 矛盾をターミナル上で透明に可視化します。

---

## 使用するタイミング

- 未決定事項の候補リスト（[decision-briefing](../decision-briefing/SKILL.md) のフェーズ 1、セッションコンテキスト、または決定テンプレートから得たもの）を構造化したいとき。
- どの決定がただちに自由に決定可能か（ルートノード）と、どの決定が前提条件や外部ブロッカーに依存しているかを明確にする必要があるとき。
- どの推奨同士が調和しているか、また二つの決定がどこで論理的または組織的に矛盾しているかを俯瞰したいとき。
- トリガーワード: `/decision-path`、「どの決定が互いに依存しているか」「決定の依存関係グラフ」「決定経路を可視化」「ASCIIの決定ツリー」「決定間の矛盾」「因果関係を確認」。
- **使用しないこと**:
  - 未決定の問いを初めて記録し、洗い出す場合。これは [decision-briefing](../decision-briefing/SKILL.md) のフェーズ 1 が担当します。
  - 推奨される選択肢を承認用に一つの整合した全体像にまとめる場合。これは [decision-draw](../decision-draw/SKILL.md) が担当します。
  - 選択肢と決定ごとの賛否を備えた、コンパクトな 5 項目の単独ブロックを作る場合。これは [decision-shot](../decision-shot/SKILL.md) が担当します。
  - 一つの複雑な問いを方法論的に検討する場合（加重スコアリング、シナリオ）。これは [decide](../decide/SKILL.md) が担当します。

---

## 決定ファミリー内での役割分担

| スキル | 役割 | 入力 | 出力 |
|---|---|---|---|
| `decide` | **一つの**決定を方法論的に検討する | 基準、選択肢 | 評価マトリクス、個別の決定 |
| `decision-briefing` | 多数の未決定事項を個別の問いに分解し、選択肢を付ける | 未決定事項のリスト | 番号付き A/B/C/D ブリーフィング、大まかなマーキング、記録 |
| `decision-path` | 多数の決定にわたる**因果関係と矛盾を検証・可視化する** | ブリーフィング/ レジスタからの大まかなマーキング | 5 つのノード評価とエッジステータスを持つ ASCII 依存関係グラフ |
| `decision-draw` | 承認のために推奨事項を**全体像にまとめる** | `decision-path` からの束 | 構想、連携（推奨案のみ）、差し戻し |
| `decision-shot` | **完了した分析**を要点に圧縮する（1 件の決定または小さな束） | 分析済みの 1 件の問いまたはグループ | 選択肢、賛否、完全分析へのリンクを含む 5 項目の要約 |
| `decision-avatar` | **ユーザーの好みのモデリング**を提供する | コンテキスト、これまでの決定 | 信頼度評価 🟢 / 🟡 / 🔴 |

### decision-briefing との契約と責任の分担

`decision-briefing` のフェーズ 1 は、読み込み時点で依存関係と順序を大まかに把握しています（例: 「その後自動的に:」のようなシグナル語、ブロッカー、チケット参照など）。`decision-path` は、この構造を黙って二度導出することはせず、これらの大まかなマーキングを直接の土台とします。

1. **decision-briefing が大まかなマーキングを提供する:** 未決定事項の生の一覧と、その最初の連結シグナルを用意します。
2. **decision-path が検証・評価・可視化する:** シグナルを実際の根拠の状態と照合し、確認済みのエッジと推測されるエッジを区別し、各ノードに 5 つの評価を付け、ゲートの衝突を容赦なく明らかにします。
3. **不一致がある場合のフィードバック:** `decision-path` が、ブリーフィングに欠けている、または不完全に記録されている依存関係を見つけた場合、それを決して黙って取り込むことはせず、修正メモとしてブリーフィングに差し戻します。

---

## ノードごとの 5 つの評価（およびエッジの根拠ステータス）

5 つの次元 `[S E U Z W]` は、**ノード**（システム的な文脈における未決定または完了済みの決定）を評価します。エッジは、その意味上の関係の種類（例: 解放する、ブロックする、前提とする）と根拠ステータス（確認済み / 推測）を持ちます。

グラフ内の各ノードは、ちょうど 5 つの次元を持つ簡潔な評価行を持ちます。

```
[S+ E:<Option> U<Richtung><Konfidenz> Z+ W-]
```

1. **妥当性（`S`）** — 専門的およびアーキテクチャ上の実現可能性:
   - `S+`: 解決策は堅牢で、現実の問題を解決し、不必要な複雑さを避けている。
   - `S~`: 部分的に妥当だが、保守やプロセス上のリスクを抱えている。
   - `S-`: 見せかけの解決策、行動のための行動、または既知の袋小路（例: 誤った箇所でのフィルター）。

2. **推奨（`E`）** — 具体的で事実に基づく行動推奨:
   - `E:<Option>`: 明確な選択肢（例: `E:A`、`E:B`、`E:klaeren`、`E:Schritt1`）。
   - `E-`: 推奨不可（事実が不足している場合や、真の根本的問題である場合など）。

3. **ユーザー適合（`U`）** — ユーザーの作業方法とルールとの一致（`decision-avatar` を経由）:
   **方向性**と**根拠の確実性 / 信頼度**を分けて符号化する:
   - **方向性（U の後の最初の文字）:**
     - `+`: ユーザーの典型的なやり方に合致 — 過去に根拠のある決定、ガイドライン（`CLAUDE.md`、ポリシー）、または明示されたユーザーの好みに一致する。
     - `~`: 中立 / 未定 — 明確な好みの方向性を根拠づけられない。
     - `-`: 典型的ではない — ユーザーのこれまでの作業方法やパターンから外れている。
   - **根拠の確実性 / 信頼度（2 文字目）:**
     - ASCII グラフ内では純粋に ASCII で表記する:
       - `!`: 高い / 確実（文章では: 🟢 根拠あり）。
       - `~`: 中 / もっともらしい（文章では: 🟡 価値判断、ユーザーによる比較検討が必要）。
       - `?`: 低い / 不確実（文章では: 🔴 未知の領域、根本的な問い）。**推測せず、エスカレーションすること！**
   - *例:* `U+!`（ユーザーの典型的なやり方に合致し、根拠あり）、`U+~`（ユーザーの典型的なやり方に合致するが、比較検討が必要）、`U-!`（根拠ありで典型的ではない）、`U~?`（未定、指定なし → エスカレーション）。

4. **整合性（`Z`）** — 隣接ノードとの柔軟な文体上およびアーキテクチャ上の適合性:
   - `Z+`: 文体およびアーキテクチャ上で継ぎ目なく適合し、摩擦のない一貫した全体を形成する。
   - `Z~`: 軽微な文体上の摩擦や組織上の追加作業はあるが、機能的には両立する。
   - `Z-`: システム全体の中で目立つ摩擦が生じる（例: 設定の乱立、不適切な結合、パラダイムの断絶）が、まだ厳格なルールには違反していない。

5. **矛盾（`W`）** — 厳格な矛盾およびルール / ゲートへの違反（**最も重要な出力 — 警報！**）:
   - `W-`: 他の推奨、拘束力のあるガイドライン、有効な保護ゲートと矛盾しない。
   - `W+`: **厳格な衝突 / 警報！** 別の推奨を無効にする、拘束力のあるポリシー（`CLAUDE.md`、P-00x）に違反する、または有効な保護ゲートを無視する。衝突するノードは、必ず原因と解消方法とともに `WIDERSPRUECHE` のセクションに記載しなければならない。

---

## エッジの種類と導出ルール

依存関係は**厳密にソースの記述から導出**し、推測で作り出すことは決してしません。エッジにはその関係の種類と根拠ステータスを付与します。

| テキスト内のシグナル | エッジの種類 | 表記 | 意味 |
|---|---|---|---|
| 「その後自動的に: …」、「解放する」、「可能にする」 | 解放する | `+-->` | 元の決定によって初めて、先の決定を実行できるようになる（確認済み） |
| 「ブロックする」、「防ぐ」、「保護ゲートが作動する」 | ブロックする | `=>` | 元の問題が解決されるまで、先の決定はブロックされたままである |
| 「前提とする」、「事前に必要とする」、「前提条件」 | 前提とする | `-->` | 先の決定は、時系列でも論理的にも元の決定を必要とする |
| 「後続の決定」、「その後のステップ 2」 | 順序 | `-->` | 実行後の論理的な後続ステップ |
| 「測定により反証されている」、「時代遅れになった」、「無効になった」 | 無効化 | `--X-->` | 元の知見によって、先の項目が陳腐化する |
| 同じ D-ID、チケットID、または同じシステムだが、テキストによる根拠がない | 推測 | `?-->` | 明示的な因果関係の証拠のない、もっともらしい結合（根拠なし） |

> **根拠のないエッジに関するルール:**
> テキスト内に明示的な因果関係の根拠がない場合、そのエッジは推測（`?-->`）として示し、確認済みの事実として示すことは決してしません。関連が全く根拠づけられない場合、ノードは互いに独立して並べて表示します。

---

## ASCII グラフの形式要件

1. **等幅フォントとターミナル向け:** 最大行幅は **100 列**。ターミナルで折り返されるような幅の広い表は使用しない。
2. **文字セットと純粋性:** 純粋な ASCII を使用する。グラフのコードブロック内では絵文字（🟢🟡🔴）を使用しない。信頼度はそこでは ASCII 文字（`!`、`~`、`?`）のみで符号化する。
3. **ノード ID:** 既存の略語のみを使用する（`PD-A`、`MD-A`、`BH-A`、`VM-A`、`QR-A`、`CL-A`、`MO-A`、`D-001`、`732597768`）。新しい架空の ID は決して作らないこと。略語がない場合は項目番号を使用する。内部の後続ステップは、エッジ上で番号のない注釈 `(...)` として記載する。
4. **階層構造:**
   - `EBENE 0 - haengt an nichts`: ルートノード、ブロックされていない決定、外部のレバー。
   - `EBENE 1 - haengt an genau einer`: 直接の後続決定。
   - `EBENE 2 - haengt an mehreren / tiefe Kette`: 複数に依存する、または下流にあるノード。
   - `WIDERSPRUECHE`: 厳格な矛盾、ゲートの衝突、一貫しない推奨（`W+`）。
   - `LEGENDE`: すべてのグラフに必須の要素。グラフで使用されるすべての構造記号（`|`、`=Option`、`(...)`、エッジの矢印）は、凡例に記載して説明しなければならない。
5. **任意の Mermaid 投影:** 追加労力なしで済む場合に限り、必要に応じて追加のコードフェンス（`mermaid`）として添付してよい。ASCII グラフが引き続き拘束力のある一次出力である。

---

## 例（パイロット抜粋: Ticket-Master 2026-09-13）

Ticket-Master の決定テンプレートからの実際の抜粋（`732597768`、`MO-A`、`CL-A`、`QR-A`、`387521104`、`CL-B`）:

```
====================================================================================================
DECISION-PATH: ABHAENGIGKEITSGRAPH (Pilot Ticket-Master 2026-09-13)
====================================================================================================

EBENE 0 - haengt an nichts (Wurzelentscheidungen & externe Blocker)
  [732597768] GitHub-Billing klaeren                        [S+ E:klaeren U+! Z+ W-]
      |  schaltet frei
      +--> [MO-A] Welle 2 freigeben                         [S+ E:A       U+~ Z+ W-]

  [CL-A] clutch Admin-Merge PR #6 & PR #8                   [S+ E:A       U+! Z+ W-]
      |  blockiert durch: [Gate "1 Approving Review" (Self-Approval unmoeglich)]
      --> (Folgeentscheidung: Branchschutz auf 0 oder Bot anpassen)

  [QR-A] Queue-Rename Junction (_TICKETS -> TICKETS)        [S+ E:B       U+! Z+ W-]
      +--> [387521104] Nachtfenster faehrt                  (belegt: nur unter B)

  [CL-B] Review-Gate-Pilot: Mac-Signierschluessel           [S+ E:Schritt1 U+~ Z+ W-]
      --> (Folgeschritte 2-4: Modell-Automatisierung nach Schluessel-Bereitstellung)

EBENE 1 - haengt an genau einer Vorbedingung
  [MO-A] Welle 2 freigeben                                  [S+ E:A       U+~ Z+ W-]
      |  setzt voraus: [732597768] (Billing geklaert, Remote-CI-Gates wieder aktiv)
      |  setzt voraus: [Gate PRIVATE.txt "gruenes Remote-CI"]
      --> (Folgeschritt: Sichtbarkeit schalten bleibt reine Nutzerhandlung)

EBENE 2 - haengt an mehreren / tiefe Kette
  [387521104] Nachtfenster Migration autonom fahren         [S+ E:B       U+! Z+ W-]
      |  setzt voraus: [QR-A]=B (NTFS-Junction gesetzt)
      |  setzt voraus: (Junction auf dem zweiten Host per Transfer-Ticket gesetzt -
      |                  Ticketnummer in der Vorlage nicht genannt)

----------------------------------------------------------------------------------------------------
WIDERSPRUECHE & GATE-KOLLISIONEN
----------------------------------------------------------------------------------------------------
  [MO-A]=B  X  [Gate PRIVATE.txt "gruenes Remote-CI"]
               Konflikt: Option B wuerde Welle 2 rein auf lokaler Testbasis freigeben,
               obwohl zwei Modulvertraege ausdruecklich gruenes Remote-CI fordern.
               Aufloesung: Empfehlung A erzwingt erst [732597768] (Billing), heilt Kollision.

  [CL-A]=StatusQuo  X  [Gate "1 Approving Review" (Self-Approval unmoeglich)]
               Konflikt: master verlangt 1 Review, einziges Repo-Konto ist lukisch.
               Aufloesung: Empfehlung A (Admin-Merge) bricht Blockade legitim auf.

----------------------------------------------------------------------------------------------------
LEGENDE & BEWERTUNGSSCHLUESSEL
----------------------------------------------------------------------------------------------------
  Kanten & Struktur:
    +-->   schaltet frei (Kausalitaet im Quelltext belegt)
    =>     blockiert / verhindert (Gate oder externer Blocker)
    -->    setzt voraus / Reihenfolge (Vorbedingung oder Folgeschritt)
    ?-->   vermutete Abhaengigkeit (Koppelung plausibel, aber unbelegt)
    --X--> entwertet / ueberholt (macht Zielposten obsolet)
    X      Widerspruch / Kollision (Gate- oder Regelverletzung)
    |      vertikaler Verbindungsstrang / Attribut-Zuordnung
    [ID]   Entscheidungsknoten (Kuerzel oder Postennummer aus Vorlage)
    [Gate]  externes Gate / Regel / Vertrag - KEIN Entscheidungsknoten
    =Opt   spezifische Option eines Knotens (z. B. [MO-A]=B)
    (...)  unnummerierte Kanten-Annotation / Folgeschritt (keine neue ID)

  Knoten-Status [S E U Z W]:
    S: Sinnvoll      (+ tragfaehig / ~ mit Vorbehalt / - ungeeignet)
    E: Empfohlen     (A, B, C, klaeren, Schritt1, - keine Empfehlung)
    U: Usertypisch   (Richtung: + typisch / ~ neutral / - untypisch;
                      Konfidenz: ! gesichert / ~ Abwaegung / ? Eskalation)
                      [! = belegt (Prosa gruen), ~ = Nutzerabwaegung (Prosa gelb),
                       ? = ungesichert / Eskalation (Prosa rot)]
    Z: Zusammenpass. (+ harmoniert stilistisch / ~ Reibung / - Architektur-Bruch)
    W: Widerspruch   (- widerspruchsfrei / + harte Kollision mit Gate oder Regel)
====================================================================================================
```

---

## decision-path が行わないこと

1. **決定を下さない:** このスキルは状況の透明な地図を提供する。決定権はユーザーに残る。
2. **選択肢を作り出さない:** このスキルは新しい案や基準カタログを議論しない。それは [decide](../decide/SKILL.md) または [decision-briefing](../decision-briefing/SKILL.md) の役割である。
3. **レジスタへの書き戻しをしない:** グラフはレジスタやチケットのファイルを変更しない。決定後の書き戻しは、[decision-briefing](../decision-briefing/SKILL.md) のフェーズ 4、または [decision-draw](../decision-draw/SKILL.md) の差し戻しの仕組みによって行われる。
4. **ユーザー向けの本文に分かりにくい略語を使わない:** グラフの結果をユーザーに説明する場合、拘束力のある文体ルール（T-20260913-883789445）が適用される。一人称（「私」）による日常的な言葉で 2〜4 文（状況、「私は…します」、フォールバック）を用いる。ノードのラベルには読みやすい短いタイトルを使う。技術的な識別子やチケット番号は付録の表に移す。

---

## セッションの来歴

依存関係グラフを永続的な分析成果物として保存する場合、文書は次の内容で締めくくる:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- ソースの優先順位: 明示的なランタイム / CLI の指定、次に信頼できるプロバイダー環境またはフック、それ以外の場合は `unbekannt`。
- サブエージェントは親セッションのセッション ID を引き継ぐ。
- 通常のチャットや一時的なターミナル出力にはスタンプを付けない。

---

## 変更履歴

### 1.1.0 (2026-09-18)
- 分かりやすい決定文書のための文体ルールを定着させた（T-20260913-883789445、ユーザー指示 2026-09-13）:
  - ユーザーへの説明は、番号の洪水を避けた自然な一人称で行う。
  - ターミナルグラフのノードには、読みやすい短いタイトルを使う。
  - 技術的な対応関係（チケット / D 番号）は付録の表に切り出した。

### 1.0.0 (2026-09-13)
- ユーザー依頼 T-20260913-107991667 に基づく初版。
- ノードごとの 5 項目の評価キー（妥当性、推奨、方向性と信頼度を分けたユーザー適合（`decision-avatar` 経由）、整合性、矛盾）を導入。エッジには関係の種類と根拠ステータスを付与。
- `decision-briefing` との拘束力のある契約を定めた: ブリーフィングが大まかなマーキングを提供し、decision-path が検証・可視化する。不一致がある場合はフィードバックを返す。
- 出力形式（選択肢と賛否を備えたコンパクトな 5 項目）によって `decision-shot` との境界を明確化。
- 因果構造を修正: CL-A を請求ではなく承認ゲートに配置。架空の ID を排除し、番号のないエッジ注釈に置き換えた。
- 統一された ASCII 仕様（最大 100 列）と、統一されたエッジ表記 `--X-->`、完全な構造凡例、絵文字を含まないグラフコードを整備。
