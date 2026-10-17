---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "Captura local e privada de dados médicos: diagnósticos, históricos de sintomas e planos de exame. Sem origem no BACH — design personalizado com armazenamento SQLite próprio. Estritamente local, sem transferência para a nuvem."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: pt
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
translated_from_sha256: b345b47fc6f0ea659604ac06a0d5bda40fadb7770d2f3b2899ce95ccb9ee463c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="medizin-daten banner">

## Finalidade

Registrar dados de saúde pessoais de forma segura e local: diagnósticos (código ICD-10
opcional), evoluções de sintomas com séries de datas e planos de exame. Todos os
dados permanecem exclusivamente local em `medizin-daten/store.db`.

A skill não substitui aconselhamento médico e não faz afirmações médicas — é um caderno estruturado para dados pessoais de saúde.

---

## Gatilhos

| Frase | Ação |
|---|---|
| „Registrar diagnóstico" | Criar novo diagnóstico |
| „Adicionar diagnóstico [Nome]" | Criar diagnóstico nomeado |
| „Evolução dos sintomas" | Registrar sintomas de hoje |
| „Registrar sintoma [Nome]" | Registrar um sintoma individual |
| „Plano de exames" | Exibir próximos agendamentos/exames |
| „Adicionar agendamento" | Registrar agendamento de exame |
| „Mostrar meus diagnósticos" | Exibir lista de diagnósticos |

---

## Fluxo de trabalho

1. **Reconhecer o modo**: Diagnóstico / Sintoma / Plano de exame
2. **Estruturar a entrada**: Data, designação, notas, código ICD-10 opcional
3. **Salvar**: Em `store.db` (local, sem acesso à rede)
4. **Exibir**: Resumo legível como contexto para LLM

---

## Entrada via CLI

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

## Armazenamento

| Propriedade | Valor |
|---|---|
| Tipo | SQLite |
| Caminho (padrão) | `skills/assist/medizin-daten/store.db` |
| Substituição | `--store <pfad>` ou variável de ambiente `MEDIZIN_STORE` |
| Tabelas | `diagnoses`, `symptoms`, `examination_plans` |

### Esquema

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

## Princípios de conduta

- Sem recomendações médicas, sem estabelecimento de diagnósticos pela skill.
- Códigos ICD-10 são armazenados como texto livre — sem validação contra um banco de dados externo.
- A escala de gravidade de 1 a 10 é subjetiva do usuário.
- Valores ausentes (data, gravidade) são sempre permitidos — vale o princípio do caderno de notas.

---

## Proteção de dados (Privacy-Gate)

> **AVISO: Dados médicos merecem proteção especial.**

- `store.db` contém dados de saúde altamente sensíveis — **nunca versionar no Git**.
- **Sem acesso à rede** — todas as operações ocorrem totalmente localmente.
- **Sem transmissão** a serviços externos, sem sincronização com backends em nuvem.
- Recomendação de backup: backup local criptografado (p. ex. `age`/`gpg`).
- Ao iniciar, a skill verifica se `store.db` está fora do sistema de arquivos local
  e emite um aviso se o caminho estiver em uma pasta de sincronização (OneDrive etc.).
- `~/.gitignore_global` ou `.gitignore` local deve excluir `store.db`.

---

## Recursos relacionados

- Skill `assist/gesundheit` — assistência geral de saúde (não dados médicos)
- MediPlaner (`tools/module-installer` → `mediplaner`) — gerenciamento de medicamentos (programa separado)

---

## Changelog

| Versão | Data | Alteração |
|---|---|---|
| 0.1.0 | 2026-06-22 | Criação inicial — concepção própria, gate de privacidade, esquema de 3 tabelas |
