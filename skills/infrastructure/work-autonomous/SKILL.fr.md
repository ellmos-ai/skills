---
name: work-autonomous
version: 1.5.1
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-09
description: "Condition d'arrêt pour les boucles autonomes : continuer à travailler de façon autonome autant que possible ET ne terminer une boucle que lorsqu'il est établi qu'aucune tâche exécutable de manière autonome ne subsiste. La simple impression « rien d'autre à faire » ne suffit PAS : elle déclenche une chaîne de vérification en quatre étapes (think/decide, _CONTROL/_DECISIONS, Gardener/USMC, decision-avatar/BYUM), qui doit d'abord GAGNER de nouvelles tâches avant que la boucle puisse se terminer. Chaque étape de la chaîne signale found/empty/unavailable au lieu d'un résultat binaire. « exhausted » n'est signalé que si TOUTES les sources ont effectivement pu être interrogées ; si au moins une source est unavailable, le skill signale « blind » au lieu de « exhausted » et n'affirme rien de non vérifié. Utilisez ce skill avec /work-autonomous, /waafap, « continue de travailler de manière autonome jusqu'à ce qu'il n'y ait plus rien à faire », comme condition de but dans une /loop, ou lorsqu'il faut vérifier s'il reste réellement du travail autonome avant qu'une boucle ou une session ne se termine."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: fr
status: active
visibility: public
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: a8ee248e73bb81d9af36df2f3e82719bed0f31e89005ab64c35f4e236b15600c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — Ne terminer la boucle que lorsqu'il est établi qu'aucune tâche autonome ne subsiste

## Objet

Ce skill poursuit deux objectifs simultanément :

1. **Continuer à travailler de façon autonome autant que possible** — un travail de session tout à fait ordinaire, rien de particulier.
2. **Ne terminer une boucle que lorsqu'il est ÉTABLI** qu'il n'existe plus aucune tâche exécutable de manière autonome. Le soupçon « je ne trouve plus rien à faire » n'est **pas** un motif d'arrêt ; c'est le **déclencheur** d'une chaîne de vérification qui essaie d'abord de **gagner** de nouvelles tâches. Ce n'est que si cette chaîne reste entièrement sans résultat que l'arrêt est considéré comme établi.

**Volontairement sans `/goal` intégré :** Le skill est utilisable de manière autonome (p. ex. directement comme appel `/work-autonomous` au sein d'une session normale) et également comme condition au sein d'une construction de boucle englobante : attribuer `/loop` normalement, puis ne nommer que ce skill comme but. Le but se formule alors en substance ainsi : *« Termine la boucle lorsqu'il n'existe plus de tâches autonomes — et continue de travailler de manière aussi autonome que possible jusque-là. »* Le skill lui-même n'appelle aucune construction `/goal` ; il fournit seulement le signal d'arrêt sans ambiguïté qu'une telle construction peut lire (voir « Signal d'arrêt » ci-dessous).

## Modèle opérationnel — deux niveaux

### Niveau 1 — Travail courant (chaque tick)

#### Porte d'admission TICKET-MASTER (priorité sur tout le reste à ce niveau)

