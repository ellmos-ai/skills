# Changelog — repo-publish-check

## 1.6.0 (2026-09-27)

- Neuer dritter Pflichtschritt nach der Umschaltung auf public (T-20260926-299328659):
  eigenen Stern setzen (`.GITHUBBOT` `run.py --self-star --repo <org>/<name>`, neu gebaut).
  Verweis auf `github-repo-care` Schritt 14, keine eigene Beschreibung — dieselbe
  Nicht-Duplizieren-Logik wie beim Org-Profil-Schritt.

## 1.5.0 (2026-09-26)

- **Zweiter Lehrfall am selben Tag (`accounts-core`):** Der in 1.4.0 gehärtete Grep meldete
  erneut fälschlich "0 Treffer" — echter Fund war `C:\_Local_DEV\repos\accounts-core` in
  `MARKETING-LOG.txt` (Arbeitsbaum) und dreimal in der Historie. Zwei unabhängige Ursachen:
  (1) Muster waren Inline-Strings im Befehl statt aus einer Datei — Backslashes können auf dem
  Transportweg zum Shell-Tool in falscher Anzahl ankommen, ohne dass der Fehler im Editor
  sichtbar wird. (2) Der Pfad-Scan lief nur über die Historie, nicht zusätzlich über den
  Arbeitsbaum.
- Schritt 2 entsprechend verschärft: Muster kommen zwingend aus einer Datei (`grep -f`), nie als
  Inline-String; eine Positivprobe mit einem geplanten Testpfad muss VOR jedem "0 Treffer"
  bestehen; der Scan läuft über Arbeitsbaum UND Historie, nicht nur eine von beiden.
- EN-Fassung synchron gehärtet.

## 1.4.0 (2026-09-26)

- Schritt 2 (Privacy-/Secret-Scan) gehärtet: Pfadmuster-Suche (`C:\Users\<name>`, `_Local_DEV`,
  `OneDrive`, `.docx`/`.xlsx`/`.pdf`, `CREDENTIALS`) läuft jetzt zwingend über dieselbe
  `git log -p --all`-Historie wie der Secret-Muster-Scan, nicht getrennt davon; das Ergebnis
  muss wörtlich im Bericht stehen. Anlass: Der erste Durchlauf auf `doc-services` meldete
  "keine Treffer", weil die Pfadsuche nur den Arbeitsbaum prüfte und der Historien-Scan nur
  Secret-Token — die Kombination fehlte. merge-reviewer fand dabei einen echten historischen
  Pfad (`C:\Users\<name>\OneDrive\Dokumente\<Dokumentname>.docx`, entfernt aus HEAD, aber über
  die Historie weiter erreichbar).
- Klargestellt: ein Historienfund wird NIE durch einen Bereinigungscommit gelöst, nur durch
  Rewrite/Neuanlage/bewusste Nutzerentscheidung.
- Neuer Teilschritt in Schritt 8: Banner (und Web-Ansichten wie Org-Profil/Repo-Seite) werden
  dem Nutzer aktiv zur Sichtprüfung geöffnet (`Invoke-Item`/`Start-Process msedge`), nicht nur
  verlinkt.
- EN-Fassung nachgezogen (war bei 1.1.0/2026-06-18 stehengeblieben): fehlender Abschnitt
  „Sample and Evidence Data" ergänzt (Parität zur DE-Fassung von 2026-09-05), Schritte 2/8
  synchron gehärtet.

## 1.3.0 (2026-09-26)

- Neuer Pflichtschritt vor jeder Umschaltung auf public: Banner-Prüfung/-Generierung
  (Default: agy, Ersatzweg: Codex), Datei-Verifikation auf der Platte statt der
  Erfolgsmeldung.
- Neuer Abschnitt für zwei Pflichtfolgen nach der Umschaltung: Banner-Vollständigkeit
  im finalen Commit verifizieren, Eintrag im Org-Profil-README per PR — Letzteres
  verweist bewusst auf `github-repo-care` Schritt 14 + `org_profile_gate.py`
  (T-20260926-796851315, am selben Tag parallel entstanden) statt den Ablauf
  ein zweites Mal zu beschreiben.
- Anlass: Nutzerauftrag 2026-09-26 (Ticket T-20260926-943955506), erste Anwendung
  auf `ellmos-ai/doc-services`.

## 1.2.0 (2026-09-05)

- Abschnitt „Beispiel- und Evidenzdaten" ergänzt (Telefonnummern, Transkripte,
  Anbieter-IDs, Git-History-Rewrite-Pflicht).

## 1.1.0 und früher

Historie vor Einführung dieser Datei nicht rekonstruiert.
