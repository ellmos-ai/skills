---
name: mermaid-lint
version: 1.0.0
type: tool
author: Lukas Geiger + Claude
created: 2026-09-20
updated: 2026-09-20
aliases: [mermaid, mermaid-fehler, diagramm-render-fehler, unable-to-render-rich-display, schaltplan-fehler]
description: "GitHub যে Mermaid ডায়াগ্রাম রেন্ডার করতে পারে না (\"Unable to render rich display\") সেগুলো খুঁজে বের করে ঠিক করে। প্রতিটি ```mermaid ব্লক ব্রাউজার ছাড়া আসল Mermaid পার্সার দিয়ে যাচাই করে, এবং পরে লাইভ GitHub পেজে ফলাফল প্রমাণ করে।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [mermaid, markdown, github, readme, diagramm, lint, dokumentation]
language: bn
status: active
visibility: public
dependencies: {'tools': ['node', 'git'], 'services': ['GitHub'], 'protocols': [], 'python': [], 'npm': ['mermaid', 'jsdom', 'playwright-core']}
translated_from_sha256: a1286c3571792da726aea23967c12360cb0daadb8d3d0bce2208ff27fc14bce9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="mermaid-lint banner">

# mermaid-lint

একটি Mermaid ডায়াগ্রামে সিনট্যাক্স ত্রুটি থাকলে GitHub-এ ডায়াগ্রামের বদলে বাক্সটি দেখায়
**"Unable to render rich display"**। স্থানীয়ভাবে এটি ধরা পড়ে না, কারণ কোনো টুল ব্লকটি যাচাই করে না।
এই Skill সেই ফাঁকটি বন্ধ করে।

## কখন ব্যবহার করবেন

- একটি README বা নথি GitHub-এ ডায়াগ্রামের বদলে একটি রেন্ডার ত্রুটি দেখায়।
- ডকুমেন্টেশনে ডায়াগ্রাম থাকা অবস্থায় প্রকাশ বা রিলিজের আগে।
- Mermaid ব্লক প্রভাবিত করে এমন Markdown পরিবর্তনের পরে প্রতিবার।
- একাধিক repo জুড়ে, যখন স্পষ্ট নয় কোথায় কোথায় কিছু ভাঙা আছে।

## দুটি টুল

### 1. `mermaid_lint.mjs` — ব্রাউজার ছাড়া সিনট্যাক্স যাচাই

```
node mermaid_lint.mjs <repo-pfad> [...] [--json]
node mermaid_lint.mjs --from <liste.txt> [--json]
```

