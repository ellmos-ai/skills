---
language: es
---

> **Español** — Versión oficial en español de `full-after-care`.

# Full After Care — la ronda profunda (Sinónimo: Deep After Care)

## Cuándo se aplica esta skill

Usa esta skill cuando un repositorio publicado deba revisarse a **fondo**: sin revisar desde hace tiempo, antes de un lanzamiento importante, en caso de asuntos de relevancia legal o cuando se trate de la integración con el resto de los proyectos propios.

La diferencia respecto a la ronda rápida es el esfuerzo, no la minuciosidad: el Nivel 2 supera los límites de un único repositorio. Consulta fuentes externas (situación legal), inventaria **todas** las organizaciones e interviene en la propia aplicación (idiomas). Por eso se ejecuta con menor frecuencia — típicamente una vez al año por repositorio o según la ocasión.

## Flujo de trabajo

### Nivel 1 completo primero

Ejecuta **`surface-after-care` por completo** — incluyendo el Paso 0 (plataformas de distribución), Privacy-Gate, intención de publicación, banner, alineación estado actual-objetivo, idiomas del README, visibilidad, entrada de la organización, issues y PRs, así como commit, push y paridad de plataformas. Nada de esto se repite ni se abrevia aquí.

Los tres pasos siguientes se añaden a lo anterior. Generan por su parte cambios en la documentación y el código — envíalos con el mismo ritmo descrito en el Nivel 1, en commits temáticamente separados.

---

### 5. Evaluación legal inicial con revisión anual

#### Primero: ¿Se requiere realmente una evaluación?

Consulta `_after-care/RECHTSCHECK.md` (la carpeta está en gitignore, ver más abajo). Si contiene una fecha de revisión de **hace menos de un año**, este paso se **omite** — incluso en la ronda profunda. Solicitar una nueva evaluación cuesta tiempo y dinero y no aporta nada nuevo.

Si la fecha es **más antigua que un año** o el archivo no existe, se realiza la evaluación. El motivo de la revisión no es que el informe pierda validez técnica, sino que la **situación legal** cambia: nuevos reglamentos, umbrales modificados, nueva jurisprudencia, normas de la plataforma cambiadas. Un informe legal de hace dos años puede ser formalmente correcto pero estar prácticamente obsoleto.

Fuera del ritmo anual, se requiere una nueva evaluación si el **objeto** ha cambiado: nuevas categorías de datos, nuevo canal de distribución, nuevo modelo de negocio, cambio de licencia, nueva dependencia con copyleft, ampliación a otra jurisdicción.

#### ¿Es el repositorio legalmente relevante?

No todos los proyectos lo necesitan. Los desencadenantes incluyen, entre otros:

- procesa datos personales, aunque sea solo localmente
- accede a servicios, sitios web o API de terceros (términos de servicio, scraping)
- proporciona información en campos regulados (derecho, medicina, impuestos, finanzas)
- contiene marcas, nombres o logotipos de terceros en el nombre, documentación o UI
- contiene dependencias con copyleft o licencia no clara, o incluye contenido de terceros
- está dirigido a menores, procesa pagos o está sujeto a regulaciones de exportación/criptografía
- toma decisiones automatizadas sobre personas o se clasifica como sistema de IA

Si nada de esto se aplica, registra en el log de ejecución **que se comprobó y resultó negativo** — de lo contrario, la siguiente ronda formulará exactamente la misma pregunta desde el principio.

#### Obtención de la evaluación

Utiliza el departamento legal (skill `law-checker`, módulo `law-checker`) y preséntale los hechos concretos: qué hace la aplicación, qué datos toca, a través de qué canales se distribuye, qué licencias incluye, a quién va dirigida. Cuanto más concretos sean los hechos, más útiles serán las referencias. El resultado es una evaluación inicial con citas de párrafos legales — **no es asesoramiento jurídico**; en caso de riesgo grave, el resultado es la recomendación de consultar a un abogado, no el veredicto en sí.

#### Almacenamiento

```
_after-care/
├── LOG.md                    # Laufprotokoll beider Stufen
└── RECHTSCHECK.md            # Datum, Gegenstand, Ergebnis, Auflagen, Wiedervorlage
```

