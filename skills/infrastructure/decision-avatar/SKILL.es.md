---
language: es
---

> **Español** — Versión oficial en español de `decision-avatar`.

# Decision Avatar

## Descripción general y propósito

Esta habilidad no imita a una persona. Proporciona un procedimiento verificable para derivar una preferencia probable en tipos de decisión recurrentes a partir de evidencias reales y autorizadas.

Utilízala solo si existe un perfil de decisión local y su uso está permitido para la tarea actual. Sin perfil, la habilidad no proporciona ninguna decisión por delegación.

El uso solo se considera autorizado si el encargo, las reglas de agente vigentes o los metadatos del perfil permiten expresamente el propósito actual. La mera accesibilidad de un archivo de perfil no constituye consentimiento.

## Principios fundamentales

1. **Evidencia sobre suposición.** Las declaraciones directas y las decisiones confirmadas tienen más peso que los patrones derivados.
2. **La predicción no es una declaración de la persona.** Los resultados del agente no deben volver al perfil como nuevas evidencias primarias.
3. **Decidir no es ejecutar.** Una recomendación puede ser firme aunque su implementación requiera autoridad adicional.
4. **El consentimiento silencioso no es retroalimentación.** La falta de objeción no confirma una predicción.
5. **Los perfiles permanecen locales y privados.** No transferir datos personales, secretos o contenido confidencial a archivos de habilidades compartidos.

## Modelo de perfil portable

Los nombres de archivo son libremente configurables; solo se requieren estas funciones:

| Función | Contenido |
|---|---|
| Metodología | Niveles de evidencia, privacidad de datos y reglas de calibración |
| Preferencias evidenciadas | Declaraciones directas y decisiones confirmadas |
| Hipótesis | Reglas derivadas con confianza y fuentes |
| Acciones | Acciones tomadas en función de una predicción |
| Retroalimentación | Confirmación, corrección o rechazo por parte de la persona |

Las decisiones más recientes relacionadas con el proyecto tienen prioridad sobre las preferencias generales.

Cada evidencia evaluada debe contener como mínimo:

```text
Quellen-ID:
Datum:
Entscheidungstyp und Gültigkeitsbereich:
Status: bestätigt/korrigiert/widerrufen
Gültig bis: <optional>
```

No utilizar evidencias revocadas, expiradas o fuera de su ámbito de validez. En caso de evidencias confirmadas contradictorias, prevalece primero la más específica y luego la más reciente. Si el conflicto persiste, establecer la confianza en "baja" y escalar.

## Bucle de decisión

### 0. Verificar la regla de prioridad local

Si existe una regla confirmada para el proyecto actual o el tipo de decisión concreto, utilízala y documenta su fuente.

### 1. Buscar evidencia real

Utilizar solo evidencias permitidas según la metodología local. Las listas de tareas, registros de agentes, respuestas anteriores del avatar y argumentos de la sesión actual no son declaraciones de la persona.

### 2. Formular la predicción

Emitir siempre el resultado con una justificación y uno de los tres niveles de confianza:

- **alta:** múltiples evidencias directas, coherentes y relevantes,
- **media:** patrón plausible con evidencia limitada o indirecta,
- **baja:** situación novedosa, evidencias contradictorias o ausencia de un patrón sólido.

Las decisiones con grandes consecuencias no son automáticamente de confianza "baja". La confianza mide la evidencia a favor de la preferencia, no el alcance de la ejecución posterior.

### 3. Separar modos

| Modo | Resultado | Efecto secundario |
|---|---|---|
| Predecir | Posición probable + evidencias + confianza | Ninguno |
| Decidir | Elección concreta + justificación + confianza | Ninguno |
| Actuar | Implementación autorizada y segura + registro de acciones | Posible |

En el modo de acción, se aplican además las reglas de autoridad y seguridad del entorno de ejecución (runtime). Una confianza baja o la falta de autorización de ejecución conduce a la escalación, no a la ejecución silenciosa.

### 4. Calibrar la retroalimentación

Tras recibir retroalimentación real:

1. Marcar la predicción como confirmada, corregida o rechazada.
2. Opcionalmente, registrar una escala de valoración.
3. Registrar la diferencia entre error de dirección y error de encuadre.
4. Ajustar la hipótesis y la confianza.
5. Transferir únicamente la retroalimentación real a las preferencias evidenciadas.

## Formato de salida

```text
Entscheidungstyp:
Modus:
Wahrscheinliche Präferenz:
Konfidenz:
Zulässige Belege:
Gegenbelege oder Unsicherheit:
Ausführung autorisiert: ja/nein
Nächster Schritt:
```

En las salidas, incluir únicamente IDs de origen redactados y el resumen de evidencias necesario para la decisión. No reproducir declaraciones privadas, rutas absolutas de perfiles ni datos confidenciales sin procesar.

## Limitaciones

- Sin diagnósticos ni afirmaciones sobre los estados internos de una persona.
- Sin uso de un perfil fuera de su propósito permitido.
- Sin adopción automática de las suposiciones del agente como conocimiento personal.
- Sin ejecución basada únicamente en una predicción si para ello se requiriera nueva autoridad.

## Historial de cambios

### 1.0.0 (2026-07-28)
- Extracción de la precognición de retroalimentación, la calibración de confianza y la separación de procedencia desde una configuración de avatar personal como un protocolo independiente y portable.
- Operacionalización de la autorización, el ciclo de vida de las evidencias, la resolución de conflictos y la salida redactada.