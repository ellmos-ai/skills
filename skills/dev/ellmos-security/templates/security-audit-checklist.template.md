# Security Audit Routing Checklist — {{target_repo}} ({{date}})

> Contract: `../sec-scan/references/contract.md` | Validator: `../sec-scan/scripts/secfind.py`

## 1. Scope & Authorization Gate
- Target path / scope: {{scope}}
- Ownership confirmed (own code / explicit authorization): {{ownership_confirmed}}
- Active locks checked (clone & workspace): {{locks_checked}}
- Cost & egress estimation acknowledged (if deep/multi-agent): {{cost_egress_ok}}

## 2. Selected Pipeline & Skills
- Entry route: {{entry_route}}
- Threat model (`sec-threat-model`): {{threat_model_status}}
- Scan (`sec-scan` / `sec-diff-scan`): {{scan_status}}
- Schema check (`python ../sec-scan/scripts/secfind.py validate findings.json coverage.json`): {{validator_exit}}
- Independent validation (`sec-validate`, different provider/model): {{validation_status}}
- Triage (`sec-triage`), Fix (`sec-fix`), Verification (`sec-verify-fix`): {{remediation_status}}

## 3. Non-Negotiable Invariants
- [ ] Secrets masked in every output, patch, and ticket
- [ ] `coverage.json` generated alongside `findings.json`
- [ ] Patches delivered as files unless commits explicitly authorized
- [ ] Public repos use private advisory drafts, never public bug issues for vulnerabilities