`_after-care/` pertenece a `.gitignore`. Esto no es un juego de escondite, sino la misma regla que en el Paso 2b del Nivel 1: los documentos de trabajo internos no son contenido del repositorio. En el caso de un informe legal, se suma que un análisis de riesgos distribuido públicamente puede interpretarse como una confesión y ofrece a los atacantes una hoja de ruta. Alternativamente, el almacenamiento puede realizarse fuera del repositorio en una carpeta propia — lo importante es que sea **localizable** en la siguiente ejecución, de lo contrario no se aplica la regla anual.

Mantén el encabezado del archivo legible por máquina:

```markdown
# Rechtscheck — <Projekt> (Deutsch)
geprüft: 2026-07-24
gegenstand: lokale Dateiverwaltung, keine Cloud, keine personenbezogenen Daten Dritter
ergebnis: unbedenklich
auflagen: Hinweis auf MIT-Lizenz der eingebetteten Bibliothek X im README
wiedervorlage: 2027-07-24
```

Lo que se hace **público** de la evaluación son únicamente las **consecuencias**: una mención de licencia, un descargo de responsabilidad, un aviso de privacidad, una descripción aclarada de lo que hace la app. Estos cambios pertenecen al repositorio; la justificación subyacente no.

---

### 9. Referencias cruzadas en todas las organizaciones

El Nivel 1 solo pregunta si el repositorio figura en las páginas de la organización. El Nivel 2 va un paso más allá: **¿Qué repositorios individuales de todas las organizaciones propias están relacionados con este y lo saben ambas partes?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

El valor no proviene del listado, sino de reconocer las relaciones. Tipos relevantes:

- **usa / es usado por** — dependencia técnica real en ambas direcciones
- **pertenece a la misma familia** — línea de productos compartida, prefijo común, arquitectura común
- **resuelve el mismo problema de forma diferente** — un usuario que llega a uno a menudo desea conocer el otro
- **predecesor / sucesor** — los proyectos reemplazados necesitan una señalización, de lo contrario los usuarios terminarán permanentemente en una versión obsoleta
- **bloque de construcción / composición** — biblioteca y la aplicación que la utiliza

Configura las referencias de forma **bidireccional**. Una calle de sentido único es el error más común en este paso: se añade una lista de proyectos relacionados en el repositorio mantenido y no se escribe nada en los proyectos relacionados. Quien llegue allí nunca encontrará el camino de regreso.

Por lo tanto, el enlace inverso se establece realmente en el repositorio de destino — de acuerdo con la **regla del árbol sucio (dirty tree)** del Paso 11 del Nivel 1, resumida brevemente: árbol limpio → commit y push propio; sucio en otros archivos → commit exacto por ruta, no hacer push; sucio en el archivo de destino o bloqueo activo → no tocar. Si no se establece el enlace, debe incluirse en la lista de tareas del repositorio de destino (`AUFGABEN.txt`/`TODO.md`), o en caso de bloqueo, solo en el propio log de ejecución. De este modo, la ronda permanece completa en sí misma sin arriesgar estados de trabajo ajenos y sin que la referencia se pierda.

Formula las referencias orientadas a la utilidad para el usuario, no como una simple lista de nombres: "**project-b** — lee las exportaciones generadas por esta herramienta y crea informes a partir de ellas" es útil; "ver también: project-b" no lo es.

Los repositorios archivados y evidentemente inactivos no se enlazan — salvo como indicación explícita de sucesor en la dirección opuesta.

Este inventario es la parte más costosa de la ronda. Si hay muchas organizaciones y repositorios que examinar, vale la pena guardar el resultado del inventario en el log de ejecución para que la próxima ronda profunda de otro repositorio pueda basarse en él.

---

### Actualizar todos los idiomas a nivel de aplicación

El Nivel 1 se encarga de las versiones de idioma del README. Aquí se trata del **producto en sí**: textos de interfaz, mensajes, ayudas, salidas de CLI, mensajes de error, descripciones de tienda y registro.

Determina primero qué idiomas conoce ya técnicamente la aplicación y cómo los gestiona:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

A continuación, completa los vacíos respondiendo a tres preguntas:

1. **¿Faltan idiomas** que el proyecto debería tener? Los idiomas estándar son alemán, inglés, español, chino simplificado, japonés y ruso — para aplicaciones orientadas al usuario. Para bibliotecas orientadas a desarrolladores, el inglés por sí solo suele ser la respuesta correcta; un idioma innecesario representa una carga de mantenimiento permanente, no una ventaja.
2. **¿Están completos los idiomas existentes?** Después de cada ciclo de características, los idiomas secundarios se quedan atrás. Las claves nuevas sin traducción a menudo recurren al idioma principal durante la ejecución y, por lo tanto, no se perciben; por ello, realiza un diff específico contra el idioma principal aquí en lugar de confiar en la apariencia superficial.
3. **¿Es accesible la selección de idioma para los usuarios?** Una traducción completa que nadie puede activar no sirve de nada. ¿Existe un conmutador, la selección es persistente, se detecta el idioma del sistema por defecto?

