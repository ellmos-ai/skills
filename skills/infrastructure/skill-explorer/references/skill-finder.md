# Skill-Finder (analog /using-superpowers)

## Idee

`/using-superpowers` ist der Finder/„Türsteher" für die Superpowers-Skills: eine Verhaltensregel,
die VOR jeder Aktion erzwingt, zu prüfen, ob ein Skill passt. Analog dazu kann den Audit-Modus
auf Wunsch einen **eigenen** Finder erzeugen, der dasselbe für die *user-eigenen* Skills tut — aktiv
routen statt nur passiv per Description matchen. Das ist der Unterschied zu `code-skill-index`
(reiner Katalog): der Finder ist eine **Routing-Verhaltensregel** plus Familien-Wegweiser.

Angeboten wird er als Entscheidung **[F]** in der Liste (analog [R]/[P1]/[P2]).

## Warum als eigener, schlanker Subskill

Der Finder soll klein und schnell ladbar sein (er wird potenziell oft konsultiert). Deshalb wird er
NICHT in `skill-explorer` eingebaut, sondern als eigener Skill `skill-finder` **ausgegründet**
(Installer-Prinzip: viele schlanke Subskills statt eines Monolithen). Er referenziert das Register
und die Familien, statt deren Inhalt zu kopieren.

## Inhalt des generierten Finders

Vorlage: `assets/skill-finder-template.md`. Kern:

1. **Die Regel** — vor nicht-trivialen Aufgaben zuerst prüfen, ob ein user-Skill passt; bei Treffer
   den Skill laden und seiner Anleitung folgen (Live-Datei lesen, nicht aus dem Gedächtnis).
2. **Familien-Routing-Tabelle** — aus `the family map` / dem Register gefüllt: Thema → Familie → Skill.
3. **Red Flags** — Rationalisierungen, die „doch keinen Skill nutzen" begründen (analog using-superpowers).
4. **Verweis aufs Register** — `code-skill-index` für die vollständige Liste.

## Pflege

Der Finder veraltet, wenn Familien sich ändern. Seine Routing-Tabelle wird vom Subskill
`skill-family-care` (P1) mitgepflegt bzw. aus dem aktuellen `inventory_skills.py`-Lauf neu erzeugt.
In `config.json` wird `finder_installed: true` + Stand vermerkt, damit ein Re-Run weiß, dass er
existiert und ihn aktualisieren statt neu anlegen soll.
