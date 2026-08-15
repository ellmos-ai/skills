---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 系统的 6 阶段 Core Debugging 协议。结构化 Bug 处理流程，包含快速检查、隔离测试、20分钟规则和 Bug 报告模板。

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


# Bugfix Protocol: 系统的 6 阶段 Debugging 协议

结构化的 Bug 处理方法 — 从症状分析到验证。
防止盲目的试错，确保修复方案可持续。

---

## 概述与目的

| 阶段 | 名称 | 目标 | 最长时间 |
|------|------|------|----------|
| 1 | 快速检查 | 排除明显原因 | 2 分钟 |
| 2 | 诊断 | 定位根本原因 | 10 分钟 |
| 3 | 隔离测试 | 使 Bug 可复现 | 5 分钟 |
| 4 | 修复 | 最小化修正 | 10 分钟 |
| 5 | 验证 | 验证修复 + 检查副作用 | 5 分钟 |
| 6 | 文档编写 | 保存知识经验 | 2 分钟 |

**20分钟规则：** 如果 20 分钟后仍无进展，请改变方法或寻求帮助。

---

## 阶段 1: 快速检查 (2 分钟)

在深入分析之前 — 检查最常见的原因：

### 检查清单

- [ ] **语法错误？** 仔细阅读错误信息，检查对应行
- [ ] **导入错误？** 模块已安装？名称正确？循环导入？
- [ ] **拼写错误？** 变量/函数名称是否正确？
- [ ] **数据类型错误？** 字符串误作为整型？本应为对象的地方为 None？
- [ ] **缓存过期？** 删除 `__pycache__`，重新启动
- [ ] **环境错误？** 是否激活了正确的 venv？Python 版本是否正确？
- [ ] **编码问题？** UTF-8 vs. cp1252 (Windows 经典)

### 快速操作

```bash
# 清除缓存
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# 检查导入
python -c "import modulename"

# 检查语法
python -m py_compile file.py
```

---

## 阶段 2: 诊断 (10 分钟)

### 策略：由外入内 (Outside-In)

1. **分析错误信息** — 从下往上阅读堆栈追踪 (traceback)
2. **检查最近的修改** — `git diff`, `git log --oneline -10`
3. **使用诊断工具** — 使用项目专属的诊断工具

### 诊断工具 (示例)

根据项目的不同，专用的诊断脚本可能会大有帮助：

| 工具 | 用途 |
|------|------|
| `import_diagnose.py` | 分析导入问题 |
| `method_analyzer.py` | 检查方法签名 |
| `env_checker.py` | 验证环境变量/路径 |

> **注意：** 创建项目专属的诊断工具或使用现有的工具。
> 重要的是系统性的方法，而不是具体的工具。

### 调试技巧

```python
# 1. Print 调试 (简单但高效)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. 断点 (交互式)
breakpoint()  # Python 3.7+

# 3. 详细堆栈追踪
import traceback
traceback.print_exc()

# 4. 使用日志替代 print
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
# test_bug.py — 最小复现测试
"""
Bug: [简短描述]
Expected: [预期发生的结果]
Actual: [实际发生的结果]
"""

# 最小化设置
# ... 仅保留核心必要代码

# Bug 触发器
# ... 触发 Bug 的精确代码

# 预期结果
# assert result == expected, f"Got {result}"
```

### 隔离策略

1. **新文件：** 在独立文件中复现 Bug
2. **移除依赖：** 逐个移除依赖，直到 Bug 消失
3. **二分查找：** 将代码块切半，检查哪一半包含 Bug
4. **Git bisect：** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## 阶段 4: 修复 (10 分钟)

### 原则

1. **最小化：** 改动越少越好
2. **彻底理解：** 绝不盲目修复 — 必须理解为什么会发生故障
3. **单件事：** 每个 commit 仅包含一个修复，不要同时修复多个问题
4. **向下兼容：** 切勿破坏原有功能

### 修复模式

