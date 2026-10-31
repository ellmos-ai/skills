---
name: design-taste-frontend
description: "Habilidade de frontend anti-slop para landing pages, portfólios e redesenhos. O agente lê o briefing, infere a direção de design adequada e entrega interfaces que não parecem templates. Sistemas de design reais quando aplicável, auditoria primeiro em redesenhos e verificação pré-voo rigorosa."
third_party: true
license: MIT
upstream: https://github.com/Leonxlnx/taste-skill
category: dev
language: pt
translated_from_sha256: 7616ab6689efd139d313f95808165c7e4752bd39d50ed6a0533a120b8ff81002
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T01:22:42.649734+00:00"
---
<img src="banner.png" width="100%" alt="taste-skill banner">

# tasteskill: Habilidade de Frontend Anti-Slop

> Landing pages, portfólios e redesenhos. Não dashboards, não tabelas de dados, não UI de produto em várias etapas.
> Cada regra abaixo é **contextual**. Nenhuma delas é aplicada automaticamente. Primeiro leia o briefing e depois utilize apenas o que se encaixa.

---

## 0. INFERÊNCIA DO BRIEFING (Leia o Contexto Antes de Qualquer Coisa)

Antes de mexer em código ou ajustar parâmetros, **infira o que o usuário realmente quer**. A maior parte da saída de design de LLMs é ruim porque o modelo pula para uma estética padrão em vez de ler o contexto.

### 0.A Leia primeiro estes sinais
1. **Tipo de página** - landing (SaaS / consumidor / agência / evento), portfólio (dev / designer / estúdio criativo), redesenho (preservar vs. reformular), editorial / blog.
2. **Palavras de vibe** usadas pelo usuário - "minimalista", "calmo", "estilo Linear", "Awwwards", "brutalista", "consumo premium", "estilo Apple", "lúdico", "B2B sério", "editorial", "de agência", "vidrado", "tech escuro".
3. **Sinais de referência** - URLs que enviaram, capturas de tela coladas, produtos citados, marcas com as quais competem.
4. **Público** - painel de compras B2B vs. consumidor exigente em design vs. recrutador examinando um portfólio. O público define a estética, não o seu gosto.
5. **Ativos de marca já existentes** - logo, cor, tipografia, fotografia. Em redesenhos, são material de partida, não entrada opcional (veja a Seção 11).
6. **Restrições implícitas** - públicos com foco em acessibilidade, setor público, indústrias reguladas, comércio que prioriza confiança, produtos infantis. Essas restrições **SOBREPÕEM** a preferência estética.

### 0.B Emita uma "Leitura de Design" em uma linha antes de gerar
Antes de qualquer código, declare em uma linha: **"Lendo isto como: \<page kind> para \<audience>, com uma linguagem \<vibe>, inclinando-se para \<design system or aesthetic family>."**

Exemplos de leituras:
- *"Lendo isto como: landing de SaaS B2B para compradores técnicos, com linguagem minimalista estilo Linear, inclinando-se para utilitários Tailwind + Geist + movimento contido."*
- *"Lendo isto como: portfólio solo de designer para gestores de contratação, com linguagem editorial / tipografia cinética, inclinando-se para CSS nativo + animação dirigida por scroll + tipografia personalizada."*
- *"Lendo isto como: redesenho de site de serviço público, com linguagem que prioriza confiança, inclinando-se para GOV.UK Frontend ou USWDS."*

### 0.C Se o briefing for ambíguo, faça uma pergunta, não adivinhe
Faça exatamente **uma** pergunta de esclarecimento - nunca um despejo de várias perguntas - e apenas quando a leitura de design realmente divergir. Exemplo: *"Isto deve parecer mais próximo de Linear-limpo ou de Awwwards-experimental?"*

Se você puder inferir com confiança pelo contexto, **não pergunte**. Declare a leitura de design e prossiga.

### 0.D Disciplina Anti-Padrão
Não recorra a: gradientes roxos de IA, hero centralizado sobre malha escura, três cards de funcionalidades iguais, glassmorphism genérico em tudo, microanimações em loop infinito por toda parte, Inter + slate-900. Esses são os padrões dos LLMs. Vá além deles deliberadamente, com base na leitura de design.

---

## 1. OS TRÊS CONTROLES (Configuração Central)

Após a leitura de design, defina três controles. Toda decisão de layout, movimento e densidade abaixo é condicionada por eles.

* **`DESIGN_VARIANCE: 8`** - 1 = Simetria Perfeita, 10 = Caos Artístico
* **`MOTION_INTENSITY: 6`** - 1 = Estático, 10 = Cinematográfico / Física
* **`VISUAL_DENSITY: 4`** - 1 = Galeria de Arte / Arejado, 10 = Cockpit / Dados Compactados

**Linha de base:** `8 / 6 / 4`. Use estes valores, a menos que a leitura de design os sobreponha. Não peça ao usuário para editar este arquivo - as alterações acontecem por conversa.

### 1.A Inferência dos Controles (leitura de design → valores)
| Sinal | VARIÂNCIA | MOVIMENTO | DENSIDADE |
|---|---|---|---|
| "minimalista / limpo / calmo / editorial / estilo Linear" | 5-6 | 3-4 | 2-3 |
| "consumo premium / estilo Apple / luxo / marca" | 7-8 | 5-7 | 3-4 |
| "lúdico / selvagem / Dribbble / Awwwards / experimental / agência" | 9-10 | 8-10 | 3-4 |
| "landing page / portfólio / site de marketing (padrão)" | 7-9 | 6-8 | 3-5 |
| "prioriza confiança / setor público / regulado / crítico para acessibilidade" | 3-4 | 2-3 | 4-5 |
| "redesenho - preservar" | igual ao existente | +1 | igual ao existente |
| "redesenho - reformular" | +2 | +2 | igual ao existente |

### 1.B Predefinições por Caso de Uso
| Caso de uso | VARIÂNCIA | MOVIMENTO | DENSIDADE |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agência / criativo) | 9 | 8 | 3 |
| Landing (Consumo premium) | 7 | 6 | 3 |
| Portfólio (Designer / estúdio) | 8 | 7 | 3 |
| Portfólio (Desenvolvedor) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Serviço de setor público | 3 | 2 | 5 |
| Redesenho - preservar | igual | igual+1 | igual |
| Redesenho - reformular | +2 | +2 | igual |

### 1.C Como os Controles Dirigem a Saída
Use estes valores (ou os valores sobrepostos pelo usuário) como variáveis globais. As referências cruzadas ao longo deste documento apontam para esses nomes exatos de variáveis - nunca invente aliases como `LAYOUT_VARIANCE` ou `ANIM_LEVEL`.

---

## 2. MAPA DO BRIEFING → SISTEMA DE DESIGN

Depois de ter a leitura de design (Seção 0) e os controles (Seção 1), escolha a base certa. Não invente CSS para coisas que têm um pacote oficial. Não finja que uma tendência estética é um sistema oficial.

### 2.A Quando recorrer a um sistema de design real (use pacotes oficiais)
| O briefing sugere… | Recorra a | Motivo |
|---|---|---|
| Microsoft / SaaS corporativo / dashboards | `@fluentui/react-components` ou `@fluentui/web-components` | Fluent UI oficial, tokens da Microsoft, acessibilidade resolvida |
| UI com cara de Google, produto em Material | `@material/web` + tokens Material 3 | Oficial, temável via Material Theming |
| Estilo IBM B2B / análise corporativa | `@carbon/react` + `@carbon/styles` | Carbon oficial, padrões maduros de densidade de dados |
| Superfícies de app Shopify | `polaris.js` web components / Polaris React | Obrigatório para a UI de admin do Shopify |
| Produto estilo Atlassian / Jira | `@atlaskit/*` + `@atlaskit/tokens` | DS oficial da Atlassian |
| Ferramenta de desenvolvedor estilo GitHub / página da comunidade | `@primer/css` ou `@primer/react-brand` | Primer oficial; variante Brand para marketing |
| Serviço do setor público britânico | `govuk-frontend` | Esperado legal / regulatoriamente |
| Setor público americano / que prioriza confiança | `uswds` | Idem |
| MVP rápido para negócio local / agência | Bootstrap 5.3 | Simples, rápido, funciona |
| Base React moderna e acessível | `@radix-ui/themes` | Primitivas + tema refinado |
| SaaS moderno onde você controla os componentes | shadcn/ui (`npx shadcn@latest add ...`) | Você é dono do código, fácil de customizar; nunca entregue o estado padrão |
| SaaS moderno baseado em Tailwind / marketing de IA | Utilitários Tailwind v4 + variante `dark:` | Padrão para projetos de equipes pequenas e independentes |

**Regra de honestidade:** se o briefing corresponder a um dos sistemas acima, instale e use o pacote **oficial**. Não recrie o CSS dele à mão. Não importe os tokens de um sistema e depois sobrescreva 90% deles.

**Um sistema por projeto.** Não misture Fluent React com Carbon na mesma árvore. Não importe componentes do shadcn/ui em um app Material 3.

### 2.B Quando o briefing é uma estética, não um sistema
Para essas direções, **não há um único pacote oficial**. Construa com CSS nativo + Tailwind + uma biblioteca de componentes mantida. Seja honesto nos comentários do código sobre o que é inspiração emprestada versus material oficial.

| Estética | Implementação honesta |
|---|---|
| Glassmorphism / "vidro fosco" | `backdrop-filter`, bordas em camadas, sobreposições de destaque. Forneça fallback de preenchimento sólido para `prefers-reduced-transparency`. |
| Bento (grades de blocos estilo Apple) | CSS Grid com células de tamanhos mistos. Nenhuma biblioteca única possui isso. |
| Brutalismo | CSS nativo, monoespaçado, bordas cruas. Sem biblioteca. |
| Editorial / revista | Tipografia serifada, grade assimétrica, espaço em branco generoso. Sem biblioteca. |
| Tech escuro / hacker | Mono + neon de destaque, motivos de terminal. Sem biblioteca. |
| Aurora / gradientes de malha | SVG ou gradientes radiais em camadas. Sem biblioteca. |
| Tipografia cinética | Animações CSS nativas, animações dirigidas por scroll, GSAP para sequestros de rolagem. Sem biblioteca. |
| **Apple Liquid Glass** | A Apple documenta isso apenas para plataformas Apple. **Não existe `liquid-glass.css` oficial.** Implementações web são aproximações usando `backdrop-filter` + bordas em camadas + destaques. Rotule claramente como aproximação. |

---

## 3. ARQUITETURA PADRÃO E CONVENÇÕES

A menos que a leitura de design escolha um sistema de design real (Seção 2.A), estes são os padrões:

### 3.A Stack
* **Framework:** React ou Next.js. Padronize Server Components (RSC).
  * **SEGURANÇA DO RSC:** Estado global funciona APENAS em Client Components. No Next.js, envolva os providers em um componente `"use client"`.
  * **ISOLAMENTO DE INTERATIVIDADE:** Qualquer componente que use Motion, listeners de scroll ou física de ponteiro DEVE ser uma folha isolada com `'use client'` no topo. Server Components renderizam apenas layouts estáticos.
* **Estilização:** **Tailwind v4** (padrão). Tailwind v3 apenas se o projeto existente exigir.
  * Para v4: NÃO use o plugin `tailwindcss` em `postcss.config.js`. Use `@tailwindcss/postcss` ou o plugin Vite.
* **Animação:** **Motion** (a biblioteca antes conhecida como Framer Motion). Importe de `motion/react` (`import { motion } from "motion/react"`). O pacote `framer-motion` ainda funciona como alias legado - prefira `motion/react` em código novo.
* **Fontes:** Sempre use `next/font` (Next.js) ou hospede localmente com `@font-face` + `font-display: swap`. Nunca carregue Google Fonts via `<link>` em produção.

### 3.B Estado
* `useState` / `useReducer` locais para UI isolada.
* Estado global APENAS para evitar prop-drilling profundo - Zustand, Jotai ou context do React.
* **NUNCA** use `useState` para acompanhar valores contínuos dirigidos pela entrada do usuário (posição do mouse, progresso do scroll, física de ponteiro, hover magnético). Use `useMotionValue` / `useTransform` / `useScroll` do Motion. `useState` re-renderiza a árvore React a cada mudança e colapsa no mobile.

