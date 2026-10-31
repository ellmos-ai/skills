---
name: software-in-worten
version: 1.0.0
type: method
author: ellmos (aus einem Entwurfsgespräch von Lukas Geiger, 2026-08-02)
created: 2026-08-02
updated: 2026-08-23
description: "Traduce entre interfaz de usuario y texto, en ambas direcciones. De una interfaz descrita se obtiene una skill; de una skill se obtiene una interfaz. Úsese cuando se diseñe una aplicación y el flujo aún no esté claro, cuando una herramienta existente deba ponerse a disposición como skill, cuando la interfaz y el acceso de los agentes empiecen a divergir, o cuando una skill se vuelva demasiado larga y nadie sepa por qué."
category: dev
tags: [design, ui, skills, methodik, uebersetzung, entwurf]
language: es
status: stable
visibility: public
standalone: true
translated_from_sha256: e9250c36688fcdb950c1914daefd7ecfaf80e7ed56db0d4d287d2db69d3b9c63
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="software-in-worten banner">

# Software en palabras

## La idea

Las personas diseñan **visualmente**: *¿cómo quiero manejar esto?* Los agentes leen **texto**.
Mientras ambos se crean por separado, se alejan uno del otro: la interfaz puede hacer algo
que la skill no conoce, y viceversa.

Sin embargo, son lo mismo, solo que en distintos estados de agregación. Existe una
traducción, y quien la conoce trabaja en ambas direcciones:

> **Diseñar una interfaz a partir de palabras. Y devolver una interfaz a palabras.**

---

## La tabla de traducción

| En la interfaz | Qué significa | En texto |
|---|---|---|
| **Puntero del ratón** | *puedo elegir* — el espacio de lo posible | el conjunto de opciones en ese punto |
| **Marcar** | *quiero esto* | una selección, un valor |
| **Clic** | *decido, quiero ir allí* | **el prompt** — la respuesta del usuario |
| **Campo, interruptor, ajuste** | una decisión que permanece | **Config** |
| **Ajustes de todo el software** | decisiones que valen en todas partes | **Policies** |
| **Formulario, máscara de entrada** | un conjunto de decisiones relacionadas | **Template** |
| **Botón que inicia algo** | *ahora pasa algo* | se dispara una **skill** o **workflow** |
| **Lo que se ejecuta después** | la secuencia de pasos | instrucciones en la skill — o un **script** |
| **Barra de progreso** | *está en marcha, y hasta dónde* | mensajes de estado en el flujo |
| **Mensaje de éxito, vista de resultados** | *esto es lo que salió* | la devolución — en la interfaz solo se presenta con más estilo |
| **Proyecto** | un estado de trabajo delimitado | una **carpeta** — y como ella misma está en una carpeta, parte del software |
| **Vista, pestaña, área** | un estado en el que uno se encuentra | un paso en el árbol de flujo |

**La línea central es el clic.** Un clic no es otra cosa que lo que un usuario diría en una
conversación, solo que más rápido. **El clic es el prompt.** Y a un prompt le sigue una
reacción: una nueva pregunta, una nueva vista, un nuevo estado.

---

## El flujo es un árbol

Cada aplicación es una secuencia de decisiones entre las cuales ocurre algo:

```
Voraussetzungen geklärt?   →  Referenzen · Kandidatenliste · Nummern · Reihenfolge
        ↓
Einverständnis des Nutzers →  START
        ↓
Will er mitlesen?          →  ja: Mitleseansicht öffnen
Will er Zwischenmeldungen? →  ja: bei jedem Ereignis melden (durch, abgelehnt, Status)
        ↓
        [ AUSFÜHRUNG — oft ausgelagert an andere Software ]
        ↓
Rückgabe kommt zurück      →  auswerten
        ↓
Was will er wissen?        →  das Ergebnis in seinen Begriffen:
                              „bestellt bei X, 40 Minuten, 30 Euro"
```

**Tres partes, siempre las mismas:**

1. **Decisiones** — si-entonces, hasta que está todo lo necesario
2. **Ejecución** — con frecuencia no en la herramienta propia, sino externalizada
3. **Retroalimentación** — el resultado devuelto a la persona, en su idioma

La tercera parte es la que más se subestima al diseñar. **La comunicación pasa por los
sentidos** — como texto, como imagen, como sonido. Una interfaz la da forma; una skill
describe *qué* se comunica y *cuándo*.

---

## El nivel intermedio: el blueprint

