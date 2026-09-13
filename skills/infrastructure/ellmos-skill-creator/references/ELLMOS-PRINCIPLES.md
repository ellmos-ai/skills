# ellmos-Prinzipien für produzierte Skills

Drei Wörter, die leicht gegeneinander gelesen werden, aber zusammengehören:
**anbieterneutral**, **userneutral**, **ellmos-neutral-aber-ellmos-sensitiv**.

## Was die drei Wörter tatsächlich fordern

- **Anbieterneutral:** Der Skill schreibt keinen einzelnen externen Anbieter fest
  verdrahtet vor (z. B. "ruft immer die ElevenLabs-API auf"). Er beschreibt eine
  **Rolle** ("Text-zu-Sprache") und lässt offen, wer sie erfüllt.
- **Userneutral:** Keine Annahmen über einen bestimmten Nutzer, Account oder Pfad,
  die außerhalb dieses Systems falsch wären. Was hier zwingend userneutral heißt,
  steht bereits vorbildlich in `.AI/.MODULES/build-your-users-mind`
  (publizierbares, `<USER>`/`<AGENT>`-generisches Muster) — dorthin verweisen,
  nicht neu erfinden.
- **ellmos-neutral, aber ellmos-sensitiv:** Der Skill funktioniert **vollständig
  allein**, ohne dieses Ökosystem (bringt alles Nötige mit — Vorlagen, Fallback-Logik,
  Minimaldaten). Sobald er aber in einer Umgebung läuft, in der ellmos-Komponenten
  vorhanden sind, **erkennt** er das und nutzt sie, statt sie zu ignorieren.
  "Neutral" und "sensitiv" widersprechen sich nicht — sie sind zwei verschiedene
  Fragen: *Muss ich?* (nein) vs. *Darf ich, wenn's da ist?* (ja, und dann besser).

Das ist wortwörtlich das Leitmotiv von `grounding-seed` selbst
(README: *"cultivated landscape, not wildflower"* / *"viable alone, more
productive together"*) — dieser Abschnitt wendet dasselbe Prinzip auf **jeden
einzelnen produzierten Skill** an, nicht nur auf Module.

## Erkennungsmuster (kein zweiter Resolver)

Genau ein Weg, kopiert aus `grounding-seed`s eigenem README-Beispiel, nicht neu
erfunden:

```python
from grounding_seed import detect_ecosystem, resolve, LocalStore
from pathlib import Path

store = LocalStore(Path(__file__).parent / "connections.json")
status = detect_ecosystem()  # -> prueft NUR: ist source_resolver importierbar?

# resolve() delegiert selbst vollstaendig an source_resolver, wenn vorhanden --
# der Skill muss NICHT selbst verzweigen. Im isolierten Fall laeuft die
# mitgelieferte Minimalfassung, formidentisch getestet (test_ladder_parity.py).
result = resolve("tts-anbieter", store=store)
```

Ist `grounding_seed` selbst nicht installiert (der produzierte Skill läuft in
einer fremden Umgebung ohne dieses Paket), fällt der Skill auf sein eigenes,
mitgeliefertes `config.json`/`connections.json` zurück — genau dafür sind die
Vorlagen unter `../templates/` gedacht. **Try/except um den Import, nie eine
harte Abhängigkeit.**

```python
try:
    from grounding_seed import detect_ecosystem, resolve, LocalStore
    HAS_GROUNDING_SEED = True
except ImportError:
    HAS_GROUNDING_SEED = False
    # -> eigenes config.json/connections.json direkt lesen (siehe unten)
```

## Docking: config.json vs. connections.json

`grounding_seed.store.LocalStore` schreibt standardmäßig eine Datei namens
`config.json` (Parameter `filename`, überschreibbar). Das führt zu der sauberen
Aufteilung, die dieser Skill für produzierte Skills vorschreibt:

| Datei | Inhalt | Beispiel-API |
|---|---|---|
| `config.json` | Skill-eigene, reine Verhaltens-Einstellungen (kein externer Bezug) | normales `json.load()` |
| `connections.json` | Aufgelöste externe Andockstellen (welcher Anbieter, seit wann, Herkunft) | `LocalStore(root, filename="connections.json")` |

Ein Skill ohne externen Bedarf braucht nur `config.json` (oder gar keine der beiden
Dateien). Ein Skill mit externem Bedarf (Programm, Dienst, Anbieter) bekommt beide,
getrennt, damit reines Verhalten und aufgelöste Fakten nicht vermischt werden
(dasselbe Muster-Argument wie "Areal *und* Feld" in `.PLUGINS/CLAUDE.md`).

## Kurz-Checkliste beim Erstellen

- [ ] Kein Anbietername im Fließtext dort, wo eigentlich eine Rolle gemeint ist
- [ ] Try/except um jeden `grounding_seed`/ellmos-spezifischen Import
- [ ] `config.json`-Vorlage vorhanden, auch wenn zunächst leer
- [ ] `connections.json`-Vorlage vorhanden, sobald der Skill externen Bedarf hat
- [ ] Ein Testlauf **ohne** installiertes `grounding_seed` funktioniert (Standalone-Probe)
