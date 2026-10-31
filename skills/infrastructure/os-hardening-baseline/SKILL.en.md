---
name: os-hardening-baseline
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: >
  Checklist for the baseline hardening of your own laptop or PC on Windows, macOS and Linux:
  updates, protection program, firewall, disk encryption, accounts and privileges, remote
  access, boot chain. Each item has a read-only check and a target state; changes only after
  a backup and individual confirmation. Defensive, meant for private use, no substitute for
  the rules of a managing IT department.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [hardening, baseline, checklist, windows, macos, linux, endpoint, defensive, security]
language: en
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: custom
  origin_path: "skills/infrastructure/os-hardening-baseline/"
  origin_version: "1.0.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# os-hardening-baseline (English)

A baseline for a device that is **your own**, after an incident or as prevention. The list is
a target, not an order: every change is explained, backed up beforehand and confirmed
individually. Structural hardening of whole software projects does not belong here but to
`sec-hardening`.

**Procedure:** first only check (all check commands are read-only), collect deviations in
`incident-notes` or a case note, then decide with the owner what is changed. Some commands
need administrator rights; use the rights only for the individual check. Do not modify
devices managed by a company or school.

## Windows

| Item | Check (read-only) | Target |
|---|---|---|
| Updates | Settings, Windows Update; `Get-HotFix` | current, automatic updates on |
| Protection program | `Get-MpComputerStatus` (fields `AntivirusEnabled`, `RealTimeProtectionEnabled`) | active, signatures current |
| Firewall | `Get-NetFirewallProfile \| Select Name, Enabled` | all profiles on |
| Drive encryption | `Get-BitLockerVolume` (administrator) or Settings | system drive encrypted (where the device supports it), recovery key stored safely and **not** on the device |
| Secure Boot | `Confirm-SecureBootUEFI` | `True` |
| User Account Control | Settings, user accounts | on |
| Accounts and privileges | `Get-LocalGroupMember Administrators`, `Get-LocalUser` | everyday account without administrator rights; no unknown accounts; guest account off |
| Remote access | Settings, Remote Desktop; remote-support programs in the software list | on only if needed; remove unknown remote-support software (after consultation) |
| Legacy features | `Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol` | SMB1 disabled |
| Autostart and tasks | Task Manager, `Get-ScheduledTask` | only known entries |

## macOS

| Item | Check (read-only) | Target |
|---|---|---|
| Updates | `softwareupdate -l` | no pending security updates |
| Disk encryption | `fdesetup status` | FileVault on, recovery key stored safely |
| Gatekeeper | `spctl --status` | enabled |
| System Integrity Protection | `csrutil status` | enabled |
| Firewall | `/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate` | on |
| Accounts | System Settings, Users & Groups; `dscl . list /Users` | everyday account without administrator rights; guest account off |
| Remote access | System Settings, Sharing (Remote Login, Screen Sharing) | on only if needed |
| Login items and profiles | System Settings, General, Login Items; profiles | only known entries |

## Linux

| Item | Check (read-only) | Target |
|---|---|---|
| Updates | `apt list --upgradable` or `dnf check-update` | no pending security updates; automatic security updates on |
| Firewall | `ufw status` or `firewall-cmd --state` or `nft list ruleset` | active, inbound denied by default |
| Listening services | `ss -tulpn` | only what is expected |
| SSH (if a server runs) | `sshd -T \| grep -E 'permitrootlogin\|passwordauthentication'` | root login off, keys instead of password |
| Encryption | `lsblk -f` (type `crypto_LUKS`) | system disk or data encrypted |
| Privileges | `getent group sudo` or `wheel` | only necessary accounts |
| Boot chain | Secure Boot, if supported (`mokutil --sb-state`) | on |
| Audit tool | a recognised hardening audit (e.g. Lynis, read-only mode) | review the hints, do not apply them blindly |

## All systems

- **Recovery:** regular backup to a medium that is not permanently connected; try a
  restore at least once.
- **Accounts:** password manager, unique long passwords, two-factor with an app or security
  key, recovery details up to date.
- **Software:** only from official sources; uninstall what is unnecessary; limit browser
  extensions to what is needed. Compare installed software with current vendor advisories:
  `security-tech-stack-check`.
- **Network:** router firmware current, default passwords changed, the router's remote access
  off unless needed.
- **Everyday:** screen lock with a short timeout, no permanent administrator use, scepticism
  towards attachments and links.

## Carrying out changes

Per change: note the state, backup confirmed, change explained, owner confirms
individually, carry out the change, re-read the result (repeat the check command), note the
way back. No change that can make data unreadable (switching on encryption, changing
partitions) without a checked backup and a safely stored recovery key.
