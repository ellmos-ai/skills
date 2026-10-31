---
name: folder-organization
version: 1.1.0
type: protocol
author: Lukas Geiger + OpenAI Codex
created: 2026-08-24
updated: 2026-08-24
description: "Organizar pastas e arquivos de forma semântica: reconhecer regras locais e taxonomia existente, atribuir arquivos por conteúdo, preservar conjuntos relacionados, arquivar sequências claras de predecessores/sucessores e logs, separar conteúdos mistos válidos e obsoletos por meio de Cut-and-Clue e mover candidatos a exclusão para uma lixeira de revisão reversível. Use esta skill para „organizar pasta“, „classificar arquivos de forma sensata“, „arquivar versões antigas“, „limpar arquivos de log“, „separar conteúdos obsoletos e válidos“ ou quando, durante a organização, surgirem arquivos de segredos ou segredos em um armazenamento em nuvem. Ela funciona de forma neutra quanto a fornecedores e usuários, apenas com recursos próprios; módulos compatíveis ou serviços de arquivos reconhecidos são usados apenas como aceleradores opcionais. Para regras de agrupamento recorrentes já totalmente definidas, use, em vez disso, uma automação de arquivos baseada em regras; para a reestruturação de uma arquitetura inteira de projeto, use um otimizador de pipeline/projeto."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: utilities
tags: [ordner, dateien, sortierung, archivierung, versionen, logs, geheimnisse, cloud, cut-and-clue, cleanup, standalone]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: ffe1a25ac259cfb78124036afbaf7b8b99b9e6c1dcb181f7d6d8f3d34da1ab2c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="folder-organization banner">

# Organização de Pastas

## Objetivo e Limite

Produza um arranjo rastreável, no qual cada alteração seja justificada por regras locais, conteúdo,
relações entre arquivos ou uma decisão explícita do usuário. A skill é um protocolo de ordenação
semântica, não um segundo programa de movimentação de arquivos e não exige vínculo com nenhum fornecedor.

Um levantamento ou uma verificação permanece somente leitura. Uma solicitação explícita como „organize
esta pasta“ autoriza movimentações seguras e reversíveis dentro da área indicada, desde que não haja
ambiguidade não resolvida. Sobrescrever, excluir definitivamente, mover para fora da área, reescrever
conteúdo ou ativar uma automação permanente exige uma liberação separada.

## Núcleo Autônomo e Seeds Opcionais

Comece sempre pelo núcleo autônomo. Ele exige apenas leitura, escrita, hashing e operações comuns com
arquivos. Para um levantamento reproduzível, está disponível [`scripts/folder_organization.py`](scripts/folder_organization.py);
padrões seguros e substituições estão em [`config.json`](config.json). Por padrão, o script
escreve apenas na saída padrão. `--out` pode criar exclusivamente um novo arquivo fora da raiz
examinada; destinos existentes não são sobrescritos. Seus achados de log e de versão são pistas de baixa
confiança, não uma autorização para arquivar.

A versão da biblioteca possui front matter de catálogo ampliado. Caso um sistema de destino aceite apenas
front matter básico portável (`name`, `description`), [`scripts/export_portable.py`](scripts/export_portable.py)
gera uma cópia independente em uma nova pasta de destino. O fluxo funcional e todas as peças locais de
substituição permanecem integralmente nela.

Depois, descubra capacidades, não nomes de marcas. Uma integração existente pode melhorar o núcleo, mas
não altera significado nem permissão:

| Capacidade necessária | Substituto autônomo | Adaptador/seed opcional reconhecido |
|---|---|---|
| Inventário, hashes, plano | script Python incluído ou busca nativa de arquivos | planejamento/recibos do FolderHome |
| Conteúdo de documentos/OCR | leitor local existente; caso contrário `unreadable/review` | doc-services ou extrator equivalente |
| Operações seguras em nuvem/com bloqueio | operação nativa com nova verificação de estado | FileCommander ou adaptador próprio do provedor |
| Regras estáveis recorrentes | configuração emitida como proposta | file-collect-sort-action ou automação equivalente |
| Reindexar pistas | marcadores CLUE chamativos no texto | Gardener ou outro indexador local |

Os componentes Ellmos são, portanto, **Grounding Seeds**: quando suas capacidades estiverem disponíveis
e liberadas para a tarefa, use seus controles mais fortes. Se não estiverem presentes, execute o mesmo
fluxo funcional de forma heurística e com as peças substitutas desta skill. Nenhuma transmissão externa
ocorre apenas porque falta um leitor local.

## Procedimento

### 1. Definir raiz, regras e modo

- Escolha a menor raiz comum de organização; não examine uma raiz inteira de usuário ou de nuvem por comodidade.
- Leia os arquivos de controle na raiz e acima dela, como `AGENTS.md`, `CLAUDE.md`,
  `README.md`, `START.md`, regras de nomenclatura, registros, manifestos e bloqueios.
