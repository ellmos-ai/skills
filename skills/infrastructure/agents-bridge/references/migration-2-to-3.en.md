# Migrating agents-bridge 2.x to 3.0

Version 3 expands the boot-loader contract into a portable, reversible instance
package. The old read-only `discover --project` and `render --truth` commands
remain compatible, but do not create a v3 profile.

## Procedure

1. Run `discover --root <instance>` and resolve missing or conflicting
   authority explicitly. Add exactly one authority marker only after that
   decision.
2. Move the old truth-source list into
   `assets/bridge-profile.example.json`, then declare every provider surface
   and pointer edge. Select the primary deliberately; `CLAUDE.md` is not a
   default.
3. Declare the shared memory index and separate silos with ownership, access,
   refresh, and merge rules. Do not combine existing silos.
4. Declare relative messenger, presence, and lock roots plus privacy includes
   and excludes.
5. Validate and capture into a new package first. Keep real personal content
   local; publish only synthetic or redacted fixtures.
6. Run doctor and plan, restore to an empty target, verify, repeat the restore
   for idempotence, and test rollback.
7. Replace installed copies through the normal skill distribution path only
   after the canonical release is green.

## Breaking changes

- The profile schema is `agents-bridge.profile.v3`.
- Absolute profile paths and non-UTF-8 content are invalid.
- Exactly one provider surface must represent the primary.
- Projections require provenance and hashes; an unmarked copy is not valid.
- Restore mutation requires explicit `--apply --yes`, a backup directory, and
  a receipt path.
