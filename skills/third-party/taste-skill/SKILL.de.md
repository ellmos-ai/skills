---
name: design-taste-frontend
description: "Anti-Slop-Frontend-Skill für Landingpages, Portfolios und Redesigns. Der Agent liest das Briefing, leitet die passende Designrichtung ab und liefert Oberflächen, die nicht nach Vorlage aussehen. Echte Designsysteme, wo sinnvoll, Audit-first bei Redesigns und eine strenge Pre-Flight-Prüfung."
third_party: true
license: MIT
upstream: https://github.com/Leonxlnx/taste-skill
category: dev
language: de
translated_from_sha256: 7616ab6689efd139d313f95808165c7e4752bd39d50ed6a0533a120b8ff81002
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T05:13:53.734409+00:00"
---
<img src="banner.png" width="100%" alt="taste-skill banner">

# tasteskill: Anti-Slop-Frontend-Skill

> Landingpages, Portfolios und Redesigns. Keine Dashboards, keine Datentabellen, keine mehrstufige Produkt-UI.
> Jede der folgenden Regeln ist **kontextabhängig**. Keine davon greift automatisch. Zuerst wird das Briefing gelesen, dann werden nur die Regeln herangezogen, die passen.

---

## 0. BRIEFING-INFERENZ (Erst die Lage erfassen, dann handeln)

Bevor Code angefasst oder an Reglern gedreht wird, **ableiten, was der Nutzer tatsächlich will**. Die meisten schlechten Design-Ergebnisse von LLMs entstehen, weil das Modell sofort zu einer Standardästhetik greift, statt die Lage zu erfassen.

### 0.A Zuerst diese Signale lesen
1. **Seitentyp** - Landingpage (SaaS / Consumer / Agentur / Event), Portfolio (Entwickler / Designer / Kreativstudio), Redesign (bewahren vs. grundlegend überarbeiten), Editorial / Blog.
2. **Stichwörter zur Anmutung**, die der Nutzer verwendet hat - „minimalistisch“, „ruhig“, „Linear-Stil“, „Awwwards“, „brutalistisch“, „Premium-Consumer“, „Apple-artig“, „verspielt“, „seriöses B2B“, „editorial“, „agenturhaft“, „glasig“, „dunkles Tech-Design“.
3. **Referenzsignale** - verlinkte URLs, eingefügte Screenshots, genannte Produkte, Marken, mit denen man konkurriert.
4. **Zielgruppe** - B2B-Einkaufsgremium vs. designbewusste Konsumenten vs. Recruiter, der ein Portfolio überfliegt. Die Zielgruppe bestimmt die Ästhetik, nicht dein persönlicher Geschmack.
5. **Bereits vorhandene Markenmittel** - Logo, Farben, Typografie, Fotografie. Bei Redesigns sind sie Ausgangsmaterial, keine optionale Eingabe (siehe Abschnitt 11).
6. **Stille Randbedingungen** - Zielgruppen mit Fokus auf Barrierefreiheit, öffentlicher Sektor, regulierte Branchen, vertrauenskritischer Handel, Kinderprodukte. Diese Randbedingungen **überstimmen** ästhetische Vorlieben.

### 0.B Vor der Generierung eine einzeilige „Design-Lesart“ ausgeben
Bevor Code entsteht, in einer Zeile festhalten: **„Ich lese das als: \<page kind> für \<audience>, mit einer \<vibe>-Sprache, tendenziell \<design system or aesthetic family>.“**

Beispiel-Lesarten:
- *„Ich lese das als: B2B-SaaS-Landingpage für technische Käufer, mit einer minimalistischen Sprache im Linear-Stil, tendenziell Tailwind-Utilities + Geist + zurückhaltende Bewegung.“*
- *„Ich lese das als: Solo-Designer-Portfolio für Personalverantwortliche, mit einer editorialen / kinetischen Typografie-Sprache, tendenziell natives CSS + scrollgesteuerte Animation + eigene Typografie.“*
- *„Ich lese das als: Redesign einer Website eines öffentlichen Dienstes, mit einer vertrauensorientierten Sprache, tendenziell GOV.UK Frontend oder USWDS.“*

### 0.C Ist das Briefing mehrdeutig, eine Rückfrage stellen, nicht raten
Genau **eine** klärende Frage stellen – niemals eine Sammlung mehrerer Fragen – und nur dann, wenn sich die Design-Lesart tatsächlich aufspaltet. Beispiel: *„Soll das eher in Richtung Linear-clean oder Awwwards-experimentell gehen?“*

Wenn sich der Kontext sicher ableiten lässt, **nicht nachfragen**. Einfach die Design-Lesart erklären und weitermachen.

### 0.D Disziplin gegen Standardlösungen
Nicht zurückgreifen auf: KI-typische Lila-Verläufe, zentrierter Hero über dunklem Mesh-Hintergrund, drei gleich große Feature-Karten, generischer Glassmorphismus auf allem, endlos laufende Mikroanimationen überall, Inter + Slate-900. Das sind die Standardvorgaben von LLMs. Bewusst darüber hinausgehen, abhängig von der Design-Lesart.

---

## 1. DIE DREI REGLER (Kernkonfiguration)

Nach der Design-Lesart drei Regler festlegen. Jede Entscheidung zu Layout, Bewegung und Informationsdichte unten richtet sich nach diesen Reglern.

* **`DESIGN_VARIANCE: 8`** - 1 = perfekte Symmetrie, 10 = künstlerisches Chaos
* **`MOTION_INTENSITY: 6`** - 1 = statisch, 10 = filmisch / physikbasiert
* **`VISUAL_DENSITY: 4`** - 1 = Kunstgalerie / luftig, 10 = Cockpit / dicht gepackte Daten

**Grundwert:** `8 / 6 / 4`. Diese Werte verwenden, sofern die Design-Lesart sie nicht überschreibt. Den Nutzer nicht bitten, diese Datei zu bearbeiten – Überschreibungen erfolgen im Gespräch.

### 1.A Reglerableitung (Design-Lesart → Reglerwerte)
| Signal | VARIANZ | BEWEGUNG | DICHTE |
|---|---|---|---|
| „minimalistisch / sauber / ruhig / editorial / Linear-Stil“ | 5-6 | 3-4 | 2-3 |
| „Premium-Consumer / Apple-artig / Luxus / Marke“ | 7-8 | 5-7 | 3-4 |
| „verspielt / wild / Dribbble / Awwwards / experimentell / agenturhaft“ | 9-10 | 8-10 | 3-4 |
| „Landingpage / Portfolio / Marketingseite (Standard)“ | 7-9 | 6-8 | 3-5 |
| „vertrauensorientiert / öffentlicher Sektor / reguliert / barrierefreiheitskritisch“ | 3-4 | 2-3 | 4-5 |
| „Redesign – bewahren“ | wie bisher | +1 | wie bisher |
| „Redesign – grundlegend überarbeiten“ | +2 | +2 | wie bisher |

### 1.B Anwendungsfall-Voreinstellungen
| Anwendungsfall | VARIANZ | BEWEGUNG | DICHTE |
|---|---|---|---|
| Landingpage (SaaS, mainstream) | 7 | 6 | 4 |
| Landingpage (Agentur / kreativ) | 9 | 8 | 3 |
| Landingpage (Premium-Consumer) | 7 | 6 | 3 |
| Portfolio (Designer / Studio) | 8 | 7 | 3 |
| Portfolio (Entwickler) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Dienst im öffentlichen Sektor | 3 | 2 | 5 |
| Redesign – bewahren | wie bisher | wie bisher +1 | wie bisher |
| Redesign – grundlegend überarbeiten | +2 | +2 | wie bisher |

### 1.C Wie die Regler die Ausgabe steuern
Diese Werte (oder die vom Nutzer überschriebenen Werte) als globale Variablen verwenden. Querverweise im gesamten Dokument beziehen sich auf genau diese Variablennamen – niemals eigene Aliasse wie `LAYOUT_VARIANCE` oder `ANIM_LEVEL` erfinden.

---

## 2. VON DER DESIGN-LESART ZUM DESIGNSYSTEM

Sobald Design-Lesart (Abschnitt 0) und Regler (Abschnitt 1) vorliegen, die passende Grundlage wählen. Kein CSS für Dinge erfinden, die es als offizielles Paket gibt. Einen ästhetischen Trend nicht als offizielles System ausgeben.

### 2.A Wann man ein echtes Design-System verwenden sollte (offizielle Pakete verwenden)

| Briefing liest sich als… | Verwenden | Warum |
|---|---|---|
| Microsoft / Enterprise-SaaS / Dashboards | `@fluentui/react-components` oder `@fluentui/web-components` | Offizielles Fluent UI, Microsoft-Tokens, Barrierefreiheit bereits umgesetzt |
| Google-ähnliche Oberfläche, Material-orientiertes Produkt | `@material/web` + Material-3-Tokens | Offiziell, über Material Theming anpassbar |
| IBM-artiges B2B / Enterprise-Analytics | `@carbon/react` + `@carbon/styles` | Offizielles Carbon, ausgereifte Muster für hohe Datendichte |
| Shopify-App-Oberflächen | `polaris.js` Web Components / Polaris React | Erforderlich für die Shopify-Admin-Oberfläche |
| Atlassian- / Jira-artiges Produkt | `@atlaskit/*` + `@atlaskit/tokens` | Offizielles Atlassian Design System |
| GitHub-artiges Devtool / Community-Seite | `@primer/css` oder `@primer/react-brand` | Offizielles Primer; Brand-Variante für Marketing |
| Öffentlicher Dienst im Vereinigten Königreich | `govuk-frontend` | Rechtlich / regulatorisch erwartet |
| Öffentlicher Sektor in den USA / vertrauensorientiert | `uswds` | Gleiche Begründung |
| Schnelle MVP für lokale Unternehmen / Agenturen | Bootstrap 5.3 | Unaufgeregt, schnell, funktioniert |
| Moderne, barrierefreie React-Grundlage | `@radix-ui/themes` | Primitives + polierte Theme |
| Moderne SaaS, bei der man die Komponenten selbst besitzt | shadcn/ui (`npx shadcn@latest add ...`) | Du besitzt den Code, leicht anpassbar; niemals im Standardzustand ausliefern |
| Tailwind-basiertes modernes SaaS / KI-Marketing | Tailwind-v4-Utilities + `dark:`-Variante | Standard für Indie- und Kleinteam-Projekte |

**Ehrlichkeitsregel:** Wenn das Briefing einem der oben genannten Systeme entspricht, installiere und verwende das **offizielle** Paket. Baue dessen CSS nicht von Hand nach. Importiere nicht die Tokens eines Systems und überschreibe dann 90 % davon.

**Ein System pro Projekt.** Mische nicht Fluent React mit Carbon im selben Komponentenbaum. Importiere keine shadcn/ui-Komponenten in eine Material-3-App.

### 2.B Wenn das Briefing eine Ästhetik und kein System ist

Für diese Richtungen gibt es **kein einzelnes offizielles Paket**. Baue mit nativem CSS + Tailwind + einer gepflegten Komponentenbibliothek. Sei in Code-Kommentaren ehrlich darüber, was geborgene Inspiration und was offizielles Material ist.

| Ästhetik | Ehrliche Umsetzung |
|---|---|
| Glassmorphismus / „Milchglas“ | `backdrop-filter`, geschichtete Rahmen, Highlight-Overlays. Eine Vollfarb-Fallback-Lösung für `prefers-reduced-transparency` bereitstellen. |
| Bento (Apple-artige Kachelraster) | CSS Grid mit gemischten Zellgrößen. Keine einzelne Bibliothek besitzt dies. |
| Brutalismus | Natives CSS, Monospace, rohe Rahmen. Keine Bibliothek. |
| Editorial / Magazin | Serifen-Typografie, asymmetrisches Raster, großzügiger Weißraum. Keine Bibliothek. |
| Dark Tech / Hacker | Mono + neonfarbener Akzent, Terminal-Motive. Keine Bibliothek. |
| Aurora / Mesh-Verläufe | SVG oder geschichtete radiale Verläufe. Keine Bibliothek. |
| Kinetische Typografie | Native CSS-Animationen, scrollgesteuerte Animationen, GSAP für Hijacks. Keine Bibliothek. |
| **Apple Liquid Glass** | Apple dokumentiert dies nur für Apple-Plattformen. **Es gibt kein offizielles `liquid-glass.css`.** Web-Umsetzungen sind Näherungen mit `backdrop-filter` + geschichteten Rahmen + Highlights. Klar als Näherung kennzeichnen. |

---

## 3. STANDARDARCHITEKTUR & KONVENTIONEN

Sofern die Designvorgabe kein echtes Design-System (Abschnitt 2.A) auswählt, gelten diese Standards:

### 3.A Stack
* **Framework:** React oder Next.js. Standardmäßig Server Components (RSC) verwenden.
  * **RSC-SICHERHEIT:** Globaler Zustand funktioniert NUR in Client Components. In Next.js Provider in eine `"use client"`-Komponente einschließen.
  * **ISOLATION INTERAKTIVITÄT:** Jede Komponente, die Motion, Scroll-Listener oder Zeigerphysik verwendet, MUSS ein isoliertes Blatt sein, oben mit `'use client'`. Server Components rendern nur statische Layouts.
* **Styling:** **Tailwind v4** (Standard). Tailwind v3 nur, wenn das bestehende Projekt es erfordert.
  * Für v4: Verwende das `tailwindcss`-Plugin NICHT in `postcss.config.js`. Verwende stattdessen `@tailwindcss/postcss` oder das Vite-Plugin.
* **Animation:** **Motion** (die früher als Framer Motion bekannte Bibliothek). Import aus `motion/react` (`import { motion } from "motion/react"`). Das Paket `framer-motion` funktioniert weiterhin als veralteter Alias – in neuem Code `motion/react` bevorzugen.
* **Schriften:** Immer `next/font` (Next.js) verwenden oder selbst hosten mit `@font-face` + `font-display: swap`. Google Fonts niemals in der Produktion über `<link>` einbinden.