- Registre o modo: ordenação semântica única, manutenção do arquivamento, manutenção de logs, Cut-and-Clue ou
  preparação de uma regra recorrente.
- As pastas de destino existentes e o seu uso real têm mais peso do que uma taxonomia ideal inventada.

### 2. Política de segredos antes de qualquer acesso ao conteúdo

Antes de abrir ou calcular o hash, verifique o nome contra `secret_policy.protected_name_patterns` e as exclusões em
`config.json`. Arquivos protegidos como `.env`, chaves privadas ou arquivos de credenciais
devem ser registrados somente por caminho e metadados; seu conteúdo não pode chegar ao contexto do modelo,
ao relatório ou a logs. `--hash-all` não suspende essa fronteira. Se um sinal de segredo for
detectado por acaso em um arquivo normalmente legível, interrompa a exibição do conteúdo e informe apenas o
ID do sinal.

Se o achado provavelmente estiver em uma raiz de nuvem/sincronização, aplica-se a `cloud_action`
configurada. O padrão é `localize-after-approval`: comprovar um destino local fora de todas as raízes de
sincronização e permissões restritivas, executar dry-run e obter aprovação, copiar o arquivo de forma opaca
e verificar internamente por hash, somente então substituir a origem na nuvem de modo recuperável e deixar
um ponteiro não secreto. Sem `local_secret_root` definido, ou com referências de execução em risco, bloqueie.

A transação completa, os modos de ponteiro (`control-file`, `sidecar`, `placeholder`),
o mapa local de ponteiros, as orientações de rotação e os bloqueios rígidos estão em
[`references/secrets-policy.md`](references/secrets-policy.md). Arquivos suspeitos de conter segredos devem ficar fora da ordenação
normal, do arquivamento, do Cut-and-Clue e da lixeira até a decisão da política.

### 3. Levantar inventário e relações

Registre caminho, tamanho, data de alteração, tipo e, na medida proporcional, SHA-256. Em documentos ambíguos,
leia o conteúdo ou os metadados. Arquivos binários ilegíveis permanecem explicitamente não esclarecidos;
nome e extensão sozinhos não justificam uma ação irreversível.

Trate arquivos relacionados como conjunto: versões em idiomas diferentes, origem/exportação, Markdown/PDF,
documento/recursos, dados/script/resultado, anexo/arquivo principal e predecessor/sucessor. Antes de mover,
verifique links, manifestos, inclusões, referências em código e registros.

Para a matriz detalhada de evidências e confiança em acervos difíceis, leia
[`references/heuristics.md`](references/heuristics.md).

### 4. Planejar a estrutura de destino e as decisões individuais

Derive a estrutura de destino a partir da finalidade, das regras existentes e dos agrupamentos reais. A raiz
é uma superfície de roteamento, não um depósito permanente. Não crie pastas genéricas como `_Sonstiges`
quando o achado for semanticamente indefinido; use `review/` ou uma lista de decisões para isso.

Cada alteração planejada contém, no mínimo:

| Campo | Conteúdo |
|---|---|
| Origem | caminho relativo exato e, opcionalmente, hash |
| Destino/ação | `keep`, `move`, `rename`, `archive`, `trash-review`, `cut-and-clue`, `review` |
| Justificativa | regra, conteúdo, relação ou indício de versão |
| Confiança | alta, média ou baixa |
| Efeito colateral | links, conjuntos, registros ou automações afetados |

- **Alta:** regra local explícita, referência clara em manifesto ou sequência de sucessão claramente comprovada.
- **Média:** forte correspondência de conteúdo ou agrupamento existente, mas sem regra explícita.
- **Baixa:** apenas nome, extensão, data de alteração ou semelhança incerta. Não mover automaticamente.

Antes de qualquer mutação, apresente um dry-run completo. Colisões, links simbólicos, bloqueios de nuvem,
arquivos ilegíveis e destinos fora da raiz bloqueiam a ação correspondente.

### 5. Arquivar versões e logs

Só arquive um arquivo antigo como predecessor quando a sequência estiver comprovada por vários sinais:
identificador de versão/data, versão interna declarada, alta sobreposição de conteúdo, finalidade compatível
e um sucessor claramente válido. A data de alteração sozinha não basta. Estados probatórios referenciados e
publicações liberadas permanecem preservados.

Nos logs, distinga entre log de execução ativo, log de auditoria/prova e histórico rotacionável. Não mova logs
ativos ou ainda em escrita. Arquive logs antigos e concluídos segundo a convenção local, caso contrário, por
exemplo, em `_archive/logs/<jahr>/`, com hash e local de origem. A compactação é uma decisão separada; arquivar não
significa excluir automaticamente.

