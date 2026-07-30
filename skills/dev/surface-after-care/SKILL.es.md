---
language: es
---

<img src="banner.png" width="100%" alt="surface-after-care banner">

> **Español** — Versión oficial en español de `surface-after-care`.

# Surface After Care — La ronda de mantenimiento regular para un repositorio publicado (Español)

## Cuándo se aplica esta habilidad

Utilízala para un repositorio que **ya es público** y debe revisarse de forma periódica. Es el nivel económico y eficiente: todo lo que se puede decidir dentro del propio repositorio, sin necesidad de inventariar repositorios de terceros ni iniciar un dictamen jurídico.

Diferenciación con habilidades afines:

| Situación | Habilidad |
|---|---|
| El repositorio se publica por primera vez | `github-repo-care` |
| El repositorio es público, ronda de mantenimiento regular | **esta habilidad** |
| Verificación legal adicional + referencias cruzadas en todas las organizaciones + i18n de la aplicación | `full-after-care` (Alias `deep-after-care`) |
| Auditoría pura de derecho/privacidad/licencia antes de hacer público | `repo-publish-check` |
| Mantener sincronizadas las versiones lingüísticas en cuanto a contenido | `bilingual-doc-sync` |
| Distribución de esta ronda en muchos repositorios, rotación justa | `rotation-check` |

## Idea central

Un repositorio publicado tiende a desviarse en dos direcciones: **la documentación describe un software más antiguo que el contenido real del repo**, y **se acumulan archivos que nunca estuvieron destinados a ojos ajenos**. Ninguna de las dos cosas suele ser dramática, pero ambas ahuyentan a los usuarios que se desea atraer: uno abandona porque la guía de instalación ya no funciona, el otro tropieza en el directorio raíz con `AUFGABEN.txt` o `Plan.txt` y se lleva la impresión de que alguien trabaja únicamente para sí mismo.

Esta ronda limpia ambos problemas. Está concebida deliberadamente para ser repetible: es preferible dedicar media hora cuatro veces al año que realizar una gran limpieza una vez al año.

## Flujo de trabajo

El orden no es arbitrario. El Paso 0 está al principio porque determina el alcance de todos los pasos siguientes. El Paso 2 se ejecuta antes de cualquier acción que envíe cambios (push); de lo contrario, se suben mejoras sobre una base que aún debe sanearse. El Paso 1 es puramente del lado del servidor y no interfiere.

### 0. Inventariar las plataformas de distribución

**Antes de modificar cualquier cosa: aclarar dónde está ubicado este proyecto.** El repositorio de GitHub raras veces es la única superficie. Una README corregida sirve de poco si la página del paquete en npm sigue mostrando la versión antigua con instrucciones de instalación erróneas; y ahí es precisamente donde terminan la mayoría de los usuarios, ya que los registros de paquetes suelen posicionarse mejor en los buscadores que el propio repositorio.

```bash
# Los manifiestos revelan los canales de distribución
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Consultar el estado publicado de los canales (solo lo que aplique)
npm view <paquete> version description keywords 2>/dev/null
pip index versions <paquete> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Plataformas habituales: npm, PyPI, Crates, Docker Hub, registro MCP, directorios de plugins/habilidades, marketplaces de VS Code o navegadores, tiendas de aplicaciones, Zenodo/DOI, sitio web del proyecto, perfil de la organización, `llms.txt`, repositorios espejo en otros hosts.

Anota la lista encontrada en el registro de ejecución. A partir de este momento es el **conjunto objetivo**: cada cambio de los pasos siguientes se reflejará al final contra esta lista (véase "Paridad en todas las plataformas"). Si encuentras una plataforma que nadie mantiene y que apunta a un estado abandonado, constituye un hallazgo propio: actualízala o retírala deliberadamente, pero no la dejes obsoleta.

### 1. Establecer temas (Topics)

Los temas son la superficie de búsqueda más importante dentro de GitHub y casi no cuestan nada.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

El objetivo es tener entre 5 y 12 temas desde tres perspectivas: **qué es** (`cli`, `mcp-server`, `python-library`), **de qué trata** (`file-management`, `tax`, `note-taking`) y **cómo funciona** (`local-first`, `offline`, `privacy`). Orientación basada en temas que realmente se utilicen en proyectos comparables; los temas inventados no atraen usuarios. Revisa la descripción y la página de inicio al mismo tiempo, ya que aparecen en la misma vista.

Los temas tienen su equivalente en las demás plataformas del Paso 0: `keywords` en `package.json`, `keywords`/`classifiers` en `pyproject.toml`, categorías y etiquetas en marketplaces y tiendas. Mantén la coherencia en su contenido: son la misma decisión expresada en múltiples lugares.

### 2a. Control de Privacidad (Privacy Gate) — Se ejecuta siempre

Este paso nunca se omite, ni siquiera en una ronda aparentemente inofensiva. Se busca en el conjunto **rastreado (tracked)** por Git, no en el árbol de trabajo visible, porque esa es la diferencia entre "parece limpio" y "está limpio".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Complementa el patrón con los **nombres de tus propias carpetas internas** — carpetas de pipelines, directorios temáticos, áreas de trabajo privadas:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<otros nombres de carpetas internas>" $(git ls-files)
```