### 3.B Zustand
* Lokaler `useState` / `useReducer` für isolierte UI.
* Globaler Zustand NUR zur Vermeidung von tiefem Prop-Drilling – Zustand, Jotai oder React Context.
* **NIEMALS** `useState` verwenden, um kontinuierliche, durch Benutzereingaben gesteuerte Werte zu verfolgen (Mausposition, Scrollfortschritt, Zeigerphysik, magnetisches Hover). Stattdessen Motions `useMotionValue` / `useTransform` / `useScroll` verwenden. `useState` rendert den React-Baum bei jeder Änderung neu und bricht auf Mobilgeräten ein.

### 3.C Icons
* **Erlaubte Bibliotheken (Prioritätsreihenfolge):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Nicht empfohlen:** `lucide-react`. Nur akzeptabel, wenn der Benutzer ausdrücklich darum bittet oder das Projekt bereits davon abhängt.
* **NIEMALS SVG-Icons von Hand erstellen.** Wenn ein Glyph fehlt, eine zweite Bibliothek installieren oder aus Primitiven zusammensetzen – Icon-Pfade nicht von Grund auf zeichnen.
* **Eine Familie pro Projekt.** Phosphor nicht mit Lucide im selben Komponentenbaum mischen.
* **`strokeWidth` global standardisieren** (z. B. `1.5` oder `2.0`).

### 3.D Emoji-Richtlinie
Standardmäßig im Code, in Markup und im sichtbaren Text nicht empfohlen. Symbole durch Icon-Bibliotheks-Glyphen ersetzen. **Ausnahme:** Emojis nur erlauben, wenn der Benutzer ausdrücklich eine verspielte / chatartige / social-native Anmutung wünscht – und auch dann sparsam und bewusst einsetzen.

### 3.E Responsivitäts- und Layout-Mechanik

* Breakpoints vereinheitlichen (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Seitenlayouts begrenzen mit `max-w-[1400px] mx-auto` oder `max-w-7xl`.
* **Viewport-Stabilität:** NIEMALS `h-screen` für vollhohe Hero-Bereiche verwenden. IMMER `min-h-[100dvh]` verwenden, um Layout-Sprünge auf mobilen Geräten (iOS Safari Adressleiste) zu verhindern.
* **Grid statt Flex-Mathematik:** NIEMALS komplexe Flexbox-Prozentberechnungen (`w-[calc(33%-1rem)]`) verwenden. IMMER CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) verwenden.

### 3.F Abhängigkeitsprüfung (verpflichtend)

Bevor eine Drittanbieter-Bibliothek importiert wird, `package.json` prüfen. Fehlt das Paket, zuerst den Installationsbefehl ausgeben. **Niemals** die Existenz einer Bibliothek voraussetzen.

---

## 4. DESIGN-ENGINEERING-RICHTLINIEN (Bias-Korrektur)

LLMs greifen standardmäßig auf Klischees zurück. Diese Voreinstellungen proaktiv überschreiben. Jede Regel hat einen kontextabhängigen Überschreibungspfad.

### 4.1 Typografie

* **Display / Überschriften:** Standard `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Fließtext / Absätze:** Standard `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Wahl der serifenlosen Schrift:**
  * **Als Standard nicht empfohlen:** `Inter`. Zuerst `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi` oder eine markengerechte Serifenschrift wählen.
  * **Überschreibung:** Inter ist akzeptabel, wenn der Nutzer ausdrücklich ein neutrales / standardisiertes / Linear-artiges Erscheinungsbild wünscht oder wenn das Briefing eine Website für den öffentlichen Sektor bzw. eine barrierefreiheitsorientierte Website betrifft.
* **Bekannte Kombinationen:** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.

* **SERIFEN-DISZIPLIN (ALS STANDARD SEHR NICHT EMPFOHLEN):**
  * Serif ist **als Standardschrift für jedes Projekt sehr nicht empfohlen.** „Wirkt kreativ / hochwertig / redaktionell“ ist KEIN Grund, zu einer Serifenschrift zu greifen. Das Standardmodell des Agenten, dass „kreatives Briefing = Serife“ bedeutet, ist der meistgetestete KI-Marker in Produktionsrunden.
  * **Serif ist nur akzeptabel, wenn EINE der folgenden Bedingungen ausdrücklich zutrifft:**
    - Das Markenbriefing nennt wörtlich eine Serifenschrift, ODER
    - Die ästhetische Familie ist tatsächlich redaktionell / Luxus / Publikation / Manuskript / Tradition / Vintage, UND du kannst begründen, warum genau diese Serifenschrift zu dieser konkreten Marke passt
  * Für alles andere (Kreativagentur, Designstudio, moderne Marke, hochwertiges Konsumgut, Portfolio, Lifestyle) gilt als **Standard eine serifenlose Display-Schrift** (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). Serifenlose Display-Schriften sind nicht „langweilig“ – sie sind der Standard aus demselben Grund, aus dem Schwarz in der Mode der Standard ist.
  * **BETONUNGSREGEL (verwandt):** Wenn du ein Wort innerhalb einer Überschrift hervorheben willst (der dynamische Stil „und `spatial` design“), verwende **Kursiv oder Fettschnitt DERSELBEN Schrift**. Füge KEIN zufälliges Serifenwort in eine serifenlose Überschrift ein (oder umgekehrt), nur um visuelles Interesse zu erzeugen. Gemischte Schriftfamilien zur Betonung wirken amateurhaft. Kursiv-/Fettbetonung innerhalb derselben Familie ist der richtige Weg.
  * **Ausdrücklich als Standard verboten:** `Fraunces` und `Instrument_Serif` (die beiden bei LLMs beliebtesten Display-Serifen).
  * **Falls eine Serifenschrift begründet ist** (selten, gemäß obigen Regeln), aus diesem Pool rotieren und NICHT dieselbe Serifenschrift in aufeinanderfolgenden Projekten wiederverwenden: PP Editorial New, GT Sectra Display, Cardinal Grotesque, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.

* **FREIRAUM FÜR KURSIVE UNTERLÄNGEN (verpflichtend):** Wird Kursiv in Display-Typografie verwendet und enthält das Wort einen Buchstaben mit Unterlänge (`y g j p q`), wird `leading-[1]` oder `leading-none` die Unterlänge abschneiden. Mindestens `leading-[1.1]` verwenden und auf dem umschließenden Element `pb-1` oder `mb-1` Freiraum ergänzen. Jedes kursive Wort in Display-Überschriften vor der Auslieferung prüfen.

### 4.2 Farbkalibrierung
* Maximal 1 Akzentfarbe. Sättigung standardmäßig < 80 %.
* **DIE LILA-REGEL:** Die Ästhetik „KI-Lila / Blau-Glühen“ wird als Standard nicht empfohlen. Keine automatischen lila Button-Glühen, keine zufälligen Neon-Verläufe. Verwende neutrale Basen (Zink / Schiefer / Stein) mit kontrastreichen, einzelnen Akzenten (Smaragd, Elektrisches Blau, Tiefes Rosé, Gebranntes Orange usw.).
* **Ausnahme:** Wenn die Marke oder das Briefing ausdrücklich Lila / Violett / Lila verlangt, wird dies umgesetzt. Dabei jedoch mit Absicht vorgehen: konsistente Palette, harmonisierte Neutraltöne, zurückhaltende Verläufe. Kein generischer KI-Verlaufs-Einheitsbrei.
* **Eine Palette pro Projekt.** Nicht zwischen warmen und kühlen Grautönen innerhalb desselben Projekts wechseln.
* **FARBKONSISTENZ-SPERRE (verpflichtend):** Sobald eine Akzentfarbe für eine Seite gewählt wurde, wird sie auf der GANZEN Seite verwendet. Eine warmgraue Website bekommt in Abschnitt 7 nicht plötzlich einen blauen CTA. Eine rosa akzentuierte Website bekommt im Footer kein türkisfarbenes Statusabzeichen. Wähle einen Akzent, sperre ihn und prüfe jede Komponente vor der Auslieferung.

* **VERBOT DER PREMIUM-CONSUMER-PALETTE (verpflichtend, zweithäufigstes KI-Erkennungsmerkmal):**
  * Bei Briefings für Premium-Konsumgüter (Kochgeschirr, Wellness, Handwerkskunst, Luxus, traditionelles Handwerk, DTC-Wohnaccessoires usw.) greift der LLM-Standard auf **warmes Beige/Creme + Messing/Ton/Ochsenblut/Ocker + Espresso/Tintenschwarz als Textfarbe** zurück. Konkret verbotene Hex-Familien als Standard-Hintergründe und Akzente:
    - Hintergründe: `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb` (alle „warmes Papier / Creme / Kreide / Knochenweiß“)
    - Akzente: `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621` (alle „Messing / Ton / Ochsenblut / Ocker“)
    - Text: `#1a1714`, `#1a1814`, `#1b1814` (alle „Espresso / warmes Fast-Schwarz“)
  * Diese Palette ist als Standard für Premium-Consumer-Briefings VERBOTEN. Jede Premium-Consumer-Website, die du jemals ausgeliefert hast, verwendete genau diese Palette. Die Marke wird dadurch unsichtbar.
  * **Standardalternativen (rotieren, nicht wiederverwenden):**
    - **Kalter Luxus:** Silbergrau + Chrom + Rauchgrau (denke an Tesla, Apple Watch, Hermès ohne das Leder)
    - **Wald:** Tiefgrün + Knochenweiß + bernsteinfarbener Akzent (denke an Filson, Patagonia Premium)
    - **Schwarz und Tan:** echtes Off-Schwarz + warmes Tan, scharfer Kontrast, kein Beige
    - **Kobaltblau + Creme:** gesättigtes Blau vor einem einzelnen Neutralton, kein Messing
    - **Terrakotta + Schiefer:** warmes Rostrot vor kühlem Grau, kein Messing
    - **Oliv + Ziegelrot + Papier:** gedämpftes Oliv mit ziegelrotem Akzent
    - **Reine Monochromie + ein gesättigter Farbtupfer:** Off-White + Off-Schwarz + ein leuchtender Akzent (elektrisches Blau, Smaragd, Knallpink usw.)
  * **Palettenrotationsregel:** Wenn das vorherige Premium-Consumer-Projekt die Beige+Messing-Familie verwendet hat, MUSS dieses eine andere Familie verwenden. Liefere nicht zweimal hintereinander dieselbe warme Handwerkspalette aus.
  * **Ausnahme:** Die Beige+Messing+Espresso-Palette ist NUR akzeptabel, wenn das Markenbriefing diese Farben ausdrücklich nennt oder wenn die Markenidentität wirklich vintage / handwerklich-warm ist UND du begründen kannst, warum genau diese Palette zu genau dieser Marke passt. Sie aus dem Grund zu wählen, dass „dies ein Kochgeschirr-Briefing ist“, ist verboten.

### 4.3 Layoutdiversifizierung
* **ANTI-ZENTRIERUNGS-BIAS:** Zentrierte Hero- / H1-Abschnitte werden vermieden, wenn `DESIGN_VARIANCE > 4`. Erzwinge „Geteilter Bildschirm“ (50/50), „Linksbündiger Inhalt / rechtsbündiges Asset“, „Asymmetrischer Weißraum“ oder scroll-fixierte Strukturen.
* **Ausnahme:** Ein zentrierter Hero ist für redaktionelle / manifestartige / Launch-Ankündigungs-Briefings in Ordnung, bei denen die Botschaft selbst das Design ist.

### 4.4 Materialität, Schatten, Karten
* Verwende Karten NUR, wenn Erhebung echte Hierarchie vermittelt. Andernfalls mit `border-t`, `divide-y` oder Negativraum gruppieren.
* Wenn ein Schatten verwendet wird, töne ihn auf den Farbton des Hintergrunds ab. Keine reinschwarzen Schlagschatten auf hellen Hintergründen.
* Für `VISUAL_DENSITY > 7`: generische Kartencontainer sind verboten. Datenmetriken brauchen in einem schlichten Layout Raum zum Atmen.
* **FORMKONSISTENZ-SPERRE (verpflichtend):** Wähle EINE Eckradius-Skala für die Seite und halte dich daran. Optionen: durchgehend scharfkantig (Radius 0), durchgehend weich (Radius 12–16 px), durchgehend pillenförmig (voller Radius für interaktive Elemente). Gemischte Systeme sind nur erlaubt, wenn eine dokumentierte Regel existiert (z. B. „Buttons sind vollständig pillenförmig, Karten haben 16 px, Eingabefelder 8 px“) und diese Regel überall befolgt wird. Runde Buttons in einem quadratischen Layout oder quadratische Karten auf einer Seite mit pillenförmigen Buttons sind fehlerhaftes Design.

### 4.5 Interaktive UI-Zustände

LLMs neigen standardmäßig zu „nur statischer Erfolgszustand". Implementiere immer vollständige Zyklen:
* **Ladezustand:** Skelett-Loader, die der Form des endgültigen Layouts entsprechen. Vermeide generische kreisförmige Spinner.
* **Leere Zustände:** Schön gestaltet; zeige an, wie man sie befüllt.
* **Fehlerzustände:** Klar, inline (bei Formularen) oder kontextbezogen (Toasts nur für vorübergehende Meldungen).
* **Taktiles Feedback:** Auf `:active` verwende `-translate-y-[1px]` oder `scale-[0.98]`, um einen physischen Tastendruck zu simulieren.
* **BUTTON-KONTRASTPRÜFUNG (verpflichtend, a11y):** Bevor ein Button ausgeliefert wird, prüfe, ob der Buttontext vor dem Buttonhintergrund gut lesbar ist. Weißer Button mit weißem Text, `bg-white`-CTA mit `text-white`-Beschriftung, transparenter Button auf dem Seitenhintergrund ohne Rahmen → alle verboten. Prüfe jeden CTA: Kontrastverhältnis mindestens WCAG AA (4,5:1 für Fließtext, 3:1 für großen Text ab 18px). Dieselbe Regel gilt für Ghost-Buttons über fotografischen Hintergründen (verwende einen Hintergrundschleier, eine Abdunklung oder eine Kontur).
* **CTA-BUTTON-UMBRUCHVERBOT (verpflichtend):** Der Buttontext MUSS auf dem Desktop in eine Zeile passen. Wenn eine Beschriftung wie „VIEW SELECTED WORK" auf 2 oder 3 Zeilen umbricht, ist der Button fehlerhaft. Behebe dies entweder durch Kürzen der Beschriftung (maximal 3 Wörter für primäre CTAs, idealerweise 1-2) ODER durch Verbreitern des Buttons (`max-width` bei CTAs nicht künstlich einschränken). Umbrochene CTAs auf dem Desktop sind ein Pre-Flight-Fehler.
* **KEINE DOPPELTE CTA-ABSICHT (verpflichtend):** Zwei CTAs mit derselben Absicht auf einer Seite sind ein Pre-Flight-Fehler. Beispiele für dieselbe Absicht: „Get in touch" + „Contact us" + „Let's talk" + „Start a project" + „Start something" + „Reach out" = alle Absicht „Kontakt" → wähle EIN Label und verwende es überall auf der Seite (Navigation, Hero-Bereich, Fußzeile). Dasselbe gilt für „Try free" + „Get started" + „Sign up free" (alle Absicht „Anmeldung") und „View work" + „See selected work" + „Browse projects" (alle Absicht „Portfolio"). Ein Label pro Absicht.
* **FORMULAR-KONTRASTPRÜFUNG (verpflichtend, a11y):** Formulareingabefelder, Platzhaltertext, Fokusrahmen, Hilfetexte und Fehlertexte müssen alle WCAG AA-Kontrast gegenüber dem Abschnittshintergrund erfüllen. Helle Platzhalter auf einem nahezu weißen Formular, weißes Formular auf weißem Seitenabschnitt, Formularbeschriftungen mit weniger als 4,5:1 Kontrast → alle verboten. Prüfe jedes Formular vor der Auslieferung.

### 4.6 Daten- & Formularmuster
* Beschriftung ÜBER dem Eingabefeld. Hilfetext optional, aber im Markup vorhanden. Fehlertext UNTER dem Eingabefeld. Standard `gap-2` für Eingabeblöcke.
* Kein Platzhalter-als-Beschriftung. Niemals.

### 4.7 Layout-Disziplin (harte Regeln. Die Verletzung einer dieser Regeln bedeutet fehlerhafte Auslieferung)

* **Hero muss im ersten Viewport passen.** Überschrift maximal 2 Zeilen auf dem Desktop, Untertext maximal **20 Wörter** UND maximal 3-4 Zeilen, CTAs ohne Scrollen sichtbar. Ist der Text zu lang: Schriftgröße reduzieren ODER Text kürzen. Wenn du das Wertversprechen nicht in 20 Wörtern Untertext beschreiben kannst, ist das Wertversprechen unklar, nicht die Regel zu eng. Lass die Hero niemals überlaufen und erzwinge kein Scrollen, um den CTA zu finden.
* **Schriftgrößen-Disziplin im Hero.** Plane Schriftgröße und Bildgröße *gemeinsam*. Ist das Hero-Asset groß und die Überschrift länger als 6 Wörter, beginne nicht bei `text-7xl/text-8xl`. Sinnvoller Standardbereich: `text-4xl md:text-5xl lg:text-6xl` für die meisten Heroes; `text-6xl md:text-7xl` nur, wenn die Überschrift 3-5 Wörter hat. Eine 4-zeilige Hero-Überschrift ist immer ein Schriftgrößenfehler, niemals ein Textlängenfehler.
* **OBERE HERO-ABSTANDSOBERGRENZE (verpflichtend):** Der obere Hero-Abstand beträgt auf dem Desktop maximal `pt-24` (≈6rem). Alles darüber lässt den Hero-Inhalt auf halber Höhe des Viewports schweben und wirkt wie ein Layoutfehler, nicht wie beabsichtigter Freiraum. Braucht dein Hero mehr Luft, erhöhe die Schriftskala oder die Asset-Größe, nicht den oberen Abstand.
* **HERO-STAPEL-DISZIPLIN (maximal 4 Textelemente).** Der Hero ist ein einzelner Moment, keine Feature-Liste. Erlaubte Textelemente, insgesamt maximal 4:
  1. Eyebrow (kleines Großbuchstaben-Label) ODER Markenleiste ODER keines - wähle null oder eines
  2. Überschrift (maximal 2 Zeilen, siehe oben)
  3. Untertext (maximal 20 Wörter, maximal 4 Zeilen)
  4. CTAs (1 primär + maximal 1 sekundär)
  - **IM HERO VERBOTEN:** winziger Tagline-Text unter den CTAs („Funktioniert mit GitHub, GitLab und selbst gehostetem Git“), Vertrauens-Mikroleiste („Genutzt von Engineering-Teams bei…“), Preisvorschau („Kostenlos für Einzelpersonen, 10 $/Nutzer für Teams“), Feature-Aufzählungsliste, Social-Proof-Avatarreihe. All das gehört in eigene Abschnitte direkt unterhalb des Heros.
  - Hast du im selben Hero einen Eyebrow UND eine Tagline unter den CTAs, streiche die Tagline. Hast du eine Markenleiste UND eine Tagline, streiche die Tagline. Pro Hero höchstens ein kleines Textelement.
* **Die Logo-Wand „Genutzt von“ / „Vertraut von“ gehört UNTER den Hero, niemals hinein.** Der Hero dient dem Wertversprechen und dem primären CTA. Die Logo-Wand ist ein eigener Abschnitt direkt darunter. Stopfe keine Vertrauenslogos in dieselbe Flex-Zeile wie der Hero-Text.
* **Die Navigation MUSS auf dem Desktop in einer einzigen Zeile dargestellt werden.** Passen die Einträge bei `lg` (1024px) nicht, verkürze die Beschriftungen, entferne sekundäre Einträge oder wechsle zu einem Hamburger-Menü. Eine zweizeilige Navigation auf dem Desktop ist fehlerhaftes Design.
* **Navigationshöhe maximal 80px auf dem Desktop, Standard 64-72px.** Keine riesigen „Agentur“-Navigationsleisten, die 15 % des Viewports fressen.
* **Bento-Raster müssen Rhythmus haben, keine einseitige Wiederholung.** Staple nicht 6 Zeilen mit Bild links / Text rechts. Variiere die Komposition: wechsle zwischen vollbreiten Feature-Zeilen, asymmetrischen Kachelgrößen und vertikalen Umbrüchen.
* **BENTO-ZELLENANZAHL-REGEL (verpflichtend):** Ein Bento-Raster hat GENAU so viele Zellen, wie du Inhalte hast. 3 Elemente → 3 Zellen (1+2-Aufteilung, 2+1 oder asymmetrisches Trio). 5 Elemente → 5 Zellen (2+3, 3+2, Hero+4 usw.). Hat dein Raster eine leere Zelle in der Mitte oder am Ende, hast du falsch geplant. Forme das Raster neu; klebe keine leere Kachel ein.
* **Verbot der Wiederholung von Abschnitts-Layouts.** Sobald du eine Layoutfamilie für einen Abschnitt verwendest (z. B. 3-Spalten-Bildkarten, vollbreites Zitat, geteilter Text-Bild-Block), darf diese Familie auf der Seite höchstens EINMAL vorkommen. „Ausgewählte Aufträge“ darf nicht wie „Was wir tun“ aussehen. Eine Landingpage mit 8 Abschnitten muss mindestens 4 verschiedene Layoutfamilien verwenden.
* **ZICKZACK-WECHSELGRENZE (verpflichtend).** Das abwechselnde Layout „Bild links + Text rechts“, dann „Text links + Bild rechts“ ist banal. Maximal 2 Abschnitte hintereinander mit diesem Bild-Text-Teilungsmuster. Die 3. aufeinanderfolgende Bild-Text-Teilung ist ein Pre-Flight-Fehler. Durchbrich das Muster mit einem vollbreiten Abschnitt, einem vertikalen Stapel-Abschnitt, einem Bento-Raster, einem Marquee oder einer anderen Layoutfamilie.
* **EYEBROW-ZURÜCKHALTUNG (verpflichtend, der in Produktionstests am häufigsten verletzte Punkt).** Ein „Eyebrow“ ist das kleine Großbuchstaben-Label mit weiter Laufweite, das über einer Abschnittsüberschrift steht (z. B. `FOUR COLORWAYS`, `SELECTED WORK`, `THE HARDWARE`, `Git-native task management`). Typische CSS-Signatur: `text-[11px] uppercase tracking-[0.18em]`, `font-mono text-[10.5px] uppercase tracking-[0.22em]`. Jede KI-gebaute Website setzt über JEDE Abschnittsüberschrift einen Eyebrow und erzeugt so denselben schablonenhaften Rhythmus. Harte Regel:
  - **Maximal 1 Eyebrow pro 3 Abschnitte.** Der Hero zählt als 1. Eine Seite mit 9 Abschnitten darf also insgesamt höchstens 3 Eyebrows verwenden.
  - Hat Abschnitt A einen Eyebrow, dürfen die nächsten 2 Abschnitte keinen haben.
  - **Pre-Flight-Prüfung ist mechanisch:** Zähle die Vorkommen von `uppercase tracking` (oder ähnlichen kleinen Mono-Labels über Überschriften) über alle Abschnittskomponenten. Ist die Anzahl > ceil(Abschnittsanzahl / 3), schlägt die Ausgabe fehl.
  - **Was stattdessen tun:** Lass den Eyebrow ganz weg. Die Überschrift allein genügt. Musst du einen Abschnitt kategorisieren, kategorisiert ihn bereits seine Position auf der Seite; kein Label nötig.
* **VERBOT DER GETEILTEN KOPFZEILE (verpflichtend).** Das Muster „große Überschrift links + kleiner erklärender Absatz rechts“ als Abschnittskopf (links col-span-7/8, rechts col-span-4/5 mit einem kleinen Fließtextabsatz in der rechten Spalte) ist **als Standard verboten**. Abschnitte sollen EINE fokussierte Botschaft haben. Brauchst du wirklich sowohl Überschrift als auch erklärenden Absatz, stapele sie vertikal (Überschrift oben, Text darunter, maximale Breite 65ch). Greife zum geteilten Kopfmuster nur bei einem echten kompositorischen Grund (z. B. wenn die rechte Spalte ein visuelles oder interaktives Element trägt, nicht bloß Fülltext).
* **Bento-Hintergrundvielfalt (verpflichtend).** Bento- und Feature-Raster-Abschnitte dürfen nicht aus 6 weiß-auf-weißen Karten mit Text bestehen. Mindestens 2-3 Zellen in jedem mehrzelligen Raster brauchen echte visuelle Abwechslung: ein echtes Bild, einen markengerechten Verlauf (nicht KI-Lila), ein Muster oder einen getönten Hintergrund. Ein cremefarbenes Bento auf Creme mit nur Typografie wirkt wie der langweilige KI-Standard, selbst wenn der Rest der Seite gut ist.
* **Der Mobil-Kollaps muss pro Abschnitt explizit sein.** Für jedes mehrspaltige Layout deklariere den `< 768px`-Fallback in derselben Komponente. Keine Annahmen à la „wird schon funktionieren, Tailwind regelt das“.

### 4.8 Bild- und visuelle Asset-Strategie

Landingpages und Portfolios sind **visuelle Produkte**. Reine Textseiten mit gefälschten Screenshot-Divs sind Slop.

**Prioritätsreihenfolge für visuelle Assets:**
1. **Bildgenerierungs-Tool zuerst.** Wenn IRGENDEIN Bildgenerierungs-Tool in der Umgebung verfügbar ist (`generate_image`, MCP-Bildtool, IDE-integrierte Generierung, OpenAI-Bildtools usw.), MUSST du es verwenden, um abschnittsspezifische Assets zu erstellen: Hero-Fotografie, Produktaufnahmen, Texturhintergründe, Stimmungsbilder. Generiere im passenden Seitenverhältnis für den jeweiligen Abschnitt. Überspringe diesen Schritt nicht, nur weil handgeschriebenes CSS schneller erscheint.
2. **Echte Web-Bilder an zweiter Stelle.** Wenn kein Generierungstool verfügbar ist, verwende echte Fotoquellen. Akzeptable Standards:
   * `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` für Platzhalterfotografie (der Seed sollte den Abschnitt beschreiben, z. B. `marrow-cookware-kitchen`)
   * Tatsächliche Stock- oder Marken-URLs, wenn das Briefing sie bereitstellt
   * Freie Lizenzquellen (Unsplash über direkte URL, Pexels), sofern ausdrücklich erlaubt
3. **Letzter Ausweg: dem Nutzer Bescheid geben.** Wenn beides nicht möglich ist, fülle die Seite NICHT mit handgebauten SVG-Illustrationen oder div-basierten "gefälschten Screenshots". Lasse stattdessen klar gekennzeichnete Platzhalterfelder (`<!-- TODO: hero product photo, 1600x1200 -->`) und sage am Ende der Antwort: *"Diese Seite benötigt echte Bilder an folgenden Stellen: \[Liste der Platzierungen\]. Bitte generiere oder stelle sie bereit."*

**Auch minimalistische Websites brauchen echte Bilder.** Eine reine Textseite ist keine Minimalismus. Sie ist unvollständige Arbeit. Selbst eine redaktionelle Website im Linear-Stil braucht mindestens 2–3 echte Bilder (Hero, ein Produkt- oder Lifestyle-Motiv, ein unterstützendes Bild). Erzeuge S/W-minimalistische Fotografie, wenn das Briefing zurückhaltend ist; überspringe Bilder nicht vollständig, nur weil der Regler niedrig steht.

**Echte Firmenlogos für Social Proof.** Wenn das Briefing eine Logo-Wand mit "Vertraut von / Genutzt von / Kunden" vorsieht, verwende NICHT standardmäßig schlichte Textmarken (`<span>Acme Co</span>`, nebeneinander gestaltet). Verwende echte SVG-Logos:
* **Quelle: Simple Icons** (`https://cdn.simpleicons.org/{slug}/ffffff` für beliebige Farben oder `simple-icons` npm-Paket). Deckt die meisten bekannten Marken ab.
* **Alternative: devicon** für Tech-Stack-Logos (`@svgr/cli` oder CDN).
* **Erfindest du den Markennamen? Dann erfinde auch eine SVG-Marke.** Erzeuge ein einfaches Monogramm (ein Buchstabe in einem Kreis, eine Zwei-Buchstaben-Ligatur, ein abstraktes Glyph), das als Inline-`<svg>` passend zum Seitenstil gerendert wird. Reine Textmarken für erfundene Markennamen wirken generisch.
* **Immer** sicherstellen, dass Logos im hellen und im dunklen Modus gut aussehen (weiß auf dunkel, schwarz auf hell oder eine einfarbige Theme-Variable).
* **NUR-LOGO-Regel (verbindlich):** Die Logo-Wand besteht aus Logos und sonst nichts. Drucke KEINE Branchen- oder Kategoriebezeichnungen unter jedem Logo (kein `Vercel` + `hosting` darunter, kein `Stripe` + `payments`, kein `Cloudflare` + `infra`). Das Logo ist die Glaubwürdigkeit, das Label fügt nichts hinzu, was der Nutzer nicht ohnehin weiß. Optional: Markenname als Alt-Text für Screenreader, optional ein Link zur Website der Marke. Mehr nicht.

**Handgebaute Illustrationen:**
* SVG-Icons aus Bibliotheken: in Ordnung (siehe Abschnitt 3.C).
* Handgebaute dekorative SVGs (eigene Illustrationen, Logos, Marken): **dringend abgeraten**, niemals als Standard. Nur akzeptabel, wenn:
  - Das Briefing es ausdrücklich verlangt ("zeichne mir ein SVG-Logo")
  - Es sich um eine einzelne, einfache geometrische Marke handelt (ein Quadrat, ein Kreis, eine Wortmarke in Display-Schrift)
  - Du von der Qualität des Ergebnisses überzeugt bist

**Div-basierte gefälschte Screenshots sind verboten.** Eine "handgebaute Produktvorschau" aus `<div>`-Rechtecken, gefälschten Aufgabenlisten, gefälschten Dashboards oder gefälschten Terminal-Fenstern ist ein Verräter. Wenn du ein Produkt zeigen musst:
* Verwende eine echte Screenshot-URL, falls vorhanden
* Erzeuge einen über das Bildtool
* Verwende eine echte Komponentenvorschau (eine tatsächliche Miniversion der Oberfläche auf der Seite)
* Oder verzichte ganz auf die Vorschau und nutze redaktionelle Fotografie

**Der Hero braucht eine echte visuelle Darstellung.** Text plus Verlaufs-Blob ist kein Hero, sondern ein Platzhalter.

### 4.9 Inhaltsdichte

Landingpages leben vom **ersten Eindruck**, nicht vom vollständigen Lesen. Kürze schonungslos.

* **Standardinhalt pro Abschnitt:** kurze Überschrift (≤ 8 Wörter) + kurzer Unterabsatz (≤ 25 Wörter) + entweder ein visuelles Element ODER einen Call-to-Action. Alles darüber hinaus muss durch die Aufgabe des Abschnitts gerechtfertigt sein.
* **Keine Datenabschnitte.** Eine Publikationstabelle mit 20 Zeilen, eine Auszeichnungsliste mit 30 Zeilen oder eine riesige Preismatrix auf einer Marketingseite ist das falsche Layout. Stattdessen:
  - Die 3-5 wichtigsten Punkte + Link „Vollständige Liste anzeigen“
  - Marquee / Karussell für die Breite
  - Eine eigene Seite, wenn die Daten selbst das Produkt sind
* **Lange Listen brauchen eine andere UI-Komponente, keine längere Liste.** Die Standardwahl mit Aufzählungspunkten bzw. `divide-y`-Zeilen unter `<ul>` ist die bequeme Lösung. Bei mehr als 5 Einträgen besser eine dieser Varianten verwenden:
  - Zweispaltige Aufteilung mit gruppierten Einträgen
  - Kartenraster mit Bild + Bezeichnung pro Eintrag
  - Tabs / Akkordeon, wenn sich die Einträge kategorisieren lassen
  - Horizontale Scroll-Snap-Pillen
  - Karussell für breite Listen (Testimonials, Logos, Fähigkeiten)
  - Marquee für „viele Dinge, die keine einzelne Aufmerksamkeit brauchen“
  Eine Spezifikationstabelle mit 10 Zeilen und einer Trennlinie unter jeder Zeile ist die SCHLECHTESTE Standardwahl. Entweder die Zeilen in 2-3 Gruppen mit dezenten Trennern aufteilen oder zu einem Karten-pro-Spezifikation-Layout wechseln.
* **Spezifikationstabellen speziell (das Marrow-Kochgeschirr-Muster).** Eine lange Produktspezifikationstabelle mit `border-b` in jeder Zeile ist der KI-Standard bei Briefings zu Kochgeschirr, Hardware, Bekleidung oder handwerklichen Waren. Verboten. Konkrete Alternativen:
  - **2-spaltiges Kartenraster:** Jede Spezifikation erhält eine eigene Karte mit dem Namen der Spezifikation, dem Wert (große Anzeigezahl) und einem einzeiligen Text „Warum es wichtig ist“. Karten auf dem Desktop zweispaltig, auf dem Mobilgerät einspaltig angeordnet.
  - **Horizontale Scroll-Snap-Pillen:** Jede Spezifikation ist eine Pille, die Nutzer durchwischen können.
  - **Gruppierte Blöcke:** 10 Spezifikationen in 3 logische Cluster gliedern (z. B. „Materialien“, „Kochen“, „Garantie“), jeder Cluster erhält EINEN dezenten Trenner und eine Cluster-Überschrift.
  - **Hervorgehoben vs. Rest:** 3-4 zentrale Spezifikationen als große Anzeige-Kacheln darstellen, der Rest unter einer Offenlegung „Vollständige Spezifikationen anzeigen“ eingeklappt.

* **TEXT-SELBSTPRÜFUNG (vor Auslieferung verpflichtend):** Bevor eine Aufgabe als erledigt gilt, jede sichtbare Zeichenkette der Seite erneut lesen (Überschriften, Unterüberschriften, Eyebrows, Button-Beschriftungen, Fließtext, Bildunterschriften, Alt-Texte, Fußzeilentext, Fehlermeldungen). Jede Zeichenkette markieren, die:
  - **grammatikalisch fehlerhaft ist** („kostenlos auf seiner Vergangenheit“, „zwei Pläne, aber einer ist ehrlich“, „es auf den Tisch bringen“ ohne Kontext)
  - **unklare Bezüge hat** („wir planen, dabei zu bleiben“ ohne vorherigen Kontext)
  - **nach KI-Halluzination klingt** (clevere, aber falsche Wortspiele, erzwungene Metaphern, die nicht tragen, Phrasen wie „elegantes Nichts“)
  - **wie ein LLM klingt, der nachdenklich wirken will** (passiv-aggressive Demut, vorgetäuschte Handwerksbezeichnungen, pseudopoetische Meta-Kommentare)
  Jede markierte Zeichenkette neu formulieren. Wenn unklar ist, ob eine Zeichenkette Sinn ergibt, durch einen schlichten, funktionalen Satz ersetzen. KI-generierter, cleverer Text ist schlechter als langweiliger Text.
* **Pseudo-präzise Zahlen werden beanstandet.** Zahlen wie `92%`, `4.1×`, `48k`, `5.8 mm` oder `13.4 lb` sind entweder:
  - aus echten Daten (Briefing, Markenrichtlinien, öffentliche Kennzahlen) - in Ordnung
  - ausdrücklich als Mock gekennzeichnet (`<!-- mock -->`, „Beispiel“, „Musterdaten“) - in Ordnung
  - von der KI erfundene Spezifikationsästhetik - verboten. Keine technische Präzision vortäuschen, die die Marke nicht beansprucht.
* **Ein Textregister pro Seite.** Technisches Mono („47 Aufgaben · 0,6 Kontextwechsel/Tag“), redaktionelle Prosa und werblichen Schlagabtausch nicht in derselben Komposition mischen, es sei denn, die Markenstimme verlangt es ausdrücklich.

### 4.10 Zitate & Testimonials

* **Maximal 3 Zeilen** Zitattext. Niemals 6. Ist das Originalzitat länger, kürzen. Ein Zitat auf einer Landingpage ist ein Auszug, keine vollständige Bewertung.
* Bei sehr kleinen Schriftgrößen (z. B. Testimonials in der Fußzeile) darf die Zeilenbegrenzung leicht gedehnt werden. Leitgedanke: „auf einen Blick erfassbar“.
* **Keine Gedankenstriche im Zitattext** als gestalterisches Element (lange Pausen, kinetische Gedankenstriche, Gedankenstrich-Aufzählungen). Siehe Abschnitt 9.G - der Gedankenstrich ist vollständig verboten.
* Zuschreibung: Name + Rolle + (optional) Unternehmen. Niemals nur der Name (z. B. „- Sarah“).
* Anführungszeichen: echte typografische Anführungszeichen („ “) oder gar keine. Nicht gerade ASCII-Anführungszeichen (" ).

### 4.11 Seitendesign-Sperre (Hell-/Dunkelmodus-Konsistenz)

Die Seite hat EIN Design. Abschnitte kehren sich nicht um.

* Ist die Seite im Dunkelmodus, sind ALLE Abschnitte im Dunkelmodus. Kein hell gehaltener, warm-papierfarbener Abschnitt zwischen dunklen Abschnitten (oder umgekehrt). Der Nutzer darf sich beim Scrollen nicht auf einer anderen Website fühlen.
* Ausnahme: Verlangt das Briefing ausdrücklich ein Gestaltungsmittel „Farbblock-Erzählung“ oder „Designwechsel beim Scrollen“ UND ist dies eine bewusste Komposition (ein einziger vollständiger Designwechsel mit starkem Übergang, nicht zufälliger Wechsel), ist dies einmal pro Seite erlaubt.
* Standardverhalten: Auf Seitenebene Hell, Dunkel oder Automatisch (`prefers-color-scheme`) wählen und sperren. Abschnittsspezifische Hintergrundtöne innerhalb derselben Designfamilie sind in Ordnung (`bg-zinc-950` neben `bg-zinc-900`); auf `bg-amber-50` mitten in einer `bg-zinc-950`-Seite umzuschalten ist fehlerhaft.
* Bei Verwendung eines Designsystems mit eingebautem Theming (Radix Themes, shadcn/ui mit `<Theme>`) das Theme EINMAL in `layout.tsx` oder im Seitenwurzelelement setzen. Einzelne Abschnitte dürfen es nicht überschreiben.

---

## 5. KONTEXTBEZOGENE PROAKTIVITÄT

Dies sind Werkzeuge, keine Standardeinstellungen. Verwenden, wenn die Designanalyse es verlangt. **Keines davon wird automatisch ausgelöst.**

* **Liquid Glass / Glassmorphism:** Geeignet für hochwertige Konsumentenprodukte, Apple-nahe Ästhetik, Luxusmarken oder Medien-Overlay-Stimmungen. Ungeeignet für Dashboards, den öffentlichen Sektor oder „langweiliges B2B“. Wenn verwendet, gehe über `backdrop-blur` hinaus: Füge eine 1px-Innenrahmen (`border-white/10`) und einen subtilen inneren Schatten (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) für physische Kantenbrechung hinzu. Stelle einen Fallback mit Vollfarbe unter `prefers-reduced-transparency` bereit.
* **Magnetische Mikrophysik:** Verwende sie, wenn `MOTION_INTENSITY > 5` UND das Briefing auf premium / verspielt / Agentur hindeutet. Implementiere sie AUSSCHLIESSLICH mit `useMotionValue` / `useTransform` von Motion außerhalb des React-Render-Zyklus. Niemals `useState`. Siehe Abschnitt 3.B.
* **Dauerhafte Mikrointeraktionen** (Pulse, Typewriter, Float, Shimmer, Carousel): Verwende sie, wenn `MOTION_INTENSITY > 5` UND der Abschnitt tatsächlich von Bewegung profitiert (Statusanzeigen, Live-Feeds, KI-Anmutung). **Nicht jede Karte braucht eine Endlosschleife.** Ist ein Abschnitt informativ, bleibt er statisch. Wende Spring Physics (`type: "spring", stiffness: 100, damping: 20`) an – keine linearen Easings.
* **„Bewegung behauptet, Bewegung gezeigt.“** Wenn `MOTION_INTENSITY > 4`, muss sich die Seite tatsächlich bewegen: Einblendübergänge am Hero, Scroll-Reveal bei zentralen Abschnitten, Hover-Physik bei CTAs, mindestens. Eine statische Seite, die `MOTION_INTENSITY: 7` beansprucht, ist fehlerhaft. Wenn du im verfügbaren Rahmen keine funktionierende Bewegung liefern kannst, reduziere den Regler auf 3 und liefere eine saubere statische Seite. Baue Bewegung niemals halb, wenn sie kaputtgeht (abgeschnittene ScrollTriggers, ruckartige Einblendungen, fehlende Cleanups).
* **BEWEGUNG MUSS BEGRÜNDET SEIN (verpflichtend).** Bevor du eine Animation hinzufügst, frage: „Was kommuniziert diese Animation?“ Gültige Antworten: Hierarchie (Aufmerksamkeit auf das Richtige lenken), Storytelling (Inhalte in einer narrativ passenden Reihenfolge enthüllen), Feedback (eine Nutzeraktion bestätigen), Zustandsübergang (zeigen, dass sich etwas geändert hat). Ungültige Antwort: „sah cool aus“. GSAP überall einzusetzen, nur weil GSAP verfügbar ist, ist amateurhaft. Jeder ScrollTrigger, jedes Marquee, jeder angepinnte Abschnitt braucht einen Grund. Kannst du den Grund nicht in einem Satz formulieren, streiche die Animation.
* **MARQUEE: MAXIMAL EINS PRO SEITE (verpflichtend).** Horizontal scrollende Textlaufbänder („Logos, die endlos laufen“, „Manifest, das seitwärts scrollt“, „kinetischer Wortstreifen“) sind höchstens EINMAL pro Seite angemessen. Zwei oder mehr Laufbänder auf derselben Seite wirken wie lustloser Füllstoff. Wähle den einen Abschnitt, in dem das Laufband dem Inhalt wirklich dient; die anderen erhalten ein anderes Layout.
* **GSAP-Sticky-Stack-Muster (wenn Scroll-Stack verwendet wird).** Ein „Kartenstapel beim Scrollen“ muss ein ECHTER Sticky-Stack sein, keine sequenzielle Reveal-Liste. Siehe das kanonische Code-Gerüst in Abschnitt 5.A unten. Häufiger Fehler: Der Trigger feuert auf halber Strecke des Scrollens statt am oberen Viewport-Rand zu pinnen. Lösung: `start: "top top"`, nicht `start: "top center"` oder `"top 80%"`.
* **GSAP-Horizontal-Pan-Muster (wenn horizontales Scroll-Hijacking verwendet wird).** Siehe das kanonische Gerüst in Abschnitt 5.B unten. Häufiger Fehler: Die Animation startet, bevor der Abschnitt angepinnt ist, sodass der Nutzer eine halbe Folie sieht. Gleiche Lösung: `start: "top top"`, den Wrapper pinnen und den inneren Track scrubben.

### 5.A Sticky-Stack – Kanonisches Gerüst

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

Kritische Punkte: `start: "top top"`, `pin: true`, jede Karte außer der letzten wird angepinnt, und die Skalierungs-/Deckkraft-Transformation wird durch den ScrollTrigger der NÄCHSTEN Karte gesteuert (sodass die vorherige Karte schrumpft, sobald die nächste erscheint).

### 5.B Horizontal-Pan – Kanonisches Gerüst

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

Kritische Punkte: `start: "top top"`, `pin: true`, `end: "+=${distance}"` (Scroll-Länge = benötigte horizontale Strecke), `scrub: 1`. Der Wrapper wird angepinnt, der innere Track gleitet horizontal, während der Nutzer vertikal scrollt.

### 5.C Scroll-Reveal-Stagger – Kanonisches Gerüst (leichtere Alternative)

Für einfache „Elemente erscheinen, sobald sie den Viewport betreten“ (ohne Pinning) bevorzuge Motions `whileInView` gegenüber GSAP – leichter, kein ScrollTrigger nötig:

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

Verwende dies für: Feature-Listen, Testimonial-Raster, Logo-Wände, alles, was nur „beim Scrollen einblenden“ braucht. Spare GSAP für echte Pin- und Scrub-Arbeit auf.

### 5.D Verbotene Animationsmuster

* **`window.addEventListener("scroll", ...)`** ist verboten. Es läuft bei jedem Scroll-Frame, ist ruckanfällig und nicht gebündelt. Verwende stattdessen Motions `useScroll()`, GSAPs `ScrollTrigger`, IntersectionObserver oder CSS `scroll-driven animations` (`animation-timeline: view()`).
* **Eigene Scroll-Fortschrittsberechnungen mit `window.scrollY`** im React-State. Aus demselben Grund. Sie rendern bei jedem Frame neu.
* **`requestAnimationFrame`-Schleifen, die den React-State berühren.** Verwende stattdessen Motion Values (`useMotionValue` + `useTransform`).
* **Layout-Übergänge:** Verwende Motions `layout`- und `layoutId`-Props für sichtbare Zustandsänderungen (Neuordnen von Listen, Aufklappen von Modals, geteilte Elemente zwischen Routen). Umschließe statischen Inhalt nicht „zur Sicherheit“ mit `layout`-Props – das kostet Messaufwand.
* **Gestaffelte Orchestrierung:** Verwende `staggerChildren` (Motion) oder die CSS-Kaskade (`animation-delay: calc(var(--index) * 100ms)`) für Reveal-Momente, in denen die Reihenfolge zählt. Für `staggerChildren` müssen Eltern (`variants`) und Kinder im selben Client-Component-Baum liegen.

---

## 6. LEISTUNGS- & BARRIEREFREIHEITSLEITPLANKEN

### 6.A Hardwarebeschleunigung
* Animiere NUR `transform` und `opacity`. Animiere niemals `top`, `left`, `width`, `height`.
* Verwende `will-change: transform` sparsam – nur bei Elementen, die tatsächlich animiert werden.

### 6.B Reduzierte Bewegung (verpflichtend)
* **Jede Bewegung oberhalb von `MOTION_INTENSITY > 3` MUSS `prefers-reduced-motion` respektieren.** Dies ist nicht verhandelbar.
* In Motion: mit `useReducedMotion()` umschließen und auf statisch zurückfallen.
* In CSS: Animationen hinter `@media (prefers-reduced-motion: no-preference)` schalten oder einen Override-Block unter `@media (prefers-reduced-motion: reduce)` bereitstellen, der sie deaktiviert.
* Endlosschleifen, Parallax, Scroll-Hijacking und magnetische Physik MÜSSEN bei reduzierter Bewegung auf statisch/sofort reduziert werden.

### 6.C Dunkelmodus (verpflichtend für jede verbraucherorientierte Seite)
* **Von Beginn an für beide Modi gestalten.** Niemals nur hell oder nur dunkel ausliefern, außer auf ausdrückliche Anweisung des Nutzers.
* Für Design-Tokens entweder die Tailwind-`dark:`-Variante ODER CSS-Variablen verwenden. Pro Projekt eine Strategie wählen.
* **Hier keine konkreten Farben für den Dunkelmodus vorschreiben.** Das Briefing entscheidet. Visuelle Hierarchie, Markenidentität und WCAG-AA-Kontrast (AAA für Fließtext) in beiden Modi beibehalten.
* `prefers-color-scheme: dark` respektieren. Standardmäßig die Systemeinstellung übernehmen, es sei denn, die Marke besteht auf einem Modus.

### 6.D Core-Web-Vitals-Ziele
* **LCP** < 2,5 s. Das Hero-Bild muss `next/image priority` sein oder vorab geladen werden.
* **INP** < 200 ms. Aufwendige Arbeit vom Haupt-Thread auslagern.
* **CLS** < 0,1. Platz für Bilder, Schriften und Einbettungen reservieren.
* Vor der Fertigstellung einer Seite Lighthouse ausführen.

### 6.E DOM-Kosten
* Korn- bzw. Rauschfilter AUSSCHLIESSLICH auf feste, `pointer-events-none`-Pseudoelemente anwenden (z. B. `fixed inset-0 z-[60] pointer-events-none`). NIEMALS auf scrollbaren Containern – ständige GPU-Neuzeichnungen zerstören die FPS auf Mobilgeräten.
* Die Bundle-Größe im Blick behalten. Bewegungsbibliotheken sind nicht klein. Three.js ist groß. Alles, was nicht oberhalb des Falzes liegt, lazy laden.

### 6.F Z-Index-Zurückhaltung
NIEMALS willkürlich `z-50` oder `z-10` verteilen. Z-Index ausschließlich für systemische Ebenenkontexte verwenden (fixierte Navigationsleisten, Modale Dialoge, Overlays, Korn-Effekt). Die Z-Index-Skala in einer Projekt-Konstantendatei dokumentieren.

---

## 7. DIAL-DEFINITIONEN (Technische Referenz)

### DESIGN_VARIANCE (Stufe 1–10)
* **1–3 (Vorhersagbar):** Symmetrisches CSS-Grid (12 Spalten, gleiche fr-Einheiten), gleichmäßige Abstände, zentrierte Ausrichtung.
* **4–7 (Versetzt):** `margin-top: -2rem`-Überlappungen, variierende Bildseitenverhältnisse (4:3 neben 16:9), linksbündige Überschriften über zentrierten Daten.
* **8–10 (Asymmetrisch):** Masonry-Layouts, CSS-Grid mit Bruchteileinheiten (`grid-template-columns: 2fr 1fr 1fr`), großzügige Leerflächen (`padding-left: 20vw`).
* **MOBILE-ÜBERSCHREIBUNG:** Für Stufen 4–10 müssen asymmetrische Layouts oberhalb von `md:` auf eine strikte einspaltige Anordnung (`w-full`, `px-4`, `py-8`) bei Viewports `< 768px` zusammenfallen.

### MOTION_INTENSITY (Stufe 1–10)
* **1–3 (Statisch):** Keine automatischen Animationen. Nur CSS-`:hover`- und `:active`-Zustände. `prefers-reduced-motion` ist ohnehin der Standardmodus.
* **4–7 (Fließendes CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay`-Kaskaden für Einblendungen beim Laden. Fokus auf `transform` und `opacity`.
* **8–10 (Fortgeschrittene Choreografie):** Komplexe scrollgesteuerte Einblendungen, Parallax, scrollgesteuerte Animation (CSS `animation-timeline` oder GSAP ScrollTrigger). Motion-Hooks verwenden. **NIEMALS `window.addEventListener('scroll')` verwenden** – das ist ein hartes Verbot, kein „besser vermeiden“. Siehe Abschnitt 5.D für die erlaubten Alternativen.

### VISUAL_DENSITY (Stufe 1–10)
* **1–3 (Kunstgalerie):** Viel Weißraum. Große Abschnittsabstände (`py-32` bis `py-48`). Teuer, sauber.
* **4–7 (Alltags-App):** Standardabstände für Webanwendungen (`py-16` bis `py-24`).
* **8–10 (Cockpit):** Enge Innenabstände. Keine Kartenrahmen; 1-px-Linien trennen Daten. Verpflichtend: `font-mono` für alle Zahlen.

---

## 8. DUNKELMODUS-PROTOKOLL

Standardmäßig Doppelmodus. Niemals von reinem Hellmodus ausgehen, außer das Briefing ist eine print-nachempfindende redaktionelle Gestaltung.

### 8.A Token-Strategie (eine wählen und beibehalten)
* **Tailwind-`dark:`-Variante** (Standard für Utility-First-Projekte): Jedes Farb-Utility wird mit seiner Dunkelmodus-Variante gepaart (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
* **CSS-Variablen** (für shadcn/ui, Radix Themes oder Komponentenbibliotheken mit Theming): Semantische Tokens definieren (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) und deren Werte unter `[data-theme="dark"]` oder `@media (prefers-color-scheme: dark)` austauschen.

### 8.B Keine konkreten Farben hier vorschreiben
Das Briefing und die Marke entscheiden. Diese Skill erzwingt nur:
* **Kontrast** – WCAG-AA-Minimum für Fließtext, AAA-Ziel für Hero-Texte.
* **Hierarchie-Parität** – Visuelle Hierarchie, die im Hellmodus funktioniert, muss auch im Dunkelmodus funktionieren. Wenn ein CTA im Hellmodus hervorsticht, sticht er auch im Dunkelmodus hervor.
* **Markentreue** – Die primäre Markenfarbe bleibt erkennbar. Die Marke nicht im Dunkelmodus entsättigen.
* **Kein reines `#000000` und kein reines `#ffffff`** – stattdessen Off-Black (zinc-950, nahezu schwarzes warmes Grau) und Off-White verwenden. Reine Werte zerstören die Tiefe.

### 8.C Standardmodus
`prefers-color-scheme` respektieren, sofern die Marke nicht auf einem Modus besteht. Einen manuellen Umschalter hinzufügen, wenn einer der beiden Modi zentrale Markenaussagen verlieren würde.

### 8.D In beiden Modi testen, bevor fertiggestellt wird
Die Seite während der Entwicklung in beiden Modi öffnen. Keine Seite ausliefern, die nur in einem Modus gesehen wurde.

---

## 9. KI-MERKMALE (Verbotene Muster)

Diese Signaturen vermeiden, sofern das Briefing sie nicht ausdrücklich verlangt.

### 9.A Visuell & CSS
* **KEINE Neonfarben / Außenglühen** standardmäßig. Innenrahmen oder dezent getönte Schatten verwenden.
* **KEIN reines Schwarz (`#000000`).** Off-Black, zinc-950 oder Anthrazit.
* **KEINE übersättigten Akzente.** Entsättigen, damit sie sich in die neutralen Töne einfügen.
* **KEIN übermäßiger Verlaufstext** für große Überschriften.
* **KEINE benutzerdefinierten Mauszeiger.** Veraltet, barrierefeindlich, leistungsschädlich.

### 9.B Typografie
* **Inter NICHT als Standard verwenden.** Siehe Abschnitt 4.1. Es gibt einen Ausnahmeweg.
* **KEINE übergroßen H1-Überschriften**, die nur schreien. Hierarchie über Gewicht und Farbe steuern, nicht über rohe Größe.
* **Serifen-Einschränkungen:** Serifen für redaktionelle / luxuriöse / publizistische Inhalte. Nicht für Dashboards.

### 9.C Layout & Abstände
* **Mathematisch perfekte** Innen- und Außenabstände. Keine schwebenden Elemente mit unbeholfenen Lücken.
* **KEINE drei gleichen Feature-Karten nebeneinander.** Die generische Reihe aus „drei identischen Karten horizontal“ ist verboten. Stattdessen zweispaltiges Zickzack-Layout, asymmetrisches Raster, scroll-fixiert oder horizontale Scroll-Alternative verwenden.

### 9.D Inhalt & Daten (Der "Jane Doe"-Effekt)
* **KEINE generischen Namen.** "John Doe", "Sarah Chan", "Jack Su" → verwende kreative, realistische, lokal passende Namen.
* **KEINE generischen Avatare.** Kein SVG-"Ei" und keine Lucide-Benutzersymbole → verwende glaubwürdige Fotoplatzhalter oder spezifische Gestaltung.
* **KEINE makellos wirkenden Zahlen.** Vermeide `99.99%`, `50%`, `1234567`. Verwende organische, unordentliche Daten (`47.2%`, `+1 (312) 847-1928`).
* **KEINE Startup-Slop-Markennamen.** "Acme", "Nexus", "SmartFlow", "Cloudly" → erfinde kontextbezogene, hochwertige Namen, die echt klingen.
* **KEINE Füllverben.** "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize" → verwende konkrete Verben.

### 9.E Externe Ressourcen & Komponenten
* **KEINE handgebauten SVG-Symbole.** Verwende Phosphor / HugeIcons / Radix / Tabler. Lucide nur auf ausdrückliche Anfrage.
* **Handgebaute dekorative SVGs sind als Standard stark abzulehnen** (siehe Abschnitt 4.8).
* **KEINE div-basierten gefälschten Screenshots.** Baue niemals eine falsche Produkt-Oberfläche aus `<div>`-Rechtecken, um einen Screenshot zu simulieren. Verwende echte Bilder, generierte Bilder oder verzichte auf die Vorschau.
* **KEINE defekten Unsplash-Links.** Verwende `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`, generierte Fotoplatzhalter oder echte Assets.
* **shadcn/ui-Anpassung:** Erlaubt, aber NIEMALS im Standardzustand. Passe Radien, Farben, Schatten und Typografie an die Ästhetik des Projekts an.
* **Produktionsreife Sauberkeit:** Der Code soll visuell sauber, einprägsam und sorgfältig verfeinert sein.

### 9.F Produktionstest-Erkennungsmerkmale (generell verboten)

Diese Muster stammen aus realen Tests von LLM-generierten Landingpages. Sie sind die Signaturen, auf die das Modell zurückgreift, wenn es versucht, "designt" auszusehen. Behandle sie als harte Verbote, sofern das Briefing nicht ausdrücklich eines davon verlangt.

**Hero & oberer Seitenbereich**
* **KEINE Versionsbezeichnungen im Hero.** `V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA` - als Standard-Eyebrows verboten. Nur akzeptabel, wenn das Briefing ausdrücklich einen Produktlaunch bzw. einen Vorschau-Status betrifft.
* **KEINE Untertitel-Eyebrows im Stil von "Marke · Nr. 01".** Mikro-Metazeilen wie "Marrow · No. 01 · The 6-quart". Weglassen.

**Abschnittsnummerierung & Mikro-Labels**
* **KEINE Abschnittsnummern-Eyebrows.** `00 / INDEX`, `001 · Capabilities`, `002 · Featured commission`, `06 · how it works`, `05 · The honest table` - verboten. Eyebrows sollen das Thema in einfacher Sprache benennen, nicht aufzählen.
* **KEINE `01 / 4`-artige Paginierung auf Bildern oder Bento-Kacheln.** Wenn der Nutzer zählen kann, braucht er das Label nicht.
* **KEINE `Scroll · 001 Capabilities`-artigen Scroll-Hinweise.** Ein einfacher Pfeil oder "Scroll" genügt; kein Abschnittsnummern-Präfix.
* **KEINE Bereichsbezeichnungen wie "Index of Work, 2018 - 2026"** als Eyebrows. Sag einfach, worum es im Abschnitt geht.

**Trenner & Punkte**
* **Der Mittelpunkt (`·`) ist rationiert.** Maximal 1 pro Zeile in Metadaten-Leisten. Verwende ihn NICHT als Standardtrenner für alles ("foo · bar · baz · qux · quux"). Wenn du eine Trennerfamilie brauchst, bevorzuge Zeilenumbrüche, Haarlinien oder Spalten.
* **KEINE dekorativen farbigen Statuspunkte bei jeder Liste, Navigation oder jedem Badge.** Ein farbiger Punkt vor "ONE Q4 SLOT OPEN" oder vor jedem Navigationslink oder jeder Aufgabenzeile - standardmäßig verboten. Nur akzeptabel, wenn der Punkt einen tatsächlichen semantischen Zustand vermittelt (ein Serverstatus, ein Verfügbarkeitsflag) und sparsam eingesetzt wird.

**Gedankenstriche & typografische Schnörkel**
* **KEIN Gedankenstrich (`—`) als Gestaltungselement ODER sonst irgendwo.** Siehe Abschnitt 9.G unten für das vollständige, nicht verhandelbare Verbot. Das Gedankenstrich-Zeichen ist in Überschriften, Eyebrows, Pills, Fließtext, Zitaten, Zuschreibungen, Bildunterschriften, Button-Text und Alt-Text verboten. Verwende den normalen Bindestrich (`-`).
* **KEINE `<br>`-artig gebrochenen und kursivierten Überschriften** als Standard-"Designtrick". Splits wie "für dreißig\<br\>*Jahre.*". Überschriften sollen zunächst natürlich lesbar sein und nur dann kreativ werden, wenn das Briefing es verlangt.
* **KEIN vertikal gedrehter Text** ("INDEX OF WORK, 2018 - 2026" um 90° gedreht). Ein Klischee von Agenturportfolios. Nur verwenden, wenn das Briefing ausdrücklich Agentur / Awwwards / experimentell ist UND es einen echten Kompositionszweck erfüllt.
* **KEINE Fadenkreuze / Haarlinien-Raster als Dekoration.** Vertikale und horizontale Linien, die nur gezogen werden, damit die Seite "designt" wirkt - verboten. Nur verwenden, wenn sie echte Inhalte strukturieren.

**Gefälschte Produktvorschauen**
* **KEINE div-basierte gefälschte Produkt-Oberfläche im Hero** (gefälschte Aufgabenliste, gefälschtes Terminal, gefälschtes Dashboard aus gestalteten Divs). Es ist das Erkennungsmerkmal Nr. 1 für LLM-Design. Verwende einen echten Screenshot, ein generiertes Bild, eine echte Komponentenvorschau oder gar keine.
* **KEINE gefälschten Versionsfußzeilen** ("v0.6.2-rc.1", "last sync 4s ago · main") innerhalb gefälschter Screenshots. Sie bringen nichts und schreien "KI".

**Marketing-Text-Erkennungsmerkmale**
* **KEINE "Still im Einsatz bei" / "Still vertrauen uns"-Überschriften** für Social Proof. Verwende natürliche Sprache: "Vertraut von", "Im Einsatz bei", "Kunden sind unter anderem", oder verzichte ganz auf die Überschrift, wenn die Logos für sich sprechen.
* **KEINE poetischen Labels im Stil von "Aus der Praxis" / "Feldnotizen" / "Gerade auf der Werkbank" / "Auf unseren Schreibtischen" / "Lose Platten"** bei Zitat-, Blog- oder Seitenleistenabschnitten. Wirkt performativ-handwerklich. Verwende schlichte funktionale Labels ("Referenzen", "Neueste Texte", "Woran wir gerade arbeiten") oder verzichte auf das Label.
* **KEINE scheinbar bescheidenen Verweise auf Branchenkollegen** wie "Wir respektieren die französischen" im Fließtext. Niedlich und KI-typisch.
* **KEINE Wetter- / Ortsleisten** ("LIS 14:23 · 18°C") in Kopf- oder Fußzeilen, sofern das Briefing nicht ausdrücklich von einem Ort oder einem über Zeitzonen verteilten Studio handelt.
* **KEINE Mikro-Metasätze unter Eyebrows.** Sätze wie *"Jede dieser Funktionen ist etwas, das wir heute ausliefern, kein Fahrplan-Versprechen. Die Liste bleibt bewusst kurz."* unter einer Abschnittsüberschrift sind unnötiger Ballast. Eyebrow + Überschrift + Fließtext genügt.
* **KEINE generischen Schrittbezeichnungen.** "Stage 1 / Stage 2 / Stage 3", "Step 1 / Step 2 / Step 3", "Phase 01 / Phase 02 / Phase 03", "Pass One / Pass Two / Pass Three". Verboten. Der eigentliche Schrittinhalt ist das Label. Wenn du einen Fortschritt zeigen musst, verwende das Verb-Substantiv direkt ("Installieren", "Konfigurieren", "Ausliefern") statt "Stage 1: Installieren".

**Pills, Labels und Versionsangaben**
* **KEINE Pills/Labels/Tags über Bildern.** Keine `<span>`-Overlays auf Fotos mit Tags wie `Brand · 02`, `PLATE · BRAND`, `Field notes - journal`. Entweder lässt man das Bild für sich selbst sprechen oder fügt direkt unterhalb (außerhalb des Bildes) eine Bildunterschrift hinzu.
* **KEINE Fotonachweise als Dekoration.** Zeichenketten wie `Field study no. 12 · Ines Caetano`, `Plate 03 · House archive`, `Frame XII · 35mm` unter Stock- oder Picsum-Bildern wirken prätentiös. Ein Fotonachweis ist NUR erlaubt, wenn ein echter Fotograf für ein echtes Foto (mit Erlaubnis) genannt wird. Andernfalls: Bildunterschrift weglassen oder eine einzeilige sachliche Bildunterschrift verwenden („Der 6-Quart-Topf in Salbeigrün.").
* **KEINE Versionsfußzeilen auf Marketing-Seiten.** Fußzeilen-Zeichenketten wie `v1.4.2`, `Build 0048`, `last sync 4s ago · main` sind CLI-/Devtool-Fixtures, kein Landingpage-Inhalt. Auf Marketing-, Landing- und Portfolio-Seiten verboten.
* **KEINE Live-Lagerzähler im Stil von „Reservierung 412 von 800"** als Dekoration. Nur wenn das Briefing explizit eine limitierte Warteliste mit echten Daten beschreibt.

**Dekorative Textstreifen**
* **KEIN dekorativer Textstreifen am unteren Herorand.** Muster wie `BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION`, `DESIGN · BUILD · SHIP`, `ESTD. 2018 · LISBON · BRAND. MOTION. SPATIAL.` als kleiner Mono-Caps-Streifen über die Unterkante des Heros sind ein Klischee von Agentur-Portfolios. Standardmäßig verboten. Nur akzeptabel, wenn der Streifen echte, navigierbare Links (fixierte untere Navigation) oder echte Statusinformationen enthält (Cookie-Banner, Build-Info auf einer Dokumentationsseite).
* **KEIN schwebender Untertext oben rechts in Abschnittsüberschriften.** Muster: Der Abschnitt hat eine große, linksbündige Überschrift; in der oberen rechten Ecke desselben Abschnittskopfs schwebt ein kleiner Erklärungsabsatz ohne erkennbare Ausrichtung zu irgendetwas anderem. Dieser Schwebeabsatz ist das Erkennungsmerkmal. Entweder den Untertext direkt unter die Überschrift setzen oder einen sauberen zweispaltigen Kopf bauen (links: Überschrift, rechts: ausgerichteter Fließtext), aber keinen winzigen Eckabsatz.

**Listen, Trenner und Bewertung**
* **KEIN `border-t` + `border-b` bei jeder Zeile einer langen Liste oder Spezifikationstabelle.** Eines wählen (Unterkante zwischen Zeilen ODER Oberkante über der Gruppe) und sparsam einsetzen. Eine 10-zeilige Spezifikationstabelle mit Haarlinien unter jeder Zeile ist das bequemste Layout – siehe Abschnitt 4.9 für alternative UI-Komponenten.
* **KEINE Bewertungs- oder Fortschrittsbalken mit gefüllten Hintergrundspuren** als Vergleichsvisualisierung. Wenn „X von Y"-Vergleiche gezeigt werden sollen, eine Zahl mit kleinem Icon bevorzugen oder einen winzigen Inline-Balken OHNE Hintergrundspur verwenden. Große, gefüllte `bg-zinc-200`-Spuren mit teilweiser Füllung darüber sind Dashboard-UI-Überladung auf einer Landingpage.

**Lokalisierung, Zeit, Scroll-Hinweise**
* **Lokalitäts-, Stadtnamen-, Uhrzeit- und Wetterstreifen sind für 99 % der Briefings verboten.** „Lisbon, working with founders" im Hero, „1200-690 Lisbon, Portugal" im Footer, „Lisbon 14:23 · 18°C" in der Navigation. Dies sind Dekorationsmerkmale von Agentur-Portfolios. Erlaubt NUR wenn: das Briefing explizit ein global verteiltes Studio mit zeitzonenrelevanter Arbeit beschreibt, ODER eine reisefokussierte Marke, ODER einen realen physischen Veranstaltungsort. Eine einzelne Kontaktadresse im Footer ist in Ordnung; ein atmosphärischer Lokalitätsstreifen nicht.
* **Scroll-Hinweise sind verboten.** `Scroll`, `↓ scroll`, `Scroll to explore`, `Scroll to walk through it`, animierte Mausrad-Icons. Hat der Nutzer noch nicht gescrollt, sieht er den Hero. Er weiß, was Scrollen ist. Der untere Rand des Viewports braucht kein Label.
* **STANDARDMÄSSIG NULL dekorative Statuspunkte.** Ein farbiger Punkt vor Navigationspunkten, Listenzeilen, Badges oder Statusbezeichnungen ist ein Erkennungsmerkmal. Nur akzeptabel, wenn er einen echten semantischen Zustand vermittelt (eine Live-Anzeige für den tatsächlichen Serverstatus, ein Live-Verfügbarkeitsflag) und auf einen Punkt pro Seitenabschnitt begrenzt ist.

### 9.G GEDANKENSTRICH-VERBOT (das am häufigsten verletzte Erkennungsmerkmal)

**Der Gedankenstrich (`—`) ist VOLLSTÄNDIG verboten.** Er ist die stilistische Krücke des LLM schlechthin und das visuelle Erkennungsmerkmal Nr. 1 in Produktionstests. Es gibt keine Ausnahme für „begrenzte Verwendung", keine Ausnahme für „natürliche Häufigkeit", keine Ausnahme für „im Fließtext in Ordnung". Keine.

* **Verboten in Überschriften.** Stattdessen einen Punkt oder ein Komma verwenden.
* **Verboten in Eyebrows / Labels / Pills / Button-Text / Bildunterschriften / Navigationspunkten.** Durch Zeilenumbrüche, Spalten oder Haarlinien ersetzen.
* **Verboten im Fließtext.** Den Satz umstrukturieren: zwei Sätze mit Punkt, ODER ein Komma, ODER Klammern, ODER ein Doppelpunkt.
* **Verboten bei Zitatangaben.** Einen normalen Bindestrich mit Leerzeichen (` - `) oder einen Zeilenumbruch + Namen in geringerer Schriftstärke verwenden.
* **Verboten auch in Form des Halbgeviertstrichs (`–`), wenn er als Trennzeichen verwendet wird.** Datumsbereiche (`2018-2026`) verwenden einen Bindestrich. Zahlenbereiche (`€40-80k`) verwenden einen Bindestrich.

Die EINZIGEN erlaubten Strichzeichen auf der Seite sind:
* Normaler Bindestrich `-` (für zusammengesetzte Wörter, Bereiche, Trennlinien im Markup)
* Minuszeichen in der Mathematik (`-5°C`)

Wenn Ihre Ausgabe auch nur einen einzigen `—` oder `–` enthält, der für den Nutzer sichtbar ist, scheitert die Ausgabe an der Pre-Flight-Prüfung und muss neu geschrieben werden.

Diese Regel ist nicht verhandelbar. Der Agent hat Gedankenstrich-Grenzen in der Vergangenheit ignoriert, wenn sie als „sparsam verwenden" formuliert waren. Die Formulierung hier ist binär: null Gedankenstriche.

---

## 10. REFERENZVOKABULAR (Mustername, die der Agent kennen sollte)

Dies ist ein Vokabular, keine Bibliothek. Der Agent sollte diese Mustername KENNEN, um über sie zu kommunizieren, sie beim Entwurf zu berücksichtigen und sie zu verwenden, wenn der Designansatz es verlangt. **Implementierungen und Code-Skizzen befinden sich im Block-Katalog (Abschnitt 12), der iterativ gepflegt wird.**

### Hero-Paradigmen
* **Asymmetrischer Split-Hero** – Text auf einer Seite, Asset auf der anderen, großzügiger Weißraum.
* **Editorialer Manifest-Hero** – Große Typografie, kein Asset, fast wie ein Poster.
* **Video-/Medienmasken-Hero** – Typografie als Maske über einem Videohintergrund ausgeschnitten.
* **Kinetik-Typografie-Hero** – Animierte Typografie als primäres visuelles Element.
* **Vorhang-Enthüllungs-Hero** – Heroteile fahren beim Scrollen wie ein Vorhang auf.
* **Scroll-fixierter Hero** – Der Hero bleibt fixiert, während der Inhalt darunter scrollt.

### Navigation & Menüs
* **Mac OS Dock-Vergrößerung** - Randnavigation, Symbole skalieren fließend beim Überfahren.
* **Magnetischer Button** - Wird zum Cursor hingezogen.
* **Gooey-Menü** - Untermenüpunkte lösen sich wie zähflüssige Flüssigkeit.
* **Dynamic Island** - Sich verformende Pille für Status / Benachrichtigungen.
* **Kontextuelles Radialmenü** - Kreisförmiges Menü, das sich am Klickpunkt öffnet.
* **Schwebende Speed-Dial** - FAB, das in gebogene Sekundäraktionen aufspringt.
* **Mega-Menü-Einblendung** - Vollbild-Dropdown, Inhalte blenden gestaffelt ein.

### Layout & Raster
* **Bento-Raster** - Asymmetrische Kachelgruppierung (Apple Control Center).
* **Masonry-Layout** - Versetztes Raster ohne feste Zeilenhöhe.
* **Chroma-Raster** - Rahmen / Kacheln mit dezent animierten Verläufen.
* **Geteilter Scroll** - Zwei Hälften, die in entgegengesetzte Richtungen gleiten.
* **Sticky-Stack-Abschnitte** - Abschnitte, die beim Scrollen fixiert und gestapelt werden.

### Karten & Container
* **Parallax-Neigungskarte** - 3D-Neigung, die den Mauskoordinaten folgt.
* **Spotlight-Rahmenkarte** - Rahmen leuchten unter dem Cursor auf.
* **Glasmorphismus-Panel** - Mattglas mit innerer Lichtbrechung.
* **Holografische Folienkarte** - Schillernder Regenbogenwechsel beim Überfahren.
* **Tinder-Wischstapel** - Physischer Kartenstapel, wegwischbar.
* **Morphing-Modal** - Button expandiert zu seinem eigenen Dialog.

### Scroll-Animationen
* **Sticky-Scroll-Stapel** - Karten haften und stapeln sich physisch.
* **Horizontal-Scroll-Hijack** - Vertikales Scrollen → horizontaler Schwenk.
* **Locomotive / Sequenz-Scroll** - Video / 3D-Sequenz an die Scrollleiste gekoppelt.
* **Zoom-Parallax** - Zentrales Hintergrundbild zoomt beim Scrollen.
* **Scroll-Fortschrittspfad** - SVG-Linie, die sich beim Scrollen zeichnet.
* **Liquid-Swipe-Übergang** - Seitenübergang wie zähflüssige Flüssigkeit.

### Galerien & Medien
* **Kuppel-Galerie** - 3D-Panoramagalerie.
* **Coverflow-Karussell** - 3D-Karussell mit abgewinkelten Kanten.
* **Ziehen-zum-Schwenken-Raster** - Grenzenlose, verschiebbare Leinwand.
* **Akkordeon-Bildslider** - Schmale Streifen, die sich beim Überfahren ausdehnen.
* **Hover-Bildspur** - Beim Verlassen mit der Maus erscheint eine Spur aufpoppender Bilder.
* **Glitch-Effekt-Bild** - RGB-Kanalverschiebung beim Überfahren.

### Typografie & Text
* **Kinetisches Laufband** - Endlose Textbänder, die sich beim Scrollen umkehren.
* **Text-Masken-Enthüllung** - Riesige Schrift als transparentes Fenster zum Video.
* **Text-Scramble-Effekt** - Matrix-artige Entschlüsselung beim Laden / Überfahren.
* **Kreisförmiger Textpfad** - Text, der sich entlang eines rotierenden Kreises krümmt.
* **Verlaufs-Konturanimation** - Umrandeter Text mit laufendem Verlauf.
* **Kinetisches Typografie-Raster** - Buchstaben, die dem Cursor ausweichen.

### Mikrointeraktionen & Effekte
* **Partikel-Explosions-Button** - Call-to-Action zerspringt bei Erfolg in Partikel.
* **Flüssiges Pull-to-Refresh** - Ladeindikator wie sich lösende Tropfen.
* **Skeleton-Shimmer** - Wandernde Lichtreflexion über Platzhalter.
* **Richtungsbewusster Hover-Button** - Füllung betritt von der exakten Cursorseite.
* **Ripple-Klick-Effekt** - Welle von den Klickkoordinaten aus.
* **Animierte SVG-Linienzeichnung** - Vektoren, die sich in Echtzeit selbst zeichnen.
* **Mesh-Verlaufshintergrund** - Organische Lavalampen-Blobs.
* **Linsenunschärfe-Tiefe** - Hintergrund-UI wird unscharf, um die Vordergrundaktion zu fokussieren.

### Wahl der Animationsbibliothek
* **Motion (`motion/react`)** - Standard für UI- / Bento- / Zustandsänderungs-Bewegung.
* **GSAP + ScrollTrigger** - für vollseitiges Scrollytelling und Scroll-Hijacks. In dedizierten Blattkomponenten mit `useEffect`-Bereinigung isolieren.
* **Three.js / WebGL** - für Canvas-Hintergründe und 3D-Szenen. Gleiche Isolationsregel.
* **NIEMALS GSAP / Three.js mit Motion im selben Komponentenbaum mischen.** Sie konkurrieren um dieselben Frames.

---

## 11. REDESIGN-PROTOKOLL

Dieser Skill behandelt **Neubauten UND Redesigns**. Eine falsche Einordnung des Modus ist die größte Einzelursache für schlechte Redesign-Ergebnisse.

### 11.A Modus erkennen (erste Aktion)
* **Neubau** - keine bestehende Website oder genehmigte Gesamtüberarbeitung. Ausgangsbasis aus Abschnitt 1.
* **Redesign - Erhalten** - modernisieren, ohne die Marke zu brechen. Zuerst prüfen, Markentoken extrahieren, schrittweise weiterentwickeln.
* **Redesign - Überarbeitung** - neue visuelle Sprache auf bestehendem Inhalt. Bei Visuals wie einen Neubau behandeln; Inhalte und Informationsarchitektur bewahren.

Bei Unklarheit **einmal** nachfragen: *„Soll dieses Redesign die bestehende Marke erhalten, oder beginnen wir visuell bei null?"*

### 11.B Vor dem Eingriff prüfen
Den aktuellen Zustand dokumentieren, bevor Änderungen vorgeschlagen werden:
* **Markentoken** - Primär- / Akzentfarben, Schriftstapel, Logo-Gestaltung, Radien.
* **Informationsarchitektur** - Seitenbaum, primäre Navigation, zentrale Konversionspfade.
* **Inhaltsblöcke** - was existiert, was seine Aufgabe erfüllt, was Füllmaterial ist.
* **Zu bewahrende Muster** - charakteristische Interaktionen, erkennbarer Hero-Bereich, Textstimme.
* **Auszumusternde Muster** - KI-Schrott-Merkmale, defekte Layouts, tote Links, generische Stockbilder, Performance-Fallen.
* **Dial-Auslesung der bestehenden Website** - aktuelle `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY` ableiten. Das ist Ihr Ausgangspunkt, nicht die Basislinie.
* **SEO-Basislinie** - aktuelle Ranking-Seiten, Meta-Titel, strukturierte Daten, OG-Karten. **SEO-Migration ist das Risiko Nr. 1 bei Redesigns.**

### 11.C Erhaltungsregeln
* **Informationsarchitektur nicht ändern**, sofern nicht gewünscht. Seiten-Slugs, Anker-IDs und primäre Navigationsbeschriftungen für SEO und Gewohnheit stabil halten.
* **Markenfarben extrahieren, bevor Abschnitt 4.2 angewendet wird.** Eine Marke, die bereits lila ist, bleibt lila – es gilt die Übersteuerung der LILA-REGEL.
* **Textstimme bewahren**, sofern keine Neufassung gewünscht ist. Visuelle Modernisierung ≠ inhaltliche Neufassung.
* **Bestehende Barrierefreiheits-Erfolge achten.** Fokuszustände, Alt-Texte, Tastaturnavigation und Kontrast nicht verschlechtern.
* **Bestehende Analytics-Ereignisse respektieren.** Schaltflächen, Formularfelder und Abschnitts-IDs, von denen nachgelagertes Tracking abhängt, nicht umbenennen.

### 11.D Modernisierungshebel (nach Priorität)

In der angegebenen Reihenfolge anwenden – aufhören, sobald das Briefing erfüllt ist:

1. **Typografie-Auffrischung** – größter visueller Gewinn pro Risikoeinheit.
2. **Abstände & Rhythmus** – Abschnittsabstände vergrößern, vertikalen Rhythmus korrigieren.
3. **Farbkalibrierung** – entsättigen, Neutraltöne vereinheitlichen, Markenakzent beibehalten.
4. **Bewegungsebene** – `MOTION_INTENSITY`-gerechte Mikrointeraktionen zu bestehenden Komponenten hinzufügen.
5. **Hero- & Schlüsselabschnitts-Neukomposition** – Einstiegsbereich mit dem Vokabular aus Abschnitt 10 neu strukturieren.
6. **Vollständiger Blockersatz** – nur, wenn der bestehende Block nicht mehr zu retten ist.

### 11.E Entscheidungsbaum: Gezielte Weiterentwicklung vs. vollständiges Redesign

* IA, Inhalt und SEO sind solide → **gezielte Weiterentwicklung** (Hebel 1–4). Etwa 70 % des Nutzens bei etwa 40 % des Risikos.
* Die visuelle Schuld ist strukturell (defekte IA, kein Designsystem, defekte mobile Ansicht) → **vollständiges Redesign** mit strikter Inhaltserhaltung.
* Die Marke selbst ändert sich → **Neuentwicklung auf der grünen Wiese**.

### 11.F Was sich niemals stillschweigend ändert

Niemals ohne ausdrückliche Zustimmung des Nutzers ändern:

* URL-Struktur / Routen-Slugs.
* Beschriftungen der primären Navigation.
* Formularfeldnamen oder deren Reihenfolge (bricht Analytics + Autofill).
* Markenlogo oder Wortmarke.
* Bestehende Rechtstexte / Einwilligungs- / Cookie-Texte.

---

## 12. DIE BLOCKBIBLIOTHEK (Vertrag – Implementierungen entstehen iterativ hier)

Das Referenzvokabular (Abschnitt 10) benennt Muster. Die Blockbibliothek implementiert sie mit echten Props, echten Bewegungsspezifikationen und echten Code-Skizzen.

**Status:** Schema hier definiert. Blöcke werden iterativ ergänzt. Keine neuen Blöcke ohne Befolgung dieses Schemas frei erfinden.

### 12.A Dateispeicherort

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


### 12.B Pflicht-Frontmatter

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


### 12.C Pflicht-Hauptabschnitte

1. **Visuelle Skizze** – kurze ASCII- oder Textbeschreibung des Layouts.
2. **Props-API** – die Schnittstelle der Komponente.
3. **Code-Skizze** – minimale lauffähige Implementierung (Server Component als Standard, Client-Insel für Bewegung).
4. **Mobiler Fallback** – explizite Einklapp-Regeln für `< 768px`.
5. **Bewegungsvarianten** – eine Variante pro `MOTION_INTENSITY`-Band (1–3, 4–7, 8–10). Fallback für reduzierte Bewegung explizit angeben.
6. **Dark-Mode-Hinweise** – Token-Strategie speziell für diesen Block.
7. **Antimuster** – häufige Arten, wie dieser Block schiefgeht.
8. **Referenzen** – Links zu echten Beispielen in der Produktion.

### 12.D Disziplin der Blockbibliothek

* Ein Block pro Datei. Keine Dateien mit mehreren Blöcken.
* Jeder Block muss eigenständig funktionieren (in eine Seite einfügen, er rendert).
* Jeder Block muss die Pre-Flight-Prüfung (Abschnitt 14) bestehen.
* Blöcke, die von einem Designsystem aus Abschnitt 2.A abhängen, liegen unter `blocks/<category>/<name>--<system>.md` (z. B. `feature/bento-grid--material.md`).

---

## 13. NICHT IM GELTUNGSBEREICH

Dieser Skill ist NICHT gedacht für:

* Dashboards / dichte Produkt-UIs / Admin-Panels (Fluent, Carbon, Atlassian oder Polaris aus Abschnitt 2.A verwenden).
* Datentabellen (TanStack Table oder AG Grid verwenden).
* Mehrstufige Formulare / Assistenten (formularspezifische Muster verwenden; dieser Skill macht sie nicht besser).
* Code-Editoren (Monaco / CodeMirror mit deren offizieller Gestaltung verwenden).
* Native Mobile-Apps (Apple HIG / Material direkt verwenden).
* Echtzeit-Kollaborations-UIs (Präsenz, Cursor, OT-bewusst – eine andere Problemklasse).

Wenn das Briefing einem der oben genannten Fälle entspricht, **dies ausdrücklich sagen**, auf das richtige Werkzeug verweisen und nur die Marketing-, Über-uns- und Landingpage-Teile dieses Skills auf die Oberflächen anwenden, für die sie zutreffen.

---

## 14. ABSCHLIESSENDE PRE-FLIGHT-PRÜFUNG

Vor der Ausgabe von Code diese Matrix durchlaufen. Dies ist der letzte Filter.

**DAS IST NICHT OPTIONAL. Jedes Kästchen prüfen. Schlägt ein Kästchen fehl, ist die Ausgabe nicht fertig.**

- [ ] **Kurze Inferenz** deklariert (Abschnitt 0.B, Einzeiler)?
- [ ] **Dial-Werte** explizit und aus dem Briefing begründet, nicht stillschweigend der Baseline folgend?
- [ ] **Designsystem** aus Abschnitt 2 gewählt, falls zutreffend, oder Ästhetik ehrlich benannt?
- [ ] **Redesign-Modus** erkannt und Audit durchgeführt (falls zutreffend, Abschnitt 11)?
- [ ] **NULL Gedankenstriche (`—`) auf der gesamten Seite.** Überschriften, Eyebrows, Pills, Fließtext, Zitate, Attributionen, Bildunterschriften, Buttons, Alt-Texte. Null. (Abschnitt 9.G, nicht verhandelbar.)
- [ ] **Page Theme Lock**: EIN Theme (hell, dunkel oder automatisch) für die gesamte Seite. Kein Abschnitt wechselt mitten auf der Seite in den invertierten Modus (Abschnitt 4.11)?
- [ ] **Color Consistency Lock**: eine Akzentfarbe, identisch in allen Abschnitten verwendet (Abschnitt 4.2)?
- [ ] **Shape Consistency Lock**: ein Eckenradius-System, konsistent angewendet (Abschnitt 4.4)?
- [ ] **Button-Kontrast-Prüfung**: jeder CTA-Text ist auf seinem Hintergrund lesbar (kein Weiß auf Weiß, WCAG AA 4,5:1)?
- [ ] **CTA-Button-Umbruch**: kein CTA-Label bricht auf Desktop in 2 oder mehr Zeilen um?
- [ ] **Formular-Kontrast-Prüfung**: Formulareingaben, Platzhalter, Fokusringe und Labels bestehen WCAG AA gegenüber dem Abschnittshintergrund?
- [ ] **Serifen-Disziplin**: falls eine Serifenschrift verwendet wird, ist es NICHT Fraunces oder Instrument_Serif (oder doch, mit expliziter Markenbegründung)? Andere Serifenschrift als im vorherigen Projekt?
- [ ] **Prüfung der Premium-Consumer-Palette**: falls das Briefing Premium-Consumer ist (Kochgeschirr / Wellness / Handwerk / Luxus), ist die Palette NICHT die KI-typische Beige-Messing-Oxblut-Espresso-Familie? Andere Familie als im vorherigen Premium-Consumer-Projekt?
- [ ] **Freiraum für kursive Unterlängen**: jedes kursive Wort mit `y g j p q` hat mindestens `leading-[1.1]` plus `pb-1` Reserve?
- [ ] **Hero passt in den Viewport**: Überschrift ≤ 2 Zeilen, Untertext ≤ 20 Wörter UND ≤ 4 Zeilen, CTA ohne Scrollen sichtbar, Schriftgröße um das Bild herum geplant?
- [ ] **Hero-Abstand oben**: maximal `pt-24` auf Desktop, Hero-Inhalt schwebt nicht auf halber Viewport-Höhe?
- [ ] **Hero-Stack-Disziplin**: maximal 4 Textelemente im Hero (Eyebrow ODER Markenleiste, Überschrift, Untertext, CTAs)? Kein winziger Tagline unter den CTAs, kein Vertrauens-Mikrostreifen im Hero?
- [ ] **EYEBROW-ANZAHL (mechanisch)**: Anzahl der `uppercase tracking`-Mikrolabels über Abschnittsüberschriften über alle Komponenten zählen. Anzahl ≤ ceil(Abschnittsanzahl / 3)? Der Hero zählt als 1.
- [ ] **Split-Header-Verbot**: kein Muster „große Überschrift links + kleiner erklärender Absatz rechts" als Abschnittskopf (stattdessen vertikaler Stack)?
- [ ] **Zickzack-Wechselgrenze**: keine 3 oder mehr aufeinanderfolgenden Abschnitte mit demselben Bild-plus-Text-Split-Layout?
- [ ] **Keine doppelte CTA-Absicht**: keine zwei CTAs mit derselben Absicht („Kontakt aufnehmen" und „Lass uns sprechen" beide auf der Seite = Fehler)?
- [ ] **Logo-Wand = nur Logos**: keine Branchen- oder Kategoriebezeichnungen unter den Logos?
- [ ] **Bento-Hintergrundvielfalt**: mindestens 2 bis 3 Bento-Zellen mit echter visueller Variation (Bild, Verlauf, Muster), nicht alle reine Textkarten auf Weiß?
- [ ] **Logo-Wand „Genutzt von / Vertraut von"** liegt UNTER dem Hero, nicht darin, verwendet ECHTE SVG-Logos (Simple Icons / devicon) oder generierte SVG-Marken, KEINE reinen Textwortmarken?
- [ ] **Selbstprüfung der Texte**: jede sichtbare Zeichenkette erneut gelesen, keine grammatikalisch defekten oder KI-halluzinierten Formulierungen („free on its past"-Typ) ausgeliefert?
- [ ] **Motion motiviert**: jede Animation lässt sich in einem Satz begründen (Hierarchie / Storytelling / Rückmeldung / Zustandsübergang), kein GSAP um der Wirkung willen?
- [ ] **Maximal ein Marquee pro Seite**: keine zwei horizontalen Laufschriften auf derselben Seite?
- [ ] **Navigation in EINER Zeile** auf Desktop, Höhe ≤ 80px?
- [ ] **Prüfung der Abschnitts-Layout-Wiederholung**: keine zwei Abschnitte teilen dieselbe Layoutfamilie (mindestens 4 verschiedene Familien über 8 Abschnitte)?
- [ ] **Bento hat Rhythmus UND exakte Zellenanzahl** (N Elemente → N Zellen, keine leeren Zellen in der Mitte oder am Ende)?
- [ ] **Lange Listen verwenden die richtige UI-Komponente** (nicht standardmäßig `<ul>` mit `divide-y` bei mehr als 5 Elementen, siehe Alternativen in Abschnitt 4.9)?
- [ ] **Echte Bilder verwendet** (zuerst Generierungstool, dann Picsum-Seed, dann explizite Platzhalterslots), KEINE div-basierten Fake-Screenshots, KEINE handgebauten dekorativen SVGs, KEIN reiner Textminimalismus?
- [ ] **Keine Pills oder Labels über Bildern** (kein `Plate · Brand`, kein `Field notes - journal`)?
- [ ] **Keine Fotonachweis-Bildunterschriften als Dekoration** (`Field study no. 12 · Ines Caetano`)?
- [ ] **Keine Versionsfußzeilen** (`v1.4.2`, `Build 0048`) auf Marketingseiten?
- [ ] **Keine Mikro-Metasätze** unter Eyebrows („Jedes davon ist eine Funktion, die wir heute ausliefern ...")?
- [ ] **Kein dekorativer Textstreifen am unteren Heroende** (`BRAND. MOTION. SPATIAL.`)?
- [ ] **Kein schwebender Untertext oben rechts** in Abschnittsüberschriften?
- [ ] **Keine Scoring- oder Fortschrittsbalken mit gefüllten Hintergrundspuren** als Vergleichsvisualisierung?
- [ ] **Keine Orts-, Stadt-, Uhrzeit- oder Wetterstreifen**, außer das Briefing ist wirklich global verteilt oder ortsbezogen?
- [ ] **Keine Scroll-Hinweise** (`Scroll`, `↓ scroll`, `Scroll to explore`)?
- [ ] **Keine Versionsangaben im Hero** (V0.6, BETA, INVITE-ONLY), außer das Briefing ist ein Launch?
- [ ] **Keine abschnittsnummerierenden Eyebrows** (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`)?
- [ ] **Keine dekorativen Punkte** (standardmäßig null, nur für echte semantische Zustände)?
- [ ] **Kein `border-t` + `border-b` in jeder Zeile** langer Listen oder Spezifikationstabellen?
- [ ] **Inhaltsdichte vernünftig**: keine Datentabellen mit 20 Zeilen, keine scheinbar präzisen Spezifikationen ohne Begründung, Unterabsätze standardmäßig ≤ 25 Wörter?
- [ ] **Zitate ≤ 3 Zeilen** Fließtext, saubere Attribution (kein Gedankenstrich)?
- [ ] **Behauptete Motion = gezeigte Motion**: falls `MOTION_INTENSITY > 4`, animiert die Seite tatsächlich und wird nicht nur behauptet?
- [ ] **GSAP Sticky-Stack / horizontales Schwenken** gemäß dem kanonischen Skelett aus Abschnitt 5.A / 5.B implementiert (`start: "top top"`, `pin: true`, korrektes Scrub)?
- [ ] **Kein `window.addEventListener('scroll')`**: nur Motion `useScroll()` / ScrollTrigger / IntersectionObserver / CSS-Scroll-gesteuerte Animationen?
- [ ] **Reduced Motion** umschließt alles, was `MOTION_INTENSITY > 3` ist?
- [ ] **Dark-Mode-Tokens** definiert und in beiden Modi getestet?
- [ ] **Mobiler Umbruch** explizit (`w-full`, `px-4`, `max-w-7xl mx-auto`) für Layouts mit hoher Varianz?
- [ ] **Viewport-Stabilität**: `min-h-[100dvh]`, niemals `h-screen`?
- [ ] **`useEffect`-Animationen** haben strikte Cleanup-Funktionen?
- [ ] **Leere, Lade- und Fehlerzustände** vorhanden?
- [ ] **Karten weggelassen** zugunsten von Abstand, wo möglich?
- [ ] **Icons** nur aus einer erlaubten Bibliothek (Phosphor / HugeIcons / Radix / Tabler), keine handgebauten SVG-Pfade?
- [ ] **Motion** in Client-Blattkomponenten isoliert, mit `'use client'` am Anfang, memoisiert?
- [ ] **Keine KI-Erkennungsmerkmale** aus Abschnitt 9 (Inter als Standard, KI-Lila, drei gleich große Karten, Jane Doe, Acme, „Still im Einsatz bei")?
- [ ] **Core Web Vitals** plausibel eingehalten (LCP < 2,5 s, INP < 200 ms, CLS < 0,1)?
- [ ] **Ein Designsystem** pro Projekt (kein Material und shadcn gemischt)?

Wenn ein einzelnes Kontrollkästchen nicht ehrlich abgehakt werden kann, ist die Seite nicht fertig. Behebe dies, bevor du sie auslieferst.

---

# ANHÄNGE - Reales, quellengestütztes Referenzmaterial

Die folgenden Abschnitte sind gebündelte Referenzinhalte. Sie liefern dem Agenten echte Installationsbefehle, echte kanonische Dokumentationslinks und funktionierende Starter-Snippets für jedes in Abschnitt 2 genannte Design-System. Nutze sie, um Entscheidungen auf produktiver Realität statt auf Trainingsdaten-Fiktion zu gründen.

## Anhang A - Installationsbefehle pro Design-System

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


## Anhang B - Kanonische Quellen (vor eigenen Neuentwicklungen lesen)

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

### Natives CSS / W3C-Standards
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-color-scheme
- https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations
- https://drafts.csswg.org/scroll-animations-1/

### Apple Liquid Glass (nur Apple-Plattformen)
- https://developer.apple.com/design/human-interface-guidelines/materials
- https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- https://developer.apple.com/documentation/SwiftUI/Material

---

## Anhang C - Apple Liquid Glass: Ehrliche Web-Annäherung

Behandle zufällige CSS-Snippets **nicht** als offizielles Apple Liquid Glass.

### Was offiziell ist
Apple dokumentiert Liquid Glass in den Human Interface Guidelines und der Developer Documentation für **Apple-Plattformen**. Es ist ein dynamisches Material, das in der UI aller Apple-Plattformen verwendet wird. Apples native Implementierung gehört zu den Apple-Plattform-APIs und Systemkomponenten, **nicht zu einem öffentlichen Web-CSS-Paket**.

Relevante offizielle Dokumentation:
- Apple Human Interface Guidelines → Materials
- Apple Developer Documentation → Liquid Glass
- Apple Developer Documentation → Adopting Liquid Glass
- SwiftUI → Material

### Was NICHT offiziell ist
Es gibt kein `liquid-glass.css` von Apple für gewöhnliche Websites.

Eine Web-Annäherung kann Folgendes verwenden:
- `backdrop-filter`
- transparente Hintergründe
- geschichtete Rahmen
- Highlight-Overlays
- Verläufe
- Bewegung
- starke Kontrast-Fallbacks

Das ist jedoch **Web-Glassmorphism / Milchglas-Annäherung**, nicht offizielles Apple Liquid Glass. Kennzeichne es entsprechend in Kommentaren.

### Sichereres Web-Annäherungs-Grundgerüst

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


**Wichtig:** `prefers-reduced-transparency` hat uneinheitliche Browser-Unterstützung; teste es. Stelle immer genügend Kontrast bereit, auch ohne Weichzeichnung.

---

**Ende der Anhänge.** Die obigen Installationsbefehle sind Realitätsanker. Das Apple-Liquid-Glass-Grundgerüst ist eine gekennzeichnete Annäherung, kein von Apple herausgegebenes Paket. Für kanonische Dokumentation pro Design-System konsultiere die offizielle Dokumentation des jeweiligen Systems (Links in Abschnitt 2 sowie Anhang B).