### 3.C Ícones
* **Bibliotecas permitidas (ordem de prioridade):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Desencorajado:** `lucide-react`. Aceitável apenas quando o usuário pedir explicitamente ou o projeto já depender dela.
* **NUNCA crie ícones SVG à mão.** Se um glifo estiver faltando, instale uma segunda biblioteca ou componha a partir de primitivas - não desenhe caminhos de ícones do zero.
* **Uma família por projeto.** Não misture Phosphor com Lucide na mesma árvore de componentes.
* **Padronize `strokeWidth` globalmente** (por exemplo, `1.5` ou `2.0`).

### 3.D Política de Emojis
Desencorajados por padrão em código, marcação e texto visível. Substitua símbolos por glifos de bibliotecas de ícones. **Exceção:** permita emojis apenas quando o usuário pedir explicitamente uma vibe lúdica / de chat / nativa de redes sociais - e, mesmo assim, use-os com moderação e intenção.

### 3.E Responsividade e Mecânica de Layout
* Padronize os breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Contenha os layouts de página usando `max-w-[1400px] mx-auto` ou `max-w-7xl`.
* **Estabilidade da Viewport:** NUNCA use `h-screen` para seções Hero de altura total. SEMPRE use `min-h-[100dvh]` para evitar saltos de layout no mobile (barra de endereço do iOS Safari).
* **Grid acima de matemática com Flex:** NUNCA use matemática complexa de porcentagens em flexbox (`w-[calc(33%-1rem)]`). SEMPRE use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).

### 3.F Verificação de Dependências (obrigatória)
Antes de importar QUALQUER biblioteca de terceiros, verifique `package.json`. Se o pacote estiver ausente, mostre primeiro o comando de instalação. **Nunca** presuma que uma biblioteca existe.

---

## 4. DIRETRIZES DE ENGENHARIA DE DESIGN (Correção de Viés)

LLMs tendem a clichês. Sobrescreva esses padrões proativamente. Cada regra tem um caminho de exceção sensível ao contexto.

### 4.1 Tipografia
* **Display / Títulos:** Padrão `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Corpo / Parágrafos:** Padrão `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Escolha de fonte sem serifa:**
  * **Desencorajada como padrão:** `Inter`. Escolha primeiro `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, ou uma serifa adequada à marca.
  * **Exceção:** Inter é aceitável quando o usuário pedir explicitamente um visual neutro / padrão / estilo Linear, ou quando o briefing for um site de setor público / que prioriza acessibilidade.
* **Combinações a conhecer:** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.

* **DISCIPLINA DE SERIFAS (MUITO DESENCORAJADA COMO PADRÃO):**
  * Serifa é **muito desencorajada como fonte padrão para qualquer projeto.** "Parece criativo / premium / editorial" NÃO é motivo para recorrer à serifa. O modelo mental padrão do agente de que "briefing criativo = serifa" é o sinal de IA mais testado em rodadas de produção.
  * **Serifa só é aceitável quando UMA destas condições for explicitamente verdadeira:**
    - O briefing da marca cita literalmente uma fonte serifada, OU
    - A família estética é genuinamente editorial / de luxo / publicação / manuscrito / herança / vintage E você consegue articular por que esta serifa específica combina com esta marca específica
  * Para todo o resto (agência criativa, estúdio de design, marca moderna, consumo premium, portfólio, lifestyle), **display sem serifa por padrão** (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). Fontes display sem serifa não são "sem graça" — são o padrão pela mesma razão que o preto é o padrão na moda.
  * **REGRA DE ÊNFASE (relacionada):** Quando quiser enfatizar uma palavra dentro de um título (o movimento cinético "e design `spatial`"), use **itálico ou negrito da MESMA fonte**. NÃO injete uma palavra em serifa aleatória em um título sem serifa (ou vice-versa) só para adicionar interesse visual. Ênfase com famílias misturadas é amadora. Ênfase em itálico/negrito na mesma família é o caminho certo.
  * **Especificamente PROIBIDAS como padrão:** `Fraunces` e `Instrument_Serif` (as duas serifas de display favoritas dos LLMs).
  * **Se uma serifa for justificada** (raro, conforme acima), faça rodízio entre este conjunto, NÃO reutilize a mesma serifa em projetos consecutivos: PP Editorial New, GT Sectra Display, Cardinal Grotesque, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.

* **FOLGA PARA DESCENDENTES EM ITÁLICO (obrigatória):** Quando itálico for usado em tipografia de display e a palavra contiver uma letra com descendente (`y g j p q`), `leading-[1]` ou `leading-none` cortará o descendente. Use `leading-[1.1]` no mínimo e adicione uma reserva de `pb-1` ou `mb-1` no elemento que contém o texto. Audite cada palavra em itálico nos títulos de display antes de entregar.

### 4.2 Calibração de Cor
* No máximo 1 cor de destaque. Saturação < 80% por padrão.
* **A REGRA DO LILÁS:** A estética "brilho roxo / azul de IA" é desencorajada como padrão. Nada de brilhos automáticos em botões roxos, nada de gradientes neon aleatórios. Use bases neutras (Zinc / Slate / Stone) com destaques singulares de alto contraste (Esmeralda, Azul Elétrico, Rosa Profundo, Laranja Queimado, etc.).
* **Exceção:** se a marca ou o briefing pedir explicitamente roxo / violeta / lilás, abrace. Mas execute com intenção: paleta consistente, neutros harmonizados, gradientes contidos. Nada de gradiente genérico de IA.
* **Uma paleta por projeto.** Não alterne entre cinzas quentes e frios dentro do mesmo projeto.
* **TRAVA DE CONSISTÊNCIA DE COR (obrigatória):** Uma vez escolhida a cor de destaque para uma página, ela é usada na página INTEIRA. Um site em cinza quente não ganha de repente um CTA azul na seção 7. Um site com destaque em rosa não ganha um badge de status em verde-azulado no rodapé. Escolha um destaque, trave-o e audite cada componente antes de entregar.

* **BANIMENTO DA PALETA DE CONSUMO PREMIUM (obrigatório, segundo sinal de IA mais recorrente):**
  * Para briefings de consumo premium (utensílios de cozinha, bem-estar, artesanato, luxo, artesanato herdado, produtos domésticos DTC etc.) o padrão dos LLMs é **bege/creme quente + latão/argila/vermelho-sangue/ocre + texto espresso/tinta escura**. Famílias de hex concretamente proibidas como fundos e destaques padrão:
    - Fundos: `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb` (todos "papel quente / creme / giz / osso")
    - Destaques: `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621` (todos "latão / argila / vermelho-sangue / ocre")
    - Texto: `#1a1714`, `#1a1814`, `#1b1814` (todos "espresso / preto quente")
  * Esta paleta é PROIBIDA como escolha padrão para briefings de consumo premium. Cada site de consumo premium que você já entregou usou exatamente esta paleta. A marca fica invisível.
  * **Alternativas padrão (faça rodízio, não reutilize):**
    - **Luxo Frio:** cinza-prateado + cromo + fumaça (pense em Tesla, Apple Watch sem o couro Hermès)
    - **Floresta:** verde profundo + osso + destaque âmbar (pense em Filson, Patagonia premium)
    - **Preto e Tan:** preto genuíno + tan quente, contraste nítido, sem bege
    - **Cobalto + Creme:** azul saturado contra um único neutro, sem latão
    - **Terracota + Ardósia:** ferrugem quente contra cinza frio, sem latão
    - **Oliva + Tijolo + Papel:** oliva suave com destaque em vermelho-tijolo
    - **Monocromático puro + um pop saturado:** off-white + off-black + um destaque vibrante (azul elétrico, esmeralda, rosa-choque etc.)
  * **Regra de rodízio de paleta:** se o último projeto de consumo premium que você gerou usou a família bege+latão, este DEVE usar outra família. Não entregue a mesma paleta artesanal quente duas vezes seguidas.
  * **Exceção:** a paleta bege+latão+espresso só é aceitável QUANDO o briefing da marca nomear explicitamente essas cores, ou quando a identidade da marca for genuinamente vintage / artesanal / de artesanato quente E você conseguir articular por que esta paleta específica combina com esta marca específica. Recorrer a ela por padrão porque "isto é um briefing de utensílios de cozinha" é proibido.

### 4.3 Diversificação de Layout
* **ANTI-VIÉS DE CENTRALIZAÇÃO:** Seções Hero / H1 centralizadas são evitadas quando `DESIGN_VARIANCE > 4`. Force "Tela Dividida" (50/50), "Conteúdo alinhado à esquerda / recurso alinhado à direita", "Espaço em branco assimétrico" ou estruturas fixadas ao scroll.
* **Exceção:** hero centralizado é aceitável para briefings editoriais / manifesto / anúncio de lançamento em que a própria mensagem é o design.

### 4.4 Materialidade, Sombras, Cards
* Use cards APENAS quando a elevação comunicar hierarquia real. Caso contrário, agrupe com `border-t`, `divide-y` ou espaço negativo.
* Quando uma sombra for usada, tinja-a com a tonalidade do fundo. Nada de sombras projetadas em preto puro sobre fundos claros.
* Para `VISUAL_DENSITY > 7`: contêineres de card genéricos são proibidos. Métricas de dados respiram em layout simples.
* **TRAVA DE CONSISTÊNCIA DE FORMA (obrigatória):** Escolha UMA escala de raio de canto para a página e mantenha-a. Opções: tudo reto (raio 0), tudo suave (raio 12-16px), tudo em pílula (raio total para interativos). Sistemas mistos são permitidos apenas quando houver uma regra documentada (por exemplo, "botões são pílula, cards têm 16px, inputs têm 8px") e essa regra for seguida em todo lugar. Botões redondos em um layout quadrado, ou cards quadrados em uma página de botões em pílula, é design quebrado.

### 4.5 Estados Interativos da UI
LLMs tendem a entregar apenas o "estado estático de sucesso". Sempre implemente os ciclos completos:
* **Carregamento:** Loaders esqueleto que correspondam à forma do layout final. Evite spinners circulares genéricos.
* **Estados Vazios:** Bem compostos; indicam como preencher.
* **Estados de Erro:** Claros, inline (formulários) ou contextuais (toasts apenas para eventos transitórios).
* **Feedback Tátil:** Em `:active`, use `-translate-y-[1px]` ou `scale-[0.98]` para simular um pressionar físico.
* **VERIFICAÇÃO DE CONTRASTE DE BOTÃO (obrigatória, a11y):** Antes de entregar qualquer botão, verifique se o texto do botão é legível sobre o fundo do botão. Botão branco + texto branco, CTA `bg-white` com rótulo `text-white`, botão transparente sobre o fundo da página sem borda → todos proibidos. Audite cada CTA: razão de contraste WCAG AA mínima (4,5:1 para corpo, 3:1 para texto grande de 18px+). A mesma regra vale para botões ghost sobre fundos fotográficos (use um backdrop, véu ou contorno).
* **PROIBIÇÃO DE QUEBRA DE LINHA EM CTA (obrigatória):** O texto do botão DEVE caber em uma linha no desktop. Se um rótulo como "VER TRABALHOS SELECIONADOS" quebrar em 2 ou 3 linhas, o botão está quebrado. Corrija ENCURTANDO o rótulo (no máximo 3 palavras para CTAs primários, idealmente 1-2) OU alargando o botão (não restrinja artificialmente `max-width` em CTAs). CTAs quebrados no desktop são uma Falha no Pré-Voo.
* **SEM INTENÇÃO DE CTA DUPLICADA (obrigatória):** Dois CTAs com a mesma intenção em uma página é uma Falha no Pré-Voo. Exemplos de mesma intenção: "Entre em contato" + "Fale conosco" + "Vamos conversar" + "Iniciar um projeto" + "Comece algo" + "Entrar em contato" = todos intenção "contato" → escolha UM rótulo e use-o em todo lugar da página (nav, hero, rodapé). O mesmo vale para "Experimente grátis" + "Comece agora" + "Cadastre-se grátis" (todos intenção "cadastro") e "Ver trabalhos" + "Ver trabalhos selecionados" + "Navegar pelos projetos" (todos intenção "portfólio"). Um rótulo por intenção.
* **VERIFICAÇÃO DE CONTRASTE DE FORMULÁRIO (obrigatória, a11y):** Campos de entrada, texto de placeholder, anéis de foco, texto de ajuda e texto de erro passam todos no contraste WCAG AA contra o fundo da seção. Placeholders claros em um formulário quase branco, formulário branco em seção de página branca, rótulos de formulário mais cinzentos que 4,5:1 de contraste → todos proibidos. Audite cada formulário antes de entregar.

