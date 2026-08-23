# Multi-Agent Scheduler Prompts & Runtime Templates

Dieses Dokument enthält die standardisierten Prompt-Vorlagen für die verschiedenen LLM-Agenten-Umgebungen zur Ausführung des Community Outreach & Solution Recommender Skills.

---

## 1. Antigravity Sidecar / Scheduled Task Prompt

**Ablage:** `.gemini/config/sidecars/community-outreach/sidecar.json`  
**Empfohlenes Modell:** `gemini-2.5-flash` / `gpt-5.4`  
**Standard-Frequenz:** `0 10 * * *` (1x täglich) oder `0 8,12,16,20 * * *` (4x täglich)

```text
Führe den 4-Phasen-Laufzyklus für Community Outreach & Repo Solution Recommender aus:

1. Inbound Check auf Community-Feedback in POST-AUSGANG.md
2. Outbound Execution für freigegebene [x] Posts in POST-EINGANG.md
3. Research & Staging für das am weitesten zurückliegende Repo in USECASES.md / usecases.json
4. Cut & Clue Selbstarchivierung

Führe dazu aus:
python <workspace_path>/scripts/outreach_engine.py --workspace <workspace_path> --full-run

Dokumentiere das Ergebnis kurz im Session-Log.
```

---

## 2. Claude Code Automation Prompt

**Aufruf:** Via CLI-Session, Cron-Job oder Loop-Runner (`claude -p "..."`)  
**Standard-Frequenz:** 1x täglich

```text
Lies ~/CLAUDE.md und öffne das Community Outreach Workspace unter <workspace_path>.

Führe den 4-Phasen-Zyklus aus:
1. Prüfe POST-AUSGANG.md auf Inbound-Diskussionen.
2. Prüfe POST-EINGANG.md auf freigegebene Einträge (- [x] Genehmigt). Wenn vorhanden, setze diese über den autorisierten Browser ab, verschiebe sie nach POST-AUSGANG.md und trage die Ziel-URL in POSTVERZEICHNIS.md ein.
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
Run `python scripts/outreach_engine.py --workspace <workspace_path> --full-run`
Verify integrity of USECASES.md, POST-EINGANG.md, and POSTVERZEICHNIS.md.
Report execution summary to .SYNC/automation-logging/.
```

---

## 4. Leitplanken für alle Agenten

- **Keine eigenmächtige Veröffentlichung:** Nur Posts mit explizitem Häkchen `- [x] Genehmigt` dürfen online abgesetzt werden.
- **Kein Spamming:** Maximal 1 Entwurf pro Lauf einstellen.
- **Duplikatschutz:** Jede URL vor dem Entwurf gegen `POSTVERZEICHNIS.md` abgleichen.
