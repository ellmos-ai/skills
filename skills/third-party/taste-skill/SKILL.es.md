---
name: design-taste-frontend
description: "Habilidad de frontend anti-slop para landing pages, portafolios y rediseños. El agente lee el brief, infiere la dirección de diseño adecuada y entrega interfaces que no parecen plantillas. Sistemas de diseño reales cuando corresponda, auditoría previa en rediseños y verificación estricta previa a la entrega."
third_party: true
license: MIT
upstream: https://github.com/Leonxlnx/taste-skill
category: dev
language: es
translated_from_sha256: 7616ab6689efd139d313f95808165c7e4752bd39d50ed6a0533a120b8ff81002
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T01:52:48.424824+00:00"
---
<img src="banner.png" width="100%" alt="taste-skill banner">

# tasteskill: Habilidad Anti-Slop para Frontend

> Landing pages, portafolios y rediseños. No dashboards, no tablas de datos, no interfaces de producto de varios pasos.
> Cada regla de abajo es **contextual**. Ninguna se activa automáticamente. Primero lee el brief y luego extrae solo lo que encaja.

---

## 0. INFERENCIA DEL BRIEF (Lee el contexto antes que nada)

Antes de tocar código o ajustar parámetros, **infiere lo que el usuario realmente quiere**. La mayoría de los diseños generados por LLM son malos porque el modelo salta a una estética por defecto en lugar de leer el contexto.

### 0.A Lee primero estas señales
1. **Tipo de página**: landing (SaaS / consumidor / agencia / evento), portafolio (desarrollador / diseñador / estudio creativo), rediseño (preservar vs. renovar total), editorial / blog.
2. **Palabras de estilo** que usó el usuario: "minimalista", "calmado", "estilo Linear", "Awwwards", "brutalista", "consumo premium", "al estilo Apple", "juguetón", "B2B serio", "editorial", "de agencia", "glassy", "tech oscuro".
3. **Señales de referencia**: URLs enlazadas, capturas pegadas, productos mencionados, marcas con las que compite.
4. **Audiencia**: panel de compras B2B vs. consumidor con sensibilidad de diseño vs. reclutador que revisa un portafolio. La audiencia define la estética, no tu gusto.
5. **Activos de marca existentes**: logotipo, color, tipografía, fotografía. En rediseños son material de partida, no una entrada opcional (ver Sección 11).
6. **Restricciones implícitas**: audiencias con prioridad en accesibilidad, sector público, industrias reguladas, comercio basado en confianza, productos infantiles. Estas restricciones ANULAN la preferencia estética.

### 0.B Escribe una "Lectura de diseño" de una línea antes de generar
Antes de cualquier código, indica en una línea: **"Lo interpreto como: \<page kind> para \<audience>, con un lenguaje \<vibe>, inclinándome hacia \<design system or aesthetic family>."**

Ejemplos de lectura:
- *"Lo interpreto como: landing de SaaS B2B para compradores técnicos, con un lenguaje minimalista estilo Linear, inclinándome hacia utilidades de Tailwind + Geist + movimiento contenido."*
- *"Lo interpreto como: portafolio de un diseñador independiente para responsables de contratación, con un lenguaje editorial / de tipografía cinética, inclinándome hacia CSS nativo + animación dirigida por scroll + tipografía personalizada."*
- *"Lo interpreto como: rediseño de un sitio de servicios públicos, con un lenguaje centrado en la confianza, inclinándome hacia GOV.UK Frontend o USWDS."*

### 0.C Si el brief es ambiguo, haz una pregunta, no adivines
Haz exactamente **una** pregunta de aclaración, nunca un volcado de varias, y solo cuando la lectura de diseño realmente diverja. Ejemplo: *"¿Debe sentirse más cercano a un Linear limpio o a algo experimental al estilo Awwwards?"*

Si puedes inferir con confianza a partir del contexto, **no preguntes**. Declara la lectura de diseño y continúa.

### 0.D Disciplina anti-valores por defecto
No caigas en: degradados morado de IA, hero centrado sobre malla oscura, tres tarjetas de características iguales, glassmorphism genérico en todo, microanimaciones en bucle infinito por todas partes, Inter + slate-900. Estos son los valores por defecto del LLM. Aléjate de ellos deliberadamente según la lectura de diseño.

---

## 1. LOS TRES CONTROLES (Configuración central)

Tras la lectura de diseño, define tres controles. Cada decisión de layout, movimiento y densidad de abajo depende de ellos.

* **`DESIGN_VARIANCE: 8`**: 1 = Simetría perfecta, 10 = Caos artístico
* **`MOTION_INTENSITY: 6`**: 1 = Estático, 10 = Cinematográfico / Físico
* **`VISUAL_DENSITY: 4`**: 1 = Galería de arte / Aireado, 10 = Cabina de control / Datos densos

**Línea base:** `8 / 6 / 4`. Usa estos valores salvo que la lectura de diseño los anule. No pidas al usuario que edite este archivo; las anulaciones se hacen de forma conversacional.

### 1.A Inferencia de controles (lectura de diseño → valores)
| Señal | VARIANZA | MOVIMIENTO | DENSIDAD |
|---|---|---|---|
| "minimalista / limpio / calmado / editorial / estilo Linear" | 5-6 | 3-4 | 2-3 |
| "consumo premium / estilo Apple / lujo / marca" | 7-8 | 5-7 | 3-4 |
| "juguetón / salvaje / Dribbble / Awwwards / experimental / agencia" | 9-10 | 8-10 | 3-4 |
| "landing page / portafolio / sitio de marketing (por defecto)" | 7-9 | 6-8 | 3-5 |
| "basado en confianza / sector público / regulado / crítico en accesibilidad" | 3-4 | 2-3 | 4-5 |
| "rediseño - preservar" | igual al existente | +1 | igual al existente |
| "rediseño - renovación total" | +2 | +2 | igual al existente |

### 1.B Preajustes por caso de uso
| Caso de uso | VARIANZA | MOVIMIENTO | DENSIDAD |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agencia / creativa) | 9 | 8 | 3 |
| Landing (Consumo premium) | 7 | 6 | 3 |
| Portafolio (Diseñador / estudio) | 8 | 7 | 3 |
| Portafolio (Desarrollador) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Servicio de sector público | 3 | 2 | 5 |
| Rediseño - preservar | igual | igual+1 | igual |
| Rediseño - renovación total | +2 | +2 | igual |

### 1.C Cómo los controles dirigen el resultado
Usa estos valores (o los indicados por el usuario) como variables globales. Las referencias cruzadas de este documento se refieren a estos nombres exactos de variable; nunca inventes alias como `LAYOUT_VARIANCE` o `ANIM_LEVEL`.

---

## 2. MAPA DE BRIEF → SISTEMA DE DISEÑO

Una vez tengas la lectura de diseño (Sección 0) y los controles (Sección 1), elige la base adecuada. No inventes CSS para cosas que tienen un paquete oficial. No finjas que una tendencia estética es un sistema oficial.

### 2.A Cuándo usar un sistema de diseño real (usa los paquetes oficiales)

| El brief sugiere… | Usa | Motivo |
|---|---|---|
| Microsoft / SaaS empresarial / paneles | `@fluentui/react-components` o `@fluentui/web-components` | Fluent UI oficial, tokens de Microsoft, accesibilidad resuelta |
| Estilo Google, producto con aspecto Material | `@material/web` + tokens de Material 3 | Oficial, personalizable mediante Material Theming |
| B2B estilo IBM / analítica empresarial | `@carbon/react` + `@carbon/styles` | Carbon oficial, patrones maduros de densidad de datos |
| Superficies de aplicaciones de Shopify | Componentes web de `polaris.js` / Polaris React | Obligatorio para la interfaz de administración de Shopify |
| Producto estilo Atlassian / Jira | `@atlaskit/*` + `@atlaskit/tokens` | Sistema de diseño oficial de Atlassian |
| Herramienta para desarrolladores estilo GitHub / página comunitaria | `@primer/css` o `@primer/react-brand` | Primer oficial; variante Brand para marketing |
| Servicio público del Reino Unido | `govuk-frontend` | Esperado legal y normativamente |
| Sector público de EE. UU. / prioridad a la confianza | `uswds` | Igual que lo anterior |
| MVP rápido para negocio local / agencia | Bootstrap 5.3 | Sencillo, rápido, funciona |
| Base React moderna y accesible | `@radix-ui/themes` | Primitivas y tema pulido |
| SaaS moderno en el que posees los componentes | shadcn/ui (`npx shadcn@latest add ...`) | Tú posees el código, fácil de personalizar; nunca lo entregues en estado predeterminado |
| SaaS moderno basado en Tailwind / marketing de IA | Utilidades de Tailwind v4 + variante `dark:` | Opción predeterminada para proyectos de desarrolladores independientes y equipos pequeños |

**Regla de honestidad:** si el brief corresponde a uno de los sistemas anteriores, instala y usa el paquete **oficial**. No recrees su CSS a mano. No importes los tokens de un sistema para luego sobrescribir el 90 % de ellos.

**Un sistema por proyecto.** No mezcles Fluent React con Carbon en el mismo árbol. No importes componentes de shadcn/ui en una aplicación de Material 3.

### 2.B Cuando el brief es una estética, no un sistema
Para estas direcciones **no existe un único paquete oficial**. Construye con CSS nativo + Tailwind + una biblioteca de componentes mantenida. Sé honesto en los comentarios del código sobre qué es inspiración tomada de otra fuente y qué es material oficial.

| Estética | Implementación honesta |
|---|---|
| Glassmorphism / "cristal esmerilado" | `backdrop-filter`, bordes en capas, superposiciones de resaltado. Proporciona un respaldo de relleno sólido para `prefers-reduced-transparency`. |
| Bento (cuadrículas de mosaicos al estilo Apple) | CSS Grid con celdas de tamaños mixtos. Ninguna biblioteca única es dueña de esto. |
| Brutalismo | CSS nativo, monoespaciado, bordes crudos. Sin biblioteca. |
| Editorial / revista | Tipografía serif, cuadrícula asimétrica, espacio en blanco generoso. Sin biblioteca. |
| Tecnológico oscuro / hacker | Monoespaciada + acento neón, motivos de terminal. Sin biblioteca. |
| Aurora / degradados de malla | SVG o degradados radiales en capas. Sin biblioteca. |
| Tipografía cinética | Animaciones CSS nativas, animaciones controladas por desplazamiento, GSAP para secuestros de scroll. Sin biblioteca. |
| **Apple Liquid Glass** | Apple documenta esto solo para las plataformas de Apple. **No existe un `liquid-glass.css` oficial.** Las implementaciones web son aproximaciones que usan `backdrop-filter` + bordes en capas + resaltados. Etiquétalo claramente como aproximación. |

---

## 3. ARQUITECTURA Y CONVENCIONES PREDETERMINADAS

A menos que la lectura del diseño elija un sistema de diseño real (Sección 2.A), estos son los valores predeterminados:

### 3.A Stack
* **Framework:** React o Next.js. Usa por defecto Server Components (RSC).
  * **SEGURIDAD RSC:** El estado global solo funciona en Client Components. En Next.js, envuelve los proveedores en un componente `"use client"`.
  * **AISLAMIENTO DE INTERACTIVIDAD:** Todo componente que use Motion, escuchadores de desplazamiento o física de punteros DEBE ser una hoja aislada con `'use client'` en la parte superior. Los Server Components solo renderizan diseños estáticos.
* **Estilos:** **Tailwind v4** (predeterminado). Tailwind v3 solo si el proyecto existente lo exige.
  * Para v4: NO uses el plugin `tailwindcss` en `postcss.config.js`. Usa `@tailwindcss/postcss` o el plugin de Vite.
* **Animación:** **Motion** (la biblioteca antes conocida como Framer Motion). Importa desde `motion/react` (`import { motion } from "motion/react"`). El paquete `framer-motion` sigue funcionando como alias heredado; prefiere `motion/react` en código nuevo.
* **Fuentes:** Usa siempre `next/font` (Next.js) o aloja tú mismo con `@font-face` + `font-display: swap`. Nunca enlaces Google Fonts mediante `<link>` en producción.

