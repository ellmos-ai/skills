---
name: github-repo-care
version: 1.3.1
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-09-27
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: "GitHub रिपॉज़िटरी को सुरक्षित रूप से बनाने, प्रकाशित करने, रिलीज़ करने, ऑडिट करने और रखरखाव करने का प्रोटोकॉल: स्थानीय नियम और लॉक जाँचें, पहले add से पहले .gitignore बनाएँ, privacy जाँच चलाएँ, README/i18n/banner/metadata तैयार करें, release tags और GitHub releases सत्यापित करें, तथा organization profiles, llms.txt फ़ाइलों और registry links को अपडेट करें।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: hi
status: active
visibility: public
dependencies: {'tools': ['git', 'gh', 'rg'], 'services': ['GitHub'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.codex/skills/github-repo-care/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': '2026-06-18', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 9a4401a2244a88c6989c3a69114c9292c405e28fe3d018cd6f832f4c5bd6c1d1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="github-repo-care banner">

# GitHub Repo Care — रिपॉज़िटरी को सुरक्षित रूप से प्रकाशित और रखरखाव करना

## यह Skill कब लागू होता है

इस Skill का उपयोग करें जब कोई GitHub रिपॉज़िटरी नया बनाना, प्रकाशित करना, रिलीज़ करना, ऑडिट करना या बाद में उसका रखरखाव करना हो। यह पहले सार्वजनिक push से पहले, release tags के समय, रिपॉज़िटरी metadata में बदलाव के समय, organization profiles के लिए और Privacy-जाँच के लिए विशेष रूप से महत्वपूर्ण है।

यह शुद्ध कोड-कार्यान्वयन के लिए लागू नहीं होता, जिसमें GitHub पर प्रकाशन शामिल न हो। ऐसी स्थिति में पहले उपयुक्त development या debugging Skill का उपयोग करें और इस Skill को केवल प्रकाशन चरण पर सक्रिय करें।

## मुख्य नियम

पहले सार्वजनिक push से पहले रिपॉज़िटरी तैयार करें। एक सही `.gitignore`, एक साफ़ Privacy-Gate, लाइसेंस, README, metadata और release की कहानी सार्वजनिक इतिहास बनने से पहले कहीं आसान होती है, बाद की तुलना में।

## प्रक्रिया

1. **स्थानीय नियम पढ़ें।** `AGENTS.md`, `CLAUDE.md`, `START.md`, Release-नीति, नामकरण-नीति और Lock-नीति की जाँच करें, यदि वे मौजूद हों।
2. **लॉक जाँचें।** यदि `LOCK.txt` या कोई उपयुक्त `LOCK.*.txt` सक्रिय है, तो इस दायरे को न बदलें।
3. **रिपॉज़िटरी का नाम तय करें।** नाम, organization, दृश्यता, लाइसेंस और उद्देश्य को एक वाक्य में लिखें।
4. **`.gitignore` को `git add` से पहले बनाएँ।** Secrets, स्थानीय डेटा, databases, build outputs, virtual environments, caches, IDE फ़ाइलें और निजी नोट्स बाहर रखें।
5. **Public-बेसिक्स जोड़ें।** आम तौर पर: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `llms.txt` और CI।
6. **README को खोज के लिए लिखें।** पहली स्क्रीन की ऊँचाई में: उद्देश्य, इंस्टॉलेशन, उपयोग, Privacy-मॉडल, प्रोजेक्ट संरचना, लाइसेंस और कैनोनिकल रिपॉज़िटरी नाम।
7. **दृश्य संकेत लगाएँ।** Banner, logo या screenshot तब जोड़ें जब वे लाभ को अधिक पहचानने योग्य बनाएँ। जब कोई वास्तविक उत्पाद-चित्र या स्पष्ट अवधारणा-चित्र संभव हो, तब सामान्य सजावट न करें।
8. **बहुभाषिकता की योजना सोच-समझकर बनाएँ।** न्यूनतम: अंग्रेज़ी और प्रोजेक्ट की भाषा। उपयोगकर्ता-उन्मुख मॉड्यूल के लिए वरीयता: जर्मन, अंग्रेज़ी, स्पेनिश, सरलीकृत चीनी, जापानी और रूसी।
9. **Tests और smokes चलाएँ।** सफलता का दावा करने या release बनाने से पहले स्थानीय रूप से सत्यापन करें।
10. **Privacy-Gate चलाएँ।** Staged/tracked सेट की जाँच करें: Secrets, स्थानीय paths, PII, `.env`, databases, निजी दस्तावेज़, जनित artefacts और Mojibake।
11. **Commit और push करें।** केवल पास हुए gate के बाद commit करें। फिर GitHub रिपॉज़िटरी बनाएँ या जोड़ें, push करें और remote स्थिति जाँचें।
12. **Metadata सेट करें।** विवरण, Topics, Homepage, दृश्यता और ब्रांच-डिफ़ॉल्ट जाँचें।
13. **Release बनाएँ।** Tag और GitHub release बनाएँ; ब्रांच और tag दोनों के लिए CI जाँचें।
14. **Discovery सतहें अपडेट करें।** Organization profile, `llms.txt`, केंद्रीय registries, स्थानीय मॉड्यूल सूचकांक और ecosystem READMEs को लिंक करें। **Publish ⇒ प्रोफ़ाइल पेज (T-20260926-796851315):** यदि रिपॉज़िटरी में banner है, तो यंत्रवत जाँचें कि वह organization profile पेज (`<org>/.github/profile/README.md`) पर पहले से दिखता है या नहीं — `python org_profile_gate.py --org <org>` (`.AI/.SKILLS/testing/`)। यदि प्रविष्टि नहीं है, तो स्क्रिप्ट डालने के लिए तैयार Markdown snippet देती है।
    **अपना स्टार सेट करना (T-20260926-299328659):** Aftercare हर अपने सार्वजनिक रिपॉज़िटरी के लिए जाँचता है कि क्या खाते ने स्वयं पहले से स्टार दिया है, और यदि नहीं, तो उसे सेट करता है — अपने GitHub-रखरखाव टूल के माध्यम से, यदि उपलब्ध हो (path और कॉल स्थानीय config से, उदाहरण के लिए `--self-star` flag: बिना रिपॉज़िटरी निर्दिष्ट किए सभी कॉन्फ़िगर की गई organizations पर एक catch-up रन, रिपॉज़िटरी निर्दिष्ट करने पर इस publish के ठीक बाद एकल रन)। कभी स्वचालित रूप से अनस्टार न करें।
    **Stargazer-रखरखाव:** नए Stargazers को फ़ॉलो करें और वास्तविक गुणवत्ता होने पर उनके सबसे अच्छे प्रोजेक्ट को बदले में स्टार करें — यदि आपके GitHub-रखरखाव टूल में पहले से पारस्परिकता-मॉड्यूल है, तो उसका उपयोग करें (यह विषयगत प्रासंगिकता का मूल्यांकन करता है और बदले में स्टार करने/आमंत्रित करने/जाँचने/छोड़ने का सुझाव देता है; फ़ॉलो करना Rate-Caps, Cooldown और Dry-run/Apply/Confirm सुरक्षा-जाल के साथ चलाता है)। यदि यह पहले से मौजूद है तो नया न बनाएँ; निर्णयों का लॉग मॉड्यूल स्वयं रखता है। कभी स्वचालित रूप से अनफ़ॉलो या अनस्टार न करें।
15. **समापन जाँच करें।** Remote README, release पेज, Topics, CI और लिंक जाँचें।

## Privacy-Gate

खोज staged या tracked सेट में करें, केवल दिखने वाले working tree में नहीं।

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

सार्वजनिक मॉड्यूलों के लिए अतिरिक्त रूप से `RELEASE_GATE.md` या समकक्ष gate दस्तावेज़ित करें: तारीख, जाँचे गए कमांड, परिणाम, शेष चेतावनियाँ और जानबूझकर किए गए अपवाद। यदि कोई Secret कभी committed हुआ हो, तो `HEAD` से उसे हटाना पर्याप्त नहीं है; Secret को rotate करना होगा।

**लिंक किए गए रिपॉज़िटरी की दृश्यता जाँचें।** Path/Token scan निजी GitHub रिपॉज़िटरी के लिंक को सार्वजनिक READMEs में नहीं ढूँढता
(केस स्टडी T-20260926-820252321: `ellmos-ai/ellmos-core` बिना ध्यान दिए एक
README तालिका में था, जबकि रिपॉज़िटरी निजी है)। यदि यह रिपॉज़िटरी में उपलब्ध हो, तो पुन: उपयोग योग्य जाँच चलाएँ:

```bash
python testing/repo_link_visibility_gate.py --repo .
```

यह जाँच केवल वास्तविक अनिश्चितता (नेटवर्क विफलता, Rate-Limit 403/429 — केवल एक संकेत, कोई रुकावट नहीं) पर fail-open है; 404 उसी तरह ब्लॉक करता है जैसे पुष्टि किया गया `private: true`, क्योंकि दोनों का अर्थ है कि लिंक बाहरी लोगों के लिए हल नहीं हो सकता (निजी है या मौजूद ही नहीं है)। यदि यह script उपलब्ध नहीं है (रिपॉज़िटरी के पास जाँच की अपनी प्रति नहीं है), तो `gh api repos/ORG/REPO --jq .private` से README में लिंक किए गए हर बाहरी या सहोदर रिपॉज़िटरी-लिंक का नमूना-आधारित जाँच करें।

## GitHub Metadata

Push के बाद metadata और release स्पष्ट रूप से सेट करें।

```bash
gh repo edit ORG/REPO --description "Kurze konkrete Beschreibung" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

इसके बाद सत्यापित करें:

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

यदि release के बाद CI लाल है, तो रिपॉज़िटरी को अभी साफ़ तरीके से प्रकाशित नहीं माना जाता। किसी अभी बनाए गए प्रारंभिक release में, नए tag को तुरंत और जानबूझकर सुधारे गए commit पर ले जाना स्वीकार्य है।

## सामान्य गलतियाँ

| त्रुटि | सुधार |
|---|---|
| `.gitignore`, `git add` के बाद बनाया जाता है | पहले unstage करें, ignore नियम सुधारें, फिर दोबारा add करें |
| README एकभाषी है, जबकि UI या Skill बहुभाषी है | भाषा-लिंक या स्थानीयकृत READMEs जोड़ें |
| कोई banner नहीं, कोई Topics नहीं, कोई विवरण नहीं | घोषणा से पहले Discovery assets जोड़ें |
| Release tag मौजूद है, लेकिन CI लाल है | CI ठीक करें और नया run जाँचें |
| Organization README अपडेट किया, लेकिन `llms.txt` भूल गए | मानव-पठनीय और मशीन-पठनीय दोनों सतहें अपडेट करें |
| स्थानीय path सार्वजनिक दस्तावेज़ में है | उसे relative paths या सामान्य उदाहरणों से बदलें |
| Public रिपॉज़िटरी में test database या notebook inbox है | फ़ाइल को tracking से हटाएँ, ignore नियम जोड़ें, gate फिर से चलाएँ |

## समापन चेकलिस्ट

- [ ] स्थानीय नियम और लॉक जाँचे गए।
- [ ] `.gitignore` पहले add से पहले मौजूद था।
- [ ] Public दस्तावेज़, लाइसेंस, Security, Contributing, Changelog और `llms.txt` मौजूद हैं।
- [ ] README में रिपॉज़िटरी नाम, उद्देश्य, इंस्टॉलेशन, उपयोग, Privacy और लाइसेंस है।
- [ ] i18n अपेक्षा पूरी हुई।
- [ ] उपयुक्त होने पर banner, logo या screenshot मौजूद है।
- [ ] Tests और smokes पास हुए।
- [ ] Privacy-, path-, secret-, database- और Mojibake-scans साफ़ हैं।
- [ ] GitHub विवरण, Topics, tag, release और CI सत्यापित।
- [ ] Organization profile, registry और ecosystem links अपडेट।
- [ ] बैनर मौजूद है? `org_profile_gate.py --org <org>` इस रिपॉज़िटरी के लिए बिना किसी निष्कर्ष के चला।

## Changelog

### 1.3.1 (2026-09-27)
- Doku-Fix: Privacy-Gate विवरण में 404 की अर्थ-व्याख्या गलत थी। `testing/repo_link_visibility_gate.py` के अनुसार 404 (निजी या मौजूद नहीं) उसी तरह ब्लॉक करता है जैसे पुष्टि किया गया `private: true`; fail-open केवल नेटवर्क विफलता और Rate-Limit (403/429) पर लागू होता है। Privacy-Gate अनुभाग और 1.2.0 changelog प्रविष्टि में सुधार किया गया।

### 1.3.0 (2026-09-27)
- चरण 14 विस्तारित (T-20260926-299328659, उपयोगकर्ता का अनुरोध): अपने सार्वजनिक रिपॉज़िटरी पर अपना स्टार जाँचना/सेट करना तथा Stargazer-रखरखाव (फ़ॉलो करना + गुणवत्ता-आधारित बदले में स्टार करना), अपने GitHub-रखरखाव टूल के माध्यम से, यदि उपलब्ध हो — कोई विशेष टूल अनिवार्य नहीं। कभी स्वचालित रूप से अनफ़ॉलो/अनस्टार नहीं।

### 1.2.0 (2026-09-26)
- नया Privacy-Gate चरण (T-20260926-820252321): लिंक किए गए GitHub रिपॉज़िटरी की दृश्यता जाँचें (`testing/repo_link_visibility_gate.py --repo .`, नेटवर्क/Rate-Limit पर fail-open, 404 और पुष्टि किए गए `private: true` पर ब्लॉक)। कारण: `ellmos-ai/ellmos-core` (निजी रिपॉज़िटरी) बिना ध्यान दिए एक README तालिका में था।

### 1.1.0 (2026-09-26)
- "Publish ⇒ प्रोफ़ाइल पेज" चरण जोड़ा गया (T-20260926-796851315): banner वाले रिपॉज़िटरी की जाँच उसकी organization की profile README (`<org>/.github/profile/README.md`) से यंत्रवत रूप से `.AI/.SKILLS/testing/org_profile_gate.py` के माध्यम से की जानी चाहिए, स्मृति पर नहीं छोड़ी जानी चाहिए। कारण: zombie-killer-tray का banner प्रकाशन के बाद dev-bricks organization पेज पर कभी नहीं पहुँचा।

### 1.0.0 (2026-06-18)
- रिपॉज़िटरी-रखरखाव और प्रकाशन प्रोटोकॉल के रूप में प्रारंभिक संस्करण बनाया गया।
