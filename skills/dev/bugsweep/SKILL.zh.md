---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: 系统化 Bug 排查协议，具备随代码库规模缩放的目标值、翻倍升级机制、区域追踪和最终验证。适用于 /bugsweep 或用户要求进行系统化 Bug 排查时。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="bugsweep banner">
> **中文** — `bugsweep` 官方中文版本。

# /bugsweep — 系统化 Bug 排查工作流 (中文)

具有收敛停止标准的迭代 Bug 寻找机制。随代码规模自适应缩放，当排查看起来流于形式时触发升级，并通过区域追踪防止重复检查。

## 1. 计算基准率 (Base rate)

```
LOC = 生产性源代码行数 (src/, lib/ — 不包括测试、配置、文档和生成的代码)
x = max(1, ceil(LOC / 1500))
base_rate = x * 3
```

| LOC | x | 基准率 (Base rate) |
|-----|---|-------------------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

向用户报告：“代码库：{LOC} LOC → 基准率 = {base_rate} 次干净搜索轮次。”

## 2. 搜索循环 (Search loop)

```
counter = 0
target = base_rate
any_bug_found = False
checked = []  # (area_name, type: code|task)

LOOP:
  area = pick_new_area()  # 参见区域规则
  checked.append(area)

  执行彻底的 Bug 搜索

  如果 发现 Bug:
    any_bug_found = True
    遵循 bugfix-protocol 修复 (阶段 4+5)
    审查: 参见模型规则（较新模型类: 无需外部审查）
    Commit + push
    counter = 0  # 重置 (RESET)
  否则:
    counter += 1
    报告: "✓ 无 Bug: {area} — {counter}/{target}"

  如果 counter >= target:
    如果 未发现任何 Bug (NOT any_bug_found):
      # 翻倍升级: 连一个 Bug 都没发现 → 搜索太浅？
      target = base_rate * 2
      any_bug_found = True  # 仅升级一次
      报告: "⚠ {base_rate} 轮搜索中未发现 Bug → 目标翻倍至 {target}。"
      继续循环 (CONTINUE LOOP)
    否则:
      跳转至 最终验证 (GOTO final verification)
```

### 搜索循环的实战心得（得自实际排查）

- **非 Git 仓库：** 在没有 `git` 的地方（例如云同步的项目文件夹），用 **版本化备份** 替代“commit + push”：在第一次修复前创建 `file_<ts>.bak`。**注意 — 修复前的备份不是您工作的备份：** 在最后一次修复后，请另存一份新的 `_FINAL_` 备份，否则同步抖动可能会抹掉整个修复会话。
- **预先已知多个 Bug：** 如果在开始时已知 N 个 Bug（例如来自之前的运行），“每个 Bug：修复 → 审查 → 提交 → 重置”是不切实际的。将已知 Bug 作为 **一个** 修复块统一处理（最后集中审查），并从发现的 **第一个新 Bug** 开始计算基准率/搜索循环。重置逻辑依然适用于扫雷过程中新发现的 Bug。
- **多处存在同一 Bug：** 发现的某个缺陷（如错误的正则表达式、破损的格式假设）通常会被复制到其他地方。每次修复后，在其他位置搜索相同的模式——这是一个非常有价值的专用“区域”。

## 3. 区域规则（防止投机）

“区域”(Area) 可以是 **代码焦点** 或 **任务**（代码的目的）。

### 代码焦点 (Code focus)
- 可以在轮次之间 **扩展**（更多文件）或 **转移**（不同部分）
- **绝不能** 与之前轮次的选择完全相同
- OK: 第 1 轮 = `maintenance.py`，第 5 轮 = `maintenance.py + orchestrator.py`（扩展）
- NOT OK: 第 1 轮 = `maintenance.py`，第 5 轮 = `maintenance.py`（完全相同）

