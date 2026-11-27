# Lernvertrag, Usecase-Abdeckung und Verbesserungspfade

Ergänzung von 2026-08-24 (Ticket T-20260824-218233618, Nachtrag): die ellmos-Regeln
sollen ein **wiederverwendbares Muster je erzeugtem Skill** werden, nicht nur einmalig
für diesen Skill selbst gelten. Bevor etwas Neues erfunden wurde, wurde geprüft, ob es
bereits etabliert ist — Ergebnis unten.

## Recherche: was existiert schon?

- **Intern, bereits installiert:** `skill-creator` (Anthropic) definiert bereits
  `evals/evals.json` (`skill_name`, `evals[].{id, prompt, expected_output, files,
  expectations}`) und `grading.json` (`expectations[].{text, passed, evidence}`,
  `summary.pass_rate`, `eval_feedback.suggestions`). Das ist **fast genau** die
  "Usecase-Sammlung + Abdeckungsgrad", nur aus Sicht des Skill-**Autors**, nicht des
  Nutzers. Nachbau vermieden — die neuen Dateien unten sind **formgleich**, damit
  dieselbe Eval-/Grading-Maschinerie später auch darüber laufen kann.
- **Extern, etabliert:** Das A2A-Protokoll (Agent2Agent, Google) definiert
  `AgentSkill` als Capability-Manifest-Schema: `id`, `name`, `description`, `tags`,
  optional `examples`. Für die Anbieter-/Fähigkeiten-Kataloge unten übernommen
  (`known-providers-and-abilities.json`), statt eigenes Vokabular zu erfinden.
- **Extern, akademisch, kein fertiges Schema:** "Skill Coverage: A Test Adequacy
  Metric for Agent Skills" (arXiv 2606.20659, 2026) — bestätigt, dass Coverage-Metrik
  für Agent-Skills ein aktives Forschungsfeld ist, liefert aber kein übernehmbares
  JSON-Schema. Zur Kenntnis genommen, nicht integriert (kein Overengineering für ein
  noch nicht konsolidiertes Forschungsergebnis).
- **Für Lücken-/Verbesserungspfad-Analyse ("wie schließe ich die Lücke") existiert
  kein fertiger externer Standard** — dafür ist unten ein eigenes, schlankes
  Haus-Schema entstanden (`gap-closing-analysis.json`), bewusst **schmal** geschnitten
  (nur strukturelle Schließungswege, keine Duplikate von `grading.json.eval_feedback`).

## grounding-seed: geprüft, keine Codeänderung nötig

`grounding-seed` wurde geprüft (README, alle Module: `self_knowledge.py`,
`location.py`, `store.py`, `scan.py`, `migration.py`, `transplant.py`). Ergebnis:
**keine Erweiterung nötig**, aus zwei Gründen:

