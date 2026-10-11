# Preflight: Gardener and Memory Query

Use memory to recover relevant prior context without treating it as current truth.

1. Extract a few distinctive terms from the task, repository, component, and reported symptom.
2. Query the configured Gardener or memory interface with those terms. Prefer a narrow search over a broad dump.
3. Record the returned source, date, and provenance. Distinguish a memory note from a live repository file, test, lock, or user decision.
4. Verify drift-prone details against their current source before relying on them. A missing result is not proof that no rule or prior work exists.
5. If the memory service is unavailable or returns no useful result, continue with targeted repository and filesystem searches. State the fallback only when it affects the conclusion.
6. Retrieve only the context needed for the task. Do not expose secrets or send private memory content to an external service.