Dichas referencias no son secretos y no activan alarmas, por lo que pasan desapercibidas; sin embargo, son **indescifrables** para lectores externos ("transferido de nuevo desde la pipeline .SOFTWARE" no dice nada a un extraño) y revelan la estructura interna propia. Se reemplazan o eliminan, no se toleran. Una búsqueda que solo rastree `C:\Users\…` y patrones de tokens garantizadamente no las encontrará.

¿Se encontró algo? El **tipo** de hallazgo determina el procedimiento: consulta la sección "Regla de Force Push". Un secreto que haya sido confirmado (commit) alguna vez está comprometido: eliminarlo de `HEAD` no basta, debe ser rotado.

### 2b. Comprobar la intención de publicación de los documentos

El verdadero núcleo de esta ronda. Revisa los archivos `.md`, `.txt` y `.json` rastreados y pregúntate en cada uno: **¿Estuvo esto pensado alguna vez para usuarios externos?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

No adivines por el nombre del archivo: examina brevemente su contenido. Un `PLAN.md` puede ser una hoja de ruta pública, mientras que un inofensivo `notes.md` podría ser la estrategia interna de precios. Tres categorías:

**Pertenece al repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, referencias de API, configuraciones de ejemplo, hojas de ruta reales, manifiestos (`package.json`, `pyproject.toml`), archivos de bloqueo (lockfiles), configuración de CI.

**No pertenece al repo, pero no es crítico** — el caso habitual en esta ronda. Archivos de tareas y planificación (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), notas de sesión y traspasos (`HANDOFF`, `BRIEFING`, `_handoff/`), archivos de estado de pipelines internas, diarios de desarrollo, `_archive/`, archivos JSON de registros o índices con rutas locales, estados intermedios y artefactos generados, archivos de trabajo de agentes. Estos archivos no son peligrosos, pero generan desorden y la sensación de una obra sin recoger. Tratamiento: añadir a `.gitignore`, ejecutar `git rm --cached <archivo>` y **hacer push normalmente**.

**No pertenece al repo y es confidencial/sensible** — credenciales, datos personales, datos de clientes, cálculos internos, estrategias de precio y negociación, planes de negocio no publicados, borradores de contratos, todo lo que posea valor competitivo. En este caso no basta con un commit normal; consulta la Regla de Force Push.

En los archivos `.json` conviene hacer una segunda revisión: los manifiestos y lockfiles se mantienen, pero las configuraciones locales, archivos de tareas/registros, volcados de exportación y cualquier elemento con rutas absolutas o nombres de host son polisones típicos.

Si eliminas un archivo que alguien pudiera estar buscando (como una hoja de ruta), menciona brevemente en el commit o en el README dónde reside ahora esa información; de lo contrario, parecerá un retroceso.

### 3. Banners (Encabezados visuales)

Un banner ayuda a determinar si un visitante comienza a leer. Comprueba si existe uno y si está incluido como primer elemento en el README.

Si falta, hay tres vías posibles, recomendadas en este orden:

1. **Generador de imágenes de un agente** (por ejemplo, agy; la palabra "generar" activa allí la creación real de PNG), cuando una imagen se adapte mejor que la tipografía.
2. **Codex**, cuando el banner deba crearse mediante código y exista un modelo de estilo de referencia.
3. **SVG propio**, cuando el banner sea principalmente marca denominativa y lenguaje visual: suele ser la opción más rápida y controlable, y el SVG permanece editable posteriormente.

Mantén la coherencia visual si el proyecto pertenece a una familia: mismo color base, misma estética, mismo tratamiento de marca. Un banner fuera de sintonía se ve peor que no tener ninguno. Tamaño habitual 1200x300; incluye el PNG en el repositorio y el SVG fuente junto a él.

### 4. Contrastar afirmaciones con el estado real

Aquí es donde se aporta el mayor valor. El README afirma cosas: verifícalas en lugar de darles crédito a ciegas:

