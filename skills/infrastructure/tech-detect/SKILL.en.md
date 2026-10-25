---
name: tech-detect
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "Capture evidence-bound hardware, installed software and Python versions as private versioned techshots; compare hosts without treating missing observations as uninstallations."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [inventory, hardware, software, python, versions, host-comparison]
language: en
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# Tech Detect

Use this skill only on an owned or explicitly authorized host. Read the existing inventory and host-slot rules first. With a `.SYNC/_inventory` style setup, `systems/<own-slot>.json` is the input seed; database and spreadsheet exports are projections. This skill never refreshes another host's seed.

Run the commands below from this skill directory, or resolve the script path first, with an **explicit Python interpreter**. Do not launch a `.py` file directly.

1. Check scope, permissions, locks and a private output directory. Capture with `python -X utf8 scripts/techshot.py capture --seed <inventory>/systems/<own-slot>.json --slot <own-slot> --output <private>/techshot-<UTC>.json`.
2. The offline helper reads the seed and local platform. On Windows it reads per-user/machine 32/64-bit Uninstall registry entries; on Linux available `dpkg-query` or `rpm`; on macOS available Homebrew inventory. None is a complete installation census. Never query `Win32_Product`: [Microsoft Learn](https://learn.microsoft.com/en-us/powershell/scripting/samples/working-with-software-installations?view=powershell-7.6) documents consistency checks and possible repair side effects.
3. Keep the effective running Python interpreter, all observed PATH candidates, and explicitly supplied `--python-path` installations or virtual environments separate. Only the running interpreter has an exact version by default. Use `--probe-python <trusted-path>` explicitly to run `-I -S --version` for another trusted executable; otherwise its version is unknown.
4. Preserve product identity, installation identity, version, evidence source and `observed`/`reported`/`uncertain`/`unknown` quality. Seed hardware remains reported with its seed date. Separate `hardware_observations` read OS, architecture, CPU model and logical cores, RAM and system-filesystem capacity; GPU remains explicitly `unknown` without a portable collector. Do not collect serial numbers, MAC addresses or the full PATH. A seed value such as `3.x` is not an exact version. Record collector failures and coverage.
5. Compare private snapshots with `python -X utf8 scripts/techshot.py compare --left <a.json> --right <b.json> --output <comparison.json>`. Version drift and a package not observed on one host are different findings; non-observation does not prove absence. Hardware fields are different or unknown, never silently equal when unmeasured. Do not merge aliases without vendor evidence.
6. Connect timestamped captures to an existing scheduler only after host authorization. Confirm the real scheduler receipt separately; a committed skill is not an installed schedule.

Contracts: `ellmos.techshot.v1` contains `captured_at_utc`, seed hash, `hardware_observations`, `python_context`, source coverage and component installations; `ellmos.techshot-comparison.v1` contains software and `hardware_changes`. Snapshots are observations beside the existing inventory source and can contain private paths. Pass only needed component evidence and hashes to `security-tech-stack-check`; unknown versions prove neither safety nor vulnerability.

## Changelog

### 1.0.0 (2026-10-25)

- Offline techshot and cross-host comparison with explicit evidence quality.
