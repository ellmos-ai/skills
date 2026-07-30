---
name: repo-publish-check
description: 在代码库首次公开前或后续复查时使用的用户中立检查，覆盖隐私、秘密信息、许可证、第三方内容、文档和批准状态，但不执行公开操作。
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-07-30
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [release, privacy, license, repository, publication]
language: zh
status: active
dependencies:
  tools: [git]
  services: []
  protocols: []
  python: []
---

<img src="banner.png" width="100%" alt="repo-publish-check banner">

# Repo Publish Check

## 用途

在首次公开前或公开后的复查中检查代码库。未通过也是有效结果。只有获得代码库
所有者的明确批准后，才能更改可见性。

本 Skill 不生成法律意见。对于法律敏感领域或不明确的个案，请使用公开的
`law-checker` Skill。两者都不能替代专业法律咨询。

## 检查记录的隐私

切勿将检查报告或风险评估 Commit 到被检查的代码库。将其保存在项目外的私有区域，
或 `<private-review-dir>` 等已被 gitignore 的目录。公开侧只包含必要的修正。

## 检查流程

1. 通过 `git ls-files`、`.gitignore` 和软件包允许列表确定公开内容；排除内部笔记、
   报告、测试数据、本地设置和锁文件。
2. 在工作树和所有可达历史中搜索凭据、Token、私钥、本地用户路径、联系方式和
   个人数据。
3. 提供合适的 `LICENSE`，并记录第三方代码、Prompt、文档和媒体的来源与许可证。
4. 说明用途和边界。涉及法律、健康、金融、安全或个人数据时，记录数据流和排除
   用途，并将法律问题交给 `law-checker`。
5. 最小化数据，披露外部处理，并提醒用户不要在公开 Issue 中发布机密案例。
6. 检查 AI 和产品声明，不暗示没有证据的认证或质量。
7. 检查名称、潜在商标冲突、README、描述和 Badge。
8. 在私有报告中记录发现、修正、剩余风险和信号灯结论；验证最终 Commit 并取得
   所有者明确批准后，才进入单独且经过授权的公开步骤。

## 限制

- 本 Skill 不执行任何公开操作。
- 它不能替代法律咨询或官方商标检索。
- 源码扫描干净不能证明早先的公开副本、Registry 或 Cache 已被删除。
