---
name: folder-organization
version: 1.1.0
type: protocol
author: Lukas Geiger + OpenAI Codex
created: 2026-08-24
updated: 2026-08-24
description: "Ordenar semánticamente carpetas y almacenes de archivos: reconocer reglas locales y la taxonomía existente, asignar archivos según su contenido, mantener los conjuntos relacionados, archivar series claras de predecesor/sucesor y registros, separar contenido mixto válido y obsoleto mediante Cut-and-Clue, y colocar los candidatos a eliminación en una papelera de revisión reversible. Usa esta skill con „limpiar carpeta“, „ordenar archivos con sentido“, „archivar versiones antiguas“, „limpiar archivos de registro“, „separar contenido vigente de obsoleto“ o cuando durante la limpieza aparezcan archivos de secretos o secretos en un almacén en la nube. Funciona de forma neutral respecto a proveedor y usuario, únicamente por sí sola; los módulos compatibles o los servicios de archivos reconocidos se usan solo como aceleradores opcionales. Para reglas de recopilación recurrentes ya completamente definidas, usa en su lugar una automatización de archivos basada en reglas; para reestructurar una arquitectura completa de proyecto, usa un optimizador de pipeline/proyecto."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: utilities
tags: [ordner, dateien, sortierung, archivierung, versionen, logs, geheimnisse, cloud, cut-and-clue, cleanup, standalone]
language: es
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
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="folder-organization banner">

# Organización de carpetas

## Objetivo y límite

Crea un archivo trazable en el que cada cambio esté justificado por reglas locales, contenido,
relaciones entre archivos o una decisión explícita del usuario. La skill es un protocolo de
ordenación semántica, no un segundo programa para mover archivos ni una obligación de vincularse
a un proveedor.

Un inventario o una revisión permanece en solo lectura. Una instrucción explícita como „limpia esta
carpeta“ autoriza traslados seguros y reversibles dentro del área indicada, siempre que no exista
una ambigüedad sin resolver. Sobrescribir, eliminar definitivamente, mover fuera del área, reescribir
contenido o activar una automatización permanente requiere una autorización aparte.

## Núcleo autónomo y semillas opcionales

Empieza siempre por el núcleo autónomo. Solo necesita lectura, escritura, cálculo de hashes y
operaciones ordinarias de archivos. Para un inventario reproducible está disponible
[`scripts/folder_organization.py`](scripts/folder_organization.py); los valores predeterminados seguros y las sobrescrituras
se encuentran en [`config.json`](config.json). El script escribe por defecto solo en
stdout. `--out` solo puede crear un archivo nuevo fuera de la raíz examinada; los destinos
existentes no se sobrescriben. Sus hallazgos de registros y versiones son pistas de búsqueda de baja
confianza, no una autorización para archivar.

La versión de biblioteca tiene front matter de catálogo ampliado. Si un sistema de destino solo acepta
front matter básico portable (`name`, `description`),
[`scripts/export_portable.py`](scripts/export_portable.py) crea una copia autónoma en una nueva carpeta de destino.
El flujo funcional y todas las piezas locales de repuesto permanecen completos.

Luego descubre capacidades, no nombres de marcas. Una integración existente puede mejorar el núcleo,
pero no cambia ni el significado ni los permisos:

| Capacidad requerida | Alternativa autónoma | Semilla/adaptador opcional detectado |
|---|---|---|
| Inventario, hashes, plan | script Python incluido o búsqueda nativa de archivos | planificación/recibos de FolderHome |
| Contenido de documentos/OCR | lector local existente; en su defecto `unreadable/review` | doc-services o extractor equivalente |
| Operaciones seguras con nube/bloqueos | operación nativa con una verificación de estado reciente | FileCommander o adaptador propio del proveedor |
| Reglas estables recurrentes | emitir la configuración como propuesta | file-collect-sort-action o automatización equivalente |
| Reindexar pistas | marcadores CLUE llamativos en el texto | Gardener u otro indexador local |

Los componentes de Ellmos son por tanto **Grounding Seeds**: si sus capacidades están disponibles y
autorizadas para la tarea, usa sus controles más estrictos. Si faltan, ejecuta el mismo flujo
funcional de forma heurística y con los repuestos de esta skill. Ninguna transmisión externa se
produce solo porque falte un lector local.

## Procedimiento

### 1. Determinar raíz, reglas y modo

- Elige la raíz común más pequeña; no escanees por comodidad un directorio de usuario completo ni una
  raíz de nube entera.
- Lee los archivos de control dentro de la raíz y hacia arriba, por ejemplo `AGENTS.md`,
  `CLAUDE.md`, `README.md`, `START.md`, reglas de nombres, registros,
  manifiestos y bloqueos.
