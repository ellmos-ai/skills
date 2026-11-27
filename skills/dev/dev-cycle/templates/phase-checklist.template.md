# Dev Cycle Phase Checklist — {{feature_name}} ({{date}})

> Target CI commit-to-feedback cadence: `< 10 min` | Bugfix approach switch threshold: `20 min`

## Phases 1–4: Functional Discovery & Design (Shift-Left)
- [ ] **Phase 1 (Feature Requests):** Functional requirement stated ("User can X"), testable acceptance criteria attached
- [ ] **Phase 2 (Current State):** Existing tools, docs, DB schema, skills, and prior use cases checked
- [ ] **Phase 3 (Functional Planning):** Workflows, agent profiles, service boundaries, and B/O/E test checks mapped
- [ ] **Phase 4 (Functional Frontend):** Skill/workflow contracts readable without ambiguity

## Phases 5–8: Technical Alignment, Execution & Gates
- [ ] **Phase 5 (Backend Plan):** CLI commands, DB schema, API endpoints, and scripts aligned
- [ ] **Phase 6 (Backend Code):** TDD tests written first, works on empty DB, CLI + file/folder inputs, idempotent, zero hardcoded paths
- [ ] **Phase 7 (Tests & Review Gate):** B/O/E tests green, 4-eyes review passed (`software-testing` + `bugfix-protocol` if failing)
- [ ] **Phase 8 (Use Cases):** End-to-end user scenarios verified; feedback tasks logged to Phase 1

Notes:
{{notes}}
