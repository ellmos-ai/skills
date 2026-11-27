# Piggyback Hosting Deployment Audit — {{app_name}} ({{date}})

> Templates: `references/DATA-FLOW-TEMPLATE.md` · `references/PRIVACY-TEMPLATE.md` · Legal guide: `references/RECHT.md`

## 1. Mode Selection (`local` default)
- Target mode (`local` | `huckepack-gift` | `huckepack-only-host` | `pay-membership` stub): {{mode}}
- Verifiable mode endpoint (if hosted): {{mode_endpoint}}

## 2. Storage & Key Isolation Checklist
- [ ] Data-flow table filled with `file:line` evidence (or honest `"not found"`)
- [ ] Storage adapter routes visitor data to browser (`sqlite_wasm_opfs` / `indexeddb`), zero shared server DB state
- [ ] BYOK key field masked and verified unlogged in `huckepack-only-host`
- [ ] User-controlled Export & Import wired and tested (mandatory for ephemeral browser storage)

## 3. GDPR / TDDDG / UWG Gate (Non-Legal-Advice Summary)
- Controller status (GDPR Art. 4(7) / ECJ C-683/21): {{controller_analysis}}
- Third parties contacted on visitor behalf (GDPR Art. 14 / DPA): {{third_party_contacts}}
- Privacy template markers `[REPLACE: ...]` completed & case-specific legal review planned: {{legal_review_status}}
