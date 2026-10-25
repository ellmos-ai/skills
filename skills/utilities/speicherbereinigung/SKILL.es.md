---
name: speicherbereinigung
version: 1.0.0
type: skill
author: Lukas Geiger und OpenAI Codex
created: 2026-08-04
updated: 2026-08-05
description: "Limpieza de almacenamiento en Windows basada en evidencias, con modo de emergencia controlado, medición de ocupación física, análisis forense de procesos y origen, y medidas reversibles contra los llenadores recurrentes de almacenamiento."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: utilities
tags: [windows, storage, cleanup, forensics, onedrive, pagefile, logs]
language: es
status: active
visibility: public
dependencies:
  tools: [powershell]
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: "~/.codex/skills/speicherbereinigung"
  origin_version: null
  origin_repo: null
  last_sync_from_origin: 2026-08-05
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6d44ad70bc2f7abc4086474c001d33a6727d9bb6f9793333d804ad3af4907661
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:53.391636+00:00"
---
<img src="banner.png" width="100%" alt="speicherbereinigung banner">

# Limpieza de almacenamiento

## Propósito y resultado

Esta skill recupera espacio de almacenamiento en Windows de forma controlada y
evita que la misma ruta de llenado vuelva a ocupar el disco de inmediato. Trabaja
en tres fases: liberación de emergencia, análisis forense de la causa y limitación
permanente.

Toda mutación sigue el mismo protocolo:

`Fund -> Entscheidung -> begrenzte Ausführung -> Readback -> Messung` (hallazgo → decisión → ejecución acotada → readback → medición)

Si el usuario no indica un objetivo superior, la tarea solo se considera completada
cuando el volumen del sistema vuelve a informar al menos 50 GB de espacio libre
tras la última mutación. El primer umbral de emergencia de 10 GB adicionales solo
pone fin al estado agudo, no a la tarea completa.

## Cuándo activar

Usa esta skill en los siguientes casos:

- disco del sistema con poco espacio o pérdida recurrente de espacio;
- logs, cachés, pagefiles, archivos o compilaciones de tamaño inusualmente grande;
- clones duplicados, generaciones de copias de seguridad o copias locales en la nube;
- eventos de agotamiento de recursos o procesos con un commit que crece rápidamente;
- sospecha de que schedulers, watchers o clientes de sincronización regeneran datos.

## Reglas de seguridad

- Antes de cada mutación, determina el espacio libre, el volumen, el estado de los
  procesos, los bloqueos, los reparse points y la ruta absoluta resuelta del destino.
- En acciones recursivas, comprueba que el destino esté dentro de la raíz
  seleccionada explícitamente. Nunca uses variables o globs como objetivos de
  borrado sin validar.
- No elimines raíces de volumen, de usuario, de repositorio, de nube ni de proyecto.
- Conserva las fuentes activas, el trabajo no confirmado, los secretos, las copias
  de conflicto, los bloqueos ajenos, `.git` y la única copia de
  recuperación.
- Prefiere la papelera, la cuarentena, la compresión o la deshidratación en la nube.
  Un borrado irreversible solo es admisible para un hallazgo exactamente identificado
  y regenerable; documenta ruta, tamaño y recuperación.
- Cambia pagefile, hibernación, servicios o límites de todo el sistema solo con los
  permisos necesarios, con un plan de reversión y con verificación completa posterior.
  `Zugriff
  verweigert` (acceso denegado) no es una medida exitosa.
- Nunca borres objetos de la nube de OneDrive para liberar almacenamiento local.
  La eliminación en la nube y la deshidratación local son operaciones distintas.

## Fase 1: liberación de emergencia

### 1. Línea base

Registra como mínimo:

```powershell
Get-PSDrive -Name C | Select-Object Used, Free
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID, Size, FreeSpace
Get-Process | Sort-Object PrivateMemorySize64 -Descending |
  Select-Object -First 15 Name, Id, PrivateMemorySize64, WorkingSet64
```

Anota la hora, el valor inicial y el objetivo. Distingue `PrivateMemory` o
commit de `WorkingSet`: un proceso puede mostrar poca RAM en su working set
y aun así ocupar mucho pagefile.

### 2. Inventario acotado

Empieza por raíces locales conocidas y ventanas de cambios recientes. No busques
de forma recursiva e indiscriminada en todos los directorios de nube o de usuario.
Son candidatos adecuados:

- cachés de modelos, paquetes y compilación claramente regenerables;
- salidas de compilación antiguas y terminadas;
- logs de aplicación rotables;
- generaciones de archivo o copia de seguridad verificadas;
- copias locales de nube completamente sincronizadas.

La longitud del archivo no equivale a ocupación física en archivos dispersos,
comprimidos o marcadores de nube. Usa la asignación NTFS (`GetCompressedFileSizeW`),
`compact` o una herramienta equivalente, y compara el espacio libre antes
y después.

### 3. Tratar un hallazgo

Procesa exactamente un hallazgo por paso de medición. Después comprueba:

- los bytes realmente recuperados;
- errores, handles abiertos y bloqueos restantes;
- que la fuente protegida siga intacta;
- la posibilidad de recuperación o regeneración;
- si algún proceso lo vuelve a generar de inmediato.

El modo de emergencia solo termina tras demostrar 10 GB adicionales. Después, el
flujo pasa directamente al análisis forense.

