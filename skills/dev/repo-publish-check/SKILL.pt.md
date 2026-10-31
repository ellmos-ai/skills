---
name: repo-publish-check
description: "Verificação neutra quanto ao usuário de repositórios antes de uma publicação ou em uma nova verificação pública. Controla privacidade, segredos, licenças, conteúdos de terceiros, documentação e status de liberação, sem realizar a publicação em si."
version: 1.6.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-09-27
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [release, privacy, license, repository, publication]
language: pt
status: active
visibility: public
dependencies:
  tools: [git, gh]
  services: []
  protocols: []
  python: []
translated_from_sha256: b96efd5a0ae9aa276c3f093eea2f4e712f485ab59d30cc9196d3277224b6f1a2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:37:30.410040+00:00"
---
<img src="banner.png" width="100%" alt="repo-publish-check banner">

# Repo Publish Check

## Finalidade

Verifique um repositório antes da primeira publicação ou em uma reavaliação posterior. Um resultado negativo é admissível. Altere a visibilidade somente quando o proprietário do repositório tiver autorizado isso expressamente.

A skill não elabora pareceres jurídicos. Em um domínio juridicamente sensível ou em um caso individual pouco claro, consulta-se a skill pública `law-checker`. Nem mesmo esta substitui a consultoria jurídica profissional.

## Privacidade para relatórios de verificação

Relatórios de verificação e avaliações de risco não são commitados no repositório verificado. Armazene-os em uma área de verificação privada, separada do projeto, ou use uma pasta ignorada pelo git, como `<private-review-dir>`. Publicamente, apenas as correções necessárias são divulgadas, por exemplo, uma indicação de licença, uma nota de privacidade ou uma descrição mais precisa.

## Fluxo de verificação

1. **Definir o escopo da publicação**
   - Verifique a árvore efetivamente rastreada com `git ls-files`.
   - Exclua notas internas, relatórios, dados de teste, configurações locais e arquivos de bloqueio.
   - Verifique `.gitignore` e as allowlists de pacotes antes do commit.
   - Em bibliotecas de skills (arquivos `SKILL*.md` presentes): cada frontmatter deve ser analisável como YAML. Se `testing/skill_frontmatter_gate.py` existir no repositório, execute-o (`--fix` faz a correção mecânica das aspas, sem alterar o texto); caso contrário, faça uma verificação por amostragem com `yaml.safe_load`.

2. **Varredura de privacidade e de segredos**
   - Pesquise tanto na árvore de trabalho QUANTO em todo o histórico git alcançável (`git log -p --all`) por endereços de e-mail, credenciais, tokens, chaves privadas, caminhos de usuário locais (`C:\Users\<name>`, `_Local_DEV`, `OneDrive`, `CREDENTIALS`) e dados pessoais.
   - Carregue obrigatoriamente os padrões de busca a partir de um arquivo (`grep -f`), nunca como strings inline sujeitas a erro; antes, execute um teste positivo com um caminho de teste.
   - Classifique cada achado como intencional, a ser removido ou como risco residual documentado.
   - Limpe conteúdos históricos problemáticos antes de uma publicação: um achado no histórico NUNCA é resolvido por um simples commit de limpeza, mas exige reescrita do histórico (`git filter-repo`) ou recriação/autorização do usuário.

3. **Licença e proveniência**
   - Deve existir um arquivo `LICENSE` adequado.
   - Documente se a licença abrange código, prompts, documentação e mídia.
   - Inventarie componentes de terceiros e conteúdos incorporados com sua proveniência e licença.
   - Publique componentes alheios somente se a licença e a decisão curatorial de publicação o permitirem.

4. **Finalidade e domínios sensíveis**
   - Descreva com clareza o que o projeto faz e o que não faz.
   - Em direito, saúde, finanças, segurança ou dados pessoais: documente limites, fluxos de dados e usos excluídos.
   - Para questões jurídicas, solicite uma avaliação preliminar atualizada por meio de `law-checker`.

5. **Privacidade e uso de nuvem**
   - Minimize os dados processados.
   - Aponte serviços externos e processamento em nuvem.
   - Oriente os usuários a não publicar dados confidenciais de casos em issues ou discussões públicas.

6. **Avisos sobre IA e produto**
   - Havendo relação com IA, documente a finalidade, o papel do provedor, limites essenciais e os avisos de transparência pertinentes.
   - Não afirme homologação, certificação ou qualidade de verificação que não esteja comprovada.

7. **Nome, banner e apresentação externa**
   - Verifique slugs e nomes de pacotes, bem como possíveis sobreposições de marca.
   - Uma pesquisa comum na web ou em plataformas não substitui uma pesquisa oficial de marcas.
   - README, descrição e badges devem refletir o escopo funcional efetivo.
   - **Verificação obrigatória do banner antes da mudança para public:**
     * Verifique se já existe um banner (`assets/banner*` ou na raiz `banner.*`) e se ele está incluído no `README.md`.
     * Se o banner estiver ausente: geração obrigatória ANTES da publicação!
     * Caminho de geração: Antigravity / Gemini (`generate_image` ou agy CLI — regra padrão: banner/artwork via agy; padrão), caminho alternativo: Codex.
     * Armazenamento em `assets/banner.png` (ou `banner.svg`); verifique a existência e o tamanho do arquivo diretamente no disco (não confie apenas na mensagem de sucesso do modelo).
     * Inclua o banner no topo (centralizado) do `README.md`.

