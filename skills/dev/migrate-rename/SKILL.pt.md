---
name: migrate-rename
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-09-06
description: "Renomeação evolutiva de arquivos com arquivos wrapper, mais o padrão conciso MOVED-stub para mudanças completas de pastas/arquivos. Permite renomeações sem quebras abruptas — as referências são atualizadas organicamente pelo uso."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 16d2b6f4499cdc4c454bcd8244fff5811ae232e7703095f43a59eb663238d837
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.342220+00:00"
---
<img src="banner.png" width="100%" alt="migrate-rename banner">

# Renomeação de arquivo com wrapper (migração evolutiva)

> Permite renomeações de arquivos SEM quebras abruptas. As referências são atualizadas organicamente pelo uso diário.

---

## Princípio: migração evolutiva

```
VORHER:                          NACHHER:
alte_datei.md                    neue_datei.md (umbenannt)
   |                                |
   +-- Verweis A                    +-- alte_datei.md (Wrapper)
   +-- Verweis B                           |
   +-- Verweis C                           +-- Log-Tabelle
                                           +-- Anleitung
                                           +-- Link zu neue_datei.md
```

Quem acessar o caminho antigo:
1. Chega ao arquivo wrapper
2. Registra-se no log
3. Corrige a referência que o encaminhou
4. Segue para o arquivo real

---

## Passo a passo

### 1. Renomear o arquivo

```bash
mv alte_datei.md neue_datei.md
```

### 2. Criar o arquivo wrapper

Crie `alte_datei.md` com o seguinte conteúdo:

```markdown
# ALTE_DATEI.md - UMGELEITET

**Status:** Diese Datei wurde umbenannt zu `neue_datei.md`

---

## Migration-Log

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| YYYY-MM-DD | [Name] | Initiale Migration | n/a (Wrapper erstellt) |

---

## Anleitung

1. **Log-Eintrag hinterlassen** (oben in Tabelle)
2. **Herkunft pruefen**: Was hat dich hierher geschickt?
3. **Verweis korrigieren**: Aendere `alte_datei.md` -> `neue_datei.md`
4. **Zur eigentlichen Datei gehen**: `neue_datei.md`

---

**Zieldatei:** `neue_datei.md`
```

### 3. Corrigir imediatamente as referências críticas
- Arquivos de ajuda (documentação primária)
- Referências no system prompt
- Código CLI que usa o caminho diretamente

### 4. Migrar as demais referências de forma evolutiva
O restante é corrigido automaticamente conforme o uso.

---

## Quando usar o método wrapper?

**SIM - wrapper faz sentido:**
- Muitas referências potenciais
- O arquivo é referenciado por diversos parceiros/ferramentas
- Não é um arquivo de sistema crítico

**NÃO - alterar tudo diretamente:**
- Poucas referências, todas conhecidas
- Arquivos de sistema críticos (config, esquema de banco de dados)
- Caminhos críticos para desempenho

---

## Mudança de pasta/arquivo com MOVED-stub

> Formalizado em 2026-09-06 (ticket T-20260906-688261413). Precedente surgido espontaneamente em
> `.ELLMOS.MIGRATED.md` (2026-08-11) e nos stubs `_control-center/_CONTROL` (2026-09-06).

Situação diferente do wrapper acima: aqui uma **pasta inteira** ou um **arquivo sem muitas
referências ativas** é movido por completo para um novo local (consolidação, renomeação,
reorganização do pipeline). Não há log de migração nem "corrigir referência" — apenas um
ponteiro conciso que diz: agora está aqui.

**Diferença em relação ao procedimento wrapper acima:**

| | Wrapper (passos 1-4 acima) | MOVED-stub |
|---|---|---|
| Uso | Arquivo único, muitas referências ativas, que devem se atualizar organicamente | Pasta ou arquivo, mudança completa |
| Conteúdo | Tabela de log de migração, cresce com o uso | Metadados estáticos, 1-3 linhas em texto simples |
| Duração | Até o log indicar: sem novas entradas | Até `remove_when` ser cumprido |

### Nome, local, campos obrigatórios

O esquema completo, o exemplo e a semântica dos campos estão no template ellmos `MOVED-STUB.md`
(`.TOPICS/.AI/_templates/project-docs/MOVED-STUB.md`, não faz parte deste repositório standalone —
o resumo basta aqui):

- **Nome/local:** `<alter-Name>.MOVED.md` fica onde a pasta/arquivo estava **antes**.
- **Campos obrigatórios** (`key: value`, nesta ordem): `moved_to`, `moved_on`, `ticket`,
  `reason`, `moved_by`, `remove_when` (padrão: `90 Tage UND 0 lebende Referenzen`).
- **Depois**, 1-3 linhas de texto simples para as pessoas. Sem log, sem tabela, sem histórico — isso
  fica no ticket referenciado.
- **Remoção:** o stub é **excluído**, nunca arquivado.

### Política

Vinculante como `.SYNC/_policies/library/P-017_umzugs-stub.md`.

### Script de verificação

`scripts/moved_stub_check.py` (nesta pasta de skill) lista todos os stubs `*.MOVED.md`/`*.MIGRATED.md`
a partir de um diretório raiz, informa campos obrigatórios ausentes e marca stubs vencidos para
remoção (mais antigos que `remove_when` dias). Uso:

```bash
python scripts/moved_stub_check.py <wurzelverzeichnis>
```

---

## Limpeza

Após cerca de 30 dias, ou quando o log mostrar que não há mais novas entradas:
1. Mover o arquivo wrapper para `_archive/deprecated/`
2. Ou excluí-lo por completo (se não houver mais entradas)

---

## Changelog

### 1.1.0 (2026-09-06)
- Seção "Mudança de pasta/arquivo com MOVED-stub" adicionada (ticket T-20260906-688261413):
  formaliza o ponteiro conciso de mudança para pastas/arquivos inteiros (padrão `<alter-Name>.MOVED.md`,
  campos obrigatórios moved_to/moved_on/ticket/reason/moved_by/remove_when), delimitado em relação ao
  procedimento wrapper acima. Script de verificação `scripts/moved_stub_check.py` adicionado.

### 1.0.0 (2026-03-15)
- Portado do BACH v3.8.0

---

*Portado do BACH v3.8.0 | Versão standalone*
