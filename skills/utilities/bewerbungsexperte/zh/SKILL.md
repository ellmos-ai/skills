---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: 整个求职申请流程的专业工具。分析职位招聘信息，优化个人资料（LinkedIn/简历），并生成定制的求职信。从 SQLite 数据库和文件夹结构生成 ASCII 格式的简历。cv_generator.py 已独立移植——无需 BACH 运行时。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: zh
status: active
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **中文** — `bewerbungsexperte` 官方中文版本。


<img src="banner.png" width="100%" alt="bewerbungsexperte banner">
# BEWERBUNGSEXPERTE v1.1 (中文)

> 您迈向职业生涯下一步的战略伙伴。

## 激活

```bash
# 无需数据库访问的示例简历（中文）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# 从 SQLite 数据库生成简历（中文）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# 将简历保存到文件（中文）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# 附带文件夹扫描（中文）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```

## 服务目录

### 1. 简历生成（`cv_generator.py`）
- **个人信息：** 从 `assistant_user_profile` 表读取（键/值）
- **工作经验：** 扫描雇主文件夹（推荐信/工作证明、合同）
- **教育背景：** 扫描学位文件夹
- **进修培训：** 扫描证书文件夹
- **推荐人：** 来自 `contacts` 表（category='beruflich'）
- **空运行（Dry-Run）：** 无需数据库——用于测试的示例数据

### 2. 职位诊断
- **关键词匹配：** 简历与职位要求的比对（ATS 友好）
- **企业核查：** 研究企业文化和福利待遇

### 3. 申请材料服务
- **简历优化：** 经验的结构化与精炼提炼
- **求职信：** 撰写个性化且具说服力的求职信
- **作品集：** 关于工作样品和推荐人的咨询

## 数据库表（可选）

如果存在，`cv_generator.py` 会从以下表中读取数据：

- `assistant_user_profile` (key TEXT, value TEXT) — 个人数据
  - 字段：name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — 推荐人

缺失的表将被忽略（简历中的相应章节显示为空）。

## 文件夹结构（用于 --career-path 等）

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```

## CLI 选项

```
--db <pfad>           SQLite 数据库路径（无 --dry-run 时必填）
--output, -o          输出文件（默认为 stdout）
--career-path         雇主文件夹路径
--education-path      学位/学历文件夹路径
--certs-path          培训证书文件夹路径
--dry-run             无需数据库访问的示例简历
```

## 工作流程：简历生成

1. **准备工作**
   - 提供 SQLite 数据库（BACH 数据库或自定义数据库）
   - 创建包含文档的文件夹结构（可选）

2. **无数据库测试**
   - `python cv_generator.py --dry-run`——检查工具是否正常工作

3. **生成简历**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - 检查输出并在必要时进行调整

4. **导出简历**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## 依赖项

仅使用 Python 标准库：`sqlite3`、`pathlib`、`argparse`、`re`、`datetime`。
无需 pip 安装，无需导入 BACH 运行时。

## 更新日志

### 1.1.0 (2026-06-22)
- 从 BACH v1.0.0 独立移植
- 使用 `--db <pfad>` 替换硬编码的源数据库路径
- 新增 `--dry-run` 模式
- 移除 `--scan-folders`（需要 BACH 的 user_data_folders 表）
- 中立化页脚文本
- 验证了独立于 BACH 运行时的独立性

### 1.0.0 (2026-01-25，BACH 内部)
- BACH system/agents/_experts/bewerbungsexperte/ 中的初始版本

---
状态：活跃
领域：职业咨询