8. **Conclusão e inspeção visual**
   - Abra ativamente para o usuário o banner, o logo e as visualizações web (como a página inicial do repositório ou o perfil da organização) para inspeção visual (`Invoke-Item` ou `Start-Process msedge`), não apenas deixando-os como links no relatório.
   - Documente achados, correções, riscos abertos e um resultado de semáforo no relatório privado de verificação.
   - Verifique novamente o commit final.
   - Obtenha a autorização expressa do proprietário do repositório.
   - Somente então uma etapa separada e autorizada pode alterar a visibilidade para public (`gh repo edit <org>/<repo> --visibility public`).

## Dados de exemplo e de evidência (números de telefone, transcrições, IDs) [C 2026-09-05]

Provas de testes de campo e de ensaio são o caminho mais comum pelo qual dados reais chegam a um repositório público — não credenciais. Verifique, em código, testes, fixtures, documentação **e no histórico git alcançável**:

- **Números de telefone:** apenas faixas de ficção/drama padronizadas e reservadas do respectivo país (DE: reservas da Bundesnetzagentur; nenhum bloco móvel ou fixo plausível). Varredura por regex com **teste positivo** (um número de exemplo inserido deve ser encontrado pela varredura), caso contrário um resultado negativo não tem valor. Formas mascaradas (`+49 17x XXXX`, `+491 ••• •`) são admissíveis.
- **Transcrições e trechos de conversas:** somente como reproduções sintéticas claramente identificadas; sem transcrições brutas, sem nomes, sem carimbos de data/hora exatos, sem fragmentos de números.
- **IDs de provedores:** sem IDs de execução/chamada/pedido (padrão de 32 hex), sem links de painel.
- **Histórico:** se algo desse tipo já tiver sido commitado, um commit de limpeza não basta — é necessária reescrita (`git filter-repo`) mais a purga pelo suporte dos objetos órfãos; depois disso, verifique se as URLs antigas de commit retornam 404. Relate o resultado sem valores (arquivo, linha, contador).

Níveis de resultado como na varredura de credenciais: *bloqueado* (achado real) · *revisar* (suspeito, possivelmente um exemplo) · *limpo*. Caso de referência: CALL-E 2026-08-24/25 (a revisão do mantenedor exigiu três reescritas de histórico).

## Etapas obrigatórias após a mudança para public

Assim que a visibilidade de um repositório for definida como `public` (`gh repo edit <org>/<repo> --visibility public`), as seguintes etapas obrigatórias devem ser cumpridas:

1. **Verificar a completude do banner na release/commit final:**
   - Verifique no GitHub se o banner carrega corretamente no README (sem 404, caminho de branch/asset acessível).

2. **Atualizar o README do perfil da organização (banner + entrada no diretório):**
   - Cada repositório recém-publicado com banner deve ser listado na página de perfil da organização (`<org>/.github/profile/README.md` e `profile/README_de.md`).
   - Verificação mecânica pelo gate do perfil da organização:
     ```bash
     python testing/org_profile_gate.py --org <org>
     ```
   - Se a entrada estiver ausente, o script gera um snippet HTML/Markdown correspondente. Insira-o na galeria de banners da categoria adequada (por exemplo, aplicações especializadas, módulos, orquestração) e inclua o repositório na tabela correspondente dos READMEs de perfil.
   - Envie a alteração por branch e Pull Request contra `<org>/.github` (veja também `github-repo-care`, etapa 14).

3. **Dar a própria estrela:**
   - Após a publicação, para cada repositório público próprio, verifique se a própria conta já deu uma estrela e, se não, adicione-a (por exemplo, via `.GITHUBBOT` `run.py --self-star --repo <org>/<name>` ou `gh api`). Detalhes em `github-repo-care`, etapa 14.

## Reavaliação de repositórios já públicos

Verifique, no mínimo, privacidade e segredos, cobertura de licença, conteúdos de terceiros, avisos legais e apresentação externa. Achados críticos no histórico são comunicados imediatamente ao proprietário do repositório e não são sobrescritos silenciosamente.

Uma organização pode manter uma fila privada e um arquivo próprio de relatórios. Esses itens não pertencem à skill pública. Reavaliações atrasadas podem ser priorizadas conforme risco, visibilidade e idade do último relatório privado de verificação.

## Formato do resultado

```markdown
# Veröffentlichungsprüfung — <Repository>
- Stand: <Commit>
- Modus: vor Veröffentlichung | Nachprüfung
- Privacy/Secrets: grün | gelb | rot
- Lizenz/Drittinhalte: grün | gelb | rot
- Dokumentation/Außendarstellung: grün | gelb | rot
- Korrekturen: <Liste>
- Offene Risiken: <Liste>
- Freigabe: ausstehend | erteilt
```

## Limites

- A skill não publica nada por conta própria.
- Não substitui consultoria jurídica nem pesquisa oficial de marcas.
- Uma varredura de código-fonte sem achados não comprova que cópias públicas anteriores, registros de pacotes ou caches foram limpos.

## Changelog

Detalhes em [CHANGELOG.md](CHANGELOG.md).
