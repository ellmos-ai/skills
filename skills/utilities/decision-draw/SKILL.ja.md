---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "束ねられた未決の決定を、推奨された全バリアントに基づく一つのまとまりのある、散文ベースの全体コンセプトにまとめる。導入後にサブシステムがどのように具体的に組み合わさるかを示し、ユーザーを数十の独立した個別質問に向き合わせることを避ける。ユーザーは全体像をまとめて承認するか、狙いを定めた修正を出す。修正は自動的に個別の決定へ変換され、decision-briefing のフェーズ4を通じてレジスタへ書き戻される。このスキルは「全部に賛成したら全体はどう見えるか」「全体像を描いてほしい」「決定の全体コンセプト」「decision draw」「/decision-draw」「システムはどう連携するか」といった依頼で使用する。各項目の代替案を議論したい場合には使用しない（それは decision-briefing の役割）。依存関係グラフには使用しない（それは decision-path の役割）。選択肢と賛否を持つ構造化された個別ブロック（密接に関連するグループの場合も含む）には使用しない（それは decision-shot の役割）。単一の決定の導出には使用しない（それは decide の役割）。"
visibility: public
language: ja
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: da661fa325502ab0dfae6d6655d70650457d6ac1ff27ca5f0ce6289c375ef2c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — 束ねられた決定の全体像と承認

> 五つや十の決定が控えていると、個々の選択肢の細部に気を取られ、生まれつつあるシステム全体が見えにくくなる。decision-draw は代替案ではなく、機能する全体を描く。すべての推奨が受け入れられたとき、システムはどのように連携するのか。ユーザーは全体像をまとめて承認するか、狙いを定めて修正する。

---

## 使用するタイミング

- 互いに関連する複数の決定（[decision-briefing](../decision-briefing/SKILL.md) または決定テンプレートから）を、粘り強い個別質問のカタログとして処理したくない場合。
- ユーザーが承認の前に、実装後に各コンポーネントが日常でどのように実際に連携するかを確認したい場合。
- 依存関係グラフ（[decision-path](../decision-path/SKILL.md)）から、機能的な単位として承認できる密接に結びついた決定の束が特定された場合。
- トリガーワード: `/decision-draw`、「全部に賛成したら全体はどう見えるか」「全体像を描いてほしい」「決定の全体コンセプト」「decision draw」「その後システムはどう連携するか」「全体承認のための全体像」。
- **使用しないこと**:
  - ユーザーが各質問の選択肢を個別に比較し、文字（A/B/C）で選びたい場合 — それは [decision-briefing](../decision-briefing/SKILL.md) の役割。
  - ターミナルでの純粋な因果関係やブロッキングの分析 — それは [decision-path](../decision-path/SKILL.md) の役割。
  - 個別の質問や密接に関連するグループに対する、5部構成の個別ブロック（コンテキスト、選択肢ごとの賛否、推奨）による選択肢の検討 — それは [decision-shot](../decision-shot/SKILL.md) の役割。
  - 単一の未決の基本問題の方法論的な検討 — それは [decide](../decide/SKILL.md) の役割。

---

## 決定ファミリー内での位置づけ

| スキル | UX と焦点 | 選択肢への姿勢 | 承認の形 |
|---|---|---|---|
| `decision-briefing` | 個別質問に**分解**する | すべての選択肢 A/B/C/D を提示 | 文字コード（`1A 2C 3B`） |
| `decision-path` | 因果関係を**構造化**する | グラフ内で選択肢を評価 | ターミナルでの診断（ASCII） |
| `decision-draw` | **まとまりのある目標像**（関連する決定を束ねる） | **推奨バリアントのみ**を記述（代替案はリンク） | 全体承認または修正文 |
| `decision-shot` | **構造化された個別ブロック**（個別質問または密接なグループ向け） | 2〜4 件の賛否を持つ選択肢を提示 | Executive Decision / 個別承認 |
| `decide` | 個別ケースを**詳細に検討する** | 評価マトリクス（基準） | 分析的な推奨 |

> **中心的なルール:**
> `decision-draw` は**推奨バリアントのみ**を記述する。却下された代替案が消えたわけではない。それらは [decision-briefing](../decision-briefing/SKILL.md)、[decision-shot](../decision-shot/SKILL.md)、またはリンクされたチケットに記録されており、ヘッダーでリンクされる。この参照がない draw は、ユーザーの選択を助けるのではなく奪うことになる。

---

## 拘束力のある文体ルール: ユーザー向けテキストに記号と番号を使わない

