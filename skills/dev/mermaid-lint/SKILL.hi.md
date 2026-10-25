---
name: mermaid-lint
version: 1.0.0
type: tool
author: Lukas Geiger + Claude
created: 2026-09-20
updated: 2026-09-20
aliases: [mermaid, mermaid-fehler, diagramm-render-fehler, unable-to-render-rich-display, schaltplan-fehler]
description: "GitHub पर रेंडर न होने वाले Mermaid आरेखों को खोजता और ठीक करता है (\"Unable to render rich display\")। हर ```mermaid-ब्लॉक को असली Mermaid-पार्सर से बिना ब्राउज़र के जाँचता है और परिणाम बाद में लाइव GitHub पेज पर सत्यापित करता है।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [mermaid, markdown, github, readme, diagramm, lint, dokumentation]
language: hi
status: active
visibility: public
dependencies: {'tools': ['node', 'git'], 'services': ['GitHub'], 'protocols': [], 'python': [], 'npm': ['mermaid', 'jsdom', 'playwright-core']}
translated_from_sha256: a1286c3571792da726aea23967c12360cb0daadb8d3d0bce2208ff27fc14bce9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
---
<img src="banner.png" width="100%" alt="mermaid-lint banner">

# mermaid-lint

GitHub पर किसी Mermaid-आरेख में सिंटैक्स त्रुटि हो तो आरेख के बजाय बॉक्स दिखता है
**"Unable to render rich display"**। स्थानीय रूप से यह ध्यान में नहीं आता, क्योंकि कोई उपकरण
ब्लॉक की जाँच नहीं करता। यह स्किल इसी कमी को भरता है।

## कब लागू करें

- README या दस्तावेज़ GitHub पर आरेख के बजाय रेंडर-त्रुटि दिखाता है।
- आरेख वाले दस्तावेज़ के प्रकाशन या रिलीज़ से पहले।
- Mermaid-ब्लॉक को छूने वाले Markdown में हर बदलाव के बाद।
- कई रिपॉज़िटरी में एक साथ, जब यह अनिश्चित हो कि कहाँ-कहाँ कुछ टूटा है।

## दो उपकरण

### 1. `mermaid_lint.mjs` — ब्राउज़र के बिना सिंटैक्स जाँच

```
node mermaid_lint.mjs <repo-pfad> [...] [--json]
node mermaid_lint.mjs --from <liste.txt> [--json]
```