Respeta el mecanismo de i18n establecido en el proyecto y no introduzcas un segundo mecanismo paralelo. Comprueba los resultados en la **interfaz real**, no solo en el archivo de recursos: las cadenas demasiado largas rompen los diseños y la falta de compatibilidad con fuentes solo se muestra al renderizar (los glifos CJK faltantes aparecen como cuadros vacíos).

Por último, incluye las plataformas del Paso 0 del Nivel 1: las descripciones de tiendas y registros tienen sus propios campos de idioma que no se trasladan automáticamente con la traducción de la aplicación.

## Log de ejecución

Añade a `_after-care/LOG.md` una entrada con el nivel `full`:

```markdown
## 2026-07-24 — full
- Stufe 1 vollständig gelaufen (siehe Eintrag oben)
- Rechtscheck: fällig (letzter 2025-06-02) -> neu eingeholt, Ergebnis unbedenklich,
  Auflage Lizenzhinweis Bibliothek X umgesetzt, Wiedervorlage 2027-07-24
- Querverweise: 4 Orgas / 38 Repos geprüft, 3 Beziehungen gefunden,
  bidirektional gesetzt; Rückverweis in repo-y offen (dort aktiver Lock)
- Sprachen App-Ebene: ES ergänzt (312 Schlüssel), JA auf Stand gebracht,
  Umschalter war vorhanden aber nicht persistent -> gefixt
```

## Errores frecuentes

| Error | Corrección |
|---|---|
| Se volvió a solicitar la evaluación legal aunque la última tenía 3 meses | Lee primero la fecha en `_after-care/RECHTSCHECK.md`; si tiene menos de un año, se omite |
| Se omitió la evaluación legal porque "nada ha cambiado" | La situación legal cambia independientemente del proyecto; se evalúa a partir de un año |
| Se confirmó la evaluación en el repo | `_after-care/` pertenece a `.gitignore`; solo las consecuencias se hacen públicas |
| No se documentó la irrelevancia legal | Incluso un "no relevante" es un hallazgo y pertenece al protocolo |
| Referencias cruzadas configuradas solo en el repo mantenido | Configurar de forma bidireccional; de lo contrario, es una calle de sentido único |
| Se comprobó solo la propia organización | El Nivel 2 significa TODAS las organizaciones — eso es exactamente lo que lo diferencia del Nivel 1 |
| Referencias enumeradas como una simple lista de nombres | Explica el beneficio en una frase breve; de lo contrario, nadie hará clic |
| Nuevo idioma creado pero no accesible en la UI | Comprueba también el conmutador, la persistencia y la detección del idioma del sistema |
| Traducción comprobada solo en el archivo de recursos | Comprueba en la interfaz real: los problemas de diseño y los glifos faltantes solo se ven allí |
| Se olvidaron los campos de idioma de la tienda/registro | No se trasladan automáticamente con la traducción de la app |

## Lista de verificación final

- [ ] `surface-after-care` ejecutado por completo (incl. push y paridad de plataformas).
- [ ] Relevancia legal comprobada; resultado documentado — incluso si es negativo.
- [ ] ¿Eran necesarias las comprobaciones legales? En caso afirmativo: obtenidas, condiciones aplicadas, fecha de revisión fijada.
- [ ] `_after-care/` en `.gitignore`, evaluación no rastreada.
- [ ] Todas las organizaciones inventariadas, relaciones determinadas.
- [ ] Referencias cruzadas configuradas bidireccionalmente, confirmadas y enviadas en los repositorios de destino.
- [ ] Repositorios de destino omitidos por dirty tree o bloqueo anotados como tareas pendientes.
- [ ] Idiomas de la app completos, conmutador accesible, verificado en la interfaz.
- [ ] Campos de idioma de la tienda/registro actualizados.
- [ ] Entrada en el log de ejecución escrita con nivel `full`.

## Historial de cambios

### 1.0.0 (2026-07-24)
- Versión inicial. Nivel 2 del mantenimiento de repositorios, basado en `surface-after-care`.
