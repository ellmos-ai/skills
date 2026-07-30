---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 系统化的 6 阶段调试协议。包含快速检查、隔离测试、20分钟规则和 Bug 报告模板的结构化 Bug 处理方法。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/bugfix-protokoll.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="bugfix-protocol banner">
> **中文** — `bugfix-protocol` 官方中文版本。

# Bugfix Protocol: 系统化 6 阶段调试协议 (中文)

一种结构化的 Bug 处理方法——从症状分析到最终验证。
避免无目的的盲目尝试，确保修复的可持续性。

---

## 概述与目的

| 阶段 | 名称 | 目标 | 最长时间 |
|------|------|------|----------|
| 1 | 快速检查 | 排除明显原因 | 2 分钟 |
| 2 | 诊断 | 定位根本原因 | 10 分钟 |
| 3 | 隔离测试 | 使 Bug 可复现 | 5 分钟 |
| 4 | 修复 (Fix) | 最小化修正 | 10 分钟 |
| 5 | 验证 | 验证修复并检查副作用 | 5 分钟 |
| 6 | 文档化 | 沉淀知识 | 2 分钟 |

**20分钟规则：** 如果 20 分钟后仍无进展，请更换方法或寻求帮助。

---

## 阶段 1: 快速检查 (2 分钟)

在深入调查之前——检查最常见的原因：

### 检查清单

- [ ] **语法错误？** 仔细阅读错误信息，检查对应行
- [ ] **导入错误？** 模块已安装？名称正确？循环导入？
- [ ] **拼写错误？** 变量/函数名称是否正确？
- [ ] **数据类型错误？** 字符串误用为整数？期望对象处为 None？
- [ ] **缓存陈旧？** 删除 `__pycache__`，重启
- [ ] **环境错误？** 激活了正确的 venv？正确的 Python 版本？
- [ ] **编码问题？** UTF-8 与 cp1252（经典 Windows 编码）

### 快速操作

```bash
# 清理缓存 (中文)
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# 检查导入 (中文)
python -c "import modulename"

# 检查语法 (中文)
python -m py_compile file.py
```

---

## 阶段 2: 诊断 (10 分钟)

### 策略：由外而内

1. **分析错误信息** — 从下往上阅读堆栈轨迹 (Traceback)
2. **检查最近的修改** — `git diff`，`git log --oneline -10`
3. **使用诊断工具** — 利用项目特定的诊断工具

### 诊断工具（示例）

根据项目的不同，专用的诊断脚本可能会大有帮助：

| 工具 | 用途 |
|------|------|
| `import_diagnose.py` | 分析导入问题 |
| `method_analyzer.py` | 检查方法签名 |
| `env_checker.py` | 验证环境变量/路径 |

> **注意：** 创建特定于项目的诊断工具或使用现有的工具。
> 重要的是系统化的方法，而不是具体的工具本身。

### 调试技巧

```python
# 1. Print 调试（快速但有效） (中文)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. 断点调试（交互式） (中文)
breakpoint()  # Python 3.7+

# 3. 详细堆栈轨迹 (中文)
import traceback
traceback.print_exc()

# 4. 用 Logging 代替 print (中文)
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## 阶段 3: 隔离测试 (5 分钟)

### 最小可复现示例 (MRE)

目标：用最少的代码复现 Bug。

```python
# test_bug.py — 最小复现测试 (中文)
"""
Bug: [简短描述]
预期: [应该发生什么]
实际: [实际发生了什么]
"""

# 最小化设置 (中文)
# ... 仅保留核心必需代码 (中文)

# Bug 触发代码 (中文)
# ... 触发 Bug 的精确代码 (中文)

# 预期结果 (中文)
# assert result == expected, f"Got {result}" (中文)
```

### 隔离策略

1. **新文件：** 在单独的文件中复现 Bug
2. **移除依赖：** 逐个移除依赖，直到 Bug 消失
3. **二分查找：** 将代码块切半，检查哪一半包含 Bug
4. **Git bisect：** `git bisect start`，`git bisect bad`，`git bisect good <commit>`

---

## 阶段 4: 修复 / Fix (10 分钟)

### 原则

1. **最小化：** 改动尽可能少
2. **深入理解：** 切勿盲目修复 — 彻底理解损坏的原因
3. **单一职责：** 每次提交仅做一项修复，不要同时修复多个问题
4. **向下兼容：** 切勿破坏现有功能

### 修复模式

```python
# 错误做法: 治标不治本 (中文)
try:
    result = broken_function()