`.md` ফাইলগুলো পুনরাবৃত্তভাবে খুঁজে বের করে, প্রতিটি ```mermaid ব্লক বের করে এবং
`mermaid.parse()` দিয়ে চালায় — **GitHub ব্রাউজারে যে পার্সার ব্যবহার করে সেটিই**।
Exit 0 = সব পার্স হয়েছে, Exit 1 = অন্তত একটি ব্লক ত্রুটিপূর্ণ। আউটপুটে ফাইল, ব্লক নম্বর, লাইন এবং
পার্সারের আক্ষরিক ত্রুটিবার্তা দেখানো হয়।

`--from <datei>` একটি পথ-তালিকা পড়ে, প্রতি লাইনে একটি করে। অনেক আর্গুমেন্টের বদলে এটি ব্যবহার করুন:
ব্যাকস্ল্যাশসহ Windows পথ Bash শেলে নীরবে নষ্ট হয়ে যায়
(`D:\code\my-repo` হয়ে যায় `D:codemy-repo`)। পথ লিখুন ফরোয়ার্ড-স্ল্যাশ দিয়ে।

একটি একক প্রক্রিয়া শত শত repo সামলাতে পারে, কারণ Mermaid একবারই লোড হয়।
Puppeteer নেই, Chromium ডাউনলোডও নেই।

### 2. `readback.mjs` — লাইভ পেজে প্রমাণ

```
node readback.mjs <github-url> [...]
```

বিদ্যমান Edge-এ পেজগুলো খোলে (কোনো ব্রাউজার ডাউনলোড ছাড়াই) এবং প্রকৃত রেন্ডার ত্রুটি গণনা করে।
প্রতিটি পেজের রায়: `OK`, `DEFEKT`, `UNKLAR` বা `KEIN-MERMAID`।

## তিনটি ফাঁদ যা এই Skill-কে প্রয়োজনীয় করে তোলে

**GitHub Mermaid-কে `viewscreen.githubusercontent.com`-এর sandboxed iframe-এ রেন্ডার করে।**
মূল পেজ তাদের ভেতরের বিষয়বস্তু দেখতে পায় না। যে শুধু `document.body.innerText` বা
`msedge --dump-dom` বিশ্লেষণ করে, সে **প্রতিটি** পেজে শূন্য ত্রুটি পায় — এমনকি যে পেজ প্রমাণিতভাবে ভাঙা
সেটিতেও। `readback.mjs` তাই সব frame বিশ্লেষণ করে।

**একটি একক DEFEKT-ফলাফল নির্ভরযোগ্য নয়।** লোড হওয়ার সময় GitHub সংক্ষেপে একটি প্লেসহোল্ডার দেখায়,
যা রেন্ডার ত্রুটির মতো দেখায়। ২০২৬-০৯-২০ তারিখে পরিমাপ অনুযায়ী: একই পেজ প্রথমে `ERR=1` দেখায়,
তারপর দুবার `ERR=0`। `readback.mjs` এজন্য নেতিবাচক ফলাফল স্বয়ংক্রিয়ভাবে পুনরায় পরীক্ষা করে;
`OK` কখনো পুনরায় পরীক্ষা করা হয় না।

**`mermaid.parse()`-এর একটি DOM দরকার**, নইলে এটি `DOMPurify.addHook`-এ ব্যর্থ হয় এবং বৈধ flowchart-কে
ভুলভাবে ভাঙা বলে। `mermaid_lint.mjs` আগে থেকে একটি jsdom উইন্ডো সরবরাহ করে। তবুও পরিবেশগত ত্রুটি থাকলে
তা আলাদাভাবে `envIssues`-এর অধীনে রাখা হয় এবং সিনট্যাক্স ত্রুটি হিসেবে **গণনা করা হয় না**।

## সবসময় একটি নেতিবাচক নিয়ন্ত্রণের বিপরীতে যাচাই করুন

একটি সবুজ ফলাফল বিশ্বাস করার আগে, টুলটি একবার এমন একটি অবস্থায় চালান যা ভাঙা বলে আপনি জানেন —
যেমন আপনার ফিক্সের আগের commit:

```
node readback.mjs "https://github.com/<org>/<repo>/blob/<alter-sha>/README.md"
```

সেটিও `OK` দেখালে, আপনার readback কিছু মাপছে না। উপরের iframe ফাঁদটি এভাবেই ধরা পড়েছিল।

## সাধারণ ত্রুটির কারণ এবং ন্যূনতম-আক্রমণাত্মক সমাধান

| পার্সার ত্রুটির লক্ষণ | কারণ | সমাধান |
|---|---|---|
| `Expecting '+', '-', '()', 'ACTOR', got 'loop'` | অংশগ্রহণকারীর নাম একটি সংরক্ষিত শব্দের মতো: `loop`, `alt`, `opt`, `par`, `end`, `critical`, `break`, `rect`, `note` | একটি alias ঘোষণা করুন: `participant L as Loop`, বার্তাগুলো `L` ব্যবহার করে। **প্রদর্শিত নাম থাকে** — নাম বদলাবেন না। |
| flowchart-এ `got 'PS'` | node label-এ গোল বন্ধনী | label-কে quote করুন: `A["Start (hier)"]` |
| `Lexical error ... Unrecognized text` | label-এ backtick বা কোলন | label-কে quote করুন, backtick সরান |
| `Expecting 'SEMI', 'NEWLINE', 'EOF'` `graph`/`flowchart`-এ | `Note:` শুধু sequence ও class ডায়াগ্রামে আছে | ব্লক থেকে ইঙ্গিতমূলক লেখা সরিয়ে তার নিচে একটি Markdown লাইন হিসেবে রাখুন, যাতে তথ্যটি দৃশ্যমান থাকে |
| sequence ডায়াগ্রামে `Expecting 'SOLID_OPEN_ARROW' ... got 'NEWLINE'` | বার্তার লেখায় **HTML entity** (`&lambda;`, `&Delta;`, `&ge;`)। এখানে বন্ধনী বা `=` ভাঙে না — entity-র শেষের `;` লেক্সার statement terminator হিসেবে পড়ে, এবং তার পরের সবকিছু নতুন statement হয়ে যায়। | entity-কে আক্ষরিক অক্ষর দিয়ে বদলান (λ, Δ, ≥), নইলে লেখা অপরিবর্তিত রাখুন। বন্ধনী থাকতে পারে। সংখ্যামান ও তার বানান কখনো বদলাবেন না। |
| sequence বার্তায় semicolon | statement শেষ হিসেবে পড়া হয় | ` - ` দিয়ে বদলান |

**quote করা flowchart label**-এ entity সমস্যা নয় — নিয়মটি শুধু sequence বার্তার জন্য প্রযোজ্য।
`mermaid_lint.mjs` এমন entity-কে আলাদা `[WARN]` লাইন হিসেবে জানায় (JSON-এ `warnings` ক্ষেত্র),
পার্সার ত্রুটির পাশাপাশি: পার্সার শুধু `got 'NEWLINE'` বলে এবং কারণ উল্লেখ করে না।

**মূলনীতি:** ন্যূনতম হস্তক্ষেপ। লেআউট, node ID, ক্রম এবং দৃশ্যমান লেখা যথাসম্ভব অপরিবর্তিত থাকে।
বৈজ্ঞানিক repo-তে এটি বিশেষভাবে সংখ্যামান ও তার বানানের ক্ষেত্রে প্রযোজ্য। EN/DE সমতা রাখলে উভয় সংস্করণের
কাঠামো একই রাখুন।

## একাধিক repo জুড়ে কার্যপ্রবাহ

1. `gh repo list <org> --limit 200 --json name,isArchived,isPrivate,defaultBranchRef` দিয়ে তালিকা তৈরি করুন।
2. Clone-গুলো **রিমোটের সর্বশেষ অবস্থায় টেনে আনুন** এবং বিচ্যুতিকে গুরুত্ব দিন। পুরোনো clone-এ lint চালালে
   ভুল অবস্থা মাপা হয়। `git pull --ff-only` ব্যর্থ হলে, কার্যকরী ডিরেক্টরির বদলে `origin`-এর বিপরীতে যাচাই করুন:
   `git archive origin/<branch> | tar -x -C <tempdir>` চালিয়ে অস্থায়ী ফোল্ডারটি lint করুন।
3. **বিভিন্ন org-এর একই নামের repo** (সাধারণত `.github`) একই clone-এ map করা যাবে না — নইলে একই repo
   নয়বার যাচাই হয়। নামের সংঘর্ষ হলে `<org>__<repo>`-এর ভেতরে সমতল করে clone করুন এবং তাজা অবস্থাটি lint করুন।
4. প্রতিটি পরিবর্তনের আগে lock পরীক্ষা করুন (`lock_scan.py`, `LOCK*.txt` — clone-এ **এবং**
   OneDrive প্রজেক্ট পথে), নিজের lock বসান এবং push-এর পরে তা সরান।
   **শুধু অস্তিত্ব নয়, পরিধিও পড়ুন:** মেয়াদোত্তীর্ণ `expires_after`-সহ `LOCK.team.*` উপেক্ষা করা যায়; `LOCK.user.zenodo-upload.txt`
   শুধু বাহ্যিক Zenodo লেখার কাজ আটকায় এবং ডকুমেন্টেশন পরিবর্তনকে স্পষ্টভাবে অনুমতি দেয়।
   অন্যদিকে একটি `LOCK.user.until-winners-announcement.txt` (Judging) প্রতিটি push আটকায় — সেখানে শুধু পড়ে যাচাই করুন এবং
   ফলাফলটি একটি ticket হিসেবে রাখুন।
5. মেরামত করুন, সবুজ না হওয়া পর্যন্ত lint করুন, commit করুন, `git pull --rebase` চালান, push করুন।
6. নেতিবাচক নিয়ন্ত্রণসহ readback। তারপরই একে সম্পন্ন ধরা হয়।

## সেটআপ

```
npm install mermaid jsdom playwright-core
```

স্ক্রিপ্টের ফোল্ডারে বা গ্লোবালভাবে; `playwright-core` ইনস্টল করা Edge (`channel: 'msedge'`) ব্যবহার করে এবং নিজের
কোনো ব্রাউজার ডাউনলোড করে না। শুধু readback-এর জন্য এটি দরকার — সিনট্যাক্স যাচাই এটি ছাড়াই চলে।

## সংশ্লিষ্ট

- GithubBot-এর `_tools/lint_mermaid.py`: `--fix`-সহ পুরোনো regex-ভিত্তিক linter। এটি পরিচিত প্যাটার্ন
  স্বয়ংক্রিয়ভাবে মেরামত করে, **কিন্তু সংরক্ষিত শব্দ চেনে না** এবং এই Skill-এর বিকল্প নয়। উপযোগী ক্রম: প্রথমে
  নির্ণয়ের জন্য `mermaid_lint.mjs`, তারপর প্রয়োজনে গণ-প্যাটার্নের জন্য `lint_mermaid.py --fix`, তারপর আবার lint।
- `github-repo-care`: repo রক্ষণাবেক্ষণ ও প্রকাশের সামগ্রিক প্রোটোকল।
