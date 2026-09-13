---
name: full-after-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-30
aliases: [deep-after-care, repo-after-care-full, tiefe-repo-pflege, repo-tiefenpflege]
description: >
  Ronda de mantenimiento profundo para un repositorio publicado de GitHub (Nivel 2): incluye
  la ejecución completa de surface-after-care y la complementa con tres pasos costosos —
  evaluación legal preliminar a través del departamento legal con revisión anual
  (el dictamen permanece en el gitignore del repo), referencias cruzadas a repositorios relacionados en TODAS
  las organizaciones y actualización de todos los idiomas a nivel de aplicación, no solo en la documentación.
  Usa esta habilidad en "full after care", "deep after care", "mantenimiento profundo de repo", "ronda grande",
  "revisión exhaustiva del repo", cuando un repo lleva tiempo sin revisarse, antes de lanzamientos principales,
  o cuando la relevancia legal, referencias cruzadas o multilingüismo se aborden explícitamente. Para la ronda
  económica y repetida con frecuencia, usa surface-after-care; para la publicación inicial, usa github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, legal, i18n, cross-linking, organization, documentation]
language: es
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: [surface-after-care]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="full-after-care banner">

# Full After Care — La ronda profunda (Sinónimo: Deep After Care)

## Cuándo usar esta habilidad

Úsala cuando un repositorio publicado deba revisarse **a fondo**: si no se ha verificado en mucho tiempo, antes de un lanzamiento principal, en temas con relevancia legal o cuando la integración con otros proyectos personales u organizacionales esté en cuestión.

La diferencia respecto a la ronda económica radica en el esfuerzo, no en la diligencia: el Nivel 2 trasciende los límites del repositorio individual. Consulta fuentes externas (situación legal), inventaría **todas** las organizaciones y modifica la propia aplicación (idiomas). Por eso se ejecuta con menos frecuencia: típicamente una vez por repositorio al año o según la ocasión.

## Flujo de trabajo

### Nivel 1 primero por completo

Ejecuta **`surface-after-care` por completo** — incluyendo el Paso 0 (superficies de distribución), puerta de privacidad, intención de publicación, banners, comparación entre estado actual y objetivo, idiomas del README, visibilidad, registro de organización, issues y PRs, así como commit, push y paridad de superficies. Nada de esto se repite ni se abrevia aquí.

Los siguientes tres pasos se añaden a lo anterior. Generan cambios en la documentación y en el código; publícalos con el mismo ritmo descrito en el Nivel 1, en commits temáticamente separados.

---

### 5. Evaluación legal preliminar con revisión anual

#### Primero: ¿Corresponde realizar una evaluación?

Consulta `_after-care/RECHTSCHECK.md` (la carpeta está en el gitignore, ver más abajo). Si contiene una fecha de auditoría que tiene **menos de un año**, este paso se **omite**, incluso en la ronda profunda. Solicitar una nueva evaluación cuesta tiempo y dinero y no aporta nada nuevo.

Si la fecha es **mayor a un año** o el archivo no existe, se realiza la evaluación. La razón de la revisión periódica no es que el dictamen pierda validez técnica, sino que la **situación legal** cambia: nuevas regulaciones, umbrales modificados, nueva jurisprudencia, reglas de plataforma actualizadas. Un dictamen legal de hace dos años puede ser formalmente correcto pero estar obsoleto en la práctica.

Fuera del ritmo anual, corresponde una reevaluación cuando el **objeto** del proyecto haya cambiado: nuevas categorías de datos, nuevo canal de distribución, nuevo modelo de negocio, cambio de licencia, nueva dependencia con copyleft o expansión a otra jurisdicción.

#### ¿El repositorio es legalmente relevante?

No todos los proyectos lo necesitan. Los desencadenantes incluyen:

- procesa datos personales, aunque sea solo de manera local
- accede a servicios, sitios web o API de terceros (términos de servicio, scraping)
- proporciona información en campos regulados (derecho, medicina, impuestos, finanzas)
- incluye marcas, nombres o logotipos de terceros en el nombre, documentación o UI
- contiene dependencias con copyleft o licencia uncierta, o incluye contenido de terceros
- está dirigido a menores, procesa pagos o cae bajo regulaciones de exportación/criptografía
- toma decisiones automatizadas sobre personas o está clasificado como sistema de IA

Si nada de esto aplica, registra en el protocolo de ejecución **que se verificó y el resultado fue negativo**; de lo contrario, la siguiente ronda volverá a plantear la misma pregunta.

#### Obtención de la evaluación

