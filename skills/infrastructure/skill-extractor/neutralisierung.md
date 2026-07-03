# Neutralisierung — Skills user- und systemneutral machen

Rohmaterial aus Sessions ist an einen User, ein System und ein Projekt gebunden. Ein Skill
soll die **Mechanik** konservieren, nicht den Kontext. Diese Regeln gelten für `skill-extractor`
und `workflow-extract` gleichermaßen.

## Grundprinzip: Mechanik vs. Konfiguration

Jede Aussage im Rohmaterial einer von zwei Klassen zuordnen:

| Klasse | Beispiel | Behandlung |
| --- | --- | --- |
| **Mechanik** | „Registry-Datei VOR der Projektauswahl lesen, sonst Doppelprüfung" | Bleibt im Skill — das ist der Wert |
| **Konfiguration** | `C:\Users\<name>\...\forschung\CHECKED-REGISTRY.md` (konkreter absoluter Pfad) | Platzhalter oder Konfigurationsblock, z. B. `<PIPELINE_ROOT>/CHECKED-REGISTRY.md` |

Test: „Würde dieser Satz für einen fremden User auf einem fremden System noch stimmen?"
Wenn nein → Konfiguration.

## Ersetzungsregeln

| Konkret | Neutral |
| --- | --- |
| Absolute User-Pfade (`C:\Users\<name>\...`, `/Users/<name>/...`) | `~/...` oder `<PIPELINE-ROOT>`, `<PROJEKT>` |
| Hostnames, IPs, Ports | `<host>`, `<ip>`, `<port>` |
| Personennamen, E-Mail-Adressen, Accounts | `<user>`, `<account>` — oder Rolle („der Reviewer") |
| Projekt-/Firmennamen | generische Rolle („das Zielprojekt", `<projekt>`) |
| Konkrete Tools, wo austauschbar | Funktionsklasse + Beispiel („ein Datei-Such-MCP, z. B. …") |
| Konkrete Modellnamen, wo austauschbar | Fähigkeitsklasse („ein starkes Reasoning-Modell") |
| Credentials, Tokens, Key-Namen | NIE übernehmen, auch nicht als Platzhalter mit echtem Namen |

## Konfigurationsblock statt Streuung

Wenn ein Skill ohne konkrete Werte nicht lauffähig ist (z. B. ein fester Registry-Pfad),
die Werte NICHT über den Text streuen, sondern in einen einzigen, klar markierten Block am
Anfang ziehen:

```markdown
## Konfiguration (pro Einsatzort anpassen)

| Parameter | Bedeutung | Beispiel |
| --- | --- | --- |
| PIPELINE_ROOT | Wurzelordner der Pipeline | `~/projects/research/` |
| REGISTRY | Check-Registry-Datei | `<PIPELINE_ROOT>/CHECKED-REGISTRY.md` |
```

Der restliche Skill-Text referenziert nur noch die Parameternamen.

## Was NICHT neutralisiert wird

- **Begründungen und Fallstricke** — „OneDrive-Sync hat 30s–5min Latenz" ist Mechanik
  (gilt für jeden OneDrive-Nutzer), kein User-Detail.
- **Zahlenwerte mit Begründung** — „Logs ab ~200 Zeilen archivieren, sonst Kontextlast"
  bleibt; die Zahl ist Erfahrungswert, die Begründung macht sie anpassbar.
- **Werkzeug-Eigenheiten** — „`agy -p` liefert kein stdout" ist übertragbares Wissen über
  das Werkzeug, nicht über den User.

## Privacy-Check vor Veröffentlichung

Skills in öffentlichen Bibliotheken (Git-Repos) zusätzlich prüfen:

1. Volltextsuche nach Usernamen, Hostnames, E-Mail-Fragmenten, `C:\Users\`, Home-Pfaden.
2. Keine internen URLs, Ticket-IDs oder Datenbank-Namen, die Rückschlüsse erlauben.
3. Beispiele aus der Ursprungs-Session paraphrasieren, nicht wörtlich zitieren, wenn sie
   Persönliches enthalten.
4. Im Zweifel: Skill per `.gitignore` privat halten statt halbherzig anonymisieren.
