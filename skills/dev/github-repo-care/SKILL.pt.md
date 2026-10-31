---
name: github-repo-care
version: 1.3.1
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-09-27
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: "Protocolo para criar, publicar, lançar, auditar e manter repositórios do GitHub com segurança: verificar regras e bloqueios locais, criar o .gitignore antes do primeiro add, executar verificações de privacidade, preparar README/i18n/banner/metadados, verificar tags de lançamento e releases do GitHub, e atualizar perfis de organizações, arquivos llms.txt e links de registros."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: pt
status: active
visibility: public
dependencies: {'tools': ['git', 'gh', 'rg'], 'services': ['GitHub'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.codex/skills/github-repo-care/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': '2026-06-18', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 9a4401a2244a88c6989c3a69114c9292c405e28fe3d018cd6f832f4c5bd6c1d1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.344178+00:00"
---
<img src="banner.png" width="100%" alt="github-repo-care banner">

# GitHub Repo Care — Publicar e manter repositórios

## Quando esta skill se aplica

Use esta skill quando um repositório do GitHub precisar ser criado, publicado, lançado, auditado ou mantido posteriormente. Ela é especialmente importante antes do primeiro push público, em tags de lançamento, em alterações nos metadados do repositório, em perfis de organização e em verificações de privacidade.

Não se aplica a implementação pura de código sem publicação no GitHub. Nesse caso, use primeiro a skill de desenvolvimento ou depuração adequada e ative esta skill apenas na etapa de publicação.

## Regra central

Prepare o repositório antes do primeiro push público. Uma `.gitignore` correta, uma verificação de privacidade limpa, licença, README, metadados e a narrativa de lançamento são bem mais fáceis de fazer antes do histórico público do que depois.

## Fluxo

1. **Ler as regras locais.** Verifique `AGENTS.md`, `CLAUDE.md`, `START.md`, a política de lançamento, a política de nomenclatura e a política de bloqueios, se existirem.
2. **Verificar bloqueios.** Se `LOCK.txt` ou um `LOCK.*.txt` correspondente estiver ativo, não altere esse escopo.
3. **Definir o nome do repositório.** Registre em uma frase o nome, a organização, a visibilidade, a licença e a finalidade.
4. **Criar `.gitignore` antes de `git add`.** Exclua segredos, dados locais, bancos de dados, saídas de build, ambientes virtuais, caches, arquivos de IDE e notas privadas.
5. **Complementar os básicos públicos.** Tipicamente: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `llms.txt` e CI.
6. **Escrever o README para descoberta.** Primeira tela: finalidade, instalação, uso, modelo de privacidade, estrutura do projeto, licença e nome canônico do repositório.
7. **Definir sinais visuais.** Adicione banner, logo ou captura de tela quando isso tornar o benefício mais reconhecível. Nada de decoração genérica quando for possível usar uma imagem real do produto ou um conceito claro.
8. **Planejar o multilinguismo com intenção.** Mínimo: inglês mais o idioma do projeto. Para módulos voltados ao usuário, preferencialmente: alemão, inglês, espanhol, chinês simplificado, japonês e russo.
9. **Executar testes e smoke tests.** Verifique localmente antes de afirmar sucesso ou criar um lançamento.
10. **Executar a verificação de privacidade.** Verifique o conjunto em stage/tracked: segredos, caminhos locais, PII, `.env`, bancos de dados, documentos privados, artefatos gerados e mojibake.
11. **Commitar e fazer push.** Commite apenas após a verificação ser aprovada. Em seguida, crie ou conecte o repositório no GitHub, faça o push e confira o status do remoto.
12. **Definir metadados.** Verifique descrição, tópicos, homepage, visibilidade e branch padrão.
13. **Criar o lançamento.** Crie a tag e a release do GitHub; verifique a CI para branch e tag.
14. **Atualizar as superfícies de descoberta.** Vincule o perfil da organização, `llms.txt`, registros centrais, índices locais de módulos e READMEs do ecossistema. **Publicar ⇒ página de perfil (T-20260926-796851315):** se o repositório tiver um banner, verifique mecanicamente se ele já aparece na página de perfil da organização (`<org>/.github/profile/README.md`) — `python org_profile_gate.py --org <org>` (`.AI/.SKILLS/testing/`). Se a entrada faltar, o script entrega um snippet Markdown pronto para inserir.
    **Definir a própria estrela (T-20260926-299328659):** o Aftercare verifica, para cada repositório público próprio, se a conta já deu estrela e, caso contrário, a define — pela ferramenta própria de manutenção do GitHub, se houver (caminho e chamada pela configuração local, p. ex. uma flag `--self-star`: sem repositório, uma execução de recuperação em todas as organizações configuradas; com repositório, uma execução individual logo após esta publicação). Nunca remover estrelas automaticamente.
    **Manutenção de stargazers:** seguir os novos stargazers e, quando a qualidade for real, dar estrela de volta ao melhor projeto deles — se a ferramenta própria de manutenção do GitHub já tiver um módulo de reciprocidade, use-o (avalia a relevância temática e sugere dar estrela de volta, convidar, revisar ou pular; executa o seguimento com limites de taxa, cooldown e rede de segurança dry-run/apply/confirm). Não reconstrua se já existir; o próprio módulo registra as decisões. Nunca deixar de seguir ou remover estrelas automaticamente.
15. **Verificar a conclusão.** Confira o README remoto, a página da release, os tópicos, a CI e os links.

## Verificação de privacidade

Pesquise no conjunto staged ou tracked, não apenas na árvore de trabalho visível.

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

Para módulos públicos, documente também um `RELEASE_GATE.md` ou um gate equivalente: data, comandos verificados, resultado, alertas residuais e exceções conscientes. Se um segredo algum dia tiver sido commitado, apagá-lo de `HEAD` não basta; o segredo precisa ser rotacionado.

**Verificar a visibilidade dos repositórios linkados.** Uma varredura de caminhos/tokens não encontra
links para repositórios privados do GitHub em READMEs públicos (caso de estudo
T-20260926-820252321: `ellmos-ai/ellmos-core` aparecia numa tabela de README sem que ninguém percebesse,
embora o repositório seja privado). Se o repositório tiver a verificação reutilizável, execute-a:

```bash
python testing/repo_link_visibility_gate.py --repo .
```

A verificação é fail-open apenas em caso de incerteza real (queda de rede, rate limit
403/429 — apenas um aviso, sem interromper); um 404 bloqueia como um `private: true`
confirmado, pois em ambos os casos o link não pode ser resolvido por terceiros (privado ou inexistente).
Sem esse script (o repositório não tem cópia própria da verificação), revise por amostragem
cada link para repositório de terceiros ou irmão no README com `gh api repos/ORG/REPO --jq .private`.

## Metadados do GitHub

Após o push, defina explicitamente os metadados e o lançamento.

```bash
gh repo edit ORG/REPO --description "Kurze konkrete Beschreibung" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

Depois, verifique:

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

Se a CI ficar vermelha após um lançamento, o repositório ainda não pode ser considerado publicado de forma limpa. Em um lançamento inicial recém-criado, é aceitável mover a nova tag imediatamente e de forma consciente para o commit corrigido.

## Erros comuns

| Erro | Correção |
|---|---|
| `.gitignore` é criado só depois de `git add` | Primeiro faça unstage, corrija as regras de ignore e só então adicione novamente |
| README em um só idioma, embora a UI ou a skill sejam multilíngues | Adicione links de idioma ou READMEs localizados |
| Sem banner, sem tópicos, sem descrição | Complete os recursos de descoberta antes do anúncio |
| A tag de lançamento existe, mas a CI está vermelha | Corrija a CI e verifique a nova execução |
| README da organização atualizado, mas `llms.txt` esquecido | Atualize as duas superfícies, humana e legível por máquina |
| Caminho local na documentação pública | Substitua por caminhos relativos ou exemplos genéricos |
| Repositório público contém banco de dados de teste ou inbox de notebooks | Remova o arquivo do tracking, adicione a regra de ignore e execute o gate novamente |

## Checklist de conclusão

- [ ] Regras locais e bloqueios verificados.
- [ ] `.gitignore` existia antes do primeiro add.
- [ ] Documentos públicos, licença, segurança, contribuição, changelog e `llms.txt` presentes.
- [ ] README contém nome do repositório, finalidade, instalação, uso, privacidade e licença.
- [ ] Expectativa de i18n atendida.
- [ ] Banner, logo ou captura de tela presente, quando fizer sentido.
- [ ] Testes e smoke tests aprovados.
- [ ] Varreduras de privacidade, caminhos, segredos, bancos de dados e mojibake limpas.
- [ ] Descrição, tópicos, tag, release e CI do GitHub verificados.
- [ ] Perfil da organização, registro e links do ecossistema atualizados.
- [ ] Banner presente? `org_profile_gate.py --org <org>` executado sem achados para este repositório.

## Changelog

### 1.3.1 (2026-09-27)
- Correção de documentação: a semântica do 404 na descrição do gate de privacidade estava errada. Segundo
  `testing/repo_link_visibility_gate.py`, um 404 (privado ou inexistente) bloqueia como um `private: true`
  confirmado; o fail-open vale apenas para queda de rede e rate limit (403/429). Corrigido na seção
  do gate de privacidade e na entrada do changelog 1.2.0.

### 1.3.0 (2026-09-27)
- Passo 14 ampliado (T-20260926-299328659, pedido do usuário): verificar/definir a própria estrela em
  repositórios públicos próprios e manutenção de stargazers (seguir + estrela de volta por qualidade),
  pela ferramenta própria de manutenção do GitHub, se houver — nenhuma ferramenta específica é exigida.
  Nunca deixar de seguir/remover estrelas automaticamente.

### 1.2.0 (2026-09-26)
- Novo passo do gate de privacidade (T-20260926-820252321): verificar a visibilidade dos repositórios do GitHub
  linkados (`testing/repo_link_visibility_gate.py --repo .`, fail-open em caso de
  rede/rate limit, bloqueia em 404 e `private: true` confirmado). Motivo:
  `ellmos-ai/ellmos-core` (repositório privado) aparecia sem ser notado em uma tabela de README.

### 1.1.0 (2026-09-26)
- Adicionado o passo "Publicar ⇒ página de perfil" (T-20260926-796851315): um repositório com banner deve ser
  verificado contra o README de perfil de sua organização (`<org>/.github/profile/README.md`), de forma mecânica via
  `.AI/.SKILLS/testing/org_profile_gate.py`, e não de memória. Motivo: o banner de zombie-killer-tray nunca
  chegou à página de perfil da org dev-bricks após a publicação.

### 1.0.0 (2026-06-18)
- Versão inicial criada como protocolo de manutenção e publicação de repositórios.
