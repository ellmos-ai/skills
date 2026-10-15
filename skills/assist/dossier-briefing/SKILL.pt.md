---
name: dossier-briefing
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "Gera um briefing de pesquisa estruturado sobre um tema ou pessoa como esqueleto em Markdown (stdout ou arquivo). Sem armazenamento persistente."
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: pt
visibility: public
translated_from_sha256: dbe880eee63e64ccec3db2527c516d0aace0924b5b7a8137e36639ad7136c356
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:35:20.810240+00:00"
---
<img src="banner.png" width="100%" alt="dossier-briefing banner">

# Dossiê-Briefing

**Briefing de pesquisa estruturado sobre um tema ou uma pessoa**

---

## Visão geral

Gera um briefing em Markdown vazio e estruturado sobre qualquer tema
(pessoa, empresa, evento, conceito). O esqueleto serve como ponto de partida para
uma pesquisa posterior com `research-agent` ou `web-reading`.

---

## Gatilhos

| Frase | Ação |
|---|---|
| „Crie um briefing sobre Marie Curie" | Esqueleto: pessoa, Tipo=person |
| „Dossiê sobre OpenAI" | Esqueleto: empresa, Tipo=organization |
| „Briefing sobre o tema computação quântica" | Esqueleto: tema, Tipo=topic |
| „Prepare um briefing de pesquisa sobre a COP30" | Esqueleto: evento, Tipo=event |

---

## Fluxo de trabalho

1. **Nomear o assunto:** extrair o nome/título do briefing a partir da entrada do usuário.
2. **Identificar o tipo:** person, organization, topic, event (ou unspecified).
3. **Gerar o esqueleto:** criar Markdown com todas as seções relevantes.
4. **Saída:** stdout ou, opcionalmente, gravação em um arquivo (`-o datei.md`).
5. **Iniciar a pesquisa:** passar o esqueleto para `research-agent` ou `web-reading`,
   para preencher as seções que faltam.

---

## CLI

```bash
# Briefing zu stdout
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# In Datei schreiben
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Themen-Briefing
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantencomputing" --typ topic

# Ereignis
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Ohne Typ-Angabe (generisch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Mein Thema"

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## Tipos de briefing e seções

| Tipo | Seções |
|---|---|
| `person` | Dados básicos, Biografia/Contexto, Obra e contribuições, Fontes, Notas |
| `organization` | Perfil, História, Produtos/Serviços, Pessoas-chave, Fontes, Notas |
| `topic` | Visão geral, Contexto/Antecedentes, Desenvolvimento atual, Fontes principais, Questões em aberto, Notas |
| `event` | Dados essenciais, Envolvidos, Cronologia/Contexto, Significado, Fontes, Notas |
| `unspecified` | Visão geral, Contexto, Detalhes, Fontes, Notas |

---

## Armazenamento

Sem armazenamento persistente. O esqueleto é apenas exibido (stdout ou arquivo),
não é guardado em um banco de dados.

---

## Postura

- Sempre enfatizar que o esqueleto está vazio e precisa ser preenchido por meio de pesquisa.
- Nunca inventar ou alucinar conteúdo — fornecer apenas estrutura.
- Em caso de tipo pouco claro, perguntar ou usar `unspecified`.

---

## Privacidade

Sem acesso à rede. Sem armazenamento. Processamento exclusivamente local.

---

## Recursos relacionados

- `research-agent` — preenche o esqueleto do briefing com resultados de pesquisa
- `web-reading` — lê páginas da web e extrai conteúdo para o briefing

---

## Changelog

| Versão | Data | Alteração |
|---|---|---|
| 1.0.0 | 2026-06-22 | Criado a partir de BACH dossier_generator.py v1.0.0; armazenamento removido, generalizado |