Entre "descrito" y "construido" falta un escalón. Se llama **blueprint** y es
**texto cuya disposición corresponde a la imagen**: una pantalla que se puede leer:

```
 Worauf hast du Hunger?   [ Burger                        ]
 Wohin liefern?           [ Dorfstraße 1, 16321 Bernau    ]
 Höchstbetrag             [ 35 ] €   ⓘ Endbetrag an der Haustür
 Modus                    (•) Lieferung  ( ) Tisch  ( ) Abholung

 Kandidaten (ziehen zum Umsortieren)            ↻ neu suchen
 ┌────────────────────────────────────────────────────┐
 │ ≡ 1  Burger House Dorfstadt      ★ Favorit   offen │
 │ ≡ 2  Pizzeria Roma                            offen │
 └────────────────────────────────────────────────────┘

 [ Trockenlauf ansehen ]   [ Wirklich anrufen → 4 Anrufe, ~0,20 € ]
```

**Por qué este escalón aporta tanto:**

Un blueprint es **a la vez legible y visible**. La persona vuelve a ver su imagen, el agente
ve campos, tipos y orden. Se crea en minutos, no cuesta nada y puede corregirse en la
conversación, a diferencia de una interfaz ya construida.

**Y a partir del blueprint la skill sale casi por sí sola:**

> **¿Qué debe poder hacer, saber y ejecutar el agente, y en qué orden, para completar
> este blueprint?**

Cada campo se convierte en una pregunta. La disposición se convierte en el orden. Lo que
viene prerrellenado no se pregunta. Lo que aparece como botón se convierte en un paso.
Después se completa lo que el agente necesita saber además: conocimiento del dominio,
límites, trampas.

**Tres etapas, entonces:** descripción → **blueprint** → skill *(y desde allí igualmente
bien hacia una interfaz construida)*.

### Un campo vacío es una pregunta — y la pregunta tiene un propósito

`[ 35 ] €` parece un número. Pero es una **consulta de datos a una persona**, y tiene
un motivo que suele quedar sin decir:

> **Necesitamos este importe máximo porque es la condición bajo la cual se pide algo.**

Así, el campo lleva tres cosas a la vez: **qué** debe entrar, **por qué** se necesita y
**dónde actuará después**. En una interfaz eso está en el diseño y en el texto de ayuda.
En el texto hay que escribirlo — de lo contrario se pierde.

**Por eso debajo de cada blueprint debe ir una leyenda de campos:**

| | |
|---|---|
| **Pregunta** | cómo se preguntaría a una persona |
| **Tipo** | número, texto, selección, lista, lista ordenada, fecha … |
| **Propósito** | para qué se usará el valor más adelante — *"criterio de corte en la cascada"* |
| **Precondición** | qué debe existir para que el campo tenga sentido |
| **Postcondición** | qué vale después de haberlo rellenado |
| **Si está vacío** | aceptar en silencio · poner un valor por defecto · preguntar · bloquear |
| **Si es incorrecto** | mensaje, pregunta de vuelta, propuesta de corrección |

**Las dos últimas filas son las que más se olvidan** — y las que más problemas dan en la
práctica. *"Precio indiferente"* es una respuesta válida y debe estar prevista como tal, no
como error.

### El campo está abierto — la pregunta restringe

Un campo vacío es **todo y nada**, como una ventana de contexto vacía: una invitación a
escribir cualquier cosa. Pero ¿qué?

**La restricción no viene del campo, sino de lo que lo rodea** — normalmente del texto
enlazado delante, encima o al lado:

> *"¿Cuánto como máximo puede costar?"*

Esa pregunta restringe **semántica y pragmáticamente**. El campo en sí sigue admitiendo
cualquier cosa — y si alguien aprovecha esa libertad, **pierde su sentido**. Por eso entran
en juego las condiciones del campo: *solo números*. No porque "treinta y cinco" fuera
incomprensible, sino porque es más difícil de procesar y más largo de escribir.

**De ahí se deduce la dirección de trabajo: de la pregunta se derivan las reglas del campo,
no al revés.** Quien define primero el tipo de dato ya ha olvidado la pregunta.

Y la pregunta suele llevar también el **propósito** — por eso en las interfaces para personas suele aparecer al lado un icono de información:

> *"No aceptamos una oferta que esté por encima de este precio."*

Esto no es cortesía, sino el significado real del campo: **una preferencia del usuario que
más tarde actúa como puerta dura.**

### El límite de control — y por qué todo debe transmitirse

De un campo se deriva una cadena:

```
Feld „Höchstbetrag"
   → der Wert wird später gebraucht        (Zweck)
   → für eine Prüfung                       (Gate)
   → also muss der Gegenwert erhoben werden (neue Frage, an anderer Stelle)
   → diese Frage stellt niemand von uns     (sie steht im Prompt)
```

**Y aquí corre la línea decisiva: con el prompt se sale de nuestro plano de control.** A
partir de ahí no hay más acceso — ni seguimiento, ni intervención, ni una segunda
oportunidad.

Por eso hay que transmitir **todo** lo que se necesita del otro lado:

- **el valor en sí** — 35 €
- **la instrucción de averiguar la contrapartida** — preguntar por el precio
- **qué vale si es más alto** — rechazar, agradecer, terminar amablemente
- **qué vale si no se menciona ninguno** — no estimar, rechazar
- **qué vale si el interlocutor no quiere hablar con una máquina** — pedir una devolución
  de llamada personal y devolver el número como valor

El último punto muestra la dirección en la que menos se piensa al diseñar: **también el caso
excepcional debe devolver un valor**, de lo contrario la persona no recibe nada más que
"no funcionó".

### El prompt es una skill generada

Con esto queda claro qué es realmente un prompt:

> **Un prompt es una skill que la interfaz acaba de ensamblar** — a partir de las
> decisiones, clics y valores de esta única ejecución. Personalizada, ajustada a la
> finalidad, y obligada a expresar todo lo querido **en lenguaje**.

Una skill escrita de forma fija dice cómo se hace *siempre*. Un prompt dice cómo debe
ejecutarse *esta vez*. Ambos tienen la misma forma: una permanece, la otra surge en el
momento y después desaparece.

**En la práctica:** quien trata la construcción de prompts como un juego de bloques de texto
construye malos prompts. Quien la trata como *generación de skills* — con finalidad, reglas,
límites, excepciones y valores de retorno — construye buenos.

### Esperar no es no hacer nada, sino no saber

Tras enviar, la persona ha cedido el control. Lo que necesita ahora no es paciencia, sino
**información**: *¿qué está pasando ahora? ¿en qué punto estamos?*

El agente ya obtiene eso — consulta el progreso. **La persona no ve nada de ello mientras
nadie lo traduzca.** Precisamente para eso existen las barras de progreso, los registros en
marcha y las líneas de estado: no son adorno, sino la traducción de un flujo de datos a algo
que alguien en espera puede soportar.

### La retroalimentación es un prompt de vuelta

El mensaje de éxito no es un cierre, sino una **entrega de vuelta**:

> *"Este es el resultado de tu encargo."*

Solo así puede la persona valorar y seguir actuando. Y precisamente por eso debe ser
completo: *"Pedido hecho — pero tres pizzas en lugar de una. Menos mal que el número de
devolución de llamada está aquí, llamo yo mismo."*

**Sin una devolución utilizable nadie puede seguir procesando.** Un mensaje que solo dice
"funcionó" no ha cerrado el círculo.

### Análisis de preguntas y campos

Para **cada** elemento de un blueprint — campo, botón, selección, visualización — las mismas
preguntas:

| | |
|---|---|
| **¿Qué se quiere, y para qué?** | la intención detrás del elemento |
| **¿Qué pasa al enviar?** | ¿se procesa de inmediato o solo se guarda? |
| **¿Dónde y cuándo vuelve a necesitarse el valor?** | el lugar donde actúa |
| **¿Cuánto tiempo debe conservarse?** | ¿más allá del clic? ¿más allá de la ejecución? |
| **¿Qué debe ocurrir con él?** | comprobar, transmitir, mostrar, descartar |

El importe máximo, por ejemplo, **no se necesita de inmediato**. Se guarda, se arrastra y
actúa solo en la conversación — así que necesita un lugar donde estar y un punto donde pase
al prompt.

### Las bifurcaciones determinan el algoritmo de preguntas

Una selección rara vez es solo un valor. A menudo es un **interruptor de vía** que
reorganiza todo el flujo posterior:

| Modo | Primera pregunta en la conversación | Qué desaparece | Qué se añade |
|---|---|---|---|
| **Entrega** | *"¿Entregan aquí?"* — un no termina la llamada de inmediato | — | Dirección de entrega |
| **Recogida** | desaparece | la pregunta de entrega | Hora de recogida |
| **Mesa** | *"¿Están abiertos, y hay una mesa libre a las X?"* | toda la comprobación de precio | Número de personas, niños, preferencia de asiento, franja horaria |