**Pertinent uniquement si un système de tickets (`_TICKETS/`) fait partie du contexte** — les sessions sans système de tickets ignorent purement et simplement cette porte ; le skill reste utilisable de manière autonome sans aucun système de tickets (voir « Objet » ci-dessus). Il faut d'abord vérifier si `INBOX/` — y compris les entrées informelles, pas encore mises au format ticket — est entièrement formalisé et trié. Si ce n'est pas le cas, cela compte précisément comme travail autonome trouvé (formaliser et trier est une tâche administrative sans décision de l'utilisateur, voir la délimitation ci-dessous) : l'effectuer ; le tick se termine, le niveau 2 n'est pas abordé, comme pour toute autre source de niveau 1.

**Tant que la INBOX est ouverte, NE DOIVENT PAS apparaître `NO_WORK`, un signal d'épuisement (`exhausted`/`blind`), un STOP de garde ni aucun autre signal d'arrêt.** Ce n'est que lorsque l'admission est entièrement triée que `ACTIONABLE`, les `BLOCKED` débloqués et les `WAITING` échus (ci-dessous) — puis, le cas échéant, le niveau 2 — peuvent être vérifiés.

*Cas documenté :* une boucle a commencé la vérification d'épuisement après le traitement de `ACTIONABLE`, alors que de nouveaux tickets `INBOX` arrivaient en continu, dont deux de priorité P1. Sans cette porte, la boucle aurait signalé `exhausted`/`blind` alors que l'entrée était ouverte ; c'est précisément ce qu'empêche la porte.

Ensuite, rechercher normalement d'autres travaux exécutables de manière autonome (voir la délimitation ci-dessous) et les effectuer : tickets `ACTIONABLE` ouverts, tickets `BLOCKED` débloqués, tickets `WAITING` échus, points `TODO.md`/`AUFGABEN.txt` ouverts dans les projets sans dépendance à l'utilisateur, contrôles de routine ou d'hygiène échus selon la politique locale, travail commencé mais non achevé lors de la dernière session (USMC `working`), **exécutions `tidy-up` échues du projet actif** (complément 1.3.0, 2026-08-19 — voir le skill `tidy-up` : passage Tasksolver+Writer+Maintainer sur le dossier de projet dans lequel la session travaillait ; l'échéance est vérifiée par `tidy-up` lui-même via son propre journal USMC allégé, voir la section correspondante « Relation avec work-autonomous »).

→ **Trouvé et traité :** signaler brièvement le résultat, le tick se termine, la boucle se poursuit normalement. Le niveau 2 n'est PAS abordé : aucune des quatre étapes de vérification coûteuses n'est nécessaire tant qu'un travail visible existe.

### Niveau 2 — Contrôle d'épuisement (uniquement en cas de soupçon « rien d'autre à faire »)

Ce n'est que lorsque le niveau 1 ne trouve plus **rien** d'autonome que naît le soupçon. Ce soupçon seul ne suffit pas. La chaîne suivante s'exécute alors **obligatoirement** afin de **gagner** de nouvelles tâches.

#### Auto-connaissance (avant la chaîne, et non après)

Avant d'interroger quoi que ce soit, le skill déclare QUELLES sources il lui faut pour son jugement. Quatre besoins (`grounding_seed.self_knowledge.Need`, si `grounding-seed` est installé ; sinon la même liste vaut comme simple déclaration sans rattachement à une bibliothèque) :

