---
name: work-autonomous
version: 1.5.1
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-09
description: "स्वायत्त लूप के लिए समाप्ति शर्त: जहाँ तक संभव हो स्वतंत्र रूप से काम जारी रखें और कोई लूप तभी समाप्त करें जब यह प्रमाणित हो कि कोई स्वायत्त रूप से निष्पादन योग्य कार्य शेष नहीं है। केवल यह धारणा कि \"अब करने को कुछ नहीं बचा\", पर्याप्त नहीं है — यह एक चार-चरणीय जाँच-श्रृंखला (think/decide, _CONTROL/_DECISIONS, Gardener/USMC, decision-avatar/BYUM) आरंभ करती है, जिसे पहले नए कार्य प्राप्त करने होंगे, तभी लूप समाप्त हो सकता है। हर श्रृंखला-चरण एक बाइनरी परिणाम के बजाय found/empty/unavailable की रिपोर्ट देता है — \"exhausted\" तभी लागू होता है जब सभी स्रोत वास्तव में पूछे जा सके थे; यदि कम से कम एक स्रोत unavailable है, तो skill \"exhausted\" के बजाय \"blind\" रिपोर्ट करता है और कुछ भी अनजाँचा प्रमाणित नहीं करता। इस skill का उपयोग /work-autonomous, /waafap, \"arbeite autonom weiter bis nichts mehr zu tun ist\", एक /loop के भीतर Goal-शर्त के रूप में, या तब करें जब जाँचना हो कि लूप/सत्र समाप्त होने से पहले सचमुच कोई स्वायत्त कार्य शेष है या नहीं।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: hi
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
translated_at: "2026-10-16T11:58:01.178661+00:00"
---
<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — लूप तभी समाप्त करें जब प्रमाणित हो कि कोई स्वायत्त कार्य शेष नहीं है

## उद्देश्य

यह skill एक साथ दो काम करती है:

1. **जहाँ तक संभव हो स्वायत्त रूप से काम जारी रखना** — सामान्य सत्र-कार्य, कोई विशेष बात नहीं।
2. **लूप तभी समाप्त करना, जब यह सिद्ध हो** कि कोई स्वायत्त रूप से निष्पादन योग्य कार्य अब मौजूद नहीं है। "मुझे अभी कुछ करने को नहीं मिल रहा" का संदेह **कोई** समाप्ति-कारण नहीं है — यह उस जाँच-श्रृंखला का **ट्रिगर** है, जो पहले नए कार्य **प्राप्त** करने का प्रयास करती है। केवल जब यह श्रृंखला पूरी तरह परिणामहीन रहती है, तभी समाप्ति सिद्ध मानी जाती है।

**जानबूझकर किसी `/goal` के बिना:** यह skill स्वतंत्र रूप से उपयोग की जा सकती है (जैसे किसी सामान्य सत्र के भीतर सीधे `/work-autonomous`-कॉल के रूप में) और उसी प्रकार एक उच्च-स्तरीय loop-संरचना के भीतर शर्त के रूप में भी: `/loop` सामान्य रूप से देकर, केवल इस skill को Goal के रूप में नामित करें। तब Goal भावार्थ में यह होता है: *„Beende den Loop, wenn keine autonomen Aufgaben mehr vorliegen — und arbeite bis dahin so weit wie möglich autonom weiter."* skill स्वयं कोई `/goal`-संरचना नहीं चलाती; वह केवल वह स्पष्ट समाप्ति-संकेत देती है, जिसे ऐसी संरचना पढ़ सकती है (नीचे „Abbruchsignal" देखें)।

## संचालन-मॉडल — दो स्तर

### स्तर 1 — सामान्य कार्य (हर टिक)

#### TICKET-MASTER-Intake-Gate (इस स्तर में अन्य सब पर प्राथमिकता)

