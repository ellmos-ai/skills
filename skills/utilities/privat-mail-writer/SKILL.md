---
name: privat-mail-writer
version: 0.2.0
type: skill
author: Lukas Geiger + GPT
created: 2026-06-19
updated: 2026-06-19
description: >
  Dieser Skill sollte genutzt werden, wenn der User private oder halbformale
  E-Mails schreiben, beantworten, absagen, nachfassen, kürzen, umformulieren
  oder im eigenen Stil entwerfen lassen will, besonders bei Terminen,
  offiziellen Absagen, freundlichen Kurzantworten und kontaktabhängigem Ton.
  Profilanalyse erst bei einem konkreten Mail-Schreibauftrag starten.

# Kompatibilität
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [mail, email, privat, antwort, absage, termin, schreibstil, kontaktprofil]
language: de
status: active

# Abhängigkeiten
dependencies:
  tools: []
  optional_tools:
    - name: mail-connector
      path: ".AI/.MODULES/mail-connector/"
      cli: "mailc"
      python_module: "mail_connector.cli"
      usage: "mailc context <kontakt> --mode reply --json  # Liefert Mail-Kontext als JSON für Profilaufbau"
      note: "Optionales lokales IMAP-CLI-Tool. Nur nutzen wenn installiert (`pip install -e .` im Modulordner). Ohne dieses Tool arbeitet der Skill ohne Mailzugriff."
  services: [mail-backend-optional]
  protocols: [kontaktprofil, usecase-registry]
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Privat-Mail-Writer

## Zweck

Privat-Mail-Writer erstellt kurze, freundliche und kontaktabhängig passende Mailentwürfe. Der Skill ist nutzerneutral angelegt: Er enthält keine echten Kontakte, keine echten Signaturen und keine echten Mailinhalte.

Der Kern ist lazy und empirisch: Erst wenn der User eine konkrete Mail an einen Kontakt schreiben will, das Profil für genau diesen Kontakt anlegen oder aktualisieren. Keine Profile auf Vorrat erzeugen. Wenn keine Mailhistorie verfügbar ist, keine Stilbehauptungen erfinden, sondern neutral kurz schreiben oder gezielt nach Beispielen fragen.

## Ressourcen

- `CONFIG.md` - zentrale Präferenzen, Wenn-dann-Regeln, Permission-Gates und Blacklist-Schalter.
- `BLACKLIST.md` - Ausschlüsse für Newsletter, Systemsender und Kontakte ohne Profil.
- `USECASES.md` - Usecase-Registry und Regeln für neue Usecases.
- `SIGNATURES.md` - neutrale Signatur- und Grußformel-Regeln.
- `MUSTER-BLOCKS.md` - kurze wiederverwendbare Textbausteine.
- `kontaktprofile.json` - leeres, nutzerneutrales Schema für Kontaktprofile. Echte Profile nur lokal und datensparsam führen.

## Arbeitsablauf

1. **Konfig laden:** `CONFIG.md` lesen. Wenn Blacklist aktiv ist, zusätzlich `BLACKLIST.md` prüfen.
2. **Trigger prüfen:** Nur bei einem konkreten Schreibauftrag für einen bestimmten Kontakt profilieren, z. B. "schreib eine Mail an Bruder Simon". Keine Inbox-Sweeps nur zur Profilanlage.
3. **Blacklist prüfen:** Newsletter, No-Reply, Systemsender und ausgeschlossene Domains/Kontakte bekommen kein Kontaktprofil. Für solche Fälle neutral antworten oder nicht antworten.
4. **Mailaufgabe erkennen:** Ziel, Empfänger, Anlass, gewünschte Kürze, Sprache, Ton und notwendige Fakten bestimmen.
5. **Usecase bestimmen:** `USECASES.md` lesen und den passendsten Usecase auswählen. Wenn kein Usecase passt, einen neuen wiederverwendbaren Usecase anlegen oder bei fehlenden Pflichtangaben kurz nachfragen.
6. **Kontaktprofil prüfen:** Für jeden nicht ausgeschlossenen Empfänger ein vorhandenes Profil in `kontaktprofile.json` oder in einer privaten lokalen Profilkopie suchen.
7. **Profil erstellen oder aktualisieren:** Wenn kein belastbares Profil vorhanden ist, bis zu die letzten zehn relevanten Mails mit genau diesem Kontakt aus dem verfügbaren Mail-Backend lesen. Gesendete Mails sind für Schreibstil stärker zu gewichten als empfangene Mails.
8. **Empirie speichern:** Im Kontaktprofil nur zusammenfassende, belegbare Stil-, Verhältnis- und Kategorie-Signale speichern. Keine Rohmails, keine langen Zitate und keine unnötigen personenbezogenen Details ablegen.
9. **Permission-Gate anwenden:** Vor Senden, heiklen Inhalten oder fehlenden Pflichtangaben die Gates aus `CONFIG.md` beachten.
10. **Entwurf schreiben:** Usecase-Form, Kontaktprofil und aktuelle Aufgabe zusammenführen. Den Stil nachahmen, ohne falsche Nähe, falsche Zusagen oder unbelegte Gründe zu erfinden.
11. **Ausgabe liefern:** Standardmäßig Betreff und Mailtext ausgeben. Nur senden, wenn der User ausdrücklich das Senden freigegeben hat und ein passendes Mail-Tool verfügbar ist.

