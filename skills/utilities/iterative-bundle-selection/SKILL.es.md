---
name: iterative-bundle-selection
version: 1.2.0
type: skill
author: Lukas Geiger
created: 2026-08-25
updated: 2026-08-25
description: "Reducir listas grandes de candidatos de forma progresiva mediante charcos temáticos opcionales, etapas de filtrado y lotes que se vuelven a mezclar repetidamente. Úsese cuando el usuario quiera seleccionar habilidades, tareas, ideas, archivos u otras entradas por grupos, filtrarlas según características o mezclarlas solo dentro de ámbitos temáticos comunes, sin descartar definitivamente las entradas restantes."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, auswahl, datenreduktion, buendel, choice-overload, workflow]
language: es
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'local_changes_since_sync': True}
translated_from_sha256: 947358cbebcf01dc7e4e4d15c4cf25da6fe10d5454a7e8fc0aa03788bf88f70f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.674908+00:00"
---
<img src="banner.png" width="100%" alt="iterative-bundle-selection banner">

# Selección iterativa por lotes

Reducir conjuntos grandes de opciones con pocas decisiones gruesas, sin descartar prematuramente los candidatos no elegidos.

## Principio básico

1. Registrar todos los candidatos como un grupo común y nombrarlos de forma inequívoca.
2. Opcionalmente, definir charcos temáticos y asignar cada candidato a exactamente un charco principal.
3. Aplicar los filtros deseados uno tras otro, de forma global o dentro de charcos concretos, y conservar sus coincidencias por separado.
4. Mezclar dentro de cada charco activo y formar, por defecto, lotes de cinco candidatos.
5. Etiquetar los lotes de la primera ronda de forma inequívoca por charco con `THEMA-A`, `THEMA-B` …
6. Dejar que el usuario seleccione lotes completos.
7. Retirar los candidatos de los lotes seleccionados del grupo abierto y enviarlos a la siguiente acción.
8. Devolver los candidatos de los lotes no elegidos a su charco correspondiente.
9. Mantener charcos y filtros, volver a mezclar cada charco por separado y usar etiquetas con guiones.
10. Continuar con más rondas hasta que el usuario se detenga o el grupo quede vacío.

Un último lote puede contener menos de cinco candidatos. Los lotes no elegidos significan "todavía abierto", no "rechazado".

## Flujo de trabajo

### 1. Preparar el grupo

- Eliminar duplicados mediante nombres o identificadores estables.
- Excluir los candidatos ya seleccionados o completados.
- Marcar los candidatos bloqueados, pero no borrarlos silenciosamente.
- Indicar el tamaño del grupo inicial.

### 2. Formar charcos temáticos

Un charco temático es un subgrupo delimitado. Los candidatos de charcos distintos no se mezclan entre sí.

- Usar este método solo si el usuario lo pide o si una separación temática es claramente útil.
- Documentar cada charco con ID estable, título, regla de asignación y número de candidatos.
- Derivar los charcos de las indicaciones del usuario, de categorías existentes o de características verificables.
- Mostrar de forma transparente las asignaciones derivadas automáticamente antes de la primera acción siguiente.
- Asignar, por defecto, cada candidato a exactamente un charco principal; no generar duplicados silenciosos en varios charcos.
- Mantener los candidatos ambiguos en `UNZU — Unzugeordnet` hasta que se establezca una asignación.
- Emitir un charco con menos de cinco candidatos como lote pequeño; nunca completarlo con otro tema.
- Los filtros pueden aplicarse globalmente a todos los charcos o localmente a un charco nombrado.
- Los candidatos filtrados conservan su asignación de charco para volver al lugar correcto al reactivarse.
- Al dividir, fusionar o renombrar un charco, descartar y reformar solo sus lotes afectados.

Ejemplo:

```text
DEV  | Entwicklung     | 12 Kandidaten | DEV-A, DEV-B, DEV-C
MED  | Medien          |  7 Kandidaten | MED-A, MED-B
UNZU | Unzugeordnet    |  2 Kandidaten | UNZU-A
```

En rondas posteriores, indicar la profundidad de la ronda con la letra del lote: `DEV-A′`, `MED-B″`.

### 3. Aplicar etapas de filtrado