### 4.6 Padrões de Dados e Formulários
* Rótulo ACIMA do campo. Texto de ajuda opcional, mas presente na marcação. Texto de erro ABAIXO do campo. `gap-2` padrão para blocos de entrada.
* Nada de placeholder como rótulo. Nunca.

### 4.7 Disciplina de Layout (Regras Rígidas. Falhar em qualquer uma delas é entregar trabalho quebrado)

* **O Hero DEVE caber na viewport inicial.** Título com no máximo 2 linhas no desktop, subtexto com no máximo **20 palavras** E no máximo 3-4 linhas, CTAs visíveis sem rolar. Se o texto for longo demais: reduza a escala da fonte OU corte o texto. Se você não consegue descrever a proposta de valor em 20 palavras de subtexto, a proposta de valor não está clara, e a regra não está apertada demais. Nunca deixe o hero transbordar e obrigar a rolar para encontrar o CTA.
* **Disciplina de escala de fonte no hero.** Planeje o tamanho da fonte e o tamanho da imagem *juntos*. Se o ativo do hero for grande e o título tiver mais de 6 palavras, não comece em `text-7xl/text-8xl`. Faixa padrão sensata: `text-4xl md:text-5xl lg:text-6xl` para a maioria dos heroes; `text-6xl md:text-7xl` apenas quando o título tiver 3-5 palavras. Um título de hero de 4 linhas é sempre um erro de tamanho de fonte, nunca um erro de tamanho de texto.
* **LIMITE DE PADDING SUPERIOR DO HERO (obrigatório):** Padding superior do hero máximo `pt-24` (≈6rem) no desktop. Mais do que isso significa que o conteúdo do hero flutua na metade da viewport e parece um bug de layout, não um espaço intencional. Se o hero precisar de mais espaço para respirar, aumente a escala da fonte ou o tamanho do ativo, não o padding superior.
* **DISCIPLINA DE PILHA DO HERO (máximo 4 elementos de texto).** O hero é um momento único, não uma lista de funcionalidades. Elementos de texto permitidos, máximo 4 no total:
  1. Eyebrow (rótulo pequeno em maiúsculas) OU faixa de marca OU nenhum - escolha zero ou um
  2. Título (máximo 2 linhas, veja acima)
  3. Subtexto (máximo 20 palavras, máximo 4 linhas)
  4. CTAs (1 primário + máximo 1 secundário)
  - **PROIBIDO no hero:** tagline minúscula abaixo dos CTAs ("Funciona com GitHub, GitLab e Git self-hosted"), micro-faixa de confiança ("Usado por equipes de engenharia em..."), teaser de preço ("Grátis para uso solo, R$ 50/usuário para equipes"), lista de tópicos de funcionalidades, fileira de avatares de prova social. Todos esses vão para seções dedicadas logo abaixo do hero.
  - Se você tiver um eyebrow E uma tagline abaixo dos CTAs no mesmo hero, remova a tagline. Se tiver uma faixa de marca E uma tagline, remova a tagline. Um pequeno elemento de texto por hero, no máximo.
* **O muro de logos "Usado por" / "Confiado por" fica ABAIXO do hero, nunca dentro dele.** O hero é para a proposta de valor e o CTA primário. O muro de logos é uma seção separada logo abaixo. Não enfie logos de confiança na mesma linha flex do texto do hero.
* **A navegação DEVE renderizar em uma única linha no desktop.** Se os itens não couberem em `lg` (1024px), condense os rótulos, remova itens secundários ou mude para hambúrguer. Uma navegação de duas linhas no desktop é design quebrado.
* **Altura máxima da navegação: 80px no desktop, padrão 64-72px.** Nada de barras de navegação "de agência" enormes que consomem 15% da viewport.
* **Grades bento DEVEM ter ritmo, não repetição unilateral.** Não empilhe 6 linhas de imagem à esquerda / texto à direita. Varie a composição: alterne linhas de recurso em largura total, tamanhos de tile assimétricos, quebras verticais.
* **REGRA DA CONTAGEM DE CÉLULAS BENTO (obrigatória):** Uma grade bento tem EXATAMENTE tantas células quanto conteúdo você tem. 3 itens → 3 células (divisão 1+2, ou 2+1, ou trio assimétrico). 5 itens → 5 células (2+3, 3+2, hero+4 etc.). Se a grade tiver uma célula vazia no meio ou no fim, você planejou errado. Refaça a grade; não cole um tile em branco.
* **Proibição de repetição de layout de seção.** Uma vez que você use uma família de layout para uma seção (por exemplo, cards-de-imagem-em-3-colunas, citação em largura total, texto-e-imagem divididos), essa família pode aparecer no máximo UMA vez na página. "Encomendas selecionadas" não pode parecer com "O que fazemos". Uma landing page com 8 seções deve usar pelo menos 4 famílias de layout diferentes.
* **LIMITE DE ALTERNÂNCIA EM ZIGUEZAGUE (obrigatório).** Layout em zigue-zague alternando "imagem à esquerda + texto à direita" e depois "texto à esquerda + imagem à direita" é banal. No máximo 2 seções seguidas com esse padrão de divisão imagem+texto. A 3ª divisão imagem+texto consecutiva é uma Falha no Pré-Voo. Quebre o padrão com uma seção de largura total, uma seção de pilha vertical, uma grade bento, um marquee ou uma família de layout diferente.
* **CONTENÇÃO DE EYEBROW (obrigatória, a regra mais violada em testes de produção).** Um "eyebrow" é o rótulo pequeno em maiúsculas com tracking largo que fica acima de um título de seção (por exemplo, `FOUR COLORWAYS`, `SELECTED WORK`, `THE HARDWARE`, `Git-native task management`). Assinatura CSS típica: `text-[11px] uppercase tracking-[0.18em]`, `font-mono text-[10.5px] uppercase tracking-[0.22em]`. Todo site construído por IA coloca um eyebrow acima de CADA cabeçalho de seção, produzindo o mesmo ritmo de template. Regra rígida:
  - **No máximo 1 eyebrow a cada 3 seções.** O hero conta como 1. Então uma página com 9 seções pode usar no máximo 3 eyebrows no total.
  - Se a seção A tiver um eyebrow, as 2 seções seguintes não podem ter.
  - **A verificação de pré-voo é mecânica:** conte instâncias de `uppercase tracking` (ou rótulos mono em versalete semelhantes acima de títulos) em todos os componentes de seção. Se a contagem for > ceil(contagemDeSeções / 3), a saída falha.
  - **O que fazer no lugar de um eyebrow:** remova totalmente. O título sozinho basta. Se precisar categorizar uma seção, a localização da seção na página já a categoriza; nenhum rótulo é necessário.
* **PROIBIÇÃO DE CABEÇALHO DIVIDIDO (obrigatória).** O padrão "título grande à esquerda + parágrafo explicativo pequeno à direita" como cabeçalho de seção (coluna esquerda col-span-7/8, coluna direita col-span-4/5 com um parágrafo de corpo pequeno flutuando) é **proibido como padrão**. Seções devem ter UMA mensagem focada. Se você realmente precisar de um título e um parágrafo explicativo, empilhe-os verticalmente (título em cima, corpo embaixo, largura máxima 65ch). Recorra ao padrão de cabeçalho dividido apenas quando houver um motivo composicional real (por exemplo, a coluna direita carrega um elemento visual ou interativo, não apenas texto de preenchimento).
* **Diversidade de Fundo em Bento (obrigatória).** Seções bento e de grade de recursos não podem ser 6 cards branco-sobre-branco com texto dentro. Pelo menos 2-3 células em qualquer grade multicélula precisam de variação visual real: uma imagem real, um gradiente adequado à marca (não roxo de IA), um padrão, um fundo tingido. Um bento creme-sobre-creme apenas com tipografia dentro parece o padrão de IA entediante, mesmo quando o resto da página é bom.
* **O colapso no mobile deve ser explícito por seção.** Para cada layout de várias colunas, declare o fallback `< 768px` no mesmo componente. Nada de suposições do tipo "vai funcionar, o Tailwind resolve".

### 4.8 Estratégia de Imagens e Ativos Visuais

Landing pages e portfólios são **produtos visuais**. Páginas só de texto com divs que imitam screenshots são lixo.

**Ordem de prioridade para ativos visuais:**
1. **Ferramenta de geração de imagens primeiro.** Se QUALQUER ferramenta de geração de imagens estiver disponível no ambiente (`generate_image`, ferramenta de imagem via MCP, geração integrada à IDE, ferramentas de imagem da OpenAI etc.) você DEVE usá-la para criar ativos específicos por seção: fotografia de hero, fotos de produto, texturas de fundo, imagens de atmosfera. Gere na proporção certa para a seção. Não pule esta etapa porque CSS feito à mão parece mais rápido.
2. **Imagens reais da web em segundo.** Quando nenhuma ferramenta de geração estiver disponível, use fontes de fotografia reais. Padrões aceitáveis:
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` para fotografia de placeholder (o seed deve descrever a seção, por exemplo `marrow-cookware-kitchen`)
   * URLs reais de estoque ou de marca quando o briefing as fornecer
   * Fontes de licença aberta (Unsplash via URL direta, Pexels) se explicitamente permitidas
3. **Último recurso: avise o usuário.** Se nenhuma opção for possível, NÃO preencha a página com ilustrações SVG feitas à mão nem com "capturas de tela falsas" feitas de divs. Em vez disso, deixe slots de placeholder claramente rotulados (`<!-- TODO: hero product photo, 1600x1200 -->`) e, no fim da resposta, diga: *"Esta página precisa de imagens reais em: \[lista de posições\]. Por favor, gere-as ou forneça-as."*

**Mesmo sites minimalistas precisam de imagens reais.** Uma página só de texto não é minimalismo. É trabalho incompleto. Até um site editorial estilo Linear precisa de pelo menos 2-3 imagens reais (hero, uma foto de produto/lifestyle, uma imagem de apoio). Gere fotografia minimalista em preto e branco se o briefing for contido; não pule as imagens por completo só porque o controle está baixo.

**Logos reais de empresas para prova social.** Quando o briefing pedir um muro de logos "Confiado por / Usado por / Clientes", NÃO recorra a marcas tipográficas de texto simples (`<span>Acme Co</span>` estilizado em linha). Use logos SVG reais:
* **Fonte: Simple Icons** (`https://cdn.simpleicons.org/{slug}/ffffff` para qualquer cor, ou o pacote npm `simple-icons`). Cobre a maioria das marcas conhecidas.
* **Alternativa: devicon** para logos de stack tecnológica (`@svgr/cli` ou CDN).
* **Inventou o nome da marca? Então invente também uma marca SVG.** Gere um monograma simples (uma letra em um círculo, uma ligadura de duas letras, um glifo abstrato) renderizado como `<svg>` inline combinando com o estilo da página. Marcas tipográficas de texto simples para nomes de marca inventados parecem genéricas.
* **Sempre** garanta que os logos renderizem tanto no modo claro quanto no escuro (branco sobre escuro, preto sobre claro, ou variável de tema de cor única).
* **Regra SÓ-LOGO (obrigatória):** muro de logos = logos e nada mais. NÃO imprima rótulos de setor / categoria abaixo de cada logo (nada de `Vercel` + `hosting` embaixo, nada de `Stripe` + `payments`, nada de `Cloudflare` + `infra`). O logo é a credibilidade; o rótulo não acrescenta nada que o usuário já não saiba. Opcional: nome da marca como texto alternativo para leitores de tela, link opcional para o site da marca. Só isso.