## Kontaktprofile

Ein Kontaktprofil beschreibt nicht die Person an sich, sondern das beobachtete Kommunikationsverhältnis und den Schreibstil des Kontoinhabers gegenüber dieser Person.

Profilfelder sollen knapp bleiben:

- letzte Kontaktzeit
- Anzahl und Zeitraum der ausgewerteten Mails
- Anrede und Grußformel
- Du/Sie/Formalität
- Satzlänge und typische Kürze
- Wärmegrad, Direktheit, Verbindlichkeit
- Verhältnis-Einschätzung mit Konfidenz
- Kontaktkategorie, z. B. `family`, `inner-circle`, `friends`, `colleagues`, `services`, `official`, `unknown`
- Quelle der Kategorie: User-Aussage, Mailtext, Adressbuch, Signatur oder Inferenz
- Evidenzgrad der Kategorie: `user-confirmed`, `strong`, `medium`, `weak`
- kurze paraphrasierte Belege wie "mehrere gesendete Mails enden mit 'Viele Grüße'" oder "Antworten bleiben unter fünf Sätzen"

Monatlich prüfen, ob ein Alters-Check fällig ist. Wenn der Monat des aktuellen Datums vom gespeicherten `last_age_check` abweicht, Profile löschen, deren `last_contact_at` mehr als ein Jahr zurückliegt, und `last_age_check` auf das aktuelle Datum setzen. Der Startwert im neutralen JSON ist `2026-06-18`.

## Stilregeln

- Kurz schreiben. Privatmails brauchen selten lange Vorreden.
- Freundlich bleiben, aber nicht übererklären.
- Echte Gründe nur nennen, wenn sie vom User genannt oder aus dem Kontext sicher sind.
- Bei offiziellen Absagen: höflich, klar, ohne Rechtfertigungsroman.
- Bei Unsicherheit über Fakten: eine knappe Rückfrage stellen, bevor der Entwurf finalisiert wird.
- Deutsche Texte mit echten Umlauten schreiben: ä, ö, ü, Ä, Ö, Ü, ß.

## Neue Usecases

Wenn eine Mailaufgabe wiederverwendbar wirkt und in `USECASES.md` noch nicht abgedeckt ist, den Usecase ergänzen:

- stabile ID, z. B. `UC-002`
- Name und typische Trigger
- Ziel der Mail
- Pflichtangaben und optionale Angaben
- Standardlänge und Ton
- kurze Vorlage oder Bausteinfolge
- offene Rückfragen, falls Pflichtangaben fehlen

Ein einmaliger Sonderfall wird nicht als Usecase aufgebläht. In diesem Fall nur den aktuellen Entwurf liefern.

## Ausgabeformat

Für normale Entwürfe:

```text
Betreff: ...

Sehr geehrte ...

...

Mit freundlichen Grüßen
[Signatur]
```

Wenn der User nur Text ohne Betreff will, nur den Mailtext liefern. Wenn mehrere Varianten sinnvoll sind, höchstens zwei Varianten anbieten: "sehr kurz" und "etwas wärmer".

## Grenzen

Kein Kontaktprofil erfinden. Keine vertraulichen Details aus Mails unnötig in die Antwort kopieren. Keine Mail ohne ausdrückliche Freigabe senden. Keine juristischen, medizinischen oder finanziellen Zusagen formulieren, wenn der User sie nicht klar vorgibt.

## Changelog

### 0.2.0 (2026-06-19)
- `CONFIG.md` und `BLACKLIST.md` ergänzt.
- Profilanlage auf konkrete Mail-Schreibaufträge begrenzt.
- Kontaktkategorien mit Quelle und Evidenzgrad in das Profilschema aufgenommen.

### 0.1.0 (2026-06-19)
- Initiale Version mit Usecase-Registry, Signaturregeln, Musterblöcken und leerem Kontaktprofil-JSON.
