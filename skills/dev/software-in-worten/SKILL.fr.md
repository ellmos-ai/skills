---
name: software-in-worten
version: 1.0.0
type: method
author: ellmos (aus einem Entwurfsgespräch von Lukas Geiger, 2026-08-02)
created: 2026-08-02
updated: 2026-08-23
description: "Traduit entre interface utilisateur et texte — dans les deux sens. D'une interface décrite on tire un skill ; d'un skill on tire une interface. À utiliser lorsqu'une application est conçue et que le déroulement n'est pas encore clair, lorsqu'un outil existant doit être rendu disponible comme skill, lorsque l'interface et l'accès des agents divergent, ou lorsqu'un skill devient trop long sans que personne ne sache pourquoi."
category: dev
tags: [design, ui, skills, methodik, uebersetzung, entwurf]
language: fr
status: stable
visibility: public
standalone: true
translated_from_sha256: e9250c36688fcdb950c1914daefd7ecfaf80e7ed56db0d4d287d2db69d3b9c63
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="software-in-worten banner">

# Logiciel en mots

## L'idée

Les humains conçoivent **visuellement** : *comment veux-je l'utiliser ?* Les agents lisent **du texte**.
Tant que les deux naissent séparément, ils divergent — l'interface peut faire quelque chose que
le skill ignore, et inversement.

Pourtant, c'est la même chose, simplement dans des états différents. Il existe une
traduction, et celui qui la connaît travaille dans les deux sens :

> **Concevoir une interface à partir de mots. Et ramener une interface en mots.**

---

## Le tableau de traduction

| Dans l'interface | Ce que cela signifie | En texte |
|---|---|---|
| **Curseur de la souris** | *je peux choisir* — l'espace du possible | l'ensemble des options à cet endroit |
| **Sélectionner** | *je veux cela* | un choix, une valeur |
| **Clic** | *je décide, je veux aller là* | **le prompt** — la réponse de l'utilisateur |
| **Champ, interrupteur, réglage** | une décision qui persiste | **Config** |
| **Réglages de tout le logiciel** | décisions valables partout | **Policies** |
| **Formulaire, masque de saisie** | un ensemble de décisions liées | **Template** |
| **Bouton qui lance quelque chose** | *maintenant, quelque chose se passe* | un **Skill** ou un **Workflow** est déclenché |
| **Ce qui se déroule ensuite** | la suite d'étapes | instructions dans le skill — ou un **script** |
| **Barre de progression** | *ça tourne, et où en est-on* | messages d'état dans le déroulement |
| **Message de succès, vue de résultat** | *voici ce qui est sorti* | le retour — dans l'interface simplement mieux présenté |
| **Projet** | un état de travail délimité | un **dossier** — et, comme il se trouve lui-même dans un dossier, partie du logiciel |
| **Vue, onglet, zone** | un état dans lequel on se trouve | une étape dans l'arbre de déroulement |

**La ligne centrale est le clic.** Un clic n'est rien d'autre que ce qu'un utilisateur dirait
dans une conversation — simplement plus vite. **Le clic est le prompt.** Et à un prompt
succède une réaction : une nouvelle question, une nouvelle vue, un nouvel état.

---

## Le déroulement est un arbre

Chaque application est une suite de décisions, entre lesquelles quelque chose se passe :

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

**Trois parties, toujours les mêmes :**

1. **Décisions** — si-alors, jusqu'à ce que tout le nécessaire soit réuni
2. **Exécution** — souvent pas dans l'outil lui-même, mais externalisée
3. **Retour** — le résultat remis à l'humain, dans sa langue

La troisième partie est la plus souvent sous-estimée lors de la conception. **La communication
passe par les sens** — par le texte, l'image, le son. Une interface la met en forme ; un skill
décrit *quoi* est signalé et *quand*.

---

## Le niveau intermédiaire : le blueprint

Entre « décrit » et « construit », il manque une étape. Elle s'appelle **Blueprint** et c'est
**un texte dont la disposition correspond à l'image** — un écran que l'on peut lire :

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

**Pourquoi cette étape apporte tant :**

