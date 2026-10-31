---
name: therapie-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "থেরাপি / পরামর্শ পরিবারের জন্য মেটা-/আম্ব্রেলা-স্কিল। এটি সমস্ত থেরাপিউটিক স্কিল (স্থিতিশীলকরণ, পদ্ধতির সারসংক্ষেপ, কথোপকথন পরিচালনা এবং নিবন্ধনমুক্ত বিশেষায়িত পদ্ধতি) সম্পর্কে জানে এবং উপযুক্ত স্কিলের দিকে পরিচালিত করে। কোন থেরাপি-/পরামর্শ স্কিল উপযুক্ত তা অস্পষ্ট হলে, উপলব্ধ পদ্ধতিগুলোর একটি সারসংক্ষেপ প্রয়োজন হলে, অথবা কোনো পরামর্শ-/সংকট পরিস্থিতি আগে শ্রেণীবদ্ধ করতে হলে এই স্কিলটি ব্যবহার করুন। „কোন থেরাপি পদ্ধতি উপযুক্ত\", „পরামর্শ কাঠামোবদ্ধ করুন\", „সংকট — কী করা উচিত\", „থেরাপিউটিক পদ্ধতি বেছে নিন\" — এমন ক্ষেত্রেও এটি সক্রিয় হবে।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: therapy
tags: [therapie, beratung, umbrella, meta, routing]
language: bn
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [counseling-basics, guideline-therapies-overview, stabilization-techniques, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/therapie-umbrella/"
  origin_version: "0.1.0"
translated_from_sha256: 11cdb04f6cb7265c340ca6748ebb395ec6b6bc445fb3dad494f25cfcffd81259
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="therapie-umbrella banner">
# থেরাপি / পরামর্শ — আম্ব্রেলা

## উদ্দেশ্য

„থেরাপি / পরামর্শ" পরিবারের প্রবেশবিন্দু। এটি সামগ্রিক রাউটিং একত্র করে এবং
বিশেষ ক্ষেত্রের জন্য উপযুক্ত স্কিলের দিকে পরিচালিত করে। তিনটি সক্রিয় প্রবেশবিন্দু-স্কিল সামনের সারি গঠন করে;
তার পেছনে বিভিন্ন নিবন্ধনমুক্ত বিশেষায়িত পদ্ধতির একটি দীর্ঘ অংশ রয়েছে, যা `code-skill-index`
(ক্যাটালগ `catalog-therapy.md`) এর মাধ্যমে পাওয়া যায়।

## সদস্য ও রাউটিং

| স্কিল | কীসের জন্য | কখন অন্যগুলোর বদলে এটি |
|-------|-------------|-------------------------|
| `/stabilization-techniques` | সংকট হস্তক্ষেপ, গ্রাউন্ডিং, নিরাপদ স্থান, PMR, প্যানিক, Window of Tolerance | তীব্র চাপ/সংকটে **প্রথমে** — পদ্ধতিগত কাজের আগে স্থিতিশীলতা |
| `/guideline-therapies-overview` | নির্দেশিকাভিত্তিক স্বীকৃত পদ্ধতিসমূহের সারসংক্ষেপ: CBT, ACT, Schematherapie, Exposition, Systemische, Tiefenpsychologie | যখন উপযুক্ত **পদ্ধতি** বেছে নিতে বা ব্যাখ্যা করতে হবে |
| `/counseling-basics` | কথোপকথন পরিচালনা: সক্রিয় শোনা, প্রতিফলন, বৈধকরণ, MI/OARS, বৃত্তাকার প্রশ্ন | যখন বিষয়টি পদ্ধতি নয়, বরং কথোপকথনের **কীভাবে** তা নিয়ে |
| (নিবন্ধনমুক্ত বিশেষায়িত স্কিল) | স্বতন্ত্র পদ্ধতি (Genogramm, Expositionsdetails, Positive Psychologie, …) | কোনো নির্দিষ্ট স্বতন্ত্র পদ্ধতি গভীরভাবে প্রয়োজন হলে → `code-skill-index` এর মাধ্যমে |

> রাউটিং নিয়ম: তীব্র সংকট → `/stabilization-techniques` · পদ্ধতি বেছে নেওয়া/ব্যাখ্যা →
> `/guideline-therapies-overview` · কথোপকথন কৌশল → `/counseling-basics` · গভীর স্বতন্ত্র পদ্ধতি →
> `code-skill-index` এর মাধ্যমে নিবন্ধনমুক্ত বিশেষায়িত স্কিল।

## ভালোভাবে যুক্ত সংমিশ্রণ

- `/stabilization-techniques` (প্রথমে, তীব্র) → `/guideline-therapies-overview` (পরে, মধ্যমেয়াদি):
  প্রথমে নিরাপত্তা/Window of Tolerance প্রতিষ্ঠা করুন, তারপর উপযুক্ত স্বীকৃত পদ্ধতি বেছে নিন।
- `/counseling-basics` **উভয়কেই** সঙ্গ দেয় — কথোপকথনের মনোভাব (MI/OARS, বৈধকরণ) স্থিতিশীলকরণ
  এবং পদ্ধতিগত কাজ উভয় ক্ষেত্রেই বহন করে।

## সাধারণ নিয়মাবলি

- রোগনির্ণয় প্রতিস্থাপন করবে না; মনোশিক্ষামূলক ও সম্পদ-ভিত্তিকভাবে কাজ করুন।
- Window of Tolerance মূল অক্ষ হিসেবে: অতিউত্তেজনায় প্রথমে স্থিতিশীল করুন, সংঘাতমূলকভাবে মোকাবিলা করবেন না।
- প্রয়োগের আগে স্বতন্ত্র স্কিলের লাইভ ফাইলগুলো পড়ুন — এই আম্ব্রেলা কোনো বিষয়বস্তু পুনরুৎপাদন করে না।

## পরিবর্তন তালিকা

### 0.1.0 (2026-06-17)
- প্রাথমিক সংস্করণ। থেরাপি / পরামর্শ পরিবারের জন্য Audit-মোড (1c1) দ্বারা তৈরি।
