---
name: trauma-psychoeducation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Psicoeducação sobre trauma: definição de trauma, reações normais, janela de tolerância, gestão de gatilhos e autocuidado."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [trauma, psychoedukation, window-of-tolerance, trigger, selbstfürsorge, ptbs]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/trauma_psychoedukation.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ac52bd5204d10d048a095b234e73ff829346834b196f90ef520b5b24c2948be9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.188621+00:00"
---
<img src="banner.png" width="100%" alt="trauma-psychoeducation banner">

# Psicoeducação sobre Trauma

> Conhecimento sobre trauma, consequências traumáticas e a janela de tolerância: compreender reações normais a acontecimentos anormais — psicoeducação pura, SEM trabalho terapêutico sobre o trauma

Ver: [ETHICS.md](../ETHICS.md)

**Ver também:** [stabilization-techniques](../stabilization-techniques/SKILL.md) (Grounding, Lugar Seguro, Containment — técnicas imediatas) | [psychoeducation](../psychoeducation/SKILL.md) (TEPT no contexto de outros quadros clínicos)

---

## Contexto

A psicoeducação sobre trauma ajuda as pessoas afetadas a compreender e a enquadrar as suas reações. Saber que sintomas como flashbacks, hiperexcitação ou evitação são reações NORMAIS a acontecimentos ANORMAIS já é aliviante e reduz a vergonha e as autoacusações.

Evidência: a psicoeducação é um componente reconhecido da terapia do trauma (Flatten et al. 2011, diretriz S3 para TEPT). Por si só não é suficiente, mas pode aumentar a motivação para a terapia e atenuar os sintomas.

**IMPORTANTE:** Esta skill transmite exclusivamente CONHECIMENTO sobre trauma. NÃO realiza trabalho terapêutico sobre o trauma, NÃO explora memórias perturbadoras e NÃO pergunta por detalhes do trauma.
**Nunca implementar:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. O que é um trauma?

### Definição

Um trauma é um acontecimento que excede as capacidades de enfrentamento de uma pessoa e que se associa à vivência de impotência, perda de controlo e/ou medo de morte. Não é o acontecimento por si só que define o trauma, mas a vivência subjetiva.

### Tipos de trauma

| Tipo | Descrição | Exemplos |
|-----|-------------|----------|
| Tipo I (trauma único) | Acontecimento único e inesperado | Acidente, assalto, catástrofe natural |
| Tipo II (trauma complexo) | Traumatização repetida e prolongada | Maus-tratos, negligência, guerra |
| Trauma acidental | Acontecimentos fortuitos | Acidente de viação, incêndio em casa, acidente de trabalho |
| Trauma interpessoal | Causado por pessoas | Violência, abuso, tortura |
| Trauma secundário | Por testemunhar/presenciar | Profissões de ajuda, familiares |

### O que NÃO é trauma (delimitação)

Nem todo acontecimento perturbador é um trauma no sentido clínico:
- Separação, despedimento, discussão — perturbadores, mas normalmente não são trauma
- Bullying — pode ter efeito traumatizante (sobretudo em crianças), mas não é automaticamente trauma
- A avaliação individual é decisiva, não o tipo de acontecimento

---

## 2. Reações normais a acontecimentos anormais

### Os três padrões de reação

```
UEBERREGUNG (Hyperarousal)
- Staendige Wachsamkeit und Anspannung
- Schreckhaftigkeit
- Schlafprobleme
- Reizbarkeit, Wutausbrueche
- Konzentrationsschwierigkeiten

WIEDERERLEBEN (Intrusion)
- Flashbacks (Erinnerungen, die sich real anfuehlen)
- Alptraeume
- Belastende Erinnerungen, die ploetzlich auftauchen
- Koerperliche Reaktionen bei Erinnerung (Herzrasen, Schwitzen)

VERMEIDUNG UND BETAEUBUNG (Constriction)
- Vermeidung von Orten, Personen, Situationen
- Emotionale Taubheit
- Rueckzug von anderen Menschen
- Gefuehl der Entfremdung
- Verlust von Interesse und Freude
```

### Mensagem importante para as pessoas afetadas

```
"Diese Reaktionen sind NORMALE Reaktionen auf UNNORMALE Ereignisse.

Dein Koerper und dein Verstand versuchen, dich zu schuetzen.
Die Wachsamkeit schuetzt dich vor erneuter Gefahr.
Die Erinnerungen versuchen, das Erlebte zu verarbeiten.
Die Vermeidung schuetzt dich vor Ueberwaltigung.

Du bist nicht 'verrueckt'. Du bist nicht 'schwach'.
Dein Nervensystem reagiert so, wie es darauf programmiert ist,
auf extreme Bedrohung zu reagieren."
```

### Evolução temporal

```
VERLAUF NACH TRAUMATISCHEM EREIGNIS

0-4 Wochen:  Akute Belastungsreaktion (NORMAL)
             - Schock, Betaeubung, Unruhe
             - Schlafprobleme, Schreckhaftigkeit
             - Flashbacks, Alptraeume
             - Bei den meisten Menschen: Spontane Erholung

4+ Wochen:   Wenn Symptome nicht nachlassen: Moegliche PTBS
             - Professionelle Diagnostik empfohlen
             - Fruehe Intervention verbessert Prognose

Monate-Jahre: Chronifizierung moeglich
             - Therapie ist auch nach langer Zeit wirksam
             - "Es ist nie zu spaet, sich Hilfe zu holen"
```

---

## 3. A janela de tolerância (Window of Tolerance)

### O modelo (segundo Dan Siegel)

```
            ________________________________________________
           |                                                |
           |   UEBER DEM FENSTER: Hyperarousal              |
           |   Panik, Wut, Ueberregung, Flashbacks          |
           |   Herzrasen, Schwitzen, Zittern                 |
           |   "Kampf oder Flucht"                           |
           |________________________________________________|
           |                                                |
           |   FENSTER DER BELASTBARKEIT                     |
           |   (Window of Tolerance)                         |
           |                                                |
           |   Hier koennen wir:                             |
           |   - Denken und fuehlen gleichzeitig             |
           |   - Informationen verarbeiten                   |
           |   - Beziehungen gestalten                       |
           |   - Probleme loesen                             |
           |   - Lernen und wachsen                          |
           |________________________________________________|
           |                                                |
           |   UNTER DEM FENSTER: Hypoarousal                |
           |   Erstarrung, Taubheit, Dissoziation            |
           |   Energielosigkeit, Leere, Abschaltung          |
           |   "Totstell-Reflex"                             |
           |________________________________________________|
```

### O que significa?

- **Dentro da janela:** conseguimos regular o stress e funcionar
- **Acima da janela:** excitação excessiva — o corpo em modo de alarme
- **Abaixo da janela:** excitação insuficiente — o corpo desliga-se

### Trauma e a janela

```
VOR dem Trauma:           NACH dem Trauma (unbehandelt):

|_______________|         |_____|
|               |         |     |  <- Fenster ist ENGER geworden
|    FENSTER    |         | F.  |
|   (breit)     |         |     |
|_______________|         |_____|

Schon kleine Reize koennen nach einem Trauma dazu fuehren,
dass man aus dem Fenster faellt (Trigger).

ZIEL der Therapie: Das Fenster wieder WEITEN.
```

### Compreender os gatilhos

```
TRIGGER sind Reize, die an das Trauma erinnern und das Nervensystem
in den Alarmmodus versetzen — oft unbewusst.

Trigger koennen sein:
- Geraeusche (Knall, Schreien, bestimmte Musik)
- Gerueche (Rauch, Parfuem, Alkohol)
- Bilder (Nachrichten, Filme, Orte)
- Koerperempfindungen (Enge, Beruehrung, Schmerz)
- Kalenderdaten (Jahrestage)
- Beziehungssituationen (Streit, Kontrollverlust)

Trigger sind KEINE Schwaeche. Sie sind gespeicherte Warnsignale
des Nervensystems. In der Therapie lernt man, Trigger zu erkennen
und das Nervensystem zu regulieren.
```

---

## 4. Estratégias de autocuidado

### Garantir as necessidades básicas

```
CHECKLISTE GRUNDBEDUERFNISSE

[ ] Schlaf: Regelmaessige Schlafenszeiten, mindestens 7 Stunden
[ ] Ernaehrung: Regelmaessige Mahlzeiten, ausreichend Wasser
[ ] Bewegung: Taeglich mindestens 20 Minuten (Spaziergang reicht)
[ ] Soziale Kontakte: Mindestens eine vertrauensvolle Person
[ ] Sicherheit: Sich im eigenen Umfeld sicher fuehlen
[ ] Struktur: Tagesablauf mit festen Ankerpunkten
```

### Estratégias de autocuidado no dia a dia

**Físico:**
- Movimento regular (reduz as hormonas do stress)
- Exercícios de respiração
- Dormir o suficiente (respeitar a higiene do sono)
- Reduzir cafeína e álcool (intensificam a hiperexcitação/entorpecimento)

**Social:**
- Ter uma pessoa de confiança (não é preciso falar sobre o trauma)
- Evitar o isolamento — também ajudam pequenos contactos
- Aprender a estabelecer limites (é permitido dizer "não")
- Aceitar apoio

**Emocional:**
- Nomear os sentimentos (sem os avaliar)
- Usar técnicas de estabilização (5-4-3-2-1, Lugar Seguro)
- Escrever um diário (opcional, não forçar)
- Encontrar formas criativas de expressão (pintura, música, escrita)

**Cognitivo:**
- Informar-se (psicoeducação — esta skill)
- Questionar as autoacusações ("não foi culpa minha")
- Verificar a realidade quando há catastrofização
- Ter paciência consigo próprio (a recuperação leva tempo)

---

## 5. Encontrar ajuda profissional

### Quando procurar ajuda profissional?

```
PROFESSIONELLE HILFE IST ANGEZEIGT, WENN:

- Symptome laenger als 4 Wochen anhalten
- Symptome sich verschlimmern statt bessern
- Der Alltag nicht mehr bewaeltigbar ist (Arbeit, Beziehungen)
- Flashbacks oder Alptraeume sehr haeufig auftreten
- Vermeidungsverhalten das Leben stark einschraenkt
- Substanzmissbrauch als Bewaeltigungsstrategie
- Suizidgedanken oder Selbstverletzung
- Das Gefuehl: "Ich schaffe das nicht alleine"
```

### Pontos de contacto (Alemanha)

```
SOFORTHILFE:
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222 (24/7, kostenlos)
- Krisenchat: krisenchat.de (per Chat, fuer junge Menschen)
- Psychiatrischer Notdienst: 112

TRAUMASPEZIFISCH:
- Traumaambulanzen (an vielen Kliniken, keine Ueberweisung noetig)
- Opferhilfe: Weisser Ring (116 006)
- Gewaltschutzambulanz (bei koerperlicher Gewalt)
- Frauenhaus-Hotline: 08000 116 016
- Hilfetelefon sexueller Missbrauch: 0800 22 55 530

THERAPIEPLATZ:
- Terminservicestelle der Kassenärztlichen Vereinigung: 116 117
- Psychotherapie-Informationsdienst (PID): www.psychotherapiesuche.de
- Wichtig: Auf "Traumatherapie" spezialisierte Therapeuten suchen
```

---

## 6. Perguntas frequentes (FAQ)

### "Estou agora traumatizado?"

Nem toda a pessoa que vive um acontecimento perturbador desenvolve uma perturbação decorrente de trauma. A maioria das pessoas recupera espontaneamente em poucas semanas. Só um profissional pode diagnosticar se existe TEPT.

### "Tenho de falar sobre isso?"

Não. Forçar-se a falar pode ser prejudicial. Algumas pessoas beneficiam de falar sobre o que viveram, outras não. Não existe um "tem de". Na terapia, o momento certo é determinado em conjunto.

### "Porque reajo assim, se já passou há tanto tempo?"

As memórias traumáticas são armazenadas de forma diferente das memórias normais. Podem ser reativadas por gatilhos e parecer que o acontecimento está a acontecer AGORA. O cérebro não distingue entre "então" e "agora". A terapia ajuda a "reorganizar" estas memórias.

### "Sou fraco por não conseguir fazer isto sozinho?"

Não. Procurar ajuda é um sinal de força. A terapia do trauma é eficaz — a maioria das pessoas consegue melhorar significativamente com ajuda profissional.

---

## Ética e limites

**Um assistente de IA pode:**
- Transmitir conhecimento sobre trauma e as suas consequências (psicoeducação)
- Normalizar reações normais e aliviar
- Explicar a janela de tolerância
- Sugerir estratégias de autocuidado
- Encaminhar para ajuda profissional
- Oferecer técnicas de estabilização

**Um assistente de IA NÃO pode:**
- Realizar trabalho terapêutico sobre o trauma (EMDR, exposição, NET, IRRT)
- Perguntar por detalhes do trauma nem explorá-los
- Trabalhar o conteúdo de flashbacks (apenas estabilizar)
- Diagnosticar TEPT ou outras perturbações traumáticas
- Avaliar a suicidalidade
- Dar recomendações relativas a medicação
- Fazer afirmações sobre culpa ou responsabilidade
- "Processar" ou "elaborar" memórias
- Fazer perguntas sugestivas ("Será que poderia ser que...")

**LIMITE ESPECIALMENTE RIGOROSO:** o trabalho terapêutico sobre o trauma pertence às mãos de terapeutas do trauma formados. Esta skill oferece exclusivamente psicoeducação e estabilização. Perante qualquer forma de exploração do trauma: PARAR e encaminhar para um profissional.

**Perante sinais de crise aguda, encaminhar SEMPRE para:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Serviço psiquiátrico de urgência: 112
- Krisenchat: krisenchat.de

---

*Adaptado de BACH v3.8.0 | Versão autónoma*
*Fontes: Flatten et al. (2011), Siegel (2012), Reddemann (2001), diretriz S3 para TEPT (2019) — Não é terapia profissional*
