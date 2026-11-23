---
language: fr
---

<img src="banner.png" width="100%" alt="medizin-daten banner">

> **Français** — Version française officielle de la compétence `medizin-daten`.

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
# Diagnose anlegen
python medizin_daten_core.py add-diagnosis "Hypertonie" [--icd I10] [--note "Anmerkung"]

# Diagnosen auflisten
python medizin_daten_core.py diagnoses

# Symptom erfassen
python medizin_daten_core.py add-symptom "Kopfschmerzen" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptomverlauf für eine Bezeichnung
python medizin_daten_core.py symptom-history "Kopfschmerzen" [--limit 30]

# Untersuchung planen
python medizin_daten_core.py add-exam "Blutbild" [--date 2026-07-01] [--note "nüchtern"]

# Anstehende Untersuchungen
python medizin_daten_core.py exams [--upcoming]

# Alternativer Store (z.B. für Tests)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## Stockage

| Propriété | Valeur |
|---|---|
| Type | SQLite |
| Chemin (par défaut) | `skills/assist/medizin-daten/store.db` |
| Surcharge | `--store <pfad>` ou variable d'env `MEDIZIN_STORE` |
| Tables | `diagnoses`, `symptoms`, `examination_plans` |

### Schéma

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (kurz: 8 Hex)
    name        TEXT NOT NULL,        -- Bezeichnung (z.B. "Hypertonie")
    icd_code    TEXT,                 -- ICD-10-Code optional (z.B. "I10")
    onset_date  TEXT,                 -- Beginn (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- Freitext-Notiz
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    name         TEXT NOT NULL,       -- Bezeichnung (z.B. "Kopfschmerzen")
    severity     INTEGER,             -- 1–10 Skala (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 Zeitstempel
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    exam_name    TEXT NOT NULL,       -- Untersuchungsbezeichnung
    planned_date TEXT,                -- Geplantes Datum (ISO-8601)
    done_date    TEXT,                -- Durchgeführt am (NULL = ausstehend)
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