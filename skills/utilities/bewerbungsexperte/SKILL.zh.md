---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: 整个求职申请过程的专家。分析招聘广告，优化个人资料（LinkedIn/简历），并生成定制的求职信。从 SQLite 数据库和文件夹结构生成 ASCII 简历。cv_generator.py 已独立移植——无需 BACH 运行时。
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

<img src="banner.png" width="100%" alt="bewerbungsexperte banner">

> **中文** — `bewerbungsexperte` 官方中文版本。


# BEWERBUNGSEXPERTE v1.1 (中文)

> 您迈向职业生涯下一步的战略伙伴。

## 激活

```bash
# 无需数据库访问的示例简历 (中文)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# 从 SQLite 数据库生成简历 (中文)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <path/to/data.db>

# 将简历保存到文件 (中文)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <path> --output lebenslauf.txt

# 配合文件夹扫描使用 (中文)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <path> --career-path <folder>
```

## 服务目录

### 1. 简历生成 (`cv_generator.py`)
- **个人数据：** 从 `assistant_user_profile` 表中读取（键/值）
- **工作经验：** 扫描雇主文件夹（工作证明、合同）
- **教育背景：** 扫描学位证书文件夹
- **进修培训：** 扫描职业资格证书文件夹
- **推荐人：** 从 `contacts` 表中读取（category='beruflich'）
- **试运行（Dry-Run）：** 无需数据库——提供用于测试的示例数据

### 2. 岗位诊断
- **关键词匹配：** 对比简历与职位要求（ATS 安全）
- **企业调查：** 调研公司文化与福利待遇

### 3. 申请材料服务
- **简历精修：** 经验结构化与亮点突出
- **求职信编写：** 撰写个性化且具说服力的求职信
- **作品集指导：** 关于工作样品和推荐人的咨询

## 数据库表（可选）

`cv_generator.py` 会从以下表中读取数据（如果存在）：

- `assistant_user_profile` (key TEXT, value TEXT) — 个人数据
  - 字段: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — 推荐人

缺失的表将被忽略（简历中对应章节显示为空白）。

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
--db <路径>           SQLite 数据库路径（不用 --dry-run 时必填）
--output, -o          输出文件（默认为 stdout）
--career-path         雇主文件夹路径
--education-path      学位证书文件夹路径
--certs-path          职业资格证书文件夹路径
--dry-run             不访问数据库生成示例简历
```

## 工作流程：简历生成

1. **准备工作**
   - 提供 SQLite 数据库（BACH 数据库或自定义数据库）
   - 创建包含文档的文件夹结构（可选）

2. **无数据库测试**
   - `python cv_generator.py --dry-run` -- 检查工具是否正常运行

3. **生成**
   - `python cv_generator.py --db <路径> --career-path <雇主文件夹>`
   - 检查输出并根据需要调整

4. **导出**
   - `python cv_generator.py --db <路径> --output lebenslauf.txt`

## 依赖项

仅限 Python 标准库：`sqlite3`、`pathlib`、`argparse`、`re`、`datetime`。
无需 pip 安装，无需导入 BACH 运行时。

## 变更日志

### 1.1.0 (2026-06-22)
- 从 BACH v1.0.0 独立移植
- 使用 `--db <路径>` 替代硬编码的原数据库路径
- 添加了 `--dry-run` 模式
- 移除了 `--scan-folders`（该选项需要 BACH 的 user_data_folders 表）
- 中立化页脚文本
- 验证了独立于 BACH 运行时的完整性

### 1.0.0 (2026-01-25, BACH 内部版)
- 在 BACH system/agents/_experts/bewerbungsexperte/ 中发布的初始版本

---
状态：活跃
领域：职业咨询