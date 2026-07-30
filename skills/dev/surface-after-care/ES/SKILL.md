---
language: es
---

> **Español** — Versión oficial en español de `surface-after-care`.

# Surface After Care — La ronda periódica de mantenimiento para un repo publicado

## Cuándo se aplica este skill

Utilízalo para un repositorio que **ya es público** y que debe revisarse periódicamente. Es el nivel ligero: todo lo que se puede decidir dentro del propio repositorio, sin inventariar repositorios de terceros ni iniciar auditorías legales.

Diferenciación con los skills vecinos:

| Situación | Skill |
|---|---|
| El repo se publica por primera vez | `github-repo-care` |
| El repo es público, ronda periódica de mantenimiento | **este skill** |
| Verificación legal adicional + referencias cruzadas en todas las orgs + i18n de la app | `full-after-care` (alias `deep-after-care`) |
| Verificación puramente legal/privacidad/licencia antes de hacer público | `repo-publish-check` |
| Mantener sincronizadas las versiones lingüísticas en contenido | `bilingual-doc-sync` |
| Distribución de esta ronda entre muchos repos, en rotación justa | `rotation-check` |

## Idea central

Un repo publicado se desvía en dos direcciones: **La documentación describe un software más antiguo que el presente en el repo**, y **se acumulan archivos que nunca estuvieron destinados a ojos ajenos**. Ninguno suele ser dramático, pero ambos cuestan exactamente los usuarios que se desea ganar: uno abandona porque las instrucciones de instalación ya no encajan, y el otro porque se topa en el directorio raíz con `AUFGABEN.txt` y `Plan.txt` y tiene la impresión de que alguien trabaja solo para sí mismo.

Esta ronda limpia ambos aspectos. Es deliberadamente repetible: es mejor media hora cuatro veces al año que una gran limpieza una sola vez.

## Desarrollo

El orden no es arbitrario. El Paso 0 está al principio porque determina el alcance de todos los pasos siguientes. El Paso 2 se ejecuta antes de cualquier push de cambios; de lo contrario, se suben mejoras sobre un estado que aún necesita limpieza. El Paso 1 es puramente del lado del servidor y no interfiere.

### 0. Inventariar superficies de distribución

**Antes de cambiar nada: aclarar dónde se encuentra este proyecto.** El repo de GitHub rara vez es la única superficie. Una README corregida sirve de poco si la página del paquete npm sigue mostrando la versión antigua con instrucciones de instalación incorrectas; y es exactamente ahí donde llega la mayoría de los usuarios, ya que los registros de paquetes a menudo posicionan mejor en motores de búsqueda que el repo.

