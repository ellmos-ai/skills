---
language: es
---

<img src="banner.png" width="100%" alt="full-after-care banner">

> **Español** — Versión oficial en español de `full-after-care`.


# Full After Care — Ronda Profunda (Sinónimo: Deep After Care) (Español)

## Cuándo se aplica este skill

Utilízalo cuando un repositorio publicado deba revisarse **fundamentalmente**: no comprobado durante mucho tiempo, antes de un lanzamiento importante, en materias legalmente relevantes, o cuando la integración con otros proyectos propios sea un tema.

La diferencia con la ronda superficial (`surface-after-care`) es el esfuerzo, no la diligencia: el Nivel 2 sale de los límites del repositorio individual. Consulta fuentes externas (situación legal), inventaria **todas** las organizaciones e interviene en la propia aplicación (idiomas). Por lo tanto, se ejecuta con menos frecuencia: típicamente una vez por repositorio al año o según la ocasión.

## Proceso

### Nivel 1 primero completo

Ejecuta **`surface-after-care` completamente** — incluyendo el Paso 0 (superficies de distribución), puerta de privacidad, intención de publicación, banners, comparación real-ideal, idiomas del README, visibilidad, entrada de organización, issues y PRs, así como commit, push y paridad de superficies. Nada de esto se repite ni se abrevia aquí.

Los tres pasos siguientes se añaden a lo anterior. Generan por su parte cambios en la documentación y en el código; publícalos al mismo ritmo descrito en el Nivel 1, en commits temáticamente separados.

---

### 5. Evaluación legal inicial con revisión anual

#### Primero: ¿Está pendiente una evaluación?

Consulta `_after-care/RECHTSCHECK.md` (la carpeta está en gitignore, ver abajo). Si hay una fecha de revisión que sea de hace **menos de un año**, este paso se **omite**, incluso en la ronda profunda. Obtener de nuevo una evaluación fresca cuesta tiempo y dinero y no aporta nada nuevo.

Si la fecha es **anterior a un año** o el archivo no existe, se realiza la revisión. La razón de la revisión no es que el dictamen empeore, sino que la **situación legal** cambia: nuevas regulaciones, umbrales modificados, nueva jurisprudencia, reglas de plataforma cambiadas. Un dictamen de dos años puede ser formalmente correcto pero estar prácticamente desfasado.

Fuera del ciclo anual, se debe realizar una reevaluación si el **objeto** ha cambiado: nuevas categorías de datos, nuevo canal de distribución, nuevo modelo de negocio, cambio de licencia, nueva dependencia con copyleft, ampliación a otra jurisdicción.

#### ¿Es el repositorio legalmente relevante?

No todos los proyectos lo necesitan. Los desencadenantes incluyen:

- procesa datos personales, aunque solo sea localmente
- accede a servicios, páginas web o interfaces de terceros (términos de uso, scraping)
- proporciona información en campos regulados (derecho, medicina, impuestos, finanzas)
- lleva marcas, nombres o logotipos de terceros en el nombre, documentación o UI
- contiene dependencias con copyleft o licencia no clara, o incluye contenidos de terceros
- está dirigido a menores, procesa pagos o cae bajo normas de exportación/criptografía
- toma decisiones automatizadas sobre personas o está clasificado como sistema de IA

Si nada de esto aplica, documenta en el protocolo de ejecución **que se verificó y se denegó**; de lo contrario, la siguiente ronda hará la misma pregunta desde el principio.

#### Obtener evaluación

Utiliza el departamento legal (Skill `law-checker`, módulo `law-checker`) y preséntale los hechos concretos: qué hace la aplicación, qué datos toca, a través de qué canales se distribuye, qué licencias intervienen, a quién se dirige. Cuanto más concretos sean los hechos, más útiles serán las referencias. El resultado es una evaluación inicial con citas de párrafos legales — **no es asesoramiento jurídico**; en caso de riesgo serio, el resultado es la recomendación de consultar a un abogado, no la sentencia en sí.

#### Almacenamiento

```
_after-care/
├── LOG.md                    # Registro de ejecución de ambos niveles
└── RECHTSCHECK.md            # Fecha, objeto, resultado, condiciones, revisión
```