**El orden en la conversación sigue la fuerza de exclusión, no la curiosidad.** Quien no
entrega no tiene que preguntar por la comida — la condición más dura va primero porque
conduce más rápido al siguiente candidato.

Y: **mucho se mantiene igual a través de los interruptores.** El importe máximo vale tanto
para entrega como para recogida, igual que la lista de candidatos. Solo cambia el algoritmo
de preguntas.

### El círculo

```
Problem  →  Use Case  →  Wille        „Ich bin auf dem Land und habe Hunger"
   ↓
was ich will, wird zu Bedingungen     5 Personen · 19 Uhr · Italiener · nicht der eine
   ↓
Bedingungen brauchen Daten            → daraus ergeben sich die FELDER
   ↓
Felder + Entscheidungen               → daraus wird der PROMPT (der erzeugte Skill)
   ↓
                [ Ausführung jenseits der Kontrollgrenze ]
   ↓
Rückgabe empfangen und speichern      → nur, was vorher mitgegeben wurde, kommt zurück
   ↓
übersetzen in Sicht- und Hörbares     → MELDUNG an den Menschen
   ↓
er bewertet und entscheidet neu       → zurück nach oben
```

**El caso de uso fundamenta los datos, y los datos fundamentan los campos.** Quien empieza
por los campos inventa formularios. Quien empieza por la intención los recibe de regalo.

### Entre dos blueprints está la causalidad

Un blueprint es una **disposición estática**. Varios seguidos aún no forman un flujo — entre
ellos ocurre algo, y **ese entre es la verdadera lógica**: ¿qué sucede si aquí se hace clic?
¿qué comprobación se ejecuta? ¿qué se guarda? ¿qué se dispara?

Tres formas de hacer visible este plano temporal:

1. **Rotulado en la imagen** — flechas y notas breves entre los blueprints
2. **Pares antes/después** — el mismo fragmento en dos estados, "antes del clic" y
   "después del clic"
3. **Puesta por escrito** — precondiciones y postcondiciones como texto bajo la imagen

La tercera forma llega más lejos porque es ejecutable. Las dos primeras ayudan a la persona
a entender.

### De los campos se deriva el modelo de datos

Quien describe un campo "añadir contacto" ya ha decidido que hay destinatarios, que se
guardan y qué datos les corresponden. **La tabla de datos se ajusta a los campos, no al
revés.**

Por eso conviene completar la leyenda de campos antes de diseñar cualquier esquema: cada
campo con tipo y propósito es una columna, cada grupo repetible una tabla, cada relación
entre campos una referencia.

## Dirección 1: de palabras a una interfaz

**Cuando primero se describió el flujo.**

1. **Reunir las decisiones.** Cada punto donde se fija algo. Ordenándolas:
   - **Obligatoria** — sin ello no se avanza → **campo obligatorio**
   - **Derivable** — puede venir del contexto o de lo existente → **campo prerrellenado** con
     posibilidad de corrección
   - **Opcional** — mejora el resultado → **área plegada**
   - **Puerta** — irreversible, cuesta dinero, llega a personas → **paso de confirmación**
2. **Agrupar lo relacionado** → una máscara, una plantilla.
3. **Cortar el árbol en vistas.** Un estado = una vista.
4. **Diseñar las retroalimentaciones.** ¿Qué se comunica y cuándo? Progreso, estado
   intermedio, resultado.
5. **Fijar una vez lo que vale en todas partes** — color, tipografía, cortes, movimiento.
   Son las policies de la interfaz.

**La ganancia:** un formulario que surge de un flujo de conversación suele ser más ligero
que uno hecho sobre el papel. Al formularlo se nota qué pregunta sobra.

## Dirección 2: de una interfaz a palabras

**Cuando la aplicación ya existe o está descrita.**

1. **Formular cada clic como pregunta.** ¿Qué le pregunta realmente este botón al usuario?
2. **Cada campo como entrada de Config** — con valor por defecto, tipo y texto de ayuda.
3. **Cada vista como paso** en el flujo.
4. **Cada mensaje como devolución** — ¿qué se informa, y con qué palabras?
5. **Comprobar lo que la interfaz sabe de forma implícita** — secuencias, bloqueos,
   dependencias que no aparecen en ningún sitio y solo están en la disposición. **Esta es la
   parte que más fácilmente se pierde al traducir.**

### Por qué esta dirección es más difícil — y cómo recorrerla igualmente

