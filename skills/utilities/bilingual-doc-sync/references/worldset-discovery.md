# Incremental World Set discovery

`scripts/worldset_discovery.py` is an offline intake adapter for the existing
World Set executor. It does not own execution states, worker leases, provider
receipts or approvals. Repeated scans retain the same source/language/hash IDs;
the native executor and its receipts remain responsible for deduplication before
any model call. No model, network request, translation application or publication
is started by discovery.

The adapter detects new registered projects, bounded filesystem project discovery,
new skills, changed English/German source documents, missing or stale editions,
and locale fields in the existing localized-map, typed entries-list and BACH
namespace-map formats. Source/target paths, hashes and field pointers stay bound.
JSON candidates require the project's field-transport adapter; they cannot be
passed to the Markdown apply command.

## Source and exclusion rules

- Explicit source-language configuration or EN/DE metadata is required. Unknown
  leading languages produce a review item with protected chunks, not guessed jobs.
- `.USR`, `.USER`, their named variants, `_USR`, `_USER`, archive directories,
  `ARC_` projects and explicit archived registry/skill statuses are excluded.
  Exclusion is checked before reading their source files. A normal `Users/User`
  home-directory name is not a private-project marker.
- Private metadata, missing skill visibility and `public potential` are withheld
  by default. A reviewed `source_visibility: public` scope can classify otherwise
  unmarked skills; explicit private metadata still wins. An explicit
  `allow_private: true` project keeps private candidates private and does not
  authorize publication or bypass user/archive exclusions.
- Existing nested skill locale conventions are retained. Translated editions do
  not become sources accidentally.
- An edited EN/DE secondary edition stays on hold across subsequent scans.
  A repeat scan is not a reverse-transfer review. Markdown conflicts can be
  resolved with an exact-source/target-hash `source_reviews` evidence entry;
  catalogue conflicts currently require an explicit operator rebaseline after
  semantic reconciliation.
- Legacy translations without source provenance remain review candidates. Their
  existence does not establish freshness or authorize overwriting them.
- Code and structural blocks use the existing `worldset.protect` contract.
  Paragraph chunks use `worldset_segments.fragments`, without overlapping text;
  concatenation reconstructs the exact protected source. RAG overlap would duplicate
  translated prose and is deliberately not used for translation reassembly.
- Unreadable, oversized, linked, secret-bearing or offline Windows cloud files
  produce attention records. No broad hydration or pinning is performed.
- Transient read/schema failures retain the last stable hash baseline. Incomplete
  directory discovery aborts before publishing a replacement snapshot. Removed or
  excluded source references retain historical hashes, never automatic cancellation.

## Private runtime configuration

Keep this configuration and output outside public repositories. Paths below are
placeholders relative to the invocation directory, not deployment defaults.

```json
{
  "projects": [
    {"id": "application", "root": "project-a", "kind": "readme", "source_language": "en", "stars": 4, "views": 9},
    {"id": "skills", "root": "skill-repo", "kind": "skills"},
    {"id": "bach", "root": "bach-repo", "source_language": "en", "catalogs": [
      {"path": "system/exports/translations/locales/de.json", "shape": "namespace-map", "source_language": "de"}
    ]}
  ],
  "registries": [{"path": "software/releases.json"}],
  "discovery_roots": [{"id": "software", "root": "software", "depth": 2, "min_project_depth": 2}],
  "chunk_characters": 6000
}
```

Registry ingestion reads only name/path/lifecycle/status/business-class/visibility fields.
Do not pass raw repository metadata or temporary clone tokens. Missing popularity
metrics stay `null`; they are not converted to zero. Explicit project overrides
win over registry and filesystem discovery. Conflicting explicit languages fail.
Registries cannot point outside their own collection. Their eligibility hash is
revalidated at export, so a project archived after a scan requires a new scan.
Discovery roots are collections by default (`min_project_depth: 1`); configure
depth 2 for category/project layouts. A matched project is not recursively treated
as a collection of new projects inside its docs or dependencies.

## Scan and take small packages

```sh
# Read-only summary; no output written.
python -B scripts/worldset_discovery.py --config runtime/config.json

# Persist a snapshot under the existing native own-fence writer contract.
python -B scripts/worldset_discovery.py --config runtime/config.json \
  --previous runtime/discovery.json --out runtime/discovery.json \
  --checker lock_scan.py --fence-file runtime/LOCK.txt --fence OWN_FENCE --owner OPERATOR

# Export at most twenty FR/HI document jobs to the existing native executor format.
python -B scripts/worldset_discovery.py --input runtime/discovery.json \
  --policy-config runtime/config.json --project application --languages fr,hi --limit 20 --out runtime/package.json \
  --checker lock_scan.py --fence-file runtime/LOCK.txt --fence OWN_FENCE --owner OPERATOR
```

Writer checks keep the complete native `--check-dir` readback for the output
directory, including descendant locks, registered twins, and hook guards. They
also ask the installed `lock_utils.active_locks_for_path()` for the exact output
file and each mapped twin target. A lock scoped only to a sibling file neither
blocks nor satisfies the output fence; the writer's own fence must protect the
exact output path. The collector keeps its whole-runtime claim and checks the
specific snapshot or receipt path immediately before publishing it.

Selection re-reads current source and target hashes. Stale snapshots cannot silently
overwrite intervening work. The native executor still requires its own source,
privacy, budget, lock, technical QA and independent semantic-review gates. A native
structure/script pass is insufficient: exact copied source prose and language
residues need separate review; legitimate shared words need field-bound reasons.

## Recurring operation

Use the existing pipeline-2k runtime, preferably on the central host, to invoke
the collector after registry/source changes or on a bounded periodic check.
The deployment wrapper owns one narrow output lock and records the invocation,
exit status and counts. It must retain the last successful snapshot on failure,
avoid overlapping runs, skip missing source volumes and leave executor receipts
untouched. This module does not install a schedule or claim that a deployed worker
exists. Document actual installation and a second-run readback in the private
pipeline workspace before reporting automation as active.

`scripts/worldset_collector.py` supplies one guarded pass for that scheduler:

```sh
python -B scripts/worldset_collector.py --config private/config.json \
  --runtime private/intake --lock-tools installed/native-lock-tools
```

The configuration and runtime directory must already exist, outside source projects.
`required_roots` is an optional list of mounted source directories; a missing root
skips collection without replacing the last successful snapshot. Explicit eligible
project roots and discovery roots must also exist. Native lock tools are an
explicit installed dependency, never a bundled or weakened lock implementation.
The runner claims only its runtime and publishes a content-addressed
`discovery-<sha256>.json` snapshot before atomically updating `last-success.json`.
That receipt points to the authoritative snapshot. Foreign claims are skipped;
expired existing claims stay for operator inspection after the original process is
proven terminal.

The host scheduler must ignore overlapping instances and impose a run time below
the thirty-minute claim lifetime. Retain the last snapshot on scan failure, record
the scheduler exit status, and do not attach provider or translation-application
commands. Install a new schedule only after two successful native runs and a fresh
independent runner review. This reference does not assert a deployed schedule.

Visibility is required for README and catalogue sources as well as skills. Missing
or unknown visibility is held for review; successful parsing and an EN/DE source
declaration do not establish that a project is public. Configure a reviewed public
project or collection scope, or use a public registry entry. Catalogue `_meta`
fields are skipped as metadata; visibility is honored only when explicitly declared.

The collector writes an immutable content-addressed snapshot and updates its
last-success receipt last. The receipt names the authoritative snapshot. If the
receipt write fails, the previous receipt and snapshot remain valid. The runner
rechecks eligible README/SKILL paths and configured catalogue files after scanning;
a changed inventory preserves the prior receipt. It binds its lock to the fence
returned by the native lock creator.
