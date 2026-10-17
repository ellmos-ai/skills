---
name: piggyback-hosting
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-02
updated: 2026-08-07
description: "Patrón de alojamiento para alojar de forma segura una aplicación construida localmente (base de datos propia, API key propia, estado en el proceso) sin construir gestión de usuarios. Rasgo central: el host no guarda nada, el navegador del visitante guarda todo, de modo que las cuentas por visitante, las comprobaciones de acceso y los plazos de borrado dejan de ser necesarios en lugar de tener que resolverse. Úselo cuando una aplicación construida localmente deba alojarse para varios visitantes, ante \"hazlo alojable sin login\", \"no construir cuentas de usuario\", \"reducir la política de privacidad de una herramienta alojada\", \"quién es responsable si no guardamos nada\" o al elegir/implementar un modo servidor (`local`, `huckepack-gift`, `huckepack-only-host`, `pay-membership`). Incluye una plantilla de plan de flujo de datos, una plantilla de privacidad y una evaluación jurídica preliminar (RGPD/TDDDG/UWG, en alemán) como referencias."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [hosting, privacy, gdpr, dsgvo, byok, client-side-storage, deployment, no-login]
language: es
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
translated_from_sha256: e4e1a66b0d6e62ff17a5a883b8eef0ca1f59b984e64d8d29030b76b4ffbcebda
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="piggyback-hosting banner">

# piggyback-hosting

**Un patrón de alojamiento para aplicaciones que, desde el diseño, nunca
aceptan datos ajenos.**

> Plano surgido el 2026-08-02 durante la construcción de tres agentes de
> llamadas. Reutilizable para cualquier aplicación diseñada para un único
> usuario local, pero que también deba poder alojarse para otros.

## Sobre el nombre

En inglés este patrón se llama **piggyback**: ir a cuestas sobre
infraestructura ajena ya es el término técnico para ello. Por eso el texto
en el texto corrido en inglés de este skill se usa *piggyback*; **"huckepack" es el título de
trabajo en alemán** bajo el que se construyó el patrón y, a la vez, el nombre
del repositorio desde el que se migró este skill. **Los valores literales de
modo siguen siendo `huckepack-gift` y `huckepack-only-host`**: son lo que se
envía en código y configuración, escrito exactamente así, independientemente
del idioma del texto que lo rodea.

## El problema

Una aplicación se construye localmente: una base de datos, una API key, un
estado que vive en el proceso. En la máquina propia eso es simplemente
correcto. En cuanto alguien la aloja para otros, cada una de estas tres
suposiciones se convierte en un error: cada visitante comparte el mismo
estado, la misma base de datos y la misma key. Quien abre la página ve los
datos de todos los demás.

La solución habitual es la gestión de usuarios: cuentas, inicio de sesión,
comprobaciones de acceso, plazos de borrado, una política de privacidad, un
contrato de encargado del tratamiento. Muchas veces es un esfuerzo mayor que
la propia aplicación.

## La idea

**El visitante conserva todo en su propio dispositivo. El host no conserva
nada.**

Esto no resuelve la gestión de usuarios: la vuelve **innecesaria**. Donde no
hay datos ajenos en el servidor, no hay nada que aislar entre visitantes, nada
que borrar según un calendario, y la política de privacidad se reduce a lo que
el servicio realmente hace.

## Los tres modos

| Modo | API key | Datos | Gestión de usuarios |
|---|---|---|---|
| **`huckepack-gift`** | del host | en el dispositivo del visitante | ninguna |
| **`huckepack-only-host`** | del visitante | en el dispositivo del visitante | ninguna |
| **`pay-membership`** | del host, facturada | servidor | obligatoria |

- **`huckepack-gift`**: el host aporta su propia key y regala la ejecución.
  Una invitación sin fricción para probar la herramienta.
- **`huckepack-only-host`**: el visitante trae su propia key. El host no paga
  nada y no guarda nada.
- **`pay-membership`**: deliberadamente dejado como stub. Aquí vuelve a ser
  necesario todo lo que los otros dos evitan: cuentas, facturación,
  almacenamiento en el servidor. Es un esfuerzo propio, no un interruptor que
  se active.

Siempre existe un **`local`** por defecto: quien no configura nada
obtiene la aplicación exactamente como funcionaba antes, en la máquina propia.

## Los componentes

| Componente | Propósito |
|---|---|
| Modo como ajuste en tiempo de instalación | una propiedad del despliegue, no de la sesión |
| Capa de almacenamiento intercambiable | la misma base de datos, otro lugar |
| SQLite en el navegador (WASM + OPFS) | el mismo esquema, las mismas consultas, otro lugar de ejecución |
| Campo de key enmascarado | solo en el modo `only-host`, nunca registrado en logs |
| Exportación e importación | **no opcionales**: los datos del navegador son volátiles |
| Comprobante como archivo descargable, carpeta de destino elegible | ningún servidor participa en la entrega |

