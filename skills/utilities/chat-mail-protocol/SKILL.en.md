---
name: chat-mail-protocol
version: 0.1.0
type: skill
author: Ocean Contributors
created: 2026-11-27
updated: 2026-11-27
description: "Use when turning chat histories (WhatsApp, Discord, Slack, Telegram, Teams) or email threads into structured summaries, decision minutes, or action-item lists (e.g. 'create chat protocol', 'summarize email thread into tasks', /chat-mail-protocol, /protokoll). Uses a self-healing channel/chat profile cascade (default-config.json -> <channel>.json -> <channel>.<chat>.json), replaceable templates, and 5 formats (html/pdf/md/txt/json) with safe dry-run delivery planning. Do NOT use for drafting individual outgoing emails (privat-mail-writer) or multi-source research dossiers (dossier-briefing)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: utilities
tags: [protocol, meeting-notes, chat, email, whatsapp, slack, discord, action-items, ocean-standard]
language: en
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: ["grounding-seed (optional, recommended)"]
  skills: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# chat-mail-protocol — Protocols & Action Lists from Chat and Email Threads

Transforms unstructured **chat exports** (WhatsApp, Slack, Discord, Telegram, Teams, JSON exports, plain transcripts) and multi-message **email threads** into source-anchored **summaries**, **decision minutes (`ergebnisprotokoll`)**, **chronological logs**, and **action-item lists** — built to the `ocean-skill-creator` (`v0.4.0`) standard using 100% Python standard library code.

## When to activate

- "turn this WhatsApp/Slack/Discord chat into decision minutes", `/chat-mail-protocol`, `/protokoll`
- "summarize this email thread and extract all open action items with owners"
- "render a print-ready PDF/HTML protocol plus a short reply for the chat"
- **Boundaries:** Do NOT use for drafting standalone outgoing letters or emails (`privat-mail-writer`), raw audio speech-to-text (`transkription`), or multi-document research briefings (`dossier-briefing`).

## Core invariants (grounding & safety)

1. **Source anchors, zero hallucination:** Every extracted decision (`D-xx`), action item (`A-xx`), open question (`Q-xx`), and blocker (`B-xx`) cites its exact message index (`#source_index`), speaker, and verbatim quote.
2. **Never invent deadlines or owners:** A due date (`due`) is populated only when an explicit date appears in the message text; otherwise it stays `due: null` (`—`). Unassigned tasks are honestly labeled `offen`.
3. **Safe-by-default delivery (`dry_run: true`):** `protocol_core.py` never sends external messages or emails autonomously. Even when `reply_in_chat: true` is active in a profile, it prepares a reviewable draft payload inside the delivery plan (`sent_externally: false`).

## Hierarchical configuration cascade & self-healing

All presentation, format, and delivery settings live outside code in JSON profiles merged from general to specific:

```text
1. default-config.json                  (tracked, user-neutral fallback shipped with the skill)
2. <config_dir>/config.json             (local instance override)
3. <config_dir>/<channel>.json          (e.g. whatsapp.json, slack.json, discord.json, email.json)
4. <config_dir>/<channel>.<chat>.json   (e.g. whatsapp.projekt-alpha.json — overrides whatsapp.json!)
5. CLI flags                            (--doc-types, --formats, --template, --anonymize)
```

- **Bundled example profiles (`profiles/`):**
  [slack.example.json](profiles/slack.example.json), [whatsapp.example.json](profiles/whatsapp.example.json), [whatsapp.projekt-alpha.example.json](profiles/whatsapp.projekt-alpha.example.json), [discord.example.json](profiles/discord.example.json), [email.example.json](profiles/email.example.json).
- **Self-healing (`self_healing`):** Missing channel or chat profiles fall back seamlessly to the previous intact layer down to [default-config.json](default-config.json). Corrupt JSON files or mistyped sections never crash execution; with `--repair-config`, corrupt files are preserved byte-for-byte as `<filename>.corrupt.<YYYYMMDDTHHMMSSZ>.bak` and restored atomically.

## Reports, 5 output formats & replaceable `templates/`

[protocol_core.py](scripts/protocol_core.py) separates extraction from layout through replaceable templates and five output formats:

- **Templates in `templates/` (overridable via `templates.custom_dir`):**
  - [ergebnisprotokoll.html](templates/ergebnisprotokoll.html) — print-ready `@media print` A4 HTML5 document with metadata header, summary, decision cards, task table, and open blockers (fully `html.escape`-protected).
  - [ergebnisprotokoll.md](templates/ergebnisprotokoll.md) — structured GitHub-Flavored Markdown minutes.
  - [ergebnisprotokoll.txt](templates/ergebnisprotokoll.txt) — clean plain-text minutes.
  - [kompakt-chat.txt](templates/kompakt-chat.txt) — concise chat reply summary for `reply_in_chat`.
  - [aufgabenliste.md](templates/aufgabenliste.md) — focused task and owner checklist.
- **Output formats (`--formats`):** `html`, `pdf` (pure-stdlib `%PDF-1.4` generator using `WinAnsiEncoding` for German Umlaute `ä ö ü Ä Ö Ü ß`, automatic page breaks, and exact `xref` byte offsets with zero browser dependency), `md`, `txt`, `json`.

## CLI quickstart

```bash
# Parse transcript, auto-detect channel, and export MD/HTML/PDF protocols
python skills/utilities/chat-mail-protocol/scripts/protocol_core.py process \
  --input chat_export.txt \
  --chat projekt-alpha \
  --out-dir ./protocols \
  --json

# Inspect merged profile cascade (and optionally self-heal corrupt local JSONs)
python skills/utilities/chat-mail-protocol/scripts/protocol_core.py show-config \
  --channel whatsapp --chat projekt-alpha --config-dir ./my-profiles --repair-config --json

# List built-in and custom templates
python skills/utilities/chat-mail-protocol/scripts/protocol_core.py list-templates --json
```

## Providers & alternatives

- **Standalone stdlib engine:** `scripts/protocol_core.py` runs 100% locally and offline with zero external packages.
- **Optional ecosystem docking:** Setting `delivery.handoff_tasks_to` (`"ticket-master"` or `"kalender"`) prepares structured action-item handoff payloads; external connectors are resolved via [connections.json](connections.json) (`grounding-seed`) and never installed without explicit user approval.

## Self-update

- Periodically check `lernvertrag.letzter_update_check` in `default-config.json` / `config.json` for updated messenger export formats and consult `skill-finder` for adjacent skills.
- Append dated lessons learned to `connections.json` (`gelernt`).

## Related skills

- `ocean-skill-creator` — v0.4.0 configuration, self-healing, and template standard used to build this skill.
- `privat-mail-writer` — drafting individual outgoing emails and letters.
- `dossier-briefing` — multi-source decision and research briefings.
- `transkription` — audio transcription upstream of chat/meeting protocol generation.
- `kalender` — scheduling follow-up deadlines and appointments.

## Changelog

### 0.1.0 (2026-11-27)
- Initial release built to the `ocean-skill-creator` (`v0.4.0`) standard: 4-stage channel/chat profile cascade (`default-config.json` -> `config.json` -> `<channel>.json` -> `<channel>.<chat>.json`), self-healing backups, multi-messenger & email-thread parser, source-anchored decision/task extractor, 5 output formats (`html`, `pdf` with `WinAnsiEncoding`, `md`, `txt`, `json`), 5 replaceable templates, and safe dry-run delivery planning.