Un blueprint est **à la fois lisible et visualisable**. L'humain retrouve son image, l'agent
voit des champs, des types et un ordre. Il se crée en quelques minutes, ne coûte rien et se
corrige dans la conversation — contrairement à une interface construite.

**Et à partir du blueprint, le skill découle presque de lui-même :**

> **Que doit savoir, pouvoir et faire l'agent — dans quel ordre —
> pour remplir ce blueprint ?**

Chaque champ devient une question. La disposition devient l'ordre. Ce qui est pré-rempli n'est
pas demandé. Ce qui figure comme bouton devient une étape. Ensuite, on enrichit ce que l'agent
doit savoir en plus — connaissances métier, limites, pièges.

**Trois niveaux donc :** description → **blueprint** → skill *(et de là tout aussi bien vers une
interface construite)*.

### Un champ vide est une question — et la question a un but

`[ 35 ] €` ressemble à un nombre. C'est pourtant une **demande de données adressée à un
humain**, et elle a une raison qui reste le plus souvent non dite :

> **Nous avons besoin de ce montant maximal, car c'est la condition sous laquelle on commande
> du tout.**

Le champ porte donc trois choses à la fois : **ce qui** doit y figurer, **pourquoi** il est
nécessaire, et **où il agira plus tard**. Dans une interface, cela se trouve dans la mise en
page et dans le texte d'aide. En texte, il faut l'écrire — sinon cela se perd.

**C'est pourquoi chaque blueprint doit être accompagné d'une légende des champs :**

| | |
|---|---|
| **Question** | la façon dont un humain la poserait |
| **Type** | nombre, texte, choix, liste, liste ordonnée, date … |
| **But** | à quoi la valeur servira plus tard — *« critère d'arrêt dans la cascade »* |
| **Précondition** | ce qui doit exister pour que le champ ait du sens |
| **Postcondition** | ce qui vaut une fois le champ rempli |
| **Si vide** | accepter silencieusement · fixer une valeur par défaut · redemander · bloquer |
| **Si faux** | message, question de précision, proposition de correction |

**Les deux dernières lignes sont celles que l'on oublie le plus souvent** — et qui causent le
plus de problèmes en exploitation. *« Le prix importe peu »* est une réponse valable et doit
être prévue comme telle, pas comme une erreur.

### Le champ est ouvert — la question restreint

Un champ vide est **tout et rien**, comme une fenêtre de contexte vide : une invitation à y
écrire n'importe quoi. Mais quoi ?

**La restriction ne vient pas du champ, mais de ce qui l'entoure** — le plus souvent du texte
qui le précède, le surplombe ou le jouxte :

> *« Quel montant maximal voulez-vous dépenser ? »*

Cette question restreint **sémantiquement et pragmatiquement**. Le champ lui-même accepte
toujours tout — et si quelqu'un exploite cette liberté, **il perd sa finalité**. C'est pourquoi
les conditions du champ interviennent : *uniquement des nombres*. Non pas parce que « trente-cinq »
serait incompréhensible, mais parce que c'est plus difficile à traiter et plus long à écrire.

**Il en découle la direction de travail : ce sont les questions qui dérivent les règles des
champs, et non l'inverse.** Celui qui fixe d'abord le type de données a déjà oublié la question.

Et la question porte généralement aussi le **but** — c'est pourquoi, chez les humains, une
icône d'information figure souvent à côté :

> *« Nous n'acceptons aucune offre dépassant ce prix. »*

Ce n'est pas de la politesse, mais la véritable signification du champ : **une préférence de
l'utilisateur qui agira plus tard comme une barrière stricte.**

### La frontière de contrôle — et pourquoi tout doit être transmis

Un champ entraîne une chaîne :

```
Feld „Höchstbetrag"
   → der Wert wird später gebraucht        (Zweck)
   → für eine Prüfung                       (Gate)
   → also muss der Gegenwert erhoben werden (neue Frage, an anderer Stelle)
   → diese Frage stellt niemand von uns     (sie steht im Prompt)
```

**C'est ici que passe la ligne décisive : avec le prompt, on quitte notre niveau de contrôle.**
Ensuite, il n'y a plus d'accès — ni relance, ni intervention, ni seconde chance.

