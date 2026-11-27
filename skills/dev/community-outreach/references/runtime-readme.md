# Community Outreach – Runtime

Diese Runtime verwaltet eine Human-in-the-Loop-Queue für lösungsorientierte Community-Beiträge. Sie trennt Planung, deterministische Originalcode-Vertragsprüfung, natürlichen Stil-Check, ausdrückliche Freigabe, externe Veröffentlichung und lokale Verbuchung strikt voneinander.

## Sicherheitsvertrag (`v1.6.0`)

- `- [x] Genehmigt` erlaubt einen Veröffentlichungsversuch, belegt aber noch keine Veröffentlichung.
- **Deterministischer Claim-Beleg-Vertrag (`#### Claim-Beleg-Vertrag (Verifiziert):`, Pflicht seit `v1.6.0` / 2026-11-13):**
  - Reine Dateinamen-Listen reichen nicht aus, weil existierende Dateien auch unbelegte Textaussagen begleiten könnten. Jeder Vorschlag in `POST-EINGANG.md` muss neben `- **Code-Beleg (Verifiziert):**` einen gefencten JSON-Block `#### Claim-Beleg-Vertrag (Verifiziert):` führen, der **jede** Aussage über unsere Software im `Textvorschlag` mit `text_anchor`, `repo`, `file`, `lines` (max. 80 Zeilen Spanne) und wortwörtlichem `verbatim_code` belegt.
  - `_verify_claim_contract()` prüft in `--verify-proposals`, `preview_post` und `phase2_outbound_execution`:
    1. Gültiges JSON-Schema und zulässiges Zeilenfenster (`<= 80` Zeilen).
    2. Exakte Teilstring-Übereinstimmung jedes `text_anchor` im `Textvorschlag` (`anchor-not-in-text`).
    3. Existenz und Path-Traversal-Freiheit der Datei unter `<local_repos_root>/<repo>`, Tracking in `git ls-files` (sofern `.git` existiert; verhindert Belege aus ungetrackten lokalen Dateien) sowie mindestens eine echte Quellcode-Datei bei Nicht-Skill-Repos (`code-file-required`).
    4. Wortwörtliche Übereinstimmung von `verbatim_code` im angegebenen Zeilenfenster des echten Quellcodes (`verbatim-code-mismatch`).
    5. Vollständige Satz- und Dateinamen-Abdeckung aller Software-Aussagesätze im `Textvorschlag` (`uncovered-software-sentence`, `unverified-mentioned-file`).
    6. Cross-Repo-Nachweis für jedes im selben Kommentar mitgenannte Schwester-Repo aus dem Katalog (`unverified-sister-repo`).
    7. Manifest-Widerspruchsschutz für `zero-dependency` / `stdlib-only`: Liest `pyproject.toml` bzw. `package.json` aus und blockiert bei vorhandenen Laufzeit-Abhängigkeiten (`predicate-contradiction:zero-dependency`) oder fehlendem Manifest-Beleg (`missing-manifest-proof:zero-dependency`).
  - Ist `compliance.require_claim_contract: true` in `config.json` gesetzt, verweigern `verify_proposals`, `preview_post` und `phase2_outbound_execution` jeden Vorschlag ohne gültigen `Claim-Beleg-Vertrag` (`missing-claim-contract` / `invalid-claim-contract`).
- **Code-Fact Verification Gate (Pflicht seit 2026-11-02):** Jeder Entwurf muss zusätzlich das Übersichts-Feld `- **Code-Beleg (Verifiziert):**` mit real existierenden Quellcode-Dateien (in Backticks) enthalten (`missing-code-evidence` bei Fehlen).
- **Natural Human Style & Anti-AI-Pattern Gate (Pflicht seit 2026-11-03):** Jeder Entwurf muss sich in Länge (1–3 kurze Absätze, 250–850 Zeichen, max. 1.200 Zeichen auf Reddit/YouTube) und Tonfall an die umgebenden Kommentare im Ziel-Thread anpassen (`- **Umgebungs-Check (Ton & Länge):**`). `_check_natural_human_style()` blockiert Markdown-Überschriften (`###`), Fettdruck (`**...**`), Geviertstriche (`—`), strukturierte Aufzählungslisten (3+ Punkte) und KI-Floskeln (`reason: "ai-style-violation"`).
- **Blacklist- & Organisations-Gate (`rejected_proposals.json`, `BLACKLIST.md` & `config.json`):** Abgelehnte Vorschläge, gesperrte Plattformen (`dev.to`) und dauerhaft ausgeschlossene Organisationen (`biotec-line`, rechtlicher Ausschluss gegen Verbreitungsrisiko) werden technisch blockiert (`status: "blacklisted"` / `excluded_org: true`).
- **Organisations-Fokus & Forschungs-Diskurs (`primary_orgs` & `discourse_only_orgs`, Pflicht seit 2026-11-09):** Regulärer Tool-/Lösungs-Outreach konzentriert sich primär auf `ellmos-ai` und die Open-Bricks-Organisationen (`dev-bricks`, `file-bricks`, `doc-bricks`, `open-bricks`). Repositories unter `research-line` (`discourse_only_orgs`) laufen im Modus `discourse_positioning` für sachlichen wissenschaftlichen Fachdiskurs.
- **3-Stufiges Qualitäts- & Aufmerksamkeits-Auswahlmodell (`selection_tier` 1 → 2 → 3):**
  1. **Stufe 1 (`selection_tier = 1`):** Beste Modul-Repos nach Qualität und eigenständiger Idee mit wenig bis mittlerer menschlicher Aufmerksamkeit (`views_unique_14d <= 6` und unbeworben), ergänzt um die Kern-Flaggschiffe (`ellmos-ai/bach`, `ellmos-ai/open-ocean`, `ellmos-ai/skills`) sowie 17 besondere Einzel-Skills (`SPECIFIC_SKILL_PROFILES`).
  2. **Stufe 2 (`selection_tier = 2`):** Starke Modul-Repos nach Qualität und Idee (`TOP_QUALITY_MODULE_SCORES`), die bereits höhere Aufmerksamkeit (`views_unique_14d > 6` oder frühere Promotionen) haben.
  3. **Stufe 3 (`selection_tier = 3`):** Weitere kleinere Repos, Spezialmodule, Seeds und Helper-Tools.
