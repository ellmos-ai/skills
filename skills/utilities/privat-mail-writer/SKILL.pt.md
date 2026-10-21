---
name: privat-mail-writer
version: 0.2.0
type: skill
author: Lukas Geiger + GPT
created: 2026-06-19
updated: 2026-06-19
description: "Esta skill deve ser usada quando o usuário quiser escrever, responder, recusar, fazer follow-up, encurtar, reformular ou rascunhar e-mails privados ou semiformais no próprio estilo, especialmente em casos de compromissos, recusas oficiais, respostas curtas e cordiais e tom dependente do contato. A análise de perfil só deve começar com um pedido concreto de redação de e-mail."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [mail, email, privat, antwort, absage, termin, schreibstil, kontaktprofil]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'optional_tools': [{'name': 'mail-connector', 'path': '.AI/.MODULES/mail-connector/', 'cli': 'mailc', 'python_module': 'mail_connector.cli', 'usage': 'mailc context <kontakt> --mode reply --json  # Liefert Mail-Kontext als JSON für Profilaufbau', 'note': 'Optionales lokales IMAP-CLI-Tool. Nur nutzen wenn installiert (`pip install -e .` im Modulordner). Ohne dieses Tool arbeitet der Skill ohne Mailzugriff.'}], 'services': ['mail-backend-optional'], 'protocols': ['kontaktprofil', 'usecase-registry'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'None', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
translated_from_sha256: 5b685b91dd56efd653a07212eab41a1cca911cbb7f4a049f37a22ff33566c423
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="privat-mail-writer banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `privat-mail-writer`.


# Privat-Mail-Writer (Deutsch)

## Visão geral e finalidade

O Privat-Mail-Writer cria rascunhos de e-mail curtos, cordiais e adequados ao contato. A skill é neutra em relação ao usuário: não contém contatos reais, assinaturas reais nem conteúdo real de e-mails.

O núcleo é lazy e empírico: somente quando o usuário quiser escrever um e-mail concreto para um contato, criar ou atualizar o perfil desse contato específico. Não criar perfis preventivamente. Se não houver histórico de e-mails disponível, não inventar afirmações sobre o estilo; escrever de forma neutra e curta ou pedir exemplos específicos.

## Recursos

- `CONFIG.md` - preferências centrais, regras se-então, portões de permissão e interruptores de lista de bloqueio.
- `BLACKLIST.md` - exclusões para newsletters, remetentes de sistema e contatos sem perfil.
- `USECASES.md` - registro de casos de uso e regras para novos casos de uso.
- `SIGNATURES.md` - regras neutras para assinatura e fórmulas de cumprimento.
- `MUSTER-BLOCKS.md` - blocos de texto curtos e reutilizáveis.
- `kontaktprofile.json` - esquema vazio e neutro para perfis de contato. Manter perfis reais apenas localmente e com economia de dados.

## Fluxo de trabalho

1. **Carregar configuração:** ler `CONFIG.md`. Se a lista de bloqueio estiver ativa, verificar também `BLACKLIST.md`.
2. **Verificar gatilho:** criar perfil somente diante de um pedido concreto de redação para um contato específico, por exemplo "escreva um e-mail para o meu irmão Simon". Não fazer varreduras da caixa de entrada apenas para criar perfis.
3. **Verificar lista de bloqueio:** newsletters, no-reply, remetentes de sistema e domínios/contatos excluídos não recebem perfil de contato. Nesses casos, responder de forma neutra ou não responder.
4. **Identificar a tarefa de e-mail:** determinar objetivo, destinatário, motivo, brevidade desejada, idioma, tom e fatos necessários.
5. **Determinar o caso de uso:** ler `USECASES.md` e selecionar o caso de uso mais adequado. Se nenhum se encaixar, criar um novo caso de uso reutilizável ou, se faltarem informações obrigatórias, fazer uma pergunta breve.
6. **Verificar o perfil de contato:** para cada destinatário não excluído, procurar um perfil existente em `kontaktprofile.json` ou em uma cópia local privada do perfil.
7. **Criar ou atualizar o perfil:** se não houver um perfil confiável, ler até os últimos dez e-mails relevantes com exatamente esse contato no back-end de e-mail disponível. Os e-mails enviados devem ter mais peso para o estilo de escrita do que os recebidos.
8. **Armazenar as evidências:** no perfil de contato, guardar apenas sinais resumidos e verificáveis sobre estilo, relação e categoria. Não armazenar e-mails brutos, longas citações nem detalhes pessoais desnecessários.
9. **Aplicar o portão de permissão:** antes do envio, de conteúdos sensíveis ou da falta de informações obrigatórias, observar os portões de `CONFIG.md`.
10. **Redigir o rascunho:** combinar a forma do caso de uso, o perfil de contato e a tarefa atual. Imitar o estilo sem criar proximidade falsa, compromissos falsos ou motivos não comprovados.
11. **Entregar o resultado:** por padrão, apresentar assunto e corpo do e-mail. Enviar somente se o usuário tiver autorizado explicitamente o envio e houver uma ferramenta de e-mail disponível.

## Perfis de contato

Um perfil de contato descreve não a pessoa em si, mas a relação de comunicação observada e o estilo de escrita do titular da conta em relação a essa pessoa.

Os campos do perfil devem ser concisos:

- último contato
- quantidade e período dos e-mails analisados
- forma de tratamento e cumprimento
- tu/você/grau de formalidade
- extensão das frases e brevidade típica
- grau de afetividade, franqueza e comprometimento
- avaliação da relação com nível de confiança
- categoria do contato, por exemplo `family`, `inner-circle`, `friends`, `colleagues`, `services`, `official`, `unknown`
- fonte da categoria: afirmação do usuário, texto do e-mail, catálogo de endereços, assinatura ou inferência
- grau de evidência da categoria: `user-confirmed`, `strong`, `medium`, `weak`
- breves evidências parafraseadas, como "vários e-mails enviados terminam com 'Viele Grüße'" ou "as respostas ficam abaixo de cinco frases"

Verificar mensalmente se uma checagem de idade está pendente. Se o mês da data atual diferir do `last_age_check` armazenado, excluir os perfis cujo `last_contact_at` tenha mais de um ano e definir `last_age_check` como a data atual. O valor inicial no JSON neutro é `2026-06-18`.

## Regras de estilo

- Escrever de forma curta. E-mails privados raramente precisam de longas introduções.
- Manter a cordialidade, sem explicar em excesso.
- Mencionar motivos reais somente se tiverem sido informados pelo usuário ou forem certos a partir do contexto.
- Em recusas oficiais: educado, claro, sem uma justificativa extensa.
- Em caso de incerteza sobre fatos: fazer uma pergunta breve antes de finalizar o rascunho.
- Escrever textos em alemão com umlauts corretos: ä, ö, ü, Ä, Ö, Ü, ß.

## Novos casos de uso

Se uma tarefa de e-mail parecer reutilizável e ainda não estiver coberta em `USECASES.md`, complementar o caso de uso:

- ID estável, por exemplo `UC-002`
- nome e gatilhos típicos
- objetivo do e-mail
- informações obrigatórias e opcionais
- extensão padrão e tom
- modelo breve ou sequência de blocos
- perguntas em aberto, caso faltem informações obrigatórias

Um caso excepcional único não deve ser transformado em caso de uso. Nesse caso, entregar apenas o rascunho atual.

## Formato de saída

Para rascunhos comuns:

```text
Betreff: ...

Sehr geehrte ...

...

Mit freundlichen Grüßen
[Signatur]
```

Se o usuário quiser apenas o texto, sem assunto, entregar somente o corpo do e-mail. Se houver várias variantes úteis, oferecer no máximo duas: "muito curta" e "um pouco mais calorosa".

## Limites

Não inventar perfis de contato. Não copiar desnecessariamente detalhes confidenciais de e-mails para a resposta. Não enviar e-mails sem autorização explícita. Não formular compromissos jurídicos, médicos ou financeiros, a menos que o usuário os indique claramente.

## Histórico de alterações

### 0.2.0 (2026-06-19)
- Adicionados `CONFIG.md` e `BLACKLIST.md`.
- Criação de perfis limitada a pedidos concretos de redação de e-mail.
- Categorias de contato com fonte e grau de evidência incorporadas ao esquema de perfil.

### 0.1.0 (2026-06-19)
- Versão inicial com registro de casos de uso, regras de assinatura, blocos de modelo e JSON vazio de perfil de contato.