- Registra el modo: ordenación semántica única, mantenimiento de archivo, mantenimiento de registros,
  Cut-and-Clue o preparación de una regla recurrente.
- Las carpetas de destino existentes y su uso real pesan más que una taxonomía ideal inventada.

### 2. Política de secretos antes de cualquier acceso al contenido

Antes de abrir o calcular el hash, compara el nombre con `secret_policy.protected_name_patterns` y con las exclusiones de
`config.json`. Los archivos protegidos como `.env`, las claves privadas o los
archivos de credenciales solo se registran por ruta y metadatos; su contenido no debe llegar al
contexto del modelo, al informe ni al registro. `--hash-all` no levanta este límite. Si en un
archivo de texto normalmente legible se detecta por casualidad una señal de secreto, detén la salida
del contenido e informa solo del ID de la señal.

Si el hallazgo probablemente está en una raíz de nube o sincronización, se aplica el
`cloud_action` configurado. El valor predeterminado es `localize-after-approval`: demostrar un destino
local fuera de todas las raíces de sincronización y con permisos restrictivos, hacer un dry-run y
obtener autorización, copiar el archivo de forma opaca y verificarlo internamente por hash, y solo
entonces reemplazar la fuente en la nube de forma recuperable y dejar un puntero no secreto. Sin
`local_secret_root` configurado o con referencias de runtime en riesgo, bloquea.

La transacción completa, los modos de puntero (`control-file`, `sidecar`,
`placeholder`), el mapa local de punteros, las indicaciones de rotación y el bloqueo estricto
están en [`references/secrets-policy.md`](references/secrets-policy.md). Retira los archivos sospechosos de contener
secretos de la ordenación normal, el archivado, Cut-and-Clue y la papelera hasta que se tome la
decisión de política.

### 3. Registrar inventario y relaciones

Registra ruta, tamaño, fecha de modificación, tipo y, en la medida en que sea proporcionado, SHA-256.
En documentos ambiguos lee el contenido o los metadatos. Los binarios ilegibles quedan explícitamente
sin aclarar; el nombre y la extensión por sí solos no justifican una acción irreversible.

Trata los archivos relacionados como conjunto: versiones de idioma, fuente/exportación, Markdown/PDF,
documento/recursos, datos/script/resultado, anexo/archivo principal y predecesor/sucesor. Antes de un
traslado, revisa enlaces, manifiestos, includes, referencias de código y registros.

Para la matriz detallada de evidencia y confianza en inventarios difíciles, lee
[`references/heuristics.md`](references/heuristics.md).

### 4. Planificar la estructura de destino y las decisiones individuales

Deriva la estructura de destino a partir del propósito, las reglas existentes y los grupos reales. La
raíz es una superficie de enrutamiento, no un almacén permanente. No crees carpetas genéricas como
`_Sonstiges` si el hallazgo sigue sin aclararse en cuanto a contenido; para ello usa
`review/` o una lista de decisiones.

Cada cambio planificado contiene como mínimo:

| Campo | Contenido |
|---|---|
| Origen | ruta relativa exacta y, opcionalmente, hash |
| Destino/acción | `keep`, `move`, `rename`, `archive`, `trash-review`, `cut-and-clue`, `review` |
| Justificación | regla, contenido, relación o prueba de versión |
| Confianza | alta, media o baja |
| Efecto secundario | enlaces, conjuntos, registros o automatización afectados |

- **Alta:** regla local explícita, referencia clara en un manifiesto o serie sucesora claramente
  documentada.
- **Media:** fuerte coincidencia de contenido o un grupo existente, pero sin regla explícita.
- **Baja:** solo nombre, extensión, fecha de modificación o similitud incierta. No moverlo
  automáticamente.

Antes de la mutación entrega un dry-run completo. Las colisiones, los enlaces simbólicos, los bloqueos
de nube, los archivos ilegibles y los destinos fuera de la raíz bloquean la acción correspondiente.

### 5. Archivar versiones y registros

Archiva un archivo antiguo como predecesor solo cuando la serie esté respaldada por varias señales:
identificador de versión o fecha, indicación de versión interna, alto solapamiento de contenido,
propósito coincidente y un sucesor claramente válido. La fecha de modificación por sí sola no basta.
Los estados de prueba referenciados y las publicaciones aprobadas se conservan.

En los registros distingue entre registro activo de ejecución, registro de auditoría o evidencia e
historial rotable. No muevas registros activos ni registros que aún se estén escribiendo. Archiva los
registros antiguos y cerrados según la convención local o, en su defecto, por ejemplo bajo
`_archive/logs/<jahr>/`, con hash y ubicación de origen. La compresión es una decisión propia; archivar no
significa eliminar automáticamente.

### 6. Aplicar Cut-and-Clue

