---
name: kalender
version: 0.1.1
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-11-22
description: "Utiliser pour enregistrer, consulter, supprimer ou exporter des rendez-vous au format ICS avec stockage SQLite local et choix de backend (ex. 'ajouter un rendez-vous', 'agenda d'aujourd'hui', 'exporter le calendrier', /kalender). Gère les événements locaux avec Flag 3 de sélection de backend. NE PAS utiliser pour la planification des jalons de projet logiciel (utiliser dev/dev-cycle)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: fr
status: stable
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin vorhanden.\n'}
---

<img src="banner.png" width="100%" alt="kalender banner">

> **Français** — Version française officielle de la compétence `kalender`.

# Calendrier (`kalender`)

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
# Ajouter un rendez-vous
python kalender_core.py add "Dentiste" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Cabinet Dr X"]

# Rendez-vous du jour
python kalender_core.py today

# Aperçu hebdomadaire
python kalender_core.py week [--from 2026-06-22]

# Aperçu mensuel
python kalender_core.py month [--month 2026-07]

# Tous les rendez-vous (avec filtre optionnel)
python kalender_core.py list [--search "Dentiste"] [--limit 50]

# Supprimer un rendez-vous
python kalender_core.py delete <id>

# Export ICS
python kalender_core.py export [--id <id>] [--out kalender.ics]

# Vérifier le backend
python kalender_core.py check-backend

# Stockage alternatif (p. ex. pour les tests)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## Stockage

| Propriété | Valeur |
|---|---|
| Type | SQLite (backend local) |
| Chemin (par défaut) | `skills/assist/kalender/store.db` |
| Surcharge | `--store <chemin>` ou variable d'env `KALENDER_STORE` |
| Tables | `events` |

### Schéma

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (court : 8 hex)
    title        TEXT NOT NULL,         -- Intitulé du rendez-vous
    date         TEXT NOT NULL,         -- Date ISO YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optionnel)
    duration_min INTEGER,               -- Durée en minutes (optionnel)
    location     TEXT,                  -- Lieu (optionnel)
    description  TEXT,                  -- Note / description
    recurrence   TEXT,                  -- ICS RRULE (optionnel, ex. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- UID ICS pour import/export
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