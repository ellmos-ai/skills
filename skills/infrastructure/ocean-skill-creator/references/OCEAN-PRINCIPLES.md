# Ocean-Prinzipien für produzierte Skills (abwärtskompatibel zu ellmos)

Drei Eigenschaften gehören in jedem produzierten Skill untrennbar zusammen:
**anbieterneutral**, **nutzerneutral**, **Ocean-/ellmos-neutral-aber-sensitiv**.

## Was die drei Eigenschaften konkret fordern

- **Anbieterneutral:** Der Skill verdrahtet keinen einzelnen externen Dienst fest im Code oder Fließtext (z. B. „ruft immer Anbieter X auf“). Er beschreibt eine **Rolle** (z. B. „Text-zu-Sprache“, „OCR“, „Kalender-Speicher“) und hält über Konfiguration und Andockstellen offen, wer sie erfüllt.
- **Nutzerneutral:** Keine Annahmen über einen bestimmten Menschen, Hostnamen, Account oder lokalen Dateipfad. Versionierte Dateien nutzen ausschließlich neutrale Defaults (`default-config.json`) oder explizite Platzhalter (`<HOME>`, `<USER>`), während persönliche Werte ausschließlich in lokalen, nicht veröffentlichten Override-Dateien (`config.json`, `<kanal>.json`) liegen.
- **Ocean-/ellmos-neutral, aber sensitiv:** Der Skill ist **vollständig allein lauffähig** (`standalone: true` — bringt `default-config.json`, `templates/` und Stdlib-Fallbacks selbst mit). Läuft er jedoch in einer Umgebung, in der Ocean- oder abwärtskompatible ellmos-Komponenten (`grounding-seed`, `source-resolver`, Memory-/Control-Module) installiert sind, **erkennt** er sie zur Laufzeit und nutzt sie automatisch.

Das entspricht exakt dem Leitmotiv von `grounding-seed` (*"cultivated landscape, not wildflower"* / *"viable alone, more productive together"*): Kein zweiter Erkennungsmechanismus wird erfunden — produzierte Skills nutzen `grounding_seed.detect_ecosystem()` mit sauberem Fallback.

## Erkennungsmuster (kein zweiter Resolver)

Immer `try/except ImportError` um optionale Ökosystem-Importe legen, niemals eine harte Abhängigkeit erzwingen:

```python
from pathlib import Path

try:
    from grounding_seed import LocalStore, detect_ecosystem, resolve
    HAS_GROUNDING_SEED = True
except ImportError:
    HAS_GROUNDING_SEED = False

skill_root = Path(__file__).resolve().parent.parent
if HAS_GROUNDING_SEED:
    store = LocalStore(skill_root, filename="connections.json")
    ecosystem_status = detect_ecosystem()
    provider = resolve("tts-anbieter", store=store)
else:
    # Eigenstaendiger Fallback ueber default-config.json + lokales connections.json
    ecosystem_status = None
```

## Saubere Dateitrennung: Einstellungen vs. externe Andockstellen

Ocean-konforme Skills trennen strikt zwischen **Verhaltenseinstellungen** (Kaskade ab `default-config.json`) und **aufgelösten externen Ressourcen** (`connections.json`):

| Datei | Aufgabe | Verwaltung |
|---|---|---|
| `default-config.json` | Versionierte, nutzerneutrale Standardeinstellungen (Formate, Schwellenwerte, `output`, `templates`, `delivery`, `self_healing`, `lernvertrag`) | Selbstheilender Config-Loader (`load_effective_config`) |
| `config.json` + `profiles/<kanal>[.<chat>].json` | Optionale lokale bzw. kanal-/chatspezifische Überschreibungen | Deep-Merge über `default-config.json`, bei Defekt `.corrupt.<ts>.bak` + Fallback |
| `connections.json` | Aufgelöste externe Programme, Dienste und gelernte Anbieter-Notizen (`ellmos.source-resolver.user-config.v1`) | `grounding_seed.store.LocalStore(root, filename="connections.json")` oder JSON-Fallback |

Ein Skill ohne externe Dienste benötigt kein `connections.json`; sobald externe Programme, APIs oder MCP-Dienste angebunden werden, hält `connections.json` die aufgelösten Fakten getrennt von den Verhaltenseinstellungen.

## Kurz-Checkliste beim Erstellen und Nachrüsten

- [ ] Rollenbegriff statt festem Anbieternamen in Logik und Struktur
- [ ] Keine persönlichen Namen, Hostnamen, lokalen Pfade oder privaten IPs in versionierten Dateien
- [ ] `try/except ImportError` um jeden optionalen `grounding_seed`-/Ökosystem-Import
- [ ] `default-config.json` vorhanden; keine Hardcodierungen für Pfade, Formate oder Schwellenwerte
- [ ] `connections.json`-Vorlage vorhanden, sobald externe Werkzeuge/Dienste genutzt werden
- [ ] Ein Standalone-Testlauf **ohne** installiertes `grounding_seed` und ohne bestehende `config.json` läuft fehlerfrei durch
