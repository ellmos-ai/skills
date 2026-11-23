---
language: fr
---

<img src="banner.png" width="100%" alt="kalender banner">

> **Français** — Version française officielle de la compétence `kalender`.

## Objectif

Enregistrer, consulter et gérer des rendez-vous — avec un backend au choix. Le cœur
(`kalender_core.py`) utilise toujours le **stockage SQLite local** par défaut.
Le LLM choisit au besoin un autre backend selon `assist/prefs.json`.

**Flag 3 — Choix du backend :**

| `kalender_backend` dans prefs.json | Comportement |
|---|---|
| `local` (par défaut) | Stockage SQLite dans ce dossier de compétence |
| `google` | Google-Calendar-MCP (voie LLM uniquement, pas dans core.py) |
| `routinika` | Calendrier Routinika via module-installer (non impl. v0.1) |
| `uptoday` | Calendrier UpToday via module-installer (non impl. v0.1) |
| non défini | Le LLM demande interactivement à l'utilisateur son backend préféré |

> `kalender_core.py` implémente exclusivement le backend `local`.
> Google-Calendar-MCP et les autres backends sont pilotés par le LLM et
> documentés dans SKILL.md, pas dans le cœur.

---

## Déclencheurs

| Formulation | Action |
|---|---|
| « Ajoute un rendez-vous » | Enregistrer un nouveau rendez-vous |
| « Qu'est-ce qui est prévu aujourd'hui ? » | Consulter les rendez-vous du jour |
| « Qu'est-ce qui est prévu cette semaine ? » | Aperçu sur 7 jours |
| « Rendez-vous [titre] le [date] » | Créer un rendez-vous avec date |
| « Tous les rendez-vous en [mois] » | Aperçu mensuel |
| « Supprimer le rendez-vous [ID] » | Retirer un rendez-vous |
| « Exporter le rendez-vous » | Export ICS de tous les rendez-vous ou d'un seul |

---

## Flux de travail

1. **Vérifier le backend** : lire `assist/prefs.json` → `kalender_backend`.
2. **Sans préférence** : le LLM demande à l'utilisateur : calendrier local, Google Calendar ou autre ?
3. **Backend local** : core.py — créer/consulter/supprimer le rendez-vous dans le stockage SQLite.
4. **Backend Google** : le LLM appelle directement Google-Calendar-MCP (core.py n'intervient pas).
5. **Sortie** : liste lisible de rendez-vous ou confirmation.

---

## Point d'entrée CLI

```bash
# Termin anlegen
python kalender_core.py add "Zahnarzt" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Praxis Dr. X"]

# Heutige Termine
python kalender_core.py today

# Wochenübersicht
python kalender_core.py week [--from 2026-06-22]

# Monatsübersicht
python kalender_core.py month [--month 2026-07]

# Alle Termine (optional mit Suchbegriff)
python kalender_core.py list [--search "Zahnarzt"] [--limit 50]

# Termin löschen
python kalender_core.py delete <id>

# ICS-Export
python kalender_core.py export [--id <id>] [--out kalender.ics]

# Backend-Check
python kalender_core.py check-backend

# Alternativer Store (z.B. für Tests)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## Stockage

| Propriété | Valeur |
|---|---|
| Type | SQLite (backend local) |
| Chemin (par défaut) | `skills/assist/kalender/store.db` |
| Surcharge | `--store <pfad>` ou variable d'env `KALENDER_STORE` |
| Tables | `events` |

### Schéma

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (kurz: 8 Hex)
    title        TEXT NOT NULL,         -- Termin-Bezeichnung
    date         TEXT NOT NULL,         -- ISO-Datum YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optional)
    duration_min INTEGER,               -- Dauer in Minuten (optional)
    location     TEXT,                  -- Ort (optional)
    description  TEXT,                  -- Notiz/Beschreibung
    recurrence   TEXT,                  -- ICS RRULE (optional, z.B. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- ICS UID für Import/Export
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
```

---

## Posture

- Le cœur implémente uniquement le backend `local` — léger, sans dépendances externes.
- L'export ICS génère un sous-ensemble valide de la RFC 5545 (VCALENDAR + VEVENT), importable dans toutes les applications de calendrier courantes.
- L'import ICS (analyse) n'est pas encore implémenté dans la v0.1 — prévu pour la v0.2.
- Les règles de récurrence (`recurrence`/RRULE) sont enregistrées mais non évaluées — l'évaluation est prévue pour la v0.2.

---

## Confidentialité

- Les rendez-vous locaux restent dans `store.db` — aucun accès réseau dans le cœur.
- Avec la voie du backend Google Calendar, Google-Calendar-MCP traite les données — la politique de confidentialité de Google s'applique.
- Ne pas commiter `store.db` dans Git (recommandé : `.gitignore`).

---

## Ressources associées

- Google-Calendar-MCP (`mcp__claude_ai_Google_Calendar__*`) — backend alternatif, piloté par le LLM
- Compétence `assist/haushalt-manager` — intégration Routinika (modèle Presence-Check)
- `tools/module-installer/module_installer.py` — pour la future intégration des backends Routinika/UpToday

---

## Journal des modifications

| Version | Date | Modification |
|---|---|---|
| 0.1.1 | 2026-11-22 | Avis de langue corrigé |
| 0.1.0 | 2026-06-22 | Création initiale — logique Flag-3, backend local, export ICS |