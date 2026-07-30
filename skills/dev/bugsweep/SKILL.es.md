---
name: bugsweep
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-06-13
description: Búsqueda sistemática de errores con un valor objetivo escalado según la base de código, escalado por duplicación, seguimiento de áreas y verificación final. Usar en /bugsweep o cuando el usuario solicite un pase de depuración sistemático.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="bugsweep banner">
> **Español** — Versión oficial en español de `bugsweep`.

# /bugsweep — Flujo de trabajo sistemático de depuración (Español)

Caza de errores iterativa con un criterio de parada convergente. Escala con la base de código, se escala si la búsqueda parece superficial y evita la repetición mediante el seguimiento de áreas.

## 1. Calcular la tasa base

```
LOC = líneas de código fuente productivo (src/, lib/ — excluyendo pruebas, configuraciones, docs, generado)
x = max(1, ceil(LOC / 1500))
tasa_base = x * 3
```

| LOC | x | Tasa base |
|-----|---|-----------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

Informe al usuario: "Base de código: {LOC} LOC → tasa base = {tasa_base} pases de búsqueda limpios."

## 2. Bucle de búsqueda

```
contador = 0
objetivo = tasa_base
algun_error_encontrado = False
verificados = []  # (nombre_area, tipo: code|task)

BUCLE:
  area = seleccionar_nueva_area()  # ver reglas de área
  verificados.append(area)

  Realizar una búsqueda exhaustiva de errores

  SI se encuentra un error:
    algun_error_encontrado = True
    Corregir siguiendo bugfix-protocol (fases 4+5)
    Revisión: ver regla del modelo (clases de modelo más nuevas: no se requiere revisión externa)
    Commit + push
    contador = 0  # REINICIO
  SINO:
    contador += 1
    Informe: "✓ Limpio: {area} — {contador}/{objetivo}"

  SI contador >= objetivo:
    SI NO algun_error_encontrado:
      # Escalado por duplicación: ni un solo error → ¿búsqueda demasiado superficial?
      objetivo = tasa_base * 2
      algun_error_encontrado = True  # escalar solo UNA VEZ
      Informe: "⚠ Ningún error en {tasa_base} pases → objetivo duplicado a {objetivo}."
      CONTINUAR BUCLE
    SINO:
      IR A verificación final
```

### Notas prácticas sobre el bucle de búsqueda (aprendidas en barridos reales)

- **Repositorios no-git:** Donde no hay `git` (por ejemplo, carpetas de proyectos sincronizadas en la nube), una **copia de seguridad versionada** reemplaza "commit + push": crear `file_<ts>.bak` antes de la primera corrección. **Precaución — la copia de seguridad previa al fix NO es una copia de respaldo de su trabajo:** después del último fix, tome una copia de seguridad `_FINAL_` fresca; de lo contrario, un fallo de sincronización puede borrar toda la sesión de corrección.
- **Muchos errores conocidos desde el principio:** Si ya se conocen N errores al inicio (por ejemplo, de una ejecución anterior), "por error: corregir → revisar → commit → reiniciar" resulta poco práctico. Procese los errores conocidos como UN bloque de corrección (revisión conjunta al final) y comience a contar la tasa base / bucle de búsqueda desde el primer error NUEVO encontrado. La lógica de reinicio sigue aplicándose a los errores recién encontrados durante el barrido.
- **El mismo error en múltiples lugares:** Un defecto encontrado (por ejemplo, una regex incorrecta, una suposición de formato rota) a menudo se copia en otros lugares. Después de cada corrección, busque el mismo patrón en otras ubicaciones; esa es una "área" dedicada muy valiosa.

## 3. Reglas de área (anti-trampas)

Un "área" es un **enfoque de código** o una **tarea** (propósito del código).

### Enfoque de código
- Puede **ampliarse** (más archivos) o **desplazarse** (diferente parte) entre pases
- NO debe ser exactamente la misma selección que en un pase anterior
- CORRECTO: pase 1 = `maintenance.py`, pase 5 = `maintenance.py + orchestrator.py` (ampliado)
- INCORRECTO: pase 1 = `maintenance.py`, pase 5 = `maintenance.py` (idéntico)

