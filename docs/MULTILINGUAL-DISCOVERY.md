# Mehrsprachige Skills: Identität, Titel und Discovery

Stand: 2026-11-02. Dieses Konzept unterscheidet implementierte Repository-Metadaten,
Sprachqualität und die tatsächlich beobachtete Darstellung fremder Verzeichnisse.

## Problem und Bestandsaufnahme

Ein Skill soll unter einer stabilen technischen Identität auffindbar und in mehreren
Sprachen lesbar sein. Sprachcodes sind keine Skill-Namen. Der öffentliche Bestand
enthielt 240 zusätzliche `SKILL.md`-Dateien in 48 Familien unter Sprachordnern,
obwohl sämtliche flachen Gegenstücke `SKILL.<code>.md` vorhanden waren. Die Inhalte
unterscheiden sich; sie dürfen nicht durch einen ungeprüften Dedupe gelöscht werden.

Der bestehende Generator `build_public_registry.py` führt bereits eine Familie je
kanonischer `SKILL.md`, verwendet Git beziehungsweise das öffentliche Quellmanifest
als Autorität und schützt private Inhalte. `build_skills_map.py` rendert daraus die
öffentliche Karte. Beide Werkzeuge bleiben zuständig; es entsteht keine zweite Queue
und keine unabhängige Übersetzungsregistry.

## Recherchierte Standards und Grenzen