> **正式なユーザー指示（フィードバック 2026-09-13 / チケット T-20260913-883789445）:**
> *「decision draws は私には技術的すぎます。番号なしにしてください。それらは背後で把握しているか、文章作成に使うものです […]。」*

1. **表示されるユーザー向けテキストに技術的な記号を使わない:**
   人が読む表示テキスト（束、コンセプト、連携、実装、問い合わせ）には、内部の記号（`BH-A`、`MD-A`、`HA-A`、`PRA` のような）、チケット番号（`T-2026...`）、D 番号（`D-2026...`）、相対パス、Git ハッシュ、測定値を**含めない**。
2. **項目ごとに 2〜4 文の平易な言葉を一人称で:**
   束の各項目は次の三つの要素で記述する:
   - *現状:* 現在の出発点は何か？
   - *「私は…する」:* 具体的に何を計画しているか／推奨する行動は何か？
   - *フォールバック:* それがうまくいかない場合に何が起こるか、あるいはユーザーはその後何を決めるのか？
   *（例:「Hermes はタスクで英語しか対応していません。Hermes に Issue として報告し、こちらではワークアラウンドを作ります。現在、使用できない旧セッションがあります。それを再び使えるようにしてみます。うまくいかなければ、10 セッションのランダムサンプルをお渡しして要約します。そうすれば救済に意味があるかどうか判断できます。」）*
3. **理解しやすい平易なタイトル:**
   各項目には分かりやすい日本語のタイトルを付ける（例:「独立した中核としてのモデルバックエンド」、「Mac 上の安全なデプロイキー」）。ユーザーはこのタイトルを使って操作するか、全体承認を出す。
4. **技術的な対応付けは付録だけに:**
   平易なタイトル、内部記号、チケット ID、レジスタ状態の対応付けは、文書末尾の付録表**だけ**で行う。自動パーサーとレジスタへの書き戻しが参照するのは、そこだけである。

---

## 拘束力のある構成（八部構成）

完全な `decision-draw` は例外なく次の構造に従う:

### 1. 束と範囲（平易な言葉で）
束に含まれる項目を平易な言葉で一覧にする（一人称、項目ごとに 2〜4 文、本文に ID や記号は使わない）。

### 2. コンセプト
すべての推奨がまさにそのように実装された場合の目標状態を、散文のまとまった文章として記述する:
- すべての推奨が正確に実装されたとき、どのようなシステム構成またはワークフローが生まれるか？
- 選択肢の並列比較や、「〜することもできる」といった並列の仮定法は使わない。
- 明確で正確な直説法: 目標状態でシステムはこのように動作する。

### 3. 連携
スキルの機能的な中核:
- 決定された部分は、実装**後に**実際にどのように連携するか？
- 単なるコンポーネント一覧ではなく、具体的なエンドツーエンドの流れに沿って示すことを優先する。
- データフロー、インターフェース、責任範囲を具体的にする。

### 4. 実装
具体的な実現の順序:
- 実際に現場で何が起こるか？
- エッジと依存関係のロジックは [decision-path](../decision-path/SKILL.md) から直接引き継ぐ。
- 独立した作業ストリームは正直に並行として示す（人工的な因果連鎖を作らない。束は複数の並行ストリームからなってよい）。順序は、裏付けのある依存関係や期限が存在する場合にのみ主張する。
- ゲート、移行ステップ、チェックを明示する。

### 5. この全体像がカバーしないもの
過剰な完全性の錯覚からの保護:
- どの周辺的な問い、未決事項、🔴 の信頼度は意図的に除外されているか？
- 隣接システムとのインターフェース境界はどこにあるか？
- 境界を隠す全体像は誤った安心感を生む。

### 6. 承認
ユーザーとのやり取り:
- ユーザーは全体像をまとめて確認する。
- 応答の選択肢 1: **明示的な全体承認**（「このままでいい」「承認」「このように実装する」）。この場合にのみ、束のすべての項目が決定済みとして記録される。
- 応答の選択肢 2: **平易なタイトルまたは平易な言葉による修正**（「Mac のデプロイでは自動再起動はしないで」「VersicherungsManager は当面延期」）。個別の決定に分解される。修正されなかった項目はすべて未決のままとなる。

