# Community Outreach – Runtime

Diese Runtime verwaltet eine Human-in-the-Loop-Queue für lösungsorientierte Community-Beiträge. Sie trennt Planung, ausdrückliche Freigabe, externe Veröffentlichung und lokale Verbuchung strikt voneinander.

## Sicherheitsvertrag

- `- [x] Genehmigt` erlaubt einen Veröffentlichungsversuch, belegt aber noch keine Veröffentlichung.
- Der mitgelieferte Runner führt selbst keine Browser-, Login- oder Plattformaktion aus.
- Nur ein angebundener Publisher darf einen Beitrag senden. Erst ein vollständiger, auf Plattform und Ziel-URL gebundener `PublishReceipt` darf History, Rotation, `POST-AUSGANG.md` und `POSTVERZEICHNIS.md` verändern.
- Doppelte Ziel-URLs werden vor dem Publisher-Aufruf exakt und plattformspezifisch erkannt. Ähnliche, aber andere URLs bleiben unterscheidbar.
- Historische `published`-Behauptungen ohne Receipt bleiben aus Sicherheitsgründen als konservative Duplikatsperre erhalten, erscheinen aber nicht als verifizierte Veröffentlichung im neu erzeugten Register.
- Ein `--dry-run` ruft keinen Publisher auf, verändert keine Datei und legt kein Verzeichnis an.
- Phase 3 erzeugt keine Platzhalter-URL. Sie liefert `needs-action`, bis eine getrennte Recherche einen echten, aktuellen, regelkonformen und noch unbenutzten Ziel-Thread samt geprüftem Entwurf in `POST-EINGANG.md` abgelegt hat.
- Phase 1 zählt nur das lokale Monitoring-Inventar. Externe Antworten werden ohne getrennten autorisierten Inbound-Adapter nicht abgerufen.

## Dateien

| Datei | Funktion |
| :--- | :--- |
| `outreach_runner.py` | Dünner, portabler CLI-Adapter |
| `outreach_engine.py` | Aus dem kanonischen Skill projizierter Core |
| `usecases.json` | Repositories und Rotationsstand |
| `POST-EINGANG.md` | Freigabe-Queue; offene oder unbelegte Einträge bleiben erhalten |
| `posts_history.json` | Maschinenlesbare, Receipt-gebundene Veröffentlichungshistorie |
| `POST-AUSGANG.md` | Nach verifiziertem Receipt erzeugte lesbare Ausgangsansicht |
| `POSTVERZEICHNIS.md` | Aus der History abgeleiteter Duplikatindex |
| `_archive/` | Älteste vollständige Ausgangseinträge; die neuesten bleiben live |

`outreach_engine.py` und `outreach_runner.py` werden gemeinsam aus dem kanonischen Skill-Verzeichnis projiziert. Der Runner verwendet ausschließlich den Core im selben Verzeichnis; er enthält keine hostabhängigen Pfade.

Die Projektion erfolgt aus dem Skill-Verzeichnis mit `python scripts/deploy_runtime.py --target <runtime-verzeichnis> --json`. Der Prüflauf mit `--check` vergleicht alle vier Runtime-Dateien bytegenau und schreibt nichts. Daten- und Queue-Dateien gehören nicht zum Deploy-Set.

## CLI

```powershell
# Schreibfreier Planlauf mit maschinenlesbarer Ausgabe
python outreach_runner.py --workspace . --full-run --dry-run --json

# Freigaben lokal prüfen; ohne angebundenen Publisher bleibt needs-action bestehen
python outreach_runner.py --workspace . --process-approvals --json

# Nächstes Repo und den offenen Rechercheauftrag anzeigen
python outreach_runner.py --workspace . --discover-candidate --json

# Alte vollständige Ausgangseinträge archivieren
python outreach_runner.py --workspace . --archive --json
```

Unterstützte Scheduler-Helfer sind Antigravity Sidecar, Windows Task Scheduler und Unix-Cron. Ein Scheduler-Aufruf ist kein Publisher und darf `needs-action` nicht als Erfolg einer Außenveröffentlichung ausgeben.
