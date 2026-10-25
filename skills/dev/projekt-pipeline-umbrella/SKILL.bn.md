---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "মেটা-/আম্ব্রেলা-স্কিল \"প্রজেক্ট-/পাইপলাইন-গঠন ও -পুনর্গঠন\" পরিবারের জন্য। এটি নতুন তৈরি, গ্রহণ, পুনর্গঠন এবং বিশ্লেষণের জন্য সমস্ত প্রজেক্ট ও পাইপলাইন স্কিল সম্পর্কে জানে এবং উপযুক্তটির কাছে পাঠিয়ে দেয়। যখন স্পষ্ট না থাকে যে কিছু নতুনভাবে তৈরি (Greenfield) করতে হবে নাকি পুনর্গঠন (Bestand) করতে হবে, অথবা বিষয়টি একটি একক প্রজেক্ট নাকি পুরো পাইপলাইন নিয়ে, তখন এই স্কিলটি ব্যবহার করুন। \"নতুন প্রজেক্ট/পাইপলাইন তৈরি করা\", \"বিদ্যমানটি পুনর্গঠন করা\", \"প্রজেক্ট গ্রহণ করা\", \"ফোল্ডার কাঠামো সংস্কার করা\", \"কোন Bootstrapper উপযুক্ত\" — এমন ক্ষেত্রেও এটি সক্রিয় হয়।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: bn
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [project-bootstrapper, pipeline-bootstrapper, project-onboarding, pipeline-optimizer, docs-analysis, dev-cycle]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/projekt-pipeline-umbrella/"
  origin_version: "0.1.0"
translated_from_sha256: 4a9761a120e11fee3911e26619e8d3b27f0b91e19925d6bc41ba7e44792a96c9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">
# প্রজেক্ট-/পাইপলাইন-গঠন ও -পুনর্গঠন — আম্ব্রেলা

## উদ্দেশ্য

"প্রজেক্ট-/পাইপলাইন-গঠন ও -পুনর্গঠন" পরিবারের প্রবেশপথ। এই পরিবারের সদস্যরা দুটি অক্ষ বরাবর সাজানো থাকে: **Greenfield বনাম Bestand** এবং **প্রজেক্ট-স্তর বনাম পাইপলাইন-স্তর**। এই আম্ব্রেলা "bootstrap" বনাম "optimize" বনাম "onboard"-এর প্রায়শ ঘটে যাওয়া বিভ্রান্তি প্রতিরোধ করে।

## সদস্য ও রাউটিং

| স্কিল | কাজ | কখন এটির পরিবর্তে অন্যটি |
|-------|-----|--------------------------|
| `/project-bootstrapper` | বিদ্যমান পাইপলাইনের **ভেতরে** নতুন প্রজেক্ট তৈরি | Greenfield, প্রজেক্ট-স্তর |
| `/pipeline-bootstrapper` | সম্পূর্ণ নতুন টপ-লেভেল পাইপলাইন তৈরি | Greenfield, পাইপলাইন-স্তর (বিরল) |
| `/project-onboarding` | বিদ্যমান প্রজেক্ট গ্রহণ/নথিভুক্ত করা | Bestand, প্রজেক্ট-স্তর |
| `/pipeline-optimizer` | বিদ্যমান পাইপলাইন/কাঠামো সংস্কার (6-ধাপের পদ্ধতি) | Bestand, পুনর্গঠন |
| `/docs-analysis` | প্রয়োজনীয়তা/ধারণাগত ডকুমেন্ট বর্তমান কোডের বিপরীতে যাচাই | Bestand, বিশ্লেষণ (পুনর্গঠন নয়) |
| `/dev-cycle` | আসল নির্মাণের জন্য 8-ধাপের উন্নয়ন কাঠামো | আড়াআড়ি: উন্নয়নের কীভাবে |

> রাউটিং নিয়ম: **নতুন + প্রজেক্ট** → `/project-bootstrapper` · **নতুন + পাইপলাইন** →
> `/pipeline-bootstrapper` · **বিদ্যমান গ্রহণ** → `/project-onboarding` · **বিদ্যমান পুনর্গঠন** →
> `/pipeline-optimizer` · **শুধু যাচাই** → `/docs-analysis` · **নির্মাণ** → `/dev-cycle`।

## ভালোভাবে যুক্ত সমন্বয়

- `/project-onboarding` (প্রথমে: বিদ্যমান অবস্থা নথিভুক্ত) → `/pipeline-optimizer` (পরে: লক্ষ্যভিত্তিক পুনর্গঠন) —
  আগে বোঝা, তারপর সংস্কার (6-ধাপের নীতি "আগে পড়া, তারপর লেখা" আচ্ছাদিত করে)।
- `/docs-analysis` (ফাঁক খোঁজা) → `/dev-cycle` (ফাঁক পূরণ করা)।
- `/project-bootstrapper` (কাঠামো) → `/dev-cycle` (বিষয়বস্তু উন্নয়ন)।

## সাধারণ নিয়মাবলি

- বিদ্যমান পাইপলাইন-নিয়মাবলি (Registry, Templates, CLAUDE.md) সর্বদা আগে পড়ুন — সমান্তরাল মানদণ্ড তৈরি করবেন না।
- Greenfield-স্কিল তৈরি করে, Bestand-স্কিল পুনর্গঠন করে — এগুলো মিশিয়ে ফেলবেন না।
- প্রয়োগের আগে একক স্কিলের Live-ফাইল পড়ুন।

## পরিবর্তন-লগ

### 0.1.0 (2026-06-17)
- প্রাথমিক সংস্করণ। প্রজেক্ট-/পাইপলাইন-পরিবারের জন্য অডিট-মোড (3c1) দ্বারা উৎপন্ন।