### Tarea (propósito)
- Puede hacerse **más granular** (verificar una subfunción) o **más amplia** (funciones relacionadas juntas)
- NO debe ser exactamente la misma tarea
- CORRECTO: pase 1 = "thread safety en el watchdog", pase 5 = "thread safety en todo el tray" (más amplio)
- CORRECTO: pase 1 = "detección de procesos", pase 5 = "coincidencia de marcadores de tienda en la detección de procesos" (más granular)
- INCORRECTO: pase 1 = "thread safety en el watchdog", pase 5 = "thread safety en el watchdog" (idéntico)

### Nombramiento
- El área DEBE ser nombrada ANTES de la búsqueda (sin asignación retroactiva)
- Formato: `"{nombre}" ({tipo}: code|task)`

## 4. Verificación final

Una vez que contador >= objetivo Y algun_error_encontrado:

**Paso A — bugfix-protocol fase 5:**
- [ ] Suite completa de pruebas en verde (`pytest`)
- [ ] **Ejecutar realmente la ruta de ejecución modificada al menos una vez**, no solo las pruebas. Pruebas unitarias en verde sobre código que nunca llama a la ubicación modificada son una falsa seguridad. Ejecute la ruta realmente modificada (ejecución en seco, prueba de humo, invocación por CLI) y verifique tracebacks / firmas / errores de nombres. `py_compile` o una simple importación solo verifica la sintaxis, no si la ruta funciona.
- [ ] **Cada corrección tiene al menos una prueba que la toca:** un fix sin una prueba que active realmente la rama modificada se considera no verificado (para rutas de orquestación/red, combine mock + ejecución en seco si es necesario).
- [ ] Comprobación de tipos (si está configurada)
- [ ] Linteo (si está configurado)
- [ ] Casos límite de las correcciones de la sesión comprobados

**Paso B — revisión (regla del modelo):**
- **Clases de modelos más recientes (ej. Claude 5 / clase Fable):** NO se requiere revisión externa por un asesor o segundo modelo. El Paso A (pruebas + ejecución de humo real) es la verificación. Opcionalmente, ante una incertidumbre genuina: un nuevo subagente de revisión, pero verifique sus hallazgos empíricamente (pruebe contra el código no modificado) antes de contarlos como errores.
  Antecedentes (experiencia de barrido 2026-06-11): el segundo revisor no estaba disponible, el subagente sustituto entregó 1 hallazgo (confianza 85) que una prueba demostró que no era un error; una revisión externa no cambió el resultado.
- **Modelos más antiguos:** discusión de cierre con el asesor (opción de respaldo: un segundo modelo como revisor); el asesor confirma o señala lagunas.

**Si se encuentra un error durante la verificación:**
→ Corregir + probar + commit
→ REINICIO: contador = 0, objetivo = tasa_base (fresco, SIN duplicación)
→ Volver al bucle de búsqueda (la lista de verificados persiste, algun_error_encontrado = True)

**Si la verificación es limpia:**
→ HECHO. Commit + push. Imprimir el protocolo.

## 5. Protocolo (al final)

```markdown
## Resultado de Bug Sweep

- **Base de código:** {LOC} LOC
- **Tasa base:** {tasa_base} (escalado: {objetivo})
- **Áreas verificadas:** {len(verificados)}
- **Errores encontrados:** {cuenta}
- **Reinicios:** {cuenta_reinicios}
- **Duplicación activada:** sí/no
- **Correcciones:**
  - {titulo} — {commit_hash}
  - ...
- **Suite final de pruebas:** {pasaron}/{total} en verde
- **Veredicto de revisión:** autoverificación (clase de modelo reciente) / asesor confirmó / lagunas señaladas
```

## Cuándo usar este flujo de trabajo

- Después del desarrollo de funciones (garantía de calidad)
- Antes de un lanzamiento (barrido de aceptación)
- Periódicamente como control de higiene
- Cuando el usuario escribe `/bugsweep`

## Interacción con otras habilidades

- **bugfix-protocol:** procedimiento de corrección (fases 4+5) para cada error encontrado
- **systematic-debugging:** para errores difíciles de reproducir dentro del barrido
- **code-review:** se puede utilizar como un área de tarea

---

## Historial de cambios

### 1.1.0 (2026-06-13)
- Se adaptó la regla del modelo para el paso B (de la instalación local del skill, estado 2026-06-11): las clases de modelos más recientes se autoverifican mediante pruebas + una ejecución de humo real, sin necesidad de revisión externa; el campo del protocolo "Veredicto de revisión" se amplió en consecuencia.

### 1.0.0 (2026-06-13)
- Primera publicación en la biblioteca de habilidades (adoptada de la instalación local del skill, estado 2026-06-01).