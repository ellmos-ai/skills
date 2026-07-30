---
language: es
---

> **Español** — Versión oficial en español de `load-project`.

# Cargar Proyecto (Español)

## Descripción general y propósito

Utiliza esta habilidad al comienzo de una tarea de proyecto específica o cuando el contexto de trabajo se haya vuelto confuso. El objetivo no es realizar una auditoría completa del repositorio, sino obtener el contexto mínimo fiable para continuar trabajando de forma segura.

## Configuración

La habilidad no requiere nombres de directorio fijos. Las instalaciones locales pueden definir opcionalmente los siguientes valores en sus reglas generales de agente o en una configuración local del proyecto:

- raíces de espacio de trabajo conocidas,
- herramientas de archivos preferidas,
- nombres de archivos de arranque o registro adicionales,
- verificadores de bloqueos,
- roles y prioridades específicos del proyecto.

Si falta dicha configuración, la habilidad funcionará exclusivamente con el objetivo especificado y las reglas del proyecto que se encuentren allí.

## Procedimiento

### 1. Resolver objetivo

1. Tomar una ruta explícita, nombre de proyecto o directorio de trabajo actual como punto de partida.
2. Determinar la raíz real del proyecto o repositorio.
3. Delimitar las coincidencias ambiguas según la tarea, los documentos raíz y los límites del repositorio; no adivinar si los objetivos son materialmente diferentes.

### 2. Cargar jerarquía de reglas

Leer del contexto general al específico:

1. reglas globales de agentes y seguridad,
2. reglas de espacio de trabajo o pipeline,
3. reglas del proyecto y del repositorio,
4. instrucciones relativas a la tarea.

Las reglas más específicas se aplican dentro de su alcance; los límites de seguridad y autorización de mayor jerarquía se mantienen vigentes.

### 3. Leer documentos raíz según sus roles

Los nombres de archivos son pistas, no una norma fija. Busca específicamente documentos con estos roles:

| Rol | Contenido típico |
|---|---|
| Entrada | Propósito, navegación, instrucciones de inicio |
| Reglas | Modo de trabajo, idioma, seguridad, convenciones |
| Arquitectura | Componentes, flujo de datos, límites |
| Estado | Estado actual, problemas abiertos, última verificación |
| Tareas | Próximo trabajo priorizado |
| Registro | Proyectos canónicos, comprobaciones o publicaciones |
| Evidencia | Pruebas, registros de auditoría, notas de evidencia |
| Entrega | Trabajo en curso, cambios de terceros, siguiente paso |

Cargar únicamente los roles relevantes para la tarea concreta.

### 4. Seguir referencias vinculantes

Si una regla leída señala expresamente otros archivos como lectura obligatoria, cargarlos de forma específica. Finalizar las cadenas de referencia en cuanto no aporten más contexto vinculante para la tarea.

### 5. Verificar estado y bloqueos

- Verificar los bloqueos según la directiva local en cuanto a propietario, alcance, marca de tiempo y criterio de validez; sin una regla de obsolescencia definida, nunca declarar un bloqueo como obsoleto por iniciativa propia,
- Estado del control de versiones y cambios de terceros,
- Procesos en ejecución o puntos de control, si corresponde,
- Actualidad de registros, pruebas e informes de estado.

Guardar el estado inicial de las áreas afectadas como línea base de estado/diff antes de realizar cambios. Si los cambios existentes no pueden asignarse con certeza, se considerarán de terceros por precaución y no se tocarán.

Tratar las capturas de estado como temporales y volver a verificarlas antes de realizar acciones de riesgo.

### 6. Elaborar informe de situación

Registrar brevemente antes de la implementación:

```text
Ziel:
Projekt-Root:
Geltende Regeln:
Evidenzquellen:
Snapshot-Zeitpunkt:
Relevanter Ist-Zustand:
Locks oder fremde Änderungen:
Erfolgskriterium:
Nächster sicherer Schritt:
```

Indicar las fuentes solo con la precisión necesaria para su verificabilidad. Redactar secretos, datos personales y contenidos confidenciales; no copiarlos en el informe de situación.

Si la tarea queda clara y autorizada con ello, continuar directamente con la ejecución.

## Límites

- No realizar búsquedas amplias e ilimitadas de archivos por defecto.
- No reinventar reglas o registros faltantes.
- No tratar informes de estado antiguos como evidencia actual.
- No sobrescribir cambios de terceros.
- No realizar un proceso de integración (onboarding) del proyecto cuando solo se deba cargar contexto para una tarea específica.

## Historial de cambios

### 1.1.0 (2026-07-28)
- Vinculaciones fijas de usuario, espacio de trabajo, herramientas y proveedores eliminadas.
- Introducida la detección de documentos basada en roles y la configuración local opcional.
- Operativa la validez de bloqueos, procedencia del árbol modificado (dirty tree), evidencias de captura e informes de situación redactados.

### 1.0.0 (2026-06-17)
- Versión local inicial.