`_after-care/` pertenece a `.gitignore`. Esto no es ocultar nada, sino la misma regla que en el Paso 2b del Nivel 1: los documentos de trabajo internos no son contenido del repositorio. En el caso de un dictamen, se suma que un análisis de riesgos distribuido públicamente puede leerse como una admisión y proporcionar a los atacantes un mapa. Alternativamente, el almacenamiento puede realizarse fuera del repositorio en una carpeta propia; lo único importante es que sea **localizable** en la siguiente ejecución, de lo contrario la regla anual no aplicará.

Mantén el encabezado del archivo legible por máquina:

```markdown
# Rechtscheck — <Proyecto> (Español)
geprüft: 2026-07-24
gegenstand: lokale Dateiverwaltung, keine Cloud, keine personenbezogenen Daten Dritter
ergebnis: unbedenklich
auflagen: Hinweis auf MIT-Lizenz der eingebetteten Bibliothek X im README
wiedervorlage: 2027-07-24
```

Lo que se vuelve **público** de la evaluación son solo las **consecuencias**: una indicación de licencia, un descargo de responsabilidad, un aviso de privacidad, una descripción precisada de lo que hace la app. Estos cambios pertenecen al repositorio; la justificación detrás de ellos no.

---

### 9. Referencias cruzadas entre todas las organizaciones

El Nivel 1 solo pregunta si el repositorio está en las páginas de la organización. El Nivel 2 va un nivel más profundo: **¿Qué repositorios individuales de todas las organizaciones propias están vinculados con este — y ambas partes lo saben?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

El valor no proviene del listado, sino del reconocimiento de relaciones. Tipos relevantes:

- **usa / es usado por** — dependencia técnica real en ambas direcciones
- **pertenece a la misma familia** — línea de productos común, prefijo común, arquitectura común
- **resuelve el mismo problema de forma diferente** — un usuario que llega a uno a menudo quiere conocer el otro
- **predecesor / sucesor** — los proyectos reemplazados necesitan una señalización, de lo contrario los usuarios aterrizan permanentemente en código obsoleto
- **componente / composición** — biblioteca y la aplicación que la utiliza

Establece las referencias de forma **bidireccional**. Una calle de sentido único es el error más común de este paso: añadir en el repositorio mantenido una lista de proyectos relacionados, mientras que en los proyectos relacionados no se escribe nada. Quien aterrice allí nunca encontrará el camino de regreso.

La referencia inversa se establece realmente en el repositorio de destino —, según la **regla de árbol sucio** del Paso 11 del Nivel 1, resumida brevemente: árbol limpio -> commit y push propios; sucio en otros archivos -> hacer commit exacto por ruta, no hacer push; sucio en el archivo de destino o bloqueo activo -> no tocar. Si no se establece la referencia, pertenece a la lista de tareas del repositorio de destino (`AUFGABEN.txt`/`TODO.md`), o en caso de bloqueo solo a tu propio protocolo. De este modo, la ronda queda autocontenida sin poner en peligro estados de trabajo ajenos y sin que la referencia se pierda.

Formula las referencias orientadas a la utilidad, no como una mera lista de nombres: "**proyecto-b** — lee las exportaciones generadas por esta herramienta y crea informes a partir de ellas" es útil; "ver también: proyecto-b" no lo es.

Los repositorios archivados y evidentemente muertos no se enlazan — excepto como aviso explícito de sucesor en la dirección opuesta.

Este inventario es la parte más costosa de la ronda. Si hay muchas organizaciones y repositorios que revisar, vale la pena guardar el resultado del inventario en el protocolo de ejecución para que la siguiente ronda profunda de otro repositorio pueda basarse en él.

---

### Actualizar todos los idiomas a nivel de aplicación

El Nivel 1 se encarga de las versiones de idioma del README. Aquí se trata del **producto en sí**: textos de interfaz, mensajes, ayudas, salidas CLI, mensajes de error, descripciones de tiendas y registros.

Determina primero qué idiomas conoce ya técnicamente la aplicación y cómo los gestiona:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Luego cierra las brechas respondiendo a tres preguntas:

