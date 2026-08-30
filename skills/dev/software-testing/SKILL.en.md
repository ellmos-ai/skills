---
name: software-testing
version: 1.0.1
type: knowledge-protocol
author: Lukas Geiger
created: 2026-08-22
updated: 2026-08-22
description: Test strategy advisor for software projects — chooses the right test levels (unit/integration/system/acceptance), test types (functional, non-functional, change-related) and test design techniques (equivalence partitioning, boundary values, decision tables, exploratory) for the given situation and SDLC/CI phase, including the test pyramid, CI/CD gates, shift-left and best practices. Use this skill ALWAYS when tests are to be written, planned, prioritized or assessed — for "write tests", "test strategy", "test plan", "test concept", "what/how should I test", "which tests are missing", "improve test coverage", "set up QA", questions about regression/smoke/sanity/load/stress/security tests, or when setting up a test pipeline — even when "test" only comes up in passing. Boundary — use superpowers:test-driven-development for the TDD loop itself, bugfix-protocol for bug diagnosis, bugsweep for systematic bug search.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [testing, teststrategie, qa, unit-test, integration, regression, testpyramide, shift-left, ci-cd, istqb]
language: en
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'claude-code-recherche', 'origin_version': '1.0.0', 'created_from': 'Online research 2026-08-22 (ISTQB systematics, test pyramid, Agile Testing Quadrants, modern techniques); sources see testarten-katalog.md'}
---

# Software Testing: Test Strategy & Test Selection

This skill answers the question **"which tests do I need here, now, for
what?"** — systematically instead of from the gut. It provides the
decision logic; the full catalogue of all test types, techniques and
definitions lives in `testarten-katalog.md` (German) in the same folder —
look there for detail questions.

---

## 1. Framework: think in three dimensions

Before you plan or write tests, place the task on three axes (ISTQB).
Whoever only keeps "a list of tests" mixes up the axes and plans with
gaps:

| Axis | Question | Variants |
|---|---|---|
| **Test level** | At which layer? | Unit → Integration → System → Acceptance |
| **Test type** | Which property? | functional / non-functional / structure-related / change-related |
| **Test technique** | How are the test cases derived? | black-box / white-box / experience-based |

Cross-cutting: **static** (reviews, static analysis — no execution,
earliest and cheapest defect detection) vs. **dynamic** (code is
executed).

---

## 2. Situation router: what's the case?

Choose the entry point by the concrete situation:

| Situation | Approach |
|---|---|
| **Building a new feature** | Clarify acceptance criteria BEFORE the code (ATDD/BDD mindset). Unit tests alongside implementation (equivalence classes + boundary values). Integration test for new interfaces. One E2E happy path, no more. |
| **Fixing a bug** | First a test that reproduces the bug (red), then the fix (green) = **re-test**. Then a **regression** of the environment. Diagnosis itself → `bugfix-protocol`. |
| **Refactoring** | NO new feature tests — the existing suite is the safety net. First check whether the suite really covers the behavior (add characterization tests if needed). Coverage/mutation as a gap indicator. |
| **Legacy code without tests** | Don't start with unit tests for every function. First lay characterization tests at the system/API level around the current behavior, then add unit tests when touching individual parts. |
| **API / microservices** | API tests at the service level as the focus (middle pyramid layer). For separate teams/deployments: **contract testing** (e.g. Pact) instead of shared staging integration tests. |
| **Preparing a release** | Order: smoke (is the build stable?) → full regression → non-functional tests (load, security) → UAT/acceptance → smoke on the release candidate. |
| **Performance concern** | First define a measurable goal (e.g. "P95 < 300 ms at 1,000 users"), otherwise no test is evaluable. Load test = normal load, stress test = breaking point + recovery. Production-like environment mandatory. |
| **Setting up a test pipeline** | Implement CI/CD gates from section 4; start with unit + lint on every commit, then expand in stages. |
| **Writing a test strategy/test concept** | Structure along the 3 dimensions + phase mapping (section 4) + risk-based prioritization (section 6, point 10). |

---

## 3. Test levels: object under test, goal, timing

| Level | Checks | When | Rule of thumb |
|---|---|---|---|
| **Unit/component** | A single function/class in isolation (mocks/stubs) | During implementation, every commit | Broad base of the pyramid; fast (< seconds), deterministic |
| **Integration** | Interaction, interfaces, DB connection | After unit tests, on every merge | Integrate incrementally (top-down/bottom-up), never big bang on large systems |
| **System** | The whole system against technical requirements | As soon as an integrated build exists | Functional AND non-functional; independent testers are valuable |
| **Acceptance** | Business expectation, real-world use | Last stage before go-live | UAT by the business department; don't forget operational aspects (backup/deploy/monitoring); alpha/beta if applicable |

**Test pyramid** as a proportion: many unit tests, targeted
integration/API tests, few E2E tests (rule of thumb ~70/20/10 as a
starting point — adjust based on actual defect origin). An inverted
pyramid (many UI tests) = slow + flaky → avoid.

---

## 4. Phase mapping: when do you check what?

### CI/CD gates (modern standard mapping)

| Pipeline stage | Gate |
|---|---|
| Every commit | Unit tests, linter, static analysis (seconds–minutes) |
| Pull request | Code review, SAST/SCA, targeted component tests |
| Merge | Integration/API/contract tests, smoke on the test environment |
| Nightly / pre-release | Full regression, E2E, performance/load tests, DAST |
| Release candidate | Smoke on staging, UAT, acceptance |
| Production (shift-right) | Monitoring/observability, canary/blue-green, feature flags, chaos experiments if applicable |

**Time budgets & blocking rules (practical rules of thumb):**

