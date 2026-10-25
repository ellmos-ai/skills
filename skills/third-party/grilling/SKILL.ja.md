---
name: grilling
description: "計画、決定、アイデアについてユーザーに容赦なく問いかけます。ユーザーが考えを厳しく検証したい場合、「grill me」または「grill-me」と言った場合（旧コマンド /grill-me は /grilling に置き換わりました）、または「grill」を含む別のトリガーフレーズを使った場合に使用します。ドイツ語の「grill mich」「grill mich zu diesem Plan」「zerpflück meinen Plan im Grill-Modus」や、日本語の「私をグリルして」「この計画を徹底的に追及して」もトリガーに含まれます。計画セッションの終了時に、ユーザーが未解決の項目があるか尋ねた場合にも使用してください。"
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: ja
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

ユーザーと共通理解に至るまで、容赦なく質問を続けてください。これを**設計ツリー**として捉えてください。すべての決定は、そこから派生する決定へと分岐します。

ツリーは**ラウンド**単位で進めてください。**フロンティア**とは、前提となる決定がすでに確定しているすべての決定を指します。つまり、まだ聞いていない回答を推測することなく、_今_ 尋ねることができる質問です。フロンティア全体を1ラウンドで尋ねてください。各質問に番号を付け、推奨する回答も併せて示します。その後、次のラウンドに進む前にユーザーの回答を待ちます。

ラウンドは次のような形式で示してください：

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

ユーザーの回答が出るたびに設計ツリーは再構成されます。確定した決定はフロンティアを外側へ広げ、それらに依存していた質問を尋ねられるようにします。フロンティアを再計算し、次のラウンドを尋ねてください。回答が、このラウンドでまだ未解決の別の質問に依存する場合、その質問は今回のラウンドではなく_後のラウンド_に回してください。

_事実_を調べることはあなたの役割であり、ユーザーの役割ではありません。フロンティアの質問が環境（ファイルシステム、ツールなど）からの事実を必要とする場合は、サブエージェントを派遣してそれを調べてください。調べられることをユーザーに尋ねてはいけません。また、その調査の完了を待って全体を止めないでください。実行中の調査は未確定の前提条件であるため、その調査に依存する質問のみがサブエージェントの報告を待ちます。それ以外のフロンティアの質問は今すぐ尋ねてください。_決定_はユーザーのものです。それらをユーザーに提示し、回答を待ってください。

セッションは、フロンティアが空になったときに完了します。つまり、設計ツリーのすべての分岐を訪れ、暗黙のうちに仮定されたままの事項が何も残っていない状態です。ユーザーが共通理解に達したことを確認するまで、それに基づいて行動しないでください。

## ローカルな追加ルール

これらのルールは元の方法を拡張しますが、変更はしません。

1. **すでに書かれている内容から始めます。** 最初のラウンドの前に計画書と、プロジェクトで決定事項を記録している場所を読み、未解決・提案中・未確認の項目をすべて集めます。すでに決まった点は再質問せず、その記録を示します。
2. **次のラウンドの前に各回答を記録します。** すべての回答を、日付と情報源を添えてプロジェクトの決定記録に「決定済み」として記入します。チャットにしかない回答は、次のコンテキストリセットで失われます。
3. **中断時は一時停止し、最初からやり直しません。** ユーザーが先に別のことを頼んだら、それを済ませてから残っている未解決項目に戻ります。決着した問いはそのまま決着済みにします。
4. **各提案には理由を一つ添えます。** 推奨する回答と、その根拠となる事実またはルールを一つ示します。ユーザーが確認するまでは、提案は決定ではありません。
5. **確認した事実を示します。** 環境で調べた事実が質問の根拠になる場合は、分かったことと確認先を伝え、ユーザーが証拠に基づいて判断できるようにします。
6. **ユーザーの言語で質問します。** 質問と提案はユーザーの言語で行い、識別子は変更しません。
7. **最後に決定事項を一覧にします。** フロンティアが空になったら、決定したことと意図的に未決のまま残したことを列挙し、共通理解に達したかユーザーに確認します。

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Improved fork. Modifications vs. upstream:
- `description`: German trigger phrases ("grill mich"), the "grill me" /
  "grill-me" phrases, and the end-of-planning trigger were added.
- `category`, `language` and this comment were added (local convention).
- "Local additions" (rules 1-7) were appended after the upstream body. The
  upstream body above that heading is unchanged, so a resync only needs to
  replace that part.

Adopted 2026-08-24 per Ticket T-20260824-594031458, together with the thin
entry point skills/third-party/grill-me/ (upstream
skills/productivity/grill-me, `disable-model-invocation: true`, body
"Call the Skill tool with grilling"). On 2026-10-25 grill-me was removed at
the user's request: one skill instead of two, the phrase triggers moved into
this description. The native /grill-me command no longer exists; /grilling
replaces it. The description only adds semantic matching and registers no
alias command. Rules 1-7 come from a planning session of the same day.
-->