### 3.B Estado
* `useState` / `useReducer` locales para la interfaz aislada.
* Estado global SOLO para evitar el prop drilling profundo: Zustand, Jotai o contexto de React.
* **NUNCA** uses `useState` para seguir valores continuos impulsados por la entrada del usuario (posición del ratón, progreso del desplazamiento, física de punteros, hover magnético). Usa `useMotionValue` / `useTransform` / `useScroll` de Motion. `useState` vuelve a renderizar el árbol de React en cada cambio y se colapsa en móviles.

### 3.C Iconos
* **Bibliotecas permitidas (orden de prioridad):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Desaconsejada:** `lucide-react`. Aceptable solo cuando el usuario lo pida explícitamente o el proyecto ya dependa de ella.
* **NUNCA crees a mano iconos SVG.** Si falta un glifo, instala una segunda biblioteca o compón a partir de primitivas; no dibujes trazados de iconos desde cero.
* **Una familia por proyecto.** No mezcles Phosphor con Lucide en el mismo árbol de componentes.
* **Estandariza `strokeWidth` globalmente** (p. ej., `1.5` o `2.0`).

### 3.D Política de emojis
Desaconsejados por defecto en el código, el marcado y el texto visible. Sustituye los símbolos por glifos de bibliotecas de iconos. **Excepción:** permite emojis solo cuando el usuario pida explícitamente un tono lúdico, de chat o nativo de redes sociales, y aun así úsalos con moderación y con intención.

### 3.E Mecánica de responsividad y maquetación

* Estandarizar los breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Contener las maquetaciones de página usando `max-w-[1400px] mx-auto` o `max-w-7xl`.
* **Estabilidad del viewport:** NUNCA usar `h-screen` para secciones Hero de altura completa. SIEMPRE usar `min-h-[100dvh]` para evitar saltos de maquetación en móviles (barra de direcciones de iOS Safari).
* **Grid antes que cálculos con Flex:** NUNCA usar cálculos complejos de porcentajes en flexbox (`w-[calc(33%-1rem)]`). SIEMPRE usar CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).

### 3.F Verificación de dependencias (obligatoria)

Antes de importar CUALQUIER biblioteca de terceros, comprobar `package.json`. Si el paquete no está presente, mostrar primero el comando de instalación. **Nunca** asumir que una biblioteca existe.

---

## 4. DIRECTIVAS DE INGENIERÍA DE DISEÑO (corrección de sesgos)

Los LLM tienden por defecto a clichés. Sobrescribir proactivamente estos valores predeterminados. Cada regla tiene una vía de anulación según el contexto.

### 4.1 Tipografía

* **Display / Titulares:** Por defecto `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Cuerpo / Párrafos:** Por defecto `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Elección de fuente sans:**
  * **Desaconsejada como predeterminada:** `Inter`. Elegir primero `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi` o una serif adecuada a la marca.
  * **Excepción:** Inter es aceptable cuando el usuario pide explícitamente un estilo neutro / estándar / tipo Linear, o cuando el encargo es un sitio del sector público o centrado en accesibilidad.
* **Combinaciones a conocer:** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.

* **DISCIPLINA DE SERIF (MUY DESACONSEJADA COMO PREDETERMINADA):**
  * La serif está **muy desaconsejada como fuente predeterminada en cualquier proyecto.** "Se siente creativa / premium / editorial" NO es razón para recurrir a una serif. El modelo mental por defecto del agente de que "encargo creativo = serif" es el indicador de IA más probado en rondas de producción.
  * **La serif solo es aceptable cuando se cumple UNA de estas condiciones de forma explícita:**
    - El brief de marca nombra literalmente una fuente serif, O
    - La familia estética es genuinamente editorial / de lujo / de publicación / manuscrita / de patrimonio / vintage Y puedes explicar por qué esta serif concreta encaja con esta marca concreta
  * Para todo lo demás (agencia creativa, estudio de diseño, marca moderna, consumo premium, portfolio, estilo de vida), **display sans-serif por defecto** (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). Las displays sans no son "aburridas": son el valor por defecto por la misma razón por la que el negro es el predeterminado en la moda.
  * **REGLA DE ÉNFASIS (relacionada):** Cuando quieras enfatizar una palabra dentro de un titular (el recurso cinético tipo "y `spatial` design"), usa **cursiva o negrita de la MISMA fuente**. NO insertes una palabra en serif aleatoria en un titular sans (ni al revés) solo para añadir interés visual. El énfasis mezclando familias es de aficionado. El énfasis en cursiva/negrita dentro de la misma familia es la opción correcta.
  * **Específicamente PROHIBIDAS como predeterminadas:** `Fraunces` y `Instrument_Serif` (las dos serifs de display favoritas de los LLM).
  * **Si una serif está justificada** (raro, según lo anterior), rota dentro de este conjunto y NO reutilices la misma serif en proyectos consecutivos: PP Editorial New, GT Sectra Display, Cardinal Grotesque, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.

* **HOLGURA PARA DESCENDENTES EN CURSIVA (obligatoria):** Cuando se use cursiva en tipografía display y la palabra contenga una letra con descendente (`y g j p q`), `leading-[1]` o `leading-none` recortarán el descendente. Usa `leading-[1.1]` como mínimo y añade una reserva de `pb-1` o `mb-1` en el elemento contenedor. Revisa cada palabra en cursiva de los titulares display antes de publicar.

### 4.2 Calibración de color
* Máximo 1 color de acento. Saturación < 80% por defecto.
* **LA REGLA LILA:** La estética "AI Purple / Blue glow" (resplandor morado/azul de IA) se desaconseja como valor por defecto. Nada de botones con resplandor morado automático ni degradados neón aleatorios. Usa bases neutras (Zinc / Slate / Stone) con acentos singulares de alto contraste (Emerald, Electric Blue, Deep Rose, Burnt Orange, etc.).
* **Excepción:** si la marca o el brief solicitan explícitamente morado / violeta / lila, adóptalo. Pero ejecútalo con intención: paleta consistente, neutros armonizados, degradados contenidos. Nada de "AI gradient slop" genérico.
* **Una paleta por proyecto.** No alternes entre grises cálidos y fríos dentro del mismo proyecto.
* **BLOQUEO DE CONSISTENCIA DE COLOR (obligatorio):** Una vez elegido un color de acento para una página, se usa en TODA la página. Un sitio con grises cálidos no pasa de repente a un CTA azul en la sección 7. Un sitio con acento rosa no lleva un distintivo de estado en verde azulado en el pie de página. Elige un acento, bloquéalo y audita cada componente antes de entregar.

* **PROHIBICIÓN DE PALETA PREMIUM-CONSUMO (obligatorio, segundo tic de IA más recurrente):**
  * Para briefs de consumo premium (batería de cocina, bienestar, artesanía, lujo, artesanía patrimonial, productos para el hogar DTC, etc.) el valor por defecto del LLM es **beige/crema cálido + latón/arcilla/burdeos/ocre + texto oscuro espresso/tinta**. Concretamente, las familias hexadecimales prohibidas como fondos y acentos por defecto:
    - Fondos: `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb` (todos "papel cálido / crema / tiza / hueso")
    - Acentos: `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621` (todos "latón / arcilla / burdeos / ocre")
    - Texto: `#1a1714`, `#1a1814`, `#1b1814` (todos "espresso / casi negro cálido")
  * Esta paleta está PROHIBIDA como opción por defecto para briefs de consumo premium. Todo sitio de consumo premium que hayas entregado antes usa exactamente esta paleta. La marca se vuelve invisible.
  * **Alternativas por defecto (rota, no repitas):**
    - **Lujo frío:** gris plateado + cromo + humo (piensa en Tesla, Apple Watch, Hermès sin el cuero)
    - **Bosque:** verde profundo + hueso + acento ámbar (piensa en Filson, Patagonia premium)
    - **Negro y tabaco:** negro verdadero desaturado + tabaco cálido, contraste nítido, sin beige
    - **Cobalto + crema:** azul saturado sobre un único neutro, sin latón
    - **Terracota + pizarra:** óxido cálido sobre gris frío, sin latón
    - **Oliva + ladrillo + papel:** oliva apagado más acento rojo ladrillo
    - **Monocromo puro + un pop saturado único:** blanco roto + negro roto + un acento brillante (azul eléctrico, esmeralda, rosa fuerte, etc.)
  * **Regla de rotación de paleta:** si el último proyecto de consumo premium que generaste usó la familia beige+latón, este DEBE usar una familia distinta. No entregues la misma paleta artesanal cálida dos veces seguidas.
  * **Excepción:** la paleta beige+latón+espresso solo es aceptable CUANDO el brief de marca nombre explícitamente esos colores, o cuando la identidad de marca sea genuinamente vintage / artesanal / de artesanía cálida Y puedas articular por qué esta paleta concreta encaja con esta marca concreta. Recurrir a ella por defecto porque "esto es un brief de batería de cocina" está prohibido.

### 4.3 Diversificación de layout
* **ANTI-SESGO CENTRADO:** Se evitan las secciones Hero / H1 centradas cuando `DESIGN_VARIANCE > 4`. Fuerza "Pantalla dividida" (50/50), "Contenido alineado a la izquierda / recurso alineado a la derecha", "Espacio en blanco asimétrico" o estructuras con fijación al desplazamiento.
* **Excepción:** el hero centrado es válido para briefs editoriales / manifiestos / anuncios de lanzamiento, donde el mensaje en sí es el diseño.

### 4.4 Materialidad, sombras, tarjetas
* Usa tarjetas SOLO cuando la elevación comunique una jerarquía real. De lo contrario, agrupa con `border-t`, `divide-y` o espacio negativo.
* Cuando se use una sombra, tíñela con el tono del fondo. Nada de sombras proyectadas negras puras sobre fondos claros.
* Para `VISUAL_DENSITY > 7`: los contenedores de tarjetas genéricos están prohibidos. Las métricas de datos respiran en un layout simple.
* **BLOQUEO DE CONSISTENCIA DE FORMA (obligatorio):** Elige UNA escala de radio de esquina para la página y mantenla. Opciones: todo angular (radio 0), todo suave (radio 12-16px), todo en píldora (radio completo para interactivos). Los sistemas mixtos solo se permiten cuando existe una regla documentada (por ejemplo, "los botones son píldora completa, las tarjetas tienen 16px, los campos tienen 8px") y esa regla se sigue en todas partes. Botones redondeados en un layout cuadrado, o tarjetas cuadradas en una página de botones en píldora, es un diseño roto.

### 4.5 Estados de la interfaz de usuario

Los LLM tienden por defecto a un "único estado estático exitoso". Implementa siempre ciclos completos:

* **Carga:** Cargadores esqueléticos que coincidan con la forma del diseño final. Evita los spinners circulares genéricos.
* **Estados vacíos:** Compuestos con cuidado; indican cómo poblar el contenido.
* **Estados de error:** Claros, en línea (formularios) o contextuales (toasts solo para los transitorios).
* **Retroalimentación táctil:** En `:active`, usa `-translate-y-[1px]` o `scale-[0.98]` para simular una pulsación física.
* **COMPROBACIÓN DE CONTRASTE DE BOTONES (obligatoria, a11y):** Antes de entregar cualquier botón, verifica que el texto del botón sea legible frente al fondo del botón. Botón blanco con texto blanco, `bg-white` CTA con etiqueta `text-white`, botón transparente sobre el fondo de la página sin borde → todos prohibidos. Audita cada CTA: ratio de contraste mínimo WCAG AA (4,5:1 para texto de cuerpo, 3:1 para texto grande de 18px o más). La misma regla se aplica a los botones ghost sobre fondos fotográficos (usa un fondo, una capa de atenuación o un trazo).
* **PROHIBICIÓN DE AJUSTE DE TEXTO EN CTA (obligatoria):** El texto del botón DEBE caber en una sola línea en escritorio. Si una etiqueta como "VER TRABAJO SELECCIONADO" se ajusta en 2 o 3 líneas, el botón está roto. Solución: acortar la etiqueta (3 palabras como máximo para CTA primarios, idealmente 1-2) O ensanchar el botón (no restrinjas artificialmente `max-width` en los CTA). Los CTA ajustados en escritorio son un fallo de verificación previa.
* **SIN INTENCIÓN DE CTA DUPLICADA (obligatoria):** Dos CTA con la misma intención en una misma página es un fallo de verificación previa. Ejemplos de la misma intención: "Ponte en contacto" + "Contáctanos" + "Hablemos" + "Inicia un proyecto" + "Empieza algo" + "Escríbenos" = todos con intención de "contacto" → elige UNA etiqueta y úsala en todas partes de la página (navegación, hero, pie de página). Lo mismo para "Pruébalo gratis" + "Empieza ya" + "Regístrate gratis" (todos con intención de "registro") y "Ver trabajos" + "Ver trabajo seleccionado" + "Explorar proyectos" (todos con intención de "portafolio"). Una etiqueta por intención.
* **COMPROBACIÓN DE CONTRASTE DE FORMULARIOS (obligatoria, a11y):** Los campos de formulario, el texto de marcador de posición, los anillos de foco, el texto de ayuda y el texto de error deben cumplir WCAG AA de contraste frente al fondo de la sección. Marcadores de posición claros sobre un formulario casi blanco, formulario blanco sobre sección de página blanca, etiquetas de formulario con contraste inferior a 4,5:1 → todos prohibidos. Audita cada formulario antes de entregarlo.