except:  # 吞掉所有异常
    result = default_value

# 正确做法: 修复根本原因 (中文)
def broken_function():
    if input_data is None:  # 真正的原因: 缺少 None 检查
        return default_value
    return process(input_data)
```

### 常见修复类别

| 类别 | 典型修复方案 |
|------|--------------|
| None/Null | 守卫语句: `if x is None: return default` |
| 索引错误 | 边界检查: `if i < len(lst)` |
| 类型错误 | 显式转换: `str(x)`, `int(x)` |
| 导入错误 | 修正路径，安装软件包 |
| 编码问题 | 显式指定 UTF-8: `encoding='utf-8'` |
| 竞态条件 | 锁/互斥量，或调整执行顺序 |
| 状态 Bug | 检查初始化，添加重置逻辑 |

---

## 阶段 5: 验证 (5 分钟)

### 检查清单

- [ ] **Bug 已修复：** 原始问题不再发生
- [ ] **MRE 通过：** 隔离测试正常运行通过
- [ ] **无回归：** 现有的测试依然通过
- [ ] **边界情况：** 空输入、None、大数据量已测试
- [ ] **项目工具：** 检查项目工具目录中的相关测试/验证工具

### 测试命令

```bash
# 单元测试 (中文)
python -m pytest tests/ -v

# 仅受影响的测试 (中文)
python -m pytest tests/test_module.py -v -k "test_name"

# 类型检查 (中文)
python -m mypy file.py

# 代码 Lint (中文)
python -m flake8 file.py
```

---

## 阶段 6: 文档化 (2 分钟)

### Bug 报告模板

```markdown
## Bug 报告: [简短标题]

**日期:** YYYY-MM-DD
**严重程度:** 紧急 / 高 / 中 / 低
**组件:** [模块/文件]

### 症状
[用户看到的现象 / 错误信息]

### 根本原因
[技术层面上的根本原因]

### 修复 (Fix)
[修改了什么 + 为什么这样修改]

### 受影响的文件
- `file1.py` — [修改内容]
- `file2.py` — [修改内容]

### 预防措施
[未来如何预防此类 Bug？]
```

### Commit 提交信息格式

```
fix: [修复的简短描述]

Cause: [一句话说明根本原因]
Fix: [修改了什么]
Test: [如何验证的]
```

---

## PyQt6 / GUI 调试 — 常见陷阱

> 本节适用于使用 PyQt6/PySide6 的桌面 GUI 项目。

### PyQt6 5 大陷阱

| 陷阱 | 问题 | 解决方案 |
|------|------|----------|
| **Signal-Slot 断开** | 信号已连接但处理函数未运行 | 在处理函数中 `print`，检查签名 |
| **线程安全** | 从工作线程更新 GUI | 使用 `QMetaObject.invokeMethod` 或信号 |
| **布局级联 (Layout Cascade)** | Widget 隐藏/错位 | `widget.show()`，检查布局层级结构 |
| **事件循环阻塞** | GUI 冻结无响应 | 将耗时操作移至 QThread |
| **垃圾回收 (GC)** | Widget 突然消失 | 将引用保持为 `self.widget` |

### PyQt6 调试辅助函数

```python
# 输出 Widget 树层级结构 (中文)
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# 信号调试 (中文)
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## 快速参考

```
发现 BUG？
     |
     v
[阶段 1: 快速检查] ──────────── 原因显而易见？ -> 修复 (FIX)
     |
     v
[阶段 2: 诊断] ──────────────── 原因明确？ -> 阶段 4
     |
     v
[阶段 3: 隔离测试] ─────────── 可复现？ -> 阶段 4
     |                                |
     |                           无法复现？
     |                                |
     |                           添加日志，
     |                           等待再次发生
     v
[阶段 4: 修复] ──────────────── 最小改动且彻底理解
     |
     v
[阶段 5: 验证] ──────────────── 测试通过（绿）？ -> 阶段 6
     |                                |
     |                           测试失败（红）？ -> 返回阶段 4
     v
[阶段 6: 文档化] ────────────── Bug 报告 + 提交 Commit
```

### 20分钟规则

如果你在 20 分钟后陷入困境：

1. **改变方法** — 尝试不同的调试技术
2. **小黄鸭调试** — 大声解释问题（或写下来）
3. **休息一下** — 离开 5 分钟，带着新鲜的视角重新思考
4. **寻求帮助** — 询问同事、Stack Overflow 或查阅文档
5. **重置** — `git stash`，彻底重新开始