**Ilustrações feitas à mão:**
* Ícones SVG de bibliotecas: tudo bem (veja a Seção 3.C).
* SVGs decorativos feitos à mão (ilustrações personalizadas, logos, marcas): **fortemente desencorajados**, nunca como padrão. Aceitáveis apenas quando:
  - O briefing pedir explicitamente ("desenhe um logo SVG para mim")
  - For uma marca geométrica única e simples (um quadrado, um círculo, uma marca tipográfica em display)
  - Você estiver confiante na qualidade da saída
  
**Capturas de tela falsas feitas de divs são proibidas.** Uma "prévia de produto feita à mão" renderizada com retângulos `<div>`, listas de tarefas falsas, dashboards falsos, janelas de terminal falsas é um Sinal. Se você precisa mostrar um produto:
* Use uma URL real de captura de tela, se existir
* Gere uma via ferramenta de imagem
* Use uma prévia real de componente (uma versão mini real da UI dentro da página)
* Ou pule a prévia por completo e use fotografia editorial

**O hero precisa de um visual real.** Texto + mancha de gradiente não é um hero — é um placeholder.

### 4.9 Densidade de Conteúdo

Landing pages vivem da **primeira impressão**, não da leitura completa. Corte sem piedade.

* **Forma de conteúdo padrão por seção:** título curto (≤ 8 palavras) + subparágrafo curto (≤ 25 palavras) + um ativo visual OU um CTA. Qualquer coisa além disso precisa se justificar pela função da seção.
* **Nada de seções que despejam dados.** Uma tabela de publicações com 20 linhas, uma lista de prêmios com 30 linhas, uma matriz de preços gigante em uma página de marketing = layout errado. Use:
  - Top 3-5 destaques + link "Ver lista completa"
  - Marquee / carrossel para amplitude
  - Uma página totalmente diferente se os dados forem o produto
* **Listas longas precisam de outro componente de UI, não de uma lista maior.** O padrão preguiçoso é `<ul>` com marcadores / linhas `divide-y`. Se você tiver mais de 5 itens, recorra a um destes:
  - Divisão em 2 colunas com itens agrupados
  - Grade de cards com imagem + rótulo por item
  - Abas / acordeão se os itens forem categorizáveis
  - Pílulas de rolagem com snap horizontal
  - Carrossel para listas de amplitude (depoimentos, logos, capacidades)
  - Marquee para "muitas-coisas-que-não-precisam-de-atenção-individual"
  Uma ficha técnica com 10 linhas e uma linha fina sob cada linha é o PIOR padrão. Ou agrupe as linhas em 2-3 blocos com divisórias esparsas, ou passe para um layout de card por especificação.
* **Fichas técnicas especificamente (o padrão de utensílios Marrow).** Uma tabela longa de especificações de produto com `border-b` em cada linha é o padrão de IA para briefings de utensílios de cozinha / hardware / vestuário / produtos artesanais. Proibido. Alternativas concretas:
  - **Grade de cards em 2 colunas:** cada especificação ganha seu próprio card, com o nome da especificação, o valor (número de display grande) e um corpo de uma linha de "por que importa". Cards dispostos em 2 colunas no desktop, 1 coluna no mobile.
  - **Pílulas horizontais com snap de rolagem:** cada especificação é uma pílula, o usuário pode navegar por elas.
  - **Blocos agrupados:** agrupe 10 especificações em 3 clusters lógicos (por exemplo, "Materiais", "Cozimento", "Garantia"), cada cluster recebe UMA divisória suave e um título de cluster.
  - **Destaque-vs-restante:** 3-4 especificações principais visualizadas como blocos de display grandes, o restante recolhido sob uma divulgação "Ver especificações completas".

* **AUTOAUDITORIA DE TEXTO (obrigatória antes da entrega):** Antes de declarar qualquer tarefa concluída, releia cada string visível da página (títulos, subtítulos, eyebrows, rótulos de botões, texto corrido, legendas, textos alternativos, texto do rodapé, mensagens de erro). Sinalize qualquer string que seja:
  - **Gramaticalmente quebrada** ("grátis em seu passado", "dois planos mas um é honesto", "colocar isso na mesa" fora de contexto)
  - **Com referentes pouco claros** ("pretendemos continuar assim" sem contexto prévio)
  - **Com cara de alucinação de IA** (trocadilhos fofos mas errados, metáforas forçadas que não se sustentam, frases de "nada elegante")
  - **Que soa como um LLM tentando parecer pensativo** (humildade passivo-agressiva, rótulos de artesão falso, micro-metacomentários poéticos)
  Reescreva cada string sinalizada. Se não tiver certeza de que uma string faz sentido, substitua-a por uma frase funcional e simples. Texto fofo gerado por IA é pior que texto sem graça.
* **Números falsamente precisos são sinalizados.** Números como `92%`, `4.1×`, `48k`, `5.8 mm`, `13.4 lb` ou:
  - Vêm de dados reais (briefing, diretrizes de marca, métricas públicas) - tudo bem
  - Estão explicitamente rotulados como simulados (`<!-- mock -->`, "exemplo", "dados de amostra") - tudo bem
  - São estética de especificação inventada por IA - proibidos. Não falsifique precisão de engenharia que a marca não afirma.
* **Um registro de texto por página.** Não misture mono técnico ("47 tarefas · 0,6 trocas de contexto/dia"), prosa editorial e impacto de marketing na mesma composição, a menos que a voz da marca exija isso explicitamente.

### 4.10 Citações e Depoimentos

