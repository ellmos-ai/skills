---
name: medizin-daten
version: 0.1.1
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-11-22
description: "Utiliser pour enregistrer de manière locale et strictement privée des données médicales personnelles, diagnostics, historiques de symptômes et plans d'examens (ex. 'noter un diagnostic', 'suivre des symptômes', 'enregistrer un bilan de santé', /medizin-daten). Stocke les données dans une base SQLite locale sans aucun envoi cloud. NE PAS utiliser pour un avis médical à distance ou une urgence médicale."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: fr
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
---

<img src="banner.png" width="100%" alt="medizin-daten banner">

> **Français** — Version française officielle de la compétence `medizin-daten`.

# Données médicales (`medizin-daten`)

## Objectif

Enregistrer des données médicales personnelles de manière sûre et locale : diagnostics
(code CIM-10 optionnel), historiques de symptômes avec séries chronologiques et plans
d'examens. Toutes les données restent exclusivement en local dans `medizin-daten/store.db`.

La compétence ne remplace pas un avis médical et ne formule aucune affirmation
médicale — il s'agit d'un carnet structuré pour les données de santé personnelles.

---

## Déclencheurs

| Formulation | Action |
|---|---|
| « Enregistrer un diagnostic » | Créer un nouveau diagnostic |
| « Ajouter le diagnostic [nom] » | Créer un diagnostic nommé |
| « Historique des symptômes » | Enregistrer les symptômes d'aujourd'hui |
| « Enregistrer le symptôme [nom] » | Saisir un symptôme isolé |
| « Plan d'examens » | Afficher les prochains rendez-vous/examens |
| « Ajouter un rendez-vous » | Saisir un rendez-vous d'examen |
| « Montrer mes diagnostics » | Afficher la liste des diagnostics |

---

## Flux de travail

1. **Détecter le mode** : diagnostic / symptôme / plan d'examens
2. **Structurer la saisie** : date, désignation, notes, code CIM-10 optionnel
3. **Enregistrer** : dans `store.db` (local, aucun accès réseau)
4. **Afficher** : résumé lisible pour le contexte du LLM

---

## Point d'entrée CLI

```bash
# Ajouter un diagnostic
python medizin_daten_core.py add-diagnosis "Hypertension" [--icd I10] [--note "Remarque"]

# Lister les diagnostics
python medizin_daten_core.py diagnoses

# Saisir un symptôme
python medizin_daten_core.py add-symptom "Maux de tête" [--severity 7] [--date 2026-06-22] [--note "..."]

# Historique d'un symptôme
python medizin_daten_core.py symptom-history "Maux de tête" [--limit 30]

# Planifier un examen
python medizin_daten_core.py add-exam "Bilan sanguin" [--date 2026-07-01] [--note "à jeun"]

# Examens à venir
python medizin_daten_core.py exams [--upcoming]

# Stockage alternatif (p. ex. pour les tests)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## Stockage

| Propriété | Valeur |
|---|---|
| Type | SQLite |
| Chemin (par défaut) | `skills/assist/medizin-daten/store.db` |
| Surcharge | `--store <chemin>` ou variable d'env `MEDIZIN_STORE` |
| Tables | `diagnoses`, `symptoms`, `examination_plans` |

### Schéma

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,      -- UUID (court : 8 hex)
    name        TEXT NOT NULL,         -- Désignation (ex. "Hypertension")
    icd_code    TEXT,                  -- Code CIM-10 optionnel (ex. "I10")
    onset_date  TEXT,                  -- Début (ISO-8601, optionnel)
    status      TEXT DEFAULT 'actif',  -- actif | rémission | clôturé
    note        TEXT,                  -- Note libre
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optionnel : rattachement
    name         TEXT NOT NULL,        -- Désignation (ex. "Maux de tête")
    severity     INTEGER,              -- Échelle 1–10 (optionnel)
    recorded_at  TEXT NOT NULL,        -- Horodatage ISO-8601
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optionnel : rattachement
    exam_name    TEXT NOT NULL,        -- Intitulé de l'examen
    planned_date TEXT,                 -- Date prévue (ISO-8601)
    done_date    TEXT,                 -- Réalisé le (NULL = en attente)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## Posture

- Aucune recommandation médicale, aucun diagnostic posé par la compétence.
- Les codes CIM-10 sont enregistrés en texte libre — aucune validation par rapport à une base externe.
- L'échelle de sévérité 1–10 est subjective pour l'utilisateur.
- Les valeurs manquantes (date, sévérité) sont toujours autorisées — le principe du carnet s'applique.

---

## Confidentialité (Privacy-Gate)

> **AVERTISSEMENT : Les données médicales nécessitent une protection particulière.**

- `store.db` contient des données de santé hautement sensibles — **ne jamais commiter dans Git**.
- **Aucun accès réseau** — toutes les opérations s'exécutent entièrement en local.
- **Aucune transmission** à des services externes, aucune synchronisation avec des backends cloud.
- Recommandation de sauvegarde : sauvegarde locale chiffrée (p. ex. `age`/`gpg`).
- Au démarrage, la compétence vérifie si `store.db` se trouve en dehors du système de fichiers local
  et émet un avertissement si le chemin est dans un dossier synchronisé (OneDrive, etc.).
- `~/.gitignore_global` ou le `.gitignore` local doit exclure `store.db`.

---

## Ressources associées

- Compétence `assist/gesundheit` — assistance santé générale (données non médicales)
- MediPlaner (`tools/module-installer` → `mediplaner`) — gestion des médicaments (programme distinct)

---

## Journal des modifications

| Version | Date | Modification |
|---|---|---|
| 0.1.1 | 2026-11-22 | Avis de langue corrigé |
| 0.1.0 | 2026-06-22 | Création initiale — conception originale, Privacy-Gate, schéma à 3 tables |