```python
# 错误做法：仅处理表面症状
try:
    result = broken_function()
except:  # 吞掉所有异常
    result = default_value

# 正确做法：修复根本原因
def broken_function():
    if input_data is None:  # 真正原因：缺少 None 检查
        return default_value
    return process(input_data)
```

### 常见修复类别

| 类别 | 典型修复方案 |
|------|--------------|
| None/Null | 卫语句：`if x is None: return default` |
| 索引错误 | 边界检查：`if i < len(lst)` |
| 类型错误 | 显式转换：`str(x)`, `int(x)` |
| 导入错误 | 修复路径，安装包 |
| 编码问题 | 显式指定 UTF-8：`encoding='utf-8'` |
| 竞态条件 | 锁/互斥锁，或调整顺序 |
| 状态 Bug | 检查初始化，添加重置机制 |

---

## 阶段 5: 验证 (5 分钟)

### 检查清单

- [ ] **Bug 已修复：** 原始问题不再发生
- [ ] **MRE 通过：** 隔离测试顺利运行通过
- [ ] **无回归错误：** 现有测试依然保持通过
- [ ] **边界情况：** 已测试空输入、None、大数据量情况
- [ ] **项目工具：** 检查项目工具目录中的相关测试/验证工具

### 测试命令

```bash
# 单元测试
python -m pytest tests/ -v

# 仅受影响的测试
python -m pytest tests/test_module.py -v -k "test_name"

# 类型检查
python -m mypy file.py

# Lint 检查
python -m flake8 file.py
```

---

## 阶段 6: 文档编写 (2 分钟)

### Bug 报告模板

```markdown
## Bug Report: [简短标题]

**Date:** YYYY-MM-DD
**Severity:** critical / high / medium / low
**Component:** [模块/文件]

### Symptom
[用户看到的现象 / 错误信息]

### Root Cause
[技术层面的根本原因]

### Fix
[修改了什么 + 为什么这样修改]

### Affected Files
- `file1.py` — [修改说明]
- `file2.py` — [修改说明]

### Prevention
[将来如何防止此类 Bug 再次发生？]
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

### PyQt6 5 大常见陷阱

| 陷阱 | 问题 | 解决方案 |
|------|------|----------|
| **Signal-Slot 断开** | 信号已连接但处理函数未运行 | 在处理函数中加 `print`，检查签名 |
| **线程安全** | 从工作线程更新 GUI | 使用 `QMetaObject.invokeMethod` 或信号 |
| **布局层叠** | 控件不可见/位置错乱 | `widget.show()`，检查布局层级 |
| **事件循环阻塞** | GUI 界面冻结 | 将耗时操作移至 QThread |
| **垃圾回收** | 控件突然消失 | 将引用保存为 `self.widget` |

### PyQt6 调试辅助函数

```python
# 打印控件层级树
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# 信号调试
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
[阶段 1: 快速检查]  ────── 明显原因？ -> 修复
     |
     v
[阶段 2: 诊断]  ────────── 原因明确？ -> 阶段 4
     |
     v
[阶段 3: 隔离测试]  ────── 可复现？ -> 阶段 4
     |                          |
     |                     不可复现？
     |                          |
     |                     添加日志，
     |                     等待再次发生
     v
[阶段 4: 修复]  ─────────── 最小化 + 已理解
     |
     v
[阶段 5: 验证]  ────────── 测试通过？ -> 阶段 6
     |                          |
     |                     测试失败？ -> 返回阶段 4
     v
[阶段 6: 文档编写]  ────── Bug 报告 + commit
```

### 20分钟规则

如果你在 20 分钟后陷入困境：

1. **改变方法** — 尝试不同的调试技巧
2. **小黄鸭调试** — 大声解释问题（或写下来）
3. **休息一下** — 离开 5 分钟，带上清醒的头脑重新开始
4. **寻求帮助** — 询问同事、查阅 Stack Overflow 或官方文档
5. **重置** — `git stash`，完全重新开始