- **Versión** en README/Badge frente a `pyproject.toml`/`package.json`/`__version__` y frente a la última etiqueta de versión (release tag). Si hay múltiples indicadores de versión, compruébalos todos.
- **Ruta de instalación**: ejecútala realmente (al menos leyendo): ¿Existe el paquete con el nombre indicado? ¿Son correctos los comandos y parámetros?
- **Lista de funcionalidades** frente al código: ¿Está presente todo lo mencionado? ¿Faltan novedades en la lista?
- **Cifras** (número de herramientas, formatos compatibles, cobertura de pruebas): recuéntalas en la fuente en lugar de arrastrar números antiguos. Las cifras en el README caducan en silencio.
- **Capturas de pantalla** frente a la interfaz actual.
- **Requisitos** (versión de Python/Node, dependencias) frente a los manifiestos.
- **Enlaces** a proyectos vecinos, documentación y registros: ¿siguen funcionando?

**Una corrección se aplica a todas las plataformas, no solo a la que llamó la atención.** Si una afirmación resulta ser falsa —especialmente si el responsable del proyecto la aclara—, es muy probable que esa misma afirmación figure en otros lugares: en el perfil de la organización, en `llms.txt`, en la segunda versión idiomática o en el README de un proyecto vecino. Busca específicamente antes de dar el punto por concluido:

```bash
gh search code "<formulación distintiva>" --owner ORG
```

De lo contrario, corregirás un punto y dejarás tres intactos, y la contradicción solo saltará a la vista cuando le toque el turno al siguiente repositorio. Eso no solo cuesta tiempo, sino que destruye la confianza en la documentación: quien encuentra dos descripciones contradictorias de lo mismo, no cree en ninguna.

A continuación, mejora la **presentación** donde sea débil: las listas largas de opciones resultan más legibles en formato tabla; los bloques de código requieren etiquetas de lenguaje; un diagrama Mermaid o árbol ASCII transmite una estructura o flujo más rápido que la prosa; la primera pantalla debe mostrar el propósito, la instalación y un ejemplo de uso, no insignias e historial. Si el README supera las ~400 líneas, traslada los detalles a `docs/` y enlaza a ellos.

**Regla de idioma para los README:** El estándar es un **`README.md` en inglés** más una **segunda versión en español/alemán según corresponda**. Excepción: si el ámbito de aplicación es intrínsecamente local o ya existe únicamente en un idioma, ese se mantiene como idioma principal. Para cada idioma adicional que el proyecto ya soporte, debe incluirse una versión propia de README. Respeta la convención de nombres ya utilizada en el repositorio (`README_es.md`, `README.es.md`, `docs/README.es.md`) y no crees una segunda paralela. Enlaza las versiones entre sí en el encabezado.

### 6. Crear idiomas estándar faltantes

Añade los README correspondientes a los **idiomas estándar** que falten: alemán, inglés, español, chino simplificado, japonés y ruso. El objetivo es el alcance, por lo que esto aplica principalmente a proyectos orientados al usuario; en una librería para desarrolladores con audiencia exclusivamente en inglés, un README en ruso no aporta valor, sino carga de mantenimiento. Decide conscientemente y registra la decisión en el historial de ejecución para que la siguiente ronda no vuelva a debatirlo.

Las nuevas versiones deben **completarse, no solo crearse y dejarse vacías**: un esbozo con "TODO: translate" es peor que la ausencia del archivo porque simula una exhaustividad falsa. La paridad de contenido y la alineación posterior las gestiona `bilingual-doc-sync`; si existen más de dos versiones, merece la pena recurrir a dicha habilidad.

### 7. Visibilidad y difusión

Considera qué acciones aportarán realmente usuarios para **este** proyecto específico y ejecútalas:

- **Registros** a los que el proyecto pertenece técnicamente: registros de paquetes (npm, PyPI), registro MCP, directorios de plugins/habilidades, marketplaces.
- **Listas seleccionadas** (`awesome-*` y colecciones temáticas), siempre que se cumplan estrictamente los criterios de inclusión. Enviar una PR a una lista cuyos criterios el proyecto no cumple cuesta reputación.
- **Superficies propias**: perfil de la organización, `llms.txt`, sitio web del proyecto, README del ecosistema, referencias desde repositorios propios relacionados.
- **Notas de lanzamiento** como oportunidad: un lanzamiento sin explicación de las novedades pasa desapercibido.

**Puerta de Aprobación (Approval Gate):** Todo lo que salga al exterior —PRs a repositorios ajenos, entradas en listas externas, publicaciones, envíos— se **propone y ejecuta solo tras aprobación explícita**, a menos que exista una autorización permanente para ese canal. Los cambios en superficies propias no requieren esta puerta. La razón es sencilla: una PR retirada en un repositorio ajeno es públicamente visible y perjudica la imagen del proyecto.

### 8. Entrada en las páginas de la organización

Primero la organización propia: ¿está el repositorio incluido en el README del perfil (`ORG/.github` → `profile/README.md`), en la sección correcta y con una descripción actualizada?

```bash
gh api user/orgs --jq '.[].login'
```

