---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "Сводит сгруппированные открытые решения в ОДНУ связную, основанную на прозе общую концепцию на основе всех рекомендованных вариантов. Показывает, как подсистемы конкретно взаимодействуют после реализации, вместо того чтобы заставлять пользователя отвечать на десятки изолированных отдельных вопросов. Пользователь принимает картину в целом или даёт целенаправленные корректировки, которые автоматически переводятся в отдельные решения и записываются обратно в реестр через decision-briefing, фаза 4. Используй этот навык при запросах «как всё будет выглядеть, если мы со всем согласимся», «нарисуй мне общую картину», «общая концепция решений», «decision draw», /decision-draw, «как системы будут взаимодействовать». НЕ используй, если нужно обсудить альтернативы по каждому отдельному пункту, — это делает decision-briefing; НЕ используй для граф зависимостей — это делает decision-path; НЕ используй для структурированных отдельных блоков с вариантами и плюсами/минусами (в том числе для тесно связанных групп), — это делает decision-shot; НЕ используй для вывода отдельного решения — это делает decide."
visibility: public
language: ru
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: da661fa325502ab0dfae6d6655d70650457d6ac1ff27ca5f0ce6289c375ef2c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — Общая картина и приёмка сгруппированных решений

> Когда предстоят пять или десять решений, в мелочах вариантов легко потерять из виду
> складывающуюся систему. decision-draw описывает не альтернативы, а работающее целое:
> как системы взаимодействуют, если все рекомендации приняты? Пользователь принимает
> картину в целом или корректирует её точечно.

---

## Когда использовать

- Несколько связанных решений (из [decision-briefing](../decision-briefing/SKILL.md) или шаблона решений) не должны обрабатываться как вязкий каталог отдельных вопросов.
- Пользователь хочет до принятия решения увидеть, как компоненты будут реально взаимодействовать в повседневной работе после реализации.
- Из графа зависимостей ([decision-path](../decision-path/SKILL.md)) выделен пакет тесно связанных решений, который может быть принят как функциональное целое.
- Ключевые слова-триггеры: `/decision-draw`, «как всё будет выглядеть, если мы со всем согласимся», «нарисуй мне общую картину», «общая концепция решений», «decision draw», «как системы будут взаимодействовать после этого», «картина для общей приёмки».
- **Не** использовать:
  - Если пользователь хочет взвесить отдельные варианты по каждому вопросу и выбрать по букве (A/B/C) — это делает [decision-briefing](../decision-briefing/SKILL.md).
  - Для чистого анализа причинности и блокировок в терминале — это делает [decision-path](../decision-path/SKILL.md).
  - Для изолированного сравнения вариантов в пятичастных отдельных блоках (контекст, плюсы/минусы каждого варианта, рекомендация) для отдельных вопросов или тесно связанных групп — это делает [decision-shot](../decision-shot/SKILL.md).
  - Для методической проработки одного открытого принципиального вопроса — это делает [decide](../decide/SKILL.md).

---

## Разграничение в семействе решений

| Навык | UX и фокус | Отношение к вариантам | Форма приёмки |
|---|---|---|---|
| `decision-briefing` | **Разбивает** на отдельные вопросы | Показывает все варианты A/B/C/D | Коды-буквы (`1A 2C 3B`) |
| `decision-path` | **Структурирует** причинно-следственные связи | Оценивает варианты в графе | Диагностика в терминале (ASCII) |
| `decision-draw` | **Связная целевая картина** (объединяет связанные решения) | Описывает **только рекомендованный вариант** (альтернативы приведены ссылками) | Общая приёмка или корректирующая фраза |
| `decision-shot` | **Структурированные отдельные блоки** (для отдельных вопросов или тесных групп) | Показывает варианты с 2–4 плюсами/минусами | Executive Decision / отдельная приёмка |
| `decide` | **Прорабатывает** отдельный случай | Матрица оценки (критерии) | Аналитическая рекомендация |

> **Центральное правило:**
> `decision-draw` описывает **исключительно рекомендованный вариант**. Отвергнутые альтернативы никуда не делись — они задокументированы в [decision-briefing](../decision-briefing/SKILL.md), [decision-shot](../decision-shot/SKILL.md) или в связанных тикетах и указываются ссылкой в заголовке. Draw без этой ссылки лишил бы пользователя выбора, вместо того чтобы облегчить его.

---

## Обязательное правило стиля: пользовательские тексты без кодов и номеров

> **Каноническое указание пользователя (обратная связь 2026-09-13 / тикет T-20260913-883789445):**
> *«Decision draws мне слишком технические, это должно быть без номера, номера ты знаешь в фоне или используешь для написания текста […].»*

