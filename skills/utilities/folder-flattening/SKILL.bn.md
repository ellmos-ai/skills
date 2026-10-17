---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "নেস্টেড ফোল্ডার হায়ারার্কিকে সমতল, মেশিন-পাঠযোগ্য কাঠামোতে রূপান্তর করুন। বুদ্ধিমান মার্জ লজিকসহ Bash-ভিত্তিক।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [ordner, flattening, filesystem, bash, reorganisation, cleanup]
language: bn
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/ordner-flattening.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ecd288c18790f209ab63e3b72bc81cf748f957b27068f37a9a4999740f4392b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="folder-flattening banner">

# ওয়ার্কফ্লো: ফোল্ডার-ফ্ল্যাটেনিং

লক্ষ্য: নেস্টেড ফোল্ডার কাঠামোকে একটি সমতল, মেশিন-পাঠযোগ্য কাঠামোতে রূপান্তর করা।
সুবিধা: আর ক্লিক করে খুঁজতে হবে না, বরং ডেটাবেস (Verzeichnis.db) দিয়ে অনুসন্ধান করা যাবে।
বিষয়গতভাবে যুক্তিসংগত হলে ডুপ্লিকেট অনুমোদিত।

---

## ধাপসমূহের সারসংক্ষেপ

| ধাপ | কী ঘটে | স্ক্রিপ্ট-অংশ |
|-----|--------|---------------|
| 1 | Flatten: সব সাবফোল্ডারকে এক স্তরে নামিয়ে আনা | `phase_flatten` |
| 2 | সংক্ষেপণ: দীর্ঘ পাথ-নামকে শেষ অংশে সংক্ষিপ্ত করা, সংঘর্ষে মার্জ করা | `phase_shorten` |
| 3 | পরিষ্কার: একাধিক আন্ডারস্কোর (`___`) সমাধান করা, ট্রেইলিং `_` সরানো | `phase_cleanup_underscores` |
| 4 | গ্রুপিং: সংখ্যা-ফোল্ডার, CD-ফোল্ডার, ছোট নামগুলো সংগ্রহ ফোল্ডারে | `phase_group_problematic` |
| 5 | ট্রিপল-বিশ্লেষণ: স্লাইডিং-উইন্ডো পদ্ধতিতে চলমান 3-এর গ্রুপ, সংক্ষিপ্ততম নাম মার্জ-লক্ষ্য হিসেবে | `phase_tripel_merge` |
| 6 | মিডিয়া-ফরম্যাট মার্জ: ফাইল-টাইপ অনুযায়ী ফোল্ডার একত্র করা (Template) | `phase_media_merge` |
| 7 | গোছানো: খালি ফোল্ডার মুছে ফেলা | `phase_cleanup_empty` |

---

## গুরুত্বপূর্ণ নিয়মাবলি

### ট্রিপল-বিশ্লেষণ ম্যাচিং
- **সাবস্ট্রিং**: `Aufklaerung` in `Aufklaerungsbroschueren` -> merge in `Aufklaerung`
- **বহুবচন/উমলাউট (ä/ö/ü)**: `Raum` = `Raeume`, `Teil` = `Teile`, `Buch` = `Buecher`
- **প্রথম-শব্দ**: `Autismus ADHS` ম্যাচ করে `Autismus Beruf` (একই শুরু)

### ন্যূনতম দৈর্ঘ্য
- ফাঁকবিহীন এক-শব্দের নাম: **কমপক্ষে 8 অক্ষর** (`Hand`, `Haus`, `Form` ঠেকায়)
- ফাঁকসহ নাম (যেমন `ICF Katalog`): **3 অক্ষর থেকে গ্রহণযোগ্য**
- এতে `ICF`, `ASS Frauen` ইত্যাদি অনুমোদিত থাকে

### মার্জের পর পুনঃসূচনা
প্রতিটি মার্জের পর ফোল্ডার-তালিকা নতুন করে লোড হয় এবং মার্জ-লক্ষ্য থেকে পুনরায় শুরু হয়।
যেমন `Autismus` সব সম্প্রসারণ সংগ্রহ করে তারপর এগিয়ে যায়।

---

## মিডিয়া-ফরম্যাট মার্জ (Template-সিস্টেম)

ধাপ 6 একটি Template-অ্যারে `MEDIA_TYPES` ব্যবহার করে। প্রতিটি এন্ট্রি সংজ্ঞায়িত করে:
- লক্ষ্য ফোল্ডার (`_` প্রিফিক্সসহ)
- ফাইল এক্সটেনশন যেগুলো এই ধরনের অন্তর্গত

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Bilder|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Erweiterbar:
    # "_Tabellen|xlsx|xls|csv|ods"
    # "_Prasentationen|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

শুধু সেই ফোল্ডারগুলো সরানো হয় যেগুলোতে **একচেটিয়াভাবে** একই ধরনের ফাইল থাকে।
সাবফোল্ডারসহ ফোল্ডার এড়িয়ে যাওয়া হয়।

### নতুন মিডিয়া-ধরন যোগ করা

`MEDIA_TYPES` অ্যারেতে কেবল একটি নতুন লাইন যোগ করুন:
```bash
"_Zielordner|ext1|ext2|ext3"
```

---

## কার্যকরকরণ

```bash
# Kompletter Durchlauf:
cd /pfad/zum/zielverzeichnis
bash ordner_flattening_komplett.sh

# Oder einzelne Phasen:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## সেশন 26.01.2026-এর অভিজ্ঞতালব্ধ মান

- শুরু: 206 ফোল্ডার + 252 আলগা ফাইল, ~5600 নেস্টেড সাবফোল্ডার
- ফ্ল্যাটেনিংয়ের পর: এক স্তরে ~2200 ফোল্ডার
- সংক্ষেপণ + পরিষ্কারের পর: ~2005 ফোল্ডার
- গ্রুপিংয়ের পর (সংখ্যা, CD): ~2005 -> সংগ্রহ ফোল্ডার তৈরি
- ট্রিপল v1-এর পর: ~1561 ফোল্ডার
- ট্রিপল v2-এর পর (8-অক্ষর নিয়ম): আরও হ্রাস
- মিডিয়া-ফরম্যাট ধাপ: Audio/Video/Bilder-ফোল্ডার একত্রীকৃত
