---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: 本地私密记录医疗数据：诊断、症状历史和检查计划。无 BACH 来源 — 采用具有独立 SQLite 存储的自定义设计。严格局限于本地，无云端传输。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: zh
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
---

<img src="banner.png" width="100%" alt="medizin-daten banner">

> **中文** — `medizin-daten` 官方中文版本。


## 概述与目的

安全、本地化地记录个人医疗数据：诊断（ICD-10 代码可选）、带日期序列的症状历史和检查计划。所有数据完全保存在本地 `medizin-daten/store.db` 中。

本 Skill 不能替代医疗咨询，也不提供任何医疗诊断或陈述 — 它只是一个用于记录个人健康数据的结构化笔记本。

---

## 触发词 (Triggers)

| 短语 | 操作 |
|---|---|
| "Record a diagnosis" / "记录诊断" | 创建新诊断 |
| "Add diagnosis [name]" / "添加诊断 [名称]" | 创建具名诊断 |
| "Symptom history" / "症状历史" | 记录今天的症状 |
| "Record symptom [name]" / "记录症状 [名称]" | 记录单个症状 |
| "Examination plan" / "检查计划" | 显示即将进行的预约/检查 |
| "Add appointment" / "添加预约" | 输入检查预约 |
| "Show my diagnoses" / "显示我的诊断" | 输出诊断列表 |

---

## 工作流程与步骤

1. **检测模式**：诊断 / 症状 / 检查计划
2. **结构化输入**：日期、名称、备注、可选的 ICD-10 代码
3. **保存**：存入 `store.db`（本地，无网络访问）
4. **输出**：适用于 LLM 上下文的可读摘要

---

## CLI 入口点

```bash
# Create diagnosis (Deutsch)
python medizin_daten_core.py add-diagnosis "Hypertension" [--icd I10] [--note "note"]

# List diagnoses (Deutsch)
python medizin_daten_core.py diagnoses

# Record symptom (Deutsch)
python medizin_daten_core.py add-symptom "Headache" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptom history for a name (Deutsch)
python medizin_daten_core.py symptom-history "Headache" [--limit 30]

# Plan examination (Deutsch)
python medizin_daten_core.py add-exam "Blood count" [--date 2026-07-01] [--note "fasting"]

# Upcoming examinations (Deutsch)
python medizin_daten_core.py exams [--upcoming]

# Alternative store (e.g. for tests) (Deutsch)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## 存储 (Store)

| 属性 | 值 |
|---|---|
| 类型 | SQLite |
| 路径（默认） | `skills/assist/medizin-daten/store.db` |
| 覆盖方式 | `--store <path>` 或环境变量 `MEDIZIN_STORE` |
| 数据表 | `diagnoses`, `symptoms`, `examination_plans` |

### 模式 (Schema)

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (short: 8 hex)
    name        TEXT NOT NULL,        -- name (e.g. "Hypertension")
    icd_code    TEXT,                 -- ICD-10 code optional (e.g. "I10")
    onset_date  TEXT,                 -- onset (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- free-text note
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    name         TEXT NOT NULL,       -- name (e.g. "Headache")
    severity     INTEGER,             -- 1–10 scale (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 timestamp
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    exam_name    TEXT NOT NULL,       -- examination name
    planned_date TEXT,                -- planned date (ISO-8601)
    done_date    TEXT,                -- completed on (NULL = pending)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## 原则与原则态度

- 本 Skill 不提供医疗建议，也不进行诊断。
- ICD-10 代码作为自由文本存储 — 不对外部数据库进行验证。
- 1–10 级的严重程度评级由用户主观决定。
- 始终允许缺失值（日期、严重程度） — 遵循笔记本原则。

---

## 隐私（隐私门界）

> **警告：医疗数据尤为敏感。**

- `store.db` 包含高度敏感的健康数据 — **切勿提交到 Git**。
- **无网络访问** — 所有操作完全在本地运行。
- **不与外部服务共享**，不与云端后端同步。
- 备份建议：加密的本地备份（例如 `age`/`gpg`）。
- 启动时，Skill 会检查 `store.db` 是否处于本地文件系统之外，如果路径位于同步文件夹（OneDrive 等）中，则发出警告。
- `~/.gitignore_global` 或本地 `.gitignore` 应排除 `store.db`。

---

## 相关资源

- Skill `assist/gesundheit` — 一般健康助手（非医疗数据）
- MediPlaner（`tools/module-installer` → `mediplaner`） — 药物管理（独立程序）

---

## 变更日志

| 版本 | 日期 | 变更 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初次创建 — 自定义设计，隐私门界，3 表架构 |