### 7. 書き戻し
ユーザーの修正を個別の決定へ体系的に変換する:
- **修正の自動的な一括記録はしない:** 明示的な全体承認があった場合にのみ、変更のない項目が記録される。部分的な修正は全体承認**ではない**。
- **修正時の分離:** 修正が来た場合は個別の決定に分解し、束の残りの項目は、ユーザーが調整済みの全体像を全体として受け入れるか、残りの項目を個別に確認するまで、厳密に**未決**（元のレジスタ／テンプレート内）のままとする。
- **書き戻しの必須表:** ユーザーの修正に対する各フィードバックは、必ず四列の構造化された集計表（元の修正、影響を受ける記号、ドミノ状態、未解決の曖昧さ）を生成する。
- **フェーズ4経由の唯一の書き込み経路:** `decision-draw` はレジスタへの独自の書き込み経路を**持たない**。記録は [decision-briefing](../decision-briefing/SKILL.md) フェーズ4 の標準手順**のみ**を通じて行う。

### 8. 付録: 技術的な参照表（記録と監査のみ用）
文書末尾にあるコンパクトな表。内容は次のとおり:
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## 例（パイロット抜粋: Ticket-Master 2026-09-13 — BACH とシステム連携）

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## 実践のためのルール

1. **コンセプトに仮定法を使わない:** 全体システムを、すでに実現されているかのように記述する。ユーザーが求めているのは結果の明確さであり、理論上の可能性ではない。
2. **時系列より因果関係を優先:** *実装* セクションの順序は [decision-path](../decision-path/SKILL.md) の依存関係グラフの階層に従う。独立したストリームは正直に並行として示し、人工的な因果連鎖にねじ曲げない。
3. **書き戻し時の明示的なドミノチェック:** ユーザーの修正は、グラフ内で依存するノードが無効化されたり影響を受けたりしないかを確認せずに、単独で記録してはならない。
4. **部分修正時の自動一括記録をしない:** 明示的な全体承認があった場合にのみ、変更のない項目を記録する。部分修正のたびに、影響を受けない項目はすべて厳密に未決のままとし、全体像が再度承認されるか、項目が個別に確認されるまで保持する。
5. **フェーズ4経由の唯一の書き込み経路:** `decision-draw` はレジスタへの独自の書き込み経路を持たない。記録は例外なく [decision-briefing](../decision-briefing/SKILL.md) のフェーズ4 を通じて行う。
6. **レジスタの契約を尊重する:** 記録は常に決定レジスタの規則に従って行う（ID の振り直しをしない、一意の記録コード、正規の対象 `DECIDED-AND-DONE.md`）。
7. **ユーザー向けテキストに技術的な番号や記号を使わない:** 人が読む表示テキストには、ID、記号、パス、チケット番号を含めない。各項目は理解しやすい一人称で記述し、すべての識別子は付録表に移す。

---

## セッションの来歴

決定ドラフトが永続的なコンセプト文書として保存される場合、次の記述で終わる:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- 情報源の優先順位: 明示的な実行時／CLI の指定、次に権威あるプロバイダー環境またはフック、それ以外は `unbekannt`。
- サブエージェントは親セッションのセッション ID を引き継ぐ。
- 純粋なチャットテンプレートにはスタンプを付けない。

---

## 変更履歴

### 1.1.0 (2026-09-18)
- ユーザー向け決定テキストの文体ルールを定着（T-20260913-883789445、ユーザー指示 2026-09-13）:
  - 表示されるユーザー向けテキストに、技術的な記号、チケット番号・D 番号、パス、測定値を含めない。
  - 各項目について、一人称の平易な言葉 2〜4 文（現状、「私は…する」、フォールバック）。
  - 識別と承認のための、わかりやすい平易なタイトル。
  - 技術的な対応付け（記号、チケット ID、レジスタ状態）は、末尾の付録表（セクション 8）に厳密に移動。

### 1.0.1 (2026-09-13)
- レビュー後の改訂:
  - 書き戻しの契約を明確化: 部分修正時の自動一括記録をしない。影響を受けない項目は全体承認まで厳密に未決のまま。
  - 四列の書き戻し必須表（元の修正、影響を受ける記号、ドミノ状態、未解決の曖昧さ）を導入。
  - 例で複数ヒットを示した（一つのユーザー修正で `MD-A` と `CF-A` が同時に動く）。
  - 契約と例の両方で、`decision-briefing` フェーズ4 経由の唯一の書き込み経路を定着。
  - 例の人工的な因果連鎖の誤りを修正: 独立した項目を、正直に四つの並行作業ストリームとして示した（方法 a）。
  - `decision-shot` との違いを出力形式で明確化（個別ブロックと賛否、対全体承認を伴うまとまった目標像）。

### 1.0.0 (2026-09-13)
- ユーザー依頼 T-20260913-107991667 に基づく初版。
- 七部からなる拘束力のある構成（束、コンセプト、連携、実装、限界、承認、書き戻し）。
- `decision-path` に基づく束ね方のロジックと、`decision-briefing` フェーズ4 への書き戻しブリッジ。
