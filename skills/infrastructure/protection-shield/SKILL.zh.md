---
name: protection-shield
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "协调获授权的即时防御及周期性服务器日志和版本核查，保留证据、回读与恢复。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [defense, incident-response, server, logs, monitoring]
language: zh
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [tech-detect, security-tech-stack-check], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# protection-shield

仅适用于自有或明确授权的系统、网络及服务器。变更前核对资产、所有者、权限、锁、影响和恢复方案。警报本身不是生产变更授权；不得反击、访问他人资产或擅自扫描服务。

紧急处置先保存 UTC 时间、有限的相关日志及配置哈希，遮盖秘密，并区分症状、已证实入侵和假设。阅读项目预案、已有决定和私有的逐资产动作配置。只有具体授权时，才通过现有本地工具处理指定服务、防火墙规则、批准的凭据轮换或 security-tech-stack-check 补丁。绑定目标与恢复路径，核查结果、功能、日志效果和副作用；单独核查回滚。

周期检查使用私有配置指定资产、获授权的日志/API 读取器、时间窗口、过滤、保留期、tech-detect 快照、计划和上报路径。接入现有调度器，不新建守护进程。每次只读取指定范围、去重并通过 security-tech-stack-check 查询当前公告。报告覆盖和读取错误。只有真实调度及结果回执才证明已启用。

同一服务器的周期检查应通过 tech-detect compare 比较前后快照，保持 slot 与 hostname 不变。回读 axis=same-host-time、chronology、两次采集时间、覆盖及未知版本。不得靠改名绕过身份检查；缺少来源时 HOLD。
