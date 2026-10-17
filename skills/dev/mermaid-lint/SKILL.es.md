---
name: mermaid-lint
version: 1.0.0
type: tool
author: Lukas Geiger + Claude
created: 2026-09-20
updated: 2026-09-20
aliases: [mermaid, mermaid-fehler, diagramm-render-fehler, unable-to-render-rich-display, schaltplan-fehler]
description: "Encuentra y corrige diagramas de Mermaid que GitHub no renderiza (\"Unable to render rich display\"). Verifica cada bloque ```mermaid con el analizador real de Mermaid, sin navegador, y después confirma el resultado en la página de GitHub en vivo."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [mermaid, markdown, github, readme, diagramm, lint, dokumentation]
language: es
status: active
visibility: public
dependencies: {'tools': ['node', 'git'], 'services': ['GitHub'], 'protocols': [], 'python': [], 'npm': ['mermaid', 'jsdom', 'playwright-core']}
translated_from_sha256: a1286c3571792da726aea23967c12360cb0daadb8d3d0bce2208ff27fc14bce9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T22:17:49.701000+00:00"
---
<img src="banner.png" width="100%" alt="mermaid-lint banner">

# mermaid-lint

Un diagrama de Mermaid con error de sintaxis muestra en GitHub, en lugar de la gráfica, el recuadro
**"Unable to render rich display"**. En local no se nota, porque ninguna herramienta
revisa el bloque. Esta skill cubre ese hueco.

## Cuándo aplicarla

- Un README o documento muestra en GitHub un error de renderizado en lugar de un diagrama.
- Antes de una publicación o de un release con diagramas en la documentación.
- Después de cada reestructuración de Markdown que afecte a bloques de Mermaid.
- En varios repositorios a la vez, cuando no está claro dónde hay algo roto.

## Las dos herramientas

### 1. `mermaid_lint.mjs` — Verificación de sintaxis sin navegador

```
node mermaid_lint.mjs <repo-pfad> [...] [--json]
node mermaid_lint.mjs --from <liste.txt> [--json]
```

