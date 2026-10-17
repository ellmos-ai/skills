---
name: grilling
description: "কোনো পরিকল্পনা, সিদ্ধান্ত বা ধারণা নিয়ে ব্যবহারকারীকে নিরলসভাবে প্রশ্ন করুন। যখন ব্যবহারকারী তাদের চিন্তাভাবনাকে চাপের মুখে যাচাই করতে চান, অথবা যেকোনো 'grill' ট্রিগার বাক্যাংশ ব্যবহার করেন, যেমন \"আমাকে গ্রিল করো\" বা \"আমার পরিকল্পনা নিয়ে আমাকে কড়া প্রশ্ন করো\" -- যার মধ্যে \"grill mich\", \"grill mich zu diesem Plan\" বা \"zerpflück meinen Plan im Grill-Modus\" এর মতো জার্মান বাক্যাংশও অন্তর্ভুক্ত -- তখন এটি ব্যবহার করুন। /grill-me কমান্ডের প্রবেশবিন্দু; সরাসরিও আহ্বান করা যায়।"
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: bn
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

ব্যবহারকারীর সাথে একটি পারস্পরিক বোঝাপড়ায় পৌঁছানো পর্যন্ত ব্যবহারকারীকে নিরলসভাবে প্রশ্ন করুন। এটিকে একটি **ডিজাইন ট্রি** হিসেবে মানচিত্রায়িত করুন: প্রতিটি সিদ্ধান্ত তার উপর নির্ভরশীল সিদ্ধান্তগুলোতে শাখাবিস্তার করে।

ট্রিটি **রাউন্ড**-এ কাজ করুন। **ফ্রন্টিয়ার** হলো এমন প্রতিটি সিদ্ধান্ত যার পূর্বশর্তগুলো ইতোমধ্যে নিষ্পন্ন হয়েছে: যেসব প্রশ্ন আপনি _এখনই_ করতে পারেন, উত্তর না শুনে অনুমান না করে। পুরো ফ্রন্টিয়ার একটি রাউন্ডে জিজ্ঞাসা করুন: প্রতিটি প্রশ্নকে ক্রমিক নম্বর দিন এবং আপনার প্রস্তাবিত উত্তর দিন। তারপর পরবর্তী রাউন্ডের আগে ব্যবহারকারীর উত্তরের জন্য অপেক্ষা করুন।

একটি রাউন্ড এভাবে বিন্যস্ত করুন:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

ব্যবহারকারীর প্রতিটি উত্তর ট্রিটিকে নতুনভাবে গড়ে তোলে: নিষ্পন্ন সিদ্ধান্তগুলো ফ্রন্টিয়ারকে বাইরের দিকে ঠেলে দেয় এবং এমন প্রশ্নগুলোকে উন্মুক্ত করে যেগুলো সেগুলোর উপর নির্ভরশীল ছিল। ফ্রন্টিয়ার পুনর্গণনা করুন এবং পরবর্তী রাউন্ড জিজ্ঞাসা করুন। যে প্রশ্নের উত্তর এই রাউন্ডের অন্য একটি এখনও খোলা প্রশ্নের উপর নির্ভর করে, সেটি এই রাউন্ডে নয়, বরং _পরবর্তী_ কোনো রাউন্ডে থাকবে।

_তথ্য_ খুঁজে বের করা আপনার দায়িত্ব, ব্যবহারকারীর নয়। কোনো ফ্রন্টিয়ার প্রশ্নের জন্য পরিবেশ থেকে (ফাইলসিস্টেম, টুল ইত্যাদি) কোনো তথ্য প্রয়োজন হলে, তা খুঁজে বের করতে একটি সাব-এজেন্ট পাঠান; আপনি নিজে যা খুঁজে নিতে পারেন তার জন্য ব্যবহারকারীকে জিজ্ঞাসা করবেন না। এর জন্য থেমে থাকবেন না: চলমান অনুসন্ধান একটি অনিষ্পন্ন পূর্বশর্ত, তাই শুধু এর উপর নির্ভরশীল প্রশ্নগুলোই সাব-এজেন্টের প্রতিবেদনের জন্য অপেক্ষা করবে; বাকি ফ্রন্টিয়ার এখনই জিজ্ঞাসা করুন। _সিদ্ধান্তগুলো_ ব্যবহারকারীর: সেগুলো তাদের সামনে রাখুন এবং অপেক্ষা করুন।

সেশনটি সম্পন্ন হয় যখন ফ্রন্টিয়ার খালি হয়: ডিজাইন ট্রির প্রতিটি শাখা পরিদর্শন করা হয়েছে, এবং নীরবে ধরে নেওয়া কিছু অবশিষ্ট নেই। ব্যবহারকারী নিশ্চিত না করা পর্যন্ত যে পারস্পরিক বোঝাপড়ায় পৌঁছানো হয়েছে, কোনো পদক্ষেপ নেবেন না।

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Modification vs. upstream: the `description` field was extended with German
trigger phrases ("grill mich"). The `category` and `language` fields and this
comment were added; all are local convention (recommended, not one of the
nine house fields), not upstream content, and `language: en` reflects that
the vendored body is unmodified English. The body (the design tree / frontier
/ rounds method) is unchanged from upstream.

Adopted 2026-08-24 per Ticket T-20260824-594031458 alongside skills/third-
party/grill-me/ (the thin, explicit-only entry point that calls this skill).
-->
