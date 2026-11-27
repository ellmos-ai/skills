# Worker Dispatch Contract — {{task_id}}

| Field | Specification |
|---|---|
| ID (`Kennung`) | {{task_id}} |
| Active Profile (`solo`/`spar`/`burst`) | {{profile}} (`operating_mode`: {{operating_mode}}) |
| Worker Model (explicit) | {{worker_model}} |
| Goal (`Ziel`) | {{goal}} |
| Inputs (`Eingaben`) | {{inputs}} |
| Positive Scope (`Du darfst`) | {{positive_scope}} |
| Negative Scope (`Du darfst nicht`) | {{negative_scope}} |
| Lock File Scope (partial, never global project lock) | {{lock_scope}} |
| Success Criterion (`Fertig, wenn`) | {{success_criterion}} |
| Expected Evidence (`Belege mit`) | {{evidence_required}} |
| Return Format (`Antworte als`) | {{return_format}} |

## Minimal Worker Prompt
```text
Auftrag: {{task_id}} — {{goal}}
Eingaben: {{inputs}}
Du darfst: {{positive_scope}}
Du darfst nicht: {{negative_scope}}
Fertig, wenn: {{success_criterion}}
Belege mit: {{evidence_required}}
Antworte als: {{return_format}}
```