Utiliza el departamento legal (Habilidad `law-checker`, Módulo `law-checker`) y preséntale los hechos concretos: qué hace la aplicación, qué datos maneja, a través de qué canales se distribuye, qué licencias incluye y a quién va dirigida. Cuanto más concretos sean los hechos, más útiles serán las referencias. El resultado es una evaluación preliminar con citas de artículos — **no es asesoramiento jurídico**; ante un riesgo serio, el resultado es la recomendación de consultar a un abogado, no la sentencia en sí.

#### Almacenamiento

```
_after-care/
├── LOG.md                    # Registro de ejecución de ambos niveles
└── RECHTSCHECK.md            # Fecha, objeto, resultado, condiciones, revisión
```

`_after-care/` debe estar en el `.gitignore`. No se trata de ocultar información, sino de la misma regla del Paso 2b del Nivel 1: los documentos de trabajo internos no forman parte del contenido del repositorio. En el caso de un dictamen legal, se suma que un análisis de riesgo público puede interpretarse como una admisión y proporcionar una hoja de ruta a posibles atacantes. Alternativamente, el almacenamiento se puede realizar fuera del repositorio en una carpeta propia; lo importante es que sea **localizable** en la siguiente ejecución, de lo contrario la regla anual no funcionará.

Encabezado del archivo, mantener en formato legible por máquina:

```markdown
# Legal check — <Proyecto>
checked: 2026-07-24
subject: local file management, no cloud, no personal data of third parties
result: unproblematic
conditions: Note on MIT license of embedded library X in README
resubmission: 2027-07-24
```

Lo que se hace **público** de la evaluación son únicamente las **consecuencias**: una mención de licencia, un descargo de responsabilidad, un aviso de privacidad o una descripción precisada de lo que hace la aplicación. Estos cambios sí pertenecen al repositorio; la justificación interna, no.

---

### 9. Referencias cruzadas en todas las organizaciones

El Nivel 1 solo pregunta si el repositorio figura en las páginas de las organizaciones. El Nivel 2 profundiza un escalón más: **¿Qué repositorios individuales de todas las organizaciones propias están relacionados con este, y ambas partes lo saben?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

El valor no se crea al listar, sino al reconocer relaciones. Tipos relevantes:

- **usa / es usado por** — dependencia técnica real en ambas direcciones
- **pertenece a la misma familia** — línea de productos compartida, prefijo común, arquitectura común
- **resuelve el mismo problema de otra manera** — un usuario que llega a uno a menudo desea conocer el otro
- **predecesor / sucesor** — los proyectos reemplazados necesitan una señalización, de lo contrario los usuarios permanecen en código obsoleto
- **componente / composición** — biblioteca y la aplicación que la utiliza

Establece las referencias de manera **bidireccional**. Un enlace unidireccional es el error más común de este paso: se añade una lista de proyectos relacionados en el repo mantenido, mientras que en los proyectos relacionados no se incluye nada. Quien aterrice allí nunca encontrará el camino de regreso.

La referencia recíproca se establece efectivamente en el repositorio destino — siguiendo la **regla del árbol sucio (Dirty Tree Rule)** del Paso 11 del Nivel 1, resumida brevemente: árbol limpio → commit y push independientes; suciedad en otros archivos → hacer commit de rutas específicas, no hacer push; suciedad en el archivo destino o bloqueo activo → no tocar. Si no se establece la referencia, añádela a la lista de tareas del repo destino (`AUFGABEN.txt`/`TODO.md`), o si está bloqueado, solo a tu propio registro de ejecución. Así, la ronda permanece autocontenida sin arriesgar estados de trabajo externos y sin perder la referencia.

Formula las referencias orientadas a la utilidad, no como una mera lista de nombres: "**project-b** — lee las exportaciones generadas por esta herramienta y crea informes a partir de ellas" es útil; "ver también: project-b" no lo es.

Los repositorios archivados u obviamente abandonados no se enlazan, excepto como una nota explícita de sucesor en la dirección opuesta.

Este inventario es la parte más costosa de la ronda. Cuando hay muchas organizaciones y repositorios por verificar, conviene guardar los resultados del inventario en el registro de ejecución para que la siguiente ronda profunda de otro repositorio pueda basarse en ellos.

---

### Actualización de todos los idiomas a nivel de aplicación

El Nivel 1 se encarga de las versiones de idioma del README. Aquí se trata del **producto en sí**: textos de interfaz, mensajes, pantallas de ayuda, salidas de CLI, mensajes de error, descripciones de tiendas y registros.

Primero determina qué idiomas ya admite la aplicación técnicamente y cómo los gestiona:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Luego cierra las brechas respondiendo a tres preguntas:

1. **¿Faltan idiomas** que el proyecto debería tener? Los idiomas estándar son alemán, inglés, español, chino simplificado, japonés y ruso para aplicaciones orientadas al usuario final. Para bibliotecas orientadas a desarrolladores, el inglés por sí solo suele ser la respuesta correcta; un idioma innecesario es una carga de mantenimiento permanente, no una ganancia.
2. **¿Los idiomas existentes están completos?** Tras cada ciclo de características, los idiomas secundarios se retrasan. Las nuevas claves sin traducción a menudo recurren silenciosamente al idioma principal durante la ejecución, por lo que aquí se debe hacer un diff explícito contra el idioma principal en lugar de confiar en la apariencia.
3. **¿La selección de idioma es accesible para los usuarios?** Una traducción completa que nadie puede activar equivale a ninguna. ¿Existe selector, la selección es persistente y el idioma del sistema se detecta por defecto?

Respeta el mecanismo i18n establecido en el proyecto y no introduzcas un segundo sistema paralelo. Verifica los resultados en la **interfaz de usuario real**, no solo en el archivo de recursos: las cadenas demasiado largas rompen los diseños y la falta de compatibilidad con conjuntos de caracteres solo se muestra al renderizar (los glifos CJK faltantes aparecen como cuadros vacíos).

Por último, incluye las superficies del Paso 0 del Nivel 1: las descripciones de tiendas y registros tienen sus propios campos de idioma que no se actualizan automáticamente con la traducción de la aplicación.

## Registro de ejecución

Añade una entrada con el nivel `full` a `_after-care/LOG.md`:

```markdown
## 2026-07-24 — full
- Nivel 1 completado por completo (ver entrada anterior)
- Chequeo legal: pendiente (último 2025-06-02) -> solicitado nuevamente, resultado sin problemas,
  condición sobre nota de licencia de la biblioteca X implementada, nueva revisión programada para 2027-07-24
- Referencias cruzadas: 4 orgs / 38 repos verificados, 3 relaciones encontradas,
  establecidas bidireccionalmente; referencia recíproca en repo-y pendiente (bloqueo activo allí)
- Idiomas a nivel de app: ES añadido (312 claves), JA actualizado,
  el selector existía pero no era persistente -> corregido
```

## Errores frecuentes

| Error | Corrección |
|---|---|
| Solicitar evaluación legal de nuevo cuando la última fue hace 3 meses | Leer primero la fecha en `RECHTSCHECK.md` — omitir si es menor a un año |
| Omitir la evaluación legal porque "nada ha cambiado" | La situación legal cambia independientemente del proyecto; auditar tras un año |
| Hacer commit del dictamen legal en el repositorio | `_after-care/` debe estar en el `.gitignore`; solo las consecuencias se hacen públicas |
| Relevancia legal negativa no documentada | Incluso "no relevante" es un hallazgo y pertenece al registro |
| Referencias cruzadas establecidas solo en el repositorio mantenido | Establecer bidireccionalmente, de lo contrario es una vía de un solo sentido |
| Verificar solo la organización propia | El Nivel 2 abarca todas las organizaciones; eso es lo que lo diferencia del Nivel 1 |
| Referencias como una mera lista de nombres | Explicar el beneficio en media frase, de lo contrario nadie hace clic |
| Añadir un nuevo idioma inaccesible en la interfaz | Verificar selector, persistencia y detección del idioma del sistema |
| Traducción verificada solo en el archivo de recursos | Verificar en la interfaz real: las roturas de diseño y glifos faltantes solo se ven allí |
| Olvidar campos de idioma de tienda/registro | No se transfieren automáticamente con la traducción de la aplicación |

## Lista de verificación final

- [ ] `surface-after-care` completado por completo (incl. push y paridad de superficies).
- [ ] Relevancia legal verificada; resultado documentado, incluso si fue negativo.
- [ ] ¿Evaluación legal pendiente? De ser así: solicitada, condiciones implementadas, nueva revisión fijada.
- [ ] `_after-care/` en `.gitignore`, dictamen legal sin rastrear.
- [ ] Todas las organizaciones inventariadas, relaciones determinadas.
- [ ] Referencias cruzadas fijadas bidireccionalmente, commiteadas y pusheadas en repositorios destino.
- [ ] Repositorios destino omitidos por árbol sucio o bloqueos anotados como puntos pendientes.
- [ ] Idiomas de aplicación completos, selector accesible, verificado en la interfaz.
- [ ] Campos de idioma en tiendas/registros actualizados.
- [ ] Entrada escrita en el registro de ejecución con el nivel `full`.

## Changelog

### 1.0.0 (2026-07-24)
- Versión inicial. Nivel 2 del mantenimiento posterior de repositorios, basado en `surface-after-care`.
