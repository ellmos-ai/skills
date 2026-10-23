---
name: doc-reality-loop
version: 0.1.0
type: protocol
author: ellmos contributors
created: 2026-10-23
updated: 2026-10-23
description: >-
  Check factual documentation claims against evidenced effects and carry
  confirmed corrections through independent review and remeasurement.
standalone: false
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: infrastructure
language: en
status: draft
visibility: public
provenance:
  origin: custom
  origin_path: https://github.com/ellmos-ai/open-ocean
  origin_version: 3f2d4f306f4fc57ad5bb7596d10312c8a8da1cfa
  last_sync_from_origin: 2026-10-23
---

# Compare documentation with actual effects

This catalog adapter exposes the shared **doc-reality-loop** maintained in Ocean.
It requires the external pinned sources and the consuming product's authority
for measurement, correction and acceptance.

## Resolve the source

Read [source-pin.v1.json](source-pin.v1.json). Locate the German or English workflow
and the contract at its fixed commit. Compare SHA-256 over exact Git blob bytes
before using their content; a Windows checkout can have different line endings.
An unreachable source or hash mismatch leaves the method unverified. Do not
substitute a moving `main` reference.

## Carry out the task

Then use the matching variant of the **fully read** shared workflow:
`help`, `root`, `requirements` or `freshness`. Product paths, registers,
intervals, tools and permissions come from the requesting consumer.
Missing host, instance, version or effect evidence remains `unknown`.
Loading this skill does not expand the task or its write permissions.

The shared contract separates triggering, task creation, actual execution,
text correction, independent review and remeasurement. Task status and dispatch
markers do not prove later stages. Preserve open requirements; archival needs
reader and link checks and a recovery path. The referenced checker validates
evidence-chain shape and does not replace checking the evidence itself.

## Product adapters

For BACH, also use its product adapter at
`system/skills/workflows/doc-reality-loop-bach.md` once it is integrated and
available in the actual BACH revision. Record a missing adapter as open
integration. Other consumers use their own evidenced adapter; this catalog entry
does not install or start a consumer.

Deutsch: [SKILL.md](SKILL.md).

## Usage example

Request: “Check the manual's version claims against the specified release.”
Load the pinned method and choose freshness. Capture each version claim with
its source and readers, compare it with actual release evidence and report
unreachable surfaces as unknown. If the task only authorizes analysis, deliver
differences and correction proposals; edit the manual only when authorized.

## Changelog

- 0.1.0 (2026-10-23): Bilingual catalog adapter with a fixed Ocean source pin.
