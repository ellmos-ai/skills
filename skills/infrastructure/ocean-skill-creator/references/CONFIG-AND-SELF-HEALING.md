# Ausgelagerte Einstellungen, Profil-Kaskade & Selbstheilung (`v0.4.0`)

Jeder mit `ocean-skill-creator` erstellte oder modernisierte Skill trennt **Code/Anweisung** strikt von **konfigurierbaren Parametern** und schützt sich durch einen **selbstheilenden Konfigurations-Loader** vor fehlenden oder beschädigten lokalen Einstellungsdateien.

## 1. Anti-Hardcoding-Regel (Was niemals im Code fest verdrahtet sein darf)

Folgende Werte gehören in `default-config.json` (und optionale Override-Profile), **niemals** als verstreute Literale in Skripten oder Prompt-Schritten:

- Ausgabeformate (`html`, `pdf`, `md`, `txt`, `json`) und Ausgabeverzeichnisse (`output.output_dir`)
- Schwellenwerte, Limits, Zeitfenster, Wiederholungsintervalle und Seitengrößen
- Sprach-, Datums- und Darstellungspräferenzen
- Vorlagenpfade (`templates.dir`, `templates.custom_dir`)
- Zustellungs- und Verteilungsoptionen (`delivery.enabled`, `delivery.dry_run`, `delivery.channel`, `delivery.target`)

Im Quellcode sind lediglich die **strukturellen Sicherheitsinvarianten** fest verankert (z. B. kein unbestätigter Außenversand ohne explizite Freigabe, Path-Traversal-Schutz, Stdlib-Fallback).

## 2. Die 5-stufige Konfigurations-Kaskade

Einstellungen werden deterministisch von links (niedrigste Priorität) nach rechts (höchste Priorität) per rekursivem Dictionary-Deep-Merge zusammengeführt:

```text
1. default-config.json              (versioniertes, 100 % nutzerneutrales Fallback im Skill-Ordner)
2. config.json                      (lokaler/privater Basis-Override der Instanz)
3. profiles/<kanal>.json            (kanalspezifischer Override, z. B. mail.json, chat.json, cli.json)
4. profiles/<kanal>.<chat>.json     (chat-/zielspezifischer Override, z. B. chat.ops-room.json)
5. CLI-Override (--set k.pfad=wert) (expliziter Laufzeitparameter des Aufrufs)
```

### Merge-Semantik (`deep_merge`)

- **Verschachtelte Objekte (`dict`):** Werden rekursiv zusammengeführt — überschreibt `profiles/mail.json` nur `{"output": {"default_format": "pdf"}}`, bleiben alle übrigen Schlüssel unter `output` (`supported_formats`, `pdf_stdlib_fallback` usw.) aus `default-config.json` und `config.json` erhalten.
- **Listen und Skalare (`list`, `str`, `int`, `float`, `bool`, `null`):** Ersetzen den jeweiligen Wert der niedrigeren Stufe vollständig.
- **Kommentarschlüssel (`_hinweis`, `_comment`):** Dienen der Dokumentation in Vorlagen und beeinflussen keine Fachlogik.

## 3. Selbstheilungs-Protokoll (`self-healing`)

Lokale Konfigurationsdateien werden in der Praxis häufig von Hand editiert oder zwischen Systemen synchronisiert. Ein Syntaxfehler (fehlendes Komma, abgeschnittene Datei) oder ein veralteter Stand darf den Skill niemals unbrauchbar machen:

1. **Graceful Fallback (immer aktiv):**
   - Fehlt `config.json` oder ein Profil, wird die Stufe übersprungen; `default-config.json` liefert jederzeit einen vollständigen, lauffähigen Zustand.
   - Enthält eine Override-Datei ungültiges JSON (`JSONDecodeError`), keine Objekt-Wurzel (`list`/`str` statt `dict`) oder überschreibt sie einen Pflicht-Objektabschnitt (z. B. `"output": "kaputt"` statt Objekt), fängt `load_effective_config()` den Fehler ab, behält den validen Basiswert aus `default-config.json` bei und gibt den Befund strukturiert unter `warnings` zurück.
2. **Verlustfreie Sicherung & Selbstreparatur (`repair=True` / `--repair`):**
   - Vor jeder Reparatur einer korrupten Datei wird der defekte Originalinhalt bytegleich unter `<dateiname>.corrupt.<YYYYMMDDTHHMMSSZ>.bak` im selben Ordner gesichert — **niemals** still gelöscht!
   - Anschließend stellt der Loader für `config.json` eine saubere Kopie auf Basis von `default-config.json` (bzw. für defekte Kanalprofile ein leeres valides Override-Objekt `{}`) wieder her und dokumentiert den Vorgang in `healed`.
3. **Additive Schema-Migration:**
   - Bringt ein Skill-Update neue Schlüssel in `default-config.json` mit, ergänzt `additive_migrate()` fehlende Schlüssel in einer bestehenden `config.json`, ohne irgendeinen bereits gesetzten Nutzwert zu verändern (`migrated_keys`).
4. **Atomares Schreiben (`atomic_write_json`):**
   - Jede Konfigurationsschreibung erfolgt in eine temporäre Datei im selben Zielverzeichnis (`NamedTemporaryFile(delete=False)` + `flush` + `os.fsync`), gefolgt von `os.replace(tmp, target)`. Dadurch entstehen selbst bei Prozessabbruch niemals halb geschriebene JSON-Dateien.

## 4. Referenz-Nutzung über `ocean_skill_scaffold.py`

### Per CLI prüfen und selbstheilen

```bash
python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py validate-config \
  --default skills/<kat>/<skill>/default-config.json \
  --config skills/<kat>/<skill>/config.json \
  --channel mail \
  --chat weekly-digest \
  --set output.default_format=pdf \
  --repair \
  --json
```

### In Python-Skripten eines Skills einbinden (100 % Stdlib)

Sowohl `ocean_skill_scaffold.load_effective_config` als auch der von `scaffold` generierte `scripts/<skill>_core.py`-Starter implementieren exakt dieses Muster ohne Drittanbieter-Abhängigkeiten.
