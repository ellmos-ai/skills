# Security Triage Summary — {{target_repo}} ({{date}})

> Validator: `python ../sec-scan/scripts/secfind.py validate findings.json coverage.json`

## 1. Import & Policy Context
- Sources imported: {{sources}}
- Security policy (`SECURITY.md`): {{policy_status}}
- Coverage state (`complete: false` for pure import): {{coverage_notes}}

## 2. Priority Breakdown
| Priority | Severity | Count | Status (`triaged` / `candidate` / `rejected`) |
|---|---|---|---|
| P0 | critical | {{p0_count}} | {{p0_status}} |
| P1 | high | {{p1_count}} | {{p1_status}} |
| P2 | medium | {{p2_count}} | {{p2_status}} |
| P3 | low | {{p3_count}} | {{p3_status}} |
| P4 | info | {{p4_count}} | {{p4_status}} |

## 3. Deduplicated & Skipped Items
- Merged duplicate IDs: {{merged_count}}
- Unimported alerts lacking file/line evidence (logged in `coverage.limits`): {{unimported_list}}

## 4. Next Steps & Ticket Tracking
- Candidates handed to `sec-validate`: {{candidate_next}}
- Ticket / Private Advisory references (secrets masked): {{ticket_refs}}
- Handover to `sec-report`: {{report_ready}}
