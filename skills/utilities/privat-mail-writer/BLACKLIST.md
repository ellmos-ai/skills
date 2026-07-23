# Privat-Mail-Writer - Blacklist

Diese Datei steuert, für wen kein Kontaktprofil angelegt werden soll. Blacklist bedeutet nicht automatisch "nie antworten"; sie bedeutet zuerst: kein Stil-/Beziehungsprofil speichern.

## Standard

```yaml
enabled: true
profile_block_on_match: true
reply_block_on_match: false
```

Bei Treffer:

1. kein Kontaktprofil erstellen
2. keine Mailhistorie zur Stilableitung auswerten
3. nur neutralen Entwurf liefern, falls der User ausdrücklich eine Antwort will

## Absender-Muster ohne Profil

```text
no-reply@
noreply@
donotreply@
do-not-reply@
mailer-daemon@
postmaster@
bounce@
notifications@
newsletter@
news@
marketing@
offers@
promo@
support@
help@
security@
alerts@
updates@
```

## Betreff-/Header-Muster ohne Profil

```text
unsubscribe
list-unsubscribe
newsletter
werbung
angebot
sale
rabatt
delivery status
undeliverable
mail delivery failed
do not reply
automatische antwort
auto-reply
```

## Kontaktarten ohne Profil

- Newsletter
- Marketing/Promotion
- Systembenachrichtigungen
- Sicherheitswarnungen
- Versandstatus/Bounces
- automatische Termin-/Ticket-/Account-Mails
- Einmalige Support-Tickets ohne echte persönliche Beziehung

## Ausnahmen

Wenn der User ausdrücklich sagt, dass ein Treffer ein echter Kontakt ist, Kategorie und Profil trotzdem anlegen, aber die Ausnahme im Profil dokumentieren:

```json
{
  "source": "user",
  "evidence_level": "user-confirmed",
  "evidence": "User hat Blacklist-Treffer als echten Kontakt bestätigt."
}
```

Beispiel: Eine echte Person nutzt eine Adresse wie `support@...` persönlich.

