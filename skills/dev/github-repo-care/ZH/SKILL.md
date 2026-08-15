---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: 安全创建、发布、Release、审计和维护 GitHub 仓库的规范协议：检查本地规则与锁文件，在首次 git add 前创建 .gitignore，运行隐私检查，准备 README/i18n/Banner/元数据，验证 release 标签与 GitHub releases，并更新组织 Profile、llms.txt 文件及注册表链接。

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

<img src="banner.png" width="100%" alt="github-repo-care banner">

> **中文** — `github-repo-care` 官方中文版本。


# GitHub Repo Care — 规范发布与维护 GitHub 仓库 (中文)

## 适用场景

当需要创建、发布、Release、审计或维护 GitHub 仓库时使用本 Skill。在首次公开推送 (public push)、Release 标签、仓库元数据、组织 Profile 和隐私检查前尤为重要。

请勿在没有 GitHub 发布步骤的纯代码实现工作中直接使用。请先完成相关的开发或调试工作流，然后再激活本 Skill 进行发布。

## 核心原则

在首次公开推送前准备好仓库。在公开提交历史产生之前，配置好正确的 `.gitignore`、隐私门禁 (privacy gate)、许可证 (license)、README、元数据和 Release 描述，成本要低得多。

## 工作流程与步骤

1. **读取本地规则。** 检查是否存在 `AGENTS.md`、`CLAUDE.md`、`START.md`、Release 策略、命名策略和锁策略。
2. **检查锁文件。** 若 `LOCK.txt` 或匹配的 `LOCK.*.txt` 处于激活状态，请勿编辑该作用域。
3. **确定仓库标识。** 确认名称、组织、可见性、许可证以及一句话的项目宗旨。
4. **在 `git add` 前创建 `.gitignore`。** 排除密钥、本地数据、数据库、构建输出、虚拟环境、缓存、IDE 文件和私有笔记。
5. **添加公共基础文件。** 典型文件：`README.md`、`LICENSE`、`CHANGELOG.md`、`SECURITY.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`llms.txt` 和 CI。
6. **撰写易于发现的 README。** 首屏内容：项目宗旨、安装步骤、使用方法、隐私模型、项目布局、许可证和规范仓库名称。
7. **添加视觉标识。** 当横幅 (banner)、Logo 或截图有助于更容易理解项目时请予以添加。当可以提供真实的产品截图或清晰的概念图时，避免使用通用的装饰性图片。
8. **从一开始妥善规划 i18n。** 最低要求：英语 + 项目语言。面向用户的模块首选标准语言集：德语、英语、西班牙语、简体中文、日语和俄语。
9. **运行测试和冒烟测试 (smokes)。** 在宣称成功或创建 Release 前在本地进行验证。
10. **运行隐私门禁检查。** 检查暂存/追踪的文件集 (staged/tracked)，确保无密钥、本地路径、个人隐私信息 (PII)、`.env`、数据库、私有文档、生成的产物和乱码 (mojibake)。
11. **提交并推送。** 仅在通过门禁检查后才进行 Commit。然后创建或关联 GitHub 仓库、Push 并验证远程状态。
12. **设置元数据。** 检查 description、topics、homepage、visibility 和默认分支。
13. **创建 Release。** 创建 Tag 和 GitHub release；验证分支与 Tag 的 CI 状态。
14. **更新入口与检索表面。** 从组织 Profile、`llms.txt`、中央注册表、本地模块索引和生态 README 中添加链接。
15. **最终验证。** 检查远程 README、Release 页面、Topics、CI 和链接。

## 隐私门禁 (Privacy Gate)

检索暂存或已追踪的文件集，而不仅仅是可见的工作区树。

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

对于公开模块，还需记录 `RELEASE_GATE.md` 或同等的门禁文档：日期、已检查的命令、结果、剩余警告和有意保留的例外。如果曾经提交过密钥，仅从 `HEAD` 删除是不够的；必须轮换 (rotate) 该密钥。

## GitHub 元数据

推送之后，显式设置元数据与 Release 数据。

```bash
gh repo edit ORG/REPO --description "Short concrete description" \
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

如果 Release 后 CI 报错 (显示红色)，说明仓库尚未规范发布。对于刚创建的初始 Release，立即且有针对性地将新 Tag 移动到修正后的 Commit 是可以接受的。

## 常见错误

| 错误 | 修复方案 |
|---|---|
| 在 `git add` 之后才添加 `.gitignore` | 先取消暂存 (unstage)，修复忽略规则，然后重新 add |
| 界面或 Skill 为多语言，但 README 仅有单一语言 | 添加语言链接或多语言本地化 README |
| 缺少 Banner、Topics 或 Description | 在对外发布前补充入口与展示资产 |
| 存在 Release tag，但 CI 报错 (显示红色) | 修复 CI 并验证新的运行结果 |
| 更新了组织 README，但遗漏了 `llms.txt` | 同时更新人类可读与机器可读的展示表面 |
| 公开文档中出现了本地路径 | 替换为相对路径或通用示例 |
| 公开仓库中包含测试数据库或 Notebook 收件箱 (inbox) | 将其从版本追踪中移除，添加忽略规则，重新运行门禁检查 |

## 最终检查清单

- [ ] 已检查本地规则与锁文件。
- [ ] 首次 add 前已存在 `.gitignore`。
- [ ] 已提供公共文档、LICENSE、SECURITY、CONTRIBUTING、CHANGELOG 和 `llms.txt`。
- [ ] README 包含仓库名称、项目宗旨、安装步骤、使用方法、隐私说明及许可证。
- [ ] 满足 i18n 预期。
- [ ] 在有用时提供了 Banner、Logo 或截图。
- [ ] 测试与冒烟测试通过。
- [ ] 隐私、路径、密钥、数据库及乱码扫描干净。
- [ ] GitHub Description、Topics、Tag、Release 及 CI 已验证。
- [ ] 组织 Profile、注册表及生态系统链接已更新。

## 变更日志

### 1.0.0 (2026-06-18)
- 创建初始仓库维护与发布规范协议。