```bash
# Manifeste verraten die Kanäle (Deutsch)
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Veröffentlichten Stand der Kanäle abfragen (nur was zutrifft) (Deutsch)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Superficies típicas: npm, PyPI, Crates, Docker Hub, MCP-Registry, directorios de plugins/skills, marketplaces de VS Code o navegadores, tiendas de aplicaciones, Zenodo/DOI, sitio web del proyecto, perfil de la organización, `llms.txt`, repos espejo en otros hosts.

Anota la lista encontrada en el registro de ejecución. A partir de ahora es el **conjunto objetivo**: Cada cambio de los siguientes pasos se reflejará al final contra esta lista (ver "Paridad en todas las superficies"). Si encuentras una superficie que ya nadie mantiene y apunta a un estado obsoleto, es un hallazgo propio: actualízala o retírala deliberadamente, pero no la dejes abandonada.

### 1. Establecer topics

Los topics son la superficie de búsqueda más importante en GitHub y no cuestan casi nada.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

El objetivo son entre 5 y 12 topics desde tres perspectivas: **qué es** (`cli`, `mcp-server`, `python-library`), **de qué trata** (`file-management`, `tax`, `note-taking`) y **cómo funciona** (`local-first`, `offline`, `privacy`). Oriéntate en topics utilizados realmente en proyectos comparables; los topics inventados no atraen usuarios. Revisa la descripción y la página web al mismo tiempo, ya que están en la misma vista.

Los topics tienen su equivalente en las otras superficies del Paso 0: `keywords` en `package.json`, `keywords`/`classifiers` en `pyproject.toml`, categorías y etiquetas en marketplaces y tiendas. Mantenlos idénticos en contenido: son la misma decisión, solo que en varios lugares.

### 2a. Filtro de privacidad (Privacy Gate) — se ejecuta siempre

Este paso nunca se omite, ni siquiera en una ronda aparentemente inofensiva. Se busca en el conjunto **rastreado (tracked)**, no en el árbol de trabajo visible, porque esa es precisamente la diferencia entre "parece limpio" y "está limpio".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Añade al patrón los **nombres de tus propias ubicaciones internas**: carpetas de pipeline, directorios temáticos, áreas de trabajo privadas:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

Tales referencias no son secretos y no activan alarmas, por lo que pasan desapercibidas; sin embargo, para los lectores son **irresolubles** ("retransferido desde la pipeline .SOFTWARE" no dice nada a extraños) y revelan tu propia estructura. Se reemplazan o eliminan, no solo se toleran. Una búsqueda que solo rastrea `C:\Users\...` y patrones de tokens garantizadamente no las encontrará.

¿Encontraste algo? Entonces el **tipo** de hallazgo determina el procedimiento (consulta la sección "Regla del Force-Push"). Un secreto que haya sido commiteado alguna vez está comprometido: eliminarlo de `HEAD` no basta; debe rotarse.

### 2b. Comprobar la intención de publicación de los documentos

El núcleo principal de esta ronda. Revisa los archivos `.md`, `.txt` y `.json` rastreados y pregúntate en cada uno: **¿Estuvo esto pensado alguna vez para personas ajenas?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

No adivines por el nombre del archivo: echa un vistazo rápido dentro. Un `PLAN.md` puede ser una hoja de ruta pública, mientras que un inofensivo `notes.md` puede contener la estrategia de precios interna. Tres categorías:

**Pertenece al repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, referencias de API, configuraciones de ejemplo, hojas de ruta reales, manifiestos (`package.json`, `pyproject.toml`), archivos lock, configuración de CI.

**No pertenece al repo, pero no es crítico** — el caso normal de esta ronda. Archivos de tareas y planificación (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), notas de sesión y traspasos (`HANDOFF`, `BRIEFING`, `_handoff/`), archivos de estado de la propia pipeline, diarios de desarrollo, `_archive/`, JSONs de registro e índice con rutas locales, estados intermedios y artefactos generados, archivos de trabajo de agentes. Dichos archivos no son peligrosos, pero crean desorden y la impresión de una obra abandonada. Tratamiento: añadir a `.gitignore`, `git rm --cached <archivo>` y **hacer push normalmente**.

**No pertenece al repo y es confidencial** — credenciales, datos personales, datos de clientes, cálculos internos, estrategias de precios y negociación, planes de negocio no publicados, borradores de contratos, todo lo que tenga valor competitivo. Aquí un commit normal no es suficiente; consulta la Regla del Force-Push.

En los archivos `.json` vale la pena mirar dos veces: los manifiestos y lockfiles se quedan, pero las configuraciones locales, archivos de tareas/registro, dumps de exportación y cualquier cosa con rutas absolutas o nombres de host son polisones típicos.

Si eliminas un archivo que alguien podría buscar (como una hoja de ruta), menciona brevemente en el commit o en el README dónde vive ahora esa información; de lo contrario parecerá un retroceso.

### 3. Banner

Un banner influye en si alguien comienza a leer. Comprueba si existe uno y si está incluido como primer elemento en el README.

Si falta, hay tres opciones en este orden lógico:

1. **Generador de imágenes de un agente** (por ejemplo agy; la palabra "generar" es allí el activador para la creación de un PNG real), si un motivo visual encaja mejor que la tipografía.
2. **Codex**, si el banner debe crearse a partir de código y existe un modelo de estilo en el que orientarse.
3. **Creado por ti mismo como SVG**, si el banner es principalmente una marca denominativa más lenguaje visual: suele ser la variante más rápida y controlable, y el SVG sigue siendo editable más adelante.

Mantén la coherencia familiar si el proyecto pertenece a un grupo: mismo color base, misma estética, mismo tratamiento de marca denominativa. Un banner fuera de sintonía se ve peor que ninguno. Tamaño habitual 1200x300; guarda como PNG en el repo y el SVG como fuente al lado.

### 4. Contrastar afirmaciones con el estado real

Aquí es donde se genera el mayor valor. El README afirma cosas: verifícalas en lugar de dar por sentado que son ciertas:

- **Versión** en el README/Badge frente a `pyproject.toml`/`package.json`/`__version__` y frente a la última etiqueta de release. Si hay múltiples portadores de versión, verifícalos todos, no solo uno.
- **Ruta de instalación**: pruébala realmente, al menos en lectura: ¿Existe el paquete con el nombre mencionado? ¿Son correctos los comandos y opciones (flags)?
- **Lista de características** frente al código: ¿Está todo lo mencionado y falta algo nuevo en la lista?
- **Cifras** (número de herramientas, formatos compatibles, cobertura de pruebas) contadas en la fuente en lugar de arrastradas. Las cifras en los README quedan obsoletas en silencio.
- **Capturas de pantalla** frente a la interfaz actual.
- **Requisitos** (versión de Python/Node, dependencias) frente a los manifiestos.
- **Enlaces** a proyectos vecinos, documentación y registros: ¿siguen funcionando?

**Una corrección se aplica a todas las superficies, no solo a aquella donde se detectó.** Si una afirmación de contenido resulta ser falsa —especialmente si el cliente la corrige—, esa misma afirmación probablemente se encuentre en otros lugares: en el perfil de la organización, en `llms.txt`, en la segunda versión de idioma, en el README de un proyecto vecino. Busca específicamente antes de marcar el punto:

```bash
gh search code "<prägnante Formulierung>" --owner ORG
```

De lo contrario, corriges un sitio y dejas tres intactos, y la contradicción solo se notará cuando le toque el turno al siguiente repo. Esto no solo cuesta tiempo, sino que daña la confianza en la documentación: quien encuentra dos descripciones contradictorias de lo mismo no cree en ninguna.

A continuación, mejora la **presentación** donde sea débil: las listas largas de opciones resultan más legibles en formato tabla; los bloques de código necesitan etiquetas de lenguaje; un esquema de estructura o flujo se capta más rápido como diagrama Mermaid o árbol ASCII que en prosa; la primera altura de pantalla debe mostrar el propósito, la instalación y un ejemplo de uso, no badges ni historia previa. Si el README supera unas 400 líneas, traslada los detalles a `docs/` y enlázalos.

**Regla de idioma para READMEs:** El estándar es un **`README.md` en inglés** más una **segunda versión en alemán**. Excepción: El ámbito del proyecto es intrínsecamente alemán (derecho alemán, sistema fiscal o de subvenciones alemán, público objetivo germanohablante) o existe hasta ahora exclusivamente una versión en alemán: en ese caso, el alemán sigue siendo el idioma principal. Para cada idioma adicional que el proyecto ya hable, debe incluirse una versión propia de README. Mantén la convención de nombres utilizada en el repo (`README_de.md`, `README.de.md`, `docs/README.de.md`) y no inventes una segunda paralela. Enlaza las versiones entre sí en la cabecera.

### 6. Crear idiomas estándar faltantes

Añade los READMEs que falten de los **idiomas estándar**: alemán, inglés, español, chino simplificado, japonés, ruso. El propósito es el alcance, por lo que se aplica principalmente a proyectos orientados al usuario; para una librería orientada a desarrolladores con un público puramente angloparlante, un README en ruso no aporta nada y solo añade carga de mantenimiento. Decide conscientemente y registra la decisión en el log de ejecución para que la siguiente ronda no vuelva a discutirla.

Las nuevas versiones se **rellenan, no se crean y se dejan vacías**: un borrador con "TODO: translate" es peor que la ausencia del archivo porque finge exhaustividad. La sincronización de contenido la gestiona `bilingual-doc-sync`; con más de dos versiones vale la pena usar dicho skill para la comparación.

### 7. Visibilidad y difusión

Considera qué medidas aportan realmente usuarios a **este** proyecto y ejecútalas:

- **Registros** a los que pertenece técnicamente el proyecto: registros de paquetes (npm, PyPI), MCP-Registry, directorios de plugins/skills, marketplaces.
- **Listas curadas** (`awesome-*` y colecciones temáticas), siempre que se cumplan realmente los criterios de admisión. Un PR a una lista cuyos criterios el proyecto no cumple cuesta reputación.
- **Superficies propias**: Perfil de la organización, `llms.txt`, sitio web del proyecto, README del ecosistema, referencias desde repos propios relacionados.
- **Notas de lanzamiento (Release Notes)** como oportunidad: Un release sin novedades explicadas no se percibe.

**Filtro de aprobación (Approval Gate):** Todo lo que salga al exterior (PRs a repos ajenos, entradas en listas ajenas, publicaciones, envíos) se **propone y se ejecuta solo tras aprobación explícita**, a menos que exista una autorización permanente para dicho canal. Los cambios en superficies propias no requieren este filtro. La razón es simple: Un PR retirado en un repo ajeno es públicamente visible y perjudica la reputación del proyecto.

### 8. Entrada en las páginas de la organización

Primero, tu propia organización: ¿Está el repo incluido en el README de perfil (`ORG/.github` → `profile/README.md`), en la categoría correcta y con la descripción actualizada?

```bash
gh api user/orgs --jq '.[].login'
```

Luego recorre **todas** las organizaciones y responde una sola pregunta por organización: ¿Se beneficiaría un visitante de esta página de organización con este repo? Normalmente la respuesta es no; en ese caso "no enlazar" es el resultado correcto y no una laguna. Donde la respuesta sea sí (afinidad temática, usuarios compartidos, una herramienta que complementa los proyectos de allí), coloca la referencia con una frase que explique la utilidad, no solo el nombre.

El perfil reside en su propio repo (`ORG/.github`). Los cambios allí se mantienen y se suben siguiendo la regla de árbol sucio (Dirty Tree) del Paso 11.

### 10. Issues y Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Trabaja en ellos en lugar de limitarte a contarlos:

- **Bugs corregibles**: solucionarlos directamente; en esta ronda el contexto ya está cargado. Correcciones pequeñas y bien delimitadas con pruebas y referencia al número de issue.
- **Issues ya resueltos**: cerrarlos con una frase explicando qué los solucionó.
- **Reportes no claros**: requieren una pregunta de seguimiento precisa (versión, sistema operativo, pasos para reproducir).
- **PRs**: leer realmente el diff, ejecutar pruebas, y luego fusionar (merge) o responder de forma fundamentada. Un PR desatendido durante meses cuesta más buena voluntad que un rechazo educado.
- **Casos obsoletos (Stale)**: resolverlos en lugar de arrastrarlos.

**Filtro de aprobación:** Los comentarios públicos, cierres con justificación y merges de contribuciones ajenas son comunicación exterior; preséntalos antes de ejecutar a menos que exista autorización permanente. Las correcciones puras de código en tu propio repo no se ven afectadas.

### 11. Commitear, hacer push y verificar

La ronda no termina con los cambios, sino cuando están **publicados fuera**. Un árbol de trabajo lleno de mejoras sin hacer push es el peor resultado: La siguiente sesión —posiblemente otro agente u otra máquina— debe orientarse primero en un estado ajeno a medio terminar, y en las superficies públicas nada ha mejorado.

Antes del push, verifica brevemente lo que sea comprobable: ejecuta pruebas y comprobaciones de humo (smoke tests), verifica los enlaces y la vista renderizada en cambios de documentación. Luego agrupa en **commits temáticos separados** en lugar de juntar todo en un único commit masivo: la limpieza, la actualización de documentación y la corrección de errores son tres cosas distintas, y si alguien quiere revertir una de ellas más tarde lo agradecerá:

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git commit -am "docs: README auf aktuellen Stand (Version, Toolzahl, Screenshots)"
git commit -am "fix: <Issue-Nummer> ..."

git pull --rebase        # bei divergiertem Branch, vor dem Push
git push
```