* **No máximo 3 linhas** de corpo de citação. Nunca 6. Se a citação original for maior → corte. Uma citação em landing page é um trecho, não a avaliação completa.
* Para tamanhos de fonte muito pequenos (por exemplo, depoimentos no estilo rodapé), o limite de linhas pode se alongar um pouco. Espírito: "cabe em um relance".
* **Sem travessões dentro do texto da citação** como floreio de design (pausas longas, travessões cinéticos, marcadores com travessão). Veja a Seção 9.G - o travessão é completamente proibido.
* Atribuição: nome + cargo + (opcionalmente) empresa. Nunca apenas o nome ("- Sarah").
* Aspas: use aspas tipográficas reais ( " " ) ou nenhuma. Não use aspas ASCII retas ( " ).

### 4.11 Trava de Tema da Página (Consistência entre Modo Claro e Escuro)

A página tem UM tema. As seções não invertem.

* Se a página estiver em modo escuro, TODAS as seções estão em modo escuro. Nenhuma seção de papel quente em modo claro intercalada entre seções escuras (ou vice-versa). O usuário não deve sentir que entrou em outro site no meio da rolagem.
* A exceção: se o briefing pedir explicitamente um dispositivo "História em Blocos de Cor" ou "Troca de Tema ao Rolar" E isso for uma composição deliberada (uma troca completa de tema com uma transição forte, não alternância aleatória), é permitido uma vez por página.
* Comportamento padrão: escolha claro, escuro ou automático (`prefers-color-scheme`) no nível da página e trave. Variações de fundo por seção dentro da mesma família de tema são aceitáveis (`bg-zinc-950` ao lado de `bg-zinc-900`); passar para `bg-amber-50` no meio de uma página `bg-zinc-950` é quebrado.
* Ao usar um sistema de design com temas embutidos (Radix Themes, shadcn/ui com `<Theme>`), defina o tema UMA vez em `layout.tsx` ou na raiz da página. Não deixe seções individuais sobrescreverem.

---

## 5. PROATIVIDADE SENSÍVEL AO CONTEXTO

Estas são ferramentas, não padrões. Use-as quando a leitura de design pedir. **Nenhuma delas é disparada automaticamente.**

* **Liquid Glass / Glassmorphism:** Apropriado para consumo premium, adjacente à Apple, marca de luxo ou vibes de sobreposição de mídia. Inadequado para dashboards, setor público ou "B2B entediante". Quando usado, vá além de `backdrop-blur`: adicione uma borda interna de 1px (`border-white/10`) e uma sombra interna sutil (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) para refração física da borda. Forneça um fallback de preenchimento sólido sob `prefers-reduced-transparency`.
* **Micro-física Magnética:** Use quando `MOTION_INTENSITY > 5` E o briefing for premium / lúdico / de agência. Implemente EXCLUSIVAMENTE com `useMotionValue` / `useTransform` do Motion, fora do ciclo de renderização do React. Nunca `useState`. Veja a Seção 3.B.
* **Micro-interações Perpétuas** (Pulso, Máquina de Escrever, Flutuação, Brilho, Carrossel): Use quando `MOTION_INTENSITY > 5` E a seção se beneficiar ativamente do movimento (indicadores de status, feeds ao vivo, sensação de IA). **Nem todo card precisa de um loop infinito.** Se uma seção for informativa, deixe-a parada. Aplique Física de Mola (`type: "spring", stiffness: 100, damping: 20`) - nada de easing linear.
* **"Movimento declarado, movimento mostrado."** Se `MOTION_INTENSITY > 4`, a página precisa realmente se mover: transições de entrada no hero, revelação ao rolar em seções-chave, física de hover em CTAs, no mínimo. Uma página estática que afirma `MOTION_INTENSITY: 7` está quebrada. Por outro lado, se você não conseguir entregar movimento funcional no escopo disponível, reduza o controle para 3 e entregue uma página estática limpa. Nunca construa movimento pela metade que quebra (ScrollTriggers cortados, entradas com trancos, limpezas ausentes).
* **MOVIMENTO DEVE TER MOTIVO (obrigatório).** Antes de adicionar qualquer animação, pergunte: "o que esta animação comunica?" Respostas válidas: hierarquia (direcionar a atenção para a coisa certa), narrativa (revelar conteúdo em sequência que acompanha uma história), feedback (reconhecer uma ação do usuário), transição de estado (mostrar que algo mudou). Resposta inválida: "ficou legal". GSAP em todo lugar só porque o GSAP está disponível é amadorismo. Cada ScrollTrigger, cada marquee, cada seção fixada precisa de um motivo. Se você não consegue articular o motivo em uma frase, remova a animação.
* **MARQUEE: NO MÁXIMO UM POR PÁGINA (obrigatório).** Marquees de texto com rolagem horizontal ("logos rolando sem fim", "manifesto rolando de lado", "faixa de palavras cinética") são apropriados no MÁXIMO UMA vez por página. Dois ou mais marquees na mesma página parecem enchimento preguiçoso. Escolha a única seção em que o marquee realmente serve ao conteúdo; as demais recebem outro layout.
* **Padrão Pilha Fixa com GSAP (quando for usada uma pilha ao rolar).** Uma "pilha de cards ao rolar" precisa ser uma pilha fixa REAL, não uma lista de revelação sequencial. Veja a Seção 5.A abaixo para o esqueleto de código canônico. Falha comum: o gatilho dispara no meio da rolagem em vez de fixar no topo da viewport. Correção: `start: "top top"`, não `start: "top center"` ou `"top 80%"`.
* **Padrão Panorâmica Horizontal com GSAP (quando for usado sequestro de rolagem horizontal).** Veja a Seção 5.B abaixo para o esqueleto canônico. Falha comum: a animação começa antes da seção estar fixada, então o usuário vê meio slide. Mesma correção: `start: "top top"`, fixe o wrapper, faça scrub da trilha interna.

### 5.A Pilha Fixa - Esqueleto Canônico

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

Pontos críticos: `start: "top top"`, `pin: true`, cada card exceto o último é fixado, a transformação de escala/opacidade é dirigida pelo gatilho de scroll do PRÓXIMO card (assim o card anterior encolhe conforme o próximo chega).

### 5.B Panorâmica Horizontal - Esqueleto Canônico

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // pin starts when section top hits viewport top
          end: () => `+=${distance}`,                    // scroll distance = track width minus viewport
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

Pontos críticos: `start: "top top"`, `pin: true`, `end: "+=${distance}"` (comprimento da rolagem = percurso horizontal necessário), `scrub: 1`. O wrapper é fixado, a trilha interna desliza horizontalmente conforme o usuário rola verticalmente.

### 5.C Escalonamento de Revelação ao Rolar - Esqueleto Canônico (alternativa mais leve)

Para o simples "itens aparecem conforme entram na viewport" (sem fixação), prefira `whileInView` do Motion ao GSAP - mais leve, sem necessidade de ScrollTrigger:

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

Use isto para: listas de recursos, grades de depoimentos, muros de logos, qualquer coisa que só precise de "entrar ao rolar". Reserve o GSAP para trabalho real de fixação/scrub.

### 5.D Padrões de Animação Proibidos

* **`window.addEventListener("scroll", ...)`** é proibido. Roda a cada frame de scroll, propenso a travamentos, sem agrupamento. Use `useScroll()` do Motion, `ScrollTrigger` do GSAP, IntersectionObserver ou `scroll-driven animations` CSS (`animation-timeline: view()`).
* **Cálculos personalizados de progresso de scroll usando `window.scrollY`** em estado do React. Mesmo motivo. Re-renderiza a cada frame.
* **Loops `requestAnimationFrame` que tocam o estado do React.** Use valores de movimento (`useMotionValue` + `useTransform`).
* **Transições de Layout:** Use as props `layout` e `layoutId` do Motion para mudanças de estado visíveis (reordenar listas, expandir modais, elementos compartilhados entre rotas). Não envolva conteúdo estático em props `layout` "por segurança" - isso custa trabalho de medição.
* **Orquestração Escalonada:** Use `staggerChildren` (Motion) ou a cascata CSS (`animation-delay: calc(var(--index) * 100ms)`) para momentos de revelação em que a sequência importa. Para `staggerChildren`, o pai (`variants`) e os filhos DEVEM compartilhar a mesma árvore de Client Component.

---

## 6. GUARDRAILS DE PERFORMANCE E ACESSIBILIDADE

### 6.A Aceleração por Hardware
* Anime APENAS `transform` e `opacity`. Nunca anime `top`, `left`, `width`, `height`.
* Use `will-change: transform` com moderação - apenas em elementos que de fato vão animar.

### 6.B Movimento Reduzido (obrigatório)
* **Qualquer movimento acima de `MOTION_INTENSITY > 3` DEVE respeitar `prefers-reduced-motion`.** Isto não é negociável.
* No Motion: envolva com `useReducedMotion()` e degrade para estático.
* Em CSS: condicione as animações a `@media (prefers-reduced-motion: no-preference)` ou forneça um bloco de sobrescrita sob `@media (prefers-reduced-motion: reduce)` que as desative.
* Loops infinitos, parallax, sequestro de scroll e física magnética DEVEM colapsar para estático / instantâneo com movimento reduzido.

### 6.C Modo Escuro (obrigatório para qualquer página voltada ao consumidor)
* Projete para **os dois modos desde o início**. Nunca entregue somente claro ou somente escuro sem instrução explícita do usuário.
* Use a variante `dark:` do Tailwind OU variáveis CSS para tokens. Escolha uma estratégia por projeto.
* **Não prescreva cores específicas de modo escuro aqui.** O briefing decide. Mantenha a hierarquia visual, a identidade da marca e o contraste WCAG AA (AAA para corpo) nos dois modos.
* Respeite `prefers-color-scheme: dark`. Padrão para a preferência do sistema, a menos que a marca insista em um modo.

### 6.D Metas de Core Web Vitals
* **LCP** < 2,5s. A imagem do hero deve ser `next/image priority` ou pré-carregada.
* **INP** < 200ms. Trabalho pesado fora da thread principal.
* **CLS** < 0,1. Reserve espaço para imagens, fontes, embeds.
* Execute o Lighthouse antes de declarar uma página concluída.

### 6.E Custo do DOM
* Aplique filtros de grão / ruído EXCLUSIVAMENTE pseudo-elementos fixos e `pointer-events-none` (por exemplo, `fixed inset-0 z-[60] pointer-events-none`). NUNCA em contêineres com rolagem - repinturas contínuas da GPU destroem o FPS no mobile.
* Atenção ao tamanho do bundle. O Motion não é pequeno. O Three.js é grande. Carregue sob demanda tudo que não estiver acima da dobra.

### 6.F Contenção de Z-Index
NUNCA espalhe `z-50` ou `z-10` arbitrários. Use z-index estritamente para contextos de camada sistêmicos (navbars fixas, modais, sobreposições, grão). Documente a escala de z-index em um arquivo de constantes do projeto.

---

## 7. DEFINIÇÕES DOS CONTROLES (Referência Técnica)

### DESIGN_VARIANCE (Nível 1-10)
* **1-3 (Previsível):** Grade CSS simétrica (12 colunas, unidades fr iguais), paddings iguais, alinhamento centralizado.
* **4-7 (Deslocado):** Sobreposições `margin-top: -2rem`, proporções de imagem variadas (4:3 ao lado de 16:9), cabeçalhos alinhados à esquerda sobre dados centralizados.
* **8-10 (Assimétrico):** Layouts masonry, grade CSS com unidades fracionárias (`grid-template-columns: 2fr 1fr 1fr`), zonas vazias massivas (`padding-left: 20vw`).
* **SOBREPOSIÇÃO PARA MOBILE:** Para níveis 4-10, layouts assimétricos acima de `md:` DEVEM colapsar para uma coluna estrita (`w-full`, `px-4`, `py-8`) em viewports `< 768px`.

### MOTION_INTENSITY (Nível 1-10)
* **1-3 (Estático):** Sem animações automáticas. Apenas estados CSS `:hover` e `:active`. `prefers-reduced-motion` é o modo padrão de qualquer forma.
* **4-7 (CSS Fluido):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. Cascatas `animation-delay` para entradas de carregamento. Foco em `transform` e `opacity`.
* **8-10 (Coreografia Avançada):** Revelações complexas disparadas por scroll, parallax, animação dirigida por scroll (`animation-timeline` CSS ou ScrollTrigger do GSAP). Use hooks do Motion. **NUNCA use `window.addEventListener('scroll')`** - é uma proibição rígida, não um "prefira não". Veja a Seção 5.D para as alternativas permitidas.

### VISUAL_DENSITY (Nível 1-10)
* **1-3 (Galeria de Arte):** Muito espaço em branco. Grandes intervalos entre seções (`py-32` a `py-48`). Caro, limpo.
* **4-7 (App Diário):** Espaçamento padrão de aplicação web (`py-16` a `py-24`).
* **8-10 (Cockpit):** Paddings apertados. Sem caixas de card; linhas de 1px separam os dados. Obrigatório: `font-mono` para todos os números.

---

## 8. PROTOCOLO DE MODO ESCURO

Modo duplo por padrão. Nunca presuma somente claro, a menos que o briefing seja um editorial que emula impressão.

### 8.A Estratégia de Tokens (escolha uma e mantenha)
* **Variante `dark:` do Tailwind** (padrão para projetos utility-first): cada utilitário de cor emparelhado com sua variante escura (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
* **Variáveis CSS** (para shadcn/ui, Radix Themes ou bibliotecas de componentes com tema): defina tokens semânticos (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) e troque os valores sob `[data-theme="dark"]` ou `@media (prefers-color-scheme: dark)`.

### 8.B Não Prescreva Cores Específicas Aqui
O briefing e a marca decidem. Esta habilidade impõe apenas:
* **Contraste** - mínimo WCAG AA para texto corrido, meta AAA para texto de hero.
* **Paridade de hierarquia** - a hierarquia visual que funciona no claro deve funcionar no escuro. Se um CTA se destaca no claro, se destaca no escuro.
* **Fidelidade à marca** - a cor primária da marca continua reconhecível. Não dessature a marca num modo escuro.
* **Sem `#000000` puro e sem `#ffffff` puro** - use off-black (zinc-950, cinza quente quase preto) e off-white. Valores puros matam a profundidade.

### 8.C Modo Padrão
Respeite `prefers-color-scheme`, a menos que a marca insista. Adicione um alternador manual se algum dos modos perder expressão essencial da marca.

### 8.D Teste nos Dois Modos Antes de Finalizar
Abra a página nos dois modos durante o desenvolvimento. Não entregue uma página que você só viu em um modo.

---

## 9. SINAIS DE IA (Padrões Proibidos)

Evite estas assinaturas, a menos que o briefing peça explicitamente.

### 9.A Visual e CSS
* **NADA de neon / brilhos externos** por padrão. Use bordas internas ou sombras tingidas sutis.
* **NADA de preto puro (`#000000`).** Off-black, zinc-950 ou grafite.
* **NADA de destaques superssaturados.** Dessature para se misturar aos neutros.
* **NADA de texto com gradiente excessivo** em cabeçalhos grandes.
* **NADA de cursores de mouse personalizados.** Desatualizados, hostis à acessibilidade, hostis à performance.

### 9.B Tipografia
* **EVITE Inter como padrão.** Veja a Seção 4.1. Existe um caminho de exceção.
* **NADA de H1s superdimensionados** que só gritam. Controle a hierarquia com peso + cor, não com escala bruta.
* **Restrições de serifa:** Serifa para editorial / luxo / publicação. Não para dashboards.

### 9.C Layout e Espaçamento
* **Padding e margens matematicamente perfeitos.** Nada de elementos flutuando com espaços estranhos.
* **NADA de 3 cards de recurso iguais em 3 colunas.** A linha genérica de "três cards idênticos lado a lado" é proibida. Use zigue-zague em 2 colunas, grade assimétrica, fixação ao scroll ou alternativa de scroll horizontal.

### 9.D Conteúdo e Dados (Efeito "João da Silva")
* **NADA de nomes genéricos.** "João Silva", "Maria Souza", "Carlos Lima" → use nomes criativos, realistas e adequados à localidade.
* **NADA de avatares genéricos.** Nada de "ovo" em SVG nem ícones de usuário do Lucide → use placeholders fotográficos críveis ou estilo específico.
* **NADA de números perfeitos e falsos.** Evite `99.99%`, `50%`, `1234567`. Use dados orgânicos e confusos (`47.2%`, `+1 (312) 847-1928`).
* **NADA de nomes de marca de startup genéricos.** "Acme", "Nexus", "SmartFlow", "Cloudly" → invente nomes contextuais e premium que soem reais.
* **NADA de verbos de enchimento.** "Elevar", "Sem atrito", "Libere", "Próxima geração", "Revolucione" → use apenas verbos concretos.

### 9.E Recursos e Componentes Externos
* **NADA de ícones SVG feitos à mão.** Use Phosphor / HugeIcons / Radix / Tabler. Lucide apenas por pedido explícito.
* **SVGs decorativos feitos à mão fortemente desencorajados** como padrão (veja a Seção 4.8).
* **NADA de capturas de tela falsas feitas de divs.** Nunca construa uma UI de produto falsa com retângulos `<div>` para simular uma captura de tela. Use imagens reais, imagens geradas, ou pule a prévia.
* **NADA de links quebrados do Unsplash.** Use `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`, ou placeholders fotográficos gerados, ou ativos reais.
* **Customização do shadcn/ui:** Permitida, mas NUNCA no estado padrão. Customize raios, cores, sombras e tipografia para a estética do projeto.
* **Limpeza pronta para produção:** código visualmente limpo, memorável, meticulosamente refinado.

### 9.F Sinais dos Testes de Produção (proibidos sem exceção)

Estes padrões surgiram de testes reais de landing pages geradas por LLM. São as assinaturas para as quais o modelo recorre quando tenta "parecer desenhado". Trate-os como proibições rígidas, a menos que o briefing peça explicitamente um deles.

**Hero e topo da página**
* **NADA de rótulos de versão no hero.** `V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA` - proibidos como eyebrows padrão. Aceitáveis apenas quando o briefing for explicitamente sobre lançamento de produto / status de prévia.
* **NADA de sub-eyebrows no estilo "Marca · Nº 01".** Linhas de micro-metadados como "Marrow · Nº 01 · A panela de 6 litros". Pule-as.

**Numeração de seções e micro-rótulos**
* **NADA de eyebrows com número de seção.** `00 / INDEX`, `001 · Capabilities`, `002 · Featured commission`, `06 · how it works`, `05 · The honest table` - proibidos. Eyebrows devem nomear o tema em linguagem simples, não enumerar.
* **NADA de paginação estilo `01 / 4` em imagens ou tiles bento.** Se o usuário consegue contar, não precisa do rótulo.
* **NADA de dicas de rolagem estilo `Scroll · 001 Capabilities`.** Uma seta simples ou "Role" basta; sem prefixo de número de seção.
* **NADA de rótulos de intervalo do tipo "Índice de trabalhos, 2018 - 2026"** como eyebrows. Diga apenas o que é a seção.

**Separadores e pontos**
* **O ponto médio (`·`) é racionado.** Máximo 1 por linha em faixas de metadados. NÃO o use como separador padrão para tudo ("foo · bar · baz · qux · quux"). Se precisar de uma família de separadores, prefira quebras de linha, linhas finas ou colunas.
* **NADA de bolinhas de status coloridas decorativas em toda lista/nav/badge.** Uma bolinha colorida antes de "UMA VAGA NO Q4 ABERTA" ou antes de cada link de navegação, ou de cada linha de tarefa - proibido por padrão. Aceitável apenas quando a bolinha transmitir estado semântico real (um status de servidor, uma flag de disponibilidade) e for usada com parcimônia.

**Travessões e floreios tipográficos**
* **NADA de travessão (`—`) como elemento de design NEM em nenhum outro lugar.** Veja a Seção 9.G abaixo para a proibição completa e inegociável. O caractere travessão é proibido em títulos, eyebrows, pílulas, texto corrido, citações, atribuições, legendas, texto de botões e textos alternativos. Use o hífen comum (`-`).
* **NADA de títulos com quebra e itálico em `<br>`** como "movimento de design" padrão. Cortes do tipo "por trinta\<br\>*anos.*". Títulos devem ler naturalmente primeiro, e só ficar espertos quando o briefing exigir.
* **NADA de texto vertical rotacionado** ("ÍNDICE DE TRABALHOS, 2018 - 2026" girado 90°). Clichê de portfólio de agência. Use apenas quando o briefing for explicitamente de agência / Awwwards / experimental E servir a um propósito composicional real.
* **NADA de linhas de grade em cruz / linhas finas como decoração.** Linhas verticais e horizontais traçadas apenas para fazer a página "parecer desenhada" - proibidas. Use-as apenas quando organizarem conteúdo real.

**Prévias de produto falsas**
* **NADA de UI de produto falsa feita de divs no hero** (lista de tarefas falsa, terminal falso, dashboard falso construído com divs estilizadas). É o Sinal nº 1 de design por LLM. Use uma captura de tela real, uma imagem gerada, uma prévia real de componente, ou nenhuma.
* **NADA de rodapés de versão falsos** ("v0.6.2-rc.1", "última sincronização há 4s · main") dentro de capturas de tela falsas. Não acrescenta nada, grita IA.

**Sinais de texto de marketing**
* **NADA de cabeçalhos de prova social "Discretamente em uso em" / "Discretamente confiado por".** Use linguagem natural: "Confiado por", "Usado em", "Clientes incluem", ou pule o cabeçalho por completo se os logos falarem por si.
* **NADA de rótulos poéticos como "Do campo" / "Notas de campo" / "Atualmente na bancada" / "Nas nossas mesas" / "Pratos soltos"** em seções de citação, blog ou barra lateral. Soa como artesão performático. Use rótulos funcionais simples ("Depoimentos", "Textos recentes", "Trabalhando agora em") ou pule o rótulo.
* **NADA de referências humildes falsas a indústrias** no corpo de texto, do tipo "Respeitamos os franceses".  Fofo e com cara de IA.
* **NADA de faixas de clima / localidade** ("LIS 14:23 · 18°C") em cabeçalhos/rodapés, a menos que o briefing seja explicitamente sobre um lugar / um estúdio distribuído em fusos horários.
* **NADA de micro-metafrases sob eyebrows.** Frases como *"Cada um deles é um recurso que entregamos hoje, não uma promessa de roadmap. A lista continuará curta de propósito."* sob um título de seção são entulho. Eyebrow + Título + Corpo basta.
* **NADA de rótulos genéricos de etapa.** "Etapa 1 / Etapa 2 / Etapa 3", "Passo 1 / Passo 2 / Passo 3", "Fase 01 / Fase 02 / Fase 03", "Primeira passagem / Segunda passagem / Terceira passagem". Proibidos. O conteúdo real da etapa é o rótulo. Se precisar mostrar progressão, use o verbo-substantivo diretamente ("Instalar", "Configurar", "Entregar") e não "Etapa 1: Instalar".

**Pílulas, rótulos e carimbos de versão**
* **NADA de pílulas/rótulos/tags sobrepostos a imagens.** Nada de sobreposições `<span>` sobre fotos com tags como `Brand · 02`, `PLATE · BRAND`, `Field notes - journal`. Ou deixe a imagem falar sozinha, ou adicione uma legenda logo abaixo (fora da imagem).
* **NADA de créditos fotográficos como decoração.** Strings como `Field study no. 12 · Ines Caetano`, `Plate 03 · House archive`, `Frame XII · 35mm` sob imagens de estoque/picsum são pretensiosas. Crédito fotográfico é permitido SOMENTE quando há um fotógrafo real sendo creditado por uma foto real (com permissão). Caso contrário: pule a legenda ou use uma legenda funcional de uma linha ("A de 6 litros, em Sálvia.").
* **NADA de rodapés de versão em páginas de marketing.** Strings de rodapé como `v1.4.2`, `Build 0048`, `last sync 4s ago · main` são acessórios de CLI / ferramentas de desenvolvedor, não conteúdo de landing page. Proibidos em páginas de marketing / landing / portfólio.
* **NADA de contadores de estoque ao vivo do tipo "Reserva 412 de 800"** como decoração. Só se o briefing for explicitamente uma lista de espera de tiragem limitada com dados reais.

**Faixas decorativas de texto**
* **NADA de faixa decorativa de texto na base do hero.** Padrões como `BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION`, `DESIGN · BUILD · SHIP`, `ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.` como uma pequena faixa mono em maiúsculas atravessando a base do hero são clichê de portfólio de agência. Proibidos por padrão. Só aceitáveis quando a faixa carregar links navegáveis reais (navegação inferior fixa) ou informação real de status (banner de cookies, informação de build num site de documentação).
* **NADA de subtexto flutuante no canto superior direito de cabeçalhos de seção.** Padrão: a seção tem um título gigante alinhado à esquerda; no canto superior direito do mesmo cabeçalho há um pequeno parágrafo explicativo flutuando sem alinhamento claro com nada. Esse flutuante é o Sinal. Ou coloque o subtexto logo abaixo do título, ou construa um cabeçalho limpo em 2 colunas (esquerda: título, direita: corpo alinhado), mas não um parágrafo minúsculo no canto.

**Listas, divisórias e pontuação**
* **NADA de `border-t` + `border-b` em cada linha de uma lista longa / tabela de especificações.** Escolha um (borda inferior entre linhas OU borda superior acima do grupo) e use com parcimônia. Uma tabela de especificações com 10 linhas e linhas finas sob cada uma é o layout mais preguiçoso - veja a Seção 4.9 para componentes de UI alternativos.
* **NADA de barras de pontuação/progresso com trilhas de fundo preenchidas** como visuais de comparação. Se precisar mostrar comparações "X de Y", prefira um número + ícone pequeno, ou uma barra inline minúscula SEM trilha de fundo. Trilhas `bg-zinc-200` grandes e preenchidas com um preenchimento parcial por cima são poluição de UI de dashboard numa landing page.

**Localidade, horário e dicas de rolagem**
* **Faixas de localidade / nome de cidade / horário / clima são proibidas em 99% dos briefings.** "Lisboa, trabalhando com fundadores" no hero, "1200-690 Lisboa, Portugal" no rodapé, "Lisboa 14:23 · 18°C" na nav. São sinais de decoração de portfólio de agência. Permitidas APENAS quando: o briefing descrever explicitamente um estúdio distribuído globalmente com trabalho relevante por fuso horário, OU uma marca focada em viagens, OU um local físico real. Uma única menção de endereço de contato no rodapé é aceitável; uma faixa atmosférica de localidade não é.
* **Dicas de rolagem são proibidas.** `Scroll`, `↓ scroll`, `Scroll to explore`, `Scroll to walk through it`, ícones animados de roda do mouse. Se o usuário ainda não rolou, ele está olhando o hero. Ele sabe o que é rolagem. A base da viewport não precisa de rótulo.
* **ZERO bolinhas de status decorativas por padrão.** Uma bolinha colorida antes de itens de navegação, antes de linhas de lista, antes de badges, antes de rótulos de status é um Sinal. Aceitável apenas quando transmitir estado semântico real (um indicador ao vivo de status real de servidor, uma flag de disponibilidade ao vivo) e limitada a uma por seção da página.

### 9.G PROIBIÇÃO DO TRAVESSÃO (o Sinal mais violado de todos)

**O travessão (`—`) é COMPLETAMENTE proibido.** É a muleta estilística assinatura dos LLMs e o Sinal visual nº 1 em testes de produção. Não há permissão de "uso limitado", nem permissão de "frequência de linguagem natural", nem permissão de "no corpo do texto está ok". Nenhuma.

* **Proibido em títulos.** Use um ponto ou uma vírgula.
* **Proibido em eyebrows / rótulos / pílulas / texto de botões / legendas de imagem / itens de navegação.** Substitua por quebras de linha, colunas ou linhas finas.
* **Proibido no corpo do texto.** Reestruture a frase: duas frases com ponto, OU uma vírgula, OU parênteses, OU dois-pontos.
* **Proibido em atribuições de citação.** Use um hífen normal com espaços (` - `) ou uma quebra de linha + nome com peso menor.
* **Proibido também em forma de meia-risca (`–`) quando usada como separador.** Intervalos de datas (`2018-2026`) usam hífen. Intervalos numéricos (`€40-80k`) usam hífen.

Os ÚNICOS caracteres de traço permitidos na página são:
* Hífen comum `-` (para palavras compostas, intervalos, divisórias de linha na marcação)
* Sinal de menos em matemática (`-5°C`)

Se a sua saída contiver um único `—` ou `–` visível ao usuário, a saída falha na Verificação de Pré-Voo e deve ser reescrita.

Esta regra é inegociável. O agente historicamente ignorou os limites de travessão quando formulados como "use com moderação". A formulação aqui é binária: zero travessões.

---

## 10. VOCABULÁRIO DE REFERÊNCIA (Nomes de Padrões que o Agente Deve Conhecer)

Este é um vocabulário, não uma biblioteca. O agente deve CONHECER estes nomes de padrões para se comunicar sobre eles, projetar tendo-os em mente e recorrer a eles quando a leitura de design pedir. **Implementações e esboços de código vivem na Biblioteca de Blocos (Seção 12), que é preenchida iterativamente.**

### Paradigmas de Hero
* **Hero Dividido Assimétrico** - Texto de um lado, ativo do outro, espaço em branco generoso.
* **Hero Manifesto Editorial** - Tipografia grande, sem ativo, quase um pôster.
* **Hero com Máscara de Vídeo / Mídia** - Tipografia recortada como máscara sobre fundo de vídeo.
* **Hero de Tipografia Cinética** - Tipografia animada como o visual principal.
* **Hero de Revelação de Cortina** - Partes do hero se abrem ao rolar como uma cortina.
* **Hero Fixado ao Scroll** - O hero fica fixado enquanto o conteúdo rola por trás.

### Navegação e Menus
* **Ampliação do Dock do Mac OS** - Navegação na borda, ícones escalam fluidamente no hover.
* **Botão Magnético** - Puxa em direção ao cursor.
* **Menu Gooey** - Subitens se desprendem como líquido viscoso.
* **Dynamic Island** - Pílula que se transforma para status / alertas.
* **Menu Radial Contextual** - Menu circular que se expande no ponto do clique.
* **Speed Dial Flutuante** - FAB que se abre em ações secundárias curvas.
* **Revelação de Mega Menu** - Dropdown em tela cheia, conteúdo com fade escalonado.

### Layout e Grades
* **Grade Bento** - Agrupamento assimétrico de tiles (Central de Controle da Apple).
* **Layout Masonry** - Grade escalonada, sem altura de linha fixa.
* **Chroma Grid** - Bordas / tiles com gradientes sutis animados.
* **Rolagem de Tela Dividida** - Duas metades deslizando em direções opostas.
* **Seções de Pilha Fixa** - Seções que fixam e empilham ao rolar.

### Cards e Contêineres
* **Card com Inclinação Parallax** - Inclinação 3D acompanhando as coordenadas do mouse.
* **Card com Borda de Holofote** - Bordas se iluminam sob o cursor.
* **Painel de Glassmorphism** - Vidro fosco com refração interna.
* **Card com Folha Holográfica** - Mudança de arco-íris iridescente no hover.
* **Pilha de Swipe tipo Tinder** - Pilha física de cards, deslizar para descartar.
* **Modal Morfose** - O botão se expande no próprio diálogo.

### Animações de Scroll
* **Pilha de Scroll Fixa** - Cards grudam e empilham fisicamente.
* **Sequestro de Scroll Horizontal** - Rolagem vertical → panorâmica horizontal.
* **Rolagem Locomotiva / de Sequência** - Vídeo / sequência 3D atrelada à barra de rolagem.
* **Parallax de Zoom** - Imagem central de fundo que dá zoom ao rolar.
* **Caminho de Progresso do Scroll** - Linha SVG desenhada ao longo da rolagem.
* **Transição de Swipe Líquido** - Transição de página como líquido viscoso.

### Galerias e Mídia
* **Galeria em Cúpula** - Galeria panorâmica 3D.
* **Carrossel Coverflow** - Carrossel 3D com bordas inclinadas.
* **Grade de Arrastar para Navegar** - Tela arrastável sem limites.
* **Slider de Imagens em Acordeão** - Tiras estreitas que se expandem no hover.
* **Trilha de Imagens no Hover** - Imagens que surgem em rastro conforme o mouse passa.
* **Imagem com Efeito Glitch** - Deslocamento de canal RGB no hover.

### Tipografia e Texto
* **Marquee Cinético** - Faixas de texto sem fim que invertem com o scroll.
* **Revelação por Máscara de Texto** - Tipografia massiva como janela transparente para vídeo.
* **Efeito de Embaralhamento de Texto** - Decodificação estilo Matrix no carregamento / hover.
* **Texto em Caminho Circular** - Texto curvando ao longo de um círculo giratório.
* **Animação de Traço em Gradiente** - Texto contornado com gradiente em movimento.
* **Grade de Tipografia Cinética** - Letras que se afastam do cursor.

### Micro-interações e Efeitos
* **Botão de Explosão de Partículas** - CTA se estilhaça em partículas no sucesso.
* **Pull-to-Refresh Líquido** - Indicador de recarga como gotas se desprendendo.
* **Brilho Esqueleto (Skeleton Shimmer)** - Reflexo de luz deslizando sobre placeholders.
* **Botão de Hover Direcional** - O preenchimento entra pelo exato lado do cursor.
* **Efeito Ripple no Clique** - Onda a partir das coordenadas do clique.
* **Desenho Animado de Linha SVG** - Vetores se desenhando em tempo real.
* **Fundo de Gradiente de Malha** - Manchas orgânicas estilo lava-lamp.
* **Profundidade por Desfoque de Lente** - Interface de fundo desfocada para focar a ação em primeiro plano.

### Escolha de Biblioteca de Animação
* **Motion (`motion/react`)** - padrão para movimento de UI / Bento / mudanças de estado.
* **GSAP + ScrollTrigger** - para scrolltelling de página inteira e sequestros de scroll. Isole em componentes folha dedicados com limpeza em `useEffect`.
* **Three.js / WebGL** - para fundos de canvas e cenas 3D. Mesma regra de isolamento.
* **NUNCA misture GSAP / Three.js com Motion na mesma árvore de componentes.** Eles brigam pelos mesmos frames.

---

## 11. PROTOCOLO DE REDESENHO

Esta habilidade cobre **construções do zero E redesenhos**. Classificar mal o modo é a maior fonte de saídas ruins em redesenhos.

### 11.A Detecte o Modo (primeira ação)
* **Do zero** - nenhum site existente, ou reformulação total aprovada. Linha de base dos controles da Seção 1.
* **Redesenho - Preservar** - modernize sem quebrar a marca. Audite primeiro, extraia os tokens da marca, evolua gradualmente.
* **Redesenho - Reformular** - nova linguagem visual sobre conteúdo existente. Trate como do zero para o visual; preserve conteúdo e IA (arquitetura de informação).

Se for ambíguo, pergunte **uma vez**: *"Este redesenho deve preservar a marca existente, ou estamos começando visualmente do zero?"*

### 11.B Audite Antes de Tocar
Documente o estado atual antes de propor mudanças:
* **Tokens da marca** - cores primária / de destaque, pilha tipográfica, tratamento do logo, raios.
* **Arquitetura de informação** - árvore de páginas, navegação primária, caminhos de conversão principais.
* **Blocos de conteúdo** - o que existe, o que está fazendo trabalho, o que é enchimento.
* **Padrões a preservar** - interações assinatura, hero reconhecível, voz do texto.
* **Padrões a aposentar** - sinais de slop de IA, layouts quebrados, links mortos, imagens de estoque genéricas, armadilhas de performance.
* **Leitura dos controles do site existente** - infira o `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY` atuais. Esse é o seu ponto de partida, não a linha de base.
* **Linha de base de SEO** - páginas que rankeiam hoje, títulos meta, dados estruturados, cards OG. **A migração de SEO é o risco nº 1 de um redesenho.**

### 11.C Regras de Preservação
* **Não mude a arquitetura de informação** sem pedido. Mantenha slugs de página, IDs de âncora e rótulos da navegação primária estáveis por causa do SEO e da memória muscular.
* **Extraia as cores da marca antes de aplicar a Seção 4.2.** Uma marca que já é roxa continua roxa - aplique a exceção da REGRA DO LILÁS.
* **Preserve a voz do texto** a menos que peçam uma reescrita. Modernização visual ≠ reescrita de conteúdo.
* **Respeite as conquistas de acessibilidade existentes.** Não regrida estados de foco, texto alternativo, navegação por teclado, contraste.
* **Respeite os eventos de análise existentes.** Não renomeie botões, campos de formulário, IDs de seção de que o rastreamento posterior depende.

### 11.D Alavancas de Modernização (ordem de prioridade)
Aplique em ordem - pare quando o briefing estiver satisfeito:
1. **Atualização tipográfica** - maior ganho visual por unidade de risco.
2. **Espaçamento e ritmo** - aumente o padding das seções, corrija o ritmo vertical.
3. **Recalibração de cor** - dessature, unifique os neutros, mantenha o destaque da marca.
4. **Camada de movimento** - adicione micro-interações adequadas aos componentes existentes via `MOTION_INTENSITY`.
5. **Recomposição de hero e seções-chave** - reestruture o topo do funil usando o vocabulário da Seção 10.
6. **Substituição completa de blocos** - somente quando o bloco existente for irrecuperável.

### 11.E Árvore de Decisão: Evolução Direcionada vs. Redesenho Completo
* IA, conteúdo e SEO em ordem → **evolução direcionada** (Alavancas 1-4). ~70% do valor com ~40% do risco.
* A dívida visual é estrutural (IA quebrada, sem sistema de design, mobile quebrado) → **redesenho completo** com preservação estrita do conteúdo.
* A própria marca está mudando → **do zero**.

### 11.F O Que Nunca Muda Silenciosamente
Nunca modifique sem aprovação explícita do usuário:
* Estrutura de URL / slugs de rota.
* Rótulos da navegação primária.
* Nomes ou ordem dos campos de formulário (quebra análise + autofill).
* Logo ou wordmark da marca.
* Textos legais / de consentimento / de cookies existentes.

---

## 12. A BIBLIOTECA DE BLOCOS (Contrato - Implementações Entram Aqui Iterativamente)

O Vocabulário de Referência (Seção 10) nomeia padrões. A Biblioteca de Blocos os implementa com props reais, especificações reais de movimento e esboços de código reais.

**Status:** esquema definido aqui. Blocos serão adicionados iterativamente. Não crie blocos de forma improvisada sem seguir este esquema.

### 12.A Localização dos Arquivos
```
skills/taste-skill/blocks/
  hero/
    asymmetric-split.md
    editorial-manifesto.md
    kinetic-type.md
    ...
  feature/
    bento-grid.md
    sticky-scroll-stack.md
    zig-zag.md
    ...
  social-proof/
  pricing/
  cta/
  footer/
  navigation/
  portfolio/
  transition/
```

### 12.B Frontmatter Obrigatório
```yaml
---
name: asymmetric-split-hero
category: hero
dial_compatibility:
  variance: [6, 10]
  motion: [3, 10]
  density: [2, 5]
when_to_use: "Landing pages with one strong asset and one strong message. Default hero for SaaS, agency, premium consumer."
not_for: "Editorial / manifesto launches where the message IS the design."
stack: ["react", "next", "tailwind", "motion"]
---
```

### 12.C Seções Obrigatórias do Corpo
1. **Esboço visual** - descrição ou ASCII curto do layout.
2. **API de Props** - a interface do componente.
3. **Esboço de código** - implementação mínima funcional (Server Component por padrão, ilha Client para movimento).
4. **Fallback mobile** - regras explícitas de colapso para `< 768px`.
5. **Variantes de movimento** - uma variante por faixa de `MOTION_INTENSITY` (1-3, 4-7, 8-10). Fallback de movimento reduzido explícito.
6. **Notas de modo escuro** - estratégia de tokens específica deste bloco.
7. **Antipadrões** - maneiras comuns de este bloco dar errado.
8. **Referências** - links para exemplos reais em produção.

### 12.D Disciplina da Biblioteca de Blocos
* Um bloco por arquivo. Nada de arquivos com múltiplos blocos.
* Cada bloco deve funcionar isoladamente (solte-o em uma página, ele renderiza).
* Cada bloco deve passar na Verificação de Pré-Voo (Seção 14).
* Blocos que dependem de um sistema de design da Seção 2.A ficam sob `blocks/<category>/<name>--<system>.md` (por exemplo, `feature/bento-grid--material.md`).

---

## 13. FORA DO ESCOPO

Esta habilidade NÃO é para:
* Dashboards / UI de produto densa / painéis administrativos (use Fluent, Carbon, Atlassian ou Polaris da Seção 2.A).
* Tabelas de dados (use TanStack Table ou AG Grid).
* Formulários de várias etapas / assistentes (use padrões específicos de formulário; esta habilidade não vai melhorá-los).
* Editores de código (use Monaco / CodeMirror com sua personalização oficial).
* Mobile nativo (use Apple HIG / Material diretamente).
* UIs de colaboração em tempo real (presença, cursores, OT - classe de problema diferente).

Se o briefing for um dos itens acima, **diga isso explicitamente**, aponte a ferramenta certa e aplique as partes de página de marketing / página sobre / landing page desta habilidade apenas nas superfícies em que se aplicam.

---

## 14. VERIFICAÇÃO FINAL DE PRÉ-VOO

Execute esta matriz antes de entregar o código. Este é o último filtro.

**ISTO NÃO É OPCIONAL. Marque todas as caixas. Se alguma caixa falhar, a saída não está pronta.**

- [ ] **Inferência do briefing** declarada (linha da Seção 0.B)?
- [ ] **Valores dos controles** explícitos e justificados pelo briefing, não usando silenciosamente a linha de base?
- [ ] **Sistema de design** escolhido da Seção 2, se aplicável, ou estética rotulada honestamente?
- [ ] **Modo de redesenho** detectado e auditoria realizada (se aplicável, Seção 11)?
- [ ] **ZERO travessões (`—`) em qualquer lugar da página.** Títulos, eyebrows, pílulas, texto corrido, citações, atribuições, legendas, botões, textos alternativos. Zero. (Seção 9.G - inegociável.)
- [ ] **Trava de Tema da Página**: UM tema (claro, escuro ou automático) para a página inteira. Nenhuma seção inverte para modo invertido no meio da página (Seção 4.11)?
- [ ] **Trava de Consistência de Cor**: um destaque de cor usado de forma idêntica em todas as seções (Seção 4.2)?
- [ ] **Trava de Consistência de Forma**: um sistema de raio de canto aplicado de forma consistente (Seção 4.4)?
- [ ] **Verificação de Contraste de Botão**: todo texto de CTA é legível sobre seu fundo (sem branco-sobre-branco, WCAG AA 4,5:1)?
- [ ] **Quebra de linha em CTA**: nenhum rótulo de CTA quebra em 2+ linhas no desktop?
- [ ] **Verificação de Contraste de Formulário**: campos, placeholders, anéis de foco, rótulos passam WCAG AA contra o fundo da seção?
- [ ] **Disciplina de serifa**: se uma serifa for usada, NÃO é Fraunces nem Instrument_Serif (ou é, com justificativa explícita de marca)? Diferente da serifa do seu projeto anterior?
- [ ] **Verificação de paleta de consumo premium**: se o briefing for de consumo premium (utensílios / bem-estar / artesanato / luxo), a paleta NÃO é a família padrão de IA bege+latão+vermelho-sangue+espresso? Família diferente do seu projeto anterior de consumo premium?
- [ ] **Folga para descendentes em itálico**: toda palavra em itálico com `y g j p q` tem `leading-[1.1]` no mínimo + reserva `pb-1`?
- [ ] **Hero cabe na viewport**: título ≤ 2 linhas, subtexto ≤ 20 palavras E ≤ 4 linhas, CTA visível sem rolar, escala da fonte planejada em torno da imagem?
- [ ] **Padding superior do hero**: máximo `pt-24` no desktop, o conteúdo do hero não flutua na metade da viewport?
- [ ] **Disciplina de pilha do hero**: máximo 4 elementos de texto no hero (eyebrow OU faixa de marca, título, subtexto, CTAs)? Sem tagline minúscula abaixo dos CTAs, sem micro-faixa de confiança no hero?
- [ ] **CONTAGEM DE EYEBROWS (mecânica)**: conte instâncias de micro-rótulos `uppercase tracking` acima de títulos de seção em todos os componentes. Contagem ≤ ceil(contagemDeSeções / 3)? O hero conta como 1.
- [ ] **Proibição de Cabeçalho Dividido**: nenhum padrão "título grande à esquerda + parágrafo explicativo pequeno à direita" como cabeçalho de seção (empilhamento vertical no lugar)?
- [ ] **Limite de Alternância em Ziguezague**: nenhuma sequência de 3+ seções consecutivas com o mesmo layout de divisão imagem+texto?
- [ ] **Sem intenção de CTA duplicada**: nenhum par de CTAs com a mesma intenção ("Entre em contato" + "Vamos conversar" na mesma página = Falha)?
- [ ] **Muro de logos = só logo**: nenhum rótulo de setor / categoria impresso abaixo dos logos?
- [ ] **Diversidade de fundo em Bento**: pelo menos 2-3 células bento com variação visual real (imagem, gradiente, padrão), não todos cards de texto branco-sobre-branco?
- [ ] **Muro "Usado por / Confiado por"** fica ABAIXO do hero, não dentro dele, usa logos SVG REAIS (Simple Icons / devicon) ou marcas SVG geradas, NÃO wordmarks tipográficos de texto simples?
- [ ] **Autoauditoria de texto**: toda string visível relida, nenhuma frase gramaticalmente quebrada ou alucinada por IA ("grátis em seu passado" tipo) entregue?
- [ ] **Movimento motivado**: toda animação pode ser justificada em uma frase (hierarquia / narrativa / feedback / transição de estado), nada de GSAP só para mostrar?
- [ ] **Marquee: no máximo um por página**: nenhum par de marquees horizontais na mesma página?
- [ ] **Navegação em UMA linha** no desktop, altura ≤ 80px?
- [ ] **Repetição de layout de seção**: nenhum par de seções compartilha a mesma família de layout (pelo menos 4 famílias diferentes em 8 seções)?
- [ ] **Bento com ritmo E contagem exata de células** (N itens → N células, sem células vazias no meio nem no fim)?
- [ ] **Listas longas usam o componente de UI certo** (não o padrão `<ul>` com `divide-y` para > 5 itens - veja alternativas na Seção 4.9)?
- [ ] **Imagens reais usadas** (ferramenta de geração primeiro, depois seed Picsum, depois slots de placeholder explícitos) - NENHUMA captura de tela falsa feita de divs, NENHUM SVG decorativo feito à mão, NENHUM minimalismo só de texto?
- [ ] **Sem pílulas/rótulos sobre imagens** (sem `Plate · Brand`, sem `Field notes - journal`)?
- [ ] **Sem créditos fotográficos como decoração** (`Field study no. 12 · Ines Caetano`)?
- [ ] **Sem rodapés de versão** (`v1.4.2`, `Build 0048`) em páginas de marketing?
- [ ] **Sem micro-metafrases** sob eyebrows ("Cada um deles é um recurso que entregamos hoje...")?
- [ ] **Sem faixa decorativa de texto na base do hero** (`BRAND. MOTION. SPATIAL.`)?
- [ ] **Sem subtexto flutuante no canto superior direito** em cabeçalhos de seção?
- [ ] **Sem barras de pontuação/progresso com trilhas de fundo preenchidas** como visuais de comparação?
- [ ] **Sem faixas de localidade / nome de cidade / horário / clima** a menos que o briefing seja genuinamente distribuído globalmente ou focado em um lugar?
- [ ] **Sem dicas de rolagem** (`Scroll`, `↓ scroll`, `Scroll to explore`)?
- [ ] **Sem rótulos de versão no hero** (V0.6, BETA, SOMENTE CONVITE) a menos que o briefing seja um lançamento?
- [ ] **Sem eyebrows com numeração de seção** (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`)?
- [ ] **Sem bolinhas decorativas** (zero por padrão, apenas para estado semântico real)?
- [ ] **Sem `border-t` + `border-b` em cada linha** de listas longas / tabelas de especificações?
- [ ] **Densidade de conteúdo** sã: sem tabelas de dados de 20 linhas, sem especificações falsamente precisas sem justificativa, subparágrafos ≤ 25 palavras por padrão?
- [ ] **Citações ≤ 3 linhas** de corpo, atribuição limpa (sem travessão)?
- [ ] **Movimento declarado = movimento mostrado**: se `MOTION_INTENSITY > 4`, a página realmente anima, não apenas declara?
- [ ] **Pilha fixa / panorâmica horizontal com GSAP** implementadas conforme o esqueleto canônico das Seções 5.A / 5.B (`start: "top top"`, `pin: true`, scrub correto)?
- [ ] **Sem `window.addEventListener('scroll')`** - usando apenas `useScroll()` do Motion / ScrollTrigger / IntersectionObserver / animações CSS dirigidas por scroll?
- [ ] **Movimento reduzido** envolvido em tudo que for `MOTION_INTENSITY > 3`?
- [ ] **Modo escuro** com tokens definidos e testados nos dois modos?
- [ ] **Colapso mobile** explícito (`w-full`, `px-4`, `max-w-7xl mx-auto`) para layouts de alta variância?
- [ ] **Estabilidade da viewport**: `min-h-[100dvh]`, nunca `h-screen`?
- [ ] **Animações `useEffect`** têm funções de limpeza estritas?
- [ ] **Estados vazio / carregamento / erro** fornecidos?
- [ ] **Cards omitidos** em favor de espaçamento sempre que possível?
- [ ] **Ícones** apenas de bibliotecas permitidas (Phosphor / HugeIcons / Radix / Tabler), sem caminhos SVG feitos à mão?
- [ ] **Movimento** isolado em componentes folha do cliente com `'use client'` no topo, memoizado?
- [ ] **Nenhum Sinal de IA** da Seção 9 (Inter como padrão, roxo de IA, três cards iguais, João Silva, Acme, "Discretamente em uso em")?
- [ ] **Core Web Vitals** plausivelmente atingidos (LCP < 2,5s, INP < 200ms, CLS < 0,1)?
- [ ] **Um sistema de design** por projeto (sem Material + shadcn misturados)?

Se uma única caixa não puder ser marcada com honestidade, a página não está pronta. Corrija antes de entregar.

---

# APÊNDICES - Material de Referência com Fontes Reais

As seções abaixo são conteúdo de referência incorporado. Elas fornecem comandos de instalação reais, links canônicos de documentação e trechos iniciais funcionais para cada sistema de design citado na Seção 2. Use-os para fundamentar decisões na realidade de produção, não em ficção dos dados de treinamento.

## Apêndice A - Comandos de Instalação por Sistema de Design

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components (framework-free)
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui (open code, owned components)
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS (GitHub product/devtool UI)
npm install --save @primer/css

# Primer Brand (GitHub marketing UI)
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components (Shopify apps only)
# Add this to your app HTML head:
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```

## Apêndice B - Fontes Canônicas (leia antes de reinventar)

### Material Web
- https://github.com/material-components/material-web
- https://material-web.dev/theming/material-theming/
- https://m3.material.io/develop/web

### Fluent UI
- https://fluent2.microsoft.design/get-started/develop
- https://fluent2.microsoft.design/components/web/react/
- https://github.com/microsoft/fluentui
- https://learn.microsoft.com/en-us/fluent-ui/web-components/

### Carbon
- https://carbondesignsystem.com/
- https://github.com/carbon-design-system/carbon
- https://carbondesignsystem.com/developing/react-tutorial/overview/
- https://carbondesignsystem.com/developing/web-components-tutorial/overview/

### Shopify Polaris
- https://shopify.dev/docs/api/app-home/web-components
- https://github.com/Shopify/polaris-react
- https://polaris-react.shopify.com/components

### Atlassian
- https://atlassian.design/get-started/develop
- https://atlassian.design/components/button/examples
- https://atlaskit.atlassian.com/packages/design-system/button/example/disabled
- https://atlassian.design/tokens/design-tokens

### Primer
- https://primer.style/
- https://github.com/primer/css
- https://github.com/primer/brand

### GOV.UK
- https://design-system.service.gov.uk/components/button/
- https://design-system.service.gov.uk/styles/layout/
- https://github.com/alphagov/govuk-frontend

### USWDS
- https://designsystem.digital.gov/documentation/developers/
- https://designsystem.digital.gov/components/button/
- https://designsystem.digital.gov/components/card/
- https://github.com/uswds/uswds

### Bootstrap
- https://getbootstrap.com/docs/5.3/layout/grid/
- https://getbootstrap.com/docs/5.3/components/card/

### Tailwind
- https://tailwindcss.com/docs/dark-mode
- https://tailwindcss.com/blog/tailwindcss-v4

### Radix
- https://www.radix-ui.com/themes/docs/components/theme
- https://www.radix-ui.com/themes/docs/components/card
- https://github.com/radix-ui/themes

### shadcn/ui
- https://ui.shadcn.com/docs
- https://ui.shadcn.com/docs/components/card
- https://github.com/shadcn-ui/ui

### CSS nativo / padrões W3C
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass (somente plataformas Apple)
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## Apêndice C - Apple Liquid Glass: Aproximação Web Honesta

**Não** trate trechos aleatórios de CSS como Apple Liquid Glass oficial.

### O que é oficial
A Apple documenta o Liquid Glass nas Human Interface Guidelines e na Developer Documentation para **plataformas Apple**. É um material dinâmico usado na UI das plataformas Apple. A implementação nativa da Apple pertence às APIs das plataformas Apple e aos componentes do sistema, **não a um pacote CSS público para web**.

Documentação oficial relevante:
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### O que NÃO é oficial
Não existe `liquid-glass.css` da Apple para sites comuns.

Uma aproximação web pode usar:
- `backdrop-filter`
- fundos transparentes
- bordas em camadas
- sobreposições de destaque
- gradientes
- movimento
- fallbacks de contraste forte

Mas isso é **aproximação web de glassmorphism / vidro fosco**, não Apple Liquid Glass oficial. Rotule-a como tal nos comentários.

### Esqueleto de aproximação web mais segura

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

**Importante:** `prefers-reduced-transparency` tem suporte irregular entre navegadores; teste. Sempre forneça contraste suficiente mesmo sem desfoque.

---

**Fim dos apêndices.** Os comandos de instalação acima são âncoras de realidade. O esqueleto de Apple Liquid Glass é uma aproximação rotulada, não um pacote emitido pela Apple. Para documentação canônica de cada sistema de design, consulte a documentação oficial do sistema (links na Seção 2 e no Apêndice B).
