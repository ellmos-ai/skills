---
name: speicherbereinigung
version: 1.0.0
type: skill
author: Lukas Geiger und OpenAI Codex
created: 2026-08-04
updated: 2026-08-05
description: "基于证据的 Windows 存储空间清理，具备受控的紧急模式、物理占用测量、进程与产生源取证，以及针对反复占满存储的可逆措施。"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: utilities
tags: [windows, storage, cleanup, forensics, onedrive, pagefile, logs]
language: zh
status: active
visibility: public
dependencies:
  tools: [powershell]
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: "~/.codex/skills/speicherbereinigung"
  origin_version: null
  origin_repo: null
  last_sync_from_origin: 2026-08-05
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6d44ad70bc2f7abc4086474c001d33a6727d9bb6f9793333d804ad3af4907661
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="speicherbereinigung banner">

# 存储空间清理

## 目的与结果

本技能在 Windows 上有控制地回收存储空间，并防止同一填充路径在短时间内再次占满磁盘。它分为三个阶段：紧急释放、根因取证和长期限制。

每一次变更都遵循同一协议：

`Fund -> Entscheidung -> begrenzte Ausführung -> Readback -> Messung`

若用户未指定更高目标，则只有在最后一次变更后系统卷再次报告至少 50 GB 可用空间，任务才视为完成。最初的紧急阈值额外 10 GB 仅结束当前的紧急状态，不结束整体任务。

## 何时启用

在以下情况使用本技能：

- 系统磁盘空间不足或反复出现空间丢失；
- 日志、缓存、页面文件、归档、构建产物异常庞大；
- 出现重复克隆、备份代次或本地云端副本；
- 出现资源耗尽事件，或进程的提交量快速增长；
- 怀疑计划任务、监视器或同步客户端在不断重新生成数据。

## 安全规则

- 在任何变更之前，确认可用空间、卷、进程状态、锁、重解析点以及解析后的绝对目标路径。
- 对递归操作，确认目标位于明确选定的根目录之内。切勿将变量或通配符作为未经检查的删除目标。
- 不得删除卷、用户、仓库、云端或项目的根目录。
- 保留活动源、未提交的工作、机密信息、冲突副本、他人持有的锁、`.git` 以及唯一的恢复副本。
- 优先使用回收站、隔离、压缩或云端去水合。只有对已精确识别、可再生成的对象才允许不可逆删除；须记录路径、大小和恢复方式。
- 仅在具备必要权限、备有回滚方案并完成完整回读验证的前提下，才可更改页面文件、休眠、服务或系统级限制。`Zugriff
  verweigert` 不构成成功的措施。
- 绝不为释放本地空间而删除 OneDrive 云端对象。云端删除与本地去水合是两种不同的操作。

## 阶段一：紧急释放

### 1. 基线

至少记录以下内容：

```powershell
Get-PSDrive -Name C | Select-Object Used, Free
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID, Size, FreeSpace
Get-Process | Sort-Object PrivateMemorySize64 -Descending |
  Select-Object -First 15 Name, Id, PrivateMemorySize64, WorkingSet64
```

记录时间、初始数值和目标。区分 `PrivateMemory`（或提交量）与 `WorkingSet`：进程的工作集可能显示较少的内存，但页面文件占用却很大。

### 2. 有限范围盘点

从已知的本地根目录和近期的变更时段开始。不要盲目递归扫描所有云端或用户目录。合适的候选对象包括：

- 明确可再生成的模型、包和构建缓存；
- 旧的、已完成的构建输出；
- 可轮转的应用日志；
- 已验证的归档或备份代次；
- 已完全同步的本地云端副本。

对于稀疏文件、压缩文件和云端占位文件，文件长度并不等于物理占用。请使用 NTFS 分配信息（`GetCompressedFileSizeW`）、`compact` 或同等工具，并对比前后的可用空间。

### 3. 处理单个对象

每个测量步骤只处理一个对象。之后检查：

- 实际回收的字节数；
- 错误、未关闭的句柄以及残留的锁；
- 受保护源是否仍然存在；
- 能否恢复或再生成；
- 是否有进程立即重新生成了该对象。

只有在确认额外回收了 10 GB 之后，紧急模式才会结束。之后流程直接转入取证。

## 阶段二：取证确定填充进程与产生源

