# Path Validation and Source Authority

Validate paths and evidence before reading, linking, or writing files.

1. Resolve each relative link against the file that contains it, not against an assumed user directory or shell working directory.
2. Confirm that repository links point to tracked or intentionally added files in the current checkout. Do not use placeholder home directories as if they were portable targets.
3. Treat home-relative locations as optional runtime configuration. Document the default and the configuration key; never publish a concrete person's home path or host name.
4. Prefer current explicit user instructions and task constraints, followed by applicable project rules, current repository files, and live command output. Memory is useful for discovery but does not override current evidence.
5. When evidence conflicts, preserve the original sources, identify which source controls the decision, and avoid silently rewriting unrelated files.
6. Before a write, confirm that the resolved destination is inside the authorized scope. Report ambiguity instead of guessing.
