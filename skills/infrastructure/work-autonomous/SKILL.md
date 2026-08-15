---
name: work-autonomous
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-08-15
description: >
  Abbruchbedingung für autonome Loops: So weit wie möglich selbständig
  weiterarbeiten UND einen Loop erst beenden, wenn belegt ist, dass keine
  autonom ausführbare Aufgabe mehr vorliegt. Der bloße Eindruck "nichts mehr
  zu tun" reicht NICHT — er löst eine vierstufige Prüfkette aus (think/decide,
  _DECISIONS, Gardener/USMC, decision-avatar/BYUM), die zuerst neue Aufgaben
  GEWINNEN muss, bevor der Loop enden darf. Nutze diesen Skill bei
  /work-autonomous, /waafap, "arbeite autonom weiter bis nichts mehr zu tun
  ist", als Goal-Bedingung innerhalb eines /loop, oder wenn geprüft werden
  soll, ob wirklich keine autonome Arbeit mehr übrig ist, bevor ein Loop/eine
  Session beendet wird.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: de
status: active
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
---

# work-autonomous — Loop erst beenden, wenn belegt keine autonomen Aufgaben mehr vorliegen

## Zweck

Dieser Skill leistet zwei Dinge zugleich:

1. **So weit wie möglich autonom weiterarbeiten** — ganz normale Sitzungsarbeit, keine Besonderheit.
2. **Einen Loop erst beenden, wenn NACHGEWIESEN ist**, dass keine autonom ausführbare Aufgabe mehr
   existiert. Der Verdacht "ich finde gerade nichts mehr zu tun" ist **kein** Abbruchgrund — er ist
   der **Auslöser** einer Prüfkette, die zuerst versucht, neue Aufgaben zu **gewinnen**. Erst wenn
   diese Kette vollständig ergebnislos bleibt, gilt der Abbruch als belegt.

