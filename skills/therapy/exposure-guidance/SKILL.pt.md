---
name: exposure-guidance
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Exposição graduada em transtornos de ansiedade: hierarquia de ansiedade, escala SUDs, planejamento e acompanhamento da exposição. Apenas psicoeducação, sem execução."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [exposition, angst, phobie, suds, graduiert, verhaltenstherapie]
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
  origin_path: "system/skills/therapie/exposition_begleitung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: cc2d8527c2aeecc0056fd3a0f28b717f4bab39d67c82f6a2fd2f67c5336fc667
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.188621+00:00"
---

<img src="banner.png" width="100%" alt="exposure-guidance banner">

# Acompanhamento de Exposição

> Compreender hierarquia de ansiedade, escala SUDs, exposição graduada e habituação: planejamento e acompanhamento — exposição real somente com terapeuta

Veja: [ETHICS.md](../ETHICS.md)

---

## Contexto

A exposição (terapia de confrontação) é um dos métodos mais eficazes da terapia comportamental nos transtornos de ansiedade, fobias, transtornos obsessivo-compulsivos e TEPT.
Ela se baseia nos princípios de habituação e extinção: ao expor-se repetidamente a uma situação que desperta ansiedade, a reação de ansiedade diminui com o tempo.

Evidência: a terapia de exposição é o tratamento padrão-ouro para fobias específicas, ansiedade social, transtorno de pânico e agorafobia (Diretrizes NICE, Bandelow et al. 2014, Diretriz S3 para transtornos de ansiedade). Os tamanhos de efeito estão entre os mais altos da pesquisa em psicoterapia.

**IMPORTANTE:** Esta habilidade apoia o PLANEJAMENTO de exercícios de exposição e transmite a compreensão dos princípios de ação. A EXECUÇÃO da exposição deve ocorrer sob orientação de um terapeuta qualificado.
**Nunca implementar:** EMDR, Exposição Prolongada (PE), Terapia de Exposição Narrativa (NET)

---

## 1. Compreender os princípios de ação

### Habituação

```
HABITUATION: Gewöhnung durch wiederholte Konfrontation

Angstlevel
100 |  *
    | * *
 80 |*   *
    |     *
 60 |      *
    |       *
 40 |        *
    |         *  *
 20 |          **  * *
    |                  * * * * * *
  0 |________________________________
    Zeit (während der Exposition)

Die Angst steigt zunächst an, erreicht einen Höhepunkt
und sinkt dann OHNE Flucht oder Vermeidung von selbst ab.

Entscheidende Erfahrung: "Die Angst geht vorbei, auch wenn
ich in der Situation bleibe."
```

### Extinção (Aprendizagem Nova)

```
EXTINKTION: Neue Erfahrungen überschreiben alte Angst-Assoziationen

Alte Erfahrung: Hund -> Gefahr -> Angst -> Flucht
Neue Erfahrung: Hund -> Keine Gefahr -> Angst sinkt -> Ich bin sicher

Die alte Assoziation wird nicht gelöscht, sondern durch neue
Erfahrungen überlagert. Deshalb kann die Angst in bestimmten
Kontexten zurückkehren (Renewal, Reinstatement) — was NORMAL ist.
```

### Por que a evitação mantém o problema

```
DER VERMEIDUNGSTEUFELSKREIS:

Angstauslösende Situation
        |
        v
Angst steigt (unangenehm)
        |
        v
Vermeidung/Flucht
        |
        v
Kurzfristige Erleichterung (Angst sinkt sofort)
        |
        v
Langfristige Verstärkung der Angst
("Die Situation IST gefährlich, gut dass ich geflohen bin")
        |
        v
Nächstes Mal: Noch mehr Angst, noch mehr Vermeidung
```

---

## 2. A escala SUDs

### Subjective Units of Distress (0-100)