`.md`-फ़ाइलें रिकर्सिवली खोजता है, हर ```mermaid-ब्लॉक निकालता है और उसे
`mermaid.parse()` से चलाता है — **वही पार्सर, जिसे GitHub ब्राउज़र में उपयोग करता है**।
Exit 0 = सब पार्स हुए, Exit 1 = कम से कम एक ब्लॉक खराब है। आउटपुट में फ़ाइल, ब्लॉक-नंबर,
पंक्ति और पार्सर की मूल त्रुटि दिखती है।

`--from <datei>` एक पथ-सूची पढ़ता है, हर पंक्ति में एक पथ। कई आर्गुमेंट के बजाय इसका उपयोग करें:
Backslash वाले Windows-पथ Bash-शेल में चुपचाप बिगड़ जाते हैं
(`D:\code\my-repo` बन जाता है `D:codemy-repo`)। पथ Forward-Slash से लिखें।

एक ही प्रक्रिया सैकड़ों रिपॉज़िटरी सँभाल लेती है, क्योंकि Mermaid केवल एक बार लोड होता है।
कोई Puppeteer नहीं, कोई Chromium-डाउनलोड नहीं।

### 2. `readback.mjs` — लाइव पेज पर सबूत

```
node readback.mjs <github-url> [...]
```

मौजूदा Edge में पेज खोलता है (कोई ब्राउज़र-डाउनलोड नहीं) और असली रेंडर-त्रुटियाँ गिनता है।
हर पेज का निर्णय: `OK`, `DEFEKT`, `UNKLAR` या `KEIN-MERMAID`।

## तीन जाल, जिनकी वजह से यह स्किल ज़रूरी है

**GitHub Mermaid को sandboxed iframes** में `viewscreen.githubusercontent.com` से रेंडर करता है।
मुख्य पेज उनकी सामग्री नहीं देखता। जो केवल `document.body.innerText` या
`msedge --dump-dom` का मूल्यांकन करता है, उसे **हर** पेज पर शून्य त्रुटियाँ मिलती हैं — यहाँ तक कि
उस पेज पर भी जो सिद्ध रूप से टूटा है। इसलिए `readback.mjs` सभी Frames का मूल्यांकन करता है।

**अकेला DEFEKT-परिणाम विश्वसनीय नहीं है।** लोड होते समय GitHub क्षणभर के लिए एक प्लेसहोल्डर
दिखाता है, जो रेंडर-त्रुटि जैसा लगता है। 2026-09-20 को मापा गया: वही पेज पहले `ERR=1`
बताता था, फिर दो बार `ERR=0`। `readback.mjs` नकारात्मक परिणामों को स्वतः दोहराता है;
`OK` कभी नहीं दोहराया जाता।

**`mermaid.parse()` को DOM चाहिए**, अन्यथा वह `DOMPurify.addHook` पर विफल होता है और वैध
Flowcharts को गलती से खराब बताता है। `mermaid_lint.mjs` पहले से एक jsdom-विंडो उपलब्ध कराता है।
यदि फिर भी कोई पर्यावरण-त्रुटि बचे, तो वह अलग से `envIssues` में जाती है और उसे सिंटैक्स-त्रुटि
के रूप में **नहीं** गिना जाता।

## हमेशा नकारात्मक नियंत्रण से जाँचें

किसी हरे परिणाम पर भरोसा करने से पहले उपकरण को एक ऐसी स्थिति पर चलाएँ जिसे आप जानते हैं कि टूटी हुई है,
जैसे आपके सुधार से पहले का कमिट:

```
node readback.mjs "https://github.com/<org>/<repo>/blob/<alter-sha>/README.md"
```

यदि वह भी `OK` बताता है, तो आपका Readback कुछ नहीं माप रहा। ऊपर की iframe-जाल
इसी तरह खोजी गई थी।

## सामान्य त्रुटि-कारण और उनका न्यूनतम-हस्तक्षेप समाधान

| पार्सर-त्रुटि में लक्षण | कारण | समाधान |
|---|---|---|
| `Expecting '+', '-', '()', 'ACTOR', got 'loop'` | प्रतिभागी का नाम आरक्षित शब्द जैसा है: `loop`, `alt`, `opt`, `par`, `end`, `critical`, `break`, `rect`, `note` | Alias घोषित करें: `participant L as Loop`, संदेश `L` का उपयोग करते हैं। **दिखने वाला नाम वही रहता है** — नाम न बदलें। |
| Flowchart में `got 'PS'` | Node-लेबल में गोल कोष्ठक | लेबल को उद्धरण-चिह्नों में लिखें: `A["Start (hier)"]` |
| `Lexical error ... Unrecognized text` | लेबल में Backticks या कोलन | लेबल को उद्धरण-चिह्नों में लिखें, Backticks हटाएँ |
| `Expecting 'SEMI', 'NEWLINE', 'EOF'` — `graph`/`flowchart` में | `Note:` केवल Sequence- और Class-आरेखों में होता है | सूचना-पाठ ब्लॉक से निकालकर उसके नीचे Markdown-पंक्ति के रूप में रखें, ताकि जानकारी दिखती रहे |
| Sequence-आरेख में `Expecting 'SOLID_OPEN_ARROW' ... got 'NEWLINE'` | संदेश-पाठ में **HTML-Entity** (`&lambda;`, `&Delta;`, `&ge;`)। यहाँ कोष्ठक और `=` समस्या नहीं पैदा करते (वे पार्स नहीं तोड़ते) — Entity का समापन `;` Lexer को Statement-Terminator लगता है, और उसके बाद का सब कुछ नया कथन बन जाता है। | Entity को शाब्दिक अक्षर से बदलें (λ, Δ, ≥), बाकी पाठ अपरिवर्तित रहे। कोष्ठक रह सकते हैं। संख्यात्मक मान और उनकी लिखावट कभी न बदलें। |
| Sequence-संदेश में अर्धविराम (;) | Statement-अंत के रूप में पढ़ा जाता है | ` - ` से बदलें |

**उद्धृत Flowchart-लेबलों** में Entities समस्या नहीं हैं — नियम केवल
Sequence-संदेशों पर लागू होता है। `mermaid_lint.mjs` ऐसी Entities को अलग `[WARN]`-पंक्ति में
दर्ज करता है (JSON में फ़ील्ड `warnings`), पार्सर-त्रुटि के अतिरिक्त: पार्सर केवल
`got 'NEWLINE'` कहता है और कारण नहीं बताता।

**सिद्धांत:** न्यूनतम-हस्तक्षेप। लेआउट, Node-IDs, क्रम और दिखने वाला पाठ जहाँ तक संभव हो अपरिवर्तित
रहें। वैज्ञानिक रिपॉज़िटरी में यह विशेष रूप से संख्यात्मक मानों और उनकी लिखावट पर लागू होता है। EN/DE-समानता
में दोनों संस्करण संरचनात्मक रूप से एक जैसे रखें।

## कई रिपॉज़िटरी में प्रक्रिया

1. `gh repo list <org> --limit 200 --json name,isArchived,isPrivate,defaultBranchRef` से सूची बनाएँ।
2. Clones को **Remote-स्थिति तक खींचें** और विचलनों को गंभीरता से लें। पुराने Clone पर Lint गलत स्थिति मापता है।
   यदि `git pull --ff-only` विफल हो, तो Working-Tree के बजाय `origin` से जाँचें:
   `git archive origin/<branch> | tar -x -C <tempdir>` और अस्थायी फ़ोल्डर को Lint करें।
3. **एक ही नाम वाले, पर अलग Orgs के रिपॉज़िटरी** (विशेषकर `.github`) एक ही Clone पर मैप न करें — अन्यथा
   एक ही रिपॉज़िटरी नौ बार जाँची जाएगी। नाम-दोहराव होने पर `<org>__<repo>` में सपाट क्लोन करें और ताज़ा स्थिति Lint करें।
4. किसी भी बदलाव से पहले Locks जाँचें (`lock_scan.py`, `LOCK*.txt`) Clone में **और** OneDrive-प्रोजेक्ट-पथ पर,
   अपना Lock लगाएँ, Push के बाद हटाएँ।
   **Scope पढ़ें, केवल मौजूदगी नहीं:** समाप्त `expires_after` वाला `LOCK.team.*` अनदेखा किया जा सकता है; `LOCK.user.zenodo-upload.txt`
   केवल बाहरी Zenodo-लेखन-संचालन को रोकता है और दस्तावेज़-बदलावों की स्पष्ट अनुमति देता है।
   इसके विपरीत `LOCK.user.until-winners-announcement.txt` (Judging) हर Push रोकता है — वहाँ केवल पढ़ें और निष्कर्ष एक Ticket में दर्ज करें।
5. सुधारें, हरे होने तक Lint करें, Commit करें, `git pull --rebase`, Push करें।
6. नकारात्मक नियंत्रण के साथ Readback। तभी इसे पूर्ण माना जाए।

## सेटअप

```
npm install mermaid jsdom playwright-core
```

स्क्रिप्ट-फ़ोल्डर में या वैश्विक रूप से; `playwright-core` स्थापित Edge (`channel: 'msedge'`) का उपयोग करता है और
अपना ब्राउज़र डाउनलोड नहीं करता। यह केवल Readback के लिए आवश्यक है — सिंटैक्स-जाँच इसके बिना चलती है।

## संबंधित

- GithubBot में `_tools/lint_mermaid.py`: `--fix` वाला पुराना Regex-आधारित Linter।
  यह ज्ञात पैटर्न स्वतः ठीक करता है, **पर आरक्षित शब्द नहीं पहचानता** और इस स्किल का विकल्प नहीं है। उचित क्रम:
  पहले निदान के लिए `mermaid_lint.mjs`, फिर बड़े पैमाने के पैटर्न के लिए आवश्यक होने पर `lint_mermaid.py --fix`, फिर दोबारा Lint।
- `github-repo-care`: रिपॉज़िटरी-रखरखाव और प्रकाशन के लिए समग्र प्रोटोकॉल।