La dirección 1 resulta fácil; la dirección 2 se siente pesada. Hay una razón:

> **Una skill es tiempo. Una pantalla es superficie.**
> Primero esto, luego aquello — frente a todo a la vez.

Así que no se traduce línea a línea, sino que **se corta un flujo en superficies**. El corte
siempre es el mismo:

**Una pantalla surge allí donde el flujo espera a una persona.**

Todo lo que ocurre entre dos puntos de espera se ejecuta por sí solo — eso **no** se
convierte en pantalla, como mucho en un indicador de progreso. Quien construye una vista para
cada paso construye una cárcel de clics.

**¿Y las cadenas si-entonces?** No todas se vuelven visibles. Cuatro casos:

| Tipo de condición | Qué se convierte |
|---|---|
| **La persona la fija** ("como máximo 35 €") | un **campo** — antes del inicio |
| **El sistema la comprueba** ("precio sobre el límite") | un **resultado** — después, con motivo |
| **Cambia lo que la persona ve** ("sin resultados") | un **estado** de la misma pantalla, no una nueva |
| **Es pura mecánica** (reintentos, tiempos de espera, validación de formato) | **nada** — permanece invisible |

**El cuarto caso es el más frecuente.** La mayoría de las ramificaciones de un script nunca
pertenecen a una pantalla. Quien aun así las muestra confunde diagrama de flujo con
interfaz.

**En la práctica, en cuatro pasos:**

1. **Marcar los puntos de espera** — cada lugar donde una persona decide, confirma o
   introduce algo. Esas son las pantallas, y suelen ser sorprendentemente pocas.
2. **Recoger hacia atrás** — ¿qué debe ser conocido antes de este punto de espera? Esos
   valores son los campos de la pantalla.
3. **Recoger hacia delante** — ¿qué pasa después, y qué de ello debe saber la persona? Eso
   es la retroalimentación.
4. **Omitir el resto** — todo lo que no es entrada ni comunicación permanece invisible.

---

## El gradiente: skill ↔ script

```
weit von der Software                                    nah an der Software
   Skill trägt alles                                    Skript trägt alles
        │                                                       │
   ausführlicher Text          ────────────►         knappe Bedienungsanleitung
   jeder Schritt erklärt                             „ruf dies auf, dann jenes"
   funktioniert ohne Werkzeug                        funktioniert nur mit Werkzeug
```

**Cuanto más automatizado está un proceso, menos tiene que explicar la skill.** Se vuelve
más corta y concreta — con el tiempo apenas es más que un manejo de los scripts: *cuándo se
usa esta herramienta, qué se le introduce, cómo se reconoce que ha funcionado.*

Dos conclusiones inversas que ayudan en el día a día:

- **Si una skill se vuelve demasiado larga, falta un script.** La longitud es una señal: lo
  que se repite y es mecánico pertenece a la automatización.
- **Si un script resulta incomprensible, falta una skill.** Una herramienta sin texto encima
  solo la puede usar quien la construyó.

---

## La moneda común

**Cada ajuste existe por triplicado** — como valor de Config, como pregunta en la skill y
como campo en la interfaz. Para que no se separen, la representación se describe **una
sola vez** y la leen las tres:

```yaml
field: sample.method
label: "Ziehungsverfahren"                       # Oberfläche
question: "Wie soll gezogen werden — zufällig, geschichtet oder alle?"   # Skill
type: choice
options: [random, stratified, census]
default: random
help: "Geschichtet nur, wenn die Merkmale in der Grundlage stehen."
locked: false        # true = nicht abschaltbar, erscheint in keiner Oberfläche
```

**Lo que está `locked` no aparece en ningún sitio como opción.** Algunas cosas no son
un ajuste, sino parte del andamiaje.

---

## Cuándo ayuda esta skill

- Se diseña una aplicación y el flujo aún no está claro → **dirección 1**
- Una herramienta existente debe ser utilizable por agentes → **dirección 2**
- La interfaz y el acceso de los agentes divergen → introducir la **moneda común**
- Una skill se vuelve demasiado larga y nadie sabe por qué → revisar el **gradiente**
- Una conversación de diseño debe fijarse antes de que se pierda → tabla + árbol

## Relacionado

`condition` traduce condiciones, momentos y secuencias en puertas comprobables
(`/if`, `/when`, `/after`, `/and`, `/or`) — el mismo movimiento para el caso especial del control de flujo.
`skill-extractor` obtiene skills a partir de historiales de conversación. `plugin-system` hace
que los scripts propios sean localizables.