- **Commit-to-feedback < 10 minutes** for the fast path (lint + unit +
  critical integration tests); the total pipeline up to staging **< 30–45
  minutes**; full regression nightly or before a release. A control loop
  that ticks slower gets bypassed.
- **Blocking vs. reporting:** unit, integration and smoke gates ALWAYS
  block (no merge/deploy on red). Nightly stages (regression, load, DAST)
  report via ticket/fix, but don't block every commit. After the prod
  deploy: smoke + monitoring — on red, rollback + incident.
- **Handover point:** the commit (git push) separates the inner loop
  (local: TDD, unit, fast iteration) from the outer loop (shared pipeline
  with gates). Whatever can be moved into the inner loop is caught there
  the cheapest (shift-left).

### Classic (V-model): design tests while specifying

Requirements↔acceptance test · system design↔system test ·
architecture↔integration test · code↔unit test. Core idea: the tests of a
level are designed **while creating the corresponding specification** —
not only at the end. Reviews of requirements/designs (static testing) are
the earliest defect detection there is.

### Agile Testing Quadrants (planning grid for sprints)

Q1 unit/TDD + Q2 story tests/BDD run continuously and **prevent** defects;
Q3 exploratory/usability/UAT + Q4 performance/security **evaluate** the
product once enough of the product exists. Details in the catalogue.

---

## 5. Choosing test design techniques

| If the test basis … | … then technique |
|---|---|
| has input ranges/value sets | **Equivalence partitioning** (one representative per class) + **boundary value analysis** (at and just beyond every boundary: for 5–50 test 4, 5, 50, 51) — the basic equipment for almost every unit test |
| has complex business rules/condition combinations | **Decision table testing** |
| has states and transitions (workflow, session, device) | **State transition testing** (also test forbidden transitions) |
| describes user flows | **Use-case/scenario testing** incl. error and exception paths |
| is code and coverage should be measured | **Statement/branch coverage** — as a gap indicator, not a goal (100% coverage ≠ correct) |
| is unclear/patchy or time is short | **Exploratory testing** (time-boxed sessions with a charter) + **error guessing** (null, empty string, special characters, time zones, race conditions) |

Systematic techniques first, experience-based ones deliberately
**complementary** — they find what scripts overlook.

---

## 6. Best practices (checklist when planning/reviewing tests)

1. **Shift-left:** reviews + static analysis starting from the
   requirements phase — the later a defect is found, the more expensive it
   gets (a widespread rule of thumb after Boehm; the direction is
   uncontested, the exact factors are disputed).
2. **Respect the test pyramid** — E2E tests sparingly, a broad unit base.
3. **Automate what repeats** (smoke, regression, API, unit) and anchor it
   in CI/CD gates; reserve manual capacity for exploratory + usability.
4. **Design test cases systematically** (section 5), not ad hoc.
5. **Make non-functional requirements measurable** — without a numeric
   target, no evaluable performance/load test.
6. **Re-test ≠ regression:** first confirm the fix, then side effects.
   Order smoke → sanity/re-test → regression.
7. **Handle flaky tests immediately** — quarantine, fix the cause or
   delete; unstable suites destroy trust in the pipeline.
8. **Manage test data/environments:** reproducible (container/IaC),
   production-like, anonymized or synthetic data.
9. **Measure test quality itself:** coverage as a gap indicator;
   **mutation testing** where coverage numbers could be misleading.
10. **Prioritize risk-based:** test depth by failure impact ×
    probability of error — not evenly distributed.
11. **Quality is a team task** (whole-team approach): involve testers
    early in requirements; BDD/ATDD as a shared vehicle with the business
    department.
12. **Don't forget shift-right:** monitoring, canary, feature flags; chaos
    engineering only once observability is mature.

---

## 7. Modern techniques — when to use additionally

| Technique | Use when … |
|---|---|
| **Contract testing** (Pact) | microservices with separate deployments/teams |
| **Mutation testing** (Stryker, PIT, mutmut) | the quality of an existing test suite should be assessed |
| **Property-based testing** (Hypothesis, fast-check) | invariants exist ("sorted is idempotent") and edge cases are feared |
| **Fuzzing** | parsers, deserialization, security-critical inputs |
| **Chaos engineering** | distributed systems + mature observability + clean rollbacks |

---

## Sibling skills (don't duplicate)

- **`superpowers:test-driven-development`** — the concrete red-green-
  refactor loop while writing code.
- **`bugfix-protocol`** — 6-phase diagnosis of a concrete bug.
- **`bugsweep`** — systematic bug-search run over a codebase.
- **`dev-cycle`** — 8-phase overall cycle (from its v1.2.0: tests are
  designed in phases 1/3/5, written in phase 6 and run in phase 7; this
  skill fills in WHICH tests should run where).

## Reference

Full catalogue (all test levels, test types incl. a detailed
non-functional table, all design techniques, agile quadrants,
static/dynamic, V-model, sources):
→ `testarten-katalog.md` (German, same folder)

Visual overall map — phases, control loops, roles and test gates as a
"software development wiring diagram" (sheet BL-5 = test hook-in, BL-2 =
control-loop cadence):
→ `../dev-cycle/SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (open in a browser)

---

## Changelog

### 1.0.1 (2026-08-22)
- Added time budgets & blocking rules for CI/CD gates (< 10 min fast path,
  < 30–45 min pipeline; blocking vs. reporting; rollback after prod-red)
  as well as the commit as the inner/outer loop handover point
- Added a reference to the wiring-diagram supplement in the dev-cycle
  skill; adjusted the dev-cycle boundary to its v1.2.0 (shift-left:
  design 1/3/5, write 6, run 7)

### 1.0.0 (2026-08-22)
- Initial version from online research (ISTQB systematics, test pyramid,
  Agile Testing Quadrants, CI/CD gates, modern techniques)
