---
language: es
---

> **Español** — Versión oficial en español de `headless`.


# Headless (Español)

## Descripción general y propósito

Utilice esta habilidad cuando la persona solicitante desee explícitamente una ejecución autónoma prolongada sin consultas continuas. Este modo aumenta la perseverancia, no las autorizaciones.

Un único elemento no ejecutable no debe detener innecesariamente el trabajo restante seguro e independiente.

## Condiciones iniciales

Registrar antes de comenzar:

- objetivo concreto y criterio de éxito,
- alcance positivo y negativo (qué incluye y qué no),
- presupuestos de tiempo o costes disponibles,
- efectos secundarios permitidos,
- reglas del proyecto, bloqueos y cambios externos,
- ruta o mecanismo para puntos de control (checkpoints),
- opcionalmente, un perfil de decisión local permitido.

Si falta un perfil de decisión, solo se utilizarán reglas explícitas y suposiciones predeterminadas seguras. El tiempo de ejecución (runtime) no debe suplantar la identidad de ninguna persona.

## Niveles de decisión

| Nivel | Base | Comportamiento |
|---|---|---|
| alto | regla explícita o patrón confirmado repetidamente | decidir; ejecutar solo si se cuenta con la autoridad adecuada |
| medio | decisión predeterminada plausible y reversible | decidir, marcar la suposición y continuar de forma segura |
| bajo | novedoso, contradictorio o sin un marco sólido | no adivinar; aplazar o escalar |

La confianza en la decisión y la autoridad para la ejecución son ejes independientes.

## Protocolo de ejecución

1. **Cargar contexto.** Verificar reglas, estado, bloqueos y objetivo.
2. **Descomponer el trabajo.** Marcar paquetes independientes, puntos de decisión y puntos de aprobación. Si se emplean al menos dos trabajadores independientes, aplicar el protocolo de tareas y evidencias de `orchestrator`, si está disponible.
3. **Ejecutar trabajo seguro.** Continuar con los pasos reversibles y autorizados.
4. **Gestionar decisiones.**
   - Con perfil permitido: utilizar el procedimiento de `decision-avatar`.
   - Sin perfil: derivar únicamente a partir de reglas explícitas del proyecto o de la tarea.
5. **Aparcar elementos no ejecutables.** Registrar la decisión o recomendación, pero sin anticipar la ejecución.
6. **Continuar el trabajo independiente.** Un elemento aparcado solo bloquea sus dependencias reales.
7. **Escribir punto de control (checkpoint).** Guardar el objetivo, los pasos completados, la evidencia, las suposiciones, los elementos aparcados y el siguiente paso.
8. **Verificar la finalización.** Verificar los resultados de forma autónoma y agrupar las decisiones pendientes en una lista compacta.

## Registro de decisiones

Registrar para cada suposición no trivial:

```text
ID:
Entscheidung:
Grundlage:
Konfidenz:
Ausgeführt: ja/nein
Evidenz:
Rücknahme oder Korrektur:
```

Las decisiones del agente no deben tratarse posteriormente como declaraciones de la persona solicitante.

## Paradas locales de paquete

Detener y aparcar un paquete individual si requiere nueva autoridad, una acción externa irreversible, reglas poco claras o un conflicto. A continuación, verificar qué otros paquetes dependen realmente de él.

## Condiciones de parada de la ejecución global

La ejecución global solo se detiene si:

- ya no es posible realizar ningún trabajo seguro e independiente,
- una decisión necesaria tiene baja confianza,
- todos los paquetes de trabajo restantes requieren nueva autoridad externa o irreversible,
- un bloqueo, conflicto o riesgo de seguridad afecta a todo el alcance restante,
- se ha alcanzado el presupuesto acordado,
- el estado actual ya no se puede guardar de manera fiable.

## Formato de finalización

```text
Erreicht:
Verifiziert durch:
Annahmen:
Zurückgestellte Entscheidungen:
Nicht ausgeführte Seiteneffekte:
Nächster sinnvoller Schritt:
```

## Registro de cambios

### 1.1.0 (2026-07-28)
- Se eliminaron las vinculaciones personales de avatar, rutas, comandos y proveedores.
- Se separaron la confianza y la autoridad de ejecución.
- Se aclaró la continuación del trabajo independiente y la escalación agrupada.
- Se separaron explícitamente los bloqueos locales de paquete de la parada de la ejecución global.

### 1.0.0 (2026-06-17)
- Versión local inicial.