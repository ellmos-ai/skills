# Third-Party Licenses & Software Inventory / Drittanbieter-Lizenzen

This document lists all third-party software components, libraries, and vendored assets used in **ellmos-skills** (`ellmos-ai/skills`).

**Project:** `ellmos-skills` (`ellmos-ai/skills`)  
**License:** [MIT License](LICENSE)  
**Audit Date:** 2026-09-20  
**Status:** AUDITED & VERIFIED (Pfad A Technical Hygiene & Licensing Governance)  

---

## 1. Runtime Dependencies & Zero-Dependency Core Architecture

**`ellmos-skills` has ZERO external runtime dependencies.**

All catalog generators, static validation gates, privacy boundary verifiers, and indexing tools operate exclusively on the Python Standard Library (`>= 3.10`):
- `pathlib` (portable filesystem path manipulation and resolution)
- `json` (structured metadata and schema serialization)
- `argparse` (deterministic command-line interfaces)
- `typing` & `dataclasses` (robust static typing and structured contract definitions)
- `re` (high-performance pattern matching and privacy token scanning)
- `subprocess` & `contextlib` (safe process boundaries and test isolation)
- `unittest` & `importlib` (regression testing and dynamic gate verification)

This architecture guarantees:
- **100% Local-First & Zero-Egress**: Zero outbound HTTP/S telemetry, no background network calls, and completely self-contained offline execution.
- **Supply-Chain Immunity**: Zero attack surface from unpinned transitive packages or hijacked registry namespaces.
- **Instant Portability**: Cold-start execution across all major platforms without compilation or package downloads.

---

## 2. Curated Third-Party Vendored Skills

The repository hosts curated, externally authored skills redistributed under verified, permissive open-source licenses within `skills/third-party/`:

| Skill / Path | Upstream Repository | Upstream Author | License | Notice & Boundary |
|:---|:---|:---|:---|:---|
| `skills/third-party/grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | MIT License | Thin entry point for plan interrogation (`disable-model-invocation: true`). Upstream `LICENSE` file preserved. |
| `skills/third-party/grilling` | [mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | MIT License | Core interrogation protocol (design-tree / frontier / rounds). Upstream `LICENSE` file preserved. |

All third-party skill inclusions are validated against the strict Third-Party Gate (`testing/privacy_gate.py`), ensuring:
- Upstream license file presence.
- Upstream pointer (`upstream` URI in frontmatter).
- Exclusively permissive licensing (0% copyleft, no commercial restrictions).

---

## 3. Development, Linting & QA Dependencies

The following open-source tools are used strictly for local development, linting, code formatting, and automated regression testing:

| Package | Version / Spec | License | Source / Upstream | Scope |
|:---|:---|:---|:---|:---|
| **pytest** | `>=7.0` | MIT License | [pytest-dev/pytest](https://github.com/pytest-dev/pytest) | Automated test execution and contract test suites |
| **ruff** | `>=0.1.0` | MIT / Apache-2.0 | [astral-sh/ruff](https://github.com/astral-sh/ruff) | High-speed static analysis, linting, and formatting |
| **setuptools** | `>=61.0` | MIT License | [pypa/setuptools](https://github.com/pypa/setuptools) | PEP 621 package build backend |

*Note: These tools are never distributed or required at runtime for skill consumers or agent runtimes.*

---

## 4. Governance & Runtime Invariants

The following 10 invariants govern every skill, utility script, and metadata manifest within **ellmos-skills**:

| Invariant ID | Name | Legal & Operational Scope | Compliance Status |
|:---|:---|:---|:---|
| **INV-LOCAL-01** | 100% Local-First & Zero Egress | Network & Privacy | **PASS** — Pure Markdown and local Python scripts; zero telemetry and zero outbound network calls. |
| **INV-PRIVACY-02** | Fail-Closed Privacy Boundary Gate | Data Protection | **PASS** — Automated privacy gate rejects concrete user homes, host-scoped names, and token patterns. |
| **INV-UNPRIV-03** | Non-Elevation & RunAsInvoker | Process Execution | **PASS** — All workflows execute strictly in unprivileged user space; root or admin elevation is prohibited. |
| **INV-SCHEMA-04** | Deterministic Frontmatter & Schema Integrity | Contract Compliance | **PASS** — YAML frontmatter strictly conforms to `docs/CONVENTIONS.md` and schema validation gates. |
| **INV-ISOLATION-05** | Portable & Self-Contained Skill Anatomy | Modularity | **PASS** — Skills package their own playbooks, references, and scripts without implicit host couplings. |
| **INV-PORTABLE-06** | Multi-Agent Runtime Portability | Interoperability | **PASS** — Compatible with Claude Code, Codex, AGY/Gemini, BACH, and local Ollama runtimes. |
| **INV-DISCOVERY-07** | Public/Private Boundary Isolation | Boundary Hygiene | **PASS** — Public catalog (`registry/components.json`) exposes only verified non-sensitive discovery fields. |
| **INV-PLATFORM-08** | Multi-OS Parity & Platform Independence | Portability | **PASS** — Linux, Windows, and macOS validated identically via multi-OS CI matrix on Python 3.10 to 3.13. |
| **INV-SYNC-09** | Multi-Host Cloud Sync & Lock Resilience | Concurrency | **PASS** — Hardened `.gitignore` and cooperative lock protocols prevent cloud sync races and data corruption. |
| **INV-SLA-10** | 48h Security Response & Triage Commitment | Governance | **PASS** — Formal response SLA: 48h initial acknowledgment, 5-day triage commitment via `SECURITY.md`. |

---

## 5. Copyleft & Legal Compliance Summary

- **Copyleft Percentage**: **0% Copyleft** (0 AGPL, 0 GPL, 0 LGPL).
- **Runtime Dependencies**: **0 external dependencies** (100% Python Standard Library).
- **Upstream Permissive Third-Party Code**: **100% MIT Licensed**.
- **Development Tooling**: **100% Permissive Open-Source** (MIT / Apache-2.0).
- **Audit Date**: 2026-09-20 (Pfad A Technical Hygiene Compliance Verification).

---

## 6. Upstream License Text

### MIT License (`ellmos-skills`, `pytest`, `ruff`, `setuptools`, `mattpocock/skills`)

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