Si un archivo contiene a la vez contenido válido y obsoleto, el traslado a ciegas es tan incorrecto
como conservarlo todo sin cambios. En ese caso, **corta** el contenido válido hacia uno o varios
archivos canónicos nuevos y deja en el material antiguo, y si procede directamente en el punto
problemático, un **Clue** legible por máquina sobre estado, motivo y sucesor. Solo después de la
verificación de completitud archiva el original.

Los marcadores, las reglas para `[sic]`, los binarios y la protección contra la pérdida de
historial están en [`references/cut-and-clue.md`](references/cut-and-clue.md). `[sic]` marca un error citado
de forma intencionada; para la obsolescencia usa `OUTDATED` o `SUPERSEDED`.

### 7. Papelera de revisión en lugar de eliminar

Mueve los candidatos a eliminación dentro de la raíz a una carpeta de ejecución como
`_trash_review/<run-id>/`. Conserva la estructura relativa y escribe `MANIFEST.md` o
`RESTORE.json` con origen, nueva ruta, hash, motivo y momento. No elimines nada de ahí de forma
automática y definitiva. Así el usuario puede revisar toda la ejecución y luego eliminar o revertir
por sí mismo.

Si existe una carpeta de entrada vigilada, crea la papelera y el archivo fuera de su área de escaneo,
para evitar una autoalimentación.

### 8. Ejecutar y documentar

- Justo antes de cada acción, vuelve a comprobar origen, hash, destino y ausencia del destino.
- Nunca sobrescribas; en caso de colisión bloquea o usa un nombre nuevo planificado explícitamente.
- Tras la ejecución, lee el estado del destino, compara hashes, busca los nombres de ruta antiguos en
  las referencias y actualiza los registros afectados.
- Elimina solo las carpetas vacías creadas por ti mismo. Para cada mutación conserva una vía de retorno
  o un manifiesto.
- Reindexa las marcas CLUE si hay un indexador local; sin indexador siguen siendo efectivas como texto
  normal y llamativo.

## Ejemplos breves

- `bericht_v1.md` y `bericht_v2.md`: al principio márcalos solo como posible serie de versiones.
  Solo la versión interna, el contenido y las referencias determinan si `v1` puede
  archivarse realmente.
- `konzept.md` contiene reglas válidas y secciones obsoletas: traslada la sustancia válida por
  completo a un nuevo archivo canónico, conserva el original byte a byte y crea Clues o un sidecar con
  el sucesor.
- `.env` en una raíz de sincronización: no lo abras ni lo copies en el informe. Genera un
  plan de política; sin `local_secret_root` acreditado, autorización y un cambio seguro de runtime, no
  modifiques ningún archivo.

## Aprendizaje y automatización

Recoge las correcciones del usuario como candidatas a regla, sin elevarlas nunca en silencio a reglas.
Solo cuando un patrón esté confirmado repetidamente, sin conflictos y claramente acotado, propón a
partir de él una automatización recurrente. Cada automatización nueva o modificada necesita de nuevo
dry-run y autorización.

## Informe final

Además de inventario, acciones, archivos, papelera, sucesores de Cut-and-Clue y decisiones abiertas,
informa de todos los candidatos a secreto exclusivamente mediante ruta o ID de señal, su estado de
política, las externalizaciones a la nube bloqueadas o autorizadas, el modo de puntero y el readback.
Nunca reproduzcas valores, rutas locales de secretos ni líneas de contexto sensibles.

Indica el inventario inicial, las acciones ejecutadas y bloqueadas, las rutas de archivo y de papelera,
los sucesores de Cut-and-Clue, las referencias actualizadas, el resultado de hash y readback, las
decisiones abiertas y las reglas recurrentes propuestas. Una planificación no es un orden ejecutado.

## Skills relacionadas

- Automatización de archivos basada en reglas: para patrones fuente-patrón-destino recurrentes ya
  conocidos.
- Optimizador de pipeline/proyecto: para la reestructuración estructural de un proyecto o stack completo.
- Tidy-up/Maintenance: para el cierre de sesión, el mantenimiento de registros y los archivos temporales
  del proyecto.
- Folder-Flattening: solo si la transformación solicitada explícitamente es el aplanado.

## Registro de cambios

### 1.1.0 (2026-08-24)

- Se añadió una política de secretos configurable con no apertura de nombres de archivo protegidos,
  detección aleatoria redactada y externalización transaccional a la nube, con mapeo local y puntero
  no secreto.

### 1.0.0 (2026-08-24)
- Versión inicial neutral respecto a proveedor y usuario, con script autónomo, principio de semilla
  opcional, ordenación semántica, archivado de versiones y registros, Cut-and-Clue y papelera de revisión.