### 4.6 Patrones de datos y formularios
* Etiqueta ENCIMA del campo. El texto de ayuda es opcional, pero debe estar presente en el marcado. El texto de error va DEBAJO del campo. Estándar `gap-2` para los bloques de entrada.
* Nunca uses el marcador de posición como etiqueta. Jamás.

### 4.7 Disciplina de diseño (reglas estrictas. Incumplir cualquiera de ellas equivale a entregar trabajo roto)

* **El héroe DEBE caber en el viewport inicial.** Titular de máximo 2 líneas en escritorio, subtexto de máximo **20 palabras** Y máximo 3-4 líneas, CTAs visibles sin desplazarse. Si el texto es demasiado largo: reducir la escala de fuente O recortar el texto. Si no puedes describir la propuesta de valor en 20 palabras de subtexto, la propuesta de valor no está clara, no es que la regla sea demasiado estricta. Nunca dejes que el héroe se desborde y obligue a desplazarse para encontrar el CTA.
* **Disciplina de escala tipográfica en el héroe.** Planifica el tamaño de fuente y el tamaño de la imagen *juntos*. Si el recurso visual del héroe es grande y el titular tiene más de 6 palabras, no empieces en `text-7xl/text-8xl`. Rango razonable por defecto: `text-4xl md:text-5xl lg:text-6xl` para la mayoría de los héroes; `text-6xl md:text-7xl` solo cuando el titular tenga 3-5 palabras. Un titular de héroe de 4 líneas es siempre un error de tamaño de fuente, nunca un error de longitud del texto.
* **LÍMITE OBLIGATORIO DEL PADDING SUPERIOR DEL HÉROE:** El padding superior del héroe no debe superar `pt-24` (≈6rem) en escritorio. Más que eso hace que el contenido del héroe flote a mitad del viewport y se perciba como un error de maquetación, no como un espacio intencional. Si tu héroe necesita más espacio, aumenta la escala de fuente o el tamaño del recurso visual, no el padding superior.
* **DISCIPLINA DE ELEMENTOS EN EL HÉROE (máximo 4 elementos de texto).** El héroe es un momento único, no una lista de funciones. Elementos de texto permitidos, máximo 4 en total:
  1. Eyebrow (etiqueta pequeña en mayúsculas) O franja de marca O ninguno - elige cero o uno
  2. Titular (máximo 2 líneas, ver arriba)
  3. Subtexto (máximo 20 palabras, máximo 4 líneas)
  4. CTAs (1 primario + máximo 1 secundario)
  - **PROHIBIDO en el héroe:** texto pequeño de tagline debajo de los CTAs ("Funciona con GitHub, GitLab y Git autoalojado"), franja de confianza ("Usado por equipos de ingeniería en..."), anticipo de precios ("Gratis para uso individual, $10/usuario para equipos"), lista de viñetas de funciones, fila de avatares de prueba social. Todo eso debe ir a secciones dedicadas justo debajo del héroe.
  - Si tienes un eyebrow Y un tagline debajo de los CTAs en el mismo héroe, elimina el tagline. Si tienes una franja de marca Y un tagline, elimina el tagline. Como máximo un elemento de texto pequeño por héroe.
* **El muro de logotipos "Usado por" / "Confiado por" va DEBAJO del héroe, nunca dentro de él.** El héroe es para la propuesta de valor y el CTA principal. El muro de logotipos es una sección separada justo debajo. No metas logotipos de confianza en la misma fila flex que el texto del héroe.
* **La navegación DEBE mostrarse en una sola línea en escritorio.** Si los elementos no caben en `lg` (1024px), condensa las etiquetas, elimina elementos secundarios o pasa a un menú hamburguesa. Una navegación de dos líneas en escritorio es un diseño roto.
* **Altura máxima de la navegación: 80px en escritorio, por defecto 64-72px.** Nada de barras de navegación enormes estilo "agencia" que ocupen el 15% del viewport.
* **Las cuadrículas bento deben tener ritmo, no repetición unilateral.** No apiles 6 filas de imagen a la izquierda / texto a la derecha. Varía la composición: alterna filas de función a ancho completo, celdas de tamaños asimétricos, cortes verticales.
* **REGLA OBLIGATORIA DEL NÚMERO DE CELDAS BENTO:** Una cuadrícula bento tiene EXACTAMENTE tantas celdas como contenido tengas. 3 elementos → 3 celdas (división 1+2, 2+1 o trío asimétrico). 5 elementos → 5 celdas (2+3, 3+2, héroe+4, etc.). Si tu cuadrícula tiene una celda vacía en medio o al final, planificaste mal. Reforma la cuadrícula; no pegues una baldosa en blanco.
* **Prohibición de repetición de familias de diseño por sección.** Una vez que uses una familia de diseño para una sección (p. ej., tarjetas de imagen en 3 columnas, cita a ancho completo, texto-imagen dividido), esa familia puede aparecer como máximo UNA vez en la página. "Comisiones seleccionadas" no debe parecer "Lo que hacemos". Una página de aterrizaje con 8 secciones debe usar al menos 4 familias de diseño distintas.
* **LÍMITE OBLIGATORIO DE ALTERNANCIA EN ZIGZAG.** La alternancia "imagen a la izquierda + texto a la derecha" seguida de "texto a la izquierda + imagen a la derecha" es un diseño banal. Máximo 2 secciones seguidas con este patrón de división imagen+texto. La 3.ª división imagen+texto consecutiva es un fallo en la comprobación previa al vuelo. Rompe el patrón con una sección a ancho completo, una sección de pila vertical, una cuadrícula bento, un marquee o una familia de diseño distinta.
* **CONTENCIÓN DE EYEBROWS (obligatorio, la regla más incumplida en pruebas de producción).** Un "eyebrow" es la pequeña etiqueta en mayúsculas de interletrado amplio situada encima de un titular de sección (p. ej., `FOUR COLORWAYS`, `SELECTED WORK`, `THE HARDWARE`, `Git-native task management`). Firma CSS típica: `text-[11px] uppercase tracking-[0.18em]`, `font-mono text-[10.5px] uppercase tracking-[0.22em]`. Cada sitio construido con IA pone un eyebrow encima de CADA encabezado de sección, produciendo el mismo ritmo de plantilla. Regla estricta:
  - **Máximo 1 eyebrow por cada 3 secciones.** El héroe cuenta como 1. Así, una página con 9 secciones puede usar como máximo 3 eyebrows en total.
  - Si la sección A tiene un eyebrow, las 2 secciones siguientes no pueden tener ninguno.
  - **La comprobación previa al vuelo es mecánica:** cuenta las instancias de `uppercase tracking` (o etiquetas similares en versalitas monoespaciadas encima de titulares) en todos los componentes de sección. Si el recuento es > ceil(número de secciones / 3), la salida falla.
  - **Qué hacer en lugar de un eyebrow:** elimínalo por completo. El titular por sí solo basta. Si necesitas categorizar una sección, la ubicación de la sección en la página ya la categoriza; no hace falta ninguna etiqueta.
* **PROHIBICIÓN DEL ENCABEZADO DIVIDIDO (obligatorio).** El patrón "titular grande a la izquierda + párrafo explicativo pequeño a la derecha" como encabezado de sección (izquierda col-span-7/8, derecha col-span-4/5 con un párrafo de cuerpo pequeño flotando en la columna derecha) está **prohibido por defecto**. Las secciones deben tener UN mensaje centrado. Si genuinamente necesitas tanto un titular como un párrafo explicativo, apílalos verticalmente (titular arriba, cuerpo debajo, ancho máximo 65ch). Recurre al patrón de encabezado dividido solo cuando haya una razón compositiva real (p. ej., la columna derecha contiene un elemento visual o interactivo, no solo texto de relleno).
* **Diversidad de fondos en bento (obligatorio).** Las secciones bento y de cuadrícula de funciones no pueden ser 6 tarjetas blancas sobre blanco con texto dentro. Al menos 2-3 celdas en cualquier cuadrícula de varias celdas necesitan variación visual real: una imagen real, un degradado acorde a la marca (no morado de IA), un patrón o un fondo tintado. Una cuadrícula bento crema sobre crema con solo tipografía dentro se percibe como el valor por defecto genérico de IA, incluso cuando el resto de la página es buena.
* **El colapso en móvil debe ser explícito por sección.** Para cada diseño de varias columnas, declara el fallback `< 768px` en el mismo componente. Nada de suposiciones del tipo "funcionará, Tailwind se encarga".

### 4.8 Estrategia de imágenes y recursos visuales

Las páginas de destino y los portafolios son **productos visuales**. Las páginas solo de texto con capturas de pantalla falsas hechas con divs son relleno de baja calidad.

**Orden de prioridad para los recursos visuales:**
1. **Herramienta de generación de imágenes primero.** Si hay DISPONIBLE en el entorno alguna herramienta de generación de imágenes (`generate_image`, herramienta de imágenes MCP, generación integrada en el IDE, herramientas de imágenes de OpenAI, etc.), DEBES usarla para crear recursos específicos de cada sección: fotografía de héroe, fotos de producto, fondos de textura, imágenes de ambiente. Genera con la relación de aspecto adecuada para cada sección. No omitas este paso porque el CSS hecho a mano parezca más rápido.
2. **Imágenes web reales en segundo lugar.** Cuando no haya herramienta de generación disponible, usa fuentes de fotografía reales. Valores predeterminados aceptables:
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` para fotografía de marcador de posición (la semilla debe describir la sección, p. ej. `marrow-cookware-kitchen`)
   * URL reales de bancos de imágenes o de marca cuando el brief las proporcione
   * Fuentes de licencia abierta (Unsplash mediante URL directa, Pexels) si se permite explícitamente
3. **Último recurso: informar al usuario.** Si no es posible ninguna de las anteriores, NO llenes la página con ilustraciones SVG hechas a mano ni con "capturas de pantalla falsas" basadas en divs. En su lugar, deja espacios de marcador de posición claramente etiquetados (`<!-- TODO: hero product photo, 1600x1200 -->`) y, al final de la respuesta, di: *"Esta página necesita imágenes reales en: \[lista de ubicaciones\]. Por favor, genéralas o proporciónalas."*

**Incluso los sitios minimalistas necesitan imágenes reales.** Una página de solo texto no es minimalismo. Es un trabajo incompleto. Incluso un sitio editorial de estilo Linear necesita al menos 2-3 imágenes reales (héroe, una foto de producto o de estilo de vida, una imagen de apoyo). Genera fotografía minimalista en blanco y negro si el brief es sobrio; no omitas las imágenes por tener un nivel bajo de expresividad.

**Logotipos reales de empresas como prueba social.** Cuando el brief pida un muro de logotipos de "Con la confianza de / Usado por / Clientes", NO recurras por defecto a marcas tipográficas de texto plano (`<span>Acme Co</span>` estilizadas en una fila). Usa logotipos SVG reales:
* **Fuente: Simple Icons** (`https://cdn.simpleicons.org/{slug}/ffffff` para cualquier color, o el paquete npm `simple-icons`). Cubre la mayoría de las marcas conocidas.
* **Alternativa: devicon** para logotipos de stacks tecnológicos (`@svgr/cli` o CDN).
* **¿Inventas el nombre de la marca? Entonces inventa también una marca SVG.** Genera un monograma sencillo (una letra en un círculo, una ligadura de dos letras, un glifo abstracto) renderizado como `<svg>` en línea que coincida con el estilo de la página. Las marcas tipográficas de texto plano para nombres de marca inventados resultan genéricas.
* **Asegúrate siempre** de que los logotipos se vean tanto en modo claro como en modo oscuro (blanco sobre oscuro, negro sobre claro, o una variable de tema de un solo color).
* **Regla SOLO LOGOTIPOS (obligatoria):** el muro de logotipos = solo logotipos y nada más. NO escribas etiquetas de industria o categoría debajo de cada logotipo (nada de `Vercel` + `hosting` debajo, ni `Stripe` + `payments`, ni `Cloudflare` + `infra`). El logotipo es la credibilidad; la etiqueta no aporta nada que el usuario no sepa ya. Opcional: el nombre de la marca como texto alternativo para lectores de pantalla, y opcionalmente un enlace al sitio de la marca. Eso es todo.

