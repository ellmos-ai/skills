---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "স্বতন্ত্র নেভিগেশন ও রাউটিং কৌশল, যা CLAUDE.md, AGENTS.md, README.md ও RULES.md এর মতো পথনির্দেশক নথি এবং ব্যবহারকারী-কনফিগারযোগ্য কীওয়ার্ড খুঁজে পেতে ডিরেক্টরি অনুক্রম উপরের দিকে ও নিচের দিকে অনুসন্ধান করে। কনফিগারেশন staircase-config.json বা config.json এর মাধ্যমে করা হয়। Up-and-Down Routing বা Walking Bass Routing নামেও পরিচিত।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
language: bn
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: 28ec74023759355f5a974506a065cb0c737455ec4d3d59d23129276e63011200
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="staircase-routing banner">

# Staircase-Routing (Up-and-Down / Walking Bass Routing)

*Up-and-Down Routing* বা *Walking Bass Routing* নামেও পরিচিত **Staircase-Routing** স্কিল এআই এজেন্টদের জন্য ডিরেক্টরি নথি পরীক্ষার কৌশলকে অন্তর্ভুক্ত করে।

যখন কোনো এজেন্ট একটি ডিরেক্টরিতে প্রবেশ করে বা কোনো ফাইলে কাজ করে, তখন কোড পরিবর্তন বা কোনো কার্যক্রম সম্পাদনের আগে প্রাসঙ্গিক প্রেক্ষাপট, নিয়ম এবং পথনির্দেশক নথি খুঁজে পেতে সে এই কৌশল ব্যবহার করে।

---

## 1. পথনির্দেশক নথির মানদণ্ড

Staircase-Routing ডিফল্টভাবে এই পথনির্দেশক নথিগুলো খোঁজে:

- **বৈশ্বিক ও প্রকল্প-সংক্রান্ত নিয়ন্ত্রণ:** `CLAUDE.md`, `AGENTS.md`,
  `START.md`, `RULES.md`
- **প্রকল্পের সারসংক্ষেপ ও কাজ:** `README.md`, `TODO.md`, `NOTIZ.md`,
  `BEWEISNOTIZ.md`
- **ব্যবহারকারী-সংজ্ঞায়িত কীওয়ার্ড:** `staircase-config.json` বা `config.json` এর মাধ্যমে কনফিগার করা হয়।

---

## 2. ট্রাভার্সাল অ্যালগরিদম

```text
                           [ Root- / Workspace-Ebene ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Schritt 2: Root-Wegweiser lesen)
                           └───────────▲────────────┘
                                       │ (Treppe aufwärts)
                           ┌───────────┴────────────┐
                           │ Unterordner / Ziel     │ ◄── (Schritt 1: Im CWD beginnen)
                           └───────────┬────────────┘
                                       │ (Treppe abwärts)
                           ┌───────────▼────────────┐
                           │ Kind- / Modulordner    │ ◄── (Schritt 3: Untergeordnete Wegweiser finden)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### ধাপ ১: বর্তমান কার্যকরী ডিরেক্টরি (CWD) পরীক্ষা করুন

- লক্ষ্য ফাইলের ডিরেক্টরি বা সক্রিয় কার্যকরী ডিরেক্টরি পরীক্ষা করুন।
- পথনির্দেশক নথি থাকলে সেগুলো অবিলম্বে পড়ুন।

### ধাপ ২: উপরের দিকে ট্রাভার্স করুন

- CWD তে কোনো পথনির্দেশক নথি **না** পাওয়া গেলে, প্যারেন্ট ডিরেক্টরিতে (`..`) যান।
- একটি রুট পথনির্দেশক নথি (`CLAUDE.md` বা `AGENTS.md`) বা ওয়ার্কস্পেসের সীমা না পৌঁছানো পর্যন্ত ধাপে ধাপে উপরের দিকে এটি পুনরাবৃত্তি করুন।
- বৈশ্বিক নির্দেশনা ও প্রকল্পের নিয়মাবলী নির্ধারণের জন্য পাওয়া সকল রুট পথনির্দেশক পড়ুন।

### ধাপ ৩: নিচের দিকে পরীক্ষা করুন

- নির্ধারিত রুট ডিরেক্টরি থেকে কাজের সাথে সম্পর্কিত উপ-ডিরেক্টরিতে নিচের দিকে যান।
- মডিউল-স্তরের বিশেষায়িত পথনির্দেশক, ডোমেইন নিয়ম বা কম্পোনেন্ট কনফিগারেশন খুঁজে পড়ুন।

---

## 3. ব্যবহারকারী-কনফিগারযোগ্য কীওয়ার্ড (`staircase-config.json`)

এজেন্টরা অনুসন্ধানকৃত পথনির্দেশকগুলো কাস্টমাইজ করতে একটি স্থানীয় বা বৈশ্বিক `staircase-config.json` পড়তে পারে:

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. `letter-hooker` ও নির্ধারিত কার্যাবলীর সাথে একীকরণ

`staircase-routing` কেন্দ্রীয় প্রিফ্লাইট বুটলোডার হিসেবে **`letter-hooker`** স্কিল এবং নির্ধারিত টাস্ক **`antigravity-kontext-and-workflow-loader-and-divider`** এর মধ্যে সংযুক্ত। এর ফলে এজেন্টরা পরিবর্তন শুরু করার আগে পথনির্দেশক নথি খুঁজে পায় ও অনুসরণ করে।