### 任务 (Task/Purpose)
- 可以变得 **更细粒度**（检查子函数）或 **更广泛**（将相关函数放在一起）
- **绝不能** 是完全相同的任务
- OK: 第 1 轮 = "看门狗中的线程安全"，第 5 轮 = "整个托盘的线程安全"（更广泛）
- OK: 第 1 轮 = "进程检测"，第 5 轮 = "进程检测内部的商店标记匹配"（更细粒度）
- NOT OK: 第 1 轮 = "看门狗中的线程安全"，第 5 轮 = "看门狗中的线程安全"（完全相同）

### 命名规则
- 区域 **必须** 在搜索前命名（不能事后指定）
- 格式：`"{name}" ({type}: code|task)`

## 4. 最终验证 (Final verification)

一旦 counter >= target 并且 any_bug_found 为 True：

**步骤 A — bugfix-protocol 阶段 5：**
- [ ] 完整测试套件通过（绿）(`pytest`)
- [ ] **至少实际执行一次修改后的执行路径** — 不仅仅是运行测试。对从不调用修改位置的代码运行绿色单元测试是假的安全。运行实际修改的路径（dry run、冒烟测试、CLI 调用）并检查是否有 traceback / 签名 / 命名错误。`py_compile` 或纯 import 仅检查语法——并不检查路径是否能正常运行。
- [ ] **每个修复都至少有一个测试覆盖到它** — 没有实际触发修改分支测试的修复被视为未验证（对于编排/网络路径，必要时结合 mock + dry run）。
- [ ] 类型检查（如果已配置）
- [ ] Lint 检查（如果已配置）
- [ ] 已检查本会话修复的边界情况

**步骤 B — 审查（模型规则）：**
- **较新模型类（如 Claude 5 / Fable 类）：** **不需要** 外部 Advisor/第二模型审查。步骤 A（测试 + 实际冒烟运行）即为验证。在存在真正不确定性时，可选使用新的审查子 Agent——但在将其计入 Bug 之前，请通过实证验证其发现（针对未修改的代码进行测试）。
  背景（2026-06-11 扫雷经验）：第二审查员不可用，替代子 Agent 提供了 1 个发现（置信度 85），但测试证明其并非 Bug——外部审查并未改变最终结果。
- **较旧模型：** 与 Advisor 进行总结讨论（退路：第二模型作为审查员）；Advisor 确认或指出遗漏。

**如果在验证期间发现 Bug：**
→ 修复 + 测试 + 提交
→ 重置：counter = 0, target = base_rate（全新的基准率，**不** 翻倍）
→ 返回搜索循环（已检查列表保留，any_bug_found = True）

**如果验证结果干净：**
→ 完成。Commit + push。输出协议总结。

## 5. 总结协议（结尾输出）

```markdown
## Bug Sweep 结果

- **代码库：** {LOC} LOC
- **基准率：** {base_rate}（升级后目标：{target}）
- **已检查区域数：** {len(checked)}
- **发现 Bug 数：** {count}
- **重置次数：** {reset_count}
- **是否触发翻倍：** 是/否
- **修复列表：**
  - {title} — {commit_hash}
  - ...
- **最终测试套件：** {passed}/{total} 通过
- **审查结论：** 自行验证（较新模型类） / Advisor 已确认 / 指出遗漏
```

## 何时使用此工作流

- 特性开发完成后（质量保证）
- 发布之前（验收排查）
- 定期的代码卫生检查
- 当用户输入 `/bugsweep` 时

## 与其他 Skill 的交互

- **bugfix-protocol：** 针对找到的每个 Bug 执行修复流程（阶段 4+5）
- **systematic-debugging：** 用于排查中难以复现的 Bug
- **code-review：** 可以作为任务区域使用

---

## 变更日志

### 1.1.0 (2026-06-13)
- 移植了步骤 B 的模型规则（自本地 Skill 安装，状态 2026-06-11）：较新模型类通过测试 + 实际冒烟运行进行自我验证，无需外部审查；协议字段“审查结论”做相应扩展。

### 1.0.0 (2026-06-13)
- 首次发布于 Skill 库（采纳自本地 Skill 安装，状态 2026-06-01）。