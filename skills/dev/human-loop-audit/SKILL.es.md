---
name: human-loop-audit
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: "Procedimiento interactivo de auditoría en cremallera para una serie de aplicaciones/objetos de prueba: el usuario prueba en vivo y da breve retroalimentación en el chat, el agente ya inicia el siguiente objeto Y evalúa en paralelo la retroalimentación del anterior (registrarla de forma estructurada, delegar de inmediato las órdenes de reparación a un worker) — en lugar de esperar secuencialmente. Usa esta skill con \"human-loop-audit\", \"lass uns die Apps im Reißverschluss durchtesten\", \"ich teste, du wertest aus und reparierst\", o cuando una serie de GUIs/productos deba probarse conjuntamente con el usuario y los hallazgos deban convertirse de inmediato en reparaciones. El cierre es una lista estructurada de hallazgos por objeto (Funciona/Defecto/Deseo) más la lista de reparaciones ya iniciadas."
# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [audit, usertest, human-in-the-loop, gui-test, reissverschluss, delegation, feedback]
language: es
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: b65128841e358d7ba0f7a3892feea4ef776f3b6e3021109bb89010a6243e82d5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:08.758785+00:00"
---
<img src="banner.png" width="100%" alt="human-loop-audit banner">

# Human-Loop-Audit

> **No confundir con `reissverschluss-merge`:** El nombre comparte la imagen de la "cremallera",
> pero `reissverschluss-merge` es un **procedimiento de merge de Git** (fusionar por secciones dos
> ramas de código). `human-loop-audit` aquí no tiene nada que ver con Git — es un **proceso
> de prueba/auditoría con el usuario**. Ambas skills usan la cremallera solo como la misma idea
> básica (unir dos hilos diente a diente, no hilo por hilo, uno tras otro).

## Propósito y reparto de roles

El tiempo del usuario es el **cuello de botella secuencial**: solo él puede manejar una app en
vivo y decir en segundos si se siente bien. Todo lo demás — abrir objetos, registrar la
retroalimentación de forma estructurada, iniciar reparaciones — lo asume el agente, y lo hace
**mientras** el usuario ya está en el siguiente objeto, no después. El agente es operador de
cockpit y evaluador a la vez.

**El núcleo es el solapamiento, no el orden en sí:** un "abrir app → esperar → evaluar → abrir
la siguiente app" puramente secuencial desperdicia el tiempo de espera, durante el cual el
usuario prueba. Human-Loop-Audit aprovecha precisamente esa ventana.

## Flujo

1. **"start"** del usuario → el agente abre el **primer** objeto de prueba. Basta con iniciar
   el proceso (p. ej. `Start-Process <exe>` o el comando de inicio correspondiente del objeto)
   — **no hace falta tomar el escritorio**, el usuario lo maneja él mismo. Confirmar brevemente
   que está abierto.
2. **El usuario prueba y escribe la retroalimentación en el chat** — bastan breves apuntes, sin
   reformular nada que cambie el significado.
3. **En cuanto llega la retroalimentación, se ejecutan dos cosas en paralelo, no una tras otra:**
   - El agente **abre de inmediato el siguiente objeto de prueba**, para que el usuario pueda
     seguir probando sin esperar.
   - **Al mismo tiempo** el agente evalúa la retroalimentación recibida: registrar el hallazgo
     por objeto de forma estructurada (**Funciona** / **Defecto** / **Deseo**, con una breve
     descripción), y ante un defecto o un deseo claro **delegar de inmediato una orden de
     reparación a un worker** (no acumularla para encargarla "más tarde" — la reparación debe
     correr mientras el usuario sigue probando).
4. **Repetir** hasta que todos los objetos estén probados (volver al paso 2/3 para cada objeto
   adicional).
5. **Cierre:** presentar al usuario la lista de hallazgos (por objeto Funciona/Defecto/Deseo) +
   la lista de reparaciones iniciadas (worker/orden/estado).

## Estructura de los hallazgos (por objeto de prueba)

| Objeto | Estado | Hallazgo | Reparación delegada a |
|---|---|---|---|
| `<App/Objekt-Name>` | Funciona / Defecto / Deseo | breve apunte, sin cambiar la redacción del usuario | nombre del worker/sesión, si se delegó |

Un objeto puede tener varias filas (varios hallazgos). Nada se resume en silencio — el cierre
se lee de esta tabla, no de la memoria.

## Delimitación frente a skills relacionadas

- **`reissverschluss-merge`** (ver nota arriba) — procedimiento de merge de Git puro, sin solapamiento
  de contenido a pesar de la imagen de nombre común.
- Ciclos de prueba por oleadas/envíos a tienda, más estrechos y con fases adicionales fijas
  (revisión de assets, hojas de envío, reescritura de IDs) y **ejecución secuencial** ("la
  implementación de los puntos se hace por separado"), existen como procedimientos locales del
  proyecto. `human-loop-audit` es deliberadamente el flujo **genérico** para **cualquier**
  serie de apps/GUIs y delega las reparaciones **de inmediato y en paralelo**, no como un paso
  posterior separado.
- **`bugsweep` / `bugfix-protocol`** — el trabajo de reparación real, al que delega
  `human-loop-audit`; esta skill en sí no repara.

## Errores frecuentes

- **No esperar a la evaluación antes de abrir el siguiente objeto** — un "esperar, evaluar,
  luego abrir el siguiente" puramente secuencial desperdicia exactamente el solapamiento que
  define esta skill.
- **Registrar la retroalimentación de inmediato de forma estructurada**, no acumularla en el
  historial del chat — si la sesión se corta, se perdería.
- **No iniciar objetos a ciegas** si se sabe que un objeto es inestable — comprobar brevemente
  que arranca antes de que el usuario se siente frente a él en vivo.
- **Delegar de inmediato, no al final en bloque** — si no, la reparación empieza cuando el
  usuario ya terminó de probar y se pierde la ventaja de tiempo del procedimiento.

## Ejemplos de activación

- "human-loop-audit"
- "Lass uns die Apps im Reißverschluss durchtesten."
- "Ich teste, du wertest aus und reparierst."
- "start" (tras haber anunciado previamente un Human-Loop-Audit, como señal de inicio del paso 1)

## Registro de cambios

### 1.0.0 (2026-08-18)
- Versión inicial. Procedimiento tomado de una definición del usuario del 2026-08-18:
  auditoría en cremallera con evaluación paralela + delegación inmediata de reparaciones,
  delimitada frente a `reissverschluss-merge` (merge de Git, misma imagen de nombre, sin relación)
  y frente a ciclos de prueba por oleadas más estrechos, locales al proyecto (ejecución secuencial
  en lugar de paralela).
