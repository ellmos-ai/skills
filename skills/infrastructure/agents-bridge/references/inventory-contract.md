# Inventarvertrag

`agents-bridge` verlangt keinen bestimmten Inventarspeicher. Ein vorhandenes
Inventar kann JSON, YAML, SQLite, eine Markdown-Datei oder ein externer Dienst
sein.

## Minimale Felder

| Feld | Bedeutung |
|---|---|
| `system_id` | stabiler Rechner- oder Laufzeitbezeichner |
| `actor_id` | Agent, CLI oder IDE |
| `boot_surface` | erkannter Zielpfad oder Zielkanal |
| `truth_profile_id` | ausdrücklich gewähltes Wahrheitsprofil |
| `strategy` | Redirect, Loader oder Projektion |
| `last_verified_at` | Zeitpunkt des letzten echten Lesetests |
| `status` | entdeckt, geplant, aktiv, stale oder blockiert |

## Zuständigkeit

Das Inventar beschreibt den Zustand; es autorisiert keine Änderungen. Ein
separates Scheduler-, Lease- oder Partnerregister kann regelmäßige Prüfungen
übernehmen. Der Bridge-Skill selbst beansprucht weder Scheduling noch
Cross-System-Ownership.

## Datenschutz

Portable Profile enthalten Platzhalter oder relative Pfade. Persönliche
absolute Pfade, Hostnamen und private Verzeichnisstrukturen gehören in ein
lokales, nicht veröffentlichtes Profil.