**Ilustraciones hechas a mano:**
* Iconos SVG de bibliotecas: correcto (ver Sección 3.C).
* SVG decorativos hechos a mano (ilustraciones personalizadas, logotipos, marcas): **muy desaconsejados**, nunca como opción por defecto. Solo aceptables cuando:
  - El brief lo pide explícitamente ("dibújame un logotipo SVG")
  - Es una marca geométrica única y sencilla (un cuadrado, un círculo, un nombre en tipografía de display)
  - Tienes plena confianza en la calidad del resultado

**Las capturas de pantalla falsas basadas en divs están prohibidas.** Una "vista previa de producto hecha a mano" renderizada con rectángulos `<div>`, listas de tareas falsas, dashboards falsos o ventanas de terminal falsas es un indicio delator. Si necesitas mostrar un producto:
* Usa una URL de captura de pantalla real si existe
* Genera una mediante la herramienta de imágenes
* Usa una vista previa real de componente (una versión miniatura auténtica de la interfaz dentro de la página)
* O prescinde de la vista previa y usa fotografía editorial

**El héroe necesita un recurso visual real.** Texto + mancha de degradado no es un héroe: es un marcador de posición.

### 4.9 Densidad de contenido

Las páginas de destino viven de la **primera impresión**, no de la lectura completa. Recorta sin piedad.

* **Estructura de contenido predeterminada por sección:** titular breve (≤ 8 palabras) + párrafo breve de apoyo (≤ 25 palabras) + un recurso visual O un CTA. Cualquier cosa adicional debe justificarse por la función de la sección.
* **Nada de secciones volcado de datos.** Una tabla de publicaciones de 20 filas, una lista de premios de 30 filas, una matriz de precios gigante en una página de marketing = diseño incorrecto. Use:
  - Las 3-5 cifras destacadas principales + un enlace "Ver lista completa"
  - Marquesina / carrusel para amplitud
  - Una página distinta por completo si el dato es el producto
* **Las listas largas necesitan otro componente de interfaz, no una lista más larga.** Por defecto `<ul>` con viñetas / filas `divide-y` es la opción perezosa. Si tiene más de 5 elementos, recurra a una de estas opciones:
  - División en 2 columnas con elementos agrupados
  - Cuadrícula de tarjetas con imagen + etiqueta por elemento
  - Pestañas / acordeón si los elementos pueden categorizarse
  - Píldoras de desplazamiento horizontal con ajuste (scroll-snap)
  - Carrusel para listas de amplitud (testimonios, logotipos, capacidades)
  - Marquesina para "muchas cosas que no necesitan atención individual"
  Una ficha técnica de 10 filas con una línea fina bajo cada fila es la opción predeterminada PEOR. Agrupe las filas en 2-3 bloques con separadores discretos, o pase a un diseño de una tarjeta por especificación.
* **Fichas técnicas específicamente (el patrón de batería de cocina Marrow).** Una tabla de especificaciones de producto larga con `border-b` en cada fila es el valor predeterminado de la IA para briefs de batería de cocina, hardware, indumentaria y artículos artesanales. Prohibido. Alternativas concretas:
  - **Cuadrícula de tarjetas de 2 columnas:** cada especificación tiene su propia tarjeta con el nombre de la especificación, el valor (número grande destacado) y un cuerpo de una línea sobre "por qué importa". Tarjetas dispuestas en 2 columnas en escritorio y 1 columna en móvil.
  - **Píldoras horizontales con ajuste (scroll-snap):** cada especificación es una píldora y el usuario puede desplazarse por ellas.
  - **Bloques agrupados:** agrupe 10 especificaciones en 3 grupos lógicos (por ejemplo, "Materiales", "Cocción", "Garantía"); cada grupo recibe UN separador suave y un encabezado de grupo.
  - **Destacadas frente al resto:** 3-4 especificaciones principales visualizadas como mosaicos grandes destacados; el resto se pliega bajo un desplegable "Ver especificaciones completas".

* **AUDITORÍA DE COPY (obligatoria antes de entregar):** Antes de declarar terminada cualquier tarea, relea cada cadena visible de la página (titulares, subtítulos, antetítulos, etiquetas de botones, texto del cuerpo, pies de foto, texto alternativo, texto del pie de página, mensajes de error). Marque cualquier cadena que sea:
  - **Gramaticalmente incorrecta** ("gratis en su pasado", "dos planes pero uno es honesto", "poner sobre la mesa" fuera de contexto)
  - **Con referentes poco claros** ("planeamos seguir así" sin contexto previo)
  - **Que suene a alucinación de IA** (juegos de palabras ingeniosos pero erróneos, metáforas forzadas que no se sostienen, frases de "nada elegante")
  - **Que parezca escrito por un LLM intentando sonar reflexivo** (humildad pasivo-agresiva, etiquetas de artesano falsas, microcomentarios meta poéticos impostados)
  Reescriba cada cadena marcada. Si no está seguro de si una cadena tiene sentido, reemplácela por una frase funcional y sencilla. El texto "ingenioso" generado por IA es peor que el texto aburrido.
* **Las cifras falsamente precisas se marcan.** Números como `92%`, `4.1×`, `48k`, `5.8 mm`, `13.4 lb` deben:
  - Proceder de datos reales (brief, directrices de marca, métricas públicas): correcto
  - Estar explícitamente etiquetados como simulados (`<!-- mock -->`, "ejemplo", "datos de muestra"): correcto
  - Ser estéticas de especificación inventadas por la IA: prohibido. No simule una precisión técnica que la marca no afirma.
* **Un solo registro de texto por página.** No mezcle lenguaje técnico en monoespaciada ("47 tareas · 0,6 cambios de contexto/día"), prosa editorial y frases de marketing contundentes en la misma composición, a menos que la voz de marca lo exija explícitamente.

### 4.10 Citas y testimonios

