---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "Skill de calendário com seleção de backend adaptativa ao usuário (Flag 3). Padrão: armazenamento SQLite local. Opcional: Google Calendar MCP, Routinika ou UpToday como backend — controlado via assist/prefs.json. Sem preferência, o LLM pergunta ao usuário interativamente."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: pt
status: stable
visibility: public
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
translated_from_sha256: 3dd9e7b8d86095d63dd54e3d9c4c3b825eef0dd3affffd992b54bbc8a03cdd7e
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.305025+00:00"
---
<img src="banner.png" width="100%" alt="kalender banner">

## Finalidade

Registrar, consultar e gerenciar compromissos — com backend selecionável. O core
(`kalender_core.py`) sempre trabalha com o **armazenamento SQLite local** como
padrão. O LLM escolhe, quando necessário, um backend alternativo com base em
`assist/prefs.json`.

**Flag 3 — Escolha de backend:**

| `kalender_backend` em prefs.json | Comportamento |
|---|---|
| `local` (Padrão/Default) | Armazenamento SQLite na pasta do skill |
| `google` | Google Calendar MCP (somente caminho do LLM, não em core.py) |
| `routinika` | Calendário Routinika via module-installer (não implementado na v0.1) |
| `uptoday` | Calendário UpToday via module-installer (não implementado na v0.1) |
| não definido | O LLM pergunta ao usuário interativamente pelo backend preferido |

> `kalender_core.py` implementa exclusivamente o backend `local`.
> Google Calendar MCP e outros backends são controlados pelo LLM e são
> documentados no SKILL.md, não no core.

---

## Gatilhos

| Frase | Ação |
|---|---|
| „Adicionar compromisso" | Registrar novo compromisso |
| „O que tenho hoje?" | Consultar compromissos de hoje |
| „O que tenho esta semana?" | Visão geral de 7 dias |
| „Compromisso [Título] em [Data]" | Criar compromisso com data |
| „Todos os compromissos em [Mês]" | Visão mensal |
| „Excluir compromisso [ID]" | Remover compromisso |
| „Exportar compromissos" | Exportação ICS de todos os compromissos ou de um compromisso individual |

---

## Fluxo de trabalho

1. **Verificar backend**: ler `assist/prefs.json` → `kalender_backend`.
2. **Sem preferência**: o LLM pergunta ao usuário: calendário local, Google Calendar ou outro?
3. **Backend local**: core.py — criar/consultar/excluir compromisso no armazenamento SQLite.
4. **Backend Google**: o LLM chama diretamente o Google Calendar MCP (core.py não participa).
5. **Saída**: lista legível de compromissos ou confirmação.

---

## Ponto de entrada CLI

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

## Armazenamento

| Propriedade | Valor |
|---|---|
| Tipo | SQLite (backend local) |
| Caminho (padrão) | `skills/assist/kalender/store.db` |
| Substituição | `--store <pfad>` ou variável de ambiente `KALENDER_STORE` |
| Tabelas | `events` |

### Esquema

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

## Princípios

- O core implementa somente o backend `local` — leve, sem dependências externas.
- A exportação ICS gera um subconjunto válido da RFC 5545 (VCALENDAR + VEVENT), importável em todos os aplicativos de calendário comuns.
- A importação ICS (parsing) ainda não está implementada na v0.1 — prevista para a v0.2.
- Regras de repetição (`recurrence`/RRULE) são armazenadas, mas não interpretadas — a interpretação está prevista para a v0.2.

---

## Privacidade

- Os compromissos locais permanecem em `store.db` — sem acesso à rede no core.
- No caminho do backend Google Calendar, o Google Calendar MCP processa os dados — aplicam-se as políticas de privacidade do Google.
- `store.db` não deve ser versionado no Git (recomendado: `.gitignore`).

---

## Recursos relacionados

- Google Calendar MCP (`mcp__claude_ai_Google_Calendar__*`) — backend alternativo, controlado pelo LLM
- Skill `assist/haushalt-manager` — integração com Routinika (padrão de verificação de presença)
- `tools/module-installer/module_installer.py` — para futura integração dos backends Routinika/UpToday

---

## Histórico de alterações

| Versão | Data | Alteração |
|---|---|---|
| 0.1.0 | 2026-06-22 | Criação inicial — lógica da Flag 3, backend local, exportação ICS |
