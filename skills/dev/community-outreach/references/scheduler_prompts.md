# Multi-Agent Scheduler Prompts & Runtime Templates

Dieses Dokument enthält die standardisierten Prompt-Vorlagen für die verschiedenen LLM-Agenten-Umgebungen zur Ausführung des Community Outreach & Solution Recommender Skills.

---

## 1. Antigravity Sidecar / Scheduled Task Prompt

**Ablage:** `.gemini/config/sidecars/community-outreach/sidecar.json`  
**Empfohlenes Modell:** `gemini-2.5-flash` / `gpt-5.4`  
**Standard-Frequenz:** `0 10 * * *` (1x täglich) oder `0 8,12,16,20 * * *` (4x täglich)

```text
Führe den 4-Phasen-Laufzyklus für Community Outreach & Repo Solution Recommender aus:

1. Lokales Monitoring-Inventar veröffentlichter History-Einträge; Plattformantworten nur mit getrenntem autorisiertem Inbound-Adapter abrufen
2. Lokale Vorprüfung freigegebener [x] Posts; ohne angebundenen Publisher bleibt der Status needs-action
3. Research-Auftrag für das am weitesten zurückliegende Repo in USECASES.md / usecases.json
4. Cut & Clue Selbstarchivierung

Führe dazu aus:
python <workspace_path>/outreach_runner.py --workspace <workspace_path> --full-run --json

Dokumentiere das Ergebnis kurz im Session-Log.
```

---

## 2. Claude Code Automation Prompt

**Aufruf:** Via CLI-Session, Cron-Job oder Loop-Runner (`claude -p "..."`)  
**Standard-Frequenz:** 1x täglich

```text
Lies ~/CLAUDE.md und öffne das Community Outreach Workspace unter <workspace_path>.

Führe den 4-Phasen-Zyklus aus:
1. Ermittle das lokale Monitoring-Inventar. Behaupte keine Prüfung externer Antworten, solange kein autorisierter Inbound-Adapter tatsächlich angebunden ist.
2. Prüfe POST-EINGANG.md auf freigegebene Einträge (- [x] Genehmigt). Eine Freigabe ist noch kein Veröffentlichungsbeleg. Übergib den Eintrag nur an einen ausdrücklich angebundenen Publisher und ändere lokale Zustände ausschließlich nach einem vollständigen, zielgebundenen PublishReceipt.
3. Wähle das nächste fällige Repository aus usecases.json (Fair Round-Robin) und recherchiere auf der nächsten Plattform (Reddit / YouTube / Fachforen) nach einer echten Problemanfrage, die das Tool löst.
4. Formuliere einen hochwertigen, lösungsorientierten Antwortvorschlag und hänge ihn als "- [ ] Genehmigt" an POST-EINGANG.md an.
5. Führe bei Bedarf Cut-and-Clue Archivierung durch.
```

---

## 3. Codex Automation Prompt

**Aufruf:** Via Codex Scheduled Task / Cron-Loop  
**Standard-Frequenz:** 1x täglich

```text
Execute Community Outreach cycle in workspace <workspace_path>:
Run `python <workspace_path>/outreach_runner.py --workspace <workspace_path> --full-run --json`.
Treat `needs-action` as an expected hand-off state, never as publication success.
Verify integrity of USECASES.md, POST-EINGANG.md, and POSTVERZEICHNIS.md.
Report execution summary to .SYNC/automation-logging/.
```

---

## 4. Leitplanken für alle Agenten

- **Keine eigenmächtige Veröffentlichung:** Nur Posts mit explizitem Häkchen `- [x] Genehmigt` dürfen online abgesetzt werden.
- **Kein Spamming:** Maximal 1 Entwurf pro Lauf einstellen.
- **Duplikatschutz:** Jede URL vor dem Entwurf gegen `POSTVERZEICHNIS.md` abgleichen.
- **Belegpflicht:** Ohne vollständigen `PublishReceipt` bleiben Queue, History, Rotation, Ausgang und Register unverändert.
- **Dry-Run:** `--dry-run` darf keinen Publisher aufrufen und weder Dateien noch Verzeichnisse verändern.