* **Máximo 3 líneas** de texto de cita. Nunca 6. Si la cita original es más larga, recórtela. Una cita de página de aterrizaje es un fragmento, no la reseña completa.
* En tamaños de fuente muy pequeños (por ejemplo, testimonios de estilo pie de página), el límite de líneas puede estirarse ligeramente. Espíritu: "se lee de un vistazo".
* **Sin guiones largos dentro del texto de la cita** como adorno de diseño (pausas largas, guiones largos cinéticos, viñetas con guion largo). Vea la sección 9.G: el guion largo está completamente prohibido.
* Atribución: nombre + cargo + (opcionalmente) empresa. Nunca solo el nombre (por ejemplo, "- Sarah").
* Comillas: use comillas tipográficas reales ( " " ) o ninguna. No comillas rectas ASCII ( " ).

### 4.11 Bloqueo de tema de página (coherencia entre modo claro y oscuro)

La página tiene UN solo tema. Las secciones no se invierten.

* Si la página está en modo oscuro, TODAS las secciones están en modo oscuro. No se intercala una sección clara de tono papel cálido entre secciones oscuras (ni al revés). El usuario no debe sentir que ha entrado en otro sitio web a mitad del desplazamiento.
* La excepción: si el brief pide explícitamente un recurso de "Historia en bloques de color" o "Cambio de tema al desplazarse" y se trata de una composición deliberada (un único cambio completo de tema con una transición marcada, no una alternancia aleatoria), se permite una vez por página.
* Comportamiento predeterminado: elija claro, oscuro o automático (`prefers-color-scheme`) a nivel de página y bloquéelo. Los matices de fondo a nivel de sección dentro de la misma familia de tema están bien (`bg-zinc-950` junto a `bg-zinc-900`); cambiar a `bg-amber-50` en mitad de una página `bg-zinc-950` está roto.
* Cuando use un sistema de diseño con temas integrados (Radix Themes, shadcn/ui con `<Theme>`), establezca el tema UNA VEZ en `layout.tsx` o en la raíz de la página. No permita que las secciones individuales lo sobrescriban.

---

## 5. PROACTIVIDAD SENSIBLE AL CONTEXTO

Estas son herramientas, no valores predeterminados. Úselas cuando la lectura del diseño lo requiera. **Ninguna se activa automáticamente.**

* **Liquid Glass / Glassmorphism:** Apropiado para productos de consumo premium, marcas de lujo o de estilo cercano a Apple, o superposiciones de medios. Inapropiado para paneles de control, sector público o B2B "aburrido". Cuando se use, ve más allá de `backdrop-blur`: añade un borde interior de 1px (`border-white/10`) y una sombra interior sutil (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) para simular la refracción física del borde. Proporciona un respaldo de relleno sólido bajo `prefers-reduced-transparency`.
* **Micro-física magnética:** Úsala cuando `MOTION_INTENSITY > 5` Y el brief sugiera un tono premium / lúdico / de agencia. Impleméntala EXCLUSIVAMENTE con `useMotionValue` / `useTransform` de Motion, fuera del ciclo de renderizado de React. Nunca `useState`. Consulta la Sección 3.B.
* **Micro-interacciones perpetuas** (Pulso, Máquina de escribir, Flotar, Brillo, Carrusel): Úsalas cuando `MOTION_INTENSITY > 5` Y la sección se beneficie activamente del movimiento (indicadores de estado, feeds en vivo, sensación de IA). **No toda tarjeta necesita un bucle infinito.** Si una sección es informativa, déjala estática. Aplica física de resortes (`type: "spring", stiffness: 100, damping: 20`), nada de easing lineal.
* **"Movimiento declarado, movimiento mostrado."** Si `MOTION_INTENSITY > 4`, la página debe moverse de verdad: transiciones de entrada en el hero, revelado al hacer scroll en las secciones clave y física al pasar el cursor sobre los CTA, como mínimo. Una página estática que declara `MOTION_INTENSITY: 7` está rota. Por el contrario, si no puedes entregar movimiento funcional dentro del alcance disponible, reduce el dial a 3 y entrega una página estática limpia. Nunca construyas a medias un movimiento que falle (ScrollTriggers cortados, entradas bruscas, limpiezas faltantes).
* **EL MOVIMIENTO DEBE TENER MOTIVO (obligatorio).** Antes de añadir cualquier animación, pregúntate: "¿qué comunica esta animación?" Respuestas válidas: jerarquía (llamar la atención sobre lo correcto), narrativa (revelar contenido en secuencia acorde a una historia), retroalimentación (reconocer una acción del usuario), transición de estado (mostrar que algo cambió). Respuesta inválida: "se veía bien". Usar GSAP en todas partes porque está disponible es de principiante. Cada ScrollTrigger, cada marquesina y cada sección fijada necesita un motivo. Si no puedes articularlo en una frase, elimina la animación.
* **MARQUESINA: MÁXIMO UNA POR PÁGINA (obligatorio).** Las marquesinas de texto con desplazamiento horizontal ("logotipos que se desplazan sin fin", "manifiesto que se desplaza de lado", "tira de palabras cinética") son apropiadas como máximo UNA vez por página. Dos o más marquesinas en la misma página resultan en relleno perezoso. Elige la única sección donde la marquesina realmente sirve al contenido; las demás usan otro diseño.
* **Patrón GSAP de pila pegajosa (cuando se use scroll-stack).** Una "pila de tarjetas al hacer scroll" debe ser una pila pegajosa REAL, no una lista de revelado secuencial. Consulta la Sección 5.A más abajo para el esqueleto de código canónico. Fallo común: el disparador se activa a mitad del scroll en lugar de fijarse en la parte superior del viewport. Solución: `start: "top top"`, no `start: "top center"` ni `"top 80%"`.
* **Patrón GSAP de paneo horizontal (cuando se use secuestro de scroll horizontal).** Consulta la Sección 5.B más abajo para el esqueleto canónico. Fallo común: la animación empieza antes de que la sección esté fijada, así que el usuario ve media diapositiva. Misma solución: `start: "top top"`, fijar el contenedor y animar con scrub la pista interna.

### 5.A Pila pegajosa: esqueleto canónico

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

Puntos críticos: `start: "top top"`, `pin: true`, cada tarjeta excepto la última queda fijada, y la transformación de escala/opacidad se controla con el disparador de scroll de la SIGUIENTE tarjeta (así la tarjeta anterior se reduce cuando llega la siguiente).

### 5.B Paneo horizontal: esqueleto canónico

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

Puntos críticos: `start: "top top"`, `pin: true`, `end: "+=${distance}"` (la longitud del scroll debe igualar el recorrido horizontal necesario), `scrub: 1`. El contenedor queda fijado y la pista interna se desliza horizontalmente mientras el usuario hace scroll vertical.

### 5.C Escalonado de revelado al hacer scroll: esqueleto canónico (alternativa más ligera)

Para "los elementos aparecen al entrar en el viewport" simple (sin fijar), prefiere `whileInView` de Motion en lugar de GSAP: es más ligero y no necesita ScrollTrigger:

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

Úsalo para: listas de características, cuadrículas de testimonios, muros de logotipos, cualquier cosa que solo necesite "entrar al hacer scroll". Reserva GSAP para trabajo real de fijado y scrub.

### 5.D Patrones de animación prohibidos

* **`window.addEventListener("scroll", ...)`** está prohibido. Se ejecuta en cada frame de scroll, es propenso a jank y no tiene agrupación. Usa `useScroll()` de Motion, `ScrollTrigger` de GSAP, IntersectionObserver, o CSS `scroll-driven animations` (`animation-timeline: view()`).
* **Cálculos personalizados de progreso de scroll con `window.scrollY`** en el estado de React. Por la misma razón. Re-renderiza en cada frame.
* **Bucles `requestAnimationFrame` que tocan el estado de React.** Usa valores de movimiento (`useMotionValue` + `useTransform`) en su lugar.
* **Transiciones de diseño:** Usa las props `layout` y `layoutId` de Motion para cambios de estado visibles (reordenar listas, expandir modales, elementos compartidos entre rutas). No envuelvas contenido estático en props `layout` "por si acaso", porque cuesta trabajo de medición.
* **Orquestación escalonada:** Usa `staggerChildren` (Motion) o la cascada CSS (`animation-delay: calc(var(--index) * 100ms)`) para momentos de revelado donde la secuencia importa. Para `staggerChildren`, el padre (`variants`) y los hijos DEBEN compartir el mismo árbol de Componentes Cliente.

---

## 6. BARRERAS DE RENDIMIENTO Y ACCESIBILIDAD

### 6.A Aceleración por hardware
* Anima SOLO `transform` y `opacity`. Nunca animes `top`, `left`, `width`, `height`.
* Usa `will-change: transform` con moderación: solo en elementos que realmente se van a animar.

### 6.B Movimiento reducido (obligatorio)
* **Todo movimiento por encima de `MOTION_INTENSITY > 3` DEBE respetar `prefers-reduced-motion`.** Esto no es negociable.
* En Motion: envuélvelo con `useReducedMotion()` y degrádalo a estático.
* En CSS: condiciona las animaciones mediante `@media (prefers-reduced-motion: no-preference)` o proporciona un bloque de anulación bajo `@media (prefers-reduced-motion: reduce)` que las desactive.
* Los bucles infinitos, el paralaje, el secuestro de scroll y la física magnética DEBEN colapsar a estático o instantáneo con movimiento reducido.

### 6.C Modo oscuro (obligatorio para cualquier página orientada al consumidor)
* Diseñe para **ambos modos desde el principio**. Nunca publique solo en claro ni solo en oscuro sin instrucción explícita del usuario.
* Use la variante `dark:` de Tailwind O variables CSS para los tokens. Elija una sola estrategia por proyecto.
* **No prescriba aquí colores específicos para el modo oscuro.** El brief decide. Mantenga la jerarquía visual, la identidad de marca y el contraste WCAG AA (AAA para el cuerpo del texto) en ambos modos.
* Respete `prefers-color-scheme: dark`. Por defecto, use la preferencia del sistema, salvo que la marca exija un modo concreto.

### 6.D Objetivos de Core Web Vitals
* **LCP** < 2,5 s. La imagen principal (hero) debe ser `next/image priority` o precargada.
* **INP** < 200 ms. Traslade el trabajo pesado fuera del hilo principal.
* **CLS** < 0,1. Reserve espacio para imágenes, fuentes e incrustaciones.
* Ejecute Lighthouse antes de dar por terminada una página.

### 6.E Coste del DOM
* Aplique los filtros de grano / ruido EXCLUSIVAMENTE a pseudoelementos fijos, `pointer-events-none` (p. ej., `fixed inset-0 z-[60] pointer-events-none`). NUNCA sobre contenedores con desplazamiento: los repintados continuos de la GPU destruyen los FPS en móviles.
* Tenga en cuenta el tamaño del paquete. El movimiento no es pequeño; Three.js es grande. Cargue de forma diferida todo lo que no esté por encima del pliegue.

### 6.F Restricción del z-index
NUNCA abuse de `z-50` ni de `z-10` arbitrarios. Use z-index estrictamente para contextos de capa sistémicos (barras de navegación fijas, modales, superposiciones, grano). Documente la escala de z-index en un archivo de constantes del proyecto.

---

## 7. DEFINICIONES DE DIALES (Referencia técnica)

### DESIGN_VARIANCE (Nivel 1-10)
* **1-3 (Predecible):** Cuadrícula CSS simétrica (12 columnas, unidades fr iguales), márgenes interiores iguales, alineación centrada.
* **4-7 (Desplazado):** Superposiciones `margin-top: -2rem`, proporciones de imagen variadas (4:3 junto a 16:9), encabezados alineados a la izquierda sobre datos centrados.
* **8-10 (Asimétrico):** Diseños tipo masonry, CSS Grid con unidades fraccionarias (`grid-template-columns: 2fr 1fr 1fr`), zonas vacías masivas (`padding-left: 20vw`).
* **ANULACIÓN PARA MÓVIL:** Para los niveles 4-10, los diseños asimétricos por encima de `md:` DEBEN colapsar a una sola columna estricta (`w-full`, `px-4`, `py-8`) en viewports `< 768px`.

### MOTION_INTENSITY (Nivel 1-10)
* **1-3 (Estático):** Sin animaciones automáticas. Solo estados CSS `:hover` y `:active`. `prefers-reduced-motion` es de todos modos el modo por defecto.
* **4-7 (CSS fluido):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` en cascada para las entradas de carga. Céntrese en `transform` y `opacity`.
* **8-10 (Coreografía avanzada):** Revelados complejos activados por desplazamiento, paralaje, animación controlada por scroll (CSS `animation-timeline` o GSAP ScrollTrigger). Use hooks de Motion. **NUNCA use `window.addEventListener('scroll')`**: es una prohibición estricta, no una preferencia. Consulte la Sección 5.D para las alternativas permitidas.

### VISUAL_DENSITY (Nivel 1-10)
* **1-3 (Galería de arte):** Mucho espacio en blanco. Separaciones de sección enormes (de `py-32` a `py-48`). Caro, limpio.
* **4-7 (App diaria):** Espaciado estándar de aplicación web (de `py-16` a `py-24`).
* **8-10 (Cabina de mando):** Márgenes interiores ajustados. Sin cajas de tarjetas; líneas de 1px separan los datos. Obligatorio: `font-mono` para todos los números.

---

## 8. PROTOCOLO DE MODO OSCURO

Doble modo por defecto. Nunca asuma solo modo claro, salvo que el brief sea un editorial que emule impresión.

### 8.A Estrategia de tokens (elija una y manténgala)
* **Variante `dark:` de Tailwind** (predeterminada para proyectos utility-first): cada utilidad de color emparejada con su variante oscura (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
* **Variables CSS** (para shadcn/ui, Radix Themes o bibliotecas de componentes con temas): defina tokens semánticos (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) e intercambie valores bajo `[data-theme="dark"]` o `@media (prefers-color-scheme: dark)`.

### 8.B No prescriba colores específicos aquí
El brief y la marca deciden. Esta skill solo exige:
* **Contraste**: mínimo WCAG AA para el texto del cuerpo, objetivo AAA para el texto principal (hero).
* **Paridad de jerarquía**: la jerarquía visual que funciona en claro debe funcionar en oscuro. Si un CTA destaca en claro, destaca en oscuro.
* **Fidelidad de marca**: el color principal de la marca debe seguir siendo reconocible. No desatúre la marca al pasarla a modo oscuro.
* **Nada de `#000000` puro ni de `#ffffff` puro**: use negro desaturado (zinc-950, gris cálido casi negro) y blanco desaturado. Los valores puros destruyen la profundidad.

### 8.C Modo por defecto
Respete `prefers-color-scheme` salvo que la marca exija lo contrario. Añada un conmutador manual si cualquiera de los dos modos perdería expresión clave de la marca.

### 8.D Pruebe en ambos modos antes de terminar
Abra la página en ambos modos durante el desarrollo. No publique una página que solo haya visto en un modo.

---

## 9. SEÑALES DE IA (Patrones prohibidos)

Evite estas firmas salvo que el brief las pida explícitamente.

### 9.A Visual y CSS
* **NADA de neones / resplandores exteriores** por defecto. Use bordes interiores o sombras tintadas sutiles.
* **NADA de negro puro (`#000000`).** Negro desaturado, zinc-950 o carbón.
* **NADA de acentos sobresaturados.** Desatúrelos para integrarlos con los neutros.
* **NADA de texto con degradado excesivo** en encabezados grandes.
* **NADA de cursores de ratón personalizados.** Obsoletos, hostiles a la accesibilidad y al rendimiento.

### 9.B Tipografía
* **EVITE Inter como predeterminada.** Consulte la Sección 4.1. Existe una vía de anulación.
* **NADA de H1 sobredimensionados** que solo griten. Controle la jerarquía con peso y color, no con escala bruta.
* **Restricciones de serif:** serif para editorial / lujo / publicación. No para paneles de control.

### 9.C Diseño y espaciado
* Márgenes interiores y exteriores **matemáticamente perfectos**. Nada de elementos flotantes con huecos extraños.
* **NADA de 3 tarjetas de características iguales en columnas.** La típica fila de "tres tarjetas idénticas en horizontal" está prohibida. Use una cuadrícula zig-zag de 2 columnas, asimétrica, fijada al scroll o con alternativa de desplazamiento horizontal.

### 9.D Contenido y datos (efecto "Jane Doe")
* **NO nombres genéricos.** "John Doe", "Sarah Chan", "Jack Su" → usa nombres creativos, realistas y adecuados a la localidad.
* **NO avatares genéricos.** Nada de iconos SVG de "huevo" ni iconos de usuario de Lucide → usa marcadores de foto creíbles o un estilo específico.
* **NO números perfectos y artificiales.** Evita `99.99%`, `50%`, `1234567`. Usa datos orgánicos e imperfectos (`47.2%`, `+1 (312) 847-1928`).
* **NO nombres de marca de relleno de startup.** "Acme", "Nexus", "SmartFlow", "Cloudly" → inventa nombres premium y contextuales que suenen reales.
* **NO verbos de relleno.** "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize" → usa verbos concretos.

### 9.E Recursos y componentes externos
* **NO iconos SVG hechos a mano.** Usa Phosphor / HugeIcons / Radix / Tabler. Lucide solo por petición explícita.
* **Los SVG decorativos hechos a mano están fuertemente desaconsejados** como opción por defecto (ver Sección 4.8).
* **NO capturas de pantalla falsas con divs.** Nunca construyas una interfaz de producto falsa con rectángulos `<div>` para simular una captura de pantalla. Usa imágenes reales, imágenes generadas u omite la vista previa.
* **NO enlaces rotos de Unsplash.** Usa `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`, marcadores de foto generados o recursos reales.
* **Personalización de shadcn/ui:** Permitida, pero NUNCA en estado por defecto. Personaliza radios, colores, sombras y tipografía según la estética del proyecto.
* **Limpieza lista para producción:** Código visualmente limpio, memorable y meticulosamente refinado.

### 9.F Señales de prueba de producción (prohibidas de forma absoluta)

Estos patrones surgieron de pruebas reales de páginas de aterrizaje generadas por LLM. Son las firmas a las que el modelo recurre cuando intenta "parecer diseñado". Tómalos como prohibiciones estrictas, salvo que el brief pida explícitamente alguno.

**Héroe y parte superior de la página**
* **NO etiquetas de versión en el héroe.** `V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA`: prohibidas como cejas predeterminadas. Solo aceptables cuando el brief trate explícitamente sobre el lanzamiento o la vista previa de un producto.
* **NO subcejas tipo "Marca · No. 01".** Líneas de micrometadatos como "Marrow · No. 01 · The 6-quart". Omítelas.

**Numeración de secciones y microetiquetas**
* **NO cejas con número de sección.** `00 / INDEX`, `001 · Capabilities`, `002 · Featured commission`, `06 · how it works`, `05 · The honest table`: prohibidas. Las cejas deben nombrar el tema en lenguaje llano, no enumerar.
* **NO paginación al estilo `01 / 4` en imágenes o tarjetas de bento.** Si el usuario puede contar, no necesita la etiqueta.
* **NO indicaciones de desplazamiento al estilo `Scroll · 001 Capabilities`.** Basta una flecha simple o "Scroll"; sin prefijo numérico de sección.
* **NO etiquetas de rango tipo "Index of Work, 2018 - 2026"** como cejas. Di simplemente qué es la sección.

**Separadores y puntos**
* **El punto medio (`·`) se racionaliza.** Máximo 1 por línea en las tiras de metadatos. NO lo uses como separador predeterminado para todo ("foo · bar · baz · qux · quux"). Si necesitas una familia de separadores, prefiere saltos de línea, filetes o columnas.
* **NO puntos de estado de color decorativos en cada lista, navegación o insignia.** Un punto de color antes de "ONE Q4 SLOT OPEN", antes de cada enlace de navegación o de cada fila de tarea: prohibido por defecto. Aceptable solo cuando el punto transmite un estado semántico real (estado de un servidor, indicador de disponibilidad) y se usa con moderación.

**Guiones largos y adornos tipográficos**
* **NO guion largo (`—`) como elemento de diseño NI en ningún otro lugar.** Consulta la Sección 9.G más abajo para la prohibición completa e inamovible. El carácter de guion largo está prohibido en titulares, cejas, píldoras, texto del cuerpo, citas, atribuciones, pies de foto, texto de botones y texto alternativo. Usa el guion normal (`-`).
* **NO titulares partidos y en cursiva** `<br>` como "movimiento de diseño" predeterminado. Divisiones tipo "for thirty\<br\>*years.*". Los titulares deben leerse de forma natural primero y ser ingeniosos solo cuando el brief lo exija.
* **NO texto vertical rotado** ("INDEX OF WORK, 2018 - 2026" girado 90°). Cliché de portafolios de agencias. Úsalo solo cuando el brief sea explícitamente de agencia / Awwwards / experimental Y sirva a un propósito real de composición.
* **NO retículas ni líneas finas de cruce como decoración.** Líneas verticales y horizontales trazadas solo para que la página "parezca diseñada": prohibidas. Úsalas solo cuando organicen contenido real.

**Vistas previas de producto falsas**
* **NO interfaces de producto falsas con divs en el héroe** (lista de tareas falsa, terminal falsa, panel falso construido con divs estilizados). Es la señal n.º 1 del diseño con LLM. Usa una captura real, una imagen generada, una vista previa de componente real o ninguna.
* **NO pies de versión falsos** ("v0.6.2-rc.1", "last sync 4s ago · main") dentro de capturas falsas. No aportan nada y delatan el origen con IA.

**Señales de copy de marketing**
* **NO encabezados de prueba social "Quietly in use at" / "Quietly trusted by".** Usa lenguaje natural: "Trusted by", "Used at", "Customers include", o elimina el encabezado si los logotipos hablan por sí solos.
* **NO etiquetas poéticas tipo "From the field" / "Field notes" / "Currently on the bench" / "On our desks" / "Loose plates"** en secciones de citas, blog o barras laterales. Suenan a artesano performativo. Usa etiquetas funcionales y simples ("Testimonials", "Latest writing", "Now working on") o no pongas etiqueta.
* **NO referencias industriales falsamente humildes** del tipo "We respect the French ones" en el cuerpo del texto. Cursi y con aire de IA.
* **NO tiras de clima o localidad** ("LIS 14:23 · 18°C") en encabezados o pies, salvo que el brief trate explícitamente sobre un lugar o un estudio distribuido por zonas horarias.
* **NO micro-frases de metadatos bajo las cejas.** Frases como *"Each of these is a feature we ship today, not a roadmap promise. The list will stay short on purpose."* bajo un titular de sección son desorden. Ceja + titular + cuerpo es suficiente.
* **NO etiquetas de paso genéricas.** "Stage 1 / Stage 2 / Stage 3", "Step 1 / Step 2 / Step 3", "Phase 01 / Phase 02 / Phase 03", "Pass One / Pass Two / Pass Three". Prohibidas. El contenido real del paso es la etiqueta. Si necesitas mostrar progresión, usa directamente el verbo-sustantivo ("Install", "Configure", "Ship"), no "Stage 1: Install".

**Pastillas, etiquetas y sellos de versión**
* **NINGUNA pastilla/etiqueta/tag superpuesta sobre imágenes.** Nada de superposiciones `<span>` sobre fotos con etiquetas como `Brand · 02`, `PLATE · BRAND`, `Field notes - journal`. O bien deja que la imagen hable por sí sola, o añade un pie de foto justo debajo (fuera de la imagen).
* **NINGÚN crédito fotográfico como decoración.** Cadenas como `Field study no. 12 · Ines Caetano`, `Plate 03 · House archive`, `Frame XII · 35mm` bajo imágenes de stock o picsum son pretenciosas. El crédito fotográfico solo se permite CUANDO hay un fotógrafo real acreditado por una foto real (con permiso). De lo contrario: omite el pie de foto o usa un pie funcional de una línea ("La de 6 cuartos, en Sage.").
* **NINGÚN pie de versión en páginas de marketing.** Cadenas de pie como `v1.4.2`, `Build 0048`, `last sync 4s ago · main` son accesorios de CLI / devtool, no contenido de página de aterrizaje. Prohibidas en páginas de marketing, landing o portafolio.
* **NADA de contadores de existencias en vivo tipo "Reserva 412 de 800"** como decoración. Solo si el brief es explícitamente una lista de espera de tirada limitada con datos reales.

**Bandas de texto decorativo**
* **NINGUNA banda de texto decorativa en la parte inferior del hero.** Patrones como `BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION`, `DESIGN · BUILD · SHIP`, `ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.` como una pequeña banda monoespaciada en mayúsculas a lo ancho de la parte inferior del hero son un cliché de portafolio de agencia. Prohibidas por defecto. Solo aceptables cuando la banda contiene enlaces reales y navegables (barra de navegación inferior fija) o información de estado real (banner de cookies, información de build en un sitio de documentación).
* **NINGÚN subtexto flotante en la esquina superior derecha de los encabezados de sección.** Patrón: la sección tiene un titular gigante alineado a la izquierda; en la esquina superior derecha del mismo encabezado hay un pequeño párrafo explicativo flotando sin alineación clara con nada más. Ese elemento flotante es el Tell. O bien coloca el subtexto directamente debajo del titular, o construye un encabezado limpio de 2 columnas (izquierda: titular, derecha: cuerpo alineado), pero no un pequeño párrafo en la esquina.

**Listas, divisores y puntuación**
* **NINGÚN `border-t` + `border-b` en cada fila de una lista larga / tabla de especificaciones.** Elige uno (borde inferior entre filas O borde superior encima del grupo) y úsalo con moderación. Una tabla de especificaciones de 10 filas con líneas finas bajo cada fila es el diseño más perezoso; consulta la Sección 4.9 para componentes de UI alternativos.
* **NINGUNA barra de puntuación/progreso con pistas de fondo rellenas** como visualización de comparación. Si necesitas mostrar comparaciones "X de Y", prefiere un número con un pequeño icono, o una pequeña barra en línea SIN pista de fondo. Las grandes pistas rellenas `bg-zinc-200` con un relleno parcial encima son ruido de interfaz de panel en una página de aterrizaje.

**Configuración regional, hora e indicaciones de desplazamiento**
* **Las bandas de configuración regional / nombre de ciudad / hora / clima están prohibidas en el 99% de los briefs.** "Lisboa, trabajando con fundadores" en el hero, "1200-690 Lisboa, Portugal" en el pie, "Lisboa 14:23 · 18°C" en la navegación. Son señales de decoración de portafolio de agencia. Permitidas SOLO cuando: el brief describe explícitamente un estudio distribuido globalmente con trabajo relevante por zona horaria, O una marca centrada en viajes, O un lugar físico real. Una única mención de dirección de contacto en el pie es aceptable; una banda atmosférica de ubicación no lo es.
* **Las indicaciones de desplazamiento están prohibidas.** `Scroll`, `↓ scroll`, `Scroll to explore`, `Scroll to walk through it`, iconos animados de rueda de ratón. Si el usuario aún no ha hecho scroll, está mirando el hero. Sabe lo que es desplazarse. La parte inferior de la ventana no necesita una etiqueta.
* **CERO puntos de estado decorativos por defecto.** Un punto de color antes de los elementos de navegación, antes de las filas de lista, antes de las insignias o las etiquetas de estado es un Tell. Solo aceptable cuando transmite un estado semántico real (un indicador en vivo del estado real de un servidor, una bandera de disponibilidad en tiempo real) y limitado a uno por sección de la página.

### 9.G PROHIBICIÓN DEL GUION LARGO (el Tell más incumplido)

**El guion largo (`—`) está COMPLETAMENTE prohibido.** Es el muleto estilístico característico del LLM y el Tell visual n.º 1 en las pruebas de producción. No hay excepción de "uso limitado", ni excepción de "frecuencia de lenguaje natural", ni excepción de "en el texto principal está bien". Ninguna.

* **Prohibido en titulares.** Usa un punto o una coma.
* **Prohibido en antetítulos / etiquetas / pastillas / texto de botones / pies de imagen / elementos de navegación.** Sustitúyelo por saltos de línea, columnas o líneas finas.
* **Prohibido en el texto principal.** Reestructura la oración: dos oraciones con punto, O una coma, O paréntesis, O dos puntos.
* **Prohibido en la atribución de citas.** Usa un guion normal con espacios (` - `) o un salto de línea + nombre con un peso tipográfico menor.
* **También prohibido en forma de semirraya (`–`) cuando se usa como separador.** Los rangos de fechas (`2018-2026`) usan guion. Los rangos numéricos (`€40-80k`) usan guion.

Los ÚNICOS caracteres de guion permitidos en la página son:
* Guion normal `-` (para palabras compuestas, rangos, divisores de línea en el marcado)
* Signo menos en matemáticas (`-5°C`)

Si tu resultado contiene un solo `—` o `–` visible para el usuario, el resultado no supera la Comprobación Previa y debe reescribirse.

Esta regla es innegociable. El agente ha ignorado históricamente los límites de guiones largos cuando se formulan como "usar con moderación". La formulación aquí es binaria: cero guiones largos.

---

## 10. VOCABULARIO DE REFERENCIA (Nombres de patrones que el agente debe conocer)

Esto es un vocabulario, no una biblioteca. El agente debe CONOCER estos nombres de patrones para comunicarse sobre ellos, diseñar teniéndolos en cuenta y recurrir a ellos cuando la lectura del diseño lo requiera. **Las implementaciones y los esbozos de código están en la Biblioteca de Bloques (Sección 12), que se completa de forma iterativa.**

### Paradigmas de Hero
* **Hero de División Asimétrica** - Texto a un lado, recurso al otro, amplio espacio en blanco.
* **Hero de Manifiesto Editorial** - Tipografía grande, sin recurso, casi un póster.
* **Hero de Máscara de Video / Medios** - Tipografía recortada como máscara sobre un fondo de video.
* **Hero de Tipografía Cinética** - Tipografía animada como elemento visual principal.
* **Hero de Revelación tipo Cortina** - Las partes del hero se despliegan al hacer scroll como una cortina.
* **Hero Fijado al Scroll** - El hero permanece fijo mientras el contenido se desplaza por detrás.

### Navegación y menús
* **Mac OS Dock Magnification** - Navegación en el borde, los iconos escalan de forma fluida al pasar el cursor.
* **Magnetic Button** - Se atrae hacia el cursor.
* **Gooey Menu** - Los subelementos se desprenden como un líquido viscoso.
* **Dynamic Island** - Píldora que se transforma para mostrar estado o alertas.
* **Contextual Radial Menu** - Menú circular que se expande en el punto de clic.
* **Floating Speed Dial** - FAB que se despliega en acciones secundarias curvas.
* **Mega Menu Reveal** - Desplegable a pantalla completa, con contenido que aparece escalonadamente.

### Diseño y cuadrículas
* **Bento Grid** - Agrupación asimétrica de mosaicos (Centro de Control de Apple).
* **Masonry Layout** - Cuadrícula escalonada, sin altura de fila fija.
* **Chroma Grid** - Bordes / mosaicos con degradados animados sutiles.
* **Split-Screen Scroll** - Dos mitades que se deslizan en direcciones opuestas.
* **Sticky-Stack Sections** - Secciones que se fijan y se apilan al hacer scroll.

### Tarjetas y contenedores
* **Parallax Tilt Card** - Inclinación 3D que sigue las coordenadas del ratón.
* **Spotlight Border Card** - Los bordes se iluminan bajo el cursor.
* **Glassmorphism Panel** - Cristal esmerilado con refracción interna.
* **Holographic Foil Card** - Cambio de color iridiscente arcoíris al pasar el cursor.
* **Tinder Swipe Stack** - Pila física de tarjetas, deslizables para descartar.
* **Morphing Modal** - El botón se expande hasta convertirse en su propio diálogo.

### Animaciones de scroll
* **Sticky Scroll Stack** - Las tarjetas se fijan y se apilan físicamente.
* **Horizontal Scroll Hijack** - Desplazamiento vertical → paneo horizontal.
* **Locomotive / Sequence Scroll** - Vídeo / secuencia 3D vinculada a la barra de desplazamiento.
* **Zoom Parallax** - Imagen de fondo central que se amplía al hacer scroll.
* **Scroll Progress Path** - Línea SVG que se dibuja a lo largo del scroll.
* **Liquid Swipe Transition** - Transición de página como un líquido viscoso.

### Galerías y medios
* **Dome Gallery** - Galería panorámica 3D.
* **Coverflow Carousel** - Carrusel 3D con bordes angulados.
* **Drag-to-Pan Grid** - Lienzo arrastrable sin límites.
* **Accordion Image Slider** - Tiras estrechas que se expanden al pasar el cursor.
* **Hover Image Trail** - Rastro de imágenes que aparecen al mover el ratón.
* **Glitch Effect Image** - Desplazamiento de canales RGB al pasar el cursor.

### Tipografía y texto
* **Kinetic Marquee** - Bandas de texto interminables que invierten su sentido al hacer scroll.
* **Text Mask Reveal** - Tipografía masiva como ventana transparente hacia un vídeo.
* **Text Scramble Effect** - Decodificación al estilo Matrix al cargar o al pasar el cursor.
* **Circular Text Path** - Texto que se curva siguiendo un círculo giratorio.
* **Gradient Stroke Animation** - Texto con contorno y un degradado en movimiento.
* **Kinetic Typography Grid** - Letras que esquivan el cursor.

### Microinteracciones y efectos
* **Particle Explosion Button** - El CTA se fragmenta en partículas al completarse con éxito.
* **Liquid Pull-to-Refresh** - Indicador de recarga como gotas que se desprenden.
* **Skeleton Shimmer** - Reflejo de luz que se desplaza sobre los marcadores de posición.
* **Directional Hover-Aware Button** - El relleno entra desde el lado exacto por donde llega el cursor.
* **Ripple Click Effect** - Onda que parte de las coordenadas del clic.
* **Animated SVG Line Drawing** - Vectores que se dibujan solos en tiempo real.
* **Mesh Gradient Background** - Manchas orgánicas tipo lámpara de lava.
* **Lens Blur Depth** - La interfaz de fondo se desenfoca para enfocar la acción en primer plano.

### Elección de biblioteca de animación
* **Motion (`motion/react`)** - predeterminada para animaciones de UI / Bento / cambios de estado.
* **GSAP + ScrollTrigger** - para narrativa de página completa y scroll hijacks. Aislar en componentes hoja dedicados con limpieza `useEffect`.
* **Three.js / WebGL** - para fondos de canvas y escenas 3D. Misma regla de aislamiento.
* **NUNCA mezclar GSAP / Three.js con Motion en el mismo árbol de componentes.** Compiten por los mismos fotogramas.

---

## 11. PROTOCOLO DE REDISEÑO

Esta skill gestiona **construcciones desde cero Y rediseños**. Clasificar mal el modo es la causa más grave de malos resultados en un rediseño.

### 11.A Detectar el modo (primera acción)
* **Desde cero** - no existe un sitio o se ha aprobado una renovación completa. Ajusta la base de referencia de la Sección 1.
* **Rediseño - Preservar** - modernizar sin romper la marca. Auditar primero, extraer los tokens de marca y evolucionar de forma gradual.
* **Rediseño - Renovación total** - nuevo lenguaje visual sobre contenido existente. Tratar como desde cero en lo visual; conservar el contenido y la arquitectura de información.

Si es ambiguo, preguntar **una vez**: *"¿Este rediseño debe conservar la marca existente o empezamos visualmente desde cero?"*

### 11.B Auditar antes de tocar
Documentar el estado actual antes de proponer cambios:
* **Tokens de marca** - colores primario / de acento, pila tipográfica, tratamiento del logotipo, radios.
* **Arquitectura de información** - árbol de páginas, navegación principal, rutas de conversión clave.
* **Bloques de contenido** - qué existe, qué cumple una función y qué es relleno.
* **Patrones a conservar** - interacciones distintivas, un héroe reconocible, tono del texto.
* **Patrones a retirar** - señales de "AI slop", diseños rotos, enlaces muertos, imágenes de stock genéricas, trampas de rendimiento.
* **Lectura de la configuración del sitio existente** - inferir el `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY` actual. Ese es tu punto de partida, no la base de referencia.
* **Línea base de SEO** - páginas con posicionamiento actual, meta títulos, datos estructurados, tarjetas OG. **La migración de SEO es el riesgo n.º 1 de un rediseño.**

### 11.C Reglas de preservación
* **No cambiar la arquitectura de información** salvo que se solicite. Mantener estables los slugs de página, los ID de anclaje y las etiquetas de la navegación principal para el SEO y la memoria del usuario.
* **Extraer los colores de marca antes de aplicar la Sección 4.2.** Una marca que ya es morada sigue siendo morada: aplicar la anulación de LILA RULE.
* **Preservar el tono del texto** salvo que se pida una reescritura. Modernización visual ≠ reescritura de contenido.
* **Respetar los logros de accesibilidad existentes.** No retroceder en estados de foco, texto alternativo, navegación por teclado ni contraste.
* **Respetar los eventos de analítica existentes.** No renombrar botones, campos de formulario ni ID de sección de los que dependa el seguimiento posterior.

### 11.D Palancas de modernización (orden de prioridad)
Aplicar en orden; detenerse cuando el brief esté satisfecho:
1. **Renovación tipográfica**: mayor impacto visual por unidad de riesgo.
2. **Espaciado y ritmo**: aumentar el padding de las secciones y corregir el ritmo vertical.
3. **Recalibración de color**: desaturar, unificar los neutros y mantener el color de acento de la marca.
4. **Capa de movimiento**: añadir micro-interacciones adecuadas a `MOTION_INTENSITY` a los componentes existentes.
5. **Recomposición del hero y de las secciones clave**: reestructurar la parte superior del embudo usando el vocabulario de la Sección 10.
6. **Sustitución completa del bloque**: solo cuando el bloque existente no sea recuperable.

### 11.E Árbol de decisión: evolución dirigida vs. rediseño completo
* Si la IA, el contenido y el SEO son correctos → **evolución dirigida** (palancas 1-4). ~70% del valor con ~40% del riesgo.
* Si la deuda visual es estructural (IA rota, sin sistema de diseño, móvil roto) → **rediseño completo** con preservación estricta del contenido.
* Si la propia marca está cambiando → **desde cero (greenfield)**.

### 11.F Lo que nunca cambia en silencio
No modificar nunca sin aprobación explícita del usuario:
* Estructura de URL / slugs de rutas.
* Etiquetas de la navegación principal.
* Nombres y orden de los campos de formulario (rompe analítica y autocompletado).
* Logotipo o marca denominativa de la marca.
* Texto legal / de consentimiento / de cookies existente.

---

## 12. LA BIBLIOTECA DE BLOQUES (contrato: las implementaciones se incorporan iterativamente)

El vocabulario de referencia (Sección 10) nombra patrones. La biblioteca de bloques los implementa con props reales, especificaciones de movimiento reales y bocetos de código reales.

**Estado:** esquema definido aquí. Los bloques se añadirán iterativamente. No inventar nuevos bloques sin seguir este esquema.

### 12.A Ubicación de archivos
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

### 12.B Frontmatter obligatorio
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

### 12.C Secciones obligatorias del cuerpo
1. **Boceto visual**: ASCII breve o descripción del diseño.
2. **API de props**: la interfaz del componente.
3. **Boceto de código**: implementación mínima funcional (Server Component por defecto, isla Client para el movimiento).
4. **Alternativa móvil**: reglas explícitas de colapso para `< 768px`.
5. **Variantes de movimiento**: una variante por banda de `MOTION_INTENSITY` (1-3, 4-7, 8-10). Alternativa explícita para movimiento reducido.
6. **Notas de modo oscuro**: estrategia de tokens específica de este bloque.
7. **Antipatrones**: formas comunes en que este bloque sale mal.
8. **Referencias**: enlaces a ejemplos reales en producción.

### 12.D Disciplina de la biblioteca de bloques
* Un bloque por archivo. Nada de archivos con varios bloques.
* Cada bloque debe funcionar de forma independiente (se coloca en una página y se renderiza).
* Cada bloque debe superar la comprobación previa (Sección 14).
* Los bloques que dependan de un sistema de diseño de la Sección 2.A se ubican en `blocks/<category>/<name>--<system>.md` (p. ej. `feature/bento-grid--material.md`).

---

## 13. FUERA DE ALCANCE

Esta skill NO es para:
* Paneles de control / interfaces de producto densas / paneles de administración (usar Fluent, Carbon, Atlassian o Polaris de la Sección 2.A).
* Tablas de datos (usar TanStack Table o AG Grid).
* Formularios de varios pasos / asistentes (usar patrones específicos de formularios; esta skill no los mejorará).
* Editores de código (usar Monaco / CodeMirror con su personalización oficial).
* Móvil nativo (usar Apple HIG / Material directamente).
* Interfaces de colaboración en tiempo real (presencia, cursores, OT; es una clase de problema distinta).

Si el brief corresponde a alguno de los casos anteriores, **indicarlo explícitamente**, señalar la herramienta adecuada y aplicar las partes de esta skill de páginas de marketing / acerca de / landing solo a las superficies donde sean pertinentes.

---

## 14. COMPROBACIÓN FINAL PREVIA AL VUELO

Ejecutar esta matriz antes de emitir código. Es el último filtro.

**ESTO NO ES OPCIONAL. Marcar cada casilla. Si alguna falla, la salida no está terminada.**

- [ ] **Inferencia breve** declarada (resumen de una línea de la Sección 0.B)?
- [ ] **Valores de los diales** explícitos y razonados a partir del brief, sin usar silenciosamente la línea base?
- [ ] **Sistema de diseño** elegido de la Sección 2 si aplica, o estética etiquetada con honestidad?
- [ ] **Modo de rediseño** detectado y auditoría realizada (si aplica, Sección 11)?
- [ ] **CERO guiones largos (`—`) en toda la página.** Titulares, antetítulos, etiquetas, cuerpo, citas, atribuciones, pies de foto, botones, texto alternativo. Cero. (Sección 9.G, innegociable.)
- [ ] **Bloqueo de tema de página**: UN tema (claro, oscuro o automático) para toda la página. Ninguna sección cambia a modo invertido a mitad de página (Sección 4.11)?
- [ ] **Bloqueo de consistencia de color**: un color de acento usado de forma idéntica en todas las secciones (Sección 4.2)?
- [ ] **Bloqueo de consistencia de forma**: un sistema de radio de esquina aplicado de forma coherente (Sección 4.4)?
- [ ] **Comprobación de contraste de botones**: el texto de cada CTA es legible sobre su fondo (sin blanco sobre blanco, WCAG AA 4.5:1)?
- [ ] **Ajuste de etiquetas CTA**: ninguna etiqueta de CTA ocupa 2 o más líneas en escritorio?
- [ ] **Comprobación de contraste de formularios**: los campos, marcadores de posición, anillos de foco y etiquetas cumplen WCAG AA sobre el fondo de la sección?
- [ ] **Disciplina de serif**: si se usa una serif, NO es Fraunces ni Instrument_Serif (o lo es, con justificación explícita de marca)? ¿Distinta de la serif de tu proyecto anterior?
- [ ] **Comprobación de paleta premium-consumo**: si el brief es premium-consumo (cocina / bienestar / artesanal / lujo), la paleta NO pertenece a la familia por defecto de IA beige+latón+rojo oscuro+café espresso? ¿Familia distinta a la de tu proyecto premium-consumo anterior?
- [ ] **Margen para descendentes en cursiva**: cada palabra en cursiva con `y g j p q` tiene `leading-[1.1]` como mínimo + `pb-1` de reserva?
- [ ] **El hero cabe en el viewport**: titular ≤ 2 líneas, subtexto ≤ 20 palabras Y ≤ 4 líneas, CTA visible sin desplazarse, escala tipográfica planificada en torno a la imagen?
- [ ] **Relleno superior del hero**: máximo `pt-24` en escritorio; el contenido del hero no flota a mitad del viewport?
- [ ] **Disciplina de pila en el hero**: máximo 4 elementos de texto en el hero (antetítulo O franja de marca, titular, subtexto, CTA)? Sin eslogan diminuto bajo los CTA, sin franja de confianza en el hero?
- [ ] **RECUENTO DE ANTETÍTULOS (mecánico)**: contar las instancias de `uppercase tracking` (etiquetas micro sobre titulares de sección) en todos los componentes. ¿Recuento ≤ ceil(númeroDeSecciones / 3)? El hero cuenta como 1.
- [ ] **Prohibición de encabezado dividido**: ningún patrón de "titular grande a la izquierda + párrafo explicativo pequeño a la derecha" como encabezado de sección (usar pila vertical)?
- [ ] **Límite de alternancia en zigzag**: no hay 3 o más secciones consecutivas con el mismo diseño de imagen+texto dividido?
- [ ] **Sin intención de CTA duplicada**: no hay dos CTA con la misma intención ("Ponte en contacto" + "Hablemos" en la misma página = Fallo)?
- [ ] **Muro de logotipos = solo logotipos**: sin etiquetas de sector o categoría impresas bajo los logotipos?
- [ ] **Diversidad de fondos en bento**: al menos 2-3 celdas bento con variación visual real (imagen, degradado, patrón), no todas tarjetas de texto blanco sobre blanco?
- [ ] **Muro de logotipos "Usado por / Con la confianza de"** BAJO el hero, no dentro de él, con logotipos SVG REALES (Simple Icons / devicon) o marcas SVG generadas, NO nombres de marca en texto plano?
- [ ] **Autoevaluación de copy**: cada cadena visible releída; no se entrega ninguna frase gramaticalmente rota ni alucinada por la IA (tipo "gratis en su pasado")?
- [ ] **Movimiento motivado**: cada animación puede justificarse en una frase (jerarquía / narrativa / retroalimentación / transición de estado), sin GSAP por espectáculo?
- [ ] **Máximo un marquee por página**: no hay dos marquees horizontales en la misma página?
- [ ] **Navegación en UNA línea** en escritorio, altura ≤ 80px?
- [ ] **Comprobación de repetición de diseño de sección**: no hay dos secciones con la misma familia de diseño (al menos 4 familias distintas en 8 secciones)?
- [ ] **El bento tiene ritmo Y número exacto de celdas** (N elementos → N celdas, sin celdas vacías en medio ni al final)?
- [ ] **Las listas largas usan el componente de UI correcto** (no el valor por defecto `<ul>` con `divide-y` para más de 5 elementos; ver alternativas en la Sección 4.9)?
- [ ] **Imágenes reales usadas** (primero herramienta de generación, luego Picsum con semilla, luego espacios de marcador explícitos): SIN capturas de pantalla falsas hechas con div, SIN SVG decorativos hechos a mano, SIN minimalismo de solo texto?
- [ ] **Sin etiquetas ni píldoras superpuestas sobre imágenes** (sin `Plate · Brand`, sin `Field notes - journal`)?
- [ ] **Sin pies de foto de crédito como decoración** (`Field study no. 12 · Ines Caetano`)?
- [ ] **Sin pies de versión** (`v1.4.2`, `Build 0048`) en páginas de marketing?
- [ ] **Sin microfrases meta** bajo los antetítulos ("Cada una de estas es una función que lanzamos hoy...")?
- [ ] **Sin franja decorativa de texto en la base del hero** (`BRAND. MOTION. SPATIAL.`)?
- [ ] **Sin subtexto flotante arriba a la derecha** en los encabezados de sección?
- [ ] **Sin barras de puntuación o progreso con pistas de fondo rellenas** como visuales de comparación?
- [ ] **Sin franjas de ubicación / nombre de ciudad / hora / clima** salvo que el brief sea de distribución global real o centrado en un lugar?
- [ ] **Sin indicadores de desplazamiento** (`Scroll`, `↓ scroll`, `Scroll to explore`)?
- [ ] **Sin etiquetas de versión en el hero** (V0.6, BETA, SOLO POR INVITACIÓN) salvo que el brief sea un lanzamiento?
- [ ] **Sin antetítulos con numeración de sección** (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`)?
- [ ] **Sin puntos decorativos** (cero por defecto, solo para estados semánticos reales)?
- [ ] **Sin `border-t` + `border-b` en cada fila** de listas largas o tablas de especificaciones?
- [ ] **Densidad de contenido sensata**: sin tablas de datos de 20 filas, sin especificaciones falsamente precisas sin justificación, subpárrafos de ≤ 25 palabras por defecto?
- [ ] **Citas ≤ 3 líneas** de cuerpo, atribución limpia (sin guion largo)?
- [ ] **Movimiento declarado = movimiento mostrado**: si se afirma `MOTION_INTENSITY > 4`, la página realmente anima, no solo lo afirma?
- [ ] **Pila fija y desplazamiento horizontal de GSAP** implementados según el esqueleto canónico de las Secciones 5.A / 5.B (`start: "top top"`, `pin: true`, scrub correcto)?
- [ ] **Sin `window.addEventListener('scroll')`**: uso exclusivo de Motion `useScroll()` / ScrollTrigger / IntersectionObserver / animaciones CSS impulsadas por desplazamiento?
- [ ] **Movimiento reducido** envuelto para todo lo que `MOTION_INTENSITY > 3`?
- [ ] **Tokens de modo oscuro** definidos y probados en ambos modos?
- [ ] **Colapso móvil** explícito (`w-full`, `px-4`, `max-w-7xl mx-auto`) para diseños de alta variación?
- [ ] **Estabilidad del viewport**: `min-h-[100dvh]`, nunca `h-screen`?
- [ ] **Las animaciones `useEffect`** tienen funciones de limpieza estrictas?
- [ ] **Estados vacío / carga / error** proporcionados?
- [ ] **Tarjetas omitidas** a favor del espaciado cuando sea posible?
- [ ] **Iconos** solo de una biblioteca permitida (Phosphor / HugeIcons / Radix / Tabler), sin trazados SVG hechos a mano?
- [ ] **Movimiento aislado** en componentes hoja de cliente con `'use client'` al inicio, memoizados?
- [ ] **Sin marcas de IA** de la Sección 9 (Inter por defecto, púrpura de IA, tres tarjetas iguales, Jane Doe, Acme, "Usado discretamente por")?
- [ ] **Core Web Vitals** razonablemente alcanzados (LCP < 2,5 s, INP < 200 ms, CLS < 0,1)?
- [ ] **Un sistema de diseño** por proyecto (sin mezclar Material + shadcn)?

Si una casilla de verificación no puede marcarse con honestidad, la página no está terminada. Corríjala antes de entregar.

---

# APÉNDICES - Material de referencia real y respaldado por fuentes

Las secciones siguientes son contenido de referencia incluido en el proyecto. Proporcionan comandos de instalación reales, enlaces canónicos a la documentación oficial y fragmentos iniciales funcionales para cada sistema de diseño mencionado en la Sección 2. Utilícelos para fundamentar las decisiones en la realidad de producción, no en ficción de datos de entrenamiento.

## Apéndice A - Comandos de instalación por sistema de diseño

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


## Apéndice B - Fuentes canónicas (léalas antes de reinventar)

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

### CSS nativo / estándares W3C
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass (solo plataformas Apple)
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## Apéndice C - Apple Liquid Glass: aproximación web honesta

**No** trate fragmentos CSS aleatorios como Apple Liquid Glass oficial.

### Qué es oficial
Apple documenta Liquid Glass en las Human Interface Guidelines de Apple y en la documentación para desarrolladores de las **plataformas Apple**. Es un material dinámico utilizado en la interfaz de todas las plataformas Apple. La implementación nativa de Apple pertenece a las API de las plataformas Apple y a los componentes del sistema, **no a un paquete CSS público para la web**.

Documentación oficial relevante:
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### Qué NO es oficial
No existe `liquid-glass.css` de Apple para sitios web normales.

Una aproximación web puede utilizar:
- `backdrop-filter`
- fondos transparentes
- bordes en capas
- superposiciones de resaltado
- gradientes
- movimiento
- alternativas de contraste fuerte

Pero eso es **glassmorphism web / aproximación de cristal esmerilado**, no Apple Liquid Glass oficial. Indíquelo así en los comentarios.

### Esqueleto de aproximación web más seguro

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


**Importante:** `prefers-reduced-transparency` tiene soporte desigual en los navegadores; pruébelo. Proporcione siempre suficiente contraste incluso sin desenfoque.

---

**Fin de los apéndices.** Los comandos de instalación anteriores son puntos de referencia de la realidad. El esqueleto de Apple Liquid Glass es una aproximación etiquetada, no un paquete emitido por Apple. Para la documentación canónica de cada sistema de diseño, consulte la documentación oficial del sistema (enlaces en la Sección 2 y en el Apéndice B).