```
SUDS-SKALA (Subjektive Belastungsskala)

  0  Völlig entspannt, keine Angst
 10  Minimale Anspannung, kaum spürbar
 20  Leichte Unruhe, gut auszuhalten
 30  Deutlich unangenehm, aber kontrollierbar
 40  Merkliche Angst, noch handlungsfähig
 50  Mittlere Angst, anstrengend aber machbar
 60  Starke Angst, Vermeidungsimpuls deutlich
 70  Sehr starke Angst, schwer auszuhalten
 80  Intensive Angst, am Rand der Belastbarkeit
 90  Extreme Angst, Panikgefühl
100  Maximale Angst, schlimmste vorstellbare Belastung
```

### Aplicação da escala SUDs

**Antes da exposição:**
- Ansiedade estimada na situação planejada (valor esperado)

**Durante a exposição:**
- Avaliar o valor SUDs atual a cada 5 minutos
- Registrar como é o curso (sobe, desce, oscila)

**Após a exposição:**
- Valor SUDs mais alto? Valor final? Com que rapidez a ansiedade diminuiu?
- Foi tão ruim quanto o esperado?

---

## 3. Criar a hierarquia de ansiedade

### Princípio

Uma hierarquia de ansiedade ordena as situações que desencadeiam ansiedade do nível mais baixo ao mais alto.
A exposição começa com situações leves e aumenta gradualmente.

### Procedimento

```
ANGST-HIERARCHIE ERSTELLEN

Schritt 1: Alle angstauslösenden Situationen sammeln
Schritt 2: Jede Situation mit SUDs-Wert (0-100) bewerten
Schritt 3: Von niedrig nach hoch ordnen
Schritt 4: Lücken füllen (möglichst 10er-Schritte)
```

### Exemplo: medo de cães

```
ANGST-HIERARCHIE: Hundephobie

SUDs | Situation
-----|--------------------------------------------------
 10  | Bild von einem Hund anschauen
 15  | Video von spielenden Hunden anschauen
 25  | Über eigene Erfahrungen mit Hunden sprechen
 30  | Einen kleinen Hund aus 10 Metern Entfernung beobachten
 40  | Einen kleinen Hund aus 5 Metern Entfernung beobachten
 50  | Neben einem angeleinten kleinen Hund stehen (2 Meter)
 55  | Einen kleinen angeleigten Hund berühren (Besitzer hält)
 60  | Einen mittelgroßen Hund aus 5 Metern beobachten
 65  | Neben einem angeleinten mittelgroßen Hund sitzen
 70  | Einen mittelgroßen Hund streicheln
 75  | An einem freilaufenden Hund vorbeigehen (Park)
 80  | Allein in einem Raum mit einem ruhigen Hund sein
 85  | Einen großen Hund streicheln
 90  | In einem Park mit mehreren freilaufenden Hunden sein
 95  | Einen Hund füttern
100  | Einen fremden Hund auf sich zulaufen lassen
```

### Exemplo: ansiedade social

```
ANGST-HIERARCHIE: Soziale Angst

SUDs | Situation
-----|--------------------------------------------------
 15  | Einen Fremden nach der Uhrzeit fragen
 20  | Im Supermarkt an der Kasse ein kurzes Gespräch führen
 30  | In einer kleinen Gruppe eine Frage stellen
 40  | Einen Bekannten anrufen
 45  | Blickkontakt halten während eines Gesprächs
 55  | Allein in ein Cafe gehen und dort essen
 60  | Einer Gruppe von 5 Personen etwas erzählen
 70  | Bei einer Feier auf einen Fremden zugehen
 75  | Im Restaurant Essen zurückschicken
 80  | Vor 10 Personen eine kurze Präsentation halten
 85  | In einer Diskussion eine abweichende Meinung vertreten
 90  | Vor 30 Personen einen Vortrag halten
 95  | Spontan eine Rede halten (Toast, Tischrede)
```

### Modelo para preenchimento

```
MEINE ANGST-HIERARCHIE

Angstthema: [...]

SUDs | Situation
-----|--------------------------------------------------
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
```

---

## 4. Tipos de exposição

### Exposição graduada (In Vivo)

**Princípio:** Confronto gradual com situações reais, começando com valores SUDs baixos.

