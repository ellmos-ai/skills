---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: "Especialista em todo o processo de candidatura. Analisa anúncios de emprego, otimiza perfis (LinkedIn/CV) e gera cartas de apresentação personalizadas. Gera CVs em ASCII a partir de uma base de dados SQLite e de uma estrutura de pastas. O cv_generator.py foi portado de forma autónoma -- não é necessário nenhum runtime do BACH."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: pt
status: active
visibility: public
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
translated_from_sha256: c71218b5c90eba7666db1a407dc59752fa0e2eccd342deb8b728fba82d967e54
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="bewerbungsexperte banner">

> **Alemão** — Versão oficial em alemão.


> **Tradução para inglês** — Versão oficial em inglês de `bewerbungsexperte`.


# ESPECIALISTA EM CANDIDATURAS v1.1 (Alemão)

> O seu parceiro estratégico para o próximo passo na carreira.

## ATIVAÇÃO

```bash
# Beispiel-CV ohne Datenbankzugriff (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# CV aus SQLite-Datenbank generieren (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# CV in Datei speichern (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# Mit Ordner-Scan (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```

## CATÁLOGO DE SERVIÇOS

### 1. Geração de CV (`cv_generator.py`)
- **Dados pessoais:** Ler a partir da tabela `assistant_user_profile` (key/value)
- **Experiência profissional:** Analisar a pasta de empregadores (certificados de trabalho, contratos)
- **Formação:** Analisar a pasta de diplomas
- **Formação contínua:** Analisar a pasta de certificados
- **Referências:** A partir da tabela `contacts` (category='beruflich')
- **Simulação (Dry-Run):** Sem base de dados -- dados de exemplo para testes

### 2. Diagnóstico de vaga
- **Correspondência de palavras-chave:** Comparação do CV com os requisitos da vaga (compatível com ATS)
- **Verificação da empresa:** Pesquisa sobre a cultura empresarial e os benefícios

### 3. Serviço de documentação
- **Ajuste do CV:** Estruturação e objetividade das experiências profissionais
- **Carta de apresentação:** Elaboração de cartas individuais e convincentes
- **Portefólio:** Aconselhamento sobre amostras de trabalho e referências

## TABELAS DA BASE DE DADOS (opcional)

`cv_generator.py` lê a partir destas tabelas, quando existirem:

- `assistant_user_profile` (key TEXT, value TEXT) — Dados pessoais
  - Campos: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — Referências

As tabelas em falta são ignoradas (secções vazias no CV).

## ESTRUTURA DE PASTAS (para --career-path etc.)

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```

## OPÇÕES CLI

```
--db <pfad>           Pfad zur SQLite-Datenbank (Pflicht ohne --dry-run)
--output, -o          Ausgabedatei (ansonsten stdout)
--career-path         Pfad zum Arbeitgeber-Ordner
--education-path      Pfad zum Abschluesse-Ordner
--certs-path          Pfad zum Fortbildungen-Ordner
--dry-run             Beispiel-CV ohne Datenbankzugriff
```

## FLUXO DE TRABALHO: GERAÇÃO DE CV

1. **Preparação**
   - Disponibilizar uma base de dados SQLite (BACH-DB ou própria)
   - Criar a estrutura de pastas com os documentos (opcional)

2. **Teste sem BD**
   - `python cv_generator.py --dry-run` -- verifica se a ferramenta funciona

3. **Geração**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - Verificar o resultado e ajustar, se necessário

4. **Exportação**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## DEPENDÊNCIAS

Apenas a biblioteca padrão do Python: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`.
Não é necessária instalação com pip, nem importação do runtime do BACH.

## REGISTRO DE ALTERAÇÕES

### 1.1.0 (2026-06-22)
- Portado de forma autónoma a partir do BACH v1.0.0
- `--db <pfad>` em vez de um caminho fixo para a BD de origem
- Modo `--dry-run` adicionado
- `--scan-folders` removido (exigia a tabela user_data_folders do BACH)
- Texto do rodapé neutralizado
- Independência do runtime do BACH verificada

### 1.0.0 (2026-01-25, interno ao BACH)
- Versão inicial em BACH system/agents/_experts/bewerbungsexperte/

---
Estado: ATIVO
Domínio: Orientação de carreira
