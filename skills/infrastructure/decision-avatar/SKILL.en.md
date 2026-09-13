---
name: decision-avatar
version: 1.0.0
type: protocol
author: Claude + Codex
created: 2026-07-28
updated: 2026-07-30
description: >
  When an authorized local decision profile exists: predict recurring decisions from
proven feedback, calibrate confidence, and strictly separate prediction, decision,
and execution.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [entscheidung, avatar, theory-of-mind, feedback, konfidenz, provenance]
language: en
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "private decision-avatar profile (not published)"
  origin_version: "1.2.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="decision-avatar banner">

# Decision Avatar

## Purpose

This skill does not replicate a person. It provides a verifiable procedure to derive a probable preference from genuine, authorized evidence for recurring decision types.

Use it only when a local decision profile exists and its use is permissible for the current task. Without a profile, the skill delivers no surrogate decision.

Use is considered authorized only if the task, applicable agent rules, or profile metadata explicitly allow the current purpose. Mere accessibility of a profile file is not consent.

## Core Principles

1. **Proof before assumption.** Direct statements and confirmed decisions carry more weight than derived patterns.
2. **Prediction is not a statement by the person.** Agent outputs must not flow back into the profile as new primary evidence.
3. **Deciding is not executing.** A recommendation can be firm, even though its implementation requires additional authority.
4. **Silent agreement is not feedback.** Absence of objection does not confirm a prediction.
5. **Profiles remain local and private.** Do not copy personal data, secrets, or sensitive content into shared skill files.

## Portable Profile Model

File names are freely configurable; only these roles are required:

| Role | Content |
|---|---|
| Methodology | Evidence levels, data protection, and calibration rules |
| Proven Preferences | Direct statements and confirmed decisions |
| Hypotheses | Derived rules with confidence and sources |
| Actions | Actions taken based on a prediction |
| Feedback | Confirmation, correction, or rejection by the person |

Project-related, more recent decisions take precedence over general preferences.

Every processed piece of evidence should contain at least:

```text
Quellen-ID:
Datum:
Entscheidungstyp und Gültigkeitsbereich:
Status: bestätigt/korrigiert/widerrufen
Gültig bis: <optional>
```

Do not use revoked, expired, or out-of-scope evidence. In case of conflicting confirmed evidence, the more specific one wins first, followed by the more recent one. If conflict persists, set confidence to "low" and escalate.

## Decision Loop

### 0. Check Local Priority Rule

If a confirmed rule exists for the current project or specific decision type, use it and document its source.

### 1. Search for Real Evidence

Use only evidence permissible according to local methodology. Task lists, agent logs, earlier avatar responses, and arguments from the current session are not statements by the person.

### 2. Form Prediction

Always output the result with justification and one of three levels:

- **high:** multiple direct, consistent, and relevant pieces of evidence,
- **medium:** plausible pattern with limited or indirect evidence,
- **low:** novel situation, contradictory evidence, or no resilient pattern.

Consequential decisions are not automatically "low". Confidence measures evidence for preference, not the scope of subsequent execution.

### 3. Separate Modes

| Mode | Result | Side Effect |
|---|---|---|
| Predict | Probable position + evidence + confidence | none |
| Decide | Concrete choice + justification + confidence | none |
| Act | Authorized, safe implementation + action log | possible |

In Action mode, runtime authority and safety rules additionally apply. Low confidence or lack of execution authority leads to escalation, not silent execution.

### 4. Calibrate Feedback

After real feedback:

1. Mark prediction as confirmed, corrected, or rejected.
2. Optionally record a rating scale.
3. Record distinction between directional error and fitting error.
4. Adjust hypothesis and confidence.
5. Only transfer genuine feedback into proven preferences.

## Output Format

```text
Entscheidungstyp:
Modus:
Wahrscheinliche Präferenz:
Konfidenz:
Zulässige Belege:
Gegenbelege oder Unsicherheit:
Ausführung autorisiert: ja/nein
Nächster Schritt:
```

In outputs, state only redacted source IDs and the evidence summary necessary for the decision. Do not reproduce private statements, absolute profile paths, or sensitive raw data.

## Limitations

- No diagnostics or assertions about a person's inner states.
- No use of a profile outside its allowed purpose.
- No automatic adoption of agent assumptions as personal knowledge.
- No execution based solely on a prediction if new authority is required for it.

## Changelog

### 1.0.0 (2026-07-28)
- Extracted feedback precognition, confidence calibration, and provenance separation from a personal avatar configuration into an independent, portable protocol.
- Operationalized authorization, evidence lifecycle, conflict resolution, and redacted output.