A continuación, recorre **todas** las organizaciones y responde una sola pregunta por organización: ¿se beneficiaría un visitante de esta página de organización al conocer este repositorio? Por lo general, la respuesta es no; en tal caso, "no enlazar" es el resultado correcto y no una laguna. Cuando la respuesta sea sí (proximidad temática, usuarios compartidos, una herramienta que complementa los proyectos de allí), añade la referencia con una línea que explique su utilidad, no solo el nombre.

El perfil reside en un repositorio propio (`ORG/.github`). Los cambios allí se mantienen y se envían mediante push siguiendo la regla de árbol sucio del Paso 11.

### 10. Incidencias (Issues) y Solicitudes de Extracción (Pull Requests)

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Trabaja en ellas en lugar de limitarte a contarlas:

- **Bugs corregibles**: solucionarlos directamente; en esta ronda el contexto ya está cargado. Correcciones pequeñas y bien delimitadas con pruebas y referencia al número de incidencia.
- **Incidencias ya resueltas**: cerrarlas indicando en una frase qué las resolvió.
- **Notificaciones poco claras**: requieren una pregunta de aclaración específica (versión, sistema operativo, pasos de reproducción).
- **PRs**: leer el diff real, ejecutar pruebas y luego fusionar o responder de forma fundamentada. Una PR sin respuesta durante meses cuesta más buena voluntad que un rechazo educado.
- **Casos inactivos (stale)**: resolverlos en lugar de arrastrarlos.

**Puerta de Aprobación:** Los comentarios públicos, cierres con justificación y fusiones de contribuciones ajenas constituyen comunicación exterior: presentarlos antes de la ejecución a menos que exista autorización permanente. Las correcciones puras de código en el repositorio propio están exentas.

### 11. Commit, Push y Verificación

La ronda no concluye con las modificaciones, sino cuando están **publicadas**. Un árbol de trabajo lleno de mejoras sin push es el peor resultado: la siguiente sesión —posiblemente con otro agente o dispositivo— tendrá que adaptarse a un estado a medio hacer, mientras que en las plataformas públicas no habrá mejorado nada.

Antes del push, verifica lo que sea comprobable: ejecuta pruebas y comprobaciones de humo (smoke tests); en cambios de documentación, revisa los enlaces y la vista renderizada. Agrupa en **commits separados por tema** en lugar de incluir todo en un commit global: la limpieza, la actualización de documentación y la corrección de errores son tres cosas distintas, y quien necesite revertir una de ellas más adelante lo agradecerá:

```bash
git add .gitignore && git rm --cached <archivos internos>
git commit -m "chore: retirar archivos de trabajo internos del repositorio"
git commit -am "docs: actualizar README al estado actual (versión, herramientas, capturas)"
git commit -am "fix: <número de incidencia> ..."

git pull --rebase        # en caso de rama divergente, antes del push
git push
```

Posteriormente, verifica en lugar de asumir: README remoto en la vista renderizada, ejecución de CI, estado de versiones y etiquetas.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**Si la CI marca error (rojo) tras un commit que solo modificó documentación**, la causa casi nunca estará en tu cambio. El caso más frecuente con diferencia es un **linter sin versión fija y sin regla explicitada**. Comprueba esto **en primer lugar** antes de sospechar de tu commit.

Mecanismo: si el flujo de trabajo ejecuta `ruff check` (o flake8, eslint…) contra una dependencia no fijada (`ruff>=0.12` o sin versión), y falta una selección explícita de reglas (`[tool.ruff.lint] select = [...]`, o un `ruff.toml` si no hay `pyproject.toml`), el linter aplicará la configuración por defecto de la versión recién instalada. Una nueva versión del linter altera este comportamiento por defecto y hace que un código intacto falle. Señales delatadoras:

- Códigos de regla que el proyecto nunca tuvo (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999`…), a veces por cientos.
- El fallo suele ser **desigual según la plataforma**: los ejecutores con versiones anteriores en caché se mantienen en verde, los nuevos fallan.
- A veces una regla cuestiona algo inamovible (`N999` sobre el propio nombre del paquete): señal clara de que nunca fue estándar.

Solución: fijar el conjunto de reglas que anteriormente daba verde (`select = ["E4","E7","E9","F"]` son los valores por defecto clásicos de ruff). Si no existe `pyproject.toml`, crea un `ruff.toml`. Verifica contra la **nueva** versión del linter (instalar, reproducir hallazgos sin configuración y confirmar "passed" con la configuración). Las nuevas reglas entran como **tarea** en el proyecto: su adopción es una decisión, no un efecto secundario de actualizar una herramienta.

Dos casos en los que **no** se hace push: si rige una prohibición de publicación o entrega en el proyecto, o si el estado se declara deliberadamente inacabado. Ambos son excepciones justificadas; el caso habitual es: commit y push.

En caso de prohibición de publicación, la ronda no se cancela, sino que se **desvía**: realizar commits locales en una rama propia (`judging-hold/…`, `freeze/…`), dejar la rama principal intacta en el estado entregado, anotar la razón del bloqueo en el registro de ejecución y actualizar tras la liberación. Es fundamental mantener la coherencia: el bloqueo no solo aplica a `git push`, sino a **cualquier cambio visible de forma remota** (temas, descripción, página de inicio, lanzamientos, acciones de incidencias y PRs).

Si existen otros clones del mismo repositorio (segundo dispositivo, copia de despliegue, espejo), actualízalos inmediatamente después del push. Un clon con diez commits de retraso generará diagnósticos erróneos sobre un estado extinto.

#### Modificaciones en otros repositorios — Excepción de árbol sucio (Dirty Tree)

Esta ronda genera con frecuencia cambios **fuera** del repositorio intervenido: una línea en el perfil de la organización (Paso 8) o una referencia inversa en un repositorio afín. Dichos cambios también se confirman y envían: una referencia no publicada no existe.

Antes de tocar un repositorio ajeno, comprueba su estado:

```bash
git -C <ruta> status --porcelain
```

**Árbol de trabajo limpio** → realizar el cambio, añadir en un **commit propio y temáticamente claro** (`docs: link <proyecto>`), y hacer push. No mezclar con los commits del repositorio principal: es un repositorio distinto con su propia historia y lectores.

**Sucio, pero los cambios ajenos están en otros archivos** → tu cambio se puede realizar de forma limpia. Prepara (stage) y confirma **únicamente tu archivo de forma precisa** para evitar incluir trabajo ajeno no verificado:

```bash
git -C <ruta> add README.md
git -C <ruta> commit -m "docs: link <proyecto>"     # solo la ruta preparada
```

Pero **no hagas push**. El commit local es inofensivo; un push podría no serlo: desconoces hacia dónde se dirige el otro estado de trabajo (podría estar en rebase o reestructuración) y tu push obligaría a una integración no deseada. El commit local asegura tu trabajo sin imponer nada a nadie; el proceso que revise ese repositorio más adelante lo encontrará y lo incorporará.

**Sucio precisamente en el archivo que debes modificar** → no tocar. En este caso tendrías que basarte en un estado intermedio ajeno y confirmarlo junto con el tuyo; comprender ese trabajo cuesta más de lo que vale la referencia.

**Bloqueo activo (`LOCK*.txt`) en el repositorio destino** → **leer primero el candado en lugar de tratarlo como una prohibición total.** Un bloqueo describe su propio alcance, que a menudo es más estrecho que "nada en absoluto". Casos típicos:

- **Bloqueo de edición** ("alguien está trabajando aquí") → no tocar nada, ni siquiera archivos secundarios.
- **Bloqueo puro de publicación/push** (entrega, evaluación, congelación) → el trabajo local sigue permitido, solo está bloqueado el contacto remoto. Trabaja en una rama propia y haz commit local; **se omiten los pasos con impacto remoto** (push, temas, descripción, página de inicio, lanzamientos y acciones en incidencias/PRs).

Interpretar un bloqueo de push como prohibición total desperdicia la parte local de la ronda sin ganar seguridad. Por contra, omitir solo el push mientras se alteran metadatos es insuficiente. En caso de duda, cita el bloqueo y consulta.

#### La intención no debe perderse

Si el cambio **no** se ejecuta por alguna de estas razones, trasládalo a la lista de tareas del repositorio destino (`AUFGABEN.txt`, `TODO.md` o `TODO.txt`, según lo que exista allí). Una entrada con fecha, cambio deseado y motivo:

```markdown
- [ ] [2026-07-24, after-care] Añadir referencia cruzada hacia <proyecto> en el README
      (omitido: el README tenía cambios ajenos sin commit)
```

Esa es la diferencia entre "pospuesto" y "olvidado": la lista de tareas es donde consultará el siguiente desarrollador, siendo más fiable que una nota en el registro de un proceso ajeno. Si no existe lista de tareas, no la crees; bastará con mantener el punto abierto en tu propio registro de ejecución.

Con un **bloqueo activo esto tampoco aplica**: no se modifica el archivo y la nota se mantiene únicamente en el registro propio. Anótalo en ambos casos para que la rotación conozca el pendiente.

Por último, atiende las plataformas del Paso 0 (véase la siguiente sección).

## Paridad en todas las plataformas de distribución

Para concluir la ronda, revisa la lista del Paso 0: **Todo cambio que un usuario pudiera ver debe llegar a cada plataforma donde pudiera buscarlo.** Un repositorio cuya página en npm cuenta una historia distinta a su código está en peor situación que uno con una sola plataforma.

Mecanismo clave: **los registros de paquetes muestran el README de la última publicación, no el estado actual del repositorio.** Una corrección en el README solo se hace visible en npm o PyPI al publicar una nueva versión. Si la corrección es relevante en contenido (instalación errónea, versión equivocada, lista de funciones obsoleta), requiere una versión parche; de lo contrario, la corrección carecerá de efecto.

| Plataforma | Qué se gestiona allí | Cómo se aplica |
|---|---|---|
| npm | README, `description`, `keywords`, enlace al repositorio | Solo mediante `npm publish` (versión parche); los metadatos provienen de `package.json` |
| PyPI | README (`long_description`), clasificadores, URLs del proyecto | Solo mediante una nueva subida; metadatos de `pyproject.toml` |
| Registro MCP / Directorios de plugins | Descripción, versión, lista de herramientas, doc de inicio | Según el registro, actualización de manifiesto o nuevo envío |
| Marketplace / Tienda | Descripción, capturas de pantalla, categorías, traducciones | Mediante la interfaz de administración correspondiente; las capturas envejecen rápido |
| Docker Hub / Registry de contenedores | Descripción, etiquetas, ejemplo de uso | Descripción del repositorio más nueva etiqueta |
| Zenodo / DOI | Metadatos, autores, versión | Edición directa para metadatos, nueva versión para contenidos |
| Sitio web / Perfil org / `llms.txt` | Descripción corta, enlace, posicionamiento | Directamente editable: las plataformas más económicas, nunca las olvides |

Si se incrementa una versión, **todos los indicadores de versión** deben actualizarse simultáneamente: manifiesto, constantes de código, insignias del README, registro de cambios, etiqueta de versión, `llms.txt`. Un estado de versión a medio actualizar es más difícil de diagnosticar que uno consistentemente antiguo.

Si una actualización no es posible o conveniente en una plataforma (por ejemplo, un lanzamiento solo por una errata), regístralo en el informe de ejecución para que la siguiente ronda no interprete la discrepancia como un descuido.

## Regla de Force Push

El estándar es **no realizar force push**. Ignorar retrospectivamente archivos de planificación interna no justifica reescribir el historial: el esfuerzo es elevado, cada clon y fork se rompe, las PR abiertas quedan inservibles y el beneficio es mínimo porque el contenido es inofensivo. Vía normal:

```bash
git rm --cached <archivo>            # fuera del seguimiento, se conserva localmente
# añadir a .gitignore
git commit -m "chore: retirar archivos de trabajo internos del repositorio"
git push
```

Reescribir el historial (y por tanto hacer push con `--force-with-lease`) solo se justifica ante **filtraciones reales (leaks)**: credenciales y claves, datos personales o de clientes, así como documentos con valor competitivo real (cálculos internos, estrategias de precios, planes no publicados, detalles de contratos). En ese caso:

1. **Rotar primero los secretos afectados**: el historial ya ha sido copiado, bifurcado y almacenado en caché. La rotación resuelve el riesgo; el borrado es cosmético.
2. Limpiar historial (`git filter-repo` o BFG), hacer push con `--force-with-lease`.
3. Revisar forks y cachés; contactar con el soporte de GitHub para objetos huérfanos si es preciso.
4. Registrar el incidente en el informe de ejecución: qué, cuándo y qué rotación se ejecutó.

Ante la duda entre "no crítico" y "confidencial": tratar como confidencial y consultar. Los costes son asimétricos.

## Los hallazgos se convierten en tareas, no en meras líneas de registro

Una ronda de mantenimiento encuentra regularmente más aspectos de los que puede o debe solucionar en la misma sesión: una versión lingüística faltante, un retraso de modernización, una publicación que nunca se realizó. **Dichos hallazgos se convierten en tareas en el momento de su descubrimiento**; de lo contrario, quedarán sepultados en el registro de una ejecución finalizada donde nadie volverá a mirar.

La tarea pertenece al **sistema local de tareas del proyecto** —allí donde consultará la persona que trabaje a continuación en el proyecto. Típicamente es `AUFGABEN.txt` o `TODO.md` en la carpeta del proyecto, que a menudo **no está en el clon de Git**, sino en la ubicación donde reside la gestión del proyecto. El clon contiene el código; la carpeta del proyecto contiene la gestión. Una entrada en el clon que desaparezca con el siguiente `git clean` no es una tarea.

Tres aspectos a considerar:

1. **Separar la lista de tareas interna de la hoja de ruta pública.** Un `TODO.md` puede ser una hoja de ruta pública cuidada; en ese caso, no es lugar para notas internas. Examínalo antes de añadir contenido: si contiene un encabezado como "Public roadmap", escribe en el archivo interno contiguo (`AUFGABEN.txt`) y márcalo como interno.
2. **Revisar entradas existentes antes de duplicar.** A menudo el hallazgo ya figura allí. En tal caso no se crea una entrada nueva, sino que se **enriquece** con la evidencia empírica de esta ejecución ("confirmado: `--help` muestra salidas completamente en español"). Un punto conocido con prueba fresca es más valioso que una segunda entrada duplicada.
3. **Anotar lo resuelto.** Lo que la ronda haya solucionado debe incluirse como punto marcado con su hash de commit. Esto explica a la siguiente ronda por qué desapareció un hallazgo y evita que vuelva a "descubrirse".

Formula la tarea de modo que resulte comprensible sin el contexto de esta ejecución: qué se encontró, por qué importa y cuál sería el siguiente paso. "i18n incompleta" no es una tarea; "El catálogo solo contiene `status.title`, es/zh/ja/ru están vacíos: trasladar primero las cadenas de CLI al catálogo, luego completar los seis idiomas" sí lo es.

## Registro de ejecución (Run Log)

Registra el resultado en `_after-care/LOG.md` (la carpeta debe incluirse en `.gitignore`: es material de pipeline, no contenido del repo, según el Paso 2b). Una línea por ejecución con fecha, nivel y decisiones conscientes:

```markdown
## 2026-07-24 — surface
- Plataformas: GitHub, npm (<paquete>), registro MCP, perfil org, llms.txt
- Temas: +local-first, +mcp-server; keywords en package.json alineados
- Eliminados: AUFGABEN.txt, _handoff/ (en gitignore, sin necesidad de force push)
- README: Versión corregida 0.9 -> 1.2, recuento de herramientas 23 -> 26
- Idiomas: EN + ES mantenidos; ZH/JA/RU omitidos deliberadamente (audiencia técnica)
- Incidencias: #12 corregida, #7 cerrada (resuelta), #15 consulta enviada
- Push: 3 commits, CI en verde; republicación en npm 1.2.1 por corrección de README
- Pendiente: Capturas de la tienda obsoletas, requieren nuevo build
```

El registro evita que la siguiente ronda vuelva a debatir las mismas decisiones y constituye la base para las rondas de mantenimiento rotativas en múltiples repositorios (`rotation-check`).

## Errores frecuentes

| Error | Corrección |
|---|---|
| Observar solo el árbol de trabajo y no `git ls-files` | Revisar siempre el conjunto rastreado: ahí residen los problemas |
| Control de privacidad limitado solo a rutas y tokens | Buscar también nombres de carpetas/pipelines internas: no activan alarmas pero exponen la estructura |
| Eliminar archivo interno reescribiendo el historial | En archivos no críticos basta con `git rm --cached` + push normal |
| Eliminar secreto de `HEAD` y dar el asunto por resuelto | Rotar el secreto; lo demás es cosmética |
| Clasificar archivos solo por su nombre | Examinar brevemente el contenido: los nombres no reflejan la intención de forma fiable |
| Arrastrar cifras en el README sin recontar | Contar en la fuente (lista de herramientas, ejecución de pruebas, manifiesto) |
| Crear nueva versión de idioma como plantilla vacía | Completar o no crear: un borrador simula una integridad falsa |
| Introducir una segunda convención de nombres para el README | Adoptar la convención existente en el repositorio |
| Enviar PR a una lista ajena sin autorización | Presentar la comunicación exterior; solo las superficies propias están preaprobadas |
| Contar incidencias en lugar de gestionarlas | Corregir, cerrar o consultar específicamente: cada caso recibe un estado definido |
| Crear un banner de forma independiente con un estilo ajeno | Respetar la familia de diseño del ecosistema |
| Corregir README en repo pero la página de npm/PyPI sigue desactualizada | Las páginas de registros provienen del último publish: realizar un patch release |
| Incrementar versión únicamente en el manifiesto | Actualizar todos los indicadores a la vez: manifiesto, código, badge, changelog, tag, `llms.txt` |
| Cambios listos pero dejados sin hacer push | Hacer commit y push forma parte de la ronda; solo las prohibiciones justifican la excepción |
| Agrupar todo en un único commit masivo | Separar limpieza, documentación y soluciones: de lo contrario, nada se puede revertir individualmente |
| CI en rojo tras commit de documentación y culparse a uno mismo | Linter sin versión fija y sin `select` sigue la nueva versión: fijar el conjunto de reglas |
| Corregir una afirmación falsa solo donde se detectó | Buscar la formulación en toda la org: suele figurar en el perfil, `llms.txt` y en el segundo idioma |
| Trabajar con `commit -a` en un repo ajeno sucio | Preparar por rutas exactas y hacer commit sin hacer push: el trabajo ajeno no se toca |
| Realizar cambio en repo limpio de perfil de org pero no hacer push | Los repos ajenos limpios reciben su propio commit **y** su propio push |
| Anotar cambio omitido únicamente en el registro propio | Registrar también en la lista de tareas del repositorio destino si existe |
| Escribir hallazgo únicamente en el registro de ejecución | Convertirlo en tarea en el sistema local de tareas: nadie consulta registros antiguos |
| Vincular trabajo interno a una hoja de ruta pública | Examinar primero; "Public roadmap" significa usar el archivo interno contiguo |
| Duplicar un hallazgo conocido como entrada nueva | Enriquecer el punto existente con la prueba empírica de esta ejecución |
| Escribir línea TODO en repo bloqueado durante prohibición de edición | El bloqueo aplica a todo el proyecto: no tocar nada allí |
| Leer bloqueo de push como prohibición total y omitir el repo | Leer el bloqueo: si solo prohíbe publicar, continuar la ronda en una rama local |
| Omitir push por bloqueo pero modificar metadatos | Los metadatos son visibles remotamente: bajo bloqueo de push también se omiten |

## Lista de comprobación final

- [ ] Plataformas de distribución identificadas y anotadas en el informe de ejecución.
- [ ] Temas, descripción y página de inicio configurados y verificados.
- [ ] Control de privacidad ejecutado sobre el conjunto rastreado y hallazgos gestionados.
- [ ] Archivos `.md`/`.txt`/`.json` revisados según intención de publicación; archivos internos ignorados.
- [ ] Sin force push salvo filtración real; en tal caso, rotación ejecutada.
- [ ] Banner presente e incluido en el README.
- [ ] Versión, funciones, cifras, capturas de pantalla y enlaces verificados con el estado real.
- [ ] Presentación mejorada (tablas, diagramas, contenido principal visible sin scroll).
- [ ] Matriz de idiomas del README completa; decisiones sobre otros idiomas documentadas.
- [ ] Acciones de visibilidad ejecutadas o presentadas para aprobación.
- [ ] Entrada en el perfil de org propia verificada; referencias a orgs externas añadidas con criterio.
- [ ] Cambios en repos ajenos: limpio → commit y push; sucio → commit local; no ejecutado → anotado en lista de tareas del repo destino.
- [ ] Incidencias y PRs llevados a un estado definido.
- [ ] Commits separados creados, enviadas las modificaciones, CI y vista remota verificadas.
- [ ] Todas las plataformas de distribución actualizadas al mismo estado (publicación parche si procede).
- [ ] Hallazgos no resueltos registrados como tareas en el sistema local de tareas del proyecto.
- [ ] Registro de ejecución guardado en `_after-care/LOG.md`.

## Registro de cambios

### 1.6.0 (2026-07-24)
- Regla añadida: Una corrección de contenido aplica a todas las plataformas. Aprendido empíricamente: una aclaración de usuario se corrigió en el Hub en la ejecución 1, pero permaneció inadvertida en cinco lugares del perfil de la organización (EN, DE, `llms.txt`) y solo se detectó nueve ejecuciones después.

### 1.5.0 (2026-07-24)
- Diagnóstico del linter precisado tras ocurrir el patrón tres veces en un día (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16): "comprobar primero", códigos de regla delatadores concretos, división por plataformas, solución `ruff.toml` si falta `pyproject.toml`, verificación contra la nueva versión del linter.

### 1.4.0 (2026-07-24)
- Diagnóstico añadido: Si la CI marca rojo tras un commit exclusivo de documentación, la causa más habitual es un linter no fijado y sin selección explícita de reglas: una nueva versión de la herramienta cambia la configuración por defecto y marca errores en código no modificado. Solución: fijar reglas y registrar nuevas reglas como tarea.

### 1.3.0 (2026-07-24)
- Nueva sección "Los hallazgos se convierten en tareas": Lo que la ronda no resuelve por sí misma se convierte en una entrada en el sistema local de tareas del proyecto en el momento de descubrirse (donde mirará el siguiente desarrollador, no en el registro de una ronda finalizada). Incluye separación de lista interna y roadmap público, enriquecer en lugar de duplicar y registrar lo completado con hash de commit.

### 1.2.0 (2026-07-24)
- El control de privacidad busca adicionalmente los nombres de las carpetas internas propias. No son secretos, por lo que no activan alarmas y superan un filtro enfocado solo en rutas y tokens, pero resultan indescifrables para los lectores y exponen la estructura interna.

### 1.1.0 (2026-07-24)
- Los bloqueos se leen en lugar de tratarse como prohibiciones generales: un bloqueo de publicación/push desvía la ronda a una rama local en lugar de cancelarla. Se aclara que bajo dicho bloqueo también se omiten metadatos, versiones y acciones en incidencias/PRs, ya que son tan visibles remotamente como un push.

### 1.0.0 (2026-07-24)
- Versión inicial. Nivel 1 del mantenimiento posterior de repositorios, derivado de `github-repo-care`.