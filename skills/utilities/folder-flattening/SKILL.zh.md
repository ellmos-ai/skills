---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 将嵌套的文件夹层级结构重构为扁平、机器可读的布局。基于 Bash 并包含智能合并逻辑。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [folder, flattening, filesystem, bash, reorganization, cleanup]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ordner-flattening.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="folder-flattening banner">

> **中文** — `folder-flattening` 官方中文版本。

# 工作流：Folder Flattening

目标：将嵌套的文件夹结构转换为扁平的、机器可读的结构。
优势：无需再逐层点击目录——通过数据库（`Verzeichnis.db`）进行搜索。
在主题上有意义时允许重复。

---

## 阶段概览

| 阶段 | 说明 | 脚本章节 |
|-------|-------------|----------------|
| 1 | 扁平化（Flatten）：将所有子文件夹拉平至同一层级 | `phase_flatten` |
| 2 | 缩短（Shorten）：将长路径名截断为最后一个片段，存在冲突时进行合并 | `phase_shorten` |
| 3 | 清理：处理多个连续下划线（`___`），移除末尾的 `_` | `phase_cleanup_underscores` |
| 4 | 分组：将数字文件夹、CD 文件夹和短名称文件夹归类到集合文件夹中 | `phase_group_problematic` |
| 5 | 三元组分析：滑动 3 个文件夹一组，取最短名称作为合并目标 | `phase_tripel_merge` |
| 6 | 媒体格式合并：按文件类型整合文件夹（模板） | `phase_media_merge` |
| 7 | 清理：删除空文件夹 | `phase_cleanup_empty` |

---

## 重要规则

### 三元组匹配规则
- **子字符串**：`EducationalBrochures` 中的 `Education` -> 合并至 `Education`
- **复数/元音变音**：`Room` = `Rooms`, `Part` = `Parts`, `Book` = `Books`
- **首个单词**：`Autism ADHD` 匹配 `Autism Career`（前缀相同）

### 最小长度
- 无空格的单词名称：**至少 8 个字符**（防止将 `Hand`、`House`、`Form` 等误合并）
- 包含空格（例如 `ICF Catalog`）：**3 个字符起即可**
- 这允许保留 `ICF`、`ASD Women` 等名称

### 合并后重新开始
每次合并后，文件夹列表将重新加载，并从合并目标位置重新开始。
这样，例如 `Autism` 会在继续之前汇集所有扩展相关内容。

---

## 媒体格式合并（模板系统）

阶段 6 使用模板数组 `MEDIA_TYPES`。每个条目定义：
- 目标文件夹（带有 `_` 前缀）
- 属于该类型的文件扩展名

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Images|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Extensible:
    # "_Spreadsheets|xlsx|xls|csv|ods"
    # "_Presentations|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

仅移动**仅包含**同一种类型文件的文件夹。
包含子文件夹的文件夹将被跳过。

### 添加新媒体类型

只需在 `MEDIA_TYPES` 数组中添加一行新内容：
```bash
"_TargetFolder|ext1|ext2|ext3"
```

---

## 执行

```bash
# Complete run:
cd /path/to/target/directory
bash ordner_flattening_komplett.sh

# Or individual phases:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## 实践数据（会话 2026-01-26）

- 起始：206 个文件夹 + 252 个独立文件，约 5600 个嵌套子文件夹
- 扁平化后：同一层级约 2200 个文件夹
- 缩短与清理后：约 2005 个文件夹
- 分组（数字、CD）后：约 2005 -> 创建了集合文件夹
- 三元组 v1 后：约 1561 个文件夹
- 三元组 v2（8 字符规则）后：进一步减少
- 媒体格式阶段：音频/视频/图片文件夹已整合