Il faut donc transmettre **tout** ce qui est nécessaire de l'autre côté :

- **la valeur elle-même** — 35 €
- **l'instruction de demander la contrepartie** — demander le prix
- **ce qui vaut si elle est plus élevée** — refuser, remercier, clore poliment
- **ce qui vaut si aucune n'est donnée** — ne pas estimer, refuser
- **ce qui vaut si le correspondant ne veut pas parler à une machine** — demander un rappel
  personnel et renvoyer le numéro comme valeur

Le dernier point montre la direction à laquelle on pense le moins souvent lors de la conception :
**même le cas d'exception doit renvoyer une valeur**, sinon l'humain ne reçoit rien d'autre que
« cela n'a pas marché ».

### Le prompt est un skill généré

On voit ainsi ce qu'est réellement un prompt :

> **Un prompt est un skill que l'interface vient tout juste d'assembler** — à partir des
> décisions, clics et valeurs de cette seule exécution. Personnalisé, adapté au but, et contraint
> d'exprimer tout ce qui est voulu **en langage**.

Un skill fixe dit comment on fait *toujours*. Un prompt dit comment cela doit se dérouler
*cette fois-ci*. Les deux ont la même forme — l'un demeure, l'autre naît au moment et disparaît
ensuite.

**En pratique :** celui qui traite la construction du prompt comme un bricolage de blocs de texte
construit de mauvais prompts. Celui qui la traite comme une *génération de skill* — avec but,
règles, limites, exceptions et valeurs de retour — en construit de bons.

### Attendre n'est pas ne rien faire, c'est ne pas savoir

Après l'envoi, l'humain a remis le contrôle. Ce dont il a besoin n'est pas de la patience, mais de
**l'information** : *que se passe-t-il en ce moment ? où en sommes-nous ?*

L'agent reçoit cela de toute façon — il interroge l'avancement. **L'humain ne voit rien de tout
cela tant que personne ne le traduit.** C'est précisément le rôle des barres de progression, des
journaux qui défilent et des lignes d'état : ce ne sont pas des ornements, mais la traduction
d'un flux de données en quelque chose qu'un utilisateur en attente peut supporter.

### Le retour est un prompt en sens inverse

Le message de réussite n'est pas une clôture, mais une **remise en retour** :

> *« Voici le résultat de ta demande. »*

Ce n'est qu'à partir de là que l'humain peut évaluer et agir. Et c'est justement pour cela qu'il
doit être complet : *« Commandé — mais trois pizzas au lieu d'une. Heureusement que le numéro de
rappel figure ici, j'appellerai moi-même. »*

**Sans retour exploitable, personne ne peut poursuivre le traitement.** Un message qui dit seulement
« ça a marché » n'a pas refermé la boucle.

### Analyse des questions et des champs

Pour **chaque** élément d'un blueprint — champ, bouton, choix, affichage — les mêmes questions :

| | |
|---|---|
| **Qu'est-ce qui est voulu, et pourquoi ?** | l'intention derrière l'élément |
| **Que se passe-t-il à l'envoi ?** | traité immédiatement, ou d'abord enregistré ? |
| **Où et quand la valeur est-elle de nouveau nécessaire ?** | l'endroit où elle agit |
| **Combien de temps doit-elle être conservée ?** | au-delà du clic ? au-delà de l'exécution ? |
| **Que doit-il advenir de cette valeur ?** | vérifier, transmettre, afficher, rejeter |

Le montant maximal, par exemple, n'est **pas** nécessaire tout de suite. Il est enregistré,
transporté et n'agit qu'au cours de la conversation — il faut donc un endroit où il est conservé
et un point où il passe dans le prompt.

### Les aiguillages déterminent l'algorithme de questions

Un choix n'est que rarement une simple valeur. Souvent, c'est un **aiguillage** qui réorganise tout le
déroulement suivant :

| Mode | Première question dans la conversation | Ce qui disparaît | Ce qui s'ajoute |
|---|---|---|---|
| **Livraison** | *« Livrez-vous ici ? »* — un non termine tout de suite l'appel | — | adresse de livraison |
| **Retrait** | disparaît | la question de livraison | heure de retrait |
| **Table** | *« Êtes-vous ouverts, et une table est-elle libre à X h ? »* | tout le contrôle de prix | nombre de personnes, enfants, souhait de placement, période |