### 1. 资源耗尽与页面文件

同时查阅当前和历史证据：

```powershell
Get-CimInstance Win32_ComputerSystem |
  Select-Object AutomaticManagedPagefile
Get-CimInstance Win32_PageFileUsage |
  Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage
Get-WinEvent -FilterHashtable @{LogName='System'; Id=2004} -MaxEvents 20
```

Windows 资源耗尽检测器的 2004 号事件包含事件发生时提交量最高的进程。请将 PID、进程名、时间戳和字节数与当前进程进行对应。仅凭一个较大的 `pagefile.sys` 无法证明该文件本身就是肇事者；需要查找触发提交的进程。

### 2. 文件增长

按以下维度对新增或修改的文件进行分组：

- 创建与修改的小时；
- 父路径与扩展名；
- 所有者或产生该文件的进程；
- 按文件数和物理占用字节数统计的每日增长速率。

请特别检查日志、缓存、同步、备份、构建、下载和会话目录。如果某个客户端每天写入数 GB，而卷又很小，那么保留七天就不合适。

### 3. 自动化任务

检查任务计划程序、服务、监视器和启动程序的频率、保留策略与执行结果：

```powershell
Get-ScheduledTask | Where-Object State -ne 'Disabled'
Get-ScheduledTaskInfo -TaskName '<task-name>'
```

分别核实操作、触发器、重复间隔、最近一次返回代码以及下次运行时间。存在某个任务本身并不能证明保留策略或频率能够控制实际增长。

## 阶段三：长期限制

选择最小且有效、可逆的措施：

- 更频繁地执行日志轮转，并同时设置大小上限；
- 有控制地重启异常客户端，并测量其提交量；
- 将终端回滚缓冲或调试日志限制在合理值；
- 删除旧的、可再生成的缓存，并观察其是否被自动重新生成；
- 对已验证的云端内容使用“释放空间”进行去水合；
- 根据经验得出的每日增长速率调整计划任务的频率与保留策略；
- 仅以管理方式更改页面文件或休眠设置，并准备重启与回滚计划。

例如，对于 Windows 终端，一个受限的默认回滚缓冲区可以这样设置：

```json
{
  "profiles": {
    "defaults": {
      "historySize": 2000
    }
  }
}
```

保留现有设置，并在修改后验证 JSON 文件。

### OneDrive 专用关卡

在去水合之前，必须确认同步状态以及待上传内容。请使用能识别云筛选器的文件管理器，或资源管理器中的“释放空间”命令。去水合不得删除云端内容。

单独检查位于 `$env:LOCALAPPDATA\Microsoft\OneDrive\logs` 下的本地 OneDrive 日志区域。如果某个子目录每天产生数 GB，请将基于时间的保留策略与严格的大小上限结合起来，并配合足够频繁的计划运行。保护新近创建或正在打开的文件，并在运行后同时检查任务状态和剩余大小。

## 结束检查与报告

在最后一次变更之后：

1. 等待异步的云端或删除操作结束。
2. 重新读取可用存储空间和进程提交量。
3. 通过回读检查已更改的配置、任务和日志大小。
4. 执行简短复测：在观察窗口内是否再次出现过度占用存储的情况？
5. 报告初始数值、每个对象及其处理决定、实际回收的物理字节数、填充进程、长期调整、回滚操作、残余风险以及最终数值。

若没有相应的当前回读结果，不得声称已完成清理、已限制进程或已达到 50 GB 目标。

## 已知限制

- 在没有管理员权限的情况下，页面文件、休眠或服务的更改可能仍被阻止。请记录确切的剩余步骤。
- 历史进程事件可证明过去存在的填充者；要了解当前状况，还需要进程和文件增长数据。
- 已规划的备份方案并不等于备份。迁移或删除必须以当前目标的身份、清单或哈希、恢复验证和挂载为前提。
- 若所有权不清、有他人正在进行的工作，或目标未知，则适用决定 `nichts`。

## 变更日志

### 1.0.0 (2026-08-05)

- 为中央技能库提供的可移植首个版本。
- 新增资源耗尽、页面文件与进程取证。
- 明确区分 NTFS 物理占用与 OneDrive 去水合。
- 加入带时间与大小限制的 OneDrive 日志轮转。
- 定义了带回读验证的严格紧急与结束关卡。
