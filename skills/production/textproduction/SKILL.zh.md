---
language: zh
---

> **中文** — `textproduction` 官方中文版本。


# Textproduction — Router (中文)

本 Skill 涵盖所有文本创作形式。它会重定向至相应的
子 Skill — 请参阅子文件夹中的详细说明。

## 路由表

| 子 Skill | 触发示例 | 详细说明 |
|---|---|---|
| **text** | “写一篇博客文章”、“5 条 LinkedIn 动态”、“新闻通讯”、“产品描述”、“正式电子邮件”、“总结 X” | `text/WORKFLOW.md` |
| **storys** | “写剧本”、“短篇小说”、“创建 RPG 冒险”、“角色卡”、“世界观构建” | `storys/WORKFLOW.md` |
| **pr** | “撰写新闻稿”、“立场文件”、“公关包”、“生成 PDF” | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## 工作流与步骤

```
1. 用户需求 → 上方路由表 → 确定匹配的子 Skill。
2. 阅读子文件夹中的详细说明 (WORKFLOW.md)。
3. 选择 Prompt 模板，填写占位符，生成文本。
4. 质量检查（在各子 Skill 中注明）。
```

## 注意事项

- **用户中立：** Skill 中不包含个人数据、API 密钥或账户信息。
  配置（语气风格、字符限制、公关联系信息）由用户自行决定。
- **PR 工具：** `pr/press_compiler.py` 可通过 LaTeX (pdflatex/xelatex)
  将新闻稿和立场文件编译为 PDF。一次性设置：将 `pr/config.example.json`
  复制为 `pr/config.json` 并填写联系信息。
- 可选样式优化：DeepL Write（每月免费最多 500,000 字符）。

## 变更日志

### 2.0.0 (2026-06-22)
- 重构为路由模式：SKILL.md = 入口 + 路由表。
- 三个子 Skill：text/（6 种文本类型）、storys/（4 种叙事格式）、
  pr/（新闻稿 + 立场文件 + LaTeX PDF 编译器）。
- 将 press_compiler.py + LaTeX 模板 + config.example.json 从
  ai-media-editor/production/pr/ 移动至此处 (SSOT)。
- 更新相关 Skill 引用为内部子 Skill 路径。

### 1.0.0 (2026-06-22)
- 初始版本。从 ai-media-editor/production/text/WORKFLOW.md 拆分出来。
- 来源 provenance: BACH agents/_experts/textproduction/ (MIT)。