- Ejecutar los filtros de forma opcional y en el orden que indique el usuario.
- Registrar cada filtro con ID estable, modo, regla y número de coincidencias.
- Realizar las comparaciones de texto sin distinguir mayúsculas y minúsculas por defecto.
- `exclude` retira las coincidencias solo del grupo activo y las deposita en el grupo filtrado.
- `include` conserva solo las coincidencias en el grupo activo; las no coincidencias pasan al grupo filtrado.
- Si falta una indicación de modo y el usuario dice que el grupo debe filtrarse o depurarse, usar `exclude` y declarar esta suposición.
- Tras cada etapa, indicar el tamaño de entrada, el número de coincidencias y el tamaño restante.
- Nunca borrar ni marcar como rechazados los candidatos filtrados; el usuario puede desactivar filtros individuales más adelante.

Ejemplo:

```text
F1 | exclude | Name enthält "aws"         | 13 Treffer
F2 | exclude | Name enthält "hyperframes" | 8 Treffer
Aktiver Pool: 44 | Filterpool: 21
```

Si cambia un filtro, descartar todos los lotes previos del grupo activo y solo después volver a mezclar.

### 4. Formar la ronda

- Mezclar realmente los candidatos; no basta con renombrar la estructura de lotes anterior.
- Usar, siempre que sea posible, cinco candidatos por lote.
- Mezclar entre sí solo candidatos del mismo charco temático.
- No duplicar ni perder candidatos.
- Si hay candidatos con dependencias funcionales, marcar la dependencia en lugar de ocultarla.

Formato de salida:

```text
Bündel DEV-A: dev-1, dev-2, dev-3, dev-4, dev-5
Bündel MED-A: media-1, media-2, media-3
```

Sin charcos temáticos, seguir usando las etiquetas simples `A`, `B`, `C` …

### 5. Procesar la selección

- Aceptar respuestas como `A, D und F`.
- Antes de una acción siguiente, volver a nombrar completamente los candidatos incluidos.
- Comprobar por candidato los bloqueos, requisitos o simulaciones (dry-runs) necesarios.
- Registrar como seleccionados o completados los candidatos que tuvieron éxito.
- Devolver al grupo restante los candidatos bloqueados o fallidos.

### 6. Reagrupar el grupo restante

- Eliminar de forma permanente solo los candidatos realmente exitosos.
- Devolver todos los demás candidatos a sus charcos anteriores y volver a mezclarlos allí por separado.
- Volver a aplicar los filtros activos al grupo restante antes de cada nueva mezcla.
- Marcar la siguiente ronda con etiquetas con guiones: `DEV-A′`, después `DEV-A″`, etc.
- Indicar el grupo total, el grupo filtrado, el tamaño del grupo activo y el tamaño de cada charco.

## Reglas de protección

- No interpretar nunca la no selección como un rechazo definitivo.
- No descartar nunca en silencio las coincidencias de filtro; permanecen recuperables en el grupo filtrado.
- No cruzar nunca los límites de los charcos al mezclar.
- No duplicar ni trasladar candidatos entre charcos al redistribuirlos, salvo que el usuario cambie la división.
- No perder candidatos por una combinación desfavorable de lotes.
- No forzar candidatos bloqueados; permanecen abiertos.
- En acciones siguientes irreversibles o de alto riesgo, pedir confirmación de cada candidato individualmente.
- Si es necesario, documentar una clave de mezcla reproducible; en caso contrario, basta una distribución nueva y trazable.
- El método reduce la complejidad de la selección, pero no sustituye la valoración técnica de cada candidato.

## Delimitación

- `decide` evalúa una decisión concreta con criterios y marcos de análisis.
- `decision-briefing` coordina varias cuestiones de decisión distintas.
- `iterative-bundle-selection` reduce un grupo grande de candidatos homogéneos mediante elección repetida por grupos y nueva mezcla.

## Cierre

El procedimiento termina cuando el grupo está vacío, el usuario se detiene explícitamente o solo quedan candidatos que requieren una decisión individual. Entonces, emitir un breve balance con seleccionados, abiertos y bloqueados.

## Registro de cambios

### 1.2.0 (2026-08-25)

- Se añadieron charcos temáticos opcionales como divisores del grupo.
- Se establecieron la mezcla ligada a charcos, los filtros locales, las etiquetas inequívocas de lotes y el tratamiento de `UNZU`.

### 1.1.0 (2026-08-25)

- Se añadieron etapas de filtrado reversibles `include` y `exclude` antes de la nueva mezcla.
- Se establecieron el registro de filtros, el grupo filtrado y el recálculo de lotes existentes.

### 1.0.0 (2026-08-25)

- Lotes iterativos de cinco, rondas con guiones, grupo restante y devolución de bloqueados quedaron registrados como un procedimiento independiente de reducción de datos y decisión.
