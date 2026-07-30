---
name: privat-mail-writer
version: 0.2.0
type: skill
author: Lukas Geiger + GPT
created: 2026-06-19
updated: 2026-06-19
description: 当用户希望以自己的风格撰写、回复、拒绝、跟进、缩短、重述或起草私人或半正式电子邮件时，尤其是在安排预约、官方拒绝、友好简短回复以及根据联系人调整语气时，应使用此 Skill。仅在有具体邮件撰写任务时才启动分析文件。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [mail, email, privat, antwort, absage, termin, schreibstil, kontaktprofil]
language: zh
status: active
dependencies: {'tools': [], 'optional_tools': [{'name': 'mail-connector', 'path': '.AI/.MODULES/mail-connector/', 'cli': 'mailc', 'python_module': 'mail_connector.cli', 'usage': 'mailc context <kontakt> --mode reply --json  # Liefert Mail-Kontext als JSON für Profilaufbau', 'note': 'Optionales lokales IMAP-CLI-Tool. Nur nutzen wenn installiert (`pip install -e .` im Modulordner). Ohne dieses Tool arbeitet der Skill ohne Mailzugriff.'}], 'services': ['mail-backend-optional'], 'protocols': ['kontaktprofil', 'usecase-registry'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'None', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **中文** — `privat-mail-writer` 官方中文版本。

# Privat-Mail-Writer (中文)

## 概述与目的

Privat-Mail-Writer 用于生成简短、友好且契合特定联系人关系的邮件草稿。该 Skill 的设计保持用户中立：不包含真实联系人、真实签名或真实邮件内容。

其核心原则是延迟加载（lazy）与基于实证：仅当用户希望给特定联系人撰写具体邮件时，才创建或更新该联系人的配置文件。切勿预先批量生成配置文件。若无邮件历史记录可用，切勿凭空捏造写作风格，而应采用中立简短的语气撰写，或针对性地询问示例。

## 资源

- `CONFIG.md` - 核心偏好、如果-那么规则、权限关卡（permission-gates）和黑名单开关。
- `BLACKLIST.md` - 针对订阅邮件、系统发送者和无配置文件联系人的排除规则。
- `USECASES.md` - 用例注册表和新用例规则。
- `SIGNATURES.md` - 中立的签名和问候语规则。
- `MUSTER-BLOCKS.md` - 简短的可复用文本模块。
- `kontaktprofile.json` - 空白、用户中立的联系人配置文件 Schema。真实配置文件仅在本地保存且遵循数据节约原则。

## 工作流程

1. **加载配置：** 读取 `CONFIG.md`。若黑名单开启，还需检查 `BLACKLIST.md`。
2. **检查触发条件：** 仅在收到给特定联系人撰写邮件的具体任务时才生成配置文件，例如“给弟弟 Simon 写封邮件”。切勿仅为了创建配置文件而扫描收件箱。
3. **检查黑名单：** 订阅邮件、No-Reply、系统发送者以及被排除的域名/联系人不建立配置文件。对此类邮件应中立回复或不予回复。
4. **识别邮件任务：** 确定目标、收件人、事由、期望长度、语言、语气和必要事实。
5. **确定用例 (Usecase)：** 读取 `USECASES.md` 并选择最合适的用例。若无匹配用例，则新建一个可复用的用例，或者在缺少必要信息时简要提问。
6. **检查联系人配置文件：** 为每位未被排除的收件人，在 `kontaktprofile.json` 或私有本地副本中查找现有配置文件。
7. **创建或更新配置文件：** 若无可靠配置文件，从可用的邮件后端读取与该联系人的最多前 10 封相关邮件。在分析写作风格时，已发送邮件的权重应高于接收到的邮件。
8. **保存实证数据：** 在联系人配置文件中仅保存总结性、可验证的风格、关系和分类特征。切勿保存原始邮件、长段引用或不必要的个人细节。
9. **应用权限关卡 (Permission-Gate)：** 发送前、处理敏感内容或缺少必要信息时，严格遵守 `CONFIG.md` 中定义的关卡。
10. **撰写草稿：** 将用例结构、联系人配置文件和当前任务融合。模仿风格时，切勿捏造虚假亲近感、虚假承诺或未经证实的原因。
11. **交付输出：** 默认输出主题和邮件正文。仅在用户明确批准发送且有合适邮件工具可用时才执行发送。

## 联系人配置文件

联系人配置文件描述的不是联系人本身，而是观察到的沟通关系以及账号所有者针对该联系人的写作风格。

配置文件字段应保持精简：

- 最后联系时间
- 评估的邮件数量及时间段
- 称呼与结束语
- 你/您/正式程度
- 句子长度及典型简短度
- 热情度、直截了当程度、确定性
- 带有置信度的关系评估
- 联系人分类，例如 `family`, `inner-circle`, `friends`, `colleagues`, `services`, `official`, `unknown`
- 分类来源：用户说明、邮件正文、通讯录、签名或推断
- 分类证据等级：`user-confirmed`, `strong`, `medium`, `weak`
- 简短的释义证据，如“多封已发送邮件以‘祝好’结尾”或“回复通常在五句话以内”

每月检查是否需要进行过期清理。若当前日期的月份与保存的 `last_age_check` 不同，删除 `last_contact_at` 超过一年的配置文件，并将 `last_age_check` 更新为当前日期。中立 JSON 中的初始值为 `2026-06-18`。

## 风格规则

- 保持简短。私人邮件很少需要长篇大论的开场白。
- 保持友好，但切勿过度解释。
- 仅在用户提供或上下文明确时才提及真实原因。
- 面对官方拒绝：礼貌、清晰，无需长篇解释。
- 对事实不确定时：在完成草稿前提出简短问询。
- 撰写德文文本时使用真实变音符号：ä, ö, ü, Ä, Ö, Ü, ß。

## 新增用例 (Usecases)

若某个邮件任务具有复用价值且未在 `USECASES.md` 中涵盖，可添加该用例：

- 稳定的 ID，例如 `UC-002`
- 名称及典型触发词
- 邮件目标
- 必填项与可选项
- 标准长度与语气
- 简短模板或模块顺序
- 缺少必填项时的提问内容

一次性的特殊情况不应扩充为通用用例，只需直接提供当前草稿。

## 输出格式

标准草稿格式：

```text
Betreff: ...

Sehr geehrte ...

...

Mit freundlichen Grüßen
[Signatur]
```

若用户仅需要无主题文本，则仅提供邮件正文。若有必要提供多种版本，最多提供两种版本：“极简”和“略带温情”。

## 边界与限制

切勿凭空捏造联系人配置文件。切勿将邮件中的敏感细节随意复制到回复中。未获得明确批准前切勿发送邮件。除非用户明确指示，否则切勿撰写法律、医疗或财务方面的承诺。

## 变更日志

### 0.2.0 (2026-06-19)
- 补充了 `CONFIG.md` 和 `BLACKLIST.md`。
- 将配置文件生成限制为具体的邮件撰写任务。
- 在配置文件 Schema 中加入了带有来源和证据等级的联系人分类。

### 0.1.0 (2026-06-19)
- 初始版本，包含用例注册表、签名规则、样例模块和空白联系人配置文件 JSON。