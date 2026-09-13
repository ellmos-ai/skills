---
name: surface-after-care
version: 1.6.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-30
aliases: [repo-after-care, repo-pflege, after-care, repo-nachpflege, repo-wartung]
description: >
  Ronda de mantenimiento regular para un repositorio publicado de GitHub (Nivel 1,
  económica y repetible con frecuencia): primero identificar todas las superficies de distribución del proyecto
  (npm, PyPI, registros, marketplaces, tiendas, sitio web) y reflejar los cambios allí más adelante,
  luego establecer temas (topics), ejecutar la puerta de privacidad, verificar documentos por intención de publicación e
  ignorar retroactivamente archivos de planificación internos, agregar banners, cotejar afirmaciones en el README con el código real,
  mejorar la presentación, completar versiones de idioma del README, implementar medidas de visibilidad, verificar la entrada
  en la página de la organización y procesar issues y pull requests abiertos.
  Usa esta habilidad cuando debas mantener, limpiar, actualizar, pulir o "revisar de nuevo" un repo existente,
  cuando un repo parezca desactualizado o desordenado, con frases como "mantenimiento de repo", "after care",
  "poner repo al día", "limpiar y pushear" o en rondas de calidad rotativas entre varios repositorios.
  Para la ronda profunda que incluye chequeo legal y referencias cruzadas entre organizaciones, usa en su lugar full-after-care;
  para la publicación inicial, usa github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, privacy, i18n, documentation, visibility, issues]
language: es
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="surface-after-care banner">
# Surface After Care — La ronda de mantenimiento regular para un repositorio publicado

## Cuándo usar esta habilidad

Úsala para un repositorio que **ya es público** y debe revisarse periódicamente. Es el nivel económico: todo lo que se puede decidir en el propio repositorio sin inventariar repositorios de terceros ni iniciar un dictamen legal.

Diferenciación con habilidades vecinas:

| Situación | Habilidad |
|---|---|
| El repo se publica por primera vez | `github-repo-care` |
| El repo es público, ronda de mantenimiento regular | **esta habilidad** |
| Adicionalmente chequeo legal + referencias cruzadas en todas las orgs + i18n de app | `full-after-care` (Alias `deep-after-care`) |
| Auditoría pura de derecho/privacidad/licencia antes de hacer público | `repo-publish-check` |
| Mantener versiones de idioma de documentos sincronizadas en contenido | `bilingual-doc-sync` |
| Distribución de esta ronda en muchos repositorios, rotando equitativamente | `rotation-check` |

## Idea central

Un repositorio publicado se desvía en dos direcciones: **la documentación describe un software más antiguo que el que reside en el repo**, y **se acumulan archivos que nunca estuvieron destinados a ojos externos**. Ninguno de los dos suele ser dramático, pero ambos cuestan exactamente los usuarios que se desea ganar: uno abandona porque las instrucciones de instalación ya no coinciden, el otro porque encuentra `AUFGABEN.txt` y `Plan.txt` en el directorio raíz y se lleva la impresión de que alguien trabaja aquí solo para sí mismo.

Esta ronda limpia ambos problemas. Está diseñada deliberadamente para ser repetible: es mejor media hora cuatro veces al año que una gran limpieza anual.

## Flujo de trabajo

El orden no es arbitrario. El Paso 0 está al principio porque determina el alcance de todos los pasos siguientes. El Paso 2 se ejecuta antes de cualquier cosa que envíe cambios (push); de lo contrario, se suben mejoras sobre un estado que aún necesita limpiarse. El Paso 1 es puramente en el servidor y no interfiere.

### 0. Inventariar superficies de distribución

**Antes de modificar cualquier cosa: aclarar dónde está presente este proyecto.** El repositorio de GitHub rara vez es la única superficie. Un README corregido sirve de poco si la página del paquete en npm sigue mostrando la versión antigua con instrucciones de instalación erróneas — y es precisamente allí donde llega la mayoría de los usuarios, ya que los registros de paquetes suelen posicionarse mejor en motores de búsqueda que el propio repositorio.

