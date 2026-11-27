# Ausgelagerte `.json`-Einstellungen, Profil-Kaskade & Selbstheilung (`v0.4.1`)

`ocean-skill-creator` trennt **Code/Anweisung** konsequent von **konfigurierbaren Parametern** — wendet dieses Prinzip aber **pragmatisch („nur dort, wo sinnvoll“)** an.

## 0. Pragmatismus-Regel: Wann eine `.json`-Datei sinnvoll ist — und wie sie heißen darf

1. **Kein Pflichtname `default-config.json`:**
   - `default-config.json` ist der empfohlene Standardname, wenn kein fachlicher Begriff sprechender ist.
   - Domänenspezifische `.json`-Dateinamen wie `models.local.json`, `routing-defaults.json`, `kalender-profiles.json`, `prefs.json`, `thresholds.json` oder `<kanal>.json` sind **vollwertig gleichgestellt** (`init <skill> --config-name <datei.json>`).
   - `audit-skill` erkennt automatisch alle validen Konfigurations-JSONs im Skill-Ordner sowie unter `config/` und `profiles/` (`config_files`, `has_external_config`) und verlangt niemals eine Umbenennung zu `default-config.json`.
2. **Kein JSON-Zwang für reine Leitfaden-Skills:**
   - Reine Beratungs-, Therapie-, Denk- oder Router-/Umbrella-Skills ohne konfigurierbare Parameter benötigen **keine** `.json`-Datei (`init <skill> --minimal` bzw. `--no-config`) und erhalten dafür keinerlei Punktabzug im Audit.

## 1. Anti-Hardcoding-Regel (Sobald ein Skill konfigurierbare Werte besitzt)

Sobald ein Skill veränderliche Betriebsparameter nutzt, gehören diese in eine `.json`-Konfigurationsdatei (und optionale Override-Profile), **niemals** als verstreute Literale in Skriptcode oder Fließtext:

- Ausgabeformate (`html`, `pdf`, `md`, `txt`, `json`) und Ausgabeverzeichnisse (`output.output_dir`)
- Schwellenwerte, Limits, Modelltabellen, Zeitfenster, Wiederholungsintervalle und Seitengrößen
- Sprach-, Datums- und Darstellungspräferenzen
- Vorlagenpfade (`templates.dir`, `templates.custom_dir`)
- Zustellungs- und Verteilungsoptionen (`delivery.enabled`, `delivery.dry_run`, `delivery.channel`, `delivery.target`)

Im Quellcode sind lediglich die **strukturellen Sicherheitsinvarianten** fest verankert (z. B. kein unbestätigter Außenversand ohne explizite Freigabe, Path-Traversal-Schutz, Stdlib-Fallback).

## 2. Die mehrstufige Konfigurations-Kaskade

Wo lokale oder kanalspezifische Überschreibungen sinnvoll sind, werden Einstellungen deterministisch von links (niedrigste Priorität) nach rechts (höchste Priorität) per rekursivem Dictionary-Deep-Merge zusammengeführt:

```text
1. <basis-config>.json              (z. B. default-config.json oder routing-defaults.json — nutzerneutral im Repo)
2. config.json                      (lokaler/privater Basis-Override der Instanz)
3. profiles/<kanal>.json            (kanalspezifischer Override, z. B. mail.json, slack.json, whatsapp.json)
4. profiles/<kanal>.<chat>.json     (chat-/zielspezifischer Override, z. B. whatsapp.projekt-alpha.json)
5. CLI-Override (--set k.pfad=wert) (expliziter Laufzeitparameter des Aufrufs)
```

### Merge-Semantik (`deep_merge`)

- **Verschachtelte Objekte (`dict`):** Werden rekursiv zusammengeführt — überschreibt `profiles/mail.json` nur `{"output": {"default_format": "pdf"}}`, bleiben alle übrigen Schlüssel unter `output` aus den niedrigeren Stufen erhalten.
- **Listen und Skalare (`list`, `str`, `int`, `float`, `bool`, `null`):** Ersetzen den jeweiligen Wert der niedrigeren Stufe vollständig.
- **Kommentarschlüssel (`_hinweis`, `_comment`):** Dienen der Dokumentation in Vorlagen und beeinflussen keine Fachlogik.

## 3. Selbstheilungs-Protokoll (`self-healing`)

Lokale Konfigurationsdateien werden in der Praxis häufig manuell angepasst oder zwischen Systemen synchronisiert. Ein Syntaxfehler oder ein veralteter Stand darf einen konfigurationsgestützten Skill niemals unkontrolliert abstürzen lassen:

1. **Graceful Fallback (immer aktiv):**
   - Fehlt `config.json` oder ein Profil, greift nahtlos die Basis-JSON (`default-config.json` bzw. `<skill>-defaults.json`).
   - Enthält eine Override-Datei ungültiges JSON (`JSONDecodeError`), keine Objekt-Wurzel (`list`/`str` statt `dict`) oder überschreibt sie einen Pflicht-Objektabschnitt mit einem Skalar, fängt `load_effective_config()` den Fehler ab, behält den validen Basiswert bei und gibt den Befund strukturiert unter `warnings` zurück.
2. **Verlustfreie Sicherung & Selbstreparatur (`repair=True` / `--repair`):**
   - Vor jeder Reparatur einer korrupten Datei wird der defekte Originalinhalt bytegleich unter `<dateiname>.corrupt.<YYYYMMDDTHHMMSSZ>.bak` im selben Ordner gesichert — **niemals** still gelöscht!
   - Anschließend stellt der Loader für `config.json` eine saubere Kopie auf Basis der Basis-JSON (bzw. für defekte Kanalprofile ein leeres valides Override-Objekt `{}`) wieder her und dokumentiert den Vorgang in `healed`.
3. **Additive Schema-Migration:**
   - Bringt ein Skill-Update neue Schlüssel in der Basis-JSON mit, ergänzt `additive_migrate()` fehlende Schlüssel in einer bestehenden `config.json`, ohne irgendeinen bereits gesetzten Nutzwert zu verändern (`migrated_keys`).
4. **Atomares Schreiben (`atomic_write_json`):**
   - Jede Konfigurationsschreibung erfolgt über eine temporäre Datei im selben Zielverzeichnis (`NamedTemporaryFile(delete=False)` + `flush` + `os.fsync`), gefolgt von `os.replace(tmp, target)`.

## 4. Referenz-Nutzung über `ocean_skill_scaffold.py`

```bash
python skills/infrastructure/ocean-skill-creator/scripts/ocean_skill_scaffold.py validate-config \
  --default skills/<kat>/<skill>/routing-defaults.json \
  --config skills/<kat>/<skill>/config.json \
  --channel mail \
  --chat weekly-digest \
  --set output.default_format=pdf \
  --repair \
  --json
```
