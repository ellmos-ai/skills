---
language: en
---

> **English** — Official English version of `decision-avatar`.

# Decision Avatar

## Overview & Purpose

This skill does not replicate a person. It provides a verifiable procedure to derive a likely preference for recurring decision types based on authentic, authorized evidence.

Use it only when a local decision profile exists and its use is permissible for the current task. Without a profile, the skill provides no proxy decision.

Usage is considered authorized only if the task, applicable agent rule, or profile metadata explicitly allows the current purpose. Mere accessibility of a profile file does not constitute consent.

## Core Principles

1. **Evidence over assumption.** Direct statements and confirmed decisions carry more weight than inferred patterns.
2. **Prediction is not a statement by the person.** Agent outputs must not flow back into the profile as new primary evidence.
3. **Deciding is not executing.** A recommendation can be firm even though its implementation requires additional authority.
4. **Silent agreement is not feedback.** Absence of objection does not confirm a prediction.
5. **Profiles remain local and private.** Do not transfer personal data, secrets, or sensitive content into shared skill files.

## Portable Profile Model

Filenames are freely configurable; only these roles are required:

| Role | Content |
|---|---|
| Methodology | Evidence tiers, data privacy, and calibration rules |
| Evidenced Preferences | Direct statements and confirmed decisions |
| Hypotheses | Derived rules with confidence and sources |
| Actions | Actions taken based on a prediction |
| Feedback | Confirmation, correction, or rejection by the person |

Project-related, more recent decisions take precedence over general preferences.

Every evaluated piece of evidence should contain at least:

```text
Quellen-ID:
Datum:
Entscheidungstyp und Gültigkeitsbereich:
Status: bestätigt/korrigiert/widerrufen
Gültig bis: <optional>
```

Do not use revoked, expired, or out-of-scope evidence. In case of conflicting confirmed evidence, the more specific one wins first, followed by the more recent one. If the conflict persists, set confidence to "low" and escalate.

## Decision Loop

### 0. Check Local Precedence Rule

If a confirmed rule exists for the current project or specific decision type, use it and document its source.

### 1. Search for Real Evidence

Only use evidence permitted under the local methodology. Task lists, agent logs, previous avatar responses, and current session arguments are not statements by the person.

### 2. Form Prediction

Always output the result with a rationale and one of three confidence levels:

- **high:** multiple direct, consistent, and relevant pieces of evidence,
- **medium:** plausible pattern with limited or indirect evidence,
- **low:** novel situation, conflicting evidence, or no reliable pattern.

High-consequence decisions are not automatically "low". Confidence measures the evidence for the preference, not the scope of subsequent execution.

### 3. Separate Modes

| Mode | Output | Side Effect |
|---|---|---|
| Predict | Likely position + evidence + confidence | None |
| Decide | Concrete choice + rationale + confidence | None |
| Act | Authorized, safe implementation + action log | Possible |

In action mode, runtime authority and safety rules additionally apply. Low confidence or lack of execution authorization leads to escalation, not silent execution.

### 4. Calibrate Feedback

Upon receiving real feedback:

1. Mark prediction as confirmed, corrected, or rejected.
2. Optionally record a rating scale.
3. Note the difference between directional error and framing error.
4. Adjust hypothesis and confidence.
5. Transfer only real feedback into evidenced preferences.

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

In outputs, include only redacted source IDs and the evidence summary necessary for the decision. Do not reproduce private statements, absolute profile paths, or sensitive raw data.

## Limitations

- No diagnostics or assertions about a person's internal mental states.
- No use of a profile outside its authorized purpose.
- No automatic adoption of agent assumptions as personal knowledge.
- No execution based solely on a prediction when new authority would be required.

## Changelog

### 1.0.0 (2026-07-28)
- Extracted feedback precognition, confidence calibration, and provenance separation from a personal avatar configuration into a standalone, portable protocol.
- Operationalized authorization, evidence lifecycle, conflict resolution, and redacted output.