---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: "Aponta para o módulo autónomo steuer-assistent: uma folha de trabalho local e offline-first para recibos de despesas relacionadas com rendimentos de trabalhador dependente na Alemanha (Werbungskosten) -- registar, somar até ao cêntimo, exportação ZIP privada. Use esta skill quando os recibos de Werbungskosten devem ser preparados de forma estruturada -- com um limite claro: não é aconselhamento fiscal, não há verificação de dedutibilidade, nem criação ou submissão de declaração fiscal (isso acontece via ELSTER ou software aprovado)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: pt
status: active
visibility: public
translated_from_sha256: 0beb350be5741675f21d27461094e9908be7de7c209e659bed7b55ab374c1bb3
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.167620+00:00"
---
<img src="banner.png" width="100%" alt="steuer-assistent banner">

# steuer-assistent -- Skill de referência

Esta skill é uma **referência leve (wrapper)** para o módulo independente e público
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
(licença MIT, público). A skill propriamente dita vive lá -- este repositório
apenas liga e documenta a instalação.

## O que o módulo faz

`steuer-assistent` é um pequeno módulo Python offline-first para recibos de
Werbungskosten (despesas profissionais do trabalhador) categorizados pelo próprio utilizador:

- Registar recibos (categoria, montante, data, nota opcional).
- Somar as Werbungskosten registadas por ano, com precisão de cêntimos.
- Exportar uma folha de trabalho ZIP privada e não oficial (CSV +
  resumo + aviso de não oficialidade, sem os ficheiros dos recibos).
- Armazenamento local (predefinição `%USERPROFILE%\.steuer-assistent\steuer.db`), sem acesso à rede,
  sem upload para a nuvem, sem acesso a bases de dados alheias.

## Limites (importante)

- **Não é aconselhamento fiscal.** O módulo não verifica a dedutibilidade fiscal
  de posições individuais, nem cria ou submete uma declaração de impostos.
- A submissão eletrónica oficial faz-se exclusivamente através do ELSTER ou de
  software para tal aprovado -- não através deste módulo.
- Âmbito: folha de trabalho privada para Werbungskosten de trabalhadores
  dependentes; sem registo de despesas comerciais ou de empresa.

## Instalação (genérica, sem caminhos locais concretos)

1. Clonar o módulo:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <klon-pfad>
   ```
2. Instalar o módulo e verificar:
   ```bash
   cd <klon-pfad>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. Incorporar `<klon-pfad>/SKILL.md` no próprio ambiente de skills (p. ex.
   `~/.claude/skills/steuer-assistent/`). NÃO fazer commit de caminhos locais reais
   ou nomes de hosts num ambiente de skills versionado.
4. Ajustar o caminho do armazenamento, se necessário, via `STEUER_ASSISTENT_DB=<pfad>` ou
   `--store <pfad>`; a predefinição é o diretório do utilizador.
5. Detalhes sobre comandos CLI, privacidade e limites: ver o README do
   repositório do módulo.

## Origem desta skill de referência

Este wrapper foi preparado em 2026-07-23 como entrada de showcase para o
repositório `ellmos-ai/skills`. **Não há duplicação de código** -- a manutenção
e o versionamento permanecem exclusivamente no repositório do módulo
`ellmos-ai/steuer-assistent`.

## Changelog

### 0.1.0 (2026-07-23)
- Skill de referência inicial para `ellmos-ai/steuer-assistent`.
