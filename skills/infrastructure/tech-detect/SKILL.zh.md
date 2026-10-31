---
name: tech-detect
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "记录有来源证据的硬件和软件版本，生成私有快照，并在不把未观察到误判为卸载的前提下比较主机。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [inventory, hardware, software, python, versions, host-comparison]
language: zh
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# Tech Detect

仅检查自有或明确授权的主机。先阅读现有清单及主机槽位规则。对于 `<inventory>` 一类结构，`systems/<本机槽位>.json` 是输入；本技能不会更新该种子，更不会写入其他主机的槽位。

1. 核对权限、锁、主机身份和私有输出路径。运行 `python -X utf8 scripts/techshot.py capture --seed <清单>/systems/<本机槽位>.json --slot <本机槽位> --output <私有目录>/techshot-<UTC>.json`。
2. 离线工具读取本地平台及 Windows 卸载注册表、可用的 `dpkg-query` 或 Homebrew。这些来源都不能保证列出所有软件。不要查询 `Win32_Product`；[Microsoft 文档](https://learn.microsoft.com/en-us/powershell/scripting/samples/working-with-software-installations?view=powershell-7.6)说明该类查询可能触发 MSI 一致性检查和修复。
3. 分别记录当前 Python 解释器、PATH 中观察到的每个候选程序，以及通过 `--python-path` 指定的安装或虚拟环境。默认只有当前解释器的版本是精确的。仅对可信路径显式使用 `--probe-python <路径>` 执行 `-I -S --version`；否则版本保持未知。
4. 每项安装保留产品身份、安装身份、版本、证据来源及 `observed`、`reported`、`uncertain` 或 `unknown` 质量。种子中的硬件信息只标作清单报告值。列出采集失败和覆盖范围。
5. 使用 `python -X utf8 scripts/techshot.py compare --left <a.json> --right <b.json> --output <比较.json>` 比较私有快照。版本漂移与某主机未观察到软件是不同结论；未观察到不等于卸载。没有厂商证据不要合并别名。
6. 获得授权后才能接入已有调度器，并单独核对真实运行回执；提交技能代码不意味着定时任务已启用。

JSON 合约为 `ellmos.techshot.v1` 和 `ellmos.techshot-comparison.v1`。快照只是现有清单旁的观察数据，可能含私有路径；未知版本既不证明安全，也不证明受漏洞影响。传给 `security-tech-stack-check` 的内容应限于必要组件和哈希。

## 更新记录

### 1.0.0 (2026-10-25)

- 离线主机快照、跨主机比较及显式证据质量。

硬件观测与库存种子分开：操作系统、架构、CPU、内存和系统文件系统容量须附来源或标记 unknown；没有可移植读取器时 GPU 为 unknown。Linux 可读取 dpkg-query 或 rpm。跨主机比较将硬件标为不同或未知，未知不等于相同。不得采集序列号、MAC 地址或完整 PATH。

比较约定：不同 slot 即为 axis=cross-host（即使 hostname 相同）；同一 slot 和 hostname 且采集时间不同为 axis=same-host-time。结果保留 chronology、两个输入哈希、采集时间、主机身份、种子绑定和覆盖信息。已知版本相同但另有未知安装时仍报告 version-uncertain。缺少必要来源时拒绝比较；完整的历史快照仍可使用。比较时间不是重新采集时间。
