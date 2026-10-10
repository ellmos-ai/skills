# Workflow, Lock, and Git Hygiene

Keep the change within the requested scope and preserve work already present in the checkout.

1. Before editing, inspect the branch, working-tree status, and diff. Identify pre-existing edits and untracked files; do not overwrite, stage, or discard them unless the task explicitly includes them.
2. Check the applicable project lock before every write, commit, or push. Treat an unknown or conflicting lock state as blocked. For non-trivial work, acquire a scoped lock when the local lock policy requires one and verify its fencing grant before writing.
3. Keep one writer per file. Make changes only in the declared scope; add generated outputs only when the task and repository rules require them.
4. Before committing, review the complete diff and stage only files owned by this task. Never use reset, clean, force-push, or broad restore commands to make the tree look clean.
5. Run the requested validation commands and report their exact outcomes. Separate validation of this change from any unrelated pre-existing work.
6. Commit or publish only when the task and applicable repository policy authorize that action. Release only locks acquired by the current run.