## Fase 2: determinar mediante análisis forense los procesos de llenado y su origen

### 1. Agotamiento de recursos y pagefile

Lee las pruebas actuales e históricas en conjunto:

```powershell
Get-CimInstance Win32_ComputerSystem |
  Select-Object AutomaticManagedPagefile
Get-CimInstance Win32_PageFileUsage |
  Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage
Get-WinEvent -FilterHashtable @{LogName='System'; Id=2004} -MaxEvents 20
```

El evento 2004 del Windows Resource Exhaustion Detector incluye los procesos con
mayor commit en el momento del evento. Relaciona PID, nombre del proceso, marca de
tiempo y bytes con los procesos actuales. Un `pagefile.sys` grande no prueba
por sí solo que el archivo sea la causa; lo que se busca es el proceso que provocó
el commit.

### 2. Crecimiento de archivos

Agrupa los archivos nuevos o modificados por:

- hora de creación y de modificación;
- ruta padre y extensión;
- propietario o proceso generador;
- tasa diaria en archivos y en bytes físicamente ocupados.

Presta especial atención a los directorios de logs, cachés, sincronización, copias
de seguridad, compilaciones, descargas y sesiones. Una retención de siete días no
es adecuada si un cliente escribe varios gigabytes al día y el volumen es pequeño.

### 3. Automatizaciones

Revisa el programador de tareas, servicios, watchers e inicio automático en cuanto
a frecuencia, retención y éxito:

```powershell
Get-ScheduledTask | Where-Object State -ne 'Disabled'
Get-ScheduledTaskInfo -TaskName '<task-name>'
```

Verifica por separado la acción, el disparador, el intervalo de repetición, el
último código de retorno y la siguiente ejecución. Que exista una tarea no demuestra
que la retención o la frecuencia controlen el crecimiento real.

## Fase 3: limitación permanente

Elige la medida reversible más pequeña que sea eficaz:

- ejecutar la rotación de logs con más frecuencia y, además, establecer un límite de tamaño;
- reiniciar de forma controlada un cliente que llame la atención y medir su commit;
- limitar el scrollback del terminal o el logging de depuración a un valor razonable;
- eliminar cachés antiguas y regenerables y observar si se vuelven a crear;
- deshidratar contenido verificado de la nube con «Liberar espacio»;
- ajustar la frecuencia del scheduler y la retención a la tasa diaria empírica;
- hacer cambios de pagefile o hibernación solo de forma administrativa, con plan de reinicio y reversión.

Por ejemplo, para Windows Terminal, un scrollback estándar limitado podría tener
este aspecto:

```json
{
  "profiles": {
    "defaults": {
      "historySize": 2000
    }
  }
}
```

Conserva los ajustes existentes y valida el archivo JSON después del cambio.

### Control específico de OneDrive

Antes de deshidratar, deben haberse comprobado el estado de sincronización y las
cargas pendientes. Usa un gestor de archivos compatible con filtros de nube o el
comando del Explorador «Liberar espacio». La deshidratación no debe eliminar el
contenido de la nube.

Revisa por separado el área local de logs de OneDrive en
`$env:LOCALAPPDATA\Microsoft\OneDrive\logs`. Si un subárea genera gigabytes al día, combina una retención
basada en tiempo con un límite máximo de tamaño y una ejecución programada con
suficiente frecuencia. Protege los archivos muy recientes o abiertos y comprueba,
tras la ejecución, tanto el estado de la tarea como el tamaño restante.

## Verificación final e informe

Tras la última mutación:

1. Espera a que terminen las operaciones asíncronas de nube o de borrado.
2. Vuelve a leer el espacio libre y el commit de los procesos.
3. Comprueba mediante readback las configuraciones modificadas, las tareas y los tamaños de los logs.
4. Ejecuta una prueba breve: ¿vuelve a generarse un exceso de almacenamiento dentro de la ventana de observación?
5. Informa del valor inicial, de cada hallazgo y su decisión, de los bytes recuperados físicamente, de los procesos de llenado, de los ajustes permanentes, de las reversiones, de los riesgos residuales y del valor final.

No afirmes una limpieza, una limitación de procesos o el logro de los 50 GB sin un
readback actual y adecuado.

## Límites conocidos

- Sin derechos administrativos, los cambios de pagefile, hibernación o servicios
  pueden seguir bloqueados. Documenta el paso exacto pendiente.
- Los eventos históricos de procesos demuestran un llenador anterior; para la
  situación actual también se necesitan datos de procesos y del crecimiento de archivos.
- Un concepto de copia de seguridad planificado no equivale a una copia de seguridad. La transferencia
  o el borrado requieren identidad actual del destino, manifiesto o hash, prueba de
  restauración y montaje.
- Si la titularidad no está clara, hay trabajo ajeno en curso o el destino es
  desconocido, aplica la decisión `nichts` (no hacer nada).

## Registro de cambios

### 1.0.0 (2026-08-05)

- Versión inicial portable para la biblioteca central de skills.
- Añadido el análisis forense de agotamiento de recursos, pagefile y procesos.
- Separadas con claridad la ocupación física NTFS y la deshidratación de OneDrive.
- Incorporada la rotación de logs de OneDrive con límite de tiempo y de tamaño.
- Definidas puertas estrictas de emergencia y de cierre con readback.