Busca de forma recursiva todos los archivos `.md`, extrae cada bloque ```mermaid y lo hace pasar
por `mermaid.parse()` — **el mismo analizador que GitHub usa en el navegador**.
Salida 0 = todos los bloques se analizan sin errores; salida 1 = al menos un bloque defectuoso. La salida indica archivo,
número de bloque, línea y el error literal del analizador.

`--from <datei>` lee una lista de rutas, una por línea. Úsala en lugar de muchos argumentos:
las rutas de Windows con barras invertidas se corrompen en silencio en el shell de Bash
(de `D:\code\my-repo` queda `D:codemy-repo`). Escribe las rutas con barras normales.

Un solo proceso puede con cientos de repositorios, porque Mermaid se carga una sola vez.
Sin Puppeteer y sin descarga de Chromium.

### 2. `readback.mjs` — Prueba en la página en vivo

```
node readback.mjs <github-url> [...]
```

Abre las páginas en el Edge instalado (sin descarga de navegador) y cuenta
los errores de renderizado reales. Veredicto por página: `OK`, `DEFEKT`, `UNKLAR` o `KEIN-MERMAID`.

## Tres trampas que hacen necesaria esta skill

**GitHub renderiza Mermaid en iframes sandboxed** de `viewscreen.githubusercontent.com`.
La página principal no ve su contenido. Quien solo evalúa `document.body.innerText` o
`msedge --dump-dom` informa cero errores en **cada** página, incluso en una que está comprobadamente rota. Por eso `readback.mjs` evalúa todos los frames.

**Un único hallazgo DEFECTUOSO no es fiable.** Durante la carga, GitHub
muestra brevemente un marcador de posición que parece un error de renderizado. Medido el 2026-09-20:
la misma página informó primero `ERR=1` y, después, dos veces `ERR=0`. `readback.mjs` repite
automáticamente los hallazgos negativos; un `OK` nunca se repite.

**`mermaid.parse()` necesita un DOM**; si no, falla en `DOMPurify.addHook` e
informa como rotos diagramas de flujo válidos. `mermaid_lint.mjs` prepara
antes una ventana jsdom. Si aun así queda un error del entorno, se registra por separado bajo `envIssues` y **no** se cuenta como error de sintaxis.

## Comprobar siempre con un control negativo

Antes de creer un resultado en verde, ejecuta la herramienta una vez sobre un estado del que sabes que está roto, por ejemplo el commit anterior a tu corrección:

```
node readback.mjs "https://github.com/<org>/<repo>/blob/<alter-sha>/README.md"
```

Si también informa `OK`, tu readback no mide nada. Así se descubrió la trampa del iframe de arriba.

## Causas frecuentes de error y su corrección mínimamente invasiva

| Síntoma en el error del analizador | Causa | Corrección |
|---|---|---|
| `Expecting '+', '-', '()', 'ACTOR', got 'loop'` | Un participante se llama igual que una palabra reservada: `loop`, `alt`, `opt`, `par`, `end`, `critical`, `break`, `rect`, `note` | Declarar un alias: `participant L as Loop`; los mensajes usan `L`. El **nombre mostrado se conserva**: no lo renombres. |
| `got 'PS'` en un diagrama de flujo | Paréntesis redondos en la etiqueta del nodo | Entrecomillar la etiqueta: `A["Start (hier)"]` |
| `Lexical error ... Unrecognized text` | Backticks o dos puntos en la etiqueta | Entrecomillar la etiqueta y quitar los backticks |
| `Expecting 'SEMI', 'NEWLINE', 'EOF'` en `graph`/`flowchart` | `Note:` solo existe en diagramas de secuencia y de clases | Quitar el texto aclaratorio del bloque y ponerlo como línea de Markdown debajo, para que la información siga visible |
| `Expecting 'SOLID_OPEN_ARROW' ... got 'NEWLINE'` en un diagrama de secuencia | **Entidad HTML** en el texto del mensaje (`&lambda;`, `&Delta;`, `&ge;`). Aquí no hay que romper los paréntesis ni el `=`: el `;` final de la entidad lo lee el lexer como terminador de sentencia, y todo lo que sigue se convierte en una nueva instrucción. | Sustituir la entidad por el carácter literal (λ, Δ, ≥) y dejar el texto sin cambios. Los paréntesis pueden quedarse. No cambies nunca los valores numéricos ni su escritura. |
| Punto y coma en un mensaje de secuencia | Se lee como fin de sentencia | Reemplazar por ` - ` |

En **etiquetas de diagramas de flujo entrecomilladas** las entidades no son problemáticas; la regla solo aplica a los mensajes de secuencia. `mermaid_lint.mjs` informa estas entidades como línea propia de tipo `[WARN]` (campo `warnings` en el JSON), además del error del analizador. El analizador solo indica `got 'NEWLINE'` y no nombra la causa.

**Principio:** mínimamente invasivo. El diseño, los IDs de nodo, el orden y el texto visible
se mantienen sin cambios en la medida de lo posible. En repositorios científicos esto vale
especialmente para los valores numéricos y su escritura. Si hay paridad EN/DE, mantén ambas versiones
con la misma estructura.

## Flujo en varios repositorios

1. Inventario con `gh repo list <org> --limit 200 --json name,isArchived,isPrivate,defaultBranchRef`.
2. Clona y trae el estado remoto, y toma en serio las divergencias. Un lint sobre un clon desactualizado mide el estado equivocado. Si `git pull --ff-only` falla, verifica contra `origin` en lugar del árbol de trabajo:
   `git archive origin/<branch> | tar -x -C <tempdir>` y lintea la carpeta temporal.
3. **Repos homónimos de organizaciones distintas** (típicamente `.github`) no deben mapearse al mismo clon; si no, se revisa nueve veces el mismo repo. Si hay nombres duplicados, clona plano en `<org>__<repo>` y lintea el estado fresco.
4. Antes de cada cambio revisa los locks (`lock_scan.py`, `LOCK*.txt`) en el clon **y** en la ruta del proyecto de OneDrive; coloca tu propio lock y retíralo tras el push.
   **Lee el alcance, no solo la existencia:** `LOCK.team.*` con `expires_after` caducado puede ignorarse; `LOCK.user.zenodo-upload.txt` bloquea exclusivamente la escritura externa en Zenodo y permite expresamente los cambios de documentación.
   En cambio, un `LOCK.user.until-winners-announcement.txt` (Judging) bloquea cualquier push: ahí solo se verifica en modo lectura y el hallazgo se registra como ticket.
5. Repara, lintea hasta que esté en verde, haz commit, `git pull --rebase` y push.
6. Readback con control negativo. Solo entonces se da por cerrado.

## Instalación

```
npm install mermaid jsdom playwright-core
```

En la carpeta de los scripts o de forma global; `playwright-core` usa el Edge instalado
(`channel: 'msedge'`) y no descarga un navegador propio. Solo hace falta para el readback:
la verificación de sintaxis funciona sin él.

## Relacionado

- `_tools/lint_mermaid.py` en GithubBot: linter más antiguo, basado en regex, con `--fix`.
  Corrige patrones conocidos automáticamente, **pero no conoce palabras reservadas**
  y no reemplaza esta skill. Orden sensato: primero `mermaid_lint.mjs` para el diagnóstico, luego, si procede, `lint_mermaid.py --fix` para los patrones masivos, y después volver a lintear.
- `github-repo-care`: protocolo general para el mantenimiento y la publicación de repositorios.