```
ABLAUF GRADUIERTER EXPOSITION:

1. Angst-Hierarchie erstellen (siehe oben)
2. Mit der leichtesten Situation beginnen (SUDs 20-30)
3. In der Situation BLEIBEN, bis die Angst nachlässt
   (mindestens 50% Reduktion oder SUDs < 25)
4. Übung mehrfach wiederholen, bis die Situation
   routinemäßig bewältigbar ist
5. Nächste Stufe der Hierarchie angehen
6. Weiter bis zur Spitze
```

### Flooding (Inundação)

**Princípio:** Confronto direto com situações que despertam forte ansiedade (valores SUDs altos) por um período prolongado.

```
FLOODING:

- Sehr wirksam, aber belastender als graduierte Exposition
- Nur unter therapeutischer Anleitung
- Voraussetzung: Gute therapeutische Beziehung und Vorbereitung
- Nicht bei unkontrollierbaren Panikattacken oder Dissoziation
- NICHT durch einen KI-Assistenten anleiten — nur erklären
```

### Exposição in sensu (na imaginação)

**Princípio:** Vivenciar situações que despertam ansiedade na imaginação.

```
EXPOSITION IN SENSU:

- Hilfreich als Vorbereitung auf reale Exposition
- Bei Situationen, die nicht leicht reproduzierbar sind
- Bei starker Vermeidung als Einstieg
- Ein KI-Assistent kann bei der Planung helfen, aber die Durchführung
  sollte therapeutisch begleitet sein
```

### Exposição interoceptiva

**Princípio:** Provocar deliberadamente sintomas corporais de ansiedade
(p. ex., taquicardia por movimento, tontura por rotação).

```
INTEROZEPTIVE EXPOSITION (bei Panikattacken):

- Durch Körperübungen: Hyperventilation, Strohhalm-Atmen,
  Kopfdrehen, Treppensteigen
- Ziel: Lernen, dass körperliche Symptome ungefährlich sind
- NUR unter therapeutischer Anleitung
```

---

## 5. Planejamento de exposição acompanhada

### Protocolo de preparação

```
EXPOSITIONS-PLANUNGSPROTOKOLL

Datum: [...]
Therapeut informiert: [ ] Ja  [ ] Nein (PFLICHT!)

Angstthema: [...]
Gewährte Situation: [...]
Erwarteter SUDs-Wert: [...]
Stufe in der Hierarchie: [...]

Was genau werde ich tun: [...]
Wo: [...]
Wann: [...]
Wie lange: [...]
Allein oder begleitet: [...]

Meine größte Befürchtung: [...]
Was realistisch passieren wird: [...]

Notfallplan (falls SUDs > 90 oder Dissoziation):
1. Grounding (5-4-3-2-1)
2. Atemübung (Box-Breathing)
3. [Vertrauensperson anrufen]: Tel. [...]
4. Situation ordentlich verlassen (kein panisches Flüchten)
```

### Protocolo de pós-processamento

```
EXPOSITIONS-NACHBEREITUNG

Datum: [...]
Situation: [...]

SUDs vorher (Erwartung): [...]
SUDs höchster Wert während: [...]
SUDs am Ende: [...]

Wie lange in der Situation geblieben: [...]
Habituation eingetreten: [ ] Ja  [ ] Teilweise  [ ] Nein

Was habe ich gelernt: [...]
War es so schlimm wie befürchtet: [ ] Schlimmer  [ ] Wie erwartet  [ ] Weniger schlimm

Was möchte ich beim nächsten Mal anders machen: [...]
Nächste Stufe: [...]
```

---

## 6. Notas de segurança e critérios de interrupção

### Pré-requisitos para a exposição