El esfuerzo de ingeniería real está en hacer la capa de almacenamiento
intercambiable: la aplicación escribe en SQLite de una forma u otra, pero una
capa intermedia decide si esa escritura acaba en el servidor o en el navegador
del visitante (`sql.js` / la build oficial de SQLite-WASM,
persistida mediante el Origin Private File System). Si WASM resulta demasiado
pesado, ordenar las opciones de almacenamiento del navegador por peso:
SQLite-WASM + OPFS (una base de datos real, mayor capacidad) > IndexedDB
(estructurado, modelo de consultas propio) > `localStorage` (solo apto para
cosas pequeñas como idioma y tema).

## Lo que este patrón no resuelve, dicho con franqueza

- **Si se borran los datos del navegador, todo desaparece.** No existe copia
  en el servidor. Por eso la exportación es una condición, no un extra.
- **No hay cambio de dispositivo** sin exportar e importar.
- **La key que vive en el navegador** (`only-host`) está menos protegida
  que una en un servidor. Pero pertenece al visitante, y la alternativa sería
  entregarla al host, que no es obviamente la opción más segura.
- **La ejecución sigue pasando por el host.** En servicios que alcanzan a un
  tercero, como una llamada telefónica, el host trata los datos de ese tercero
  con independencia de dónde estén los registros propios del visitante. Esto no
  vuelve superflua una política de privacidad, solo la hace más breve.

## Lo que arrojó la revisión jurídica

Una evaluación jurídica preliminar (`references/RECHT.md`, en alemán; examina la
normativa alemana y de la UE, por lo que citarla traducida sería menos preciso,
no más accesible) comprobó el patrón frente al RGPD, el TDDDG y la UWG.
**Evaluación preliminar con referencias, no asesoramiento jurídico.** Tres
hallazgos, una línea cada uno:

- **El host sigue siendo responsable aunque no guarde nada.** El art. 4(7)
  RGPD vincula la responsabilidad a decidir sobre los fines y los medios, no al
  almacenamiento; el TJUE lo ha dicho expresamente así (C-683/21). Lo que se
  vuelve innecesario es la **gestión de usuarios**, no la responsabilidad.
- **Para la persona contactada no se reduce nada.** Los deberes de información
  del art. 14, una ponderación documentada de la base jurídica, un contrato de
  encargado del tratamiento con el servicio que ejecuta el contacto: suelen ser
  las secciones más largas de una política de privacidad, y el patrón no las
  toca.
- **La excepción doméstica beneficia al visitante, no al host.** Cubre el uso
  puramente personal por una persona física; un servicio ofrecido a otros no es
  una actividad puramente personal. Ahí es precisamente donde empieza el
  alojamiento piggyback.

La ganancia está en el **alcance de las obligaciones y el tamaño de la
superficie de ataque**, no en su naturaleza, lo que a la vez es la afirmación
más honesta sobre el patrón.

## Cómo se aplica este patrón

1. Leer `references/DATA-FLOW-TEMPLATE.md` y completarlo para la aplicación real, basándose en
   evidencias (cada línea necesita un `file:line` o "no encontrado"). Esto
   deja al descubierto qué suposiciones locales se rompen bajo el alojamiento
   multiusuario, antes de cambiar código.
2. Decidir qué modos necesita realmente la aplicación: `local` es
   siempre el valor por defecto; `huckepack-gift` y `huckepack-only-host` son los
   dos que evitan la gestión de usuarios; `pay-membership` sigue siendo un stub
   mientras no exista una razón concreta para cuentas reales.
3. Hacer intercambiable la capa de almacenamiento (el paso central de arriba),
   añadir el campo de key enmascarado para `only-host` y conectar la
   exportación/importación antes de publicar nada: es la red de seguridad del
   almacenamiento volátil del navegador.
4. Completar `references/PRIVACY-TEMPLATE.md` para el despliegue concreto; eliminar los bloques
   que no apliquen, verificar cada dato del proveedor contra los contratos
   vigentes y obtener una revisión jurídica específica del caso antes de tratar
   datos reales. La plantilla es un punto de partida, no una declaración
   terminada.
5. En cualquier instalación que afecte a terceros reales (llamadas telefónicas,
   mensajes a personas que no se registraron por sí mismas) o a participantes de
   investigación, tratar las recomendaciones de `references/RECHT.md` como una lista
   de comprobación y no como una autorización: consultar a un abogado antes de la
   primera ejecución pública.

## Referencias

- `references/DATA-FLOW-TEMPLATE.md`: plantilla y procedimiento para un plan de flujo de
  datos; cada línea necesita un file:line, de lo contrario es una suposición y
  no un hallazgo.
- `references/PRIVACY-TEMPLATE.md`: política de privacidad modelo con marcadores de
  posición para una instalación piggyback.
- `references/RECHT.md`: evaluación jurídica preliminar (en alemán) con
  referencias al RGPD, al TDDDG y a la UWG.

Ambas plantillas son **modelos, no asesoramiento jurídico**. Quien aloja una
aplicación la adapta y es responsable del resultado.

## Origen

Surgido durante la construcción de HungryCall, Ringedingeding y ResearchCall:
tres agentes de llamadas en los que una auditoría de flujo de datos mostró que
alojarlos sin cambios habría sido un incidente de protección de datos con nombre propio adjunto.
Migrado desde el repositorio independiente `huckepack` a esta biblioteca
de skills.