**L'ordre dans la conversation suit la force d'exclusion, non la curiosité.** Celui qui ne livre
pas n'a pas besoin qu'on l'interroge sur le repas — la condition la plus stricte vient
en premier, parce qu'elle mène le plus vite au candidat suivant.

Et : **beaucoup de choses restent identiques à travers les aiguillages.** Le montant maximal vaut
pour la livraison comme pour le retrait, la liste des candidats également. Seul l'algorithme de
questions change.

### Le cercle

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

**Le cas d'usage fonde les données, les données fondent les champs.** Celui qui commence par les
champs invente des formulaires. Celui qui commence par la volonté les reçoit en cadeau.

### Entre deux blueprints se trouve la causalité

Un blueprint est un **agencement statique**. Plusieurs blueprints à la suite ne forment pas encore
un déroulement — il se passe quelque chose entre les deux, et **cet entre-deux est la véritable
logique** : que se passe-t-il quand on clique ici ? Quel contrôle s'exécute ? Qu'est-ce qui est
enregistré ? Qu'est-ce qui est déclenché ?

Trois façons de rendre visible ce niveau temporel :

1. **Annotation dans l'image** — flèches et brèves notes entre les blueprints
2. **Paires avant/après** — le même extrait dans deux états, « avant le clic » et « après le clic »
3. **Mise par écrit** — préconditions et postconditions en texte sous l'image

La troisième voie porte le plus loin, parce qu'elle est exécutable. Les deux premières aident
l'humain à comprendre.

### Des champs découle le modèle de données

Celui qui décrit un champ « Ajouter un contact » a déjà décidé qu'il existe des destinataires, qu'ils
sont enregistrés et quelles informations en font partie. **Le tableau de données se règle sur les
champs, et non l'inverse.**

C'est pourquoi il vaut la peine de compléter la légende des champs avant de concevoir le moindre
schéma : chaque champ avec son type et son but est une colonne, chaque groupe répétable une table,
chaque relation entre champs une référence.

## Sens 1 : des mots vers une interface

**Lorsque le déroulement a d'abord été décrit.**

1. **Rassembler les décisions.** Chaque endroit où quelque chose est fixé. Trier au passage :
   - **Obligatoire** — sans cela, rien ne peut avancer → **champ obligatoire**
   - **Déductible** — peut provenir du contexte ou de l'existant → **champ pré-rempli** avec
     possibilité de correction
   - **Facultatif** — améliore le résultat → **zone repliable**
   - **Barrière** — irréversible, coûte de l'argent, atteint des personnes → **étape de confirmation**
2. **Regrouper ce qui va ensemble** → un masque, un template.
3. **Découper l'arbre en vues.** Un état = une vue.
4. **Concevoir les retours.** Quoi est signalé et quand ? Avancement, état intermédiaire,
   résultat.
5. **Fixer une fois ce qui vaut partout** — couleur, typographie, mise en page, mouvement.
   Ce sont les policies de l'interface.

**Le gain :** un formulaire né d'un déroulement de conversation est presque toujours plus épuré
qu'un formulaire conçu sur la planche à dessin. En formulant, on remarque quelle question est
superflue.

## Sens 2 : d'une interface vers des mots

**Lorsque l'application existe déjà ou a été décrite.**

1. **Formuler chaque clic comme une question.** Que demande réellement ce bouton à l'utilisateur ?
2. **Chaque champ comme entrée de config** — avec valeur par défaut, type et texte d'aide.
3. **Chaque vue comme étape** dans le déroulement.
4. **Chaque message comme retour** — que rapporte-t-il, et en quels termes ?
5. **Vérifier ce que l'interface sait implicitement** — ordres, verrous, dépendances qui ne sont
   écrits nulle part et ne résident que dans la mise en page. **C'est la partie la plus facile à
   perdre lors de la traduction.**

### Pourquoi ce sens est plus difficile — et comment le parcourir malgré tout

Le sens 1 est aisé, le sens 2 semble laborieux. Il y a une raison :

