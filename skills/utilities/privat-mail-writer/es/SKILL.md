---
name: privat-mail-writer
version: 0.2.0
type: skill
author: Lukas Geiger + GPT
created: 2026-06-19
updated: 2026-06-19
description: Esta skill debe utilizarse cuando el usuario desee escribir, responder, rechazar, hacer seguimiento, acortar, reformular o redactar correos electrónicos privados o semi-formales en su propio estilo, especialmente para citas, rechazos oficiales, respuestas cortas amables y un tono adaptado al contacto. Iniciar el análisis del perfil solo cuando haya un encargo concreto de redacción de correo.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [mail, email, privat, antwort, absage, termin, schreibstil, kontaktprofil]
language: es
status: active
dependencies: {'tools': [], 'optional_tools': [{'name': 'mail-connector', 'path': '.AI/.MODULES/mail-connector/', 'cli': 'mailc', 'python_module': 'mail_connector.cli', 'usage': 'mailc context <kontakt> --mode reply --json  # Liefert Mail-Kontext als JSON für Profilaufbau', 'note': 'Optionales lokales IMAP-CLI-Tool. Nur nutzen wenn installiert (`pip install -e .` im Modulordner). Ohne dieses Tool arbeitet der Skill ohne Mailzugriff.'}], 'services': ['mail-backend-optional'], 'protocols': ['kontaktprofil', 'usecase-registry'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'None', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `privat-mail-writer`.

# Privat-Mail-Writer (Español)

## Descripción general y propósito

Privat-Mail-Writer crea borradores de correo cortos, amables y adecuados según el contacto. La skill está diseñada de forma neutra para el usuario: no contiene contactos reales, firmas reales ni contenido de correo real.

El núcleo es perezoso (lazy) y empírico: solo cuando el usuario desee escribir un correo concreto a un contacto, se creará o actualizará el perfil para ese contacto específico. No se generan perfiles por adelantado. Si no hay historial de correo disponible, no invente afirmaciones sobre el estilo, sino escriba de forma neutra y corta o pida ejemplos de forma dirigida.

## Recursos

- `CONFIG.md` - preferencias centrales, reglas de tipo "si-entonces", puertas de permisos (permission-gates) e interruptores de lista negra.
- `BLACKLIST.md` - exclusiones para boletines, remitentes del sistema y contactos sin perfil.
- `USECASES.md` - registro de casos de uso y reglas para nuevos casos de uso.
- `SIGNATURES.md` - reglas neutras de firma y fórmulas de despedida.
- `MUSTER-BLOCKS.md` - bloques de texto cortos y reutilizables.
- `kontaktprofile.json` - esquema vacío y neutro para perfiles de contacto. Mantener los perfiles reales solo localmente y de forma austera con los datos.

## Flujo de trabajo

1. **Cargar configuración:** Leer `CONFIG.md`. Si la lista negra está activa, consultar además `BLACKLIST.md`.
2. **Comprobar activador (trigger):** Crear perfil únicamente ante un encargo de redacción concreto para un contacto específico, p. ej. "escribe un correo a mi hermano Simon". No realizar barridos de la bandeja de entrada solo para crear perfiles.
3. **Comprobar lista negra:** Los boletines, correos no-reply, remitentes del sistema y dominios/contactos excluidos no reciben perfil de contacto. En tales casos, responder de forma neutra o no responder.
4. **Identificar la tarea de correo:** Determinar objetivo, destinatario, motivo, brevedad deseada, idioma, tono y datos necesarios.
5. **Determinar el caso de uso (usecase):** Leer `USECASES.md` y seleccionar el caso de uso más adecuado. Si ninguno encaja, crear un nuevo caso de uso reutilizable o hacer una breve pregunta si faltan datos obligatorios.
6. **Comprobar el perfil de contacto:** Para cada destinatario no excluido, buscar un perfil existente en `kontaktprofile.json` o en una copia de perfil privada local.
7. **Crear o actualizar el perfil:** Si no existe un perfil fiable, leer hasta los últimos diez correos relevantes con ese contacto específico desde el backend de correo disponible. Los correos enviados se deben ponderar más que los recibidos para determinar el estilo de redacción.
8. **Guardar evidencia empírica:** Guardar en el perfil de contacto únicamente señales resumidas y comprobables sobre el estilo, la relación y la categoría. No almacenar correos sin procesar, citas largas ni detalles personales innecesarios.
9. **Aplicar puertas de permisos (Permission-Gates):** Antes de enviar, incluir contenido delicado o si faltan datos obligatorios, respetar las puertas definidas en `CONFIG.md`.
10. **Redactar el borrador:** Combinar la estructura del caso de uso, el perfil de contacto y la tarea actual. Imitar el estilo sin inventar una falsa cercanía, compromisos falsos ni motivos no fundamentados.
11. **Entregar el resultado:** De forma predeterminada, mostrar el asunto y el texto del correo. Solo enviar si el usuario ha autorizado explícitamente el envío y se dispone de una herramienta de correo adecuada.

## Perfiles de contacto

Un perfil de contacto no describe a la persona en sí, sino la relación de comunicación observada y el estilo de redacción del titular de la cuenta hacia esa persona.

Los campos del perfil deben mantenerse breves:

- última fecha de contacto
- cantidad y período de los correos evaluados
- saludo y despedida
- trato de tú/usted/formalidad
- longitud de las oraciones y concisión típica
- grado de calidez, franqueza, compromiso
- evaluación de la relación con nivel de confianza
- categoría de contacto, p. ej. `family`, `inner-circle`, `friends`, `colleagues`, `services`, `official`, `unknown`
- fuente de la categoría: declaración del usuario, texto del correo, libreta de direcciones, firma o inferencia
- nivel de evidencia de la categoría: `user-confirmed`, `strong`, `medium`, `weak`
- breves evidencias parafraseadas como "varios correos enviados terminan con 'Un saludo'" o "las respuestas se mantienen por debajo de cinco oraciones"

Comprobar mensualmente si se debe realizar una verificación de antigüedad. Si el mes de la fecha actual difiere de la fecha guardada en `last_age_check`, eliminar los perfiles cuyo `last_contact_at` sea superior a un año y establecer `last_age_check` a la fecha actual. El valor inicial en el JSON neutro es `2026-06-18`.

## Reglas de estilo

- Escribir en corto. Los correos privados rara vez necesitan introducciones largas.
- Mantener la amabilidad, sin dar explicaciones excesivas.
- Mencionar razones reales solo si las indica el usuario o si son seguras según el contexto.
- En rechazos oficiales: cortés, claro, sin discursos de justificación.
- En caso de duda sobre los datos: hacer una pregunta concisa antes de finalizar el borrador.
- Escribir textos en alemán con sus acentos/caracteres correspondientes según el idioma meta.

## Nuevos casos de uso (usecases)

Si una tarea de correo parece reutilizable y aún no está cubierta en `USECASES.md`, añadir el caso de uso:

- ID estable, p. ej. `UC-002`
- Nombre y activadores típicos
- Objetivo del correo
- Datos obligatorios y opcionales
- Longitud estándar y tono
- Plantilla corta o secuencia de bloques
- Preguntas abiertas en caso de que faltan datos obligatorios

Un caso especial único no se inflará como caso de uso. En ese caso, entregar únicamente el borrador actual.

## Formato de salida

Para borradores normales:

```text
Betreff: ...

Sehr geehrte ...

...

Mit freundlichen Grüßen
[Signatur]
```

Si el usuario solo desea texto sin asunto, entregar únicamente el texto del correo. Si tienen sentido varias variantes, ofrecer como máximo dos variantes: "muy corta" y "un poco más cálida".

## Límites

No inventar perfiles de contacto. No copiar innecesariamente detalles confidenciales de correos en la respuesta. No enviar ningún correo sin autorización explícita. No formular compromisos legales, médicos o financieros a menos que el usuario los especifique claramente.

## Historial de cambios

### 0.2.0 (2026-06-19)
- Añadidos `CONFIG.md` y `BLACKLIST.md`.
- Creación de perfiles limitada a encargos concretos de redacción de correo.
- Incluidas categorías de contacto con fuente y nivel de evidencia en el esquema del perfil.

### 0.1.0 (2026-06-19)
- Versión inicial con registro de casos de uso, reglas de firma, bloques de muestra y JSON de perfil de contacto vacío.
