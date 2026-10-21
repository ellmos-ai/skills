# Integration

Der neutrale Kern benötigt Python 3.10 oder neuer und keine Pakete. Er startet keine Worker und ändert keine Ziele. Der Store unterstützt kooperierende Prozesse auf einem lokalen Dateisystem mit atomarem `O_EXCL` und `replace`.

Ein Hook darf die von seinem Host gelieferte `session_id` oder `thread_id` nutzen und den Stand als Kontext laden. Keine globale Ersatz-ID verwenden. Bei beschädigtem Store oder bestehender Schreibsperre den Fehler melden; keine fremde Sperre löschen.

Für Claude kann ein dünner Befehl `prios.md` diesen Skill mit `$ARGUMENTS` aufrufen. In Codex ist `$priorities` der Skillaufruf; ein Legacy-Prompt kann je nach Version als `/prompts:prios` erscheinen. Behaupte keinen universell unterstützten `/prios`-Alias.

Private Erweiterung: `config.json` im Deployment oder ein externes Nutzerprofil darf Speicherorte und bevorzugte Planungsskills enthalten. Der Kern bleibt identisch. Ein System ohne vertrauenswürdige Sitzungs-ID verwendet ausschließlich den aktuellen Gesprächskontext.