1. **Никаких технических кодов в видимом пользовательском тексте:**
   В видимом для человека тексте (пакет, концепция, взаимодействие, реализация, запрос) **не** должны встречаться внутренние коды (например `BH-A`, `MD-A`, `HA-A`, `PRA`), номера тикетов (`T-2026...`), номера D (`D-2026...`), относительные пути, хеши Git или измеренные значения.
2. **По 2–4 предложения обычным языком от первого лица на каждый пункт:**
   Каждый пункт пакета формулируется по схеме из трёх частей:
   - *Ситуация:* каков текущий исходный статус?
   - *«Я делаю …»:* что я конкретно планирую / какова моя рекомендация?
   - *Запасной вариант:* что произойдёт, если это не сработает, и что решает пользователь дальше?
   *(Пример: «Hermes поддерживает задачи только на английском. Я сообщаю об этом в Hermes как issue, а для нас делаю обходное решение. Сейчас есть старые сессии, которыми нельзя пользоваться. Я попробую сделать их снова пригодными. Если не получится, дам тебе случайную выборку из 10 сессий и кратко их опишу — так ты сможешь решить, стоит ли их спасать.»)*
3. **Понятные заголовки для ориентации:**
   Каждый пункт получает понятный русскоязычный заголовок (например, *«Бэкенд моделей как собственное ядро»*, *«Безопасные ключи деплоя на Mac»*). Пользователь взаимодействует через этот заголовок или даёт общую приёмку.
4. **Техническое соответствие только в приложении:**
   Сопоставление между понятным заголовком, внутренним кодом, ID тикета и состоянием реестра выполняется **исключительно в итоговой таблице приложения** в конце документа. Только там работают автоматические парсеры и обратная запись в реестр.

---

## Обязательная структура (восемь частей)

Полный `decision-draw` без исключений следует этой структуре:

### 1. Пакет и объём (обычным языком)
Обзор сгруппированных пунктов обычным языком (от первого лица, 2–4 предложения на пункт, без ID и кодов в тексте).

### 2. Концепция
Целевое состояние как связный текст прозой:
- Какой ландшафт систем или какой рабочий процесс возникает, если все рекомендации будут реализованы именно так?
- Никаких сопоставлений вариантов, никакого сослагательного наклонения рядом («можно было бы также»).
- Ясное, точное изъявительное наклонение: так система работает в целевом состоянии.

### 3. Взаимодействие
Функциональное ядро навыка:
- Как принятые части взаимодействуют **после** реализации в реальности?
- Предпочтительно изложение по конкретному сквозному сценарию, а не простой список компонентов.
- Делает наглядными потоки данных, интерфейсы и зоны ответственности.

### 4. Реализация
Конкретный порядок реализации:
- Что реально происходит на практике?
- Логика рёбер и зависимостей берётся напрямую из [decision-path](../decision-path/SKILL.md).
- Независимые рабочие потоки честно показываются как параллельные (не придумывать искусственных причинных цепочек; пакет может состоять из нескольких параллельных потоков). Порядок утверждается только там, где есть подтверждённые зависимости или сроки.
- Назвать шлюзы, шаги миграции и проверки.

### 5. Чего эта картина не охватывает
Защита от мнимой полноты:
- Какие краевые вопросы, открытые пункты или 🔴-уверенности намеренно исключены?
- Где проходят границы интерфейсов с соседними системами?
- Картина, которая умалчивает о своих границах, создаёт ложную уверенность.

### 6. Приёмка
Взаимодействие с пользователем:
- Пользователь проверяет картину в целом.
- Вариант ответа 1: **Явная общая приёмка** («Так подходит», «Принято», «Так и реализовать»). Только в этом случае все пункты пакета учитываются как принятые.
- Вариант ответа 2: **Корректировка через понятный заголовок или обычным языком** («При деплое на Mac лучше без автоматического перезапуска», «VersicherungsManager пока отложим»). Ведёт к разбивке на отдельные решения; все некорректированные пункты остаются открытыми.