**केवल तभी प्रासंगिक, जब संदर्भ में कोई टिकट-प्रणाली (`_TICKETS/`) हो** — बिना टिकट-प्रणाली वाले सत्र इस gate को पूरी तरह छोड़ देते हैं; skill बिना किसी टिकट-प्रणाली के भी स्वतंत्र रूप से उपयोग योग्य रहती है (ऊपर „Zweck" देखें)। यदि ऐसा है, तो पहले जाँचें कि क्या `INBOX/` — जिनमें अनौपचारिक, अभी तक टिकट-प्रारूप में न लाई गई प्रविष्टियाँ भी शामिल हैं — पूरी तरह औपचारिक और ट्रायज़्ड हैं। यदि ऐसा नहीं है, तो यही स्थिति पाए गए स्वायत्त कार्य के रूप में गिनी जाती है (औपचारिक बनाना/ट्रायज़ करना उपयोगकर्ता-निर्णय के बिना क्लेरिकल कार्य है, नीचे की सीमांकन देखें) — उसे निपटाएँ, टिक समाप्त होता है, स्तर 2 में प्रवेश नहीं किया जाता, जैसे इस स्तर के किसी अन्य स्रोत में।

**जब तक INBOX खुला है, तब तक `NO_WORK`, कोई समाप्ति-संकेत (`exhausted`/`blind`), कोई Guard-STOP या कोई अन्य समाप्ति-संकेत उत्पन्न NICHT हो सकता।** केवल जब Intake पूरी तरह ट्रायज़ हो जाए, तभी `ACTIONABLE`, अनब्लॉक्ड `BLOCKED` और देय `WAITING` (नीचे) — और उसके बाद यदि आवश्यक हो तो स्तर 2 — जाँचे जा सकते हैं।

*उदाहरण-स्थिति:* `ACTIONABLE` निपटाने के बाद एक लूप ने समाप्ति-जाँच शुरू की, जबकि लगातार नए `INBOX`-टिकट आ रहे थे, जिनमें दो प्राथमिकता P1 के थे। इस gate के बिना लूप `exhausted`/`blind` रिपोर्ट कर देता, यद्यपि इनबॉक्स खुला था — ठीक यही gate रोकता है।

इसके बाद सामान्य रूप से स्वायत्त रूप से निष्पादन योग्य कार्य खोजें (नीचे की सीमांकन देखें) और उन्हें निपटाएँ: खुले `ACTIONABLE`-टिकट, अनब्लॉक्ड `BLOCKED`-टिकट, देय `WAITING`-टिकट, ऐसी परियोजनाओं में खुले `TODO.md`/`AUFGABEN.txt`-बिंदु जिनमें उपयोगकर्ता-निर्भरता नहीं है, स्थानीय नीति के अनुसार देय नियमित/स्वच्छता-जाँचें, पिछले सत्र से शुरू किया गया लेकिन पूरा न हुआ कार्य (USMC `working`), **सक्रिय परियोजना के देय `tidy-up`-रन** (परिशिष्ट 1.3.0, 2026-08-19 — skill `tidy-up` देखें: Tasksolver+Writer+Maintainer-पास उस परियोजना-फ़ोल्डर के लिए, जिसमें सत्र अभी काम कर रहा था; देयता `tidy-up` स्वयं अपने स्वतंत्र, हल्के USMC-लॉग से जाँचता है, देखें वहाँ का खंड „Verhältnis zu work-autonomous").

→ **मिला और निपटाया गया:** परिणाम संक्षेप में बताएँ, टिक समाप्त होता है, लूप सामान्य रूप से आगे चलता है। स्तर 2 में प्रवेश **नहीं** होता — जब तक दृश्य कार्य मौजूद है, चारों महंगी जाँच-चरणों की आवश्यकता नहीं।

### स्तर 2 — थकान-जाँच (केवल „अब करने को कुछ नहीं" के संदेह पर)

केवल तब जब स्तर 1 को अब कोई स्वायत्त कार्य नहीं मिलता, संदेह उत्पन्न होता है। यह संदेह अकेले पर्याप्त नहीं है। अब **अनिवार्य रूप से** नीचे की श्रृंखला चलती है, ताकि नए कार्य **प्राप्त** किए जा सकें।

#### आत्म-ज्ञान (श्रृंखला से पहले, उसके बाद नहीं)

किसी भी चीज़ से पूछने से पहले: skill घोषित करती है कि अपने निर्णय के लिए उसे कौन-से स्रोत चाहिए। चार आवश्यकताएँ (`grounding_seed.self_knowledge.Need`, यदि `grounding-seed` स्थापित है — अन्यथा वही सूची बिना लाइब्रेरी-संबंध की केवल घोषणा के रूप में मानी जाती है):

| भूमिका | श्रृंखला-चरण | इसके पीछे क्या है |
|---|---|---|
| `decisions.ledger` | 2 | केंद्रीय निर्णय-रजिस्टर |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide` (चरण 1) जानबूझकर कोई घोषित स्रोत Nहीं है।** यह मॉडल का अपना विश्लेषण चरण है, कोई बाहरी प्रणाली नहीं जो पहुँच योग्य या पहुँच से बाहर हो सकती है — इस भेद के अर्थ में यह हमेशा „उपलब्ध" है। केवल चरण 2–4 `unavailable` बन सकते हैं।

शुद्ध स्थान-निर्धारण प्रश्न (found/unavailable, अभी सामग्री-जाँच के बिना) के लिए वैकल्पिक, परीक्षण योग्य उपकरण: इस स्किल-फ़ोल्डर में `scripts/exhaustion_check.py`। यह `grounding_seed.resolve()` + `status_from_resolution()` का उपयोग `decisions.ledger`/`user.model` के लिए करता है (वहाँ एक वास्तविक `source-resolver`-प्रदाता मौजूद है), और `memory.organic`/`memory.curated` की जाँच **हमेशा** सीधे CLI-पहुँच (PATH पर `gardener`/`usmc`) से करता है — इन दो भूमिकाओं के लिए 2026-08-15 तक कोई पंजीकृत `source-resolver`-प्रदाता नहीं था; उन्हें रिज़ॉल्वर से पूछने पर केवल `unavailable` लौटता, चाहे Gardener/USMC वास्तव में स्थापित हों या नहीं। यह स्थापित `grounding-seed` के साथ और उसके बिना एक समान चलता है।

**अपडेट 2026-08-25 (K3=C, `T-20260825-342866657`):** अंतर बंद हो गया है — `source-resolver` अब `memory.organic` (Gardener) और `memory.curated` (USMC) दोनों को स्टेज-1-भूमिका के रूप में उसी CLI-उपस्थिति-जाँच (`shutil.which("gardener")`/`shutil.which("usmc")`) के साथ पंजीकृत करता है, जिसे यह स्क्रिप्ट अब तक स्वयं हार्डकोड करती थी। इसलिए `exhaustion_check.py` तुरंत नहीं बदला गया (कोई कार्यक्षमता-हानि नहीं, मौजूदा जाँच सही रहती है) — अगले स्किल-केयर-रन में चरण 3 को चरण 2 (`decisions.ledger`) की तरह `source_resolver.resolve("memory.organic"/"memory.curated")` पर बदला जा सकता है, ताकि CLI-जाँच दोहरी न रखनी पड़े।

#### चार शृंखला-चरण — प्रत्येक found | empty | unavailable रिपोर्ट करता है

हर चरण दो स्तरों में चलता है: पहले **स्थान-निर्धारण** (क्या मुझे कोई पहुँच योग्य स्थान पता है?), फिर — केवल स्थान मिलने पर — **सामग्री-जाँच** (मॉडल अपने उपकरणों से वास्तव में पढ़ता है कि वहाँ कुछ नया है या नहीं)। जिस स्रोत का स्थान नहीं मिल सका, उसकी सामग्री-जाँच कभी नहीं होती — वह `unavailable` गिना जाता है, `empty` नहीं।

1. **`/think` + `/decide`** को प्रश्न पर लागू करें: „क्या सचमुच अब कोई स्वायत्त रूप से निष्पादन योग्य कार्य नहीं बचा है, या मुझसे कुछ छूट रहा है?" — अनुमान के बजाय संरचित विश्लेषण। found/empty/unavailable-स्थिति नहीं (ऊपर देखें, कोई स्रोत नहीं)।
2. **`decisions.ledger`** — स्थान-निर्धारण `source_resolver.resolve("decisions.ledger")` / `grounding_seed.resolve(...)` के माध्यम से, यदि स्थापित हो; अन्यथा ज्ञात फ़ॉलबैक-पथ (`_control-center/_CONTROL/_DECISIONS/`, `TO-DECIDE-USER*.txt`-शृंखला, होस्ट-स्वयं की `TO-DECIDE-USER-<HOST>.txt`, `DECIDED-AND-DONE.md`)। स्थान मिला → सामग्री पढ़ें: क्या हाल में ऐसे निर्णय हुए हैं जो पहले अवरुद्ध या स्वीकृति की प्रतीक्षा कर रहे कार्य को अब खोल देते हैं? मिला → `found`। पढ़ा गया, कुछ नया नहीं → `empty`। स्थान नहीं मिला (रिज़ॉल्वर नहीं है और फ़ॉलबैक-पथ भी मौजूद नहीं) → `unavailable`।
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — दो अलग स्रोत, एक शृंखला-चरण। स्थान-निर्धारण: PATH पर CLI (`gardener`/`usmc`), ऊपर की स्व-जानकारी देखें। पहुँच योग्य → सामग्री पढ़ें (`find()`/`recall()` या `usmc facts|lessons|working|context`): खुले Working-Memory-बिंदु, अधूरे अनुवर्ती कार्य वाले Lessons, ऐसे तथ्य जो अनदेखे किंतु निष्पादन योग्य कार्य की ओर संकेत करते हैं (यही वह जगह है जहाँ पिछले सत्र अधूरे बिंदु छोड़ते हैं — `RESUME:`-फ़ील्ड, खुली `note`-प्रविष्टियाँ)। मिला → `found`। पढ़ा गया, कुछ नया नहीं → `empty`। PATH पर CLI नहीं → `unavailable`।
4. **`user.model` (decision-avatar/BYUM)** — स्थान-निर्धारण `decisions.ledger` जैसा (रिज़ॉल्वर या फ़ॉलबैक-पथ `_control-center/_CONTROL/_USER-MIND/`)। स्थान मिला → सामग्री जाँचें: क्या कोई पुष्ट पैटर्न है, जिसके अनुसार उपयोगकर्ता चाहता था कि इस स्थान पर कोई विशेष क्रिया स्वायत्त रूप से हो? केवल पर्याप्त विश्वास (🟢/🟡) पर `found` गिना जाता है — 🔴 को `empty` गिना जाता है, जीता हुआ कार्य नहीं, बल्कि नीचे „Nur-User-Rest" चरण के लिए खुला बिंदु। स्थान नहीं मिला → `unavailable`।

**„Exhausted" केवल तभी रिपोर्ट किया जा सकता है, जब सभी चारों स्रोत (चरण 2–4, तीन चरण, चार भूमिकाएँ) वास्तव में पूछे जा सके — यानी `found` या `empty`, एक भी `unavailable` नहीं।** यह `grounding_seed.self_knowledge.GroundingReport.all_answerable()` से मेल खाता है। यदि कम से कम एक भूमिका `unavailable` है, तो „exhausted" लागू नहीं होता, बल्कि अपना संकेत „blind" (नीचे Abbruchsignal देखें) होता है — लूप फिर भी समाप्त होता है (वह वैसे भी कुछ पूछ नहीं सकता), पर वह ऐसी जाँच का दावा नहीं करता जो वह कर नहीं सका।

यदि कोई चरण नया कार्य पाता है → वापस Ebene 1, कार्य करें, Guard-Zustand (नीचे देखें) को „exhausted"/„blind" के बजाय „found" पर सेट करें।

### विशेष मामला: केवल उपयोगकर्ता-बंधित अवशेष

यदि शृंखला **कोई स्वायत्त** कार्य नहीं पाती, पर `USER/*`-टिकट या अनिर्णीत `_DECISIONS`-बिंदु खुले हैं, तो यह फिर भी **स्वायत्तता के लिए STOP** है — पर „करने को कुछ नहीं" नहीं, बल्कि „स्वायत्त रूप से करने को कुछ नहीं"। ये बिंदु Autonomie-Loop-Regel के अनुसार `ticket-master` से **एकीकृत** प्रस्तुत किए जाते हैं (एक संग्रह-टेम्पलेट, अलग-अलग Einzel-Pings नहीं), अलग-अलग नहीं पूछे जाते। Abbruchsignal इस मामले को वास्तविक खालीपन से स्पष्ट रूप से अलग करता है।

## सीमांकन — „स्वायत्त रूप से निष्पादन योग्य" में क्या गिना जाता है?

संदर्भ: `ticket-master` श्रेणियाँ (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`)।

| फ़ॉल | स्वायत्त? | कारण |
|---|---|---|
| `INBOX/` सहित औपचारिक रूप से दर्ज न की गई प्रविष्टियाँ, TICKET-MASTER के अंतर्गत (ट्रायेज से पहले) | **हाँ, प्राथमिकता के साथ** | औपचारिकीकरण/ट्रायेज उपयोगकर्ता के निर्णय के बिना किया जाने वाला क्लेरिकल कार्य है — यह `ACTIONABLE`/`BLOCKED`/`WAITING` से पहले किया जाता है और तब तक किसी भी रुकावट-संकेत (ऊपर दिए Intake-Gate देखें) को अवरुद्ध करता है। |
| `ACTIONABLE`-टिकट | **हाँ** | कोई अवरोध नहीं, उपयोगकर्ता पर कोई निर्भरता नहीं — परिभाषा के अनुसार। |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | नहीं, जब तक अवरोध **अनुभवजन्य रूप से** समाप्त न हो गया हो | आवधिक पुनः-जाँच की अनुमति है (Autonomie-Loop), „उपस्थित है" प्रमाण के रूप में पर्याप्त नहीं — साक्ष्य आवश्यक है। |
| `WAITING/*` (scheduled, review-due, marker) समय/मार्कर से पहले | नहीं | समय-बद्ध। |
| `WAITING/*` समय/मार्कर आने के बाद | **हाँ** | शर्त पूरी हुई → `ACTIONABLE` में चला जाता है। |
| `USER/*` (decision, data, freigabe, hardware, session) | **कभी स्वायत्त नहीं** | अनिवार्य रूप से उपयोगकर्ता का निर्णय/डेटा/स्वीकृति/हार्डवेयर/सत्र। ऊपर बताए अनुसार एकत्रित करके प्रस्तुत करें। |
| `PARKED/*` (skip, backlog, until-trigger) | नहीं, जब तक स्पष्ट आदेश/ट्रिगर न हो | जानबूझकर स्थगित, कोई स्वचालित पुनः-जाँच नहीं। |
| `TODO.md`/`AUFGABEN.txt` के खुले बिंदु, बिना स्वीकृति-/निर्णय-नोट के | **हाँ** | परियोजना रजिस्टर, सामान्य कार्य। |
| देय नियमित/स्वच्छता-जाँच (Cooldown समाप्त, कोई Lock नहीं) | **हाँ** | स्थानीय नीति के अनुसार सामान्य रखरखाव कार्य। |
| `LOCK.user.*` द्वारा लॉक किए गए क्षेत्र | **कभी नहीं** | उपयोगकर्ता-Lock — केवल उपयोगकर्ता इसे हटा सकता है, देखें LOCK-SYSTEM। |
| नीति-स्वीकृति के बिना अपरिवर्तनीय/बाहरी रूप से प्रभावी चरण (Zenodo-Upload, संरक्षित/judged शाखाओं पर Push, Laptop-सीमा से परे Server-Spend निर्णय, पूर्वावलोकन के बिना स्थायी हटाना) | **नहीं** | स्वीकृति/निर्णय आवश्यक है, भले ही तकनीकी रूप से निष्पादन संभव हो। |
| केवल GUI/Login से शुरू होने वाला सत्र (जैसे Claude-Desktop-कार्य, इंटरैक्टिव लॉगिन, भौतिक हार्डवेयर-क्रिया) | **कभी नहीं** | „केवल उपयोगकर्ता द्वारा शुरू किया जाने वाला सत्र" — कोई Loop इसे नहीं संभाल सकता। |

मूल नियम: स्वायत्त वह है जो उपयोगकर्ता के निर्णय, स्वीकृति, डेटा, हार्डवेयर या सत्र के **बिना** पूरा किया जा सकता है और जिसके लिए कोई अपरिवर्तनीय या बाहरी रूप से प्रभावी कार्रवाई दस्तावेज़ीकृत नीति-स्वीकृति के बिना आवश्यक नहीं है।

## एंडलेस-लूप के विरुद्ध गार्ड (अनिवार्य)

**समस्या:** बिना किसी ब्रेक के चार-चरणीय श्रृंखला हर पुनः जाँच पर पूरी तरह फिर से चलेगी, भले ही पिछले परिणामहीन रन के बाद कुछ भी न बदला हो — महंगा और निरर्थक, विशेषकर जब Skill बार-बार बुलाया जाए (Loop, Scheduled Task, कुछ ही समय बाद दोबारा मैन्युअल कॉल)।

**स्थिति USMC में संग्रहीत होती है** (इस सिस्टम पर प्रक्रिया-स्थिति वहीं होनी चाहिए, Markdown-फ़ाइलों में नहीं):

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**फ़िंगरप्रिंट दो घटकों से बना है — स्थिति और उपलब्धता:**

1. **स्थिति-घटक** (पहले जैसा): खुले `ACTIONABLE`-टिकटों की संख्या/IDs, `_DECISIONS`-श्रृंखला का mtime (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), पिछली श्रृंखला-रन के बाद से नए USMC-`working`-प्रविष्टियों की संख्या।
2. **उपलब्धता-घटक (नया, संस्करण 1.2.0 से अनिवार्य):** Selbstkenntnis-जाँच (`exhaustion_check.availability_fingerprint_component()`) से अभी रिपोर्ट की गई `unavailable` भूमिकाओं का क्रमबद्ध tuple, उदाहरण के लिए `("memory.organic",)` या `()`।

**दूसरा घटक क्यों अनिवार्य है — „अन्यथा गार्ड अंतर विरासत में लेता है":** इसके बिना फ़िंगरप्रिंट (घटक 1) अन्य बातों के साथ `_DECISIONS`-श्रृंखला के mtime पर निर्भर करता है। यदि किसी सिस्टम पर यह श्रृंखला पूरी तरह अनुपस्थित है, तो फ़िंगरप्रिंट का यह भाग हमेशा के लिए स्थिर रहता है — एक बार गलत तरीके से सेट किया गया `exhausted`/`blind` फिर कभी दोबारा जाँचा नहीं जाएगा, भले ही बाद में `source-resolver` इंस्टॉल हो या `_control-center/_CONTROL/_DECISIONS/` बनाया जाए। उपलब्धता-घटक इसे सटीक रूप से ठीक करता है: बदलता है कि कौन-सी भूमिकाएँ unavailable हैं (कोई स्रोत जुड़ता है या हटता है), तो फ़िंगरप्रिंट अपने-आप बदल जाता है — गार्ड अगली कॉल पर इसे पहचानता है और श्रृंखला नए सिरे से चलाता है। यह Grounding-रूपक (T-20260815-371628859) के अर्थ में „Verpflanzung" है: परिवेश का बदलाव बिना किसी के गार्ड को मैन्युअल रीसेट किए नई खोज शुरू कर देता है।

**प्रत्येक श्रृंखला-रन से पहले का क्रम:**

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

एक एकल, पूरी तरह निष्पादित श्रृंखला-रन, जिसमें ALLE VIER Quellen befragbar waren और KEINE davon einen Treffer lieferte, „keine autonomen Aufgaben mehr" के लिए प्रमाण के रूप में पर्याप्त है (टिकट-निर्देश: „erst wenn ALLE Schritte eines Durchlaufs ergebnislos bleiben" — ergebnislos heißt hier ausdrücklich `empty`, nicht `unavailable`)। गार्ड स्वयं के निष्कर्ष को नहीं रोकता, बल्कि केवल **बार-बार, अपरिवर्तित पुनः-निष्कर्ष** को रोकता है, घने अनुवर्ती कॉल पर — और यह `exhausted` UND für `blind` अलग-अलग होता है, कभी आपस में नहीं मिलाया जाता।

`GUARD_INTERVAL` कॉन्फ़िगर योग्य है (डिफ़ॉल्ट 15 मिनट) — बहुत धीमे परिवेश में (कम नए टिकट/निर्णय) लंबा मान चुना जा सकता है, बहुत सक्रिय परिवेश में छोटा।

## Abbruchsignal (रुकने का संकेत)

हर रन **एक** स्पष्ट, grep-योग्य पंक्ति पर समाप्त होता है, ताकि कोई आसपास का `/loop` या भविष्य का `/goal`-निर्माण इससे पढ़ सके कि आगे बढ़ना है या नहीं:

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE` एकमात्र संकेत है जिस पर कोई उच्च-स्तरीय लूप एक और टिक शुरू करे। सभी `STOP`-रूप सत्यापित रुकावट हैं — कारण सहित कि कौन-सा मामला लागू है।

`exhausted` और `blind` के बीच का अंतर उपयोगकर्ता के लिए महत्वपूर्ण है, केवल सजावटी नहीं:
`exhausted` का अर्थ है „मैंने वह सब जाँच लिया है जिसे जाँचना था — काम पूरा हो गया है"। `blind` का अर्थ है
„मेरे पास जाँच करने के लिए बुनियादी ढाँचा ही नहीं है — यह कोई कार्य-स्थिति नहीं, बल्कि एक कमी है"।
एक `/loop`/`/goal`-संरचना, जो दोनों को एक जैसा मानती है (लूप दोनों स्थितियों में समाप्त हो जाता है), उन्हें उपयोगकर्ता को एक जैसा रिपोर्ट नहीं करनी चाहिए — अन्यथा ठीक वही जानकारी खो जाती है, जिसकी माँग T-20260815-205101335 ने की थी।

## अन्य Skills से संबंध

- **`think`/`decide`** — श्रृंखला-चरण 1 में संरचित विश्लेषण/निर्णय उपलब्ध कराते हैं। इन्हें यहाँ एक घटक के रूप में बुलाया जाता है, दोबारा नहीं बनाया जाता।
- **`decision-avatar`** (यह Skill, उपयोगकर्ता-निरपेक्ष) — श्रृंखला-चरण 4 उपलब्ध कराता है। उन सिस्टमों पर जिनमें कोई ठोस, अधिकृत प्रोफ़ाइल है, यह `user-model` + `build-your-users-mind` के अनुरूप होता है।
- **`orchestrator`** — नियंत्रित करता है कि Subagents को कैसे सौंपा जाए और उनकी पूर्णता-सूचना कैसे जाँची जाए। `work-autonomous` नियंत्रित करता है कि खोज कब पूरी तरह रोकी जाए; दोनों संयोज्य हैं (ऑर्केस्ट्रेटर स्तर 1 में पूरे किए गए कार्य के हिस्से के रूप में प्रकट हो सकता है)।
- **`bugsweep`** — एक अन्य, स्वयं-सीमित खोज-प्रोटोकॉल का उदाहरण (चार-चरणीय श्रृंखला के बजाय दोगुनी-वृद्धि वाली एस्केलेशन)। `work-autonomous` अधिक सामान्य है: यह केवल कोड में बग नहीं जाँचता, बल्कि स्वायत्त कार्य के हर स्रोत की जाँच करता है।
- **Ticket-Kategorien (`ticket-master`)** — „स्वायत्त रूप से निष्पादन योग्य" के लिए शब्दावली (देखें पृथक्करण-तालिका) और स्वायत्तता-लूप के लिए ढाँचा प्रदान करते हैं (BLOCKED-पुनर्जाँच, USER-समूहन, WAITING-समय-खींचना, PARKED-ठहराव)।
- **`tidy-up`** (1.3.0 से) — स्तर 1 का एक अतिरिक्त स्रोत प्रदान करता है: वर्तमान में संसाधित प्रोजेक्ट-फ़ोल्डर के लिए एक बार का Tasksolver+Writer+Maintainer-पास। यह अपनी नियत तिथि स्वयं जाँचता है (हल्का USMC-लॉग, यहाँ जैसा चार-चरणीय Guard नहीं) — `work-autonomous` इसे कई स्तर-1 स्रोतों में से केवल एक के रूप में बुलाता है, बिना इसके तर्क को दोहराए।

## उदाहरण-प्रवाह

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


## Changelog

### 1.5.1 (2026-09-09)
- T-20260909-282509082: `decisions.ledger` और `user.model` के लिए दस्तावेज़ीकृत फ़ॉलबैक, सिद्ध Control-Center-स्थानांतरण के बाद `_CONTROL/_DECISIONS` और `_CONTROL/_USER-MIND` की ओर चलता है। Resolver-प्राथमिकता और fail-closed व्यवहार अपरिवर्तित रहते हैं।

### 1.5.0 (2026-09-09)
- P-018: नए बनाए गए और स्थायी रूप से सहेजे गए महत्वपूर्ण कार्य-रिपोर्ट, Handoffs और Receipts `session: <session-id> | <agent>@<host> | YYYY-MM-DD` के साथ समाप्त होते हैं। स्रोत-प्राथमिकता है: स्पष्ट रनटाइम-/CLI-मान, फिर अधिकृत Provider-Umgebung/Hook, फिर `unbekannt`; मान कभी अनुमानित नहीं किए जाते, Subagents मूल-Session का उपयोग करते हैं। Routine-Chat, Quellen, Policies, `CLAUDE.md`, READMEs और पुरानी फ़ाइलें सामान्य या पूर्वव्यापी स्टैम्पिंग से बाहर रहती हैं।

### 1.4.0 (2026-09-03)
- Ticket T-20260902-729068782 से न्यूनतम-आक्रामक जोड़: स्तर 1 में नया **TICKET-MASTER-Intake-Gate** (`ACTIONABLE`/`BLOCKED`/`WAITING` से पहले प्राथमिकता) — केवल तब प्रासंगिक जब कोई Ticketsystem संदर्भ का हिस्सा हो। जब तक `INBOX/` (औपचारिक प्रविष्टियों सहित) पूरी तरह triagiert नहीं है, कोई `NO_WORK`/Erschöpfungssignal/Guard-STOP उत्पन्न नहीं होना चाहिए। उदाहरण-मामला: एक लूप ने `INBOX` में खुली प्रविष्टियाँ (जिनमें दो P1-Tickets शामिल थे) रहते हुए थकावट-जाँच शुरू कर दी। मौजूदा चार-चरणीय थकावट-श्रृंखला, Guard और गैर-TICKET-MASTER उपयोगिता अपरिवर्तित रहते हैं — यह Gate केवल स्तर 1 में और केवल TICKET-MASTER के अंतर्गत कार्य करता है।
- नया, परीक्षित सहायक-फ़ंक्शन `scripts/exhaustion_check.py::intake_gate_blocks_stop()` + `tests/test_exhaustion_check.py` में回归-परीक्षण (व्यवहार-आधारित: खुले INBOX पर Gate रोकता है, खाली INBOX पर छोड़ता है)।

### 1.3.0 (2026-08-19)
- Ticket T-20260819-461890468 से न्यूनतम-आक्रामक जोड़ (नया Skill `tidy-up`): स्तर 1 को एक अतिरिक्त, स्वतंत्र स्रोत मिलता है — „सक्रिय प्रोजेक्ट की नियत `tidy-up`-रनें" (Tasksolver+Writer+Maintainer-पास, देखें Skill `tidy-up`)। कोई नया श्रृंखला-चरण नहीं, स्तर 2/Guard/Abbruchsignal में कोई बदलाव नहीं — `tidy-up` अपनी नियत तिथि स्वयं एक हल्के USMC-लॉग के माध्यम से जाँचता है और यहाँ केवल एक और स्तर-1 स्रोत के रूप में संदर्भित है, पहले से मौजूद स्रोतों (Tickets, TODO/AUFGABEN, Routine-Checks, USMC `working`) के समान। इस प्रकार `tidy-up`-बिंदु उस `/goal`-संरचना के अर्थ में स्वायत्त रूप से निष्पादित किए जाने योग्य कार्य गिने जाते हैं, जो `/work-autonomous` + `/tidy-up` को जोड़ती है (Ticket का मुख्य उपयोग-मामला)। चार-चरणीय थकावट-श्रृंखला या Guard में कोई हस्तक्षेप नहीं — स्तर 2 अपरिवर्तित रहता है।

### 1.2.0 (2026-08-15)
- टिकट T-20260815-205101335 से रेट्रोफ़िट (जाँच-कार्य: „जाँचें कि ग्राउंडिंग-मेटाफ़ोर के संदर्भ में समाधान वहाँ टिकता है या नहीं", निष्कर्ष प्रकाशित Skill पर: यह तीन बिंदुओं पर टिका, लेकिन „पूछा गया और खाली" बनाम „पूछा ही नहीं जा सका" के भेद पर नहीं टिका — श्रृंखला `STOP (exhausted)` की रिपोर्ट करती थी, भले ही Gardener/USMC/`_DECISIONS` मौजूद न हों, और इसकी कभी जाँच नहीं हुई थी। `grounding-seed` का पहला वास्तविक उपयोग-मामला, टिकट T-20260815-371628859)।
- **स्व-ज्ञान जोड़ा गया:** श्रृंखला से पहले चार घोषित आवश्यकताएँ (`decisions.ledger`, `memory.organic`, `memory.curated`, `user.model`), ताकि चार निश्चित नामों वाले स्थानों पर अंधाधुंध न खोजा जाए।
- **प्रत्येक श्रृंखला-चरण (2–4) द्विआधारी परिणाम के बजाय found | empty | unavailable रिपोर्ट करता है** — दो स्तरों में: पहले स्थान-निर्धारण (`grounding-seed`/`source-resolver` के लिए `decisions.ledger`/ `user.model`, `memory.organic`/`memory.curated` के लिए सीधी CLI-जाँच, जिनके पास अभी तक `source-resolver`-प्रदाता नहीं है), और सामग्री-जाँच केवल सफल स्थान-निर्धारण के बाद।
- **`exhausted` अब तभी लागू होता है जब चारों स्रोत वास्तव में पूछे जा सकते थे** (सभी found/empty, कोई unavailable नहीं)। यदि कम से कम एक स्रोत अप्राप्य था, तो एक नया, अलग पहचाना जाने वाला संकेत `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)` है — लूप फिर भी समाप्त होता है, पर वह अब कोई जाँचा हुआ परिणाम होने का दावा नहीं करता।
- **Guard-Fingerprint में उपलब्धता-खंड जोड़ा गया** (अभी unavailable भूमिकाओं का क्रमबद्ध टपल)। यह अनुवर्ती निष्कर्ष „Guard विरासत में लेता है खामी" को ठीक करता है: इस खंड के बिना, एक बार गलती से सेट हुआ `exhausted`/`blind` हमेशा वैध रहता है, यदि `_DECISIONS`-श्रृंखला पूरी तरह गायब हो (तब पुराना fingerprint-हिस्सा स्थिर रहता है)। इस खंड के साथ, फिर से उपलब्ध हुआ स्रोत स्वचालित रूप से श्रृंखला का नया दौर चलाता है (ग्राउंडिंग-मेटाफ़ोर के अर्थ में प्रत्यारोपण)।
- नई, परीक्षित सहायक स्क्रिप्ट `scripts/exhaustion_check.py` (+ `tests/test_exhaustion_check.py`, 11 परीक्षण, दोनों संचालन-प्रकार जाँचे गए: `grounding-seed` स्थापित होने के साथ और उसके बिना) — स्व-ज्ञान/स्थान-निर्धारण की जाँच नियतात्मक रूप से देती है, ताकि Skill इसे हर चलने पर फिर से अनुमान न लगाए। यह वैकल्पिक रहती है: Skill अब भी मुख्यतः एक प्रोटोकॉल है, जिसे कोई मॉडल अपने स्वयं के उपकरणों से पालन करता है।
- निर्भरता: `grounding_seed.self_knowledge.assess()`/`status_from_resolution()`, `grounding-seed` 0.2.0 से — पुराने `grounding-seed`-संस्करणों (0.1.0) में एक श्रेणी-त्रुटि थी (`not_found` को गलती से `empty` माना गया था), जो ठीक यहाँ सुधारे गए भेद को फिर से धुंधला कर देती। `grounding-seed` स्थापित न होने पर दस्तावेज़ीकृत विकल्प समान रूप से चलता है।

### 1.1.0 (2026-08-15)
- संदर्भ-रेट्रोफ़िट टिकट T-20260815-385400870 से: चरण 2 (निर्णय-रजिस्टर) अब अपना स्थान भूमिका `decisions.ledger` के माध्यम से हल करता है (`source_resolver.resolve(...)`, मॉड्यूल `source-resolver`), इसे कठोर रूप से जोड़ने के बजाय — यदि resolver स्थापित नहीं है तो दस्तावेज़ीकृत विकल्प के रूप में पिछले पथ पर वापस जाता है। कार्यात्मक व्यवहार अपरिवर्तित।

### 1.0.0 (2026-08-15)
- टिकट T-20260815-522639345 से प्रारंभिक संस्करण: दो-स्तरीय संचालन-मॉडल, चार-चरणीय जाँच-श्रृंखला, `ticket-master`-श्रेणियों के अनुसार सीमांकन-तालिका, अनंत लूप के विरुद्ध USMC-समर्थित Guard, और `/loop`/`/goal`-निर्माणों के लिए स्पष्ट निरस्तीकरण-संकेत।
