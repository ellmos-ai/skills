---
name: endpoint-triage
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: >
  Read-only collection and analysis plan for laptops and PCs (Windows, macOS, Linux) when
  malware, persistence or misconfiguration is suspected: what is collected, how the
  collection scripts run safely, how the output is read on a clean machine (processes,
  autostarts, services, network connections, accounts, patch level) and how observation
  stays separate from interpretation. The default is diagnosis without any change to the
  target device.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [incident-response, endpoint, triage, persistence, autostart, malware, windows, macos, linux, defensive, read-only]
language: en
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [rescue-intake]
  python: []

provenance:
  origin: custom
  origin_path: "skills/infrastructure/endpoint-triage/"
  origin_version: "1.0.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# endpoint-triage (English)

A collection plan and reading guide for a device that does not feel right. Precondition:
`rescue-intake` is complete (ownership, consent, mode). The skill is purely defensive and
**changes nothing on the target device.** What happens next is covered by
`malware-cleanup-guide`; case notes are kept with `incident-notes`.

## Principles

1. **Read-only.** Collection is read-only. Only the case folder may be written, and it lives
   on the removable medium, not on the target device's disk.
2. **Collect on site, analyse elsewhere (mode A).** The output is read on a clean machine.
   No agent accounts are signed in on the target device.
3. **Distrust the instrument.** On a compromised system, operating-system tools (process
   list, network status) may return manipulated output. A clean result is therefore only
   weak evidence of "clean". The more reliable view comes from inspecting the disk offline
   from a live system (mode B).
4. **Observation is not interpretation.** Every finding is noted as `observation` (what the
   output shows) and `interpretation` (what it might mean, with a confidence level),
   separately.
5. **No files into online services.** Only hash values are looked up, and only after the
   accompanying data has been anonymised (see `rescue-intake`).

## Collecting

The rescue package's collection scripts (`collect_win.ps1`, `collect_mac.sh`,
`collect_linux.sh`) write one text file per topic block into a case folder and create an
`INDEX.sha256` with checksums. **Always set the case folder explicitly to the removable
medium** (argument `-Case` or first argument), because the default is relative to the
current directory. Read the script content before starting and show it to the owner.

| Operating system | What is collected |
|---|---|
| Windows | OS version and last boot, processes (with path), startup commands, Run keys (`HKLM`/`HKCU`), services, scheduled tasks, TCP connections, local accounts, installed software, hotfixes, Defender status |
| macOS | Version, kernel, processes, network connections (`lsof -i`), launchd list, Launch Agents/Daemons (system and user), SIP, Gatekeeper and FileVault status, accounts, recent logins, disks |
| Linux | Kernel and distribution, processes, network connections and listening ports, systemd services and timers, `/etc/passwd`, recent logins, system cron, loaded kernel modules, disks and mounts, recently installed packages (dpkg) |

**Known gaps** of the standard scripts (query additionally if suspicion remains, still
read-only, and record the additional query in the case log):

- Windows: users' Startup folders, WMI event subscriptions, browser extensions, the `hosts`
  file and DNS settings, event logs (sign-ins, service installations).
- macOS: login items, configuration profiles, browser extensions, user cron.
- Linux: user crontabs, `authorized_keys`, shell startup files, contents of systemd unit
  files, `ld.so.preload`, package manager sources.

## Analysing (on the clean machine)

First verify `INDEX.sha256` against the files. Then, per topic block:

- **Processes and autostarts:** entries starting from user-writable paths (Temp, Downloads,
  AppData, `/tmp`, user LaunchAgents), with random-looking names, without a recognisable
  publisher, or with names imitating system processes (spelling variants), deserve a look.
  Remember: **conspicuous is not the same as malicious.**
- **Services, scheduled tasks, timers, cron, launchd:** newly added, unknown or
  schedule-triggered entries; persistence often shows up here.
- **Network connections:** unexpected listening ports, permanent connections to foreign
  addresses, connections from a process that should not be networked. Map process to
  connection through the process ID.
- **Accounts and sign-ins:** unknown local accounts, recently created accounts, sign-ins at
  unusual times.
- **Protection settings:** Defender or protection features switched off, SIP, Gatekeeper or
  FileVault off, missing updates (patch level). Compare installed software with current
  vendor advisories: `security-tech-stack-check`.
- **Timeline:** when does the conspicuous start (install date, start time, first entry)
  relative to what the owner did last?

Result per finding: ID, observation, interpretation with confidence level
(`confirmed`/`likely`/`unclear`), source (file in the case folder), recommended check. Open
questions stay explicitly open; "nothing found" only means that the collection shows
nothing, not that the device is clean.

## Handover

- Findings go into `incident-notes`.
- Further steps (isolate, back up, clean or reinstall): `malware-cleanup-guide`.
- Configuration weaknesses unrelated to an incident go into `os-hardening-baseline`.

## Out of scope

No obtaining of credentials, no bypassing of protection measures, no examination of other
people's devices without consent, no changes to the target device in this skill.
