# Privat-Mail-Writer - Config

Diese Datei ist die zentrale Steuerung für den Skill. Sie enthält Präferenzen, Wenn-dann-Regeln, Permission-Gates und den Blacklist-Schalter. Sie ist nutzerneutral: keine echten Kontakte, keine echten Signaturen und keine privaten Mailinhalte eintragen.

## Profiling-Trigger

Kontaktprofile erst anlegen oder aktualisieren, wenn der User eine konkrete Mail an einen konkreten Kontakt schreiben will.

**Profiling erlaubt**

- "Schreib eine Mail an Bruder Simon ..."
- "Antworte Frau Müller kurz ..."
- "Formuliere an meinen Kollegen Jan ..."
- "Sag meiner Mutter ..."

**Profiling nicht erlaubt**

- allgemeine Inbox-Sichtung
- Newsletter-/Werbe-/Systemmails
- "Welche Kontakte habe ich?"
- Profilanlage ohne aktuelle Schreibaufgabe

## Präferenzen

| Feld | Standard | Regel |
|---|---|---|
| Länge | kurz | lieber 3 gute Sätze als 8 erklärende Sätze |
| Ton | freundlich, klar | warm, aber nicht ausschweifend |
| Begründungen | sparsam | Gründe nur nennen, wenn vom User genannt oder sicher aus Kontext |
| Varianten | wenige | höchstens zwei Varianten: `sehr kurz` und `etwas wärmer` |
| Sprache | Deutsch | echte Umlaute verwenden |
| Profilstore | lokal bevorzugt | echte Profile in `kontaktprofile.local.json`, nicht in die neutrale Skill-Datei |

## Wenn-dann-Regeln

| Wenn | Dann |
|---|---|
| User nennt einen konkreten Empfänger | Blacklist prüfen, dann Profil suchen oder lazy erstellen |
| User nennt "Bruder", "Mutter", "Vater", "Schwester" usw. | Kategorie `family` als User-Quelle mit Evidenzgrad `user-confirmed` setzen |
| User nennt "enger Freund", "Partner", "beste Freundin" | Kategorie `inner-circle` oder `friends` als User-Quelle setzen |
| User nennt "Kollege", "Chefin", "Team" | Kategorie `colleagues` setzen |
| Empfänger ist Behörde, Praxis, Schule, Kanzlei, Verwaltung | Kategorie `official` setzen, formeller schreiben |
| Kontakt kommt nur in Newslettern/Systemmails vor | kein Kontaktprofil erstellen |
| Mailhistorie widerspricht User-Kategorie | User-Kategorie behalten, Widerspruch als Evidenznotiz mit niedriger Priorität speichern |
| Pflichtangaben fehlen | eine knappe Rückfrage stellen |
| User verlangt "kurz" | maximal Dank, Kernbotschaft, Abschluss |
| User verlangt Senden | Permission-Gate prüfen und vor dem Versand nochmals bestätigen, wenn Risiko nicht `low` ist |

## Permission-Gates

| Gate | Beispiele | Aktion |
|---|---|---|
| `low` | reine Entwürfe, harmlose organisatorische Antworten | Entwurf direkt liefern |
| `medium` | Terminabsagen, klare Zusagen, sensible private Gründe | Entwurf liefern, vor Versand bestätigen lassen |
| `high` | Recht, Geld, Medizin, Behördenfristen, Konflikte, Beschwerden | Rückfrage/Freigabe vor finaler Formulierung oder Versand |
| `blocked` | Täuschung, Drohung, fremde Identität, unerlaubte Datenweitergabe | nicht ausführen, sichere Alternative formulieren |

## Blacklist-Schalter

Blacklist ist standardmäßig aktiv.

```yaml
blacklist_enabled: true
blacklist_file: BLACKLIST.md
```

Wenn `blacklist_enabled` aktiv ist, vor Profilanlage und vor Antwortentwurf `BLACKLIST.md` prüfen. Bei einem Treffer kein Kontaktprofil erstellen. Nur dann antworten, wenn der User ausdrücklich eine Antwort an diesen Absender will und der Fall nicht systemisch/newsletterartig ist.

## Profilkategorien

Erlaubte Hauptkategorien:

- `family`
- `inner-circle`
- `friends`
- `colleagues`
- `professional-network`
- `official`
- `services`
- `medical`
- `education`
- `unknown`

Jede Kategorie braucht:

- `label`
- `source`: `user`, `mail-text`, `address-book`, `signature`, `domain`, `inference`
- `evidence_level`: `user-confirmed`, `strong`, `medium`, `weak`
- `evidence`: kurze paraphrasierte Begründung

User-Aussagen haben Vorrang vor Mailtext-Inferenz. Mailtext-Inferenz nie als sicher ausgeben, sondern als Einschätzung.

## Alters-Check

Einmal pro Monat prüfen, ob Profilbereinigung nötig ist. Startwert: `2026-06-18`.

Profile löschen, wenn seit mehr als 365 Tagen kein Mailkontakt stattfand. Danach `last_age_check` aktualisieren.