**Bewusst ohne eingebautes `/goal`:** Der Skill ist eigenständig nutzbar (z. B. direkt als
`/work-autonomous`-Aufruf innerhalb einer normalen Session) und ebenso als Bedingung innerhalb
einer übergeordneten Loop-Konstruktion: `/loop` normal vergeben, dann als Goal nur diesen Skill
nennen. Das Goal lautet dann sinngemäß: *"Beende den Loop, wenn keine autonomen Aufgaben mehr
vorliegen — und arbeite bis dahin so weit wie möglich autonom weiter."* Der Skill selbst ruft
kein `/goal`-Konstrukt auf; er liefert nur das eindeutige Abbruchsignal, das ein solches Konstrukt
lesen kann (siehe „Abbruchsignal" unten).

## Betriebsmodell — zwei Ebenen

### Ebene 1 — Normalarbeit (jeder Tick)

Bei jedem Aufruf zuerst ganz normal nach autonom ausführbarer Arbeit suchen (siehe Abgrenzung
unten) und sie erledigen: offene `ACTIONABLE`-Tickets, entblockte `BLOCKED`-Tickets, fällige
`WAITING`-Tickets, offene `TODO.md`/`AUFGABEN.txt`-Punkte in Projekten ohne User-Abhängigkeit,
fällige Routine-/Hygiene-Checks nach lokaler Policy, angefangene, aber nicht abgeschlossene Arbeit
aus der letzten Session (USMC `working`).

→ **Gefunden & erledigt:** Ergebnis kurz melden, Tick endet, Loop läuft normal weiter. Ebene 2 wird
NICHT betreten — keine der vier teuren Prüfschritte ist nötig, solange sichtbare Arbeit vorliegt.

### Ebene 2 — Exhaustion-Check (nur bei Verdacht „nichts mehr zu tun")

Erst wenn Ebene 1 **nichts** Autonomes mehr findet, entsteht der Verdacht. Dieser Verdacht allein
genügt nicht. Jetzt läuft **pflichtgemäß** die folgende Kette, um neue Aufgaben zu **gewinnen**:

1. **`/think` + `/decide`** auf die Frage anwenden: „Gibt es wirklich keine autonom ausführbare
   Arbeit mehr, oder übersehe ich etwas?" — strukturierte Analyse statt Bauchgefühl.
2. **Das zentrale Entscheidungsregister des Systems auswerten** — dort, wo offene und getroffene
   Nutzerentscheidungen geführt werden. Den Ort dafür **über die Rolle `decisions.ledger` auflösen**,
   nicht hart verdrahten: `source_resolver.resolve("decisions.ledger")` (Modul `source-resolver`,
   `.MODULES/.CONTROL/source-resolver`), falls installiert. Ist `source-resolver` nicht installiert
   oder liefert `not_found`, gilt ersatzweise der bekannte Fallback-Pfad (auf diesem System:
   `_control-center/_DECISIONS/`, `TO-DECIDE-USER*.txt`-Kette, host-eigene `TO-DECIDE-USER-<HOST>.txt`,
   `DECIDED-AND-DONE.md`; auf anderen Systemen entsprechend die dort geführte Entscheidungsablage) —
   der Skill funktioniert also identisch, mit oder ohne Resolver. Sind kürzlich Entscheidungen
   gefallen, die vorher blockierte oder auf Freigabe wartende Arbeit jetzt entsperren? Ein frisch
   entschiedener Punkt ist fast immer eine neue autonome Aufgabe (die Entscheidung umsetzen).
3. **Gardener und USMC auswerten** (`find()`/`recall()` bzw. `usmc facts|lessons|working|context`):
   Stehen dort offene Working-Memory-Punkte, Lessons mit unerledigter Folgeaufgabe, oder Fakten,
   die auf übersehene, aber ausführbare Arbeit hindeuten? Das ist genau der Ort, an dem frühere
   Sessions unfertige Punkte (`RESUME:`-Feld, offene `note`-Einträge) hinterlassen.
4. **`decision-avatar` anwenden** (auf Systemen mit lokalem Profil: `tom-lm` +
   `build-your-users-mind`/BYUM): Gibt es ein belegtes Muster, nach dem der Nutzer an dieser
   Stelle eine bestimmte Handlung autonom erledigt sehen wollte? Nur bei ausreichender Konfidenz
   (🟢/🟡) als neue Aufgabe zählen — 🔴 zählt nicht als gewonnene Aufgabe, sondern als offener
   Punkt für Schritt „Nur-User-Rest" unten.

**Nur wenn alle vier Schritte ergebnislos bleiben**, gilt „keine autonomen Aufgaben mehr" als
**belegt**. Erst dann ist der Loop wirklich zu Ende.

Findet irgendein Schritt neue Arbeit → zurück zu Ebene 1, Arbeit erledigen, Guard-Zustand (siehe
unten) auf „found" setzen statt „exhausted".

### Sonderfall: nur User-gebundene Reste

Wenn die Kette **keine autonome** Aufgabe mehr findet, aber `USER/*`-Tickets oder unentschiedene
`_DECISIONS`-Punkte offen sind, ist das trotzdem ein **STOP für die Autonomie** — aber nicht
„nichts zu tun", sondern „nichts *autonom* zu tun". Diese Punkte werden nach der Autonomie-Loop-Regel
aus `ticket-master` **gebündelt** vorgelegt (eine Sammelvorlage, keine Einzel-Pings), nicht einzeln
nachgefragt. Das Abbruchsignal unterscheidet diesen Fall ausdrücklich von echtem Leerstand.

## Abgrenzung — was zählt als „autonom ausführbar"?

Referenz: `ticket-master` Kategorien (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`).

| Fall | Autonom? | Begründung |
|---|---|---|
| `ACTIONABLE`-Ticket | **Ja** | Kein Blocker, keine User-Abhängigkeit — per Definition. |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | Nein, solange Blocker nicht **empirisch** entfallen ist | Periodischer Re-Check ist erlaubt (Autonomie-Loop), „vorhanden" reicht als Nachweis nicht — Beleg nötig. |
| `WAITING/*` (scheduled, review-due, marker) vor Termin/Marker | Nein | Zeitgebunden. |
| `WAITING/*` nach Termin/Marker-Eintritt | **Ja** | Bedingung erfüllt → zieht nach `ACTIONABLE`. |
| `USER/*` (decision, data, freigabe, hardware, session) | **Nie autonom** | Zwingend Nutzerentscheidung/-daten/-freigabe/-hardware/-sitzung. Gebündelt vorlegen, siehe oben. |
| `PARKED/*` (skip, backlog, until-trigger) | Nein, außer explizitem Auftrag/Trigger | Bewusst zurückgestellt, kein Auto-Re-Check. |
| Offene `TODO.md`/`AUFGABEN.txt`-Punkte ohne Freigabe-/Entscheidungsvermerk | **Ja** | Projektregister, normale Arbeit. |
| Fällige Routine-/Hygiene-Checks (Cooldown abgelaufen, kein Lock) | **Ja** | Reguläre Wartungsarbeit nach lokaler Policy. |
| Von `LOCK.user.*` gesperrte Bereiche | **Nie** | User-Lock — nur der Nutzer hebt ihn auf, siehe LOCK-SYSTEM. |
| Irreversible/extern wirksame Schritte ohne Policy-Freigabe (Zenodo-Upload, Push auf gejudgte/geschützte Branches, Server-Spend-Entscheidung jenseits der Laptop-Schwelle, endgültiges Löschen ohne Vorschau) | **Nein** | Braucht Freigabe/Entscheidung, auch wenn technisch ausführbar. |
| Nur per GUI/Login startbare Sitzung (z. B. Claude-Desktop-Aufgabe, interaktiver Login, physische Hardware-Handlung) | **Nie** | „Nur vom User startbare Sitzung" — kann kein Loop übernehmen. |

Faustregel: Autonom ist, was **ohne** Nutzerentscheidung, -freigabe, -daten, -hardware oder
-Sitzung zu Ende gebracht werden kann UND keine irreversible/extern wirksame Handlung ohne
dokumentierte Policy-Freigabe voraussetzt.

## Guard gegen Endlosschleifen (Pflicht)

**Problem:** Ohne Bremse würde die vierstufige Kette bei jeder erneuten Prüfung wieder komplett
laufen, obwohl sich seit dem letzten ergebnislosen Durchlauf nichts geändert hat — teuer und
witzlos, vor allem wenn der Skill wiederholt aufgerufen wird (Loop, Scheduled Task, erneuter
manueller Aufruf kurz nacheinander).

**Zustand wird in USMC persistiert** (Prozess-State gehört auf diesem System dorthin, nicht in
Markdown-Dateien):

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**Fingerprint** = eine grobe, aber prüfbare Kennzahl aus: Anzahl/IDs offener `ACTIONABLE`-Tickets,
mtime der `_DECISIONS`-Kette (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), Zahl neuer
USMC-`working`-Einträge seit dem letzten Kettendurchlauf. Ändert sich einer dieser Werte, hat sich
die Lage geändert — der Guard darf dann nicht mehr blind auf „exhausted" verharren.

**Ablauf vor jedem Kettendurchlauf:**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result == "exhausted"
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:
       → Kette NICHT erneut fahren.
       → Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                  Kein neuer Trigger. STOP (Guard aktiv)."
sonst:
       → Kette vollständig fahren (alle vier Schritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|found).
       → exhausted → STOP (belegt). found → zurück zu Ebene 1, Arbeit erledigen.
```

Ein einziger vollständig ergebnisloser Kettendurchlauf reicht als Beleg für „keine autonomen
Aufgaben mehr" (Ticket-Vorgabe: „erst wenn ALLE Schritte eines Durchlaufs ergebnislos bleiben").
Der Guard verhindert nicht das Feststellen selbst, sondern nur das **wiederholte, unveränderte
Neu-Feststellen** bei dichten Folgeaufrufen.

`GUARD_INTERVAL` ist konfigurierbar (Default 15 Minuten) — bei sehr träger Umgebung (seltene neue
Tickets/Entscheidungen) darf länger gewählt werden, bei sehr aktiver Umgebung kürzer.

## Abbruchsignal

Jeder Durchlauf endet mit **einer** eindeutigen, grep-baren Zeile, damit ein umgebender `/loop`
oder ein künftiges `/goal`-Konstrukt daraus lesen kann, ob weitergemacht werden soll:

```
WORK-AUTONOMOUS: CONTINUE                        — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                — Kette 1–4 vollständig ergebnislos, belegt keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (guard, unchanged since …) — Guard aktiv, kein neuer Trigger seit Zeitstempel.
WORK-AUTONOMOUS: STOP (user-only)                — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE` ist das einzige Signal, bei dem eine übergeordnete Schleife einen weiteren Tick
anstoßen soll. Alle `STOP`-Varianten sind der belegte Abbruch — inklusive Begründung, welcher der
drei STOP-Fälle vorliegt.

## Verhältnis zu anderen Skills

- **`think`/`decide`** — liefern die strukturierte Analyse/Entscheidung in Kettenschritt 1. Werden
  hier als Baustein aufgerufen, nicht neu erfunden.
- **`decision-avatar`** (dieser Skill, nutzerneutral) — liefert Kettenschritt 4. Auf Systemen mit
  einem konkreten, autorisierten Profil entspricht das `tom-lm` + `build-your-users-mind`.
- **`orchestrator`** — regelt, WIE an Subagenten delegiert und deren Fertigmeldung geprüft wird.
  `work-autonomous` regelt WANN überhaupt aufgehört wird zu suchen; beide sind kombinierbar
  (der Orchestrator kann als Teil der in Ebene 1 erledigten Arbeit auftreten).
- **`bugsweep`** — ein Beispiel für ein anderes, sich selbst begrenzendes Suchprotokoll
  (Verdopplungs-Eskalation statt Vier-Schritt-Kette). `work-autonomous` ist generischer: Es prüft
  nicht nur Code auf Bugs, sondern jede Quelle autonomer Arbeit.
- **Ticket-Kategorien (`ticket-master`)** — liefern das Vokabular für „autonom ausführbar" (siehe
  Abgrenzungstabelle) und die Vorlage für den Autonomie-Loop (BLOCKED-Re-Check, USER-Bündelung,
  WAITING-Termin-Ziehen, PARKED-Stillstand).

## Beispielablauf

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Kette 1–4 läuft.
        → Schritt 2 (_DECISIONS): DECIDED-AND-DONE.md hat einen neuen Eintrag seit 10 Min.
          → daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar.
        → Ebene 2: Kette 1–4 läuft, alle vier Schritte ergebnislos.
        → Guard: result=exhausted, fingerprint=FP1, timestamp=T1 geschrieben.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, unchanged since T1)
```

## Changelog

### 1.1.0 (2026-08-15)
- Referenz-Retrofit aus Ticket T-20260815-385400870: Schritt 2 (Entscheidungsregister) löst
  seinen Ort jetzt über die Rolle `decisions.ledger` auf (`source_resolver.resolve(...)`, Modul
  `source-resolver`), statt ihn hart zu verdrahten — mit dokumentiertem Fallback auf den bisherigen
  Pfad, falls der Resolver nicht installiert ist. Funktionsverhalten unverändert.

### 1.0.0 (2026-08-15)
- Erstversion aus Ticket T-20260815-522639345: Zwei-Ebenen-Betriebsmodell, Vier-Schritt-Prüfkette,
  Abgrenzungstabelle nach `ticket-master`-Kategorien, USMC-gestützter Guard gegen Endlosschleifen,
  eindeutiges Abbruchsignal für `/loop`/`/goal`-Konstruktionen.