| Rôle | Étape de la chaîne | Ce qui se cache derrière |
|---|---|---|
| `decisions.ledger` | 2 | registre central des décisions |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide` (étape 1) n'est délibérément PAS une source déclarée.** Il s'agit de l'analyse propre du modèle, pas d'un système externe qui pourrait être joignable ou non ; il est toujours « disponible » au sens de cette distinction. Seules les étapes 2 à 4 peuvent devenir `unavailable`.

Outil optionnel et testable pour la seule question de localisation (found/unavailable, SANS contrôle du contenu pour l'instant) : `scripts/exhaustion_check.py` dans le dossier de ce skill. Il utilise `grounding_seed.resolve()` + `status_from_resolution()` pour `decisions.ledger`/`user.model` (il existe là un véritable fournisseur `source-resolver`). Il vérifie en revanche `memory.organic`/`memory.curated` **toujours** directement par joignabilité CLI (`gardener`/`usmc` dans le PATH). Pour ces deux rôles, il n'existait pas encore, jusqu'au 2026-08-15, de fournisseur `source-resolver` enregistré ; les interroger via le résolveur n'aurait fait que signaler `unavailable`, indépendamment du fait que Gardener/USMC soient réellement installés. Il fonctionne de manière identique avec ou sans `grounding-seed` installé.

**Mise à jour 2026-08-25 (K3=C, `T-20260825-342866657`) :** La lacune est comblée. `source-resolver` enregistre désormais `memory.organic` (Gardener) et `memory.curated` (USMC) comme rôles de niveau 1, avec le même contrôle de présence CLI (`shutil.which("gardener")`/`shutil.which("usmc")`) que ce script codait jusqu'ici en dur. `exhaustion_check.py` n'a donc PAS été modifié immédiatement (aucune perte de fonction, le contrôle existant reste correct). Lors du prochain passage de maintenance du skill, l'étape 3 pourra être basculée sur `source_resolver.resolve("memory.organic"/"memory.curated")`, par analogie avec l'étape 2 (`decisions.ledger`), au lieu de maintenir le contrôle CLI en double.

#### Les quatre étapes de la chaîne — chacune signale found | empty | unavailable

Chaque étape se déroule en deux temps : d'abord la **localisation** (connais-je seulement un emplacement joignable ?), puis, uniquement si la source est localisée, la **vérification du contenu** (le modèle relit réellement s'il y a quelque chose de nouveau, avec ses propres outils). Une source qui n'a pas pu être localisée n'est JAMAIS vérifiée quant à son contenu : elle compte comme `unavailable`, et non comme `empty`.

1. Appliquer **`/think` + `/decide`** à la question : « Existe-t-il vraiment encore du travail exécutable de manière autonome, ou est-ce que je passe quelque chose à côté ? » — analyse structurée au lieu d'une impression intuitive. Pas de statut found/empty/unavailable (voir ci-dessus, pas de source).
2. **`decisions.ledger`** — localisation via `source_resolver.resolve("decisions.ledger")` / `grounding_seed.resolve(...)`, si installé ; sinon le chemin de repli connu (`_control-center/_CONTROL/_DECISIONS/`, chaîne `TO-DECIDE-USER*.txt`, `TO-DECIDE-USER-<HOST>.txt` propre à l'hôte, `DECIDED-AND-DONE.md`). Localisé → lire le contenu : des décisions ont-elles récemment été prises qui débloquent un travail auparavant bloqué ou en attente de validation ? Résultat → `found`. Lu, rien de nouveau → `empty`. Non localisable (résolveur absent ET chemin de repli inexistant) → `unavailable`.
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — deux sources distinctes, une seule étape de la chaîne. Localisation : CLI dans le PATH (`gardener`/`usmc`), voir l'auto-connaissance ci-dessus. Joignable → lire le contenu (`find()`/`recall()` ou `usmc facts|lessons|working|context`) : points ouverts de la mémoire de travail, leçons avec une tâche de suivi non effectuée, faits suggérant un travail passé inaperçu mais exécutable (c'est exactement l'endroit où les sessions antérieures laissent des points inachevés : champ `RESUME:`, entrées `note` ouvertes). Résultat → `found`. Lu, rien de nouveau → `empty`. CLI absent du PATH → `unavailable`.
4. **`user.model` (decision-avatar/BYUM)** — localisation comme pour `decisions.ledger` (résolveur ou chemin de repli `_control-center/_CONTROL/_USER-MIND/`). Localisé → vérifier le contenu : existe-t-il un schéma avéré selon lequel l'utilisateur souhaitait voir une action précise accomplie de manière autonome à cet endroit ? Ne compter comme `found` qu'avec une confiance suffisante (🟢/🟡) ; 🔴 compte comme `empty`, non comme tâche gagnée, mais comme point ouvert pour l'étape « Reste réservé à l'utilisateur » ci-dessous. Non localisable → `unavailable`.

**« Exhausted » ne peut être signalé que si les QUATRE sources (étapes 2–4, trois étapes, quatre rôles) ont effectivement PU être interrogées, soit `found` soit `empty`, aucune `unavailable`.** Cela correspond à `grounding_seed.self_knowledge.GroundingReport.all_answerable()`. Si au moins un rôle est `unavailable`, il ne faut PAS signaler « exhausted », mais le signal propre « blind » (voir le signal d'arrêt ci-dessous) : la boucle se termine néanmoins (elle ne peut de toute façon rien interroger), mais elle n'affirme plus avoir vérifié ce qu'elle n'a pas pu contrôler.

Si une étape trouve du nouveau travail → retour au niveau 1, exécution du travail, positionnement de l'état du garde (voir ci-dessous) sur « found » au lieu de « exhausted » ou « blind ».

### Cas particulier : seulement des restes liés à l'utilisateur

Si la chaîne ne trouve plus **aucune** tâche autonome, mais que des tickets `USER/*` ou des points `_DECISIONS` non tranchés restent ouverts, cela constitue néanmoins un **STOP pour l'autonomie**, mais pas « rien à faire » : plutôt « rien à faire *de manière autonome* ». Ces points sont présentés **regroupés** selon la règle de boucle autonome issue de `ticket-master` (un seul modèle de synthèse, pas de relances individuelles), sans être redemandés un par un. Le signal d'arrêt distingue expressément ce cas d'un véritable vide.

## Délimitation — qu'est-ce qui compte comme « exécutable de manière autonome » ?

Référence : catégories `ticket-master` (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`).

| Cas | Autonome ? | Justification |
|---|---|---|
| `INBOX/`, y compris entrées informelles, sous TICKET-MASTER (avant triage) | **Oui, avec priorité** | Formaliser et trier est une tâche administrative sans décision de l'utilisateur ; passe avant `ACTIONABLE`/`BLOCKED`/`WAITING` et bloque jusque-là tout signal d'arrêt (voir la porte d'admission ci-dessus). |
| Ticket `ACTIONABLE` | **Oui** | Aucun bloqueur, aucune dépendance à l'utilisateur, par définition. |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | Non, tant que le bloqueur n'a pas été **empiriquement** levé | Une revérification périodique est autorisée (boucle autonome), mais « présent » ne suffit pas comme preuve : une preuve est nécessaire. |
| `WAITING/*` (scheduled, review-due, marker) avant échéance ou marqueur | Non | Lié à une échéance. |
| `WAITING/*` après l'échéance ou l'arrivée du marqueur | **Oui** | Condition remplie → passe dans `ACTIONABLE`. |
| `USER/*` (decision, data, freigabe, hardware, session) | **Jamais autonome** | Requiert impérativement une décision, des données, une validation (freigabe), du matériel ou une session de l'utilisateur. Présenter groupé, voir ci-dessus. |
| `PARKED/*` (skip, backlog, until-trigger) | Non, sauf ordre ou déclencheur explicite | Volontairement mis de côté, pas de revérification automatique. |
| Points `TODO.md`/`AUFGABEN.txt` ouverts sans mention de validation ou de décision | **Oui** | Registre de projet, travail normal. |
| Contrôles de routine ou d'hygiène échus (cooldown écoulé, pas de verrou) | **Oui** | Travail de maintenance régulier selon la politique locale. |
| Zones verrouillées par `LOCK.user.*` | **Jamais** | Verrou utilisateur ; seul l'utilisateur le lève, voir LOCK-SYSTEM. |
| Étapes irréversibles ou à effet externe sans validation par la politique (envoi Zenodo, push sur des branches évaluées (« gejudgte ») ou protégées, décision de dépense serveur au-delà du seuil du portable, suppression définitive sans aperçu) | **Non** | Nécessite une validation ou décision, même si techniquement exécutable. |
| Session démarrable uniquement via GUI ou connexion (p. ex. tâche Claude Desktop, connexion interactive, manipulation physique du matériel) | **Jamais** | « Session démarrable uniquement par l'utilisateur » : aucune boucle ne peut la prendre en charge. |

Règle empirique : est autonome ce qui peut être mené à son terme **sans** décision, validation, données, matériel ou session de l'utilisateur, ET qui ne requiert aucune action irréversible ou à effet externe sans validation documentée de la politique.

## Garde contre les boucles sans fin (obligatoire)

**Problème :** sans frein, la chaîne en quatre étapes repartirait entièrement à chaque nouvelle vérification, alors que rien n'a changé depuis le dernier passage sans résultat. C'est coûteux et inutile, surtout lorsque le skill est appelé à plusieurs reprises (boucle, tâche planifiée, nouvel appel manuel peu après).

**L'état est persisté dans USMC** (sur ce système, l'état de processus relève de là, et non de fichiers Markdown) :

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```


**L'empreinte (fingerprint) se compose de DEUX éléments : la situation ET la joignabilité :**

1. **Élément de situation** (comme auparavant) : nombre et identifiants des tickets `ACTIONABLE` ouverts, mtime de la chaîne `_DECISIONS` (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), nombre de nouvelles entrées USMC `working` depuis le dernier passage de la chaîne.
2. **Élément de disponibilité (nouveau, obligatoire depuis 1.2.0) :** le tuple trié des rôles actuellement signalés `unavailable` lors de la vérification d'auto-connaissance (`exhaustion_check.availability_fingerprint_component()`), p. ex. `("memory.organic",)` ou `()`.

**Pourquoi le second élément est obligatoire : « sinon le garde hérite de la lacune » :** sans lui, l'empreinte (élément 1) repose notamment sur le mtime de la chaîne `_DECISIONS`. Si cette chaîne manque entièrement sur un système, cette part de l'empreinte reste constante à jamais : un `exhausted`/`blind` posé à tort ne serait alors JAMAIS revérifié, même si `source-resolver` est installé plus tard ou si `_control-center/_CONTROL/_DECISIONS/` est créé. L'élément de disponibilité corrige précisément ce point : si change la liste des rôles QUI sont unavailable (une source apparaît ou disparaît), l'empreinte change automatiquement. Le garde le détecte au prochain appel et relance la chaîne. C'est une « transplantation » au sens de la métaphore d'ancrage (grounding, T-20260815-371628859) : un changement d'environnement déclenche une nouvelle recherche, sans que quiconque doive réinitialiser manuellement le garde.

**Déroulement avant chaque passage de la chaîne :**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result in ("exhausted", "blind")
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:      # Lage- UND Verfügbarkeits-Baustein
       → Kette NICHT erneut fahren.
       → guard.result == "exhausted":
           Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                    Kein neuer Trigger. STOP (Guard aktiv, exhausted unchanged since …)."
       → guard.result == "blind":
           Melden: "Weiterhin blind (Quellen nicht verfügbar) — unverändert seit {guard.timestamp}.
                    STOP (Guard aktiv, blind unchanged since …)."
sonst:
       → Kette vollständig fahren (Selbstkenntnis-Prüfung + alle vier Kettenschritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|blind|found).
       → alle vier Quellen befragbar UND alle empty → exhausted → STOP (belegt).
       → mindestens eine Quelle unavailable → blind → STOP (nicht belegt, nur unerreichbar).
       → mindestens eine Quelle liefert einen Treffer → found → zurück zu Ebene 1, Arbeit erledigen.
```


Un seul passage de chaîne entièrement exécuté, au cours duquel les QUATRE sources étaient interrogeables et AUCUNE n'a donné de résultat, suffit comme preuve de « plus aucune tâche autonome » (exigence du ticket : « seulement lorsque TOUTES les étapes d'un passage restent sans résultat » ; sans résultat signifie ici expressément `empty`, et non `unavailable`). Le garde n'empêche pas le constat lui-même, mais seulement le **nouveau constat répété et inchangé** lors d'appels rapprochés successifs, et ce pour `exhausted` ET pour `blind` séparément, sans jamais les confondre.

`GUARD_INTERVAL` est configurable (valeur par défaut : 15 minutes). Dans un environnement très calme (nouveaux tickets ou décisions rares), on peut choisir une valeur plus longue ; dans un environnement très actif, une valeur plus courte.

## Signal d'arrêt

Chaque passage se termine par **une** ligne unique, exploitable par grep, afin qu'une `/loop` englobante ou une future construction `/goal` puisse y lire s'il faut continuer :

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```


`CONTINUE` est le seul signal pour lequel une boucle englobante doit déclencher un tick supplémentaire. Toutes les variantes `STOP` constituent l'arrêt établi, avec indication du cas considéré.

**La différence entre `exhausted` et `blind` est essentielle pour l'utilisateur, et non cosmétique :** `exhausted` signifie « j'ai tout vérifié de ce qui devait l'être, le travail est terminé ». `blind` signifie « il me manque l'infrastructure pour vérifier quoi que ce soit : ce n'est pas un état du travail, mais une lacune ». Une construction `/loop`/`/goal` qui traite les deux de la même façon (la boucle se termine dans tous les cas) ne doit pas les SIGNALER à l'utilisateur de manière identique, sinon disparaît précisément l'information que T-20260815-205101335 réclamait.

## Relation avec d'autres skills

- **`think`/`decide`** — fournissent l'analyse ou la décision structurée de l'étape 1 de la chaîne. Ils sont appelés ici comme briques, sans être réinventés.
- **`decision-avatar`** (ce skill, neutre vis-à-vis de l'utilisateur) — fournit l'étape 4 de la chaîne. Sur les systèmes disposant d'un profil concret et autorisé, cela correspond à `user-model` + `build-your-users-mind`.
- **`orchestrator`** — règle COMMENT déléguer à des sous-agents et comment contrôler leur signalement d'achèvement. `work-autonomous` règle QUAND on cesse du tout de chercher ; les deux sont combinables (l'orchestrateur peut intervenir comme partie du travail effectué au niveau 1).
- **`bugsweep`** — un exemple d'un autre protocole de recherche auto-limitant (escalade par doublement au lieu de la chaîne en quatre étapes). `work-autonomous` est plus générique : il ne vérifie pas seulement le code à la recherche de bugs, mais chaque source de travail autonome.
- **Catégories de tickets (`ticket-master`)** — fournissent le vocabulaire de « exécutable de manière autonome » (voir le tableau de délimitation) et le modèle de la boucle autonome (revérification BLOCKED, regroupement USER, report à l'échéance WAITING, arrêt PARKED).
- **`tidy-up`** (depuis 1.3.0) — fournit une source supplémentaire de niveau 1 : le passage unique Tasksolver+Writer+Maintainer pour le dossier de projet en cours de traitement. Il vérifie lui-même son échéance (journal USMC allégé, pas de garde à quatre étapes comme ici) ; `work-autonomous` ne l'appelle que comme l'une de plusieurs sources de niveau 1, sans dupliquer sa logique.

## Exemple de déroulement

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Selbstkenntnis + Kette 1–4 läuft.
        → Schritt 2 (decisions.ledger): verortet, DECIDED-AND-DONE.md hat einen neuen Eintrag
          seit 10 Min. → found, daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar. Voll ausgestattetes System (Gardener, USMC, _DECISIONS, BYUM alle da).
        → Ebene 2: alle vier Quellen verortet UND befragt, alle vier empty.
        → Guard: result=exhausted, fingerprint=FP1 (Lage + Verfügbarkeit ()), timestamp=T1.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since T1)

Gegenbeispiel — System OHNE Gardener/USMC (der Kernfall aus T-20260815-205101335):
Tick 1: Nichts sichtbar. Selbstkenntnis-Prüfung: decisions.ledger verortet (leer, empty),
        memory.organic/memory.curated NICHT verortet (CLI fehlt) → unavailable,
        user.model verortet (empty).
        → nicht alle vier Quellen befragbar → KEIN exhausted.
        → Guard: result=blind, fingerprint=FP2 (Verfügbarkeit ("memory.curated","memory.organic")).
        → WORK-AUTONOMOUS: STOP (blind, 2/4 Quellen nicht verfuegbar: memory.organic, memory.curated)
Tick 2 (Nutzer installiert grounding-seed + usmc auf diesem System):
        → Selbstkenntnis-Prüfung: memory.curated jetzt verortet (CLI auf PATH) → Verfügbarkeits-
          Baustein ändert sich zu ("memory.organic",) → fingerprint(jetzt) != FP2.
        → Guard erkennt Änderung, Kette läuft neu (Verpflanzung) — ohne dass jemand den Guard
          manuell zurückgesetzt hätte.
```


## Journal des modifications

### 1.5.1 (2026-09-09)
- T-20260909-282509082 : Le repli documenté pour `decisions.ledger` et `user.model` suit le déménagement avéré du Control Center vers `_CONTROL/_DECISIONS` et `_CONTROL/_USER-MIND`. La priorité du résolveur et le comportement fail-closed restent inchangés.

### 1.5.0 (2026-09-09)
- P-018 : Les rapports de travail, handoffs et receipts importants nouvellement créés et conservés durablement se terminent par `session: <session-id> | <agent>@<host> | YYYY-MM-DD`. La priorité des sources est : indication explicite d'exécution ou CLI, puis environnement ou hook du fournisseur faisant autorité, puis `unbekannt` ; les valeurs ne sont jamais devinées, et les sous-agents utilisent la session parente. Les échanges de routine, les sources, les policies, `CLAUDE.md`, les README et les fichiers anciens sont exclus de tout horodatage global ou rétroactif.

### 1.4.0 (2026-09-03)
- Ajout minimal issu du ticket T-20260902-729068782 : nouvelle **porte d'admission TICKET-MASTER** au niveau 1 (priorité sur `ACTIONABLE`/`BLOCKED`/`WAITING`), pertinente uniquement si un système de tickets fait partie du contexte. Tant que `INBOX/` (y compris les entrées informelles) n'est pas entièrement trié, aucun `NO_WORK`, signal d'épuisement ou STOP de garde ne doit apparaître. Cas documenté : une boucle a commencé la vérification d'épuisement alors que `INBOX` contenait encore des entrées ouvertes (dont deux tickets P1). La chaîne d'épuisement en quatre étapes, le garde et l'utilisabilité hors TICKET-MASTER restent inchangés : la porte n'agit qu'au niveau 1 et uniquement sous TICKET-MASTER.
- Nouvelle fonction auxiliaire testée `scripts/exhaustion_check.py::intake_gate_blocks_stop()` + tests de régression dans `tests/test_exhaustion_check.py` (orientés comportement : la porte bloque si la INBOX est ouverte, elle se libère si la INBOX est vide).

### 1.3.0 (2026-08-19)
- Ajout minimal issu du ticket T-20260819-461890468 (nouveau skill `tidy-up`) : le niveau 1 reçoit une source supplémentaire et autonome, « exécutions `tidy-up` échues du projet actif » (passage Tasksolver+Writer+Maintainer, voir le skill `tidy-up`). Pas de nouvelle étape de chaîne, aucune modification du niveau 2, du garde ou du signal d'arrêt : `tidy-up` vérifie lui-même son échéance via un journal USMC allégé et n'est ici référencé que comme source supplémentaire de niveau 1, par analogie avec les sources déjà existantes (tickets, TODO/AUFGABEN, contrôles de routine, USMC `working`). Ainsi, les points `tidy-up` comptent comme tâches à exécuter de manière autonome au sens d'une construction `/goal` combinant `/work-autonomous` + `/tidy-up` (cas d'usage central du ticket). Aucune modification de la chaîne d'épuisement en quatre étapes ni du garde : le niveau 2 reste inchangé.

### 1.2.0 (2026-08-15)
- Retrofit issu du ticket T-20260815-205101335 (mandat d'examen : « vérifier si la solution tient dans ce contexte avec la métaphore du grounding »). Constat sur le skill livré : elle tenait sur trois points, mais PAS sur la distinction « interrogé et vide » vs. « n'a pas pu être interrogé du tout » : la chaîne signalait `STOP (exhausted)` aussi sur des systèmes sans Gardener/USMC/`_DECISIONS`, sans l'avoir jamais vérifié. Premier cas d'usage réel de `grounding-seed`, ticket T-20260815-371628859.
- **Auto-connaissance ajoutée :** quatre besoins déclarés (`decisions.ledger`, `memory.organic`, `memory.curated`, `user.model`) avant la chaîne, au lieu de chercher à l'aveugle à quatre emplacements fixes.
- **Chaque étape de la chaîne (2–4) signale found | empty | unavailable** au lieu d'un résultat binaire, en deux temps : localisation d'abord (`grounding-seed`/`source-resolver` pour `decisions.ledger`/`user.model`, contrôle CLI direct pour `memory.organic`/`memory.curated`, qui n'ont pas encore de fournisseur `source-resolver`), vérification du contenu uniquement en cas de localisation réussie.
- **`exhausted` ne s'applique plus que si les quatre sources étaient effectivement interrogeables** (toutes found/empty, aucune unavailable). Nouveau signal distinct `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)` pour le cas où au moins une source était injoignable : la boucle se termine néanmoins, mais n'affirme plus de résultat vérifié.
- **Empreinte du garde complétée par un élément de disponibilité** (tuple trié des rôles actuellement unavailable). Corrige le constat de suivi « le garde hérite de la lacune » : sans cet élément, un `exhausted`/`blind` posé à tort reste valable à jamais si la chaîne `_DECISIONS` manque entièrement (la part existante de l'empreinte est alors constante). Avec cet élément, une source devenue disponible déclenche automatiquement un nouveau passage de la chaîne (transplantation au sens de la métaphore d'ancrage).
- Nouveau script auxiliaire testé `scripts/exhaustion_check.py` (+ `tests/test_exhaustion_check.py`, 11 tests, les deux modes de fonctionnement vérifiés : avec et sans `grounding-seed` installé) : fournit de façon déterministe la vérification d'auto-connaissance et de localisation, afin que le skill n'ait pas à la redeviner à chaque exécution. Reste optionnel : le skill demeure avant tout un protocole que suit un modèle avec ses propres outils.
- Dépendance : `grounding_seed.self_knowledge.assess()`/`status_from_resolution()` depuis `grounding-seed` 0.2.0. Les états plus anciens de `grounding-seed` (0.1.0) comportaient une erreur de catégorie (`not_found` était à tort devenu `empty`), qui aurait précisément brouillé la distinction corrigée ici. Sans `grounding-seed` installé, le repli documenté fonctionne de manière identique.

### 1.1.0 (2026-08-15)
- Retrofit de référence issu du ticket T-20260815-385400870 : l'étape 2 (registre des décisions) résout désormais son emplacement via le rôle `decisions.ledger` (`source_resolver.resolve(...)`, module `source-resolver`), au lieu de le câbler en dur, avec un repli documenté sur le chemin précédent si le résolveur n'est pas installé. Comportement fonctionnel inchangé.

### 1.0.0 (2026-08-15)
- Première version issue du ticket T-20260815-522639345 : modèle opérationnel à deux niveaux, chaîne de vérification en quatre étapes, tableau de délimitation selon les catégories `ticket-master`, garde contre les boucles sans fin appuyé sur USMC, signal d'arrêt sans ambiguïté pour les constructions `/loop`/`/goal`.