- Die [Agent-Skills-Spezifikation](https://agentskills.io/specification) bindet den
  technischen `name` an den Skill-Ordner; sie definiert keinen Vertrag für
  Sprachfamilien oder lokalisierte Anzeigenamen. Ihre `metadata`-Erweiterung ist
  möglich, garantiert aber keine Interpretation durch Verbraucher.
- Die [Vercel-CLI](https://github.com/vercel-labs/skills/blob/main/src/skills.ts)
  sucht `SKILL.md`, liest `name` und `description` und dedupliziert Namen. Die
  Auswahl einzelner Ordner oder rekursive Suche kann Sprachunterordner als eigene
  Skills erreichen. Der geprüfte Code enthält keine Übersetzungsgruppierung.
- Für Webseiten sind [BCP-47-Sprachkennungen](https://www.w3.org/International/articles/language-tags/)
  und wechselseitige [hreflang-Verweise](https://developers.google.com/search/docs/specialty/international/localized-versions)
  etablierte Mechanismen. `hreflang` gehört in einen kontrollierten HTML-Head,
  HTTP-Header oder eine Sitemap. Ein Markdown-Kommentar auf GitHub ersetzt das nicht.
- Schema.org bietet [translationOfWork](https://schema.org/translationOfWork) und
  [workTranslation](https://schema.org/workTranslation). Die Pipeline kann diese
  Beziehungen als JSON-LD exportieren; das ist kein spezieller Agent-Skills-Standard
  und keine Garantie für eine bestimmte Suchdarstellung.

## Beobachtete Verzeichniseinträge

| Fall | Quelle und beobachtetes Ergebnis |
|---|---|
| Eigene falsche Identität | [Skills Directory: Zh](https://www.skillsdirectory.com/skills/ellmos-ai-skills-1aa636e2) zeigt einen Chunking-Skill als `Zh` und empfiehlt `--skill zh`. |
| Eigene Vermischung | [DecimalAI: ellmos-ai/zh](https://app.decimal.ai/skills/ellmos-ai-zh) zeigt einen Hygiene-Titel, eine Ideenfindungsbeschreibung und als Quellpfad `idea-mining/zh/SKILL.md`. Das ist ein beobachteter fehlerhafter Eintrag, keine verifizierte Qualitätsbewertung. |
| Parallele Sprachen desselben Anbieters | [supper-skills EN](https://github.com/supper-skills/develpment-skills/blob/main/skills/brainstorming/SKILL.md) und [ZH](https://github.com/supper-skills/develpment-skills/blob/main/skills_zh-CN/brainstorming/SKILL.md) heißen beide `brainstorming`. SkillsMP zeigt [EN](https://skillsmp.com/creators/supper-skills/develpment-skills/skills-brainstorming) und [ZH](https://skillsmp.com/creators/supper-skills/develpment-skills/skills-zh-cn-brainstorming) als einzelne Einträge mit erkannter Sprache, ohne sichtbare Paargruppierung. |
| Sprachfork | [Matt Pocock EN](https://github.com/mattpocock/skills/blob/main/skills/productivity/handoff/SKILL.md) und [vinvcn ZH](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/main/skills/productivity/handoff/SKILL.md) erscheinen unter getrennten [EN](https://www.skills.sh/mattpocock/skills/handoff)- und [ZH](https://www.skills.sh/vinvcn/mattpocock-skills-zh-cn/handoff)-Detailseiten. |
| Weiterer Sprachfork | [killvxk/pm-skills-zh](https://github.com/killvxk/pm-skills-zh) bezeichnet sich als Übersetzung von phuryn/pm-skills. [SkillsMP ZH](https://skillsmp.com/creators/killvxk/pm-skills-zh/pm-execution-skills-create-prd) und [skills.sh EN](https://www.skills.sh/phuryn/pm-skills/create-prd) sind getrennte Einträge. |

Die Stichproben belegen keine allgemeine Fähigkeit zur Gruppierung. Nichterreichbare
Seiten wurden nicht als Beweis fehlender Indexierung gezählt. Alte Einträge können
nach einer Quellkorrektur weiterbestehen; eine Korrektur beim Anbieter erfordert
separaten Readback beziehungsweise dessen Korrekturverfahren.

## Architekturentscheidung

1. **Ein installierbarer Einstieg:** `skills/<kategorie>/<slug>/SKILL.md`.
   Die technische Identität bleibt über Sprachen stabil. Neue Namen `en`, `zh`
   oder `zn` sind unzulässig.
2. **Sprachfassungen im bestehenden flachen Format:** `SKILL.en.md`, `SKILL.zh.md`
   usw. Ein nativer H1-Titel und eine lokalisierte Beschreibung machen die Fassung
   erkennbar, ohne den technischen Slug zu übersetzen.
3. **Alte Einstiegspunkte werden Dokumente:** `<sprache>/SKILL.md` wird nach
   vorhandenem flachen Gegenstück in demselben Ordner zu `README.md` umbenannt.
   Alle Bytes bleiben erhalten. Diese abweichenden Altstände sind keine zusätzlich
   freigegebenen Sprachfassungen und werden nicht in `localizations` aufgenommen.
4. **Familienzuordnung in der vorhandenen Registry:** Das additive Feld
   `localizations` enthält Sprache, kanonischen Dateipfad, nativen Titel und
   Beschreibung. `id`, `name`, `path` und die bisherigen Felder bleiben stabil.
   `languages` bleibt aus Kompatibilitätsgründen ein historischer Dateibestandswert;
   Verbraucher sollen für benannte/verlinkte Fassungen `localizations` verwenden.
5. **Unvollständigkeit sichtbar lassen:** Marker-Stubs ohne eigene Identität oder
   Beschreibung werden nicht als Localizations beworben. Ein begründeter,
   versionierter Bestandsbaseline erlaubt bestehende Lücken, blockiert neue.
   Metadatenprüfung ersetzt keine vollständige sprachliche oder fachliche Abnahme.
6. **Eigener Katalog und optionale Webintegration:** Die Skill-Karte zeigt die
   Sprachfassungen gruppiert mit nativen Titeln. `--jsonld` exportiert Schema.org
   aus denselben gefilterten Daten. Eine künftige eigene Website muss pro Sprache
   korrekte, wechselseitige `hreflang`-Links und selbstbezogene Canonical-URLs
   erzeugen. GitHub-Dateien werden nicht mit unwirksamen SEO-Tags versehen.

## Pipeline und Abnahme

```bash
# Nur Vorschau, kein Modell und keine Veröffentlichung:
python skill_localizations.py --retire-legacy
# Explizite Migration im eigenen, eng gesperrten Worktree:
python skill_localizations.py --retire-legacy --apply
# Umbenennungen vor Generierung in den vorgeschlagenen Git-Stand aufnehmen.
python build_public_registry.py
python build_skills_map.py
python skill_localizations.py
python skill_localizations.py --jsonld
python build_public_registry.py --check
python build_skills_map.py --check
```

CI prüft verbleibende aktive Locale-Einstiege und neue Metadatenlücken. Tests decken
Sprachcode-Namen, Marker-Stubs, Titel in Codebeispielen, ungeführte/private Dateien,
abweichende Altinhalte, Kollisionen beim Umbenennen und Übersetzungsbeziehungen ab.
Die Migration wird vor/nachher auf Dateizahl und bytegenaue Erhaltung geprüft.
Keine Deployment-Verzeichnisse, Nutzerdaten, fremden Skills oder Credentials ändern.

Die Umsetzung im Repository kann Fremdcrawlerfehler vermeiden helfen. Erst nach
Veröffentlichung und erneutem Abruf der konkreten Anbieter-Seiten kann eine
verbesserte externe Darstellung als belegt gelten. Es gibt keine fingierte
Reindexierungs- oder Website-Erfolgsmeldung.