1. **¿Faltan idiomas** que el proyecto debería tener? Los idiomas estándar son alemán, inglés, español, chino simplificado, japonés, ruso — para aplicaciones orientadas al usuario. En bibliotecas para desarrolladores, el inglés solo suele ser la respuesta correcta; un idioma innecesario es una carga de mantenimiento permanente, no una ganancia.
2. **¿Están completas las traducciones existentes?** Tras cada ciclo de funciones, los idiomas secundarios se quedan atrás. Las nuevas claves sin traducción a menudo recurren al idioma principal sin que se note — por lo que se debe hacer un diff explícito contra el idioma principal en lugar de fiarse de la inspección visual.
3. **¿Es accesible la selección de idioma para los usuarios?** Una traducción completa que nadie puede activar actúa como si no existiera. ¿Selector presente, selección persistente, idioma del sistema detectado por defecto?

Respeta el mecanismo de i18n establecido en el proyecto y no introduzcas un segundo mecanismo paralelo. Comprueba los resultados en la **interfaz real**, no solo en el archivo de recursos: las cadenas demasiado largas rompen los diseños, y la falta de soporte de fuentes solo se muestra en el renderizado (los caracteres CJK faltantes aparecen como cuadros vacíos).

Por último, incluye las superficies del Paso 0 del Nivel 1: Las descripciones de tiendas y registros tienen sus propios campos de idioma que no se mueven automáticamente con la traducción de la aplicación.

## Registro de ejecución

Añade una entrada con el nivel `full` a `_after-care/LOG.md`:

```markdown
## 2026-07-24 — full
- Nivel 1 ejecutado completamente (ver entrada anterior)
- Chequeo legal: pendiente (último 2025-06-02) -> obtenido nuevamente, resultado sin objeciones,
  condición de aviso de licencia de biblioteca X implementada, revisión 2027-07-24
- Referencias cruzadas: 4 orgs / 38 repos revisados, 3 relaciones encontradas,
  establecidas bidireccionalmente; referencia inversa en repo-y pendiente (bloqueo activo allí)
- Idiomas a nivel de app: ES añadido (312 claves), JA actualizado,
  selector presente pero no persistente -> corregido
```

## Errores frecuentes

| Error | Corrección |
|---|---|
| Chequeo legal obtenido de nuevo aunque el último fue hace 3 meses | Leer la fecha en `RECHTSCHECK.md` primero — menos de un año se omite |
| Chequeo legal omitido porque "nada ha cambiado" | La situación legal cambia independientemente del proyecto; a partir de un año se revisa |
| Dictamen legal incluido en commit del repo | `_after-care/` pertenece a `.gitignore`; solo las consecuencias se hacen públicas |
| Relevancia legal denegada no documentada | Incluso un "no relevante" es un hallazgo y pertenece al protocolo |
| Referencias cruzadas solo en el repo mantenido | Establecer bidireccionalmente, de lo contrario es una calle de sentido único |
| Revisada solo la org propia | El Nivel 2 significa todas las organizaciones — eso la distingue del Nivel 1 |
| Referencias como simple lista de nombres | Explicar la utilidad en media frase, de lo contrario nadie hace clic |
| Nuevo idioma creado pero no accesible en la UI | Probar selector, persistencia y detección del idioma del sistema |
| Traducción probada solo en el archivo de recursos | Probar en la interfaz real — diseños rotos y caracteres faltantes solo se ven allí |
| Campos de idioma de tiendas/registros olvidados | No se mueven automáticamente con la traducción de la app |

## Lista de comprobación final

- [ ] `surface-after-care` ejecutado completamente (incl. push y paridad de superficies).
- [ ] Relevancia legal revisada; resultado documentado — incluso si es denegado.
- [ ] ¿Estaba pendiente el chequeo legal? En caso afirmativo: obtenido, condiciones implementadas, revisión fijada.
- [ ] `_after-care/` en `.gitignore`, dictamen no rastreado.
- [ ] Todas las organizaciones inventariadas, relaciones determinadas.
- [ ] Referencias cruzadas establecidas bidireccionalmente, committeadas y pusheadas en repositorios de destino.
- [ ] Repositorios de destino omitidos por árbol sucio o bloqueo anotados como puntos pendientes.
- [ ] Idiomas de la aplicación completos, selector accesible, comprobado en la interfaz.
- [ ] Campos de idioma de tiendas/registros sincronizados.
- [ ] Entrada de registro de ejecución escrita con nivel `full`.

## Historial de cambios

### 1.0.0 (2026-07-24)
- Versión inicial. Nivel 2 del mantenimiento posterior del repositorio, basándose en `surface-after-care`.