> **Un skill est du temps. Un écran est une surface.**
> D'abord ceci, puis cela — face à tout à la fois.

On ne traduit donc pas ligne par ligne, mais **on découpe un déroulement en surfaces**. L'arête de
coupe est toujours la même :

**Un écran naît là où le déroulement attend un humain.**

Tout ce qui se trouve entre deux points d'attente s'exécute de soi-même — cela ne devient **pas**
un écran, tout au plus une barre de progression. Celui qui construit une vue pour chaque étape
construit une cage à clics.

**Et les chaînes si-alors ?** Elles ne deviennent pas toutes visibles. Quatre cas :

| Nature de la condition | Ce qui en résulte |
|---|---|
| **L'humain la fixe** (« 35 € maximum ») | un **champ** — avant le démarrage |
| **Le système la vérifie** (« prix au-dessus de la limite ») | un **résultat** — après coup, avec justification |
| **Elle modifie ce que l'humain voit** (« aucun résultat ») | un **état** du même écran, pas un nouvel écran |
| **Elle relève de la pure mécanique** (répétitions, dépassements de délai, contrôle de format) | **rien du tout** — elle reste invisible |

**Le quatrième cas est le plus fréquent.** La plupart des embranchements d'un script n'ont jamais
leur place sur un écran. Celui qui les montre quand même confond organigramme et interface.

**Concrètement, en quatre étapes :**

1. **Marquer les points d'attente** — chaque endroit où un humain décide, confirme ou saisit
   quelque chose. Ce sont les écrans, et ils sont généralement étonnamment peu nombreux.
2. **Récolter à rebours** — qu'est-ce qui doit être connu avant ce point d'attente ? Ces valeurs
   sont les champs de l'écran.
3. **Récolter vers l'avant** — que se passe-t-il ensuite, et qu'est-ce que l'humain doit en
   apprendre ? C'est le retour.
4. **Omettre le reste** — tout ce qui n'est ni saisie ni message reste invisible.

---

## Le gradient : skill ↔ script

```
weit von der Software                                    nah an der Software
   Skill trägt alles                                    Skript trägt alles
        │                                                       │
   ausführlicher Text          ────────────►         knappe Bedienungsanleitung
   jeder Schritt erklärt                             „ruf dies auf, dann jenes"
   funktioniert ohne Werkzeug                        funktioniert nur mit Werkzeug
```

**Plus un processus est automatisé, moins le skill a besoin d'expliquer.** Il devient plus court et
plus concret — à terme, il n'est guère plus qu'un mode d'emploi des scripts : *quand utiliser cet
outil, qu'y mettre, à quoi reconnaître qu'il a réussi.*

Deux conclusions inverses, utiles au quotidien :

- **Si un skill devient trop long, il manque un script.** La longueur est un signal : ce qui se
  répète et relève de la mécanique doit être automatisé.
- **Si un script devient incompréhensible, il manque un skill.** Un outil sans texte explicatif
  n'est utilisable que par celui qui l'a construit.

---

## La monnaie commune

**Chaque réglage existe en triple exemplaire** — comme valeur de config, comme question dans le
skill, comme champ dans l'interface. Pour qu'ils ne divergent pas, la représentation est décrite
**une seule fois** et lue par les trois :

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

**Ce qui est `locked` n'apparaît nulle part comme option.** Certaines choses ne sont pas des
réglages, mais une partie de l'ossature.

---

## Quand ce skill aide

- Une application est conçue et le déroulement est encore flou → **sens 1**
- Un outil existant doit devenir utilisable par des agents → **sens 2**
- L'interface et l'accès des agents divergent → introduire une **monnaie commune**
- Un skill devient trop long et personne ne sait pourquoi → vérifier le **gradient**
- Un échange de conception doit être consigné avant de s'évaporer → tableau + arbre

## Liens connexes

`condition` traduit conditions, moments et ordres en barrières vérifiables
(`/if`, `/when`, `/after`, `/and`, `/or`) — le même mouvement pour le cas particulier du pilotage de déroulement.
`skill-extractor` dégage des skills à partir des fils de conversation. `plugin-system` rend
des scripts propres retrouvables.
