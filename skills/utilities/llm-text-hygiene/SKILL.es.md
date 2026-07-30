---
language: es
description: Eliminar artefactos de IA, residuos de chat, marcadores de posición y patrones de estilo LLM de textos finales, y auditar divulgaciones de IA.
---

> **Español** — Versión oficial en español de `llm-text-hygiene`.

<img src="banner.png" width="100%" alt="llm-text-hygiene banner">

# LLM-Text-Hygiene — Eliminar residuos de IA de textos terminados

## Descripción general y propósito

Los textos creados con la ayuda de la IA acumulan residuos que permanecen invisibles en el borrador y solo resultan vergonzosos en el documento publicado: fragmentos de conversación de la sesión de chat, instrucciones de dirección que se salen de la estructura argumentativa, agradecimientos al modelo de lenguaje, marcadores de posición no resueltos, patrones de estilo insistentes de LLM —y una divulgación de IA (AI disclosure) que falta, está mal ubicada o ya no es cierta. Esta habilidad es el pase de limpieza sistemático previo a la publicación: inspeccionar, limpiar de forma conservadora y corregir la divulgación. **Nunca cambia la sustancia** —elimina aquello que no forma parte de la obra.

## Catálogo de comprobación (Auditoría)

Cinco clases de hallazgos, desde inequívocos (corregir directamente) hasta delicados (solo marcar):

### 1. Residuos de chat e instrucciones de dirección (inequívocos → eliminar/reparar)

Frases que pertenecen a la CREACIÓN del texto, no al texto en sí: "Como se habló, dejamos esta parte en el artículo porque...", "Aquí está la sección revisada:", "Con gusto me gustaría añadir...", fragmentos de prompt sobrantes, metacomentarios al cliente/solicitante.
**Principio de detección:** La frase se sale de la estructura del texto y de la argumentación —se dirige a una situación de conversación en lugar de al lector. Al eliminar, comprobar si se debe salvar algún núcleo sustancial (transferir la explicación a una nota al pie/texto principal).

### 2. Marcadores de posición y notas de trabajo en curso (inequívocos → resolver)

`[TODO: …]`, `[insertar referencia]`, `XXX`, `<ejemplo aquí>`, secciones vacías con encabezado, "(¿fuente?)". Resolver o —si no es posible resolverlo— transferir como tareas pendientes reales al TODO del proyecto y eliminar del entregable.

### 3. Agradecimientos a LLM y expresiones antropomórficas (inequívocos → eliminar)

Agradecer a ChatGPT/Claude/Gemini & Co. no pertenece a la sección de agradecimientos —no se da las gracias a las herramientas, su uso se declara en la divulgación de IA. Asimismo, eliminar formulaciones antropomórficas sobre la herramienta ("la IA amablemente sugirió").

### 4. Divulgación de IA (AI Disclosure) (comprobar → corregir)

- **¿Presente?** Si el documento se creó con la ayuda de IA y el medio/proyecto exige o prevé una divulgación: ¿existe la sección?
- **¿Correcta?** ¿Describe el uso real (ni infravalorado ni exagerado)? ¿Utiliza el esquema de divulgación del proyecto/medio si está definido (p. ej., niveles graduados)?
- **¿Bien ubicada?** En el lugar habitual del medio (métodos/entorno de agradecimientos/sección dedicada), idéntica en todas las versiones lingüísticas.

### 5. Patrones de estilo LLM (delicados → corregir solo casos claros, marcar el resto)

Transiciones formularias ("En resumen se puede decir", "Es importante destacar"), inflación de viñetas donde corresponde texto corrido, cadenas de "no solo... sino también", densidad de guiones largos, frases de cobertura (hedging), y en inglés los marcadores conocidos (entre otros "delve", "tapestry", "it's worth noting"). **Precaución:** El estilo es territorio del autor —suavizar solo la formularidad inequívoca; presentar todo lo demás como lista de hallazgos al autor en lugar de reescribir el texto. Un texto de sonido humano no es el objetivo de esta habilidad; el objetivo es un texto libre de cuerpos extraños.

## Flujo de trabajo