### 7. Обратный перенос
Систематический перевод корректировок пользователя в отдельные решения:
- **Без автоматического зачисления:** только при явной общей приёмке неизменённые пункты засчитываются. Частичная корректировка — **не** общая приёмка!
- **Изоляция при корректировках:** если поступает корректировка, она разбивается на отдельные решения; все остальные пункты пакета строго остаются **открытыми** (в исходном реестре / шаблоне), пока пользователь не примет уточнённую картину целиком или не подтвердит оставшиеся пункты по отдельности.
- **Обязательная таблица обратного переноса:** каждый ответ с корректировкой обязательно порождает структурированную таблицу с четырьмя столбцами (исходная корректировка, затронутые коды, статус домино, открытые неоднозначности).
- **Исключительно путь записи через фазу 4:** `decision-draw` **не имеет** собственного пути записи в реестр. Запись выполняется **исключительно** по стандартной процедуре из [decision-briefing](../decision-briefing/SKILL.md), фаза 4.

### 8. Приложение: техническая справочная таблица (только для записи и аудита)
Компактная таблица в конце документа с:
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## Пример (пилотный фрагмент: Ticket-Master 2026-09-13 — BACH и системное объединение)

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## Правила на практике

1. **Без сослагательного наклонения в концепции:** описывай общую систему так, будто она уже реализована. Пользователь хочет ясности о результате, а не теоретических допущений.
2. **Причинность важнее хронологии:** порядок в разделе *Реализация* следует уровням графа зависимостей из [decision-path](../decision-path/SKILL.md). Независимые потоки честно показываются как параллельные и не сгибаются в искусственную причинную цепочку.
3. **Обязательная проверка домино при обратном переносе:** корректировку пользователя никогда нельзя записывать изолированно без проверки, не обесцениваются ли или не затрагиваются ли зависимые узлы графа.
4. **Никакого автоматического зачисления при частичных корректировках:** только при явной общей приёмке засчитываются неизменённые пункты. При каждой частичной корректировке все не затронутые пункты строго остаются открытыми, пока общая картина не будет повторно одобрена или пункты не будут подтверждены по отдельности.
5. **Исключительно путь записи через фазу 4:** `decision-draw` не имеет собственного пути записи в реестр. Записи выполняются без исключений через [decision-briefing](../decision-briefing/SKILL.md), фаза 4.
6. **Соблюдать контракты реестра:** записи всегда выполняются по правилам реестра решений (без перенумерации ID, уникальные коды записей, каноническая цель `DECIDED-AND-DONE.md`).
7. **Пользовательские тексты без технических номеров и кодов:** в видимом для человека тексте нет ID, кодов, путей или номеров тикетов. Каждый пункт формулируется понятным языком от первого лица; все обозначения переносятся в таблицу приложения.

---

## Происхождение сессии

Если decision draw сохраняется как постоянный концептуальный документ, он заканчивается так:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Приоритет источников: явная указанная во время выполнения/CLI информация, затем авторитетное окружение провайдера или хук, иначе `unbekannt`.
- Субагенты наследуют ID сессии родительской сессии.
- Чисто чатовые шаблоны штампа не получают.

---

## Журнал изменений

### 1.1.0 (2026-09-18)
- Правило стиля для понятных пользователю текстов решений закреплено (T-20260913-883789445, указание пользователя 2026-09-13):
  - Никаких технических кодов, номеров тикетов и D, путей или измеренных значений в видимом пользовательском тексте.
  - 2–4 предложения обычным языком от первого лица (ситуация, «Я делаю …», запасной вариант) на каждый пункт.
  - Понятные описательные заголовки для идентификации и приёмки.
  - Техническое соответствие (коды, ID тикетов, состояние реестра) строго перенесено в итоговую таблицу приложения (раздел 8).

### 1.0.1 (2026-09-13)
- Доработка после ревью:
  - Договор обратного переноса ужесточён: никакого автоматического зачисления при частичных корректировках; не затронутые пункты строго остаются открытыми до общей приёмки.
  - Введена обязательная таблица обратного переноса с 4 столбцами (исходная корректировка, затронутые коды, статус домино, открытые неоднозначности).
  - В примере показано множественное совпадение (одна корректировка пользователя одновременно затрагивает `MD-A` и `CF-A`).
  - Исключительный путь записи через фазу 4 `decision-briefing` закреплён в договоре и примере.
  - Ошибочное предположение о причинной цепочке в примере исправлено: независимые пункты честно показаны как четыре параллельных рабочих потока (вариант a).
  - Разграничение с `decision-shot` по формату вывода (структурированные отдельные блоки с плюсами/минусами против связной целевой картины с общей приёмкой) уточнено.

### 1.0.0 (2026-09-13)
- Первая редакция по пользовательскому заданию T-20260913-107991667.
- Семичастная обязательная структура (пакет, концепция, взаимодействие, реализация, границы, приёмка, обратный перенос).
- Логика группировки основана на `decision-path` и мосте обратной записи к `decision-briefing`, фаза 4.
