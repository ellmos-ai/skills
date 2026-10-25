---
name: tech-detect
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "根拠付きのハードウェア・ソフトウェア版数を私的なスナップショットに記録し、未観測を未インストールと断定せずホストを比較する。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [inventory, hardware, software, python, versions, host-comparison]
language: ja
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# Tech Detect

所有または明示的に許可されたホストだけを対象にする。既存インベントリとホスト別スロットの規則を先に読む。`.SYNC/_inventory` 型の構成では `systems/<自ホストのスロット>.json` を入力とし、このスキルは種ファイルや他ホストのスロットを更新しない。

1. 権限、ロック、ホスト識別、非公開の出力先を確認し、`python -X utf8 scripts/techshot.py capture --seed <インベントリ>/systems/<自ホスト>.json --slot <自ホスト> --output <非公開>/techshot-<UTC>.json` を実行する。
2. オフラインの補助スクリプトはローカルのプラットフォームと Windows のアンインストール用レジストリ、利用可能な `dpkg-query` または Homebrew を読む。どの情報源も全アプリの網羅を保証しない。`Win32_Product` は使わない。[Microsoft の説明](https://learn.microsoft.com/en-us/powershell/scripting/samples/working-with-software-installations?view=powershell-7.6)では MSI の整合性確認と修復の副作用が示される。
3. 実行中の Python、PATH で見つかった各候補、`--python-path` で明示した導入先や仮想環境を分ける。標準では実行中の版数だけが正確。信頼できるパスに限って `--probe-python <パス>` で `-I -S --version` を明示実行し、そうでなければ版数を未知とする。
4. 各導入に製品・導入識別子、版数、出典と品質 `observed`、`reported`、`uncertain`、`unknown` を残す。種ファイルのハードウェア値は申告値として扱い、収集失敗と対象範囲を示す。
5. `python -X utf8 scripts/techshot.py compare --left <a.json> --right <b.json> --output <比較.json>` で非公開スナップショットを比較する。版数差と片方で未観測は別物であり、未観測は削除の証明ではない。別名を統合するにはベンダー根拠が必要。
6. 定期収集は許可後に既存のスケジューラへ接続し、実際の実行記録を別途確認する。コードのコミットだけでは有効化されない。

JSON 契約は `ellmos.techshot.v1` と `ellmos.techshot-comparison.v1`。既存インベントリに並ぶ観測結果であり、私的パスを含み得る。未知の版数から安全性や脆弱性を断定しない。`security-tech-stack-check` には必要な構成要素とハッシュだけを渡す。

## 変更履歴

### 1.0.0 (2026-10-25)

- オフラインのスナップショットと根拠品質付きホスト比較。

ハードウェアの観測は在庫の申告値と分け、OS、アーキテクチャ、CPU、RAM、システムファイルシステム容量に出典または unknown を付ける。移植可能な収集手段がなければ GPU は unknown。Linux では dpkg-query または rpm を読む。ホスト比較の unknown を一致とみなさない。シリアル番号、MAC、PATH 全体は収集しない。

比較契約: slot が異なれば hostname が同じでも axis=cross-host。同じ slot と hostname で収集時刻が異なる場合は axis=same-host-time。結果には chronology、双方のハッシュ、収集時刻、ホスト、元の在庫と収集範囲を残す。既知版が同じでも未知の追加インストールは version-uncertain として残す。必須の出典が欠ければ拒否し、完全な過去の記録は年齢に関係なく比較できる。比較時刻は新しい測定ではない。