1. **Aclarar el alcance:** ¿Qué entregables (archivos), qué versiones lingüísticas? Aplicar los cambios SIEMPRE de forma sincrónica en todas las versiones (cotejo: `bilingual-doc-sync`).
2. **Escaneo mecánico:** Búsqueda de texto completo según patrones de señal (tabla siguiente) —económico, encuentra de forma fiable las clases 2/3 y partes de la clase 1.
3. **Pase de lectura:** Leer el documento a lo largo de la estructura argumentativa —los hallazgos de clase 1 solo se reconocen estructuralmente (la frase se dirige a la conversación en lugar de al lector). Comprobar especialmente: inicio/final de secciones, agradecimientos, introducción/conclusión (los residuos suelen terminar allí).
4. **Limpieza:** Corregir directamente las clases 1–3 (de forma conservadora, preservando la sustancia), corregir la clase 4, emitir la clase 5 como lista de hallazgos; suavizar directamente solo casos inequívocos.
5. **Documentar:** Registrar lo encontrado/modificado/marcado —en trabajos con obligación de versionado, anotar si se requiere una nueva versión/re-subida.
6. **Pase periódico sobre un repositorio:** Combinar con `rotation-check` (un documento/proyecto por ejecución, registro como memoria).

## Patrones de señal para el escaneo mecánico

| Clase | Patrón de búsqueda (DE) | Patrón de búsqueda (EN) |
| --- | --- | --- |
| Residuos de chat | "wie besprochen", "wie gewünscht", "hier ist", "gerne", "im Chat", "wie du sagtest", "lassen wir" | "as discussed", "as requested", "here is the", "I have added", "per your" |
| Marcadores de posición | `TODO`, `XXX`, `[…einfügen]`, `<…>`, "Quelle?" | `TBD`, `[insert`, `placeholder`, `citation needed` |
| Gracias a LLM | "Dank an ChatGPT/Claude/Gemini", "mithilfe von KI erstellt" (fuera de la divulgación) | "thanks to ChatGPT/Claude", "grateful to the AI" |
| Marcadores de estilo | "zusammenfassend lässt sich", "es ist wichtig zu betonen", "nicht nur … sondern auch" | "delve", "tapestry", "it's worth noting", "in conclusion" |

La tabla es un punto de partida, no un sustituto del filtro: los patrones proporcionan candidatos, la decisión se toma en contexto (pasos 3–4). Para la higiene de caracteres puramente mecánica (escaneo de emojis, caracteres de control, umlaute rotos), utilizar herramientas existentes —los daños de codificación son territorio de `encoding-fix`, no de esta habilidad.

## Ejemplo y aplicación

```text
Solicitud: "Comprueba el artículo en busca de residuos de IA antes de subirlo."

1. Alcance: paper_de.tex + paper_en.tex.
2. Escaneo: 1× "as discussed" (EN, sección 4), 1× "[TODO: insertar referencia Smith]" (ambos),
   los agradecimientos mencionan "valiosa ayuda de Claude".
3. Pase de lectura: En la introducción, una frase que se dirige directamente al revisor
   ("Tratamos esta objeción como se solicitó en el apartado 3.2") → instrucción de dirección.
4. Soluciones: Instrucción de dirección eliminada (el contenido ya estaba en 3.2), TODO transferido como tarea
   a TODO.md + marcador eliminado, agradecimiento a LLM eliminado, en su lugar
   sección de divulgación de IA precisada sobre el uso real —todo en DE y EN.
5. Nota: Cambio sustancial → se requiere nueva versión del artículo, anotado en TODO.md.
```

## Banderas rojas (Red Flags)

| Pensamiento | Realidad |
| --- | --- |
| "Aprovecho para redactar el texto con más fluidez" | La sustancia y la voz pertenecen al autor —la habilidad elimina cuerpos extraños, no pule el estilo. |
| "Marcador de estilo encontrado → eliminar" | La clase 5 se marca, no se reescribe automáticamente; suavizar solo la formularidad inequívoca. |
| "La versión en alemán es suficiente" | Los residuos a menudo están en UNA SOLA versión —comprobar siempre todas las versiones lingüísticas y mantenerlas en sincronía. |
| "Eliminar la divulgación, así queda limpio" | Al revés: eliminar agradecimientos a LLM, incluir la divulgación correcta de IA —ocultar no es higiene. |

## Skills relacionadas

- `encoding-fix` — Reparación de bytes/codificación (mojibake); esta habilidad trabaja a nivel de contenido.
- `bilingual-doc-sync` — Mantenimiento de la sincronización entre versiones lingüísticas donde se aplican las soluciones.
- `rotation-check` — Estructura para ejecuciones periódicas sobre un repositorio de documentos.
- `textproduction` — Generación de texto (esta habilidad es el control de calidad posterior).

## Registro de cambios

### 1.0.0 (2026-07-04)
- Versión inicial. Abstraído de la automatización Codex "research-llm-muster-check"
  (fragmentos de chat en artículos, agradecimientos a LLM, divulgación de IA) y generalizado a cualquier
  texto entregable; catálogo de auditoría ampliado con marcadores de posición, patrones de estilo y tabla de señales de escaneo.