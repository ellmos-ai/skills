---
name: design-taste-frontend
description: "Skill frontend anti-slop pour les pages d'atterrissage, les portfolios et les refontes. L'agent lit le brief, déduit la bonne direction de design et livre des interfaces qui n'ont pas l'air de modèles génériques. Systèmes de design réels lorsque c'est pertinent, audit préalable pour les refontes et vérification pré-vol stricte."
third_party: true
license: MIT
upstream: https://github.com/Leonxlnx/taste-skill
category: dev
language: fr
translated_from_sha256: 7616ab6689efd139d313f95808165c7e4752bd39d50ed6a0533a120b8ff81002
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T06:39:14.326129+00:00"
---
<img src="banner.png" width="100%" alt="taste-skill banner">

# tasteskill : Skill Frontend Anti-Slop

> Pages d'atterrissage, portfolios et refontes. Pas de tableaux de bord, pas de tableaux de données, pas d'interfaces produit en plusieurs étapes.
> Chaque règle ci-dessous est **contextuelle**. Aucune ne s'applique automatiquement. Lisez d'abord le brief, puis ne retenez que ce qui convient.

---

## 0. DÉDUCTION DU BRIEF (Lire la situation avant tout le reste)

Avant de toucher au code ou de régler les cadrans, **déduisez ce que l'utilisateur veut réellement**. La plupart des productions de design par LLM sont mauvaises parce que le modèle adopte une esthétique par défaut au lieu de lire la situation.

### 0.A Lisez d'abord ces signaux
1. **Type de page** - atterrissage (SaaS / grand public / agence / événement), portfolio (développeur / designer / studio créatif), refonte (préserver ou refonte complète), éditorial / blog.
2. **Mots d'ambiance** employés par l'utilisateur - « minimaliste », « calme », « style Linear », « Awwwards », « brutaliste », « grand public premium », « façon Apple », « ludique », « B2B sérieux », « éditorial », « agence », « effet verre », « tech sombre ».
3. **Signaux de référence** - URL fournies, captures d'écran collées, produits cités, marques concurrentes.
4. **Audience** - jury d'achats B2B, consommateur sensible au design, recruteur qui parcourt un portfolio. L'audience choisit l'esthétique, pas votre goût.
5. **Actifs de marque existants** - logo, couleurs, typographie, photographies. Pour les refontes, ce sont des matériaux de départ, pas des données facultatives (voir la section 11).
6. **Contraintes implicites** - publics privilégiant l'accessibilité, secteur public, industries réglementées, commerce axé sur la confiance, produits pour enfants. Ces contraintes **PRIMENT** sur la préférence esthétique.

### 0.B Produisez une « Lecture de design » d'une ligne avant de générer
Avant tout code, énoncez en une ligne : **« Lecture de ce brief : \<page kind> pour \<audience>, avec un langage \<vibe>, penchant vers \<design system or aesthetic family>. »**

Exemples de lectures :
- *« Lecture de ce brief : atterrissage SaaS B2B pour acheteurs techniques, avec un langage minimaliste façon Linear, penchant vers les utilitaires Tailwind + Geist + une animation discrète. »*
- *« Lecture de ce brief : portfolio d'un designer indépendant pour des responsables de recrutement, avec un langage éditorial / typographie cinétique, penchant vers le CSS natif + l'animation pilotée par le défilement + une typographie sur mesure. »*
- *« Lecture de ce brief : refonte d'un site de service public, avec un langage axé sur la confiance, penchant vers GOV.UK Frontend ou USWDS. »*

### 0.C Si le brief est ambigu, posez une question, ne devinez pas
Posez **une seule** question de clarification - jamais une salve de questions - et seulement lorsque la lecture de design diverge réellement. Exemple : *« Ce projet doit-il ressembler davantage à du Linear épuré ou à de l'expérimental façon Awwwards ? »*

Si vous pouvez déduire la réponse avec confiance à partir du contexte, **ne posez pas la question**. Énoncez simplement la lecture de design et poursuivez.

### 0.D Discipline anti-défaut
Ne retombez pas sur : dégradés violets typiques de l'IA, héros centré sur un maillage sombre, trois cartes de fonctionnalités égales, effet verre générique appliqué partout, micro-animations en boucle infinie partout, Inter + slate-900. Ce sont les valeurs par défaut des LLM. Écartez-vous-en délibérément selon la lecture de design.

---

## 1. LES TROIS CADRANS (Configuration de base)

Après la lecture de design, réglez trois cadrans. Chaque décision de mise en page, de mouvement et de densité ci-dessous en dépend.

* **`DESIGN_VARIANCE: 8`** - 1 = Symétrie parfaite, 10 = Chaos artistique
* **`MOTION_INTENSITY: 6`** - 1 = Statique, 10 = Cinématique / Physique
* **`VISUAL_DENSITY: 4`** - 1 = Galerie d'art / Aéré, 10 = Cockpit / Données denses

**Valeurs de référence :** `8 / 6 / 4`. Utilisez ces valeurs, sauf si la lecture de design les modifie. Ne demandez pas à l'utilisateur de modifier ce fichier : les ajustements se font par la conversation.

### 1.A Déduction des cadrans (lecture de design → valeurs)
| Signal | VARIANCE | MOUVEMENT | DENSITÉ |
|---|---|---|---|
| « minimaliste / épuré / calme / éditorial / style Linear » | 5-6 | 3-4 | 2-3 |
| « grand public premium / façon Apple / luxe / marque » | 7-8 | 5-7 | 3-4 |
| « ludique / sauvage / Dribbble / Awwwards / expérimental / agence » | 9-10 | 8-10 | 3-4 |
| « page d'atterrissage / portfolio / site marketing (par défaut) » | 7-9 | 6-8 | 3-5 |
| « axé sur la confiance / secteur public / réglementé / accessibilité critique » | 3-4 | 2-3 | 4-5 |
| « refonte - préserver » | identique à l'existant | +1 | identique à l'existant |
| « refonte - refonte complète » | +2 | +2 | identique à l'existant |

### 1.B Préréglages par cas d'usage
| Cas d'usage | VARIANCE | MOUVEMENT | DENSITÉ |
|---|---|---|---|
| Atterrissage (SaaS, grand public) | 7 | 6 | 4 |
| Atterrissage (agence / créatif) | 9 | 8 | 3 |
| Atterrissage (grand public premium) | 7 | 6 | 3 |
| Portfolio (designer / studio) | 8 | 7 | 3 |
| Portfolio (développeur) | 6 | 5 | 4 |
| Éditorial / Blog | 6 | 4 | 3 |
| Service public | 3 | 2 | 5 |
| Refonte - préserver | identique | identique+1 | identique |
| Refonte - refonte complète | +2 | +2 | identique |

### 1.C Comment les cadrans pilotent le résultat
Utilisez ces valeurs (ou celles fournies par l'utilisateur) comme variables globales. Les renvois dans ce document désignent ces noms exacts de variables : n'inventez jamais d'alias comme `LAYOUT_VARIANCE` ou `ANIM_LEVEL`.

---

## 2. CARTE BRIEF → SYSTÈME DE DESIGN

Une fois la lecture de design (section 0) et les cadrans (section 1) établis, choisissez la bonne base. N'inventez pas de CSS pour ce qui dispose d'un paquet officiel. Ne faites pas passer une tendance esthétique pour un système officiel.

### 2.A Quand utiliser un véritable système de design (utiliser les packages officiels)

| Le brief évoque… | Utiliser | Pourquoi |
|---|---|---|
| Microsoft / SaaS d'entreprise / tableaux de bord | `@fluentui/react-components` ou `@fluentui/web-components` | Fluent UI officiel, jetons Microsoft, accessibilité déjà traitée |
| Interface « à la Google », produit d'inspiration Material | `@material/web` + jetons Material 3 | Officiel, personnalisable via Material Theming |
| B2B de type IBM / analytique d'entreprise | `@carbon/react` + `@carbon/styles` | Carbon officiel, modèles de densité de données éprouvés |
| Surfaces d'applications Shopify | Composants web `polaris.js` / Polaris React | Requis pour l'interface d'administration Shopify |
| Produit de type Atlassian / Jira | `@atlaskit/*` + `@atlaskit/tokens` | Système de design Atlassian officiel |
| Outil pour développeurs de type GitHub / page communautaire | `@primer/css` ou `@primer/react-brand` | Primer officiel ; variante Brand pour le marketing |
| Service public britannique | `govuk-frontend` | Attendu légalement et réglementairement |
| Service public américain / orienté confiance | `uswds` | Idem |
| MVP rapide pour commerce local / agence | Bootstrap 5.3 | Simple, rapide, fonctionnel |
| Socle React moderne et accessible | `@radix-ui/themes` | Primitives + thème soigné |
| SaaS moderne où l'on possède les composants | shadcn/ui (`npx shadcn@latest add ...`) | Vous possédez le code, facile à personnaliser ; ne jamais livrer l'état par défaut |
| SaaS moderne basé sur Tailwind / marketing IA | Utilitaires Tailwind v4 + variante `dark:` | Par défaut pour les projets indépendants et les petites équipes |

**Règle d'honnêteté :** si le brief correspond à l'un des systèmes ci-dessus, installez et utilisez le package **officiel**. Ne recréez pas son CSS à la main. N'importez pas les jetons d'un système pour ensuite en remplacer 90 %.

**Un système par projet.** N'associez pas Fluent React et Carbon dans le même arbre. N'importez pas de composants shadcn/ui dans une application Material 3.

### 2.B Quand le brief est une esthétique et non un système

Pour ces directions, il n'existe **aucun package officiel unique**. Construisez avec du CSS natif + Tailwind + une bibliothèque de composants maintenue. Soyez honnête dans les commentaires de code sur ce qui relève d'une inspiration empruntée et ce qui relève de matériel officiel.

| Esthétique | Implémentation honnête |
|---|---|
| Glassmorphisme / « verre dépoli » | `backdrop-filter`, bordures superposées, superpositions de surbrillance. Fournir un repli à remplissage plein pour `prefers-reduced-transparency`. |
| Bento (grilles de tuiles façon Apple) | CSS Grid avec des cellules de tailles mixtes. Aucune bibliothèque unique ne possède ce motif. |
| Brutalisme | CSS natif, police à chasse fixe, bordures brutes. Aucune bibliothèque. |
| Éditorial / magazine | Typographie empattée, grille asymétrique, espaces blancs généreux. Aucune bibliothèque. |
| Tech sombre / hacker | Police monospace + néon d'accent, motifs de terminal. Aucune bibliothèque. |
| Aurora / dégradés en maillage | SVG ou dégradés radiaux superposés. Aucune bibliothèque. |
| Typographie cinétique | Animations CSS natives, animations pilotées par le défilement, GSAP pour les détournements. Aucune bibliothèque. |
| **Apple Liquid Glass** | Apple documente ce style uniquement pour les plateformes Apple. **Il n'existe aucun `liquid-glass.css` officiel.** Les implémentations web sont des approximations utilisant `backdrop-filter` + bordures superposées + surbrillances. Indiquer clairement qu'il s'agit d'une approximation. |

---

## 3. ARCHITECTURE PAR DÉFAUT ET CONVENTIONS

Sauf si la lecture du design retient un véritable système de design (Section 2.A), voici les valeurs par défaut :

### 3.A Pile technique
* **Framework :** React ou Next.js. Utiliser par défaut les Server Components (RSC).
  * **SÉCURITÉ RSC :** L'état global ne fonctionne QUE dans les Client Components. Dans Next.js, englober les fournisseurs dans un composant `"use client"`.
  * **ISOLATION DE L'INTERACTIVITÉ :** Tout composant utilisant Motion, des écouteurs de défilement ou une physique du pointeur DOIT être une feuille isolée avec `'use client'` en haut. Les Server Components ne rendent que des mises en page statiques.
* **Styles :** **Tailwind v4** (par défaut). Tailwind v3 uniquement si le projet existant l'exige.
  * Pour la v4 : ne PAS utiliser le plugin `tailwindcss` dans `postcss.config.js`. Utiliser `@tailwindcss/postcss` ou le plugin Vite.
* **Animation :** **Motion** (anciennement connu sous le nom de Framer Motion). Importer depuis `motion/react` (`import { motion } from "motion/react"`). Le package `framer-motion` fonctionne toujours comme alias hérité - préférer `motion/react` dans le nouveau code.
* **Polices :** Toujours utiliser `next/font` (Next.js) ou auto-héberger avec `@font-face` + `font-display: swap`. Ne jamais lier Google Fonts via `<link>` en production.

### 3.B État
* `useState` / `useReducer` locaux pour l'interface isolée.
* État global UNIQUEMENT pour éviter le passage de props en profondeur - Zustand, Jotai ou contexte React.
* **JAMAIS** utiliser `useState` pour suivre des valeurs continues pilotées par l'utilisateur (position de la souris, progression du défilement, physique du pointeur, survol magnétique). Utiliser `useMotionValue` / `useTransform` / `useScroll` de Motion. `useState` provoque un nouveau rendu de l'arbre React à chaque changement et s'effondre sur mobile.

### 3.C Icônes
* **Bibliothèques autorisées (par ordre de priorité) :** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Déconseillée :** `lucide-react`. Acceptable uniquement lorsque l'utilisateur le demande explicitement ou lorsque le projet en dépend déjà.
* **NE JAMAIS créer à la main des icônes SVG.** Si un glyphe manque, installer une seconde bibliothèque ou le composer à partir de primitives - ne pas dessiner de tracés d'icônes à partir de zéro.
* **Une seule famille par projet.** Ne pas mélanger Phosphor et Lucide dans le même arbre de composants.
* **Standardiser `strokeWidth` globalement** (par exemple `1.5` ou `2.0`).

### 3.D Politique concernant les emojis
Déconseillés par défaut dans le code, le balisage et le texte visible. Remplacer les symboles par des glyphes de la bibliothèque d'icônes. **Exception :** n'autoriser les emojis que lorsque l'utilisateur demande explicitement une ambiance ludique, de type chat ou native des réseaux sociaux - et même dans ce cas, les utiliser avec parcimonie et à dessein.

### 3.E Mécanique de réactivité et de mise en page

* Standardiser les points de rupture (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Contenir les mises en page des pages à l'aide de `max-w-[1400px] mx-auto` ou `max-w-7xl`.
* **Stabilité de la fenêtre d'affichage :** N'utilisez JAMAIS `h-screen` pour les sections Hero de pleine hauteur. Utilisez TOUJOURS `min-h-[100dvh]` pour éviter les décalages de mise en page sur mobile (barre d'adresse d'iOS Safari).
* **Grille plutôt que calcul flex :** N'utilisez JAMAIS de calculs complexes en pourcentages avec flexbox (`w-[calc(33%-1rem)]`). Utilisez TOUJOURS CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).

### 3.F Vérification des dépendances (obligatoire)

Avant d'importer UNE bibliothèque tierce, vérifiez `package.json`. Si le paquet est absent, affichez d'abord la commande d'installation. **Ne supposez jamais** qu'une bibliothèque existe.

---

## 4. DIRECTIVES D'INGÉNIERIE DU DESIGN (correction de biais)

Les LLM tendent par défaut vers les clichés. Corrigez proactivement ces valeurs par défaut. Chaque règle comporte une voie de dérogation tenant compte du contexte.

### 4.1 Typographie

* **Affichage / Titres :** Par défaut `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Corps / Paragraphes :** Par défaut `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Choix de police sans empattement :**
  * **Déconseillée par défaut :** `Inter`. Choisissez d'abord `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, ou une police avec empattement adaptée à la marque.
  * **Dérogation :** Inter est acceptable lorsque l'utilisateur demande explicitement un rendu neutre / standard / de type Linear, ou lorsque le brief concerne un site du secteur public ou axé sur l'accessibilité.
* **Associations à connaître :** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.

* **DISCIPLINE DES EMPATTEMENTS (TRÈS DÉCONSEILLÉE PAR DÉFAUT) :**
  * Les polices avec empattement sont **très déconseillées par défaut pour tout projet.** « Cela semble créatif / premium / éditorial » n'est PAS une raison de recourir à un empattement. Le modèle mental par défaut de l'agent selon lequel « brief créatif = empattement » est le signe révélateur d'IA le plus souvent constaté lors des cycles de production.
  * **Un empattement n'est acceptable que lorsqu'UNE de ces conditions est explicitement vraie :**
    - Le brief de marque nomme littéralement une police avec empattement, OU
    - La famille esthétique relève réellement de l'éditorial / du luxe / de la publication / du manuscrit / du patrimoine / du vintage ET vous pouvez expliquer pourquoi cet empattement précis convient à cette marque précise
  * Pour tout le reste (agence créative, studio de design, marque moderne, consommation premium, portfolio, style de vie), **utilisez par défaut une police d'affichage sans empattement** (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). Les polices d'affichage sans empattement ne sont pas « ennuyeuses » : elles sont le choix par défaut pour la même raison que le noir est la couleur par défaut dans la mode.
  * **RÈGLE D'EMPHASE (liée) :** Lorsque vous souhaitez mettre en valeur un mot dans un titre (le geste cinétique du type « et `spatial` design »), utilisez l'**italique ou le gras de LA MÊME police**. N'injectez PAS un mot en empattement aléatoire dans un titre sans empattement (ou l'inverse) juste pour ajouter de l'intérêt visuel. L'emphase mêlant deux familles est amateur. L'emphase par italique ou gras dans la même famille est le bon choix.
  * **Spécifiquement INTERDITES par défaut :** `Fraunces` et `Instrument_Serif` (les deux polices d'affichage à empattement préférées des LLM).
  * **Si un empattement est justifié** (rare, selon ce qui précède), alternez dans cette liste et NE réutilisez PAS le même empattement sur des projets consécutifs : PP Editorial New, GT Sectra Display, Cardinal Grotesque, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.

* **DÉGAGEMENT DES JAMBAGES DE L'ITALIQUE (obligatoire) :** Lorsque l'italique est utilisé en typographie d'affichage et que le mot contient une lettre à jambage descendant (`y g j p q`), `leading-[1]` ou `leading-none` rognera le jambage. Utilisez `leading-[1.1]` au minimum et ajoutez une réserve de `pb-1` ou `mb-1` sur l'élément englobant. Auditez chaque mot en italique des titres d'affichage avant livraison.

### 4.2 Calibrage des couleurs
* Maximum 1 couleur d'accent. Saturation < 80 % par défaut.
* **LA RÈGLE LILA :** L'esthétique « lueur violette / bleue IA » est déconseillée par défaut. Pas de lueurs automatiques de boutons violets, pas de dégradés néon aléatoires. Utiliser des bases neutres (Zinc / Slate / Stone) avec des accents singuliers à fort contraste (Émeraude, Bleu électrique, Rose profond, Orange brûlé, etc.).
* **Dérogation :** si la marque ou le brief demande explicitement du violet / de la violette / du lila, l'adopter. Mais l'exécuter avec intention : palette cohérente, neutres harmonisés, dégradés sobres. Pas de bouillie de dégradés IA générique.
* **Une seule palette par projet.** Ne pas alterner entre gris chauds et gris froids au sein d'un même projet.
* **VERROUILLAGE DE COHÉRENCE DES COULEURS (obligatoire) :** Une fois une couleur d'accent choisie pour une page, elle est utilisée sur TOUTE la page. Un site aux gris chauds ne reçoit pas soudainement un bouton d'appel à l'action bleu dans la section 7. Un site à accent rose ne reçoit pas un badge de statut sarcelle dans le pied de page. Choisir un accent, le verrouiller, auditer chaque composant avant livraison.

* **INTERDICTION DE LA PALETTE GRAND PUBLIC PREMIUM (obligatoire, second signe d'IA le plus récurrent) :**
  * Pour les briefs grand public premium (batterie de cuisine, bien-être, artisanat, luxe, artisanat patrimonial, articles pour la maison en vente directe, etc.), le choix par défaut du LLM est **beige/crème chaud + laiton/argile/bordeaux/ocre + texte sombre espresso/encre**. Concrètement, les familles hexadécimales interdites comme arrière-plans et accents par défaut :
    - Arrière-plans : `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb` (tous « papier chaud / crème / craie / os »)
    - Accents : `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621` (tous « laiton / argile / bordeaux / ocre »)
    - Texte : `#1a1714`, `#1a1814`, `#1b1814` (tous « espresso / quasi-noir chaud »)
  * Cette palette est INTERDITE comme choix par défaut pour les briefs grand public premium. Chaque site grand public premium que vous avez déjà livré utilise exactement cette palette. La marque devient invisible.
  * **Alternatives par défaut (alterner, ne pas réutiliser) :**
    - **Luxe froid :** gris argenté + chrome + fumée (pensez Tesla, Apple Watch, Hermès sans le cuir)
    - **Forêt :** vert profond + os + accent ambre (pensez Filson, Patagonia premium)
    - **Noir et fauve :** noir véritable + fauve chaud, contraste net, aucun beige
    - **Cobalt + crème :** bleu saturé sur un seul neutre, sans laiton
    - **Terre cuite + ardoise :** rouille chaude sur gris froid, sans laiton
    - **Olive + brique + papier :** olive atténué avec accent brique rouge
    - **Monochrome pur + une seule touche saturée :** blanc cassé + noir cassé + un accent vif (bleu électrique, émeraude, rose vif, etc.)
  * **Règle de rotation des palettes :** si le précédent projet grand public premium que vous avez généré utilisait la famille beige+laiton, celui-ci DOIT utiliser une famille différente. Ne pas livrer deux fois de suite la même palette artisanale chaude.
  * **Dérogation :** la palette beige+laiton+espresso n'est acceptable QUE lorsque le brief de marque nomme explicitement ces couleurs, ou lorsque l'identité de marque est véritablement vintage / artisanale / artisanat chaud ET que vous pouvez expliquer pourquoi cette palette précise convient à cette marque précise. Y recourir par défaut parce que « c'est un brief de batterie de cuisine » est interdit.

### 4.3 Diversification de la mise en page
* **ANTI-BIAIS CENTRÉ :** Les sections Hero / H1 centrées sont évitées lorsque `DESIGN_VARIANCE > 4`. Imposer « écran partagé » (50/50), « contenu aligné à gauche / ressource alignée à droite », « espace blanc asymétrique », ou des structures à défilement épinglé.
* **Dérogation :** un hero centré est acceptable pour les briefs éditoriaux / manifestes / annonces de lancement où le message lui-même constitue le design.

### 4.4 Matérialité, ombres, cartes
* Utiliser des cartes UNIQUEMENT lorsque l'élévation communique une hiérarchie réelle. Sinon, regrouper avec `border-t`, `divide-y`, ou des espaces négatifs.
* Lorsqu'une ombre est utilisée, la teinter à la teinte de l'arrière-plan. Pas d'ombres portées noir pur sur les arrière-plans clairs.
* Pour `VISUAL_DENSITY > 7` : les conteneurs de cartes génériques sont interdits. Les indicateurs de données respirent dans une mise en page simple.
* **VERROUILLAGE DE COHÉRENCE DES FORMES (obligatoire) :** Choisir UNE échelle de rayon de coin pour la page et s'y tenir. Options : tout anguleux (rayon 0), tout arrondi (rayon 12-16 px), tout en pilule (rayon complet pour l'interactif). Les systèmes mixtes ne sont autorisés que s'il existe une règle documentée (p. ex. « les boutons sont en pilule complète, les cartes ont 16 px, les champs 8 px ») et que cette règle est appliquée partout. Des boutons ronds dans une mise en page carrée, ou des cartes carrées sur une page à boutons en pilule, constituent une conception défaillante.

### 4.5 États d'interface interactifs

Les LLM ont tendance à ne produire que « l'état statique de réussite ». Implémentez toujours les cycles complets :

* **Chargement :** Des loaders squelettes qui reproduisent la forme de la mise en page finale. Évitez les spinners circulaires génériques.
* **États vides :** Soigneusement composés ; indiquez comment les remplir.
* **États d'erreur :** Clairs, en ligne (formulaires), ou contextuels (toasts uniquement pour les messages transitoires).
* **Retour tactile :** Sur `:active`, utilisez `-translate-y-[1px]` ou `scale-[0.98]` pour simuler un appui physique.
* **VÉRIFICATION DU CONTRASTE DES BOUTONS (obligatoire, a11y) :** Avant de livrer tout bouton, vérifiez que le texte du bouton est lisible sur le fond du bouton. Un bouton blanc avec un texte blanc, un `bg-white` CTA avec un libellé `text-white`, un bouton transparent sur le fond de la page sans bordure → tous interdits. Auditez chaque CTA : rapport de contraste WCAG AA minimum (4,5:1 pour le texte courant, 3:1 pour les grands textes à partir de 18px). La même règle s'applique aux boutons fantômes sur des arrière-plans photographiques (utilisez un fond, un voile ou un contour).
* **INTERDICTION DU RETOUR À LA LIGNE DES CTA (obligatoire) :** Le texte d'un bouton DOIT tenir sur une seule ligne sur ordinateur. Si un libellé comme « VIEW SELECTED WORK » passe sur 2 ou 3 lignes, le bouton est cassé. Corrigez en raccourcissant le libellé (3 mots maximum pour les CTA principaux, idéalement 1 à 2) OU en élargissant le bouton (ne contraignez pas artificiellement `max-width` sur les CTA). Des CTA qui reviennent à la ligne sur ordinateur constituent un échec de pré-vérification.
* **PAS D'INTENTION DE CTA EN DOUBLE (obligatoire) :** Deux CTA ayant la même intention sur une même page constituent un échec de pré-vérification. Exemples de même intention : « Get in touch » + « Contact us » + « Let's talk » + « Start a project » + « Start something » + « Reach out » = toutes d'intention « contact » → choisissez UN seul libellé et utilisez-le partout sur la page (navigation, section d'accueil, pied de page). Idem pour « Try free » + « Get started » + « Sign up free » (toutes d'intention « inscription ») et « View work » + « See selected work » + « Browse projects » (toutes d'intention « portfolio »). Un libellé par intention.
* **VÉRIFICATION DU CONTRASTE DES FORMULAIRES (obligatoire, a11y) :** Les champs de saisie, le texte d'espace réservé, les anneaux de focus, le texte d'aide et le texte d'erreur doivent tous respecter le contraste WCAG AA par rapport au fond de la section. Des placeholders clairs sur un formulaire presque blanc, un formulaire blanc sur une section de page blanche, des libellés de formulaire dont le contraste est inférieur à 4,5:1 → tous interdits. Auditez chaque formulaire avant livraison.

### 4.6 Modèles de données et de formulaires

* Libellé AU-DESSUS du champ. Texte d'aide facultatif mais présent dans le balisage. Texte d'erreur SOUS le champ. `gap-2` standard pour les blocs de saisie.
* Pas de placeholder utilisé comme libellé. Jamais.

### 4.7 Discipline de mise en page (règles strictes. Ne pas en respecter une seule revient à livrer un travail défectueux)

* **Le héros DOIT tenir dans la fenêtre d'affichage initiale.** Titre de 2 lignes maximum sur ordinateur, texte de présentation de **20 mots maximum** ET 3 à 4 lignes maximum, boutons d'action visibles sans défilement. Si le texte est trop long : réduire l'échelle de police OU raccourcir le texte. Si vous ne pouvez pas décrire la proposition de valeur en 20 mots de texte de présentation, c'est la proposition de valeur qui est floue, et non la règle trop stricte. Ne laissez jamais le héros déborder et forcer un défilement pour trouver le bouton d'action.
* **Discipline de l'échelle typographique du héros.** Planifiez la taille de police et la taille de l'image *ensemble*. Si le visuel du héros est grand et que le titre comporte plus de 6 mots, ne commencez pas à `text-7xl/text-8xl`. Plage par défaut raisonnable : `text-4xl md:text-5xl lg:text-6xl` pour la plupart des héros ; `text-6xl md:text-7xl` uniquement lorsque le titre comporte 3 à 5 mots. Un titre de héros sur 4 lignes est toujours une erreur de taille de police, jamais une erreur de longueur de texte.
* **PLAFOND OBLIGATOIRE DU REMBOURRAGE SUPÉRIEUR DU HÉROS :** rembourrage supérieur du héros de `pt-24` (≈6rem) maximum sur ordinateur. Au-delà, le contenu du héros flotte à mi-hauteur de la fenêtre et donne l'impression d'un bogue de mise en page plutôt qu'un espace intentionnel. Si votre héros a besoin de plus d'air, augmentez l'échelle de police ou la taille du visuel, et non le rembourrage supérieur.
* **DISCIPLINE DE PILE DU HÉROS (4 éléments de texte maximum).** Le héros est un moment unique, et non une liste de fonctionnalités. Éléments de texte autorisés, 4 au total :
  1. Surtitre (petite étiquette en majuscules) OU bandeau de marque OU aucun des deux - choisissez zéro ou un
  2. Titre (2 lignes maximum, voir ci-dessus)
  3. Texte de présentation (20 mots maximum, 4 lignes maximum)
  4. Boutons d'action (1 principal + 1 secondaire maximum)
  - **INTERDIT dans le héros :** petite accroche sous les boutons (« Fonctionne avec GitHub, GitLab et Git auto-hébergé »), bandeau de confiance (« Utilisé par des équipes d'ingénierie chez... »), aperçu tarifaire (« Gratuit pour un utilisateur seul, 10 $/utilisateur pour les équipes »), liste de puces de fonctionnalités, rangée d'avatars de preuve sociale. Tous ces éléments passent dans des sections dédiées directement sous le héros.
  - Si vous avez un surtitre ET une accroche sous les boutons dans le même héros, supprimez l'accroche. Si vous avez un bandeau de marque ET une accroche, supprimez l'accroche. Un seul petit élément de texte par héros, au maximum.
* **Le mur de logos « Utilisé par » / « Approuvé par » se place SOUS le héros, jamais à l'intérieur.** Le héros est réservé à la proposition de valeur et au bouton d'action principal. Le mur de logos est une section distincte juste en dessous. N'entassez pas les logos de confiance dans la même rangée flexible que le texte du héros.
* **La navigation DOIT tenir sur une seule ligne sur ordinateur.** Si les éléments ne tiennent pas à 1024px (`lg`), condensez les libellés, retirez les éléments secondaires ou passez à un menu hamburger. Une navigation sur deux lignes sur ordinateur est une conception défectueuse.
* **Hauteur de navigation plafonnée à 80px maximum sur ordinateur, 64-72px par défaut.** Pas de grandes barres de navigation « agence » qui mangent 15 % de la fenêtre d'affichage.
* **Les grilles bento doivent avoir un rythme, et non une répétition unilatérale.** N'empilez pas 6 rangées image à gauche / texte à droite. Variez la composition : alternez des rangées de fonctionnalités pleine largeur, des tuiles de tailles asymétriques, des ruptures verticales.
* **RÈGLE DU NOMBRE DE CELLULES BENTO (obligatoire) :** une grille bento compte EXACTEMENT autant de cellules que de contenus disponibles. 3 éléments → 3 cellules (découpage 1+2, 2+1, ou trio asymétrique). 5 éléments → 5 cellules (2+3, 3+2, héros+4, etc.). Si votre grille contient une cellule vide au milieu ou à la fin, votre planification était erronée. Redessinez la grille ; ne collez pas une tuile vide.
* **Interdiction de répétition de famille de mise en page par section.** Une fois qu'une famille de mise en page est utilisée pour une section (par ex. cartes-images en 3 colonnes, citation pleine largeur, texte-image divisé), cette famille ne peut apparaître qu'UNE SEULE FOIS sur la page. « Commandes sélectionnées » ne doit pas ressembler à « Ce que nous faisons ». Une page d'accueil de 8 sections doit utiliser au moins 4 familles de mise en page différentes.
* **PLAFOND D'ALTERNANCE EN ZIGZAG (obligatoire).** L'alternance « image à gauche + texte à droite », puis « texte à gauche + image à droite », est une mise en page banale. Maximum 2 sections consécutives avec ce motif de division image+texte. La 3e division image+texte consécutive constitue un échec de la vérification préalable. Rompez le motif avec une section pleine largeur, une section en pile verticale, une grille bento, un défilement de type marquee, ou une autre famille de mise en page.
* **RETENUE DANS L'UTILISATION DES SURTITRES (obligatoire, la règle la plus souvent enfreinte en production).** Un « surtitre » est la petite étiquette en majuscules à fort interlettrage placée au-dessus d'un titre de section (par ex. `FOUR COLORWAYS`, `SELECTED WORK`, `THE HARDWARE`, `Git-native task management`). Signature CSS typique : `text-[11px] uppercase tracking-[0.18em]`, `font-mono text-[10.5px] uppercase tracking-[0.22em]`. Chaque site construit par IA place un surtitre au-dessus de CHAQUE en-tête de section, produisant le même rythme de gabarit. Règle stricte :
  - **Maximum 1 surtitre pour 3 sections.** Le héros compte pour 1. Ainsi, une page de 9 sections ne peut utiliser qu'au maximum 3 surtitres au total.
  - Si la section A a un surtitre, les 2 sections suivantes ne peuvent pas en avoir.
  - **La vérification préalable est mécanique :** comptez les occurrences de `uppercase tracking` (ou d'étiquettes monospace en petites capitales similaires au-dessus des titres) dans tous les composants de section. Si le nombre est supérieur à ceil(nombreDeSections / 3), la sortie échoue.
  - **Que faire à la place d'un surtitre :** supprimez-le entièrement. Le titre seul suffit. Si vous devez catégoriser une section, son emplacement sur la page la catégorise déjà ; aucune étiquette n'est nécessaire.
* **INTERDICTION DE L'EN-TÊTE DIVISÉ (obligatoire).** Le motif « grand titre à gauche + petit paragraphe explicatif à droite » comme en-tête de section (colonne gauche col-span-7/8, colonne droite col-span-4/5 avec un petit paragraphe flottant dans la colonne de droite) est **interdit par défaut**. Les sections doivent porter UN SEUL message ciblé. Si vous avez réellement besoin à la fois d'un titre et d'un paragraphe explicatif, empilez-les verticalement (titre en haut, texte en dessous, largeur maximale 65ch). N'utilisez le motif d'en-tête divisé que lorsqu'il existe une raison de composition réelle (par ex. la colonne de droite porte un visuel ou un élément interactif, et non simplement du texte de remplissage).
* **Diversité des arrière-plans bento (obligatoire).** Les sections bento et les grilles de fonctionnalités ne peuvent pas être 6 cartes blanc sur blanc contenant du texte. Au moins 2 à 3 cellules de toute grille multi-cellules doivent présenter une réelle variation visuelle : une vraie image, un dégradé adapté à la marque (pas de violet « IA »), un motif, un arrière-plan teinté. Un bento crème sur crème ne contenant que de la typographie se lit comme un défaut générique d'IA, même lorsque le reste de la page est réussi.
* **Le repli mobile doit être explicite pour chaque section.** Pour chaque mise en page multi-colonnes, déclarez le repli `< 768px` dans le même composant. Aucune hypothèse du type « ça ira, Tailwind s'en charge ».

### 4.8 Stratégie des images et des ressources visuelles

Les pages de destination et les portfolios sont des **produits visuels**. Les pages purement textuelles avec des divs imitant des captures d'écran sont du remplissage bâclé.

**Ordre de priorité pour les ressources visuelles :**
1. **Outil de génération d'images en premier.** Si UN outil de génération d'images est disponible dans l'environnement (`generate_image`, outil d'image MCP, génération intégrée à l'IDE, outils d'image OpenAI, etc.), vous DEVEZ l'utiliser pour créer des ressources propres à chaque section : photographies de héros, photos de produits, textures d'arrière-plan, images d'ambiance. Générez au ratio d'aspect adapté à la section. Ne sautez pas cette étape parce que le CSS fait main semble plus rapide.
2. **Images web réelles en second.** Lorsqu'aucun outil de génération n'est disponible, utilisez des sources de photographies réelles. Valeurs par défaut acceptables :
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` pour les photographies de substitution (la graine doit décrire la section, par ex. `marrow-cookware-kitchen`)
   * Des URL réelles de stock ou de marque lorsque le brief les fournit
   * Des sources à licence ouverte (Unsplash via URL directe, Pexels) si explicitement autorisées
3. **Dernier recours : prévenir l'utilisateur.** Si aucune de ces options n'est possible, NE remplissez PAS la page avec des illustrations SVG faites main ni des « fausses captures d'écran » en divs. Laissez plutôt des emplacements de substitution clairement étiquetés (`<!-- TODO: hero product photo, 1600x1200 -->`) et, à la fin de la réponse, indiquez : *« Cette page a besoin d'images réelles aux emplacements suivants : \[liste des emplacements\]. Veuillez les générer ou les fournir. »*

**Même les sites minimalistes ont besoin d'images réelles.** Une page purement textuelle n'est pas du minimalisme. C'est un travail inachevé. Même un site éditorial de style Linear a besoin d'au moins 2 à 3 images réelles (héros, une photo de produit ou de mode de vie, une image d'appui). Générez des photographies minimalistes en noir et blanc si le brief est sobre ; ne sautez pas les images entièrement parce que le curseur de densité est bas.

**Logos d'entreprises réelles pour la preuve sociale.** Lorsque le brief demande un mur de logos « Ils nous font confiance / Utilisé par / Clients », N'utilisez PAS par défaut des marques typographiques en texte brut (`<span>Acme Co</span>` stylisés en ligne). Utilisez de vrais logos SVG :
* **Source : Simple Icons** (`https://cdn.simpleicons.org/{slug}/ffffff` pour toute couleur, ou le paquet npm `simple-icons`). Couvre la plupart des marques connues.
* **Alternative : devicon** pour les logos de stacks technologiques (`@svgr/cli` ou CDN).
* **Vous inventez le nom de la marque ? Inventez alors aussi une marque SVG.** Générez un monogramme simple (une lettre dans un cercle, une ligature de deux lettres, un glyphe abstrait) rendu sous forme de `<svg>` en ligne, correspondant au style de la page. Les marques textuelles en texte brut pour des noms inventés paraissent génériques.
* **Toujours** s'assurer que les logos s'affichent en mode clair et sombre (blanc sur sombre, noir sur clair, ou variable de thème monochrome).
* **Règle LOGO UNIQUEMENT (obligatoire) :** un mur de logos = des logos et rien d'autre. N'affichez PAS d'étiquettes de secteur ou de catégorie sous chaque logo (ni `Vercel` + `hosting` en dessous, ni `Stripe` + `payments`, ni `Cloudflare` + `infra`). Le logo fait office de crédibilité, l'étiquette n'apporte rien que l'utilisateur ne sache déjà. Facultatif : nom de la marque en texte alternatif pour les lecteurs d'écran, lien facultatif vers le site de la marque. C'est tout.

**Illustrations faites main :**
* Icônes SVG issues de bibliothèques : acceptable (voir Section 3.C).
* Les SVG décoratifs faits main (illustrations personnalisées, logos, marques) : **fortement déconseillés**, jamais par défaut. Acceptables uniquement lorsque :
  - Le brief le demande explicitement (« dessine-moi un logo SVG »)
  - Il s'agit d'une marque géométrique unique et simple (un carré, un cercle, un mot en typographie d'affichage)
  - Vous êtes certain de la qualité du résultat

**Les fausses captures d'écran construites avec des divs sont interdites.** Un « aperçu de produit construit à la main » rendu avec des rectangles `<div>`, de fausses listes de tâches, de faux tableaux de bord ou de fausses fenêtres de terminal est un signe révélateur. Si vous devez montrer un produit :
* Utilisez une URL de capture d'écran réelle si elle existe
* Générez-en une via un outil d'image
* Utilisez un véritable aperçu de composant (une mini-version réelle de l'interface dans la page)
* Ou renoncez à l'aperçu et utilisez une photographie éditoriale

**Le héros a besoin d'un visuel réel.** Un texte accompagné d'un dégradé flou n'est pas un héros, c'est un emplacement provisoire.

### 4.9 Densité du contenu

Les pages de destination vivent de la **première impression**, pas de la lecture complète. Coupez sans pitié.

* **Contenu par défaut par section :** titre court (≤ 8 mots) + court sous-paragraphe (≤ 25 mots) + un seul élément visuel OU un seul CTA. Tout élément supplémentaire doit être justifié par le rôle de la section.
* **Aucune section de type vidage de données.** Un tableau de 20 publications, une liste de 30 récompenses, une grande matrice tarifaire sur une page marketing = mauvaise mise en page. Utilisez plutôt :
  - Les 3 à 5 points forts + un lien « Voir la liste complète »
  - Un bandeau défilant ou un carrousel pour la largeur
  - Une page entièrement différente si les données sont le produit
* **Les longues listes nécessitent un autre composant d'interface, non une liste plus longue.** La valeur par défaut `<ul>` avec des puces / des lignes `divide-y` est le choix paresseux. Si vous avez plus de 5 éléments, utilisez plutôt l'un de ces composants :
  - Une division en deux colonnes avec des éléments regroupés
  - Une grille de cartes avec image + étiquette par élément
  - Des onglets ou un accordéon si les éléments sont catégorisables
  - Des pastilles à défilement horizontal avec accrochage (scroll-snap)
  - Un carrousel pour les listes à forte largeur (témoignages, logos, capacités)
  - Un bandeau défilant pour « beaucoup de choses qui n'ont pas besoin d'une attention individuelle »
  Une fiche technique de 10 lignes avec un filet sous chaque ligne est le PIRE choix par défaut. Regroupez les lignes en 2 à 3 blocs avec des séparateurs discrets, ou passez à une mise en page en carte par spécification.
* **Fiches techniques spécifiquement (le modèle des ustensiles Marrow).** Un long tableau de spécifications produit avec `border-b` sur chaque ligne est le choix par défaut de l'IA pour les briefs d'ustensiles de cuisine, de quincaillerie, de vêtements ou d'articles artisanaux. Interdit. Alternatives concrètes :
  - **Grille de cartes sur 2 colonnes :** chaque spécification a sa propre carte, avec le nom de la spécification, la valeur (grand chiffre d'affichage) et un corps d'une ligne « pourquoi c'est important ». Cartes disposées sur 2 colonnes sur ordinateur, 1 colonne sur mobile.
  - **Pastilles horizontales à accrochage :** chaque spécification est une pastille, l'utilisateur peut la faire défiler.
  - **Blocs regroupés :** regroupez 10 spécifications en 3 grappes logiques (par exemple « Matériaux », « Cuisson », « Garantie »), chaque grappe reçoit UN seul séparateur discret et un titre de grappe.
  - **Vedettes contre reste :** 3 à 4 spécifications phares présentées en grandes tuiles d'affichage, le reste replié sous une rubrique « Voir toutes les spécifications ».

* **AUTO-AUDIT DU TEXTE (obligatoire avant livraison) :** Avant de déclarer toute tâche terminée, relisez chaque chaîne visible de la page (titres, sous-titres, surtitres, libellés de boutons, corps de texte, légendes, texte alternatif, texte de pied de page, messages d'erreur). Signalez toute chaîne qui est :
  - **Grammaticalement incorrecte** (« gratuit sur son passé », « deux forfaits mais l'un est honnête », « mettre sur la table » hors contexte)
  - **Dont les référents sont flous** (« nous prévoyons de rester ainsi » sans contexte préalable)
  - **Qui ressemble à une hallucination d'IA** (jeux de mots mignons mais faux, métaphores forcées qui ne tiennent pas, formules « élégant rien »)
  - **Qui se lit comme un LLM tentant de paraître réfléchi** (humilité passive-agressive, étiquettes d'artisan factices, méta-poésie artificielle)
  Réécrivez chaque chaîne signalée. En cas de doute sur le sens d'une chaîne, remplacez-la par une phrase fonctionnelle et simple. Un texte mignon généré par l'IA est pire qu'un texte ennuyeux.
* **Les chiffres faussement précis sont signalés.** Les chiffres comme `92%`, `4.1×`, `48k`, `5.8 mm`, `13.4 lb` doivent soit :
  - Provenir de données réelles (brief, charte de marque, indicateurs publics) : acceptable
  - Être explicitement étiquetés comme fictifs (`<!-- mock -->`, « exemple », « données de test ») : acceptable
  - Être des esthétiques de spécification inventées par l'IA : interdit. Ne simulez pas une précision d'ingénierie que la marque ne revendique pas.
* **Un seul registre de texte par page.** Ne mélangez pas le mono technique (« 47 tâches · 0,6 changement de contexte/jour »), la prose éditoriale et l'accroche marketing dans une même composition, sauf si la voix de marque l'exige explicitement.

### 4.10 Citations et témoignages

* **3 lignes maximum** pour le corps d'une citation. Jamais 6. Si la citation originale est plus longue, coupez-la. Une citation de page d'accueil est un extrait, non l'avis complet.
* Pour de très petites tailles de police (par exemple des témoignages en pied de page), la limite de lignes peut légèrement s'étendre. Esprit : « se lit d'un coup d'œil ».
* **Aucun tiret cadratin à l'intérieur du texte de la citation** comme effet de style (longues pauses, tirets cinétiques, puces en tirets cadratins). Voir la section 9.G : le tiret cadratin est totalement interdit.
* Attribution : nom + fonction + (facultativement) entreprise. Jamais le nom seul (« - Sarah »).
* Guillemets : utilisez de vrais guillemets typographiques (« ») ou aucun. Pas de guillemets ASCII droits ( " ).

### 4.11 Verrouillage du thème de page (cohérence clair / sombre)

La page a UN seul thème. Les sections ne s'inversent pas.

* Si la page est en mode sombre, TOUTES les sections sont en mode sombre. Aucune section en mode clair type papier chaud placée entre des sections sombres (ou l'inverse). L'utilisateur ne doit pas avoir l'impression d'avoir changé de site en cours de défilement.
* Exception : si le brief demande explicitement un dispositif « Histoire en blocs de couleur » ou « Changement de thème au défilement » ET qu'il s'agit d'une composition délibérée (un seul changement complet de thème avec une transition marquée, non une alternance aléatoire), c'est autorisé une fois par page.
* Comportement par défaut : choisissez clair, sombre ou automatique (`prefers-color-scheme`) au niveau de la page et verrouillez-le. Les variations de teinte d'arrière-plan au sein de la même famille de thème sont acceptables (`bg-zinc-950` à côté de `bg-zinc-900`) ; passer à `bg-amber-50` au milieu d'une page `bg-zinc-950` est une erreur.
* Lorsque vous utilisez un système de design avec thèmes intégrés (Radix Themes, shadcn/ui avec `<Theme>`), définissez le thème UNE SEULE FOIS dans `layout.tsx` ou à la racine de la page. Ne laissez aucune section individuelle le remplacer.

---

## 5. PROACTIVITÉ CONTEXTUELLE

Ce sont des outils, non des valeurs par défaut. Utilisez-les lorsque la lecture du design l'exige. **Aucun ne se déclenche automatiquement.**

* **Liquid Glass / Glassmorphism :** Approprié pour le grand public premium, les marques de luxe ou d'inspiration Apple, ou les ambiances d'overlay médiatique. Inapproprié pour les tableaux de bord, le secteur public ou le B2B « ennuyeux ». Lorsqu'il est utilisé, allez au-delà de `backdrop-blur` : ajoutez une bordure intérieure de 1px (`border-white/10`) et une ombre intérieure subtile (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) pour une réfraction physique des bords. Fournissez un repli à remplissage plein sous `prefers-reduced-transparency`.
* **Micro-physique magnétique :** À utiliser lorsque `MOTION_INTENSITY > 5` ET que le brief évoque le premium / le ludique / l'agence. Implémentez EXCLUSIVEMENT avec `useMotionValue` / `useTransform` de Motion, en dehors du cycle de rendu React. Jamais `useState`. Voir la section 3.B.
* **Micro-interactions perpétuelles** (Pulse, Typewriter, Float, Shimmer, Carousel) : À utiliser lorsque `MOTION_INTENSITY > 5` ET que la section bénéficie activement du mouvement (indicateurs de statut, flux en direct, effet IA). **Toutes les cartes n'ont pas besoin d'une boucle infinie.** Si une section est informative, laissez-la immobile. Appliquez la physique des ressorts (`type: "spring", stiffness: 100, damping: 20`) - pas d'easing linéaire.
* **« Mouvement annoncé, mouvement montré. »** Si `MOTION_INTENSITY > 4`, la page doit réellement bouger : transitions d'entrée sur le hero, révélation au défilement sur les sections clés, physique au survol des CTA, au minimum. Une page statique qui prétend `MOTION_INTENSITY: 7` est cassée. Inversement, si vous ne pouvez pas livrer un mouvement fonctionnel dans le périmètre disponible, ramenez le curseur à 3 et livrez une page statique propre. Ne construisez jamais un mouvement à moitié fonctionnel qui casse (ScrollTriggers tronqués, entrées saccadées, nettoyages manquants).
* **LE MOUVEMENT DOIT ÊTRE MOTIVÉ (obligatoire).** Avant d'ajouter toute animation, demandez-vous : « que communique cette animation ? » Réponses valides : hiérarchie (attirer l'attention sur ce qui compte), narration (révéler un contenu en séquence conforme à un récit), retour (accuser réception d'une action de l'utilisateur), transition d'état (montrer qu'un élément a changé). Réponse invalide : « ça faisait joli ». Mettre du GSAP partout parce que GSAP est disponible relève de l'amateurisme. Chaque ScrollTrigger, chaque marquee, chaque section épinglée doit avoir une raison. Si vous ne pouvez pas formuler cette raison en une phrase, supprimez l'animation.
* **MARQUEE : MAXIMUM UN PAR PAGE (obligatoire).** Les marquees de texte défilant horizontalement (« logos défilant sans fin », « manifeste défilant latéralement », « bande de mots cinétique ») sont appropriés au plus UNE fois par page. Deux marquees ou plus sur la même page donnent une impression de remplissage paresseux. Choisissez l'unique section où le marquee sert réellement le contenu ; les autres reçoivent une mise en page différente.
* **Motif GSAP Sticky-Stack (lorsqu'un scroll-stack est utilisé).** Une « pile de cartes au défilement » doit être un VÉRITABLE sticky-stack, et non une liste de révélations séquentielles. Voir la section 5.A ci-dessous pour le squelette de code canonique. Échec courant : le déclencheur se déclenche à mi-défilement au lieu de s'épingler en haut du viewport. Correction : `start: "top top"` et non `start: "top center"` ou `"top 80%"`.
* **Motif GSAP Horizontal-Pan (lorsqu'un détournement de défilement horizontal est utilisé).** Voir la section 5.B ci-dessous pour le squelette canonique. Échec courant : l'animation démarre avant que la section ne soit épinglée, si bien que l'utilisateur voit une demi-diapositive. Même correction : `start: "top top"`, épingler l'enveloppe et faire défiler (scrub) la piste interne.

### 5.A Sticky-Stack - Squelette canonique

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

Points critiques : `start: "top top"`, `pin: true`, chaque carte sauf la dernière est épinglée, et la transformation d'échelle/opacité est pilotée par le déclencheur de défilement de la CARTE SUIVANTE (ainsi la carte précédente rétrécit lorsque la suivante arrive).

### 5.B Horizontal-Pan - Squelette canonique

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // pin starts when section top hits viewport top
          end: () => `+=${distance}`,                    // scroll distance = track width minus viewport
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

Points critiques : `start: "top top"`, `pin: true`, `end: "+=${distance}"` (la longueur de défilement = le déplacement horizontal nécessaire), `scrub: 1`. L'enveloppe est épinglée, la piste interne glisse horizontalement pendant que l'utilisateur fait défiler verticalement.

### 5.C Stagger de révélation au défilement - Squelette canonique (alternative plus légère)

Pour les « éléments qui apparaissent en entrant dans le viewport » simples (sans épinglage), préférez `whileInView` de Motion à GSAP : plus léger, sans ScrollTrigger :

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

À utiliser pour : listes de fonctionnalités, grilles de témoignages, murs de logos, tout ce qui a seulement besoin d'« apparaître au défilement ». Réservez GSAP aux véritables travaux d'épinglage et de scrub.

### 5.D Motifs d'animation interdits

* **`window.addEventListener("scroll", ...)`** est banni. Il s'exécute à chaque frame de défilement, sujet aux saccades, sans regroupement. Utilisez `useScroll()` de Motion, `ScrollTrigger` de GSAP, IntersectionObserver, ou CSS `scroll-driven animations` (`animation-timeline: view()`).
* **Calculs personnalisés de progression de défilement utilisant `window.scrollY`** dans l'état React. Même raison. Re-rendus à chaque frame.
* **Boucles `requestAnimationFrame` qui touchent à l'état React.** Utilisez plutôt les valeurs de mouvement (`useMotionValue` + `useTransform`).
* **Transitions de mise en page :** Utilisez les props `layout` et `layoutId` de Motion pour les changements d'état visibles (réordonnancement de listes, expansion de modales, éléments partagés entre routes). N'enveloppez pas un contenu statique dans des props `layout` « par sécurité » : cela coûte du travail de mesure.
* **Orchestration échelonnée :** Utilisez `staggerChildren` (Motion) ou la cascade CSS (`animation-delay: calc(var(--index) * 100ms)`) pour les moments de révélation où la séquence compte. Pour `staggerChildren`, le parent (`variants`) et les enfants DOIVENT partager le même arbre de Client Components.

---

## 6. GARDE-FOUS DE PERFORMANCE ET D'ACCESSIBILITÉ

### 6.A Accélération matérielle
* Animez UNIQUEMENT `transform` et `opacity`. N'animez jamais `top`, `left`, `width`, `height`.
* Utilisez `will-change: transform` avec parcimonie, uniquement sur les éléments qui vont réellement s'animer.

### 6.B Mouvement réduit (obligatoire)
* **Tout mouvement au-delà de `MOTION_INTENSITY > 3` DOIT respecter `prefers-reduced-motion`.** Ce point n'est pas négociable.
* Dans Motion : enveloppez avec `useReducedMotion()` et dégradez vers le statique.
* En CSS : conditionnez les animations derrière `@media (prefers-reduced-motion: no-preference)` ou fournissez un bloc de remplacement sous `@media (prefers-reduced-motion: reduce)` qui les désactive.
* Les boucles infinies, le parallaxe, le détournement de défilement et la physique magnétique DOIVENT se réduire à un état statique / instantané lorsque le mouvement réduit est activé.

### 6.C Mode sombre (obligatoire pour toute page destinée aux consommateurs)
* Concevoir pour **les deux modes dès le départ**. Ne jamais livrer uniquement en mode clair ou uniquement en mode sombre sans instruction explicite de l'utilisateur.
* Utiliser la variante Tailwind `dark:` OU des variables CSS pour les tokens. Choisir une seule stratégie par projet.
* **Ne pas prescrire ici de couleurs spécifiques pour le mode sombre.** Le cahier des charges décide. Maintenir la hiérarchie visuelle, l'identité de marque et le contraste WCAG AA (AAA pour le corps de texte) dans les deux modes.
* Respecter `prefers-color-scheme: dark`. Par défaut, suivre la préférence du système, sauf si la marque impose un mode.

### 6.D Objectifs Core Web Vitals
* **LCP** < 2,5 s. L'image héroïque doit être `next/image priority` ou préchargée.
* **INP** < 200 ms. Déporter les traitements lourds hors du thread principal.
* **CLS** < 0,1. Réserver l'espace pour les images, les polices et les intégrations.
* Exécuter Lighthouse avant de déclarer une page terminée.

### 6.E Coût du DOM
* Appliquer les filtres de grain / bruit EXCLUSIVEMENT aux pseudo-éléments fixes `pointer-events-none` (par exemple `fixed inset-0 z-[60] pointer-events-none`). NE JAMAIS les appliquer aux conteneurs défilants : les repeintes GPU continues détruisent les FPS sur mobile.
* Surveiller la taille du bundle. L'animation n'est pas légère. Three.js est volumineux. Charger en différé tout élément qui n'est pas au-dessus de la ligne de flottaison.

### 6.F Retenue en matière de z-index
NE JAMAIS multiplier les valeurs arbitraires `z-50` ou `z-10`. Utiliser z-index strictement pour les contextes de couches systémiques (barres de navigation collantes, modales, superpositions, grain). Documenter l'échelle de z-index dans un fichier de constantes du projet.

---

## 7. DÉFINITIONS DES CURSEURS (Référence technique)

### DESIGN_VARIANCE (Niveau 1-10)
* **1-3 (Prévisible) :** Grille CSS symétrique (12 colonnes, unités fr égales), marges intérieures égales, alignement centré.
* **4-7 (Décalé) :** Chevauchements `margin-top: -2rem`, ratios d'image variés (4:3 à côté de 16:9), en-têtes alignés à gauche au-dessus de données centrées.
* **8-10 (Asymétrique) :** Mises en page en maçonnerie, grille CSS avec unités fractionnaires (`grid-template-columns: 2fr 1fr 1fr`), zones vides massives (`padding-left: 20vw`).
* **SURCHARGE MOBILE :** Pour les niveaux 4-10, les mises en page asymétriques au-dessus de `md:` DOIVENT se replier en une colonne stricte (`w-full`, `px-4`, `py-8`) sur les viewports `< 768px`.

### MOTION_INTENSITY (Niveau 1-10)
* **1-3 (Statique) :** Aucune animation automatique. Uniquement les états CSS `:hover` et `:active`. `prefers-reduced-motion` est de toute façon le mode par défaut.
* **4-7 (CSS fluide) :** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. Cascades `animation-delay` pour les apparitions au chargement. Se concentrer sur `transform` et `opacity`.
* **8-10 (Chorégraphie avancée) :** Révélations complexes déclenchées au défilement, parallaxe, animation pilotée par le défilement (CSS `animation-timeline` ou GSAP ScrollTrigger). Utiliser les hooks Motion. **NE JAMAIS utiliser `window.addEventListener('scroll')`** : c'est une interdiction stricte, et non une simple préférence. Voir la section 5.D pour les alternatives autorisées.

### VISUAL_DENSITY (Niveau 1-10)
* **1-3 (Galerie d'art) :** Beaucoup d'espace blanc. Écarts de section très importants (de `py-32` à `py-48`). Coûteux, épuré.
* **4-7 (Application quotidienne) :** Espacement standard d'application web (de `py-16` à `py-24`).
* **8-10 (Cockpit) :** Marges intérieures serrées. Pas de cartes encadrées ; des lignes de 1 px séparent les données. Obligatoire : `font-mono` pour tous les nombres.

---

## 8. PROTOCOLE DU MODE SOMBRE

Double mode par défaut. Ne jamais supposer un mode clair uniquement, sauf si le cahier des charges est une édition imitant l'impression.

### 8.A Stratégie de tokens (en choisir une, et s'y tenir)
* **Variante Tailwind `dark:`** (par défaut pour les projets utility-first) : chaque utilitaire de couleur associé à sa variante sombre (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
* **Variables CSS** (pour shadcn/ui, Radix Themes ou les bibliothèques de composants avec thématisation) : définir des tokens sémantiques (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) et permuter leurs valeurs sous `[data-theme="dark"]` ou `@media (prefers-color-scheme: dark)`.

### 8.B Ne pas prescrire de couleurs spécifiques ici
Le cahier des charges et la marque décident. Ce skill impose uniquement :
* **Contraste** : minimum WCAG AA pour le texte courant, cible AAA pour le texte d'accroche.
* **Parité hiérarchique** : la hiérarchie visuelle qui fonctionne en clair doit fonctionner en sombre. Si un CTA ressort en clair, il doit ressortir en sombre.
* **Fidélité à la marque** : la couleur de marque principale reste reconnaissable. Ne pas désaturer la marque pour passer en mode sombre.
* **Ni `#000000` pur ni `#ffffff` pur** : utiliser un noir atténué (zinc-950, gris chaud presque noir) et un blanc cassé. Les valeurs pures détruisent la profondeur.

### 8.C Mode par défaut
Respecter `prefers-color-scheme`, sauf si la marque impose un mode. Ajouter un bouton de bascule manuel si l'un des modes perdrait une expression de marque essentielle.

### 8.D Tester dans les deux modes avant de finaliser
Ouvrir la page dans les deux modes pendant le développement. Ne jamais livrer une page que l'on n'a vue que dans un seul mode.

---

## 9. SIGNATURES IA (Motifs interdits)

Éviter ces signatures, sauf si le cahier des charges les demande explicitement.

### 9.A Visuel et CSS
* **AUCUN néon / halo extérieur** par défaut. Utiliser des bordures intérieures ou des ombres teintées discrètes.
* **AUCUN noir pur (`#000000`).** Noir atténué, zinc-950 ou anthracite.
* **AUCUN accent sur-saturé.** Désaturer pour se fondre dans les neutres.
* **AUCUN texte en dégradé excessif** pour les grands titres.
* **AUCUN curseur de souris personnalisé.** Obsolète, hostile à l'accessibilité, néfaste pour les performances.

### 9.B Typographie
* **ÉVITER Inter par défaut.** Voir la section 4.1. Une voie de contournement existe.
* **AUCUN H1 surdimensionné** qui crie. Contrôler la hiérarchie par le poids et la couleur, et non par une échelle brute.
* **Contraintes des empattements :** Empattements pour l'éditorial / le luxe / la publication. Pas pour les tableaux de bord.

### 9.C Mise en page et espacement
* Marges intérieures et extérieures **mathématiquement parfaites**. Aucun élément flottant avec des écarts malencontreux.
* **AUCUNE rangée de 3 cartes de fonctionnalités identiques en colonnes.** La rangée générique « trois cartes identiques à l'horizontale » est interdite. Utiliser une disposition en zigzag sur 2 colonnes, une grille asymétrique, un épinglage au défilement ou une alternative à défilement horizontal.

### 9.D Contenu et données (effet « Jane Doe »)
* **AUCUN nom générique.** « John Doe », « Sarah Chan », « Jack Su » → utilisez des noms créatifs, réalistes et adaptés à la langue et à la région.
* **AUCUN avatar générique.** Pas d'icône « œuf » SVG ni d'icône utilisateur Lucide → utilisez des espaces réservés photo crédibles ou un style spécifique.
* **AUCUN chiffre trop parfait.** Évitez `99.99%`, `50%`, `1234567`. Utilisez des données organiques et désordonnées (`47.2%`, `+1 (312) 847-1928`).
* **AUCUN nom de marque type startup.** « Acme », « Nexus », « SmartFlow », « Cloudly » → inventez des noms contextuels et haut de gamme qui sonnent réels.
* **AUCUN verbe de remplissage.** « Elevate », « Seamless », « Unleash », « Next-Gen », « Revolutionize » → verbes concrets uniquement.

### 9.E Ressources externes et composants
* **AUCUNE icône SVG faite main.** Utilisez Phosphor / HugeIcons / Radix / Tabler. Lucide uniquement sur demande explicite.
* **Les SVG décoratifs faits main sont fortement déconseillés** par défaut (voir section 4.8).
* **AUCUNE fausse capture d'écran en div.** Ne construisez jamais une fausse interface produit à partir de rectangles `<div>` pour simuler une capture d'écran. Utilisez de vraies images, des images générées, ou omettez l'aperçu.
* **AUCUN lien Unsplash cassé.** Utilisez `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`, des espaces réservés photo générés, ou de vrais éléments.
* **Personnalisation shadcn/ui :** autorisée, mais JAMAIS dans son état par défaut. Personnalisez les rayons, couleurs, ombres et typographie selon l'esthétique du projet.
* **Propreté prête pour la production :** code visuellement propre, mémorable et méticuleusement raffiné.

### 9.F Signatures de tests de production (interdites explicitement)

Ces motifs proviennent de tests réels de pages d'accueil générées par LLM. Ce sont les signatures vers lesquelles le modèle se tourne par défaut lorsqu'il tente de « paraître conçu ». Considérez-les comme des interdictions strictes, sauf si le brief exige explicitement l'un d'eux.

**Héros et haut de page**
* **AUCUNE étiquette de version dans le héros.** `V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA` - interdites comme sur-titres par défaut. Acceptables uniquement lorsque le brief porte explicitement sur un lancement ou un statut d'aperçu de produit.
* **AUCUNE sous-étiquette de type « Marque · No. 01 ».** Les lignes de micro-méta comme « Marrow · No. 01 · La cocotte 6 litres ». Supprimez-les.

**Numérotation de sections et micro-étiquettes**
* **AUCUN sur-titre à numéro de section.** `00 / INDEX`, `001 · Capabilities`, `002 · Featured commission`, `06 · how it works`, `05 · The honest table` - interdits. Les sur-titres doivent nommer le sujet en langage simple, sans énumérer.
* **AUCUNE pagination de type `01 / 4` sur les images ou tuiles bento.** Si l'utilisateur peut compter, il n'a pas besoin de l'étiquette.
* **AUCUN repère de défilement de type `Scroll · 001 Capabilities`.** Une simple flèche ou « Défiler » suffit ; aucun préfixe de numéro de section.
* **AUCUNE étiquette de plage du type « Index des travaux, 2018 - 2026 »** comme sur-titre. Dites simplement ce qu'est la section.

**Séparateurs et points**
* **Le point médian (`·`) est rationné.** Maximum 1 par ligne dans les bandeaux de métadonnées. NE l'utilisez PAS comme séparateur par défaut pour tout (« foo · bar · baz · qux · quux »). Si vous avez besoin d'une famille de séparateurs, privilégiez les retours à la ligne, les filets fins ou les colonnes.
* **AUCUN point de statut coloré décoratif sur chaque liste, navigation ou badge.** Un point coloré avant « ONE Q4 SLOT OPEN », avant chaque lien de navigation ou chaque ligne de tâche est interdit par défaut. Acceptable uniquement lorsque le point traduit un état sémantique réel (statut d'un serveur, indicateur de disponibilité) et est utilisé avec parcimonie.

**Tirets cadratins et fioritures typographiques**
* **AUCUN tiret cadratin (`—`) comme élément de design NI ailleurs.** Voir la section 9.G ci-dessous pour l'interdiction complète et non négociable. Le caractère tiret cadratin est interdit dans les titres, sur-titres, pastilles, corps de texte, citations, attributions, légendes, textes de boutons et textes alternatifs. Utilisez le trait d'union ordinaire (`-`).
* **AUCUN titre coupé et en italique** (`<br>`) comme « grand geste » de design par défaut. Les coupures du type « pendant trente\<br\>*ans.* » Les titres doivent d'abord se lire naturellement, et ne devenir ingénieux que si le brief l'exige.
* **AUCUN texte pivoté verticalement** (« INDEX DES TRAVAUX, 2018 - 2026 » pivoté de 90°). Cliché des portfolios d'agences. À utiliser uniquement lorsque le brief est explicitement agence / Awwwards / expérimental ET que cela sert une véritable composition.
* **AUCUN réticule ni filet de grille comme décoration.** Les lignes verticales et horizontales tracées uniquement pour faire paraître la page « conçue » sont interdites. Utilisez-les seulement lorsqu'elles organisent un contenu réel.

**Fausses prévisualisations de produit**
* **AUCUNE fausse interface produit en div dans le héros** (fausse liste de tâches, faux terminal, faux tableau de bord construit à partir de divs stylées). C'est le signe n°1 du design généré par LLM. Utilisez une vraie capture d'écran, une image générée, un véritable aperçu de composant, ou aucun.
* **AUCUN faux pied de page de version** (« v0.6.2-rc.1 », « dernière synchro il y a 4 s · main ») à l'intérieur de fausses captures d'écran. N'ajoute rien et trahit l'IA.

**Tics de l'argumentaire marketing**
* **AUCUN en-tête de preuve sociale « Discrètement utilisé chez » / « Discrètement approuvé par ».** Utilisez un langage naturel : « Approuvé par », « Utilisé chez », « Parmi nos clients », ou omettez le titre si les logos parlent d'eux-mêmes.
* **AUCUNE étiquette poétique du type « Depuis le terrain » / « Notes de terrain » / « Actuellement sur l'établi » / « Sur nos bureaux » / « Assiettes en vrac »** sur les sections de citations, de blog ou de barre latérale. Cela sonne comme de l'artisanat performatif. Utilisez des étiquettes fonctionnelles et simples (« Témoignages », « Derniers articles », « En cours ») ou omettez l'étiquette.
* **AUCUNE référence industrielle à l'humilité feinte** du type « Nous respectons les françaises » dans le corps du texte. Mignon et typique de l'IA.
* **AUCUNE bande météo ou de localisation** (« LIS 14:23 · 18 °C ») dans les en-têtes ou pieds de page, sauf si le brief porte explicitement sur un lieu ou sur un studio réparti entre fuseaux horaires.
* **AUCUNE micro-phrase méta sous les sur-titres.** Des phrases comme *« Chacune de ces fonctionnalités est livrée aujourd'hui, et non promise pour une feuille de route. La liste restera courte à dessein. »* placées sous un titre de section encombrent la page. Sur-titre + titre + corps suffisent.
* **AUCUNE étiquette d'étape générique.** « Étape 1 / Étape 2 / Étape 3 », « Step 1 / Step 2 / Step 3 », « Phase 01 / Phase 02 / Phase 03 », « Premier passage / Deuxième passage / Troisième passage ». Interdit. Le contenu de l'étape est l'étiquette. Si vous devez montrer une progression, utilisez directement le verbe et le nom (« Installer », « Configurer », « Livrer ») et non « Étape 1 : Installer ».

**Pastilles, étiquettes et tampons de version**
* **AUCUNE pastille/étiquette/tag superposé sur les images.** Pas de superpositions `<span>` sur les photos avec des tags comme `Brand · 02`, `PLATE · BRAND`, `Field notes - journal`. Soit on laisse l'image parler seule, soit on ajoute une légende directement sous l'image (en dehors de celle-ci).
* **AUCUNE mention de crédit photo décorative.** Les chaînes comme `Field study no. 12 · Ines Caetano`, `Plate 03 · House archive`, `Frame XII · 35mm` sous des images d'banque d'images ou picsum sont prétentieuses. Le crédit photo n'est autorisé QUE lorsqu'un vrai photographe est crédité pour une vraie photo (avec autorisation). Sinon : on omet la légende ou on utilise une légende fonctionnelle d'une ligne (« La 6-quart, en Sauge. »).
* **AUCUN pied de page de version sur les pages marketing.** Les chaînes de pied de page comme `v1.4.2`, `Build 0048`, `last sync 4s ago · main` sont des fixtures CLI / d'outils de développement, non du contenu de page de destination. Interdites sur les pages marketing, de destination ou de portfolio.
* **AUCUN compteur de stock en direct de type « Réservation 412 sur 800 »** à titre décoratif. Uniquement si le brief est explicitement une liste d'attente à tirage limité avec des données réelles.

**Bandes de texte décoratives**
* **AUCUNE bande de texte décorative en bas du hero.** Les motifs comme `BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION`, `DESIGN · BUILD · SHIP`, `ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.`, sous forme de petite bande en majuscules monospace en travers du bas du hero, sont un cliché de portfolio d'agence. Interdites par défaut. Acceptables uniquement lorsque la bande contient de vrais liens navigables (barre de navigation inférieure collante) ou de véritables informations d'état (bannière de cookies, informations de build sur un site de documentation).
* **AUCUN sous-texte flottant en haut à droite dans les titres de section.** Motif : la section possède un grand titre aligné à gauche ; dans le coin supérieur droit de ce même en-tête se trouve un petit paragraphe explicatif flottant, sans alignement clair avec quoi que ce soit d'autre. Ce flottant est le Signe révélateur. Soit on place le sous-texte directement sous le titre, soit on construit un en-tête propre sur 2 colonnes (à gauche : le titre, à droite : le corps aligné), mais pas un minuscule paragraphe dans le coin.

**Listes, séparateurs et notation**
* **AUCUN `border-t` + `border-b` sur chaque ligne d'une longue liste / d'un tableau de spécifications.** Choisir l'un des deux (bordure inférieure entre les lignes OU bordure supérieure au-dessus du groupe) et l'utiliser avec parcimonie. Un tableau de spécifications de 10 lignes avec des filets sous chaque ligne est la mise en page la plus paresseuse ; voir la section 4.9 pour d'autres composants d'interface.
* **AUCUNE barre de notation/progression avec des pistes de fond pleines** comme visuel de comparaison. Si vous devez montrer des comparaisons « X sur Y », privilégiez un nombre accompagné d'une petite icône, ou une petite barre en ligne SANS piste de fond. Les grandes pistes pleines `bg-zinc-200` avec un remplissage partiel par-dessus sont un encombrement de type tableau de bord sur une page de destination.

**Paramètres régionaux, heure et repères de défilement**
* **Les bandes de lieu / nom de ville / heure / météo sont interdites pour 99 % des briefs.** « Lisbonne, au service des fondateurs » dans le hero, « 1200-690 Lisbonne, Portugal » dans le pied de page, « Lisbonne 14:23 · 18 °C » dans la navigation. Ce sont des signes de décoration de portfolio d'agence. Autorisées UNIQUEMENT lorsque : le brief décrit explicitement un studio distribué mondialement avec un travail dépendant des fuseaux horaires, OU une marque tournée vers le voyage, OU un lieu physique réel. Une seule mention d'adresse de contact dans le pied de page est acceptable ; une bande d'ambiance de lieu ne l'est pas.
* **Les repères de défilement sont interdits.** `Scroll`, `↓ scroll`, `Scroll to explore`, `Scroll to walk through it`, icônes de molette de souris animées. Si l'utilisateur n'a pas encore défilé, il regarde le hero. Il sait ce qu'est le défilement. Le bas de la fenêtre d'affichage n'a pas besoin d'étiquette.
* **AUCUN point de statut décoratif par défaut.** Un point coloré avant les éléments de navigation, avant les lignes de liste, avant les badges, avant les étiquettes d'état est un Signe révélateur. Acceptable uniquement lorsqu'il transmet un état sémantique réel (un indicateur en direct sur un statut serveur réel, un indicateur de disponibilité en direct), et limité à un par section de page.

### 9.G INTERDICTION DU TIRET CADRATIN (le Signe révélateur le plus transgressé)

Le **tiret cadratin (`—`) est totalement interdit.** C'est la béquille stylistique caractéristique du LLM et le Signe visuel n° 1 dans les tests de production. Il n'existe aucune autorisation d'« usage limité », aucune autorisation de « fréquence du langage naturel », aucune autorisation « dans le corps du texte, c'est acceptable ». Aucune.

* **Interdit dans les titres.** Utiliser un point ou une virgule.
* **Interdit dans les surtitres / étiquettes / pastilles / textes de boutons / légendes d'images / éléments de navigation.** Remplacer par des sauts de ligne, des colonnes ou des filets.
* **Interdit dans le corps du texte.** Restructurer la phrase : deux phrases séparées par un point, OU une virgule, OU des parenthèses, OU deux-points.
* **Interdit dans l'attribution des citations.** Utiliser un trait d'union normal entouré d'espaces (` - `) ou un saut de ligne + nom en graisse plus légère.
* **Interdit également sous forme de tiret demi-cadratin (`–`) lorsqu'il sert de séparateur.** Les plages de dates (`2018-2026`) utilisent un trait d'union. Les plages de nombres (`€40-80k`) utilisent un trait d'union.

Les SEULS caractères de tiret autorisés sur la page sont :
* Le trait d'union ordinaire `-` (pour les mots composés, les plages, les séparateurs de lignes dans le balisage)
* Le signe moins en mathématiques (`-5°C`)

Si votre sortie contient un seul `—` ou `–` visible par l'utilisateur, la sortie échoue à la vérification préalable et doit être réécrite.

Cette règle est non négociable. L'agent a historiquement ignoré les limites de tirets cadratins lorsqu'elles étaient formulées en « à utiliser avec parcimonie ». La formulation ici est binaire : zéro tiret cadratin.

---

## 10. VOCABULAIRE DE RÉFÉRENCE (Noms de motifs que l'agent doit connaître)

Il s'agit d'un vocabulaire, non d'une bibliothèque. L'agent doit CONNAÎTRE ces noms de motifs pour communiquer à leur sujet, concevoir en les gardant à l'esprit, et y recourir lorsque la lecture du design l'exige. **Les implémentations et esquisses de code se trouvent dans la Bibliothèque de blocs (section 12), qui est alimentée de manière itérative.**

### Paradigmes de hero
* **Hero en découpe asymétrique** - Texte d'un côté, élément visuel de l'autre, espace blanc généreux.
* **Hero manifeste éditorial** - Typographie grande, sans élément visuel, presque une affiche.
* **Hero à masque vidéo / média** - Typographie découpée en masque sur un arrière-plan vidéo.
* **Hero à typographie cinétique** - Typographie animée comme visuel principal.
* **Hero à révélation en rideau** - Les parties du hero se dévoilent au défilement comme un rideau.
* **Hero épinglé au défilement** - Le hero reste fixé pendant que le contenu défile derrière lui.

### Navigation et menus
* **Effet de zoom du Dock macOS** - Navigation en bordure, les icônes s'agrandissent de façon fluide au survol.
* **Bouton magnétique** - Attiré vers le curseur.
* **Menu gluant** - Les sous-éléments se détachent comme un liquide visqueux.
* **Dynamic Island** - Pastille à morphing pour le statut et les alertes.
* **Menu radial contextuel** - Menu circulaire qui se déploie au point de clic.
* **Speed Dial flottant** - Bouton d'action flottant qui se déploie en actions secondaires incurvées.
* **Méga-menu en révélation** - Menu déroulant plein écran, contenu apparaissant en fondu échelonné.

### Mise en page et grilles
* **Grille Bento** - Regroupement asymétrique de tuiles (Centre de contrôle d'Apple).
* **Disposition en maçonnerie** - Grille échelonnée, sans hauteur de ligne fixe.
* **Chroma Grid** - Bordures et tuiles avec des dégradés animés subtils.
* **Défilement en écran partagé** - Deux moitiés glissant dans des directions opposées.
* **Sections en pile collante** - Sections qui se fixent et s'empilent au défilement.

### Cartes et conteneurs
* **Carte inclinable en parallaxe** - Inclinaison 3D suivant les coordonnées de la souris.
* **Carte à bordure lumineuse** - Les bordures s'illuminent sous le curseur.
* **Panneau en glassmorphism** - Verre dépoli avec réfraction interne.
* **Carte feuille holographique** - Changement de couleur irisé arc-en-ciel au survol.
* **Pile de cartes façon Tinder** - Pile de cartes physique, à balayer pour écarter.
* **Modale à morphing** - Le bouton se transforme en sa propre boîte de dialogue.

### Animations de défilement
* **Pile de cartes collante** - Les cartes se fixent et s'empilent physiquement.
* **Détournement du défilement horizontal** - Défilement vertical → déplacement horizontal.
* **Défilement locomotive / séquence** - Vidéo ou séquence 3D liée à la barre de défilement.
* **Parallaxe de zoom** - Image de fond centrale qui zoome au défilement.
* **Chemin de progression du défilement** - Ligne SVG qui se dessine au fil du défilement.
* **Transition par balayage liquide** - Transition de page comme un liquide visqueux.

### Galeries et médias
* **Galerie en dôme** - Galerie panoramique 3D.
* **Carrousel Coverflow** - Carrousel 3D aux bords inclinés.
* **Grille à faire glisser** - Toile glissable sans limites.
* **Curseur d'images en accordéon** - Fines bandes qui s'élargissent au survol.
* **Traînée d'images au survol** - Traînée d'images qui apparaissent sur le passage de la souris.
* **Effet glitch sur image** - Décalage des canaux RVB au survol.

### Typographie et texte
* **Bandeau cinétique** - Bandes de texte sans fin qui s'inversent au défilement.
* **Révélation par masque de texte** - Typographie massive servant de fenêtre transparente sur une vidéo.
* **Effet de brouillage de texte** - Décodage façon Matrix au chargement ou au survol.
* **Texte en chemin circulaire** - Texte courbé le long d'un cercle en rotation.
* **Animation de contour en dégradé** - Texte contourné avec un dégradé défilant.
* **Grille typographique cinétique** - Lettres qui fuient le curseur.

### Micro-interactions et effets
* **Bouton à explosion de particules** - L'appel à l'action se brise en particules en cas de succès.
* **Rafraîchissement par tirer liquide** - Indicateur de rechargement façon gouttelettes qui se détachent.
* **Scintillement de squelette** - Reflet lumineux qui se déplace sur les espaces réservés.
* **Bouton sensible à la direction du survol** - Le remplissage entre depuis le côté exact du curseur.
* **Effet d'ondulation au clic** - Onde émise depuis les coordonnées du clic.
* **Tracé animé de lignes SVG** - Vecteurs qui se dessinent en temps réel.
* **Arrière-plan en dégradé maillé** - Taches organiques façon lampe à lave.
* **Flou de profondeur par lentille** - Interface en arrière-plan floutée pour focaliser l'action au premier plan.

### Choix de la bibliothèque d'animation
* **Motion (`motion/react`)** - par défaut pour les animations d'interface, Bento et de changement d'état.
* **GSAP + ScrollTrigger** - pour le scrollytelling pleine page et les détournements de défilement. Isoler dans des composants feuilles dédiés avec `useEffect` nettoyage.
* **Three.js / WebGL** - pour les arrière-plans en canevas et les scènes 3D. Même règle d'isolation.
* **NE JAMAIS mélanger GSAP / Three.js avec Motion dans la même arborescence de composants.** Ils se disputent les mêmes images.

---

## 11. PROTOCOLE DE REFONTE

Cette compétence gère **les créations ex nihilo ET les refontes**. Mal classer le mode est la principale source de mauvais résultats de refonte.

### 11.A Détecter le mode (première action)
* **Création ex nihilo** - aucun site existant, ou refonte complète approuvée. Repère de base issu de la section 1.
* **Refonte - Préservation** - moderniser sans trahir la marque. Auditer d'abord, extraire les jetons de marque, faire évoluer progressivement.
* **Refonte - Remaniement complet** - nouveau langage visuel appliqué au contenu existant. Traiter comme une création ex nihilo pour le visuel ; préserver le contenu et l'architecture de l'information.

En cas d'ambiguïté, demander **une seule fois** : *« Cette refonte doit-elle préserver l'identité de marque existante, ou repartons-nous visuellement de zéro ? »*

### 11.B Auditer avant toute modification
Documenter l'état actuel avant de proposer des changements :
* **Jetons de marque** - couleurs primaire / d'accent, pile typographique, traitement du logo, rayons de bordure.
* **Architecture de l'information** - arborescence des pages, navigation principale, parcours de conversion clés.
* **Blocs de contenu** - ce qui existe, ce qui remplit une fonction, ce qui est superflu.
* **Motifs à préserver** - interactions signatures, héros reconnaissable, ton éditorial.
* **Motifs à retirer** - marques de contenu généré bâclé, mises en page cassées, liens morts, imagerie générique, pièges de performance.
* **Lecture des réglages du site existant** - déduire les `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY` actuels. C'est votre point de départ, pas la référence.
* **Référence SEO** - pages positionnées actuelles, balises titre, données structurées, cartes OG. **La migration SEO est le risque n° 1 d'une refonte.**

### 11.C Règles de préservation
* **Ne pas modifier l'architecture de l'information** sauf demande explicite. Conserver stables les slugs de pages, les identifiants d'ancres et les libellés de navigation principale, pour le SEO et les habitudes des utilisateurs.
* **Extraire les couleurs de marque avant d'appliquer la section 4.2.** Une marque déjà violette reste violette : appliquer la dérogation de la RÈGLE LILA.
* **Préserver le ton éditorial** sauf demande de réécriture. Modernisation visuelle ≠ réécriture du contenu.
* **Respecter les acquis d'accessibilité existants.** Ne pas régresser sur les états de focus, les textes alternatifs, la navigation au clavier, le contraste.
* **Respecter les événements analytiques existants.** Ne pas renommer les boutons, champs de formulaire ou identifiants de section dont dépend le suivi en aval.

### 11.D Leviers de modernisation (par ordre de priorité)

Appliquer dans l'ordre - s'arrêter dès que le brief est satisfait :
1. **Rafraîchissement typographique** - plus grand gain visuel par unité de risque.
2. **Espacement et rythme** - augmenter le padding des sections, corriger le rythme vertical.
3. **Recalibrage des couleurs** - désaturer, unifier les neutres, conserver l'accent de marque.
4. **Couche de mouvement** - ajouter des micro-interactions adaptées à `MOTION_INTENSITY` aux composants existants.
5. **Recomposition du héros et des sections clés** - restructurer le haut de l'entonnoir en utilisant le vocabulaire de la section 10.
6. **Remplacement complet de bloc** - uniquement lorsque le bloc existant est irrécupérable.

### 11.E Arbre de décision : évolution ciblée ou refonte complète

* IA, contenu et SEO sains → **évolution ciblée** (leviers 1 à 4). Environ 70 % de la valeur pour environ 40 % du risque.
* La dette visuelle est structurelle (IA défaillante, absence de système de design, mobile cassé) → **refonte complète** avec préservation stricte du contenu.
* La marque elle-même change → **projet from scratch (greenfield)**.

### 11.F Ce qui ne change jamais silencieusement

Ne jamais modifier sans approbation explicite de l'utilisateur :
* Structure des URL / slugs de routes.
* Libellés de la navigation principale.
* Noms ou ordre des champs de formulaire (casse les analytics et l'auto-remplissage).
* Logo ou marque de la marque.
* Textes juridiques / de consentement / de cookies existants.

---

## 12. LA BIBLIOTHÈQUE DE BLOCS (contrat - les implémentations arrivent itérativement)

Le vocabulaire de référence (section 10) nomme les motifs. La bibliothèque de blocs les implémente avec de vraies props, de vraies spécifications de mouvement et de véritables esquisses de code.

**Statut :** schéma défini ici. Des blocs seront ajoutés itérativement. Ne pas improviser de nouveaux blocs sans suivre ce schéma.

### 12.A Emplacement du fichier
```
skills/taste-skill/blocks/
  hero/
    asymmetric-split.md
    editorial-manifesto.md
    kinetic-type.md
    ...
  feature/
    bento-grid.md
    sticky-scroll-stack.md
    zig-zag.md
    ...
  social-proof/
  pricing/
  cta/
  footer/
  navigation/
  portfolio/
  transition/
```


### 12.B Frontmatter requis
```yaml
---
name: asymmetric-split-hero
category: hero
dial_compatibility:
  variance: [6, 10]
  motion: [3, 10]
  density: [2, 5]
when_to_use: "Landing pages with one strong asset and one strong message. Default hero for SaaS, agency, premium consumer."
not_for: "Editorial / manifesto launches where the message IS the design."
stack: ["react", "next", "tailwind", "motion"]
---
```


### 12.C Sections obligatoires du corps
1. **Esquisse visuelle** - description ou schéma ASCII court de la mise en page.
2. **API des props** - l'interface du composant.
3. **Esquisse de code** - implémentation minimale fonctionnelle (Server Component par défaut, îlot Client pour le mouvement).
4. **Repli mobile** - règles d'effondrement explicites pour `< 768px`.
5. **Variantes de mouvement** - une variante par bande `MOTION_INTENSITY` (1-3, 4-7, 8-10). Repli explicite pour la réduction de mouvement.
6. **Notes pour le mode sombre** - stratégie de tokens spécifique à ce bloc.
7. **Anti-motifs** - façons courantes dont ce bloc échoue.
8. **Références** - liens vers de vrais exemples en production.

### 12.D Discipline de la bibliothèque de blocs

* Un bloc par fichier. Pas de fichiers multi-blocs.
* Chaque bloc doit fonctionner de manière autonome (on le dépose dans une page, il s'affiche).
* Chaque bloc doit passer la vérification préalable (section 14).
* Les blocs qui dépendent d'un système de design de la section 2.A sont placés sous `blocks/<category>/<name>--<system>.md` (par ex. `feature/bento-grid--material.md`).

---

## 13. HORS PÉRIMÈTRE

Cette compétence n'est PAS destinée à :
* Tableaux de bord / interfaces produit denses / panneaux d'administration (utiliser Fluent, Carbon, Atlassian ou Polaris de la section 2.A).
* Tableaux de données (utiliser TanStack Table ou AG Grid).
* Formulaires en plusieurs étapes / assistants (utiliser des motifs spécifiques aux formulaires ; cette compétence ne les améliorera pas).
* Éditeurs de code (utiliser Monaco / CodeMirror avec leur habillage officiel).
* Mobile natif (utiliser directement Apple HIG / Material).
* Interfaces de collaboration temps réel (présence, curseurs, OT - classe de problème différente).

Si le brief relève de l'un des cas ci-dessus, **le dire explicitement**, indiquer l'outil approprié, et n'appliquer les parties page marketing / page à propos / page d'atterrissage de cette compétence qu'aux surfaces où elles s'appliquent.

---

## 14. VÉRIFICATION PRÉALABLE FINALE

Exécuter cette matrice avant de produire du code. C'est le dernier filtre.

**CE N'EST PAS FACULTATIF. Cocher chaque case. Si une case échoue, la sortie n'est pas terminée.**

- [ ] **Inférence de brief** déclarée (phrase unique de la Section 0.B) ?
- [ ] **Valeurs des cadrans** explicites et justifiées par le brief, et non reprises silencieusement de la valeur de référence ?
- [ ] **Système de design** choisi dans la Section 2 si applicable, ou esthétique étiquetée honnêtement ?
- [ ] **Mode refonte** détecté et audit réalisé (si applicable, Section 11) ?
- [ ] **ZÉRO tiret cadratin (`—`) nulle part sur la page.** Titres, surtitres, pastilles, corps de texte, citations, attributions, légendes, boutons, texte alternatif. Zéro. (Section 9.G - non négociable.)
- [ ] **Verrouillage du thème de page** : UN seul thème (clair, sombre ou auto) pour toute la page. Aucune section ne passe en mode inversé en cours de page (Section 4.11) ?
- [ ] **Verrouillage de cohérence des couleurs** : une seule couleur d'accent utilisée de manière identique dans toutes les sections (Section 4.2) ?
- [ ] **Verrouillage de cohérence des formes** : un seul système de rayons d'angle appliqué de manière cohérente (Section 4.4) ?
- [ ] **Vérification du contraste des boutons** : le texte de chaque CTA est lisible sur son fond (pas de blanc sur blanc, WCAG AA 4,5:1) ?
- [ ] **Retour à la ligne des CTA** : aucun libellé de CTA ne passe sur 2 lignes ou plus en version bureau ?
- [ ] **Vérification du contraste des formulaires** : les champs, placeholders, anneaux de focus et libellés respectent WCAG AA sur le fond de section ?
- [ ] **Discipline des empattements** : si une police avec empattements est utilisée, ce n'est PAS Fraunces ni Instrument_Serif (ou c'en est une, avec une justification de marque explicite) ? Différente de celle de votre projet précédent ?
- [ ] **Palette grand public premium** : si le brief est grand public premium (ustensiles de cuisine / bien-être / artisanat / luxe), la palette n'appartient PAS à la famille par défaut de l'IA beige + laiton + bordeaux + espresso ? Famille différente de celle de votre précédent projet grand public premium ?
- [ ] **Dégagement des descendantes en italique** : chaque mot en italique avec `y g j p q` dispose d'au moins `leading-[1.1]` et d'une réserve `pb-1` ?
- [ ] **Le héros tient dans la fenêtre d'affichage** : titre sur ≤ 2 lignes, sous-titre ≤ 20 mots ET ≤ 4 lignes, CTA visible sans défilement, échelle typographique planifiée en fonction de l'image ?
- [ ] **Marge supérieure du héros** : `pt-24` au maximum en version bureau, le contenu du héros ne flotte pas à mi-hauteur de la fenêtre ?
- [ ] **Discipline de pile du héros** : maximum 4 éléments textuels dans le héros (surtitre OU bandeau de marque, titre, sous-titre, CTA) ? Pas de petit slogan sous les CTA, pas de bandeau de confiance miniature dans le héros ?
- [ ] **NOMBRE DE SURTITRES (mécanique)** : compter les occurrences de micro-libellés `uppercase tracking` au-dessus des titres de section dans tous les composants. Le nombre ≤ ceil(nombreDeSections / 3) ? Le héros compte pour 1.
- [ ] **Interdiction de l'en-tête fendu** : aucun motif « grand titre à gauche + petit paragraphe explicatif à droite » comme en-tête de section (empilement vertical à la place) ?
- [ ] **Plafond d'alternance en zigzag** : pas 3 sections consécutives ou plus avec la même mise en page image + texte en deux colonnes ?
- [ ] **Pas d'intention de CTA en double** : deux CTA avec la même intention (« Nous contacter » + « Parlons-en » tous deux sur la page = échec) ?
- [ ] **Bandeau de logos = logos seulement** : aucun libellé de secteur ou de catégorie imprimé sous les logos ?
- [ ] **Diversité des arrière-plans en bento** : au moins 2 à 3 cellules bento présentent une variation visuelle réelle (image, dégradé, motif), et pas uniquement des cartes de texte blanc sur blanc ?
- [ ] **Bandeau « Utilisé par / Ils nous font confiance »** placé SOUS le héros, et non dedans, utilise de VRAIS logos SVG (Simple Icons / devicon) ou des marques SVG générées, PAS de simples noms de marque en texte ?
- [ ] **Autocontrôle du texte** : chaque chaîne visible a été relue, aucune formulation grammaticalement cassée ou hallucinée par l'IA (du type « libre sur son passé ») n'a été livrée ?
- [ ] **Mouvement motivé** : chaque animation peut être justifiée en une phrase (hiérarchie / récit / retour / transition d'état), pas de GSAP gratuit pour l'effet ?
- [ ] **Au plus un marquee par page** : pas deux bandeaux défilants horizontaux sur la même page ?
- [ ] **Navigation sur UNE ligne** en version bureau, hauteur ≤ 80 px ?
- [ ] **Vérification de répétition des mises en page de section** : aucune paire de sections ne partage la même famille de mise en page (au moins 4 familles différentes sur 8 sections) ?
- [ ] **Le bento a un rythme ET un nombre exact de cellules** (N éléments → N cellules, aucune cellule vide au milieu ou à la fin) ?
- [ ] **Les longues listes utilisent le bon composant d'interface** (pas le `<ul>` par défaut avec `divide-y` pour plus de 5 éléments, voir les alternatives de la Section 4.9) ?
- [ ] **Images réelles utilisées** (outil de génération d'abord, puis Picsum avec graine, puis emplacements explicites) - AUCUNE fausse capture d'écran en div, AUCUN SVG décoratif fait main, AUCUN minimalisme purement textuel ?
- [ ] **Aucune pastille ou étiquette superposée aux images** (pas de `Plate · Brand`, pas de `Field notes - journal`) ?
- [ ] **Aucune légende de crédit photo décorative** (`Field study no. 12 · Ines Caetano`) ?
- [ ] **Aucun pied de page de version** (`v1.4.2`, `Build 0048`) sur les pages marketing ?
- [ ] **Aucune micro-phrase méta** sous les surtitres (« Chacune de ces fonctionnalités est livrée aujourd'hui... ») ?
- [ ] **Aucune bande de texte décorative en bas du héros** (`BRAND. MOTION. SPATIAL.`) ?
- [ ] **Aucun sous-texte flottant en haut à droite** dans les titres de section ?
- [ ] **Aucune barre de score ou de progression avec fond plein** comme visuel de comparaison ?
- [ ] **Aucune bande de lieu / nom de ville / heure / météo** sauf si le brief est réellement mondial ou centré sur un lieu ?
- [ ] **Aucun indicateur de défilement** (`Scroll`, `↓ scroll`, `Scroll to explore`) ?
- [ ] **Aucune étiquette de version dans le héros** (V0.6, BETA, SUR INVITATION) sauf si le brief est un lancement ?
- [ ] **Aucun surtitre de numérotation de section** (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`) ?
- [ ] **Aucun point décoratif** (zéro par défaut, uniquement pour un état sémantique réel) ?
- [ ] **Pas de `border-t` + `border-b` sur chaque ligne** des longues listes / tableaux de spécifications ?
- [ ] **Densité de contenu raisonnable** : pas de tableaux de données de 20 lignes, pas de spécifications fictivement précises sans justification, sous-paragraphes ≤ 25 mots par défaut ?
- [ ] **Citations ≤ 3 lignes** de corps de texte, attribution propre (sans tiret cadratin) ?
- [ ] **Mouvement annoncé = mouvement affiché** : si `MOTION_INTENSITY > 4`, la page s'anime réellement, et pas seulement en apparence ?
- [ ] **Empilement collant GSAP / défilement horizontal** implémenté selon le squelette canonique des Sections 5.A / 5.B (`start: "top top"`, `pin: true`, scrub correct) ?
- [ ] **Aucun `window.addEventListener('scroll')`** - uniquement Motion `useScroll()` / ScrollTrigger / IntersectionObserver / animations CSS pilotées par le défilement ?
- [ ] **Mouvement réduit** encapsulé pour tout ce qui est `MOTION_INTENSITY > 3` ?
- [ ] **Jetons du mode sombre** définis et testés dans les deux modes ?
- [ ] **Repli mobile explicite** (`w-full`, `px-4`, `max-w-7xl mx-auto`) pour les mises en page très variables ?
- [ ] **Stabilité de la fenêtre d'affichage** : `min-h-[100dvh]`, jamais `h-screen` ?
- [ ] **Les animations `useEffect`** disposent de fonctions de nettoyage strictes ?
- [ ] **États vide / chargement / erreur** prévus ?
- [ ] **Cartes omises** au profit de l'espacement lorsque c'est possible ?
- [ ] **Icônes** issues uniquement d'une bibliothèque autorisée (Phosphor / HugeIcons / Radix / Tabler), sans tracés SVG faits main ?
- [ ] **Mouvement** isolé dans des composants feuilles côté client avec `'use client'` en tête, mémoïsés ?
- [ ] **Aucun signe d'IA** de la Section 9 (Inter par défaut, violet IA, trois cartes égales, Jane Doe, Acme, « Discrètement utilisé par ») ?
- [ ] **Core Web Vitals** vraisemblablement atteints (LCP < 2,5 s, INP < 200 ms, CLS < 0,1) ?
- [ ] **Un seul système de design** par projet (pas de Material et shadcn mélangés) ?

Si une case à cocher ne peut pas être honnêtement cochée, la page n'est pas terminée. Corrigez-la avant de livrer.

---

# ANNEXES - Matériel de référence réel et sourcé

Les sections ci-dessous constituent du contenu de référence intégré. Elles fournissent de vraies commandes d'installation, de vrais liens vers la documentation canonique et de vrais extraits de démarrage fonctionnels pour chaque système de design nommé dans la section 2. Utilisez-les pour fonder les décisions sur la réalité de production, et non sur des fictions issues des données d'entraînement.

## Annexe A - Commandes d'installation par système de design

```bash
# Material Web (Material 3)
npm install @material/web

# Fluent UI React (v9)
npm install @fluentui/react-components

# Fluent UI Web Components (framework-free)
npm install @fluentui/web-components @fluentui/tokens

# IBM Carbon
npm install @carbon/react @carbon/styles

# Radix Themes
npm install @radix-ui/themes

# shadcn/ui (open code, owned components)
npx shadcn@latest init
npx shadcn@latest add button card badge separator input

# Primer CSS (GitHub product/devtool UI)
npm install --save @primer/css

# Primer Brand (GitHub marketing UI)
npm install @primer/react-brand

# GOV.UK Frontend
npm install govuk-frontend

# USWDS (US Web Design System)
npm install uswds

# Atlassian Design System (Atlaskit)
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card

# Bootstrap 5.3
npm install bootstrap

# Shopify Polaris Web Components (Shopify apps only)
# Add this to your app HTML head:
#   <meta name="shopify-api-key" content="%SHOPIFY_API_KEY%" />
#   <script src="https://cdn.shopify.com/shopifycloud/polaris.js"></script>
```


## Annexe B - Sources canoniques (à lire avant de réinventer)

### Material Web
- https://github.com/material-components/material-web
- https://material-web.dev/theming/material-theming/
- https://m3.material.io/develop/web

### Fluent UI
- https://fluent2.microsoft.design/get-started/develop
- https://fluent2.microsoft.design/components/web/react/
- https://github.com/microsoft/fluentui
- https://learn.microsoft.com/en-us/fluent-ui/web-components/

### Carbon
- https://carbondesignsystem.com/
- https://github.com/carbon-design-system/carbon
- https://carbondesignsystem.com/developing/react-tutorial/overview/
- https://carbondesignsystem.com/developing/web-components-tutorial/overview/

### Shopify Polaris
- https://shopify.dev/docs/api/app-home/web-components
- https://github.com/Shopify/polaris-react
- https://polaris-react.shopify.com/components

### Atlassian
- https://atlassian.design/get-started/develop
- https://atlassian.design/components/button/examples
- https://atlaskit.atlassian.com/packages/design-system/button/example/disabled
- https://atlassian.design/tokens/design-tokens

### Primer
- https://primer.style/
- https://github.com/primer/css
- https://github.com/primer/brand

### GOV.UK
- https://design-system.service.gov.uk/components/button/
- https://design-system.service.gov.uk/styles/layout/
- https://github.com/alphagov/govuk-frontend

### USWDS
- https://designsystem.digital.gov/documentation/developers/
- https://designsystem.digital.gov/components/button/
- https://designsystem.digital.gov/components/card/
- https://github.com/uswds/uswds

### Bootstrap
- https://getbootstrap.com/docs/5.3/layout/grid/
- https://getbootstrap.com/docs/5.3/components/card/

### Tailwind
- https://tailwindcss.com/docs/dark-mode
- https://tailwindcss.com/blog/tailwindcss-v4

### Radix
- https://www.radix-ui.com/themes/docs/components/theme
- https://www.radix-ui.com/themes/docs/components/card
- https://github.com/radix-ui/themes

### shadcn/ui
- https://ui.shadcn.com/docs
- https://ui.shadcn.com/docs/components/card
- https://github.com/shadcn-ui/ui

### CSS natif / standards W3C
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass (plateformes Apple uniquement)
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## Annexe C - Apple Liquid Glass : approximation web honnête

Ne **considérez pas** les extraits CSS aléatoires comme du véritable Apple Liquid Glass.

### Ce qui est officiel
Apple documente Liquid Glass dans ses Human Interface Guidelines et sa documentation pour développeurs destinées aux **plateformes Apple**. Il s'agit d'un matériau dynamique utilisé dans l'interface des plateformes Apple. L'implémentation native d'Apple relève des API des plateformes Apple et des composants système, **et non d'un package CSS web public**.

Documentation officielle pertinente :
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### Ce qui n'est PAS officiel
Il n'existe aucun `liquid-glass.css` publié par Apple pour les sites web classiques.

Une approximation web peut utiliser :
- `backdrop-filter`
- des arrière-plans transparents
- des bordures superposées
- des superpositions de mise en évidence
- des dégradés
- des animations
- des solutions de repli à fort contraste

Mais il s'agit d'une **approximation de glassmorphism / verre dépoli web**, et non du véritable Apple Liquid Glass. Indiquez-le clairement dans les commentaires.

### Squelette d'approximation web plus sûr

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```


**Important :** `prefers-reduced-transparency` présente une prise en charge inégale selon les navigateurs ; testez-le. Fournissez toujours un contraste suffisant, même sans flou.

---

**Fin des annexes.** Les commandes d'installation ci-dessus sont des points de référence réels. Le squelette Apple Liquid Glass est une approximation étiquetée, et non un package publié par Apple. Pour la documentation canonique de chaque système de design, consultez la documentation officielle du système (liens de la section 2 et annexe B).
