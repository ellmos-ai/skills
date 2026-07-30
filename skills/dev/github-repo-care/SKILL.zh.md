---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: 安全创建、发布、发行、审计和维护 GitHub 仓库的协议：检查本地规则和锁、在第一次 git add 之前创建 .gitignore、执行隐私检查、准备 README/i18n/Banner/元数据、验证发布标签与 GitHub Releases，并更新组织主页、llms.txt 文件和注册表链接。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: zh
status: active
dependencies: {'tools': ['git', 'gh', 'rg'], 'services': ['GitHub'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.codex/skills/github-repo-care/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': '2026-06-18', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `github-repo-care` 官方中文版本。


# GitHub Repo Care — 规范发布与维护仓库 (中文)

## 何时使用

当需要创建、发布、发行、审计或维护 GitHub 仓库时使用此 Skill。在首次公开推送、发布 Tag 标签、仓库元数据、组织主页以及隐私检查之前尤为重要。

请勿在没有 GitHub 发布步骤的纯实现开发中使用它。请先完成相关的开发或调试工作流，然后再激活此 Skill 进行发布。

## 核心规则

在首次公开推送之前准备好仓库。在公开提交历史产生之前，配置好正确的 `.gitignore`、隐私关口、许可证、README、元数据和版本发布说明的成本要低得多。

## 工作流与步骤

1. **阅读本地规则。** 检查是否存在 `AGENTS.md`、`CLAUDE.md`、`START.md`、发布策略、命名策略和锁策略。
2. **检查锁定状态。** 如果 `LOCK.txt` 或匹配的 `LOCK.*.txt` 处于激活状态，请勿修改该作用域。
3. **确定仓库身份。** 确认名称、组织、可见性、许可证和一句话项目目的。
4. **在 `git add` 之前创建 `.gitignore`。** 排除密钥、本地数据、数据库、构建输出、虚拟环境、缓存、IDE 文件和私有笔记。
5. **添加公共基础文件。** 典型文件：`README.md`、`LICENSE`、`CHANGELOG.md`、`SECURITY.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`llms.txt` 和 CI 配置文件。
6. **编写易于发现的 README。** 首屏展示：项目目的、安装方式、使用说明、隐私模型、项目结构、许可证和标准仓库名称。
7. **添加视觉标识。** 当 Banner、Logo 或截图有助于更容易理解项目时添加它们。在可以展示真实产品截图或清晰概念图时，避免使用通用的装饰性图片。
8. **精心地规划国际化 i18n。** 最低要求：英语加项目主语言。面向用户的模块的首选标准语言集：德语、英语、西班牙语、简体中文、日语和俄语。
9. **运行测试和冒烟测试。** 在声明成功或创建发布之前，在本地进行验证。
10. **运行隐私关口检查。** 检查暂存/追踪的文件集，排查密钥、本地路径、个人身份信息 (PII)、`.env`、数据库、私有文档、生成的产物和乱码 (mojibake)。
11. **提交并推送。** 仅在隐私关口检查通过后才进行 Commit 提交。然后创建或关联 GitHub 仓库，执行 Push 推送，并验证远端状态。
12. **设置元数据。** 检查描述 (description)、主题标签 (topics)、主页 (homepage)、可见性 (visibility) 和默认分支 (default branch)。
13. **创建 Release 发布。** 创建 Tag 标签和 GitHub Release；验证分支和 Tag 的 CI 状态。
14. **更新入口与展示面。** 从组织主页、`llms.txt`、中央注册表、本地模块索引以及生态系统 README 中进行链接关联。
15. **最终验证。** 检查远端 README、Release 页面、Topics 标签、CI 状态和链接。

## 隐私关口 (Privacy Gate)

排查已暂存 (staged) 或已追踪 (tracked) 的文件集，而不仅仅是可见的工作树。

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

对于公开模块，还需要记录 `RELEASE_GATE.md` 或同等检查文档：日期、检查过的命令、结果、剩余警告以及有意的例外情况。如果密钥曾被提交过，仅从 `HEAD` 中删除是不够的；必须轮换废弃该密钥。

## GitHub 元数据

在推送之后，显式设置元数据和 Release 数据。

```bash
gh repo edit ORG/REPO --description "简短具体的描述" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

然后进行验证：

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

如果 Release 发布后 CI 标红，说明仓库尚未规范发布完成。对于刚创建的初始 Release，立即故意将新 Tag 移动到修正后的 Commit 提交上是可以接受的。

## 常见错误

| 错误 | 纠正方法 |
|---|---|
| 在 `git add` 之后才添加 `.gitignore` | 先取消暂存，修复忽略规则，然后再重新添加 |
| 虽然 UI 或 Skill 是多语言的，但 README 只有单语言 | 添加语言切换链接或多语言本地化 README |
| 缺少 Banner、Topics 标签或 Description 描述 | 在对外发布宣传前补全这些展示要素 |
| Release Tag 已存在，但 CI 标红 | 修复 CI 并验证新的运行流程 |
| 更新了组织 README，但遗漏了 `llms.txt` | 同时更新面向人类与面向机器的展示面 |
| 本地绝对路径出现在公开文档中 | 替换为相对路径或通用示例 |
| 公开仓库中包含测试数据库或 Notebook 收件箱文件夹 | 从 Git 追踪中移除，添加忽略规则，重新运行隐私关口检查 |

## 最终检查清单

- [ ] 已检查本地规则和锁状态。
- [ ] 在第一次 add 之前已有 `.gitignore`。
- [ ] 公开文档、许可证、安全策略、贡献指南、变更日志和 `llms.txt` 健全。
- [ ] README 包含仓库名称、项目目的、安装方式、使用说明、隐私策略和许可证。
- [ ] 满足 i18n 预期。
- [ ] 在有帮助时展示了 Banner、Logo 或截图。
- [ ] 测试和冒烟测试通过。
- [ ] 隐私、路径、密钥、数据库和乱码扫描干净。
- [ ] GitHub 描述、Topics 标签、Tag 标签、Release 和 CI 验证通过。
- [ ] 组织主页、注册表和生态系统链接已更新。

## 变更日志

### 1.0.0 (2026-06-18)
- 创建了初始仓库维护与发布协议。