```
CHECKLISTE VOR EXPOSITIONSBEGINN:

[ ] Qualifizierter Therapeut ist einbezogen
[ ] Ausreichende Stabilisierung vorhanden
[ ] Angst-Hierarchie ist erstellt und besprochen
[ ] Notfallplan ist vorbereitet
[ ] Person versteht das Wirkprinzip (Habituation)
[ ] Keine akute Suizidalität
[ ] Keine unkontrollierte psychotische Symptomatik
[ ] Keine schwere dissoziative Störung (ohne therapeutische Begleitung)
[ ] Keine akute Substanzintoxikation
[ ] Person hat freiwillig zugestimmt (keine Zwangsexposition!)
```

### Critérios de interrupção

```
EXPOSITION ABBRECHEN, WENN:

- Dissoziation auftritt (Person "ist weg", reagiert nicht)
- Panikattacke mit Kontrollverlust
- Person will ausdrücklich abbrechen (Autonomie respektieren!)
- Körperliche Symptome: Brustschmerz, Atemnot, Ohnmacht
- Suizidgedanken während der Exposition
- Die Situation objektiv unsicher wird

BEI ABBRUCH:
1. Grounding und Stabilisierung (5-4-3-2-1, Atemübung)
2. Sicherstellen, dass die Person orientiert und stabil ist
3. Erfahrung besprechen (was ist passiert, was wurde gelernt)
4. Keinen Vorwurf machen ("Du hättest bleiben sollen")
5. Nächsten Schritt mit Therapeut planen
```

### Reconhecer comportamentos de segurança

```
SICHERHEITSVERHALTEN (Safety Behaviors):

Sicherheitsverhalten sind Strategien, die die Angst kurzfristig senken,
aber das Lernen verhindern:

| Sicherheitsverhalten | Problem |
|---------------------|---------|
| Ablenkung während Exposition | Verhindert volle Konfrontation |
| Handy griffbereit halten | "Ich habe es nur geschafft, weil..." |
| Begleitperson dabei | Lernt nicht, es allein zu schaffen |
| Beruhigungstablette vorher | Erfolg wird Tablette zugeschrieben |
| Nur kurz in Situation bleiben | Habituation hat keine Zeit |
| Fluchtweg im Kopf planen | Aufmerksamkeit nicht bei Erfahrung |

Ziel: Sicherheitsverhalten schrittweise reduzieren,
damit die volle Lernerfahrung möglich wird.
Aber: Nicht zu früh wegnehmen — in Absprache mit Therapeut.
```

---

## Ética e limites

**Um assistente de IA pode:**
- Explicar os princípios da exposição (psicoeducação)
- Criar em conjunto a hierarquia de ansiedade
- Explicar e usar a escala SUDs
- Apoiar o planejamento da exposição (preencher protocolos)
- Documentar o pós-processamento
- Dar orientações de segurança
- Motivar e normalizar ("a ansiedade durante a exposição é desejada e normal")

**Um assistente de IA NÃO pode:**
- Realizar ou conduzir a exposição por conta própria
- Conduzir flooding (SOMENTE terapeuta)
- Conduzir exposição interoceptiva (SOMENTE terapeuta)
- Realizar Exposição Prolongada no TEPT
- Acompanhar exposição em caso de dissociação grave
- Pressionar para a exposição ("você precisa enfrentar isso")
- Garantir resultados
- Fazer diagnósticos ou criar um plano terapêutico
- Dar recomendações relacionadas a medicamentos

**LIMITE ESPECIALMENTE RIGOROSO:** Um assistente de IA planeja e explica. A exposição real
ocorre sob orientação de um terapeuta qualificado. Em qualquer
pedido de execução: encaminhar a um profissional. Exposição sem
acompanhamento profissional pode retraumatizar ou intensificar a ansiedade.

**Em caso de sinais de crise aguda, SEMPRE encaminhar para:**
- Telefonseelsorge (linha de apoio emocional): 0800 111 0 111 / 0800 111 0 222
- Serviço psiquiátrico de emergência: 112
- Krisenchat: krisenchat.de

---

*Portado do BACH v3.8.0 | Versão standalone*
*Fontes: Foa & Kozak (1986), Craske et al. (2014), Bandelow et al. (2014), Diretriz S3 para transtornos de ansiedade (2014) — Não é terapia profissional*