```bash
# Los manifiestos revelan los canales
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Consultar el estado publicado de los canales (solo lo que aplique)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Superficies típicas: npm, PyPI, Crates, Docker Hub, registro MCP, directorios de plugins/skills, marketplaces de VS Code o navegadores, tiendas de aplicaciones, Zenodo/DOI, sitio web del proyecto, perfil de organización, `llms.txt`, repositorios espejo en otros hosts.

Anota la lista encontrada en el registro de ejecución. A partir de ahora es el **conjunto objetivo**: cada cambio de los pasos siguientes se reflejará al final contra esta lista (ver "Paridad en todas las superficies"). Si encuentras una superficie que ya nadie mantiene y apunta a código abandonado, es un hallazgo por sí mismo: actualízala o retírala deliberadamente, pero no la dejes abandonada.

### 1. Establecer temas (Topics)

Los temas son la superficie de búsqueda más importante dentro de GitHub y casi no cuestan nada.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

El objetivo son aproximadamente entre 5 y 12 temas desde tres ángulos: **qué es** (`cli`, `mcp-server`, `python-library`), **de qué trata** (`file-management`, `tax`, `note-taking`) y **cómo funciona** (`local-first`, `offline`, `privacy`). Oriéntate por temas que realmente se utilicen en proyectos comparables; los temas inventados no atraen usuarios. Verifica también la descripción y la página de inicio (homepage) al mismo tiempo; aparecen en la misma vista.

Los temas tienen un homólogo en las otras superficies del Paso 0: `keywords` en `package.json`, `keywords`/`classifiers` in `pyproject.toml`, categorías y etiquetas en marketplaces y tiendas. Mantén el contenido idéntico: representan la misma decisión en múltiples lugares.

### 2a. Puerta de Privacidad (Privacy-Gate) — se ejecuta siempre

Este paso nunca se omite, ni siquiera en una ronda aparentemente inofensiva. Se busca en el conjunto **rastreado (tracked)**, no en el árbol de trabajo visible, porque esa es precisamente la diferencia entre "parece limpio" y "está limpio".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Complementa el patrón con los **nombres de tus propios directorios internos** — carpetas de pipeline, directorios temáticos, áreas de trabajo privadas:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

Tales referencias no son secretos y no activan escáneres de seguridad, por lo que se pasan por alto; pero son **irresolubles** para lectores externos ("transferido de la pipeline .SOFTWARE" no dice nada a extraños) y revelan tu estructura interna. Reemplázalas o elimínalas, no las toleres. Una búsqueda que solo rastrea `C:\Users\…` y patrones de tokens garantizadamente no las encontrará.

¿Encontraste algo? La **naturaleza** del hallazgo determina el procedimiento — consulta la sección "Regla de Force-Push". Un secreto que se ha subido en un commit una vez está comprometido: eliminarlo de `HEAD` no basta, debe rotarse.

### 2b. Verificar la intención de publicación de documentos

El verdadero núcleo de esta ronda. Revisa los archivos `.md`, `.txt` y `.json` rastreados y pregunta en cada uno: **¿Estuvo esto destinado alguna vez a ojos externos?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

No adivines por el nombre de archivo: echa un vistazo rápido dentro. Un `PLAN.md` puede ser una hoja de ruta pública, un inofensivo `notes.md` la estrategia interna de precios. Tres categorías:

**Pertenece al repositorio** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, referencias de API, configuraciones de ejemplo, hojas de ruta reales, manifiestos (`package.json`, `pyproject.toml`), archivos de bloqueo (lockfiles), configuración de CI.

**No pertenece al repositorio, pero es no crítico** — el caso habitual de esta ronda. Archivos de tareas y planificación (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), notas de sesión y traspasos (`HANDOFF`, `BRIEFING`, `_handoff/`), archivos de estado de la propia pipeline, diarios de desarrollo, `_archive/`, JSONs de registro e índice con rutas locales, estados intermedios y artefactos generados, archivos de trabajo de agentes. Estos archivos no son peligrosos, pero crean desorden y la impresión de una obra sin recoger. Solución: actualizar `.gitignore`, `git rm --cached <archivo>` y **hacer push normalmente**.

**No pertenece al repositorio y es delicado** — Credenciales, datos personales, datos de clientes, cálculos internos, estrategias de precios/negociación, planes de negocio no publicados, borradores de contratos, cualquier cosa con valor competitivo. Aquí un commit normal no es suficiente; consulta la Regla de Force-Push.

En los archivos `.json` vale la pena mirar dos veces: los manifiestos y lockfiles permanecen, pero las configuraciones locales, archivos de tareas/registros, dumper de exportación y cualquier cosa con rutas absolutas o nombres de host son polizones típicos.

Si eliminas un archivo que alguien podría buscar (una hoja de ruta, por ejemplo), menciona brevemente en el commit o en el README dónde vive ahora esa información; de lo contrario, parecerá un retroceso.

### 3. Banner

Un banner decide a menudo si alguien empieza a leer. Verifica si existe uno y si está incluido como primer elemento en el README.

Si falta, hay tres caminos (en este orden de preferencia):

1. **Generador de imágenes de un agente** (p. ej., agy; la palabra "generar" es allí el disparador para la creación real de PNG) si un motivo visual encaja mejor que la tipografía.
2. **Codex**, si el banner debe crearse a partir de código y existe una referencia estética en la que basarse.
3. **Creado por ti mismo como SVG**, si el banner es principalmente una marca denominativa más lenguaje de formas: suele ser la opción más rápida y controlable, y el SVG sigue siendo editable más adelante.

Mantén la familia de diseño si el proyecto pertenece a un grupo: mismo color base, misma estética, mismo tratamiento de marca. Un banner que desencaja luce peor que no tener ninguno. Tamaño estándar 1200x300; guarda el PNG en el repositorio y el código fuente SVG al lado.

### 4. Cotejar afirmaciones contra el código real

Aquí se genera la mayor parte del valor. El README afirma cosas — verifícalas en lugar de darles crédito a ciegas:

- **Versión** en README/Badge contra `pyproject.toml`/`package.json`/`__version__` y contra la última etiqueta de lanzamiento (release tag). Si hay múltiples portadores de versión, verifícalos todos.
- **Ruta de instalación** ejecutarla (al menos leyendo): ¿Existe el paquete con el nombre indicado? ¿Coinciden los comandos y flags?
- **Lista de características** contra el código: ¿Está presente todo lo mencionado y falta algo nuevo en la lista?
- **Cifras** (número de herramientas, formatos soportados, cobertura de pruebas) volver a contar en la fuente en lugar de arrastrarlas. Las cifras en el README envejecen silenciosamente.
- **Capturas de pantalla** contra la interfaz actual.
- **Requisitos** (versión de Python/Node, dependencias) contra los manifiestos.
- **Enlaces** a proyectos vecinos, documentación y registros: ¿siguen funcionando?

**Una corrección aplica a todas las superficies, no solo a la que llamó la atención.** Si una afirmación resulta ser falsa —especialmente si la aclara el propietario—, es muy probable que esa misma afirmación figure en otra parte: en el perfil de la organización, en `llms.txt`, en la segunda versión de idioma, en el README de un proyecto vecino. Busca específicamente antes de marcar el punto como completado:

```bash
gh search code "<frase concisa>" --owner ORG
```

De lo contrario corregirás un punto y dejarás tres en pie — y la contradicción solo saldrá a la luz cuando le toque el turno al siguiente repositorio. Eso no solo hace perder tiempo, destruye la confianza en la documentación: quien encuentra dos descripciones distintas de lo mismo no cree en ninguna.

A continuación, mejora la **presentación** donde sea débil: las listas largas de opciones se leen mejor como tabla; los bloques de código necesitan etiquetas de idioma; una visión general de estructura o flujo se capta más rápido como diagrama Mermaid o árbol ASCII que en prosa; la primera altura de pantalla debe mostrar propósito, instalación y un ejemplo de uso, no insignias e historia previa. Si el README supera las ~400 líneas, delega los detalles a `docs/` y enlaza.

**Regla de idioma para READMEs:** El estándar es un **`README.md` en inglés** más una **segunda versión en alemán**. Excepción: el dominio de la aplicación es alemán en sí mismo (derecho alemán, sistema tributario/de subvenciones alemán, audiencia objetivo de habla alemana) o hasta ahora existe exclusivamente una versión en alemán — entonces el alemán sigue siendo el idioma principal. Para cada idioma adicional que el proyecto ya hable en código, corresponde una versión de README equivalente. Respeta la convención de nombres establecida en el repo (`README_de.md`, `README.de.md`, `docs/README.de.md`) y no inventes una segunda. Enlaza las versiones mutuamente en el encabezado.

### 6. Añadir idiomas estándar faltantes

Completa los READMEs que falten de los **idiomas estándar**: alemán, inglés, español, chino simplificado, japonés, ruso. El propósito es el alcance, por lo que esto aplica principalmente a proyectos orientados a usuarios finales — para una biblioteca orientada a desarrolladores con audiencia exclusivamente en inglés, un README en ruso no es una ganancia, sino una carga de mantenimiento. Decide conscientemente y registra la decisión en el historial de ejecución para que la próxima ronda no la discuta de nuevo.

Las nuevas versiones se **rellenan, no se crean vacías** — un borrador con "TODO: translate" es peor que la ausencia del archivo porque finge completitud. La paridad de contenido y la re-alineación las gestiona `bilingual-doc-sync`; con más de dos versiones, conviene invocar esa habilidad.

### 7. Visibilidad y Promoción

Considera qué medidas aportan realmente usuarios para **este** proyecto e impleméntalas:

- **Registros** a los que el proyecto pertenece técnicamente: Registros de paquetes (npm, PyPI), registro MCP, directorios de plugins/skills, marketplaces.
- **Listas curadas** (`awesome-*` y colecciones temáticas), siempre que los criterios de admisión se cumplan genuinamente. Un PR a una lista cuyos criterios el proyecto no cumple cuesta reputación.
- **Superficies propias**: Perfil de la organización, `llms.txt`, sitio web del proyecto, README del ecosistema, enlaces desde repositorios propios relacionados.
- **Notas de lanzamiento** como oportunidad: Un lanzamiento sin una narrativa detrás de las nuevas funciones pasa desapercibido.

**Puerta de Aprobación:** Todo lo que vaya hacia afuera —PRs a repositorios externos, entradas en listas externas, publicaciones, envíos— se **propone y ejecuta solo tras una aprobación explícita**, a menos que exista una autorización permanente para ese canal. Los cambios en superficies propias no requieren esta puerta. La razón es simple: un PR retirado en un repositorio ajeno es visible públicamente y repercute negativamente en el proyecto.

### 8. Entrada en páginas de la organización

Primero la organización propia: ¿Figura el repositorio en el README del perfil (`ORG/.github` → `profile/README.md`) en absoluto, en la sección correcta, con una descripción actualizada?

```bash
gh api user/orgs --jq '.[].login'
```

Luego recorre **todas** las organizaciones y responde a una sola pregunta por organización: ¿Se beneficiaría un visitante de esta página de organización de este repositorio? La mayoría de las veces la respuesta es no — entonces "no enlazar" es el resultado correcto y no un vacío. Donde la respuesta sea sí (proximidad temática, usuarios compartidos, una herramienta que complemente los proyectos de allí), establece la referencia con una línea que explique el beneficio, no solo citando el nombre.

El perfil vive en su propio repositorio (`ORG/.github`). Los cambios allí se mantienen y se envían (push) en paralelo — siguiendo la Regla del Árbol Sucio del Paso 11.

### 10. Issues y Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Procrésalos en lugar de solo contarlos:

- **Bugs corregibles** reparar directamente — el contexto ya está cargado durante esta ronda. Correcciones pequeñas y bien definidas con pruebas y referencia al número de issue.
- **Issues ya resueltos** cerrar con una frase explicando qué los resolvió.
- **Reportes poco claros** solicitar aclaración orientada (versión, sistema operativo, pasos de reproducción).
- **PRs**: Leer el diff minuciosamente, ejecutar pruebas, luego fusionar (merge) o responder de forma fundamentada. Un PR desatendido durante meses cuesta más buena voluntad que un rechazo educado.
- **Casos estancados (Stale)** resolver en lugar de arrastrarlos.

**Puerta de Aprobación:** Los comentarios públicos, cierres con justificación y fusiones de contribuciones externas son comunicación hacia el exterior — presentar antes de la ejecución a menos que exista autorización permanente. Las correcciones puras de código en el propio repo están exentas.

### 11. Hacer commit, push y verificar

La ronda no termina con las ediciones, sino cuando estas están **publicadas fuera**. Un árbol de trabajo lleno de mejoras sin enviar es el peor resultado: la siguiente sesión —posiblemente otro agente u otro dispositivo— debe orientarse primero en un estado ajeno e incompleto, y en las superficies públicas nada ha mejorado.

Antes de hacer push, asegura brevemente lo que sea verificable: ejecuta pruebas y comprobaciones de humo, verifica enlaces y vista renderizada en cambios de documentación. Luego agrupa en **commits temáticamente separados** en lugar de volcarlo todo en uno solo — la limpieza, las actualizaciones de documentación y las correcciones de errores son tres cosas distintas, y quien necesite revertir una más tarde lo agradecerá:

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: eliminar archivos de trabajo internos del rastreo"
git commit -am "docs: actualizar README (versión, número de herramientas, capturas)"
git commit -am "fix: <número de issue> ..."

git pull --rebase        # si la rama ha divergido, antes de hacer push
git push
```

