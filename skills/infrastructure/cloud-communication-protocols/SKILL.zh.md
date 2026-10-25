---
name: cloud-communication-protocols
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-25
language: zh
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [ping-pong, agent-beam, listeners, cross-machine, sync-yard, coordination]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: "用于跨不同机器的智能体之间基于云的通信协议的总括性技能(Ping-Pong、agent-beam、Listener 及未来协议)。当工作需要通过共享同步文件夹或 Message-Yard 跨机器协调时使用。"

translated_from_sha256: 9f6c20f17b3f62f11b709c05cde26d3c28b48495a60ffaa26cf96a17af27a8ce
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="cloud-communication-protocols banner">

# cloud-communication-protocols

一组协议,使两个或更多智能体在不同机器上通过一个共享的、云同步的文件夹(即"Yard")进行协调,而无需直接通道。本技能是**总括层**:它汇集这些协议,标明哪些已经过验证,并锁定仍处于概念阶段的协议。

## 何时使用

- 工作跨越两台或更多机器(验证、镜像部署、试点),且不存在直接的智能体对智能体通道。
- 需要在这些机器之间就任务、回复、节奏和升级建立共同的术语。

## 本协议族中的协议

### 1. Ping-Pong(已验证,基础协议)

两个或更多工作进程使用错开的计划扫描来弥合云同步延迟:每一方扫描 Yard 中寻址给自己的任务,执行,留下回复,并可为另一方签发后续任务。

核心规则:只写入自己的时隙,每项操作都有凭证,保证幂等性,Yard 中不存放机密(仅公钥/指纹/路径),协作式错误增量,回读优先于日志的验证。

**节奏:自适应轮询频率。** 节奏控制不属于基础协议的载荷规则,但任何实现都需要它——固定的轮询间隔要么会对空的 Yard 造成洪泛,要么会错过新的工作。两种机制均适用,且必须明确处理,而不能隐含:

- **A — 自调整(默认,无需操作员输入;即 `cooldown`/退避模式)。** 发现新任务 → 立即跳到最快间隔(例如 15 分钟)。空运行 → 沿阶梯降温:连续 4 次空运行 → 30 分钟,再 2 次 → 1 小时,之后每个新的空运行系列加倍(2 小时、4 小时、8 小时),直至硬上限(24 小时,绝不更高)。将空运行计数器和当前间隔持久化到工作进程的一个小状态文件中(而不是对话记忆里),以便在重启后保留;更改节奏意味着删除旧的计划任务,并以新间隔创建新任务,计数器延续。完整的参考模式、状态文件模式以及其他循环类型(突发、唤醒辅助):配套技能 **`cron-tuner`**。
- **B — 对等方指令覆盖。** 每一方可在任务文本中明确设定另一方的节奏——`CADENCE: match 15m` 以便同步到更窄的时间窗口,或 `CADENCE: pause 1h → 2h after 3
  empty` 以便让一方在可规划的深度工作中降速。更改对等方节奏的一方,须在下一次增量中确认新间隔(回读同样适用于时钟)。

两种机制都只改变响应时间,绝不改变基础协议规则(时隙纪律、凭证、无机密)。一个相互的 `WAKE: <Grund>` 通道允许在周期之外进行扫描,仅作为提示而非权威;读取后即删除。

完整规范与参考凭证:
`dev-bricks/system-gap-master` → `docs/communications-protocols-skill.md`。

### 2. agent-beam(概念,已锁定)

用于紧急工作:由提示词加启动脚本组成的数据包被放入目标时隙,目标机器上的监视器用它启动本地智能体运行——智能体带着任务和启动脚本"落地",并立即开始工作。

已锁定:在任何激活之前,需要一份已签名的启动脚本信任契约、一个隔离/审查步骤以及明确的操作员批准。

### 3. Listener / Ear-to-Ear-Listening(概念,已锁定)

监视器观察 Yard 中的触发器(文件到达、标志文件、注册表变更),并在另一台机器上启动智能体。"Ear-to-Ear":一台主机的监听器观察另一台主机的收件箱。

已锁定:需首先制定防抖规则、按时隙划分的触发器白名单以及安全契约。

## 通用不变量(所有协议)

- Yard 是传输层,绝不是工作区,也绝不是机密存储。
- 每项操作都会留下可验证的凭证;没有产物的"已完成"并不算完成。
- 错误处理是协作式的:附带假设和反向测试的错误增量,欢迎第二意见。
- 合作伙伴的缺席通过平台的空缺规则处理(例如 48 小时),而不是通过升级处理。

## 添加新协议

新协议通过在 `communications-protocols-skill.md` 中作为子章节加入本协议族(先作为概念,在被称为"已验证"之前须具备自己的安全契约和凭证)。在此列出,每个协议一行:名称、状态(概念/试点/已验证)、用途。
