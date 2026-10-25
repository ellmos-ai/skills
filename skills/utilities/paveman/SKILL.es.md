---
name: paveman
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-20
description: "Detecta solicitudes para acortar un archivo de reglas o de memoria (\"acorta mi CLAUDE.md\", \"MEMORY.md es demasiado largo\", \"comprime la documentación sin tocar la parte técnica\", \"este archivo de reglas se corta por el límite de caracteres\") y utiliza para ello el módulo paveman, una herramienta CLI determinista y sin modelo para acortar prosa en archivos Markdown o de texto, con ejecución de prueba como predeterminada, reversión y un validador estricto de protección para rutas, encabezados y código. Usa esta habilidad con frases como \"acorta <Datei>\", \"este archivo es demasiado largo o se corta\", \"shrink this rule file\", \"comprime sin modificar el contenido\" o cuando un archivo de reglas o de memoria alcanza claramente un límite de caracteres o de líneas."
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [kürzen, kompression, regeldatei, gedächtnis, deterministisch, dry-run, rollback, dokumentation]
language: es
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [paveman]
  services: []
  protocols: []
  python: []
  modules: [paveman]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: cb1c7bfcbc7a4592a1df4a844c4e3d2a5f5da3f268d81b246c0ce05024927bc1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.479548+00:00"
---
<img src="banner.png" width="100%" alt="paveman banner">

# Paveman — Acortar archivos de reglas y de memoria de forma determinista

> Envoltorio delgado e independiente del usuario alrededor del módulo `paveman`, provisto por separado.
> La habilidad detecta cuándo la herramienta es adecuada y describe su flujo seguro. No presupone
> una máquina concreta, una ruta de instalación fija ni un perfil personal.

## Cuándo se activa esta habilidad

Los activadores son frases del usuario que quieren acortar un **archivo existente de reglas,
convenciones o memoria** sin alterar su contenido técnico:

- "Acorta `<Datei>`" / "este archivo es demasiado largo" / "se corta en X caracteres o líneas"
- "Comprime la documentación sin tocar la parte técnica ni el código"
- "MEMORY.md o CLAUDE.md se ha vuelto demasiado grande"
- "Haz este archivo de reglas más breve, pero deja el significado intacto"
- Cualquier variante que signifique **acortar un archivo existente**, no **escribir contenido nuevo**
  ni **traducir** (véase la delimitación más abajo)

**No** es esta habilidad:

- **`knappform`**: cambia la forma en que el propio modelo se expresa en la conversación en curso
  (estilo de comunicación del LLM, basado en modelo, sin acceso a archivos). `paveman`, en cambio, modifica
  el contenido de un archivo existente de forma determinista y sin llamada a ningún modelo. Ambos pueden
  coexistir; son técnica y funcionalmente independientes.
- **`bilingual-doc-sync`**: completa versiones lingüísticas que faltan. `paveman` acorta una versión
  y no traduce nada.
- **`llm-text-hygiene`**: elimina rastros de IA o restos de chat de los textos. Su finalidad es distinta
  de acortar.
- Escribir o inventar contenido nuevo: `paveman` solo acorta lo que ya existe.

## Qué puede hacer el módulo

`paveman` es un acortador de prosa determinista y basado en reglas para archivos Markdown y de texto:
sin llamadas a modelos, sin tokens y sin envío por red. La forma de distribución puede variar según el
sistema; lo determinante es la versión del módulo o paquete autorizada en cada caso.

| Indicador | Efecto |
|---|---|
| *(sin indicador)* | **Ejecución de prueba (predeterminada).** Muestra el diff y el ahorro de caracteres, sin escribir nada. |
| `--apply` | Escribe de verdad; antes crea automáticamente una copia de seguridad. |
| `--rollback` | Restaura la última copia de seguridad. |
| `--locker` | Informa de las desviaciones en rutas o encabezados solo como advertencia, en lugar de como error. |
| `--kontext N` | Define el número de líneas de contexto del diff. |

El **validador de protección se ejecuta en cada llamada**. Los bloques de código, las rutas y los
encabezados no pueden modificarse. En el modo predeterminado, una desviación impide la escritura
en lugar de limitarse a notificarla.

## Flujo: siempre en este orden

1. **Primero la ejecución de prueba.** Ejecuta `paveman <Datei>` sin `--apply`. Muestra al usuario el
   ahorro de caracteres, el diff y el estado del validador ("OK" o el mensaje de error concreto).
2. **Escribir solo con autorización expresa.** Solo entonces ejecuta `paveman <Datei> --apply`;
   nunca cambies automáticamente de la ejecución de prueba al modo de escritura.
3. **Menciona `--rollback` antes de escribir.** El usuario debe saber de antemano cómo deshacer un
   resultado no deseado.
4. **Toma en serio los errores del validador.** No uses `--locker` solo para sortear un error.
   Primero comprueba si la desviación es realmente inofensiva; el modo más permisivo requiere una
   decisión consciente del usuario.
5. **Respeta el contenido curado.** Una herramienta basada en reglas no detecta con fiabilidad si una
   formulación es deliberadamente extensa. En caso de duda, revisa con cuidado el diff de la ejecución de prueba.

## Requisito previo: comprobar la disponibilidad del módulo

1. Comprueba con `paveman --help` si la CLI está disponible en el entorno actual.
2. Si falta el comando, localiza la vía de módulo o paquete autorizada para este sistema. No inventes
   una estructura de rutas locales, un nombre de paquete ni un repositorio.
3. Si no se puede resolver ninguna fuente autorizada, informa del requisito previo como un paso de
   configuración aparte, en lugar de ejecutar la habilidad a ciegas o crear un módulo paralelo.
4. Tras una instalación, vuelve a ejecutar primero `paveman --help` y después una ejecución de prueba inofensiva;
   una prueba de escritura real sigue requiriendo autorización.

## Ejemplos

```text
User: „Kürze meine CLAUDE.md, sie wird beim Sessionstart abgeschnitten.“

→ `paveman CLAUDE.md` (Trockenlauf)
→ Ergebnis: „12.400 → 9.800 Zeichen (-21 %), Validator: OK.“
→ Diff zeigen und auf `--rollback` hinweisen.
→ Nutzer bestätigt.
→ `paveman CLAUDE.md --apply`
```

```text
User: „MEMORY.md ist zu voll, kürze sie bitte.“

→ Trockenlauf: „893 → 893 Zeichen, keine Regel griff — der Text ist bereits knapp.“
→ Kein `--apply` empfehlen; den fehlenden Mehrwert ehrlich melden.
```


## Registro de cambios

### 1.0.1 (2026-08-20)

- Se desacopló por completo el envoltorio público de nombres de equipos, rutas locales de checkout,
  datos de instalación, referencias privadas de tickets y resultados de pruebas locales.
- Se añadió un contrato de disponibilidad e instalación independiente del usuario y se corrigieron
  los caracteres alemanes con diéresis.

### 1.0.0 (2026-08-19)

- Primera versión pública del envoltorio con ejecución de prueba, paso de autorización, reversión y
  límites del validador.
- Delimitación frente a `knappform`, `bilingual-doc-sync` y `llm-text-hygiene`.
