---
name: using-blender
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-06-20
updated: 2026-06-20
description: "AI এজেন্টদের জন্য সাধারণ Blender ওয়ার্কফ্লো স্কিল, যা .blend, .fbx, .obj, .glb, glTF, মেটেরিয়াল, সিন ইনস্পেকশন, bpy অটোমেশন, হেডলেস Blender ব্যাচ রান, এক্সপোর্ট/রিইম্পোর্ট ভ্যালিডেশন, প্রিভিউ এবং ঐচ্ছিক Blender MCP নিয়ন্ত্রণ সম্পর্কিত কাজের জন্য। যখন কোনো কাজে Blender বা 3D অ্যাসেট ফাইল ব্যবহারকারী-নিরপেক্ষভাবে খোলা, পরিদর্শন, তৈরি, অটোমেট, রূপান্তর, অপ্টিমাইজ, রেন্ডার বা যাচাই করার অনুরোধ থাকে, তখন এটি ব্যবহার করুন।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
dependencies: {'tools': ['blender'], 'services': [], 'protocols': [], 'python': []}
category: game-dev
tags: [blender, bpy, 3d, assets, fbx, glb, gltf, mcp]
language: bn
status: active
visibility: public
provenance: {'origin': 'custom', 'origin_path': 'skills/game-dev/using-blender', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: 7bfddc52a5ef221e1ec94d0aae4bbc1095390df9b944341075b64321ab8782ff
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="using-blender banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **English Translation** — Official English version of `using-blender`.

# Blender ব্যবহার (Deutsch)

## মূল নিয়ম

কাজের প্রয়োজন অনুযায়ী Blender-এর তিনটি মোডে কাজ করুন:

1. **GUI-Modus:** ব্যবহারকারী যখন কোনো অ্যাসেট দেখতে, মূল্যায়ন করতে বা ম্যানুয়ালি আরও সম্পাদনা করতে চান, তখন Blender দৃশ্যমানভাবে খুলুন।
2. **Headless-Modus:** এক্সপোর্ট, রিইম্পোর্ট, ব্যাচ প্রসেসিং বা পুনরুৎপাদনযোগ্য যাচাই চাওয়া হলে `blender --background --python <script.py>` ব্যবহার করুন।
3. **MCP-Modus:** শুধুমাত্র তখনই ব্যবহার করুন যখন একটি চলমান Blender-Addon ইচ্ছাকৃতভাবে সংযুক্ত থাকে এবং লাইভ সিন নিয়ন্ত্রণ প্রয়োজন। আগে নিরাপত্তা ও লাইসেন্সের অবস্থা পরীক্ষা করুন।

## স্ট্যান্ডার্ড প্রক্রিয়া

1. লক্ষ্য স্পষ্ট করুন: দেখা, তৈরি, রূপান্তর, অপ্টিমাইজ, রেন্ডার বা যাচাই।
2. বিদ্যমান ফাইল পড়ুন: প্রথমে Manifest, README, এক্সপোর্ট ফরম্যাট এবং বিদ্যমান যাচাই ফলাফল দেখুন।
3. Blender-এর পথ নির্ধারণ করুন: PATH-এ `blender`, প্রজেক্ট-নির্দিষ্ট কনফিগারেশন বা ব্যবহারকারীর পথ। প্রকাশযোগ্য ডকুমেন্টেশনে কোনো স্থানীয় ব্যক্তিগত পথ লিখবেন না।
4. অটোমেশনের জন্য একটি ছোট `bpy`-Script ব্যবহার করুন, যা ইনপুট, আউটপুট ও ত্রুটিগুলো সুস্পষ্টভাবে প্রকাশ করে।
5. প্রতিটি এক্সপোর্টের পর ফলাফলকে ব্যবহারযোগ্য বলার আগে অন্তত একটি রিইম্পোর্ট বা লোড-যাচাই চালান।
6. আর্টিফ্যাক্টগুলো সংক্ষেপে নথিভুক্ত করুন: উৎস, এক্সপোর্ট ফরম্যাট, টুল-ভার্সন, যাচাইয়ের অবস্থা এবং জানা সীমাবদ্ধতা।

## এক্সপোর্ট ও যাচাইয়ের নিয়ম

- সাধারণ ওয়েব/প্রিভিউ ব্যবহারের জন্য সাধারণত `.glb` পছন্দ করুন।
- Game-Engine ও DCC-আদান-প্রদানের জন্য, লক্ষ্য ওয়ার্কফ্লো প্রয়োজন হলে, অতিরিক্তভাবে `.fbx` বা `.obj/.mtl` প্রস্তাব করুন।
- রাউন্ডট্রিপে সবসময় যাচাই করুন: ফাইল আছে, খালি নয়, রিইম্পোর্ট করা যায়, প্রত্যাশিত অবজেক্ট/মেটেরিয়ালের নাম বিদ্যমান।
- বড় অ্যাসেটের জন্য মেট্রিক সংগ্রহ করুন: Mesh-সংখ্যা, মেটেরিয়াল, Bounding Box, ফাইলের আকার এবং ঐচ্ছিকভাবে Triangle Count।
- রেন্ডার যাচাইয়ের জন্য ব্যয়বহুল Cycles- বা Full-HD-রেন্ডার শুরু করার আগে ছোট প্রিভিউ-রেজোলিউশন ব্যবহার করুন।

## নিরাপত্তা নিয়ম

- `bpy`-কোড হলো ফাইল-সিস্টেম অ্যাক্সেস সহ স্থানীয় Python-কোড। শুধুমাত্র নিজে লেখা বা অডিট করা Script চালান।
- লাইসেন্স ও গোপনীয়তা পরীক্ষা ছাড়া কোনো বাইরের Blender-Addon, অ্যাসেট-ডাউনলোডার বা টেলিমেট্রি-সার্ভার সক্রিয় করবেন না।
- যেকোনো `execute_python`-টুল সহ MCP-সার্ভারের ক্ষেত্রে আগে Scope, নেটওয়ার্ক, কার্যনির্বাহী ডিরেক্টরি ও Timeout সীমিত করুন।
- Marketplace বা বাইরের অ্যাসেটের ক্ষেত্রে লাইসেন্স আলাদাভাবে যাচাই করুন। প্রযুক্তিগতভাবে লোড করা যাওয়া ব্যবহারের অধিকারের বিকল্প নয়।

## MCP-বিকল্প

লাইভ নিয়ন্ত্রণের জন্য, যখন কোনো Blender-MCP-সার্ভার নির্বাচন, ইনস্টল বা মূল্যায়ন করতে হবে, তখন [references/blender-mcp-review.md](references/blender-mcp-review.md) পড়ুন।

## পরিবর্তন-লগ

### 1.0.0 (2026-06-20)
- GUI, Headless ও MCP রাউটিংসহ প্রাথমিক ব্যবহারকারী-নিরপেক্ষ Blender-স্কিল।

## GUI না খুলে ফলাফল যাচাই

অ্যাসেটের জন্য একটি প্রস্তুত Background-Gate আছে, যা একটি রানেই **চারটি রেন্ডার ও পরিমাপযোগ্য মেট্রিক** দেয় (Rotation, Pivot, ভাসমান অংশ):

```powershell
blender.exe --background --factory-startup `
  --python "<OneDrive>\.TOPICS\.ROBLOX\_tools\verify_asset_visual.py" -- `
  --fbx "<asset.fbx>" --out "<ordner>" --json
```

কোনো GUI লাগে না, ফোকাসেরও প্রয়োজন নেই। বিস্তারিত ও সীমাবদ্ধতা (যেমন: MCP-সার্ভার `ellmos-blender-use` **রেন্ডার করতে পারে না**): `.ROBLOX\BLENDER_ASSET_CHANNELS.md`।
বিস্তারিত ওয়ার্কফ্লো: স্কিল `build-assets-with-blender`।