1. **Falsche Formpassung.** `LocalStore`/`RoleEntry` ist strukturell auf "eine Rolle
   → eine aufgelöste Quelle" zugeschnitten (`rolle, aktiv, quelle, stufe,
   bestaetigt_am, herkunft`). Usecase-Listen, Coverage-Lücken, Anbieter-Kataloge und
   Verbesserungsvorschläge sind strukturell etwas anderes (Listen strukturierter
   Einträge mit eigenen Feldern) — sie in `RoleEntry` zu pressen wäre die Form
   verbiegen, nicht wiederverwenden.
2. **Bewusste Scope-Disziplin des Moduls selbst.** `grounding-seed`s eigenes README
   listet unter "Was hier bewusst fehlt" bereits mehrere angrenzende Wünsche, die
   **explizit abgelehnt** wurden (Ressourcen-Erreichbarkeits-Checks, echte
   Migrations-Ziel-Adapter, der `work-autonomous`-Retrofit als **eigenes**
   Folge-Ticket statt Teil dieses Repos). Usecase-Coverage/Lernvertrag folgt
   demselben Muster: ein neues, eigenständiges Anliegen, kein Nachrüsten des
   bestehenden.

**Einzige Stelle, an der `grounding-seed` weiterhin genutzt wird:** `connections.json`
(unverändert aus v0.1.0 — die tatsächlich aufgelösten externen Andockstellen) und
`grounding_seed.scan.scan_resources()` zur Prüfung, ob ein bekannter Anbieter
installiert ist (Feld `installiert` in `known-providers-and-abilities.json`).

Damit ist der Prüfauftrag "Anpassungen an grounding-seed nötig?" mit **Nein,
begründet** beantwortet — kein Folgeticket dafür nötig.

## Das Dateiset (final, gegenüber dem Vorschlag reduziert)

Der ursprüngliche 7-Dateien-Vorschlag wurde geprüft und auf **6 Dateien** verdichtet:
`skill-usecases.json` entfällt als eigene Datei — diese Rolle übernimmt bereits
`evals/evals.json` (siehe oben), und der Verhaltenscodex wandert als Objekt in
`config.json` statt eine siebte Datei zu werden (config.json ist per Definition
bereits "skill-eigene Verhaltens-Einstellungen" — ein Lernvertrag ist genau das).

| Datei | Rolle | Neu oder wiederverwendet |
|---|---|---|
| `evals/evals.json` | Vom Skill-Autor entworfene Testfälle | **wiederverwendet** (skill-creator-Standard) |
| `user-usecases.json` | Vom Nutzer tatsächlich vorgebrachte Anwendungsfälle | neu, formgleich zu `evals.json` |
| `usecase-gaps.json` | Abgleich: welche Nutzer-Usecases sind ungetestet/ungedeckt | neu, referenziert statt kopiert |
| `known-providers-and-abilities.json` | Kandidatenraum: bekannte Anbieter je Rolle (SOTA/Ersatz/ellmos) | neu, Felder an A2A `AgentSkill` angelehnt |
| `gap-closing-analysis.json` | Strukturelle Schließungswege je Lücke | neu, schmal geschnitten |
| `connections.json` | Tatsächlich aufgelöste externe Andockstellen | unverändert (grounding-seed `LocalStore`) |
| `config.json` (Feld `lernvertrag`) | Verhaltenscodex: beste Option wählen, User als König, nie selbständig installieren | Erweiterung der bestehenden Datei, keine neue |

Schemas: `.SKILLS/schemas/user-usecases-v1.schema.json`,
`usecase-gaps-v1.schema.json`, `known-providers-v1.schema.json`,
`gap-closing-analysis-v1.schema.json` — dieselbe Haus-Konvention wie
`skill-v1.schema.json` etc., keine Parallelstruktur.

## Wie der Kreis sich schließt (Lernschleife im Dateisystem)

```
user-usecases.json  --(Abgleich gegen evals.json + grading.json)-->  usecase-gaps.json
usecase-gaps.json    --(je Lücke: wie schließen?)-->                  gap-closing-analysis.json
gap-closing-analysis.json --(Anbieterfrage?)-->                       known-providers-and-abilities.json
known-providers-and-abilities.json --(gewählt+bestätigt)-->           connections.json (grounding-seed)
config.json.lernvertrag --(steuert alle Schritte: beste Option, User entscheidet, nie Auto-Install)
```

Jede Datei referenziert die andere per `id`, keine kopiert Inhalt einer anderen —
dasselbe P10-Muster ("zwei Schalter, die niemand vergleicht, sind eine zweite
Lügen-Stelle") wie in `.PLUGINS/CLAUDE.md`.

## Onboardmittel

"Skill + Onboardmittel" aus dem Auftrag: der Onboard-Teil ist **kein weiteres
Dateiformat**, sondern der bereits in `SKILL.md` Schritt 7 vorgesehene Registrierungs-
Schritt (Kategorie wählen, `skill-finder` befragen) plus — sobald `user-usecases.json`
erste Einträge hat — ein kurzer Hinweis im SKILL.md-Abschnitt "Wann aktivieren", der
reale Nutzerformulierungen aus `user-usecases.json` als Trigger-Beispiele aufnimmt
(verbessert die Trigger-Genauigkeit, siehe `skill-creator`s eigener
`improve_description.py`-Schritt — auch hier: wiederverwenden statt duplizieren).