- **Modell-Pflicht:** Entwürfe und Code-Verifikationen dürfen ausschließlich von `Gemini 4 Argon (High)` (`--model=pro`) oder gleichwertigen `thinker_reviewer`-Modellen erstellt werden (keine Flash-/Haiku-Modelle).
- Der mitgelieferte Runner führt selbst keine Browser-, Login- oder Plattformaktion aus. Nur ein angebundener Publisher darf einen Beitrag senden, und erst ein vollständiger `PublishReceipt` verändert History, Rotation, `POST-AUSGANG.md` und `POSTVERZEICHNIS.md`.
- Ein `--dry-run` ruft keinen Publisher auf, verändert keine Datei und legt kein Verzeichnis an.

## Dateien

| Datei | Funktion |
| :--- | :--- |
| `outreach_runner.py` | Dünner, portabler CLI-Adapter |
| `outreach_engine.py` | Aus dem kanonischen Skill projizierter Core inkl. `_verify_claim_contract` |
| `usecases.json` | Repositories und Rotationsstand |
| `POST-EINGANG.md` | Freigabe-Queue mit `- **Code-Beleg:**`, `#### Claim-Beleg-Vertrag (Verifiziert):` und natürlichem Kommentar-Stil je Vorschlag |
| `BLACKLIST.md` | Menschenlesbares Sperrregister abgelehnter Vorschläge und Plattformen |
| `rejected_proposals.json` | Maschinenlesbare Sperrliste für URLs, Proposal-IDs, Repos und Plattformen |
| `config.json` | Instanz-Konfiguration (`require_code_evidence`, `require_claim_contract`, `require_natural_style`, `local_repos_root`, `excluded_platforms`) |
| `posts_history.json` | Maschinenlesbare, Receipt-gebundene Veröffentlichungshistorie |
| `POST-AUSGANG.md` | Nach verifiziertem Receipt erzeugte lesbare Ausgangsansicht |
| `POSTVERZEICHNIS.md` | Aus der History erzeugtes Verzeichnis: veröffentlichte (mit Beleg) und unbestätigte Beiträge, Queue-Zähler |
| `_archive/` | Älteste vollständige Ausgangseinträge; die neuesten bleiben live |
| `_archive/POSTVERZEICHNIS_ARCHIV_v<n>.md` | Cut-and-Clue-Archiv des Verzeichnisses (je 150 Veröffentlichungen, Pointer auf Vorläufer und Nachfolger) |
| `githubbot_bridge.py` | Übernimmt Sichtbarkeit und 14-Tage-Traffic aus GitHubBot (`--sync-githubbot`) |

`outreach_engine.py`, `outreach_runner.py` und `githubbot_bridge.py` werden gemeinsam aus dem kanonischen Skill-Verzeichnis mit `python scripts/deploy_runtime.py --target <runtime-verzeichnis> --json` projiziert (`--check` vergleicht alle fünf Runtime-Dateien bytegenau und schreibt nichts).

## CLI

```powershell
# Schreibfreier Planlauf mit maschinenlesbarer Ausgabe
python outreach_runner.py --workspace . --full-run --dry-run --json

# Alle Vorschläge in POST-EINGANG.md gegen Blacklist, Duplikate, Originalcode-Vertrag und natürlichen Stil prüfen
python outreach_runner.py --workspace . --verify-proposals --repos-root <local_repos_root> --json

# Freigaben lokal prüfen; ohne angebundenen Publisher bleibt needs-action bestehen
python outreach_runner.py --workspace . --process-approvals --json

# Nächstes Repo und den offenen Rechercheauftrag anzeigen
python outreach_runner.py --workspace . --discover-candidate --json

# Alte vollständige Ausgangseinträge archivieren
python outreach_runner.py --workspace . --archive --json

# Verzeichnis und Archive aus der History neu erzeugen (mit --dry-run nur anzeigen)
python outreach_runner.py --workspace . --rebuild-registry --json

# Sichtbarkeit und Traffic aus GitHubBot übernehmen (Fehler: Exitcode 1, nichts geändert)
python outreach_runner.py --workspace . --sync-githubbot --json
```