Luego verifica en lugar de asumir: README remoto en la vista renderizada, ejecución de CI, estado de lanzamientos y etiquetas.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**Si la CI se pone roja aunque tu commit solo tocó documentación**, la causa casi nunca es tu cambio. Con diferencia, el caso más frecuente —encontrado **tres veces** en un solo día en esta familia de repositorios— es un **linter sin fijar y sin selección de reglas definida**. Verifica esto **primero** antes de sospechar de tu commit.

El mecanismo: Si el flujo de trabajo ejecuta `ruff check` (o flake8, eslint …) contra una dependencia sin fijar (`ruff>=0.12`, o sin versión en absoluto), y carece de selección explícita de reglas (`[tool.ruff.lint] select = [...]`, o un `ruff.toml` si falta `pyproject.toml`), entonces el linter sigue el valor por defecto de la versión **recién instalada**. Un nuevo lanzamiento del linter cambia este valor por defecto y hace que un código sin cambios se ponga rojo. Señales delatadoras:

- Códigos de reglas que el proyecto nunca tuvo (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999` …), a veces en números de tres dígitos.
- El fallo suele dividirse **entre plataformas**: los ejecutores con versiones antiguas en caché permanecen en verde, los nuevos se ponen en rojo.
- A veces una regla señala algo incorregible (`N999` en el propio nombre del paquete) — señal segura de que nunca fue estándar.

Solución: Fijar la selección de reglas que antes estaba en verde — `select = ["E4","E7","E9","F"]` son los valores por defecto clásicos de ruff. Si `pyproject.toml` no existe, crea un `ruff.toml`. Verifica contra la **nueva** versión del linter (instalar, reproducir hallazgos sin configuración, ver "passed" con configuración). Las nuevas reglas se convierten en una **tarea** para el proyecto: adoptarlas conscientemente es una decisión, no un efecto secundario de actualizar una herramienta. Este es un hallazgo real y recurrente: Sin la fijación de versión, la CI volverá a fallar en el siguiente lanzamiento del linter en **cada** repositorio configurado de manera similar.

Dos casos en los que **no** se hace push: si se aplica una congelación de publicación o envío al proyecto, o si el estado está explícitamente incompleto. Ambos son excepciones que se justifican — el caso estándar es: hacer commit y push.

Bajo una congelación de publicación, la ronda no se aborta, sino que se **redirige**: hacer commit localmente en una rama dedicada (`judging-hold/…`, `freeze/…`), dejar la rama principal intacta en el estado enviado, anotar el motivo del bloqueo en el registro de ejecución y ponerse al día tras el desbloqueo. La coherencia es vital: bloqueado no es solo `git push`, sino **cualquier cambio visible remotamente** — los temas, la descripción, la página de inicio, los lanzamientos y las acciones de issues/PR modifican el proyecto publicado del mismo modo.

Si existen otros clones del mismo repositorio (segundo dispositivo, copia de despliegue, espejo), actualízalos inmediatamente tras el push. Un clon diez commits por detrás produce errores de diagnóstico contra un estado que ya no existe en la siguiente sesión de depuración.

#### Cambios en otros repositorios — Excepción de Árbol Sucio (Dirty-Tree)

Esta ronda produce regularmente cambios **fuera** del repositorio mantenido: una línea en el perfil de la organización (Paso 8), más adelante en la ronda profunda un enlace recíproco en un repositorio relacionado. Tales cambios también se commitean y se pushean: un enlace recíproco sin publicar no es un enlace.

Antes de tocar un repositorio ajeno, verifica brevemente su estado:

```bash
git -C <ruta> status --porcelain
```

**Árbol de trabajo limpio** → hacer la edición, commitear en un **commit independiente y temáticamente claro** (`docs: link <proyecto>`) y hacer push. No mezclar con los commits del repositorio mantenido: es un repositorio diferente con su propia historia y lectores.

**Dirty, pero los cambios ajenos están en otros archivos** → tu edición aún se puede hacer de forma limpia. Prepara (stage) y haz commit **de forma específica por ruta solo de tu archivo**, para que el trabajo ajeno no verificado no se incluya:

```bash
git -C <ruta> add README.md
git -C <ruta> commit -m "docs: link <proyecto>"     # solo la ruta preparada
```

Pero **no hagas push**. El commit es localmente inofensivo; un push podría no serlo: no sabes a qué apunta el otro estado de trabajo (tal vez se esté modificando, reestructurando o cortando de otra forma), y tu push obligaría a otros a resolver el conflicto. El commit local asegura el trabajo sin imponerlo; la ejecución que más tarde se ocupe de ese repositorio lo encontrará y lo llevará consigo.

**Dirty en el archivo exacto que debes editar** → no tocar. Aquí tendrías que basarte en un estado intermedio ajeno y commitearlo a la vez; entenderlo primero cuesta más de lo que vale este único enlace.

**Bloqueo activo (`LOCK*.txt`) en el repositorio destino** → **leer primero el bloqueo en lugar de tratarlo como una prohibición total.** Un bloqueo describe su propio alcance, que a menudo es más estrecho que "nada en absoluto". Casos típicos:

- **Bloqueo de edición** ("alguien está trabajando activamente aquí") → no tocar nada, ni siquiera archivos secundarios.
- **Bloqueo puro de publicación/push** (envío, evaluación, congelación) → el trabajo local sigue estando permitido, solo el contacto remoto está bloqueado. Trabajar en una rama dedicada y hacer commit localmente; **los pasos visibles remotamente se omiten** — no solo el push, sino también temas, descripción, página de inicio, lanzamientos y acciones de issues/PR.

Leer un bloqueo que solo impide el push como una prohibición total desperdicia toda la parte local de la ronda sin ganar seguridad. A la inversa, omitir solo el push mientras se alteran los metadatos es insuficiente. En caso de duda, cita el bloqueo y pregunta.

#### La solicitud no debe perderse

Si una edición **no** se ejecuta debido a una de estas razones, regístrala en la lista de tareas del repositorio destino — `AUFGABEN.txt`, `TODO.md` o `TODO.txt`, según lo que exista allí. Una entrada con fecha, edición deseada y motivo:

```markdown
- [ ] [2026-07-24, after-care] Añadir enlace recíproco a <proyecto> en el README
      (omitido: el README tenía cambios de terceros no commiteados)
```

Esa es la diferencia entre "pospuesto" y "olvidado": la lista de tareas reside donde el siguiente mantenedor de ese repositorio mirará de todos modos, siendo más confiable que una nota en el registro de una ejecución ajena. Si no existe lista de tareas, no crees una; el punto pendiente en tu propio registro es suficiente.

Bajo un **bloqueo activo, ni siquiera esto aplica**: el archivo se deja sin tocar y la nota permanece únicamente en tu propio registro de ejecución. Anótala allí en ambos casos para que la rotación conozca los puntos pendientes.

Por último, atiende las superficies del Paso 0; consulta la siguiente sección.

## Paridad en todas las superficies de distribución

Al final de la ronda, verifica contra la lista del Paso 0: **Cada cambio que un usuario vería debe llegar a cada superficie donde lo busque.** Un repositorio cuya página en npm cuenta una historia diferente a GitHub está peor que uno con una sola superficie.

El mecanismo decisivo: **Los registros de paquetes muestran el README del último lanzamiento (publish), no el estado actual del repositorio.** Una corrección del README en npm o PyPI solo se hace visible con una nueva versión. Si la corrección es relevante en cuanto a contenido (instalación incorrecta, versión errónea, lista de funciones obsoleta), corresponde incluir un lanzamiento de parche (patch release); de lo contrario, la corrección no tendrá efecto.

| Superficie | Qué se mantiene allí | Cómo llega |
|---|---|---|
| npm | README, `description`, `keywords`, enlace al repositorio | Solo mediante `npm publish` (versión de parche); los metadatos provienen de `package.json` |
| PyPI | README (`long_description`), clasificadores, URLs del proyecto | Solo mediante nueva subida; metadatos de `pyproject.toml` |
| Registro MCP / Directorios de plugins | Descripción, versión, lista de herramientas, doc de inicio | Depende del registro: actualización de manifiesto o reenvío |
| Marketplace / Tienda | Descripción, capturas de pantalla, categorías, versiones de idioma | A través de la interfaz de gestión respectiva; las capturas envejecen especialmente rápido allí |
| Docker Hub / Registro de contenedores | Descripción, etiquetas, ejemplo de uso | Descripción del repositorio más nueva etiqueta |
| Zenodo / DOI | Metadatos, autores, versión | Edición directa para metadatos, nueva versión para contenidos |
| Sitio web / Perfil de Org / `llms.txt` | Descripción corta, enlace, posicionamiento | Directamente editable — las superficies más económicas, nunca las olvides |

Cuando se incrementa una versión, **todos los portadores de versión** deben avanzar simultáneamente: manifiesto, constante de código, insignia en README, changelog, etiqueta de lanzamiento, `llms.txt`. Un estado de versión a medio incrementar es más difícil de diagnosticar que uno consistentemente antiguo.

Si una actualización en una superficie no es posible o práctica en ese momento (p. ej., un lanzamiento solo por una errata), regístralo en el historial de ejecución para que la siguiente ronda no confunda la desviación con un descuido.

## Regla de Force-Push

El estándar es **no hacer force-push**. Ignorar retroactivamente archivos de planificación internos no justifica reescribir la historia: el esfuerzo es alto, cada clon y fork se rompe, los PRs abiertos se vuelven inservibles y la ganancia es menor porque el contenido no es crítico. Forma estándar:

```bash
git rm --cached <archivo>            # eliminar del rastreo, mantener localmente
# actualizar .gitignore
git commit -m "chore: eliminar archivos de trabajo internos del rastreo"
git push
```

Reescribir la historia (y por tanto hacer push con `--force-with-lease`) solo está justificado en **filtraciones reales (leaks)**: credenciales y claves, datos personales o de clientes, y documentos con valor competitivo real (cálculos internos, estrategias de precios, planes no publicados, detalles de contratos). En ese caso:

1. **Rotar primero los secretos afectados**: la historia ya ha sido copiada, forkeada y almacenada en caché para ese momento. La rotación funciona; la eliminación es solo cosmética.
2. Limpiar la historia (`git filter-repo` o BFG), hacer push con `--force-with-lease`.
3. Verificar forks y cachés; contactar con el soporte de GitHub para objetos huérfanos si es necesario.
4. Registrar el procedimiento en el historial de ejecución: qué, cuándo y qué rotación.

En caso de duda entre "no crítico" y "delicado": tratar como delicado y presentar para revisión. Los costos son asimétricos.

## Los hallazgos se convierten en tareas, no solo en líneas de registro

Una ronda de mantenimiento encuentra regularmente más de lo que puede o debe resolver en la misma ejecución: una versión de idioma faltante, un retraso de modernización, una publicación que nunca ocurrió. **Tales hallazgos se convierten en tareas en el momento de su descubrimiento**; de lo contrario, permanecen enterrados en el registro de una ejecución completada donde el siguiente mantenedor del proyecto no mirará.

La tarea pertenece al **sistema de tareas local de la carpeta del proyecto** —donde la persona que trabaje a continuación en este proyecto consulte. Típicamente es `AUFGABEN.txt` o `TODO.md` en la carpeta del proyecto, que a menudo **no está dentro del clon de Git**, sino en el directorio donde vive la planificación del proyecto. El clon contiene código; la carpeta del proyecto contiene la gestión; una entrada en el clon que desaparece en el siguiente `git clean` no es una tarea.

Ten en cuenta tres cosas:

1. **Separar la lista de tareas interna de la hoja de ruta pública.** Un `TODO.md` puede ser una hoja de ruta pública mantenida —entonces no es un vertedero de trabajo interno. Mira dentro antes de añadir: si aparece un encabezado como "Public roadmap", escribe en el archivo interno de al lado (`AUFGABEN.txt`) y márcalo como interno.
2. **Verificar entradas existentes antes de duplicar.** A menudo el hallazgo ya está anotado. Entonces no se crea una entrada nueva, sino que se **enriquece** con evidencia empírica de esta ejecución ("confirmado: `--help` muestra salidas en español"). Un punto conocido con evidencia fresca es más valioso que una segunda entrada duplicada.
3. **Registrar lo resuelto.** Lo que la ronda solucionó pertenece como punto tachado con su hash de commit. Eso explica a la siguiente ronda por qué desapareció un hallazgo y evita que se vuelva a "descubrir".

Formula las tareas de modo que tengan sentido sin el contexto de esta ejecución: qué se encontró, por qué importa, cuál sería el siguiente paso. "i18n incompleto" no es una tarea; "El catálogo contiene solo `status.title`, allí es/zh/ja/ru están vacíos — primero transferir cadenas CLI al catálogo, luego rellenar los seis idiomas" sí lo es.

## Registro de ejecución

Registra los resultados en `_after-care/LOG.md` (la carpeta pertenece al `.gitignore`: es material de pipeline, no contenido del repo, según el Paso 2b). Una línea por ejecución con fecha, nivel y decisiones conscientes:

```markdown
## 2026-07-24 — surface
- Superficies: GitHub, npm (<paket>), registro MCP, Perfil Org, llms.txt
- Temas: +local-first, +mcp-server; keywords en package.json alineadas
- Eliminado: AUFGABEN.txt, _handoff/ (en gitignore, no requiere force push)
- README: Versión 0.9 -> 1.2 corregida, recuento de herramientas 23 -> 26 actualizado
- Idiomas: EN + DE mantenidos; ES/ZH/JA/RU omitidos conscientemente (audiencia técnica)
- Issues: #12 corregido, #7 cerrado (resuelto), #15 consulta enviada
- Push: 3 commits, CI verde; nuevo publish en npm 1.2.1 por corrección en README
- Pendiente: Capturas de pantalla de la tienda obsoletas, requieren nueva compilación
```

El registro evita que la siguiente ronda tome las mismas decisiones de nuevo y constituye la base para rondas de mantenimiento rotativas en múltiples repositorios (`rotation-check`).

## Errores frecuentes

| Error | Corrección |
|---|---|
| Mirar solo el árbol de trabajo, no `git ls-files` | Verificar siempre el conjunto rastreado: ahí se esconden los problemas |
| La puerta de privacidad solo buscó rutas y tokens | Buscar también nombres de directorios/pipelines propios: no activan alertas y se pasan por alto |
| Archivo interno eliminado reescribiendo la historia | Para archivos no críticos, `git rm --cached` + push normal es suficiente |
| Secreto eliminado de `HEAD` y considerado resuelto | Rotar el secreto; todo lo demás es cosmética |
| Clasificar archivos estrictamente por el nombre | Mirar brevemente dentro: los nombres no transmiten la intención de forma confiable |
| Reutilizar cifras en el README sin volver a contar | Contar en la fuente (lista de herramientas, ejecución de pruebas, manifiesto) |
| Crear nueva versión de idioma como borrador vacío | Rellenar u omitir: un borrador finge completitud |
| Introducir una segunda convención de nombres para README | Adoptar la convención existente en el repositorio |
| Enviar PR a una lista externa sin aprobación | Presentar comunicación externa primero; solo las superficies propias son libres |
| Contar issues en lugar de procesarlos | Corregir, cerrar o solicitar información: cada caso obtiene un estado |
| Crear banner por cuenta propia en un estilo ajeno | Mantener la familia de diseño del ecosistema |
| README en el repo corregido, la página de npm/PyPI sigue mostrando lo antiguo | Las páginas de registros provienen del último lanzamiento: realizar un patch release |
| Incrementar versión solo en el manifiesto | Todos los portadores de versión a la vez: manifiesto, código, insignia, changelog, etiqueta, `llms.txt` |
| Cambios listos, pero dejados sin hacer push | Hacer commit y push pertenece a la ronda; solo los bloqueos justifican una excepción |
| Todo en un solo commit global | Separar limpieza, documentación y correcciones: de lo contrario nada se puede revertir individualmente |
| CI roja tras commit de documentación, sospechar de uno mismo | Linter sin fijar sin `select` sigue el valor por defecto de la nueva versión: fijar reglas |
| Corregir afirmación falsa solo donde llamó la atención | Buscar en toda la organización la frase: suele figurar en el perfil org, `llms.txt` y 2da versión de idioma |
| Trabajar en repo ajeno sucio con `commit -a` | Preparar (stage) por rutas específicas y hacer commit, no hacer push: el trabajo ajeno queda intacto |
| Edición en repo de perfil org limpio, pero sin hacer push | Los repositorios ajenos limpios reciben un commit independiente **y** un push independiente |
| Edición omitida anotada solo en el registro propio | Registrar además en la lista de tareas del repo destino, si existe una |
| Hallazgo escrito solo en el registro de ejecución | Se convierte en tarea en el sistema local de la carpeta: nadie mira el registro más tarde |
| Trabajos internos colgados de una hoja de ruta pública | Verificar dentro primero; "Public roadmap" significa: usar archivo interno al lado |
| Hallazgo conocido duplicado como nueva entrada | Enriquecer el punto existente con evidencia empírica de esta ejecución |
| Bajo bloqueo de edición escribir línea TODO en el repo bloqueado | El bloqueo aplica a todo el proyecto: no tocar nada allí |
| Leer bloqueo de push como prohibición total y omitir todo el repo | Leer el bloqueo: si solo impide publicar, ejecutar la ronda local en una rama dedicada |
| Bajo bloqueo de push no hacer push, pero editar temas o descripción | Los metadatos son visibles remotamente: bajo congelación de publicación también se omiten |

## Lista de verificación final

- [ ] Superficies de distribución identificadas y anotadas en el registro de ejecución.
- [ ] Temas, descripción y página de inicio configurados y verificados.
- [ ] Puerta de privacidad ejecutada sobre el conjunto rastreado, hallazgos gestionados.
- [ ] `.md`/`.txt`/`.json` verificados por intención de publicación, archivos internos ignorados.
- [ ] Sin force-push sin una filtración real; rotación realizada en caso de filtración.
- [ ] Banner presente e incluido en el README.
- [ ] Versión, características, cifras, capturas de pantalla, enlaces verificados contra el estado real.
- [ ] Presentación mejorada (tablas, diagramas, primera altura de pantalla).
- [ ] Matriz de idiomas del README completa; decisiones sobre otros idiomas documentadas.
- [ ] Medidas de visibilidad implementadas o presentadas para aprobación.
- [ ] Entrada en el perfil de la propia org verificada, enlaces a orgs externas con sentido establecidos.
- [ ] Ediciones en repositorios ajenos: limpio → commiteado y pusheado; dirty → commiteado localmente;
      no ejecutado → registrado en la lista de tareas del repositorio destino.
- [ ] Issues y PRs llevados a un estado definido.
- [ ] Commits separados creados, pusheados, CI y vista remota verificadas.
- [ ] Todas las superficies de distribución llevadas al mismo estado (patch release si es necesario).
- [ ] Hallazgos no resueltos registrados como tareas en el sistema de tareas local de la carpeta.
- [ ] Registro de ejecución escrito en `_after-care/LOG.md`.

## Registro de cambios

### 1.6.0 (2026-07-24)
- Regla añadida: Una corrección de contenido aplica a todas las superficies. Aprendido empíricamente: una aclaración de usuario se corrigió en la ejecución 1 en el hub, pero figuraba sin notar cinco veces más en el perfil de la organización (EN, DE, `llms.txt`) y solo se notó nueve ejecuciones después.

### 1.5.0 (2026-07-24)
- Diagnóstico de linter precisado tras ocurrir el patrón tres veces en un solo día (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16): "verificar primero", códigos de regla culpables concretos, división por plataforma, `ruff.toml` como solución ante falta de `pyproject.toml`, verificación contra la nueva versión del linter.

### 1.4.0 (2026-07-24)
- Diagnóstico añadido: Si la CI se pone roja tras un commit de pura documentación, la causa más frecuente es un linter sin fijar sin conjunto de reglas definido —un nuevo lanzamiento de la herramienta cambia el valor por defecto y pone el código sin cambios en rojo. Solución: fijar conjunto de reglas, nuevas reglas como tarea. Ocurrió dos veces seguidas (n8n-workflow-manager con ruff 0.15, clirec con 0.16).

### 1.3.0 (2026-07-24)
- Nueva sección "Los hallazgos se convierten en tareas": Lo que la ronda no puede solucionar por sí misma se convierte en una entrada en el sistema de tareas local de la carpeta del proyecto en el momento del descubrimiento —donde mirará el siguiente mantenedor, no en el registro de una ejecución completada. Incluye separación de lista interna y hoja de ruta pública, enriquecer en lugar de duplicar, elementos completados con commit.

### 1.2.0 (2026-07-24)
- La puerta de privacidad busca adicionalmente los nombres de las carpetas internas propias. No son secretos, por lo que no activan alarmas y superan puertas que solo buscan rutas y tokens, pero permanecen irresolubles para lectores y revelan la estructura interna.

### 1.1.0 (2026-07-24)
- Los bloqueos se leen en lugar de tratarse como prohibiciones totales: un bloqueo puro de publicación/push redirige la ronda a una rama local en lugar de abortarla. Al mismo tiempo se aclara que bajo tal bloqueo los metadatos, lanzamientos y acciones de issues/PR se omiten también: son tan visibles remotamente como un push.

### 1.0.0 (2026-07-24)
- Versión inicial. Nivel 1 del mantenimiento posterior de repositorios, derivado de `github-repo-care`.