Después verifica en lugar de asumir: README remoto en la vista renderizada, ejecución de CI, estado de releases y etiquetas.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**Si la CI se pone roja aunque tu commit solo tocó documentación**, la causa casi nunca es tuya. El caso más común con diferencia —encontrado **tres veces** en un solo día en esta familia de repos— es un **linter no fijado (unpinned) sin un conjunto de reglas explícito**. Comprueba esto **primero** antes de sospechar de tu commit.

El mecanismo: Si el workflow ejecuta `ruff check` (o flake8, eslint...) contra una dependencia no fijada (`ruff>=0.12`, o sin versión), y falta una selección explícita de reglas (`[tool.ruff.lint] select = [...]`, o un archivo `ruff.toml` propio si falta `pyproject.toml`), el linter sigue el valor por defecto de la versión **recién instalada**. Un nuevo lanzamiento del linter modifica este valor por defecto y un código que no ha cambiado se vuelve rojo. Las señales delatoras:

- Códigos de regla que el proyecto nunca tuvo (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999`...), a veces en cantidades de tres dígitos.
- El fallo suele ser **dividido por plataformas**: los ejecutores con versiones anteriores en caché se mantienen verdes, los nuevos se vuelven rojos.
- A veces una regla señala algo insubsanable (`N999` señalando el propio nombre del paquete), signo seguro de que nunca fue estándar.

Solución: fijar el conjunto de reglas que antes daba verde — `select = ["E4","E7","E9","F"]` son los valores por defecto clásicos de ruff. Si no existe `pyproject.toml`, crea un `ruff.toml`. Verifica contra la **nueva** versión del linter (instalar, reproducir hallazgos sin configuración, asegurar "passed" con configuración). Las nuevas reglas entran al proyecto como **tareas**: adoptarlas conscientemente es una decisión, no un efecto secundario de actualizar una herramienta. Este es un hallazgo real y recurrente: sin fijar la versión, la CI volverá a fallar en el siguiente lanzamiento del linter en **cada** repo configurado así.

Dos casos en los que **no** se hace push: cuando se aplica una restricción de publicación o entrega en el proyecto, o cuando el estado está explícitamente sin terminar. Ambos son excepciones que se justifican; el caso normal es: commitear y hacer push.

Ante una restricción de publicación, la ronda no se cancela sino que se **redirige**: commitear localmente en una rama propia (`judging-hold/...`, `freeze/...`), dejar la rama principal intacta en el estado entregado, anotar la razón del bloqueo en el log de ejecución y ponerse al día tras el desbloqueo. Lo importante es ser consecuente: lo bloqueado no es solo `git push`, sino **cualquier cambio visible remotamente**: topics, descripción, página web, releases y acciones en issues/PR cambian el proyecto publicado por igual.

Si existen otros clones del mismo repo (segundo dispositivo, copia de despliegue, espejo), actualízalos inmediatamente después del push. Un clon con diez commits de retraso producirá diagnósticos sobre un estado que ya no existe durante la siguiente búsqueda de errores.

#### Cambios en otros repositorios — Excepción de árbol sucio (Dirty Tree)

Esta ronda genera regularmente cambios **fuera** del repo mantenido: una línea en el perfil de la organización (Paso 8), o más adelante en la ronda profunda una referencia cruzada en un repo relacionado. Dichos cambios también se commitean y se hace push: una referencia cruzada no publicada no existe.

Antes de tocar un repo ajeno, comprueba brevemente su estado:

```bash
git -C <pfad> status --porcelain
```

**Árbol de trabajo limpio** → realizar el cambio, commitear en un **commit propio y temáticamente claro** (`docs: link <projekt>`) y hacer push. No mezclar con los commits del repo mantenido: es otro repo con su propia historia y lectores.

**Sucio (Dirty), pero los cambios ajenos están en otros archivos** → tu propio cambio se puede hacer de forma limpia. Prepara (stage) y commitea **únicamente tu archivo por ruta**, para que el trabajo ajeno sin verificar no se incluya:

```bash
git -C <pfad> add README.md
git -C <pfad> commit -m "docs: link <projekt>"     # nur der gestagte Pfad
```

Pero **no hagas push**. El commit local es inofensivo; un push no necesariamente lo sería: no sabes a dónde se dirige el otro trabajo; tal vez se esté modificando, reestructurando o cambiando, y tu push le obligaría a lidiar con ello. El commit local asegura tu trabajo sin imponer nada a nadie; el proceso que más tarde se ocupe de ese repo lo encontrará y lo incluirá.

**Sucio en el archivo exacto que necesitas cambiar** → no tocar. Aquí tendrías que basarte en un estado intermedio ajeno y commitearlo conjuntamente; entenderlo primero cuesta más de lo que vale esta única referencia.

**Bloqueo activo (`LOCK*.txt`) en el repo destino** → **leer el bloqueo primero en lugar de tratarlo como una prohibición total.** Un bloqueo describe su propio alcance, que a menudo es más estrecho que "nada en absoluto". Casos típicos:

- **Bloqueo de edición** ("alguien está trabajando aquí ahora") → no tocar nada, ni siquiera archivos secundarios.
- **Bloqueo puro de publicación/push** (entrega, juzgado, freeze) → el trabajo local sigue estando permitido, solo el contacto remoto está bloqueado. Trabajar en una rama propia y commitear localmente; **se omiten los pasos visibles remotamente**: no solo el push, sino también topics, descripción, página web, releases y acciones en issues/PRs, ya que también alteran el proyecto publicado.

Leer un bloqueo que solo prohíbe el push como una prohibición completa hace perder toda la parte local de la ronda sin ganar seguridad. Por el contrario, omitir el push pero modificar metadatos no es suficiente. En caso de duda, cita el bloqueo y consulta.

#### La solicitud no debe perderse

Si el cambio **no** se ejecuta por alguna de estas razones, pasa a la lista de tareas del repo destino (`AUFGABEN.txt`, `TODO.md` o `TODO.txt`, según lo que exista allí). Una entrada con fecha, cambio deseado y motivo:

```markdown
- [ ] [2026-07-24, after-care] Rückverweis auf <projekt> im README ergänzen
      (übersprungen: README hatte uncommittete Fremdänderungen)
```

Esa es la diferencia entre "pospuesto" y "olvidado": La lista de tareas está donde mirará el próximo encargado de este repo, mucho más confiable que una nota en el log de un proceso ajeno. Si no existe lista de tareas, no crees una; la tarea pendiente en tu propio log de ejecución es suficiente.

Con un **bloqueo activo esto tampoco se aplica**: el archivo no se toca y la nota permanece en tu propio log de ejecución. Anótala en ambos casos allí también para que la rotación conozca el punto pendiente.

Por último, atiende las superficies del Paso 0 (ver la sección siguiente).

## Paridad en todas las superficies de distribución

Al finalizar la ronda, contrasta con la lista del Paso 0: **Cada cambio que vería un usuario debe llegar a cada superficie en la que lo busque.** Un repo cuya página de npm cuenta una historia diferente está en peor situación que uno con una sola superficie.

El mecanismo decisivo: **Los registros de paquetes muestran el README del último publish, no el estado actual del repo.** Una corrección del README en npm o PyPI solo se hace visible con una nueva versión. Si la corrección es relevante en cuanto a contenido (instalación incorrecta, versión errónea, lista de funciones obsoleta), se requiere un lanzamiento de parche (patch release); de lo contrario, la corrección no tendrá efecto.

| Superficie | Qué se mantiene allí | Cómo llega |
|---|---|---|
| npm | README, `description`, `keywords`, enlace al repositorio | Solo mediante `npm publish` (versión patch); los metadatos provienen de `package.json` |
| PyPI | README (`long_description`), clasificadores, URLs del proyecto | Solo mediante nueva subida; metadatos de `pyproject.toml` |
| MCP-Registry / Directorios de plugins | Descripción, versión, lista de herramientas, docu de inicio | Según el registro, actualización de manifiesto o nuevo envío |
| Marketplace / Store | Descripción, capturas de pantalla, categorías, versiones de idioma | A través de la interfaz de administración correspondiente; las capturas envejecen rápido allí |
| Docker Hub / Container-Registry | Descripción, etiquetas, ejemplo de uso | Descripción del repositorio más nueva etiqueta |
| Zenodo / DOI | Metadatos, autores, versión | Edición directa para metadatos, nueva versión para contenidos |
| Sitio web / Perfil org / `llms.txt` | Descripción corta, enlace, posicionamiento | Directamente editable: las superficies más baratas, por lo que nunca deben olvidarse |

Cuando se incrementa una versión, **todos los portadores de versión** deben actualizarse simultáneamente: manifiesto, constante en código, badge de README, changelog, etiqueta de release, `llms.txt`. Un estado de versión actualizado a medias es más difícil de diagnosticar que uno antiguo en todas partes.

Si una actualización en una superficie no es posible o conveniente en ese momento (por ejemplo, un release solo por una errata), regístralo en el log de ejecución para que la siguiente ronda no considere la discrepancia como un descuido.

## Regla del Force-Push

El estándar es **no hacer force-push**. Ignorar archivos de planificación interna a posteriori no justifica reescribir la historia: El esfuerzo es alto, cada clon y fork se rompe, los PRs abiertos quedan inservibles y el beneficio es bajo porque el contenido es inofensivo. Procedimiento normal:

```bash
git rm --cached <datei>            # aus dem Tracking, bleibt lokal erhalten
# .gitignore ergänzen (Deutsch)
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git push
```

Reescribir la historia (y por tanto hacer push con `--force-with-lease`) solo está justificado en caso de **filtraciones reales (leaks)**: credenciales y claves, datos personales o de clientes, así como documentos con valor competitivo real (cálculos internos, estrategias de precios, planes no publicados, detalles de contratos). En este caso:

1. **Rotar primero** los secretos afectados: la historia en ese momento ya ha sido copiada, bifurcada y guardada en caché. La rotación funciona; el borrado es meramente cosmético.
2. Limpiar la historia (`git filter-repo` o BFG), hacer push con `--force-with-lease`.
3. Revisar forks y cachés; si es necesario, contactar con el soporte de GitHub para objetos huérfanos.
4. Registrar el proceso en el log de ejecución: qué, cuándo y qué rotación.

En caso de duda entre "no crítico" y "sensible": tratar como sensible y presentar para revisión. Los costes son asimétricos.

## Los hallazgos se convierten en tareas, no solo en líneas de registro

Una ronda de mantenimiento encuentra regularmente más de lo que puede o debe solucionar en la misma ronda: una versión de idioma faltante, un retraso de modernización, una publicación que nunca se realizó. **Tales hallazgos se convierten en tareas en el momento de su descubrimiento**; de lo contrario, se quedan en el registro de un proceso cerrado donde el siguiente encargado del proyecto no mirará.

La tarea pertenece al **sistema de tareas local de la carpeta del proyecto**: donde mirará quien trabaje a continuación en este proyecto. Típicamente es `AUFGABEN.txt` o `TODO.md` en la carpeta del proyecto, y esta a menudo **no está en el clon de Git**, sino en el directorio de planificación. El clon contiene el código, la carpeta del proyecto la gestión; una entrada en el clon que desaparece en el siguiente `git clean` no es una tarea.

Ten en cuenta tres aspectos:

1. **Separar la lista de tareas interna de la hoja de ruta pública.** Un `TODO.md` puede ser una hoja de ruta pública mantenida; en ese caso no es lugar para tareas internas. Mira dentro antes de añadir: Si hay un encabezado como "Public roadmap", escribe en el archivo interno de al lado (`AUFGABEN.txt`) y márcalo como interno.
2. **Comprobar las entradas existentes en lugar de duplicar.** A menudo el hallazgo ya está anotado. En ese caso no se crea de nuevo, sino que se **enriquece** con la evidencia empírica de esta ronda ("confirmado: `--help` muestra mensajes completamente en alemán"). Un punto conocido con pruebas frescas es más valioso que una segunda entrada al lado.
3. **Anotar lo resuelto.** Lo que la ronda ha solucionado debe incluirse como punto marcado con el hash del commit. Esto explica a la siguiente ronda por qué desapareció un hallazgo y evita que vuelva a "descubrirlo".

Formula la tarea de modo que sea comprensible sin el contexto de esta ronda: qué se encontró, por qué importa, cuál sería el siguiente paso. "i18n incompleto" no es una tarea; "El catálogo solo contiene `status.title`, es/zh/ja/ru están vacíos: primero transferir las cadenas de CLI al catálogo, luego rellenar los seis idiomas" sí lo es.

## Registro de ejecución (Log)

Registra el resultado en `_after-care/LOG.md` (la carpeta pertenece a `.gitignore`: es material de pipeline, no contenido del repo, según el Paso 2b). Una línea por ronda con fecha, nivel y decisiones conscientes:

```markdown
## 2026-07-24 — surface
- Flächen: GitHub, npm (<paket>), MCP-Registry, Org-Profil, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json angeglichen
- Entfernt: AUFGABEN.txt, _handoff/ (gitignored, kein Force-Push nötig)
- README: Version 0.9 -> 1.2 korrigiert, Toolzahl 23 -> 26 nachgezählt
- Sprachen: EN + DE gepflegt; ES/ZH/JA/RU bewusst nicht (entwicklernahes Publikum)
- Issues: #12 gefixt, #7 geschlossen (erledigt), #15 Rückfrage gestellt
- Push: 3 Commits, CI grün; npm-Republish 1.2.1 wegen README-Korrektur
- Offen: Store-Screenshots veraltet, brauchen neuen Build
```

El registro evita que la siguiente ronda tenga que tomar las mismas decisiones de nuevo y es la base para las rondas de mantenimiento rotativas en múltiples repos (`rotation-check`).

## Errores frecuentes

| Error | Corrección |
|---|---|
| Solo se examinó el árbol de trabajo, no `git ls-files` | Comprobar siempre el conjunto rastreado: ahí está el problema |
| Filtro de privacidad dirigido solo a rutas y tokens | Buscar también nombres de carpetas/pipeline internas: no activan alarmas y pasan desapercibidas |
| Se eliminó archivo interno reescribiendo la historia | Para archivos no críticos basta con `git rm --cached` + push normal |
| Se eliminó secreto de `HEAD` y se consideró resuelto | Rotar el secreto; todo lo demás es cosmética |
| Se clasificaron archivos solo por el nombre | Echar un vistazo dentro: los nombres no reflejan la intención de forma confiable |
| Se arrastraron cifras en el README sin volver a contar | Contar en la fuente (lista de herramientas, test, manifiesto) |
| Se creó nueva versión de idioma como borrador vacío | Rellenar o prescindir: un borrador finge exhaustividad |
| Se introdujo segunda convención de nombres para el README | Adoptar la convención existente |
| Se envió PR a una lista ajena sin aprobación | Presentar la comunicación exterior; solo las superficies propias son libres |
| Se contaron issues en lugar de procesarlos | Solucionar, cerrar o preguntar: cada caso recibe un estado |
| Se creó un banner por cuenta propia en estilo ajeno | Respetar la familia de diseño del ecosistema |
| Se corrigió el README en el repo, pero npm/PyPI sigue mostrando el antiguo | Las páginas de registro provienen del último publish: realizar release de parche |
| Se incrementó la versión solo en el manifiesto | Todos los portadores simultáneamente: manifiesto, código, badge, changelog, etiqueta, `llms.txt` |
| Cambios listos, pero dejados sin hacer push | Commitear y hacer push forma parte de la ronda; solo los bloqueos justifican excepciones |
| Todo agrupado en un único commit masivo | Separar limpieza, docu y correcciones; de lo contrario nada es reversible por separado |
| CI en rojo tras commit de docu, sospechando de uno mismo | Linter no fijado sin `select` sigue el valor por defecto de la nueva versión: fijar conjunto de reglas |
| Afirmación falsa corregida solo donde se detectó | Buscar la formulación en toda la org: suele estar en el perfil de la org, en `llms.txt` y en el segundo idioma |
| Se trabajó en repo ajeno sucio con `commit -a` | Preparar y commitear específicamente por ruta, no hacer push: el trabajo ajeno no se toca |
| Cambio realizado en repo limpio de perfil de org, pero no se hizo push | Los repos ajenos limpios reciben su propio commit **y** su propio push |
| Cambio omitido anotado solo en el log propio | Añadir además a la lista de tareas del repo destino, si existe |
| Hallazgo escrito solo en el log de ejecución | Se convierte en tarea del sistema local de tareas: nadie mira registros antiguos |
| Tarea interna colgada en una hoja de ruta pública | Revisar primero; "Public roadmap" significa usar el archivo interno de al lado |
| Hallazgo conocido duplicado como nueva entrada | Enriquecer el punto existente con la evidencia empírica de esta ronda |
| Línea TODO escrita en repo bloqueado durante bloqueo de edición | El bloqueo de edición se aplica a todo el proyecto: no tocar nada allí |
| Bloqueo de push leído como prohibición total y se saltó el repo por completo | Leer el bloqueo: si solo prohíbe la publicación, la ronda local continúa en una rama propia |
| No se hizo push bajo bloqueo de push, pero se cambiaron topics o descripción | Los metadatos también son visibles remotamente: se omiten durante un bloqueo de publicación |

## Lista de comprobación final

- [ ] Superficies de distribución identificadas y anotadas en el log de ejecución.
- [ ] Topics, descripción y página web establecidos y verificados.
- [ ] Filtro de privacidad ejecutado sobre el conjunto rastreado, hallazgos tratados.
- [ ] `.md`/`.txt`/`.json` revisados cuanto a intención de publicación, archivos internos ignorados.
- [ ] Sin force-push sin filtración real; en caso de filtración, rotación realizada.
- [ ] Banner presente e incluido en el README.
- [ ] Versión, funciones, cifras, capturas de pantalla y enlaces comprobados con el estado real.
- [ ] Presentación mejorada (tablas, diagramas, primera altura de pantalla).
- [ ] Matriz de idiomas del README completa; decisiones sobre otros idiomas documentadas.
- [ ] Medidas de visibilidad implementadas o presentadas para aprobación.
- [ ] Entrada en el perfil de org propio revisada, enlaces a orgs ajenas convenientes colocados.
- [ ] Cambios en repos ajenos: limpio → commiteado y push realizado; sucio → commiteado localmente;
      no ejecutado → anotado en la lista de tareas del repo destino.
- [ ] Issues y PRs llevados a un estado definido.
- [ ] Commits separados creados, push realizado, CI y vista remota verificadas.
- [ ] Todas las superficies de distribución llevadas al mismo estado (release de parche si es necesario).
- [ ] Hallazgos no resueltos anotados como tareas en el sistema local de tareas de la carpeta.
- [ ] Log de ejecución escrito en `_after-care/LOG.md`.

## Historial de cambios

### 1.6.0 (2026-07-24)
- Regla añadida: Una corrección de contenido se aplica a todas las superficies. Aprendido empíricamente:
  una aclaración de un usuario se corrigió en la pasada 1 en el Hub, pero permanecía desapercibida
  cinco veces más en el perfil de la organización (EN, DE, `llms.txt`) y solo se notó nueve pasadas después.

### 1.5.0 (2026-07-24)
- Se intensificó el diagnóstico del linter tras ocurrir el patrón tres veces en un día
  (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16): "comprobar primero", códigos
  delatores concretos, división de plataformas, `ruff.toml` como solución si falta `pyproject.toml`,
  verificación contra la nueva versión del linter.

### 1.4.0 (2026-07-24)
- Diagnóstico añadido: Si la CI se pone roja tras un commit de solo docu, la causa más frecuente
  es un linter no fijado sin conjunto de reglas explícito: una nueva versión de la herramienta desplaza
  el valor por defecto y vuelve rojo el código no modificado. Solución: fijar conjunto de reglas,
  nuevas reglas como tarea. Ocurrió dos veces seguidas (n8n-workflow-manager con ruff 0.15, clirec con 0.16).

### 1.3.0 (2026-07-24)
- Nueva sección "Los hallazgos se convierten en tareas": Lo que la ronda no soluciona por sí misma
  se convierte en el momento del descubrimiento en una entrada en el sistema local de tareas del proyecto,
  donde mirará el siguiente encargado, no en el registro de un proceso cerrado. Incluye separación de
  lista interna y roadmap público, enriquecer en lugar de duplicar, tareas completadas con commit.

### 1.2.0 (2026-07-24)
- El filtro de privacidad busca además los nombres de las propias ubicaciones internas. No son
  secretos, por lo que no activan alarmas y superan un filtro que solo busca rutas y tokens,
  pero siguen siendo irresolubles para los lectores y revelan la estructura propia.

### 1.1.0 (2026-07-24)
- Los bloqueos se leen en lugar de tratarse como prohibición general: un bloqueo puro de
  publicación/push redirige la ronda a una rama local en lugar de cancelarla. Asimismo se aclara
  que bajo dicho bloqueo los metadatos, releases y acciones en issues/PR también se omiten,
  ya que son tan visibles remotamente como un push.

### 1.0.0 (2026-07-24)
- Versión inicial. Nivel 1 del mantenimiento posterior del repo, derivado de `github-repo-care`.