### 6. Aplicar Cut-and-Clue

Se um arquivo contém ao mesmo tempo conteúdo válido e conteúdo obsoleto, mover tudo às cegas é tão errado quanto
manter tudo. Nesse caso, **recorte** o conteúdo válido para um ou mais novos arquivos canônicos e deixe, no material
antigo e, quando necessário, diretamente no ponto problemático, um **Clue** legível por máquina indicando status,
motivo e sucessor. Somente após verificar a integridade arquive o original.

Os marcadores, as regras para `[sic]`, binários e a proteção contra perda de histórico estão em
[`references/cut-and-clue.md`](references/cut-and-clue.md). `[sic]` marca um erro citado de propósito; para
obsolescência use `OUTDATED` ou `SUPERSEDED`.

### 7. Lixeira de revisão em vez de exclusão

Mova candidatos a exclusão, dentro da raiz, para uma pasta de execução como `_trash_review/<run-id>/`. Mantenha a
estrutura relativa e grave `MANIFEST.md` ou `RESTORE.json` com origem, novo caminho, hash, motivo e
momento. Nada disso é excluído definitivamente de forma automática. Assim, o usuário pode revisar toda a execução
e depois removê-la ou revertê-la.

Se existir uma pasta de entrada monitorada, crie a lixeira e o arquivo fora da sua área de varredura, para evitar
realimentação.

### 8. Executar e comprovar

- Imediatamente antes de cada ação, verifique novamente origem, hash, destino e ausência do destino.
- Nunca sobrescreva; em caso de colisão, bloqueie ou use um novo nome explicitamente planejado.
- Após a execução, leia o estado final do destino, compare hashes, procure nomes de caminho antigos em referências
  e atualize os registros afetados.
- Remova apenas pastas vazias criadas por você mesmo. Para cada mutação, preserve um caminho de reversão ou manifesto.
- Reindexe as marcações CLUE quando houver um indexador local; sem indexador, elas permanecem eficazes como texto
  comum e chamativo.

## Exemplos Breves

- `bericht_v1.md` e `bericht_v2.md`: inicialmente apenas marque como possível sequência de versões. Somente a
  versão interna, o conteúdo e as referências decidem se `v1` pode realmente ser arquivado.
- `konzept.md` contém regras válidas e seções obsoletas: transfira integralmente a substância válida para um
  novo arquivo canônico, preserve o original byte a byte e crie Clues/sidecar com o sucessor.
- `.env` em uma raiz de sincronização: não abra nem copie para o relatório. Gere um plano de política;
  sem `local_secret_root` comprovado, aprovação e troca segura em tempo de execução, não altere o arquivo.

## Aprendizado e Automação

Colete as correções do usuário como candidatas a regra, nunca as promova silenciosamente. Somente quando um padrão
for confirmado repetidamente, sem conflitos e com escopo claramente limitado, proponha a partir dele uma automação recorrente.
Toda automação nova ou alterada exige novamente dry-run e aprovação.

## Relatório Final

Além do inventário, das ações, dos arquivos arquivados, da lixeira, dos sucessores de Cut-and-Clue e das decisões
em aberto, informe todos os candidatos a segredo exclusivamente por caminho/ID de sinal, seu status de política,
transferências para a nuvem bloqueadas ou aprovadas, modo de ponteiro e resultado da releitura. Nunca reproduza
valores, caminhos locais de segredos ou linhas de contexto sensíveis.

Informe o inventário inicial, as ações executadas e bloqueadas, os caminhos de arquivo e de lixeira, os sucessores de
Cut-and-Clue, as referências atualizadas, o resultado de hash/releitura, as decisões em aberto e as regras recorrentes
propostas. Um planejamento não é uma organização executada.

## Skills Relacionadas

- Automação de arquivos baseada em regras: para padrões fixos e recorrentes de origem-padrão-destino já conhecidos.
- Otimizador de pipeline/projeto: para a reestruturação estrutural de um projeto ou stack inteiro.
- Tidy-up/Manutenção: para encerramento de sessão, manutenção de registros e arquivos temporários de projeto.
- Achatamento de pastas: somente se a transformação expressamente desejada for justamente achatar.

## Changelog

### 1.1.0 (2026-08-24)

- Política de segredos configurável com não abertura de nomes de arquivos protegidos, detecção aleatória
  redigida e transferência transacional para a nuvem, com mapeamento local e ponteiro não secreto, acrescentada.

### 1.0.0 (2026-08-24)
- Versão inicial neutra quanto a fornecedores e usuários, com script autônomo, princípio opcional de seeds,
  ordenação semântica, arquivamento de versões/logs, Cut-and-Clue e lixeira de revisão.
