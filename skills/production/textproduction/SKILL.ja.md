---
language: ja
---

> **日本語** — `textproduction` の公式日本語版。


# Textproduction — Router (日本語)

この Skill はあらゆるテキスト作成形式をカバーします。適切な
サブ Skill へルーティングします。詳細な手順はサブフォルダを参照してください。

## ルーティングテーブル

| サブ Skill | トリガー例 | 詳細手順 |
|---|---|---|
| **text** | 「ブログ記事を書いて」、「LinkedInの投稿5件」、「ニュースレター」、「商品説明」、「フォーマルなメール」、「Xを要約して」 | `text/WORKFLOW.md` |
| **storys** | 「脚本を書いて」、「短編小説」、「RPGアドベンチャーを作成」、「キャラクターシート」、「世界観設定」 | `storys/WORKFLOW.md` |
| **pr** | 「プレスリリースを作成」、「ポジションペーパー」、「PRパッケージ」、「PDF生成」 | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## ワークフローと手順

```
1. ユーザーの要望 → 上記のルーティングテーブル → 適切なサブ Skill を特定。
2. サブフォルダ内の詳細手順を読む (WORKFLOW.md)。
3. プロンプトパターンを選択し、プレースホルダーを入力してテキストを生成。
4. 品質チェック（各サブ Skill に記載）。
```

## 注意事項

- **ユーザー中立:** Skill 内に個人データ、APIキー、アカウント情報を含めない。
  設定（トーン＆マナー、文字数制限、PR用連絡先情報）はユーザーの責任となります。
- **PRツール:** `pr/press_compiler.py` は LaTeX (pdflatex/xelatex) を介して
  プレスリリースやポジションペーパーを PDF にコンパイルします。初回セットアップ: `pr/config.example.json` を
  `pr/config.json` にコピーし、連絡先情報を入力します。
- 意図的なスタイル最適化（オプション）: DeepL Write（月間最大50万文字まで無料）。

## 変更履歴

### 2.0.0 (2026-06-22)
- ルーターパターンへの再構成: SKILL.md = エントリポイント + ルーティングテーブル。
- 3つのサブ Skill: text/（6つのテキストタイプ）、storys/（4つの物語フォーマット）、
  pr/（プレスリリース + ポジションペーパー + LaTeX PDFコンパイラ）。
- press_compiler.py + LaTeX テンプレート + config.example.json を
  ai-media-editor/production/pr/ からここへ移動 (SSOT)。
- 関連 Skill の参照を内部サブ Skill パスに更新。

### 1.0.0 (2026-06-22)
- 初期バージョン。ai-media-editor/production/text/WORKFLOW.md から抽出。
- 根拠 provenance: BACH agents/_experts/textproduction/ (MIT)。