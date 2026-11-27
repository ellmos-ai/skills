# After-Care Run Report — {{repo}} ({{date}})

> Tier: `{{tier}}` (`surface` | `full`)

## 1. Distribution Surfaces
- Target surfaces: {{surfaces}}
- Topics / homepage / description verified: {{topics_status}}

## 2. Privacy & Tracked Artifacts Gate
- Tracked files scanned (`git ls-files`): {{privacy_status}}
- Internal artifacts moved to `.gitignore` / untracked: {{removed_artifacts}}
- Force-push / secret rotation needed: {{secret_rotation_needed}}

## 3. Documentation & Language Parity
- README version & claims matched against code: {{version_parity}}
- Banners checked (`1200x300`): {{banner_status}}
- Standard languages (`de`, `en`, `es`, `zh`, `ja`, `ru`): {{language_decisions}}

## 4. Issues, PRs & Surface Parity
- Issues / PRs triaged: {{issues_prs_summary}}
- Registry / org profile / downstream parity: {{parity_status}}

## 5. Open Findings Turned Into Project Tasks
{{open_tasks}}
