# Multi-Agent Scheduler Prompts & Runtime Templates

Dieses Dokument enthält die standardisierten Prompt-Vorlagen für die verschiedenen LLM-Agenten-Umgebungen zur Ausführung des Community Outreach & Solution Recommender Skills (`v1.6.0`).

---

## 1. Antigravity Sidecar / Scheduled Task Prompt

- **Ablage:** `.gemini/config/sidecars/community-outreach/sidecar.json`
- **Verpflichtendes Modell:** `Gemini 4 Argon (High)` (`--model=pro`)
- **Standard-Frequenz:** `0 11 * * *` (1x täglich)

```text
Führe den 4-Phasen-Laufzyklus für Community Outreach & Repo Solution Recommender (v1.6.0) aus:

1. Lokales Monitoring-Inventar veröffentlichter History-Einträge; Plattformantworten nur mit getrenntem autorisiertem Inbound-Adapter abrufen
2. Lokale Vorprüfung freigegebener [x] Posts inkl. Claim-Beleg-Vertrag; ohne angebundenen Publisher bleibt der Status needs-action
3. Research-Auftrag für das nächste Kandidaten-Repo in usecases.json: Echten Quellcode lesen, Nachbarkommentare prüfen und Entwurf samt vollständigem JSON-Block "#### Claim-Beleg-Vertrag (Verifiziert):" erstellen
4. Pflicht-Gate vor Abschluss: python <workspace_path>/outreach_runner.py --workspace <workspace_path> --verify-proposals --repos-root <local_repos_root> --json (muss status == verified, failed_count == 0 liefern)
5. Cut & Clue Selbstarchivierung
```

---

## 2. Claude Code Automation Prompt

- **Aufruf:** Via CLI-Session, Cron-Job oder Loop-Runner (`claude --model opus -p "..."`)
- **Standard-Frequenz:** 1x täglich

```text
Lies ~/CLAUDE.md und öffne das Community Outreach Workspace unter <workspace_path>.

Führe den 4-Phasen-Zyklus aus:
1. Ermittle das lokale Monitoring-Inventar. Behaupte keine Prüfung externer Antworten, solange kein autorisierter Inbound-Adapter tatsächlich angebunden ist.
2. Prüfe POST-EINGANG.md auf freigegebene Einträge (- [x] Genehmigt). Eine Freigabe ist noch kein Veröffentlichungsbeleg. Übergib den Eintrag nur an einen ausdrücklich angebundenen Publisher, nachdem --verify-proposals inkl. Claim-Beleg-Vertrag grün ist, und ändere lokale Zustände ausschließlich nach einem vollständigen, zielgebundenen PublishReceipt.
3. Wähle das nächste fällige Repository aus usecases.json und recherchiere auf der nächsten Plattform (Reddit / YouTube / Fachforen) nach einer echten Problemanfrage (< 24 Monate alt), die das Tool löst.
4. Lies den echten Quellcode unter <local_repos_root>/<repo>, formuliere einen natürlichen Kommentar-Entwurf ohne KI-Formatierung und belege JEDE Software-Aussage im JSON-Block "#### Claim-Beleg-Vertrag (Verifiziert):" mit text_anchor, repo, file, lines und wortwörtlichem verbatim_code.
5. Verifiziere die Queue mit: python <workspace_path>/outreach_runner.py --workspace <workspace_path> --verify-proposals --repos-root <local_repos_root> --json.
```

---

## 3. Codex Automation Prompt

**Aufruf:** Via Codex Scheduled Task / Cron-Loop  
**Standard-Frequenz:** 1x täglich

```text
Execute Community Outreach cycle in workspace <workspace_path>:
Run `python <workspace_path>/outreach_runner.py --workspace <workspace_path> --full-run --json` and `python <workspace_path>/outreach_runner.py --workspace <workspace_path> --verify-proposals --repos-root <local_repos_root> --json`.
Treat `needs-action` as an expected hand-off state, never as publication success.
Every software claim in POST-EINGANG.md must carry a verified `#### Claim-Beleg-Vertrag (Verifiziert):` block backed by verbatim source code.
```

---

## 4. Leitplanken für alle Agenten

- **Keine eigenmächtige Veröffentlichung:** Nur Posts mit explizitem Häkchen `- [x] Genehmigt` dürfen online abgesetzt werden.
- **Claim-Beleg-Vertrag Pflicht (`v1.6.0`):** Jede Aussage über eigene Software muss mit `text_anchor`, `repo`, `file`, `lines` und wortwörtlichem `verbatim_code` belegt und per `--verify-proposals` verifiziert sein.
- **Kein Spamming:** Maximal 1 Veröffentlichungsversuch pro Laufzyklus (`max_posts_per_cycle: 1`).
- **Duplikatschutz:** Jede URL vor dem Entwurf gegen `POSTVERZEICHNIS.md` und `rejected_proposals.json` abgleichen.
- **Belegpflicht:** Ohne vollständigen `PublishReceipt` bleiben Queue, History, Rotation, Ausgang und Register unverändert.
- **Dry-Run:** `--dry-run` darf keinen Publisher aufrufen und weder Dateien noch Verzeichnisse verändern.
