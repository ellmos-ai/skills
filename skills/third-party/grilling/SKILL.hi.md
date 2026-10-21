---
name: grilling
description: "किसी योजना, निर्णय या विचार के बारे में उपयोगकर्ता से निर्मम प्रश्न पूछें। जब उपयोगकर्ता अपनी सोच की कसौटी लेना चाहता हो, या कोई भी 'grill' ट्रिगर वाक्यांश प्रयोग करे—जिसमें \"grill mich\", \"grill mich zu diesem Plan\" या \"zerpflück meinen Plan im Grill-Modus\" जैसे जर्मन वाक्यांश, तथा 'मुझे ग्रिल करो', 'इस योजना पर मुझे ग्रिल करो' और 'ग्रिल मोड में मेरी योजना की धज्जियाँ उड़ाओ' जैसे हिंदी वाक्यांश भी शामिल हैं—तब इसका उपयोग करें। यह /grill-me कमांड के लिए प्रवेश बिंदु है; इसे सीधे भी आमंत्रित किया जा सकता है।"
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: hi
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

उपयोगकर्ता के साथ साझा समझ तक पहुँचने तक बिना रुके, निर्ममता से साक्षात्कार लें। इसे एक **डिज़ाइन ट्री** के रूप में मानचित्रित करें: हर निर्णय उन निर्णयों में शाखाएँ बनाता है जो उससे जुड़े होते हैं।

इस ट्री पर **राउंड** में काम करें। **फ्रंटियर** वह हर निर्णय है जिसकी पूर्वापेक्षाएँ पहले ही तय हो चुकी हैं: वे प्रश्न जिन्हें आप _अभी_ पूछ सकते हैं, बिना उन उत्तरों का अनुमान लगाए जो आपने अभी तक नहीं सुने हैं। पूरे फ्रंटियर को एक राउंड में पूछें: हर प्रश्न को क्रमांकित करें और अपना अनुशंसित उत्तर दें। फिर अगले राउंड से पहले उपयोगकर्ता के उत्तरों की प्रतीक्षा करें।

एक राउंड को इस प्रकार प्रारूपित करें:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

हर राउंड में उपयोगकर्ता का उत्तर डिज़ाइन ट्री को नया आकार देता है: तय हुए निर्णय फ्रंटियर को बाहर की ओर धकेलते हैं और उन प्रश्नों को अवरोध हटा देते हैं जो उन पर निर्भर थे। फ्रंटियर की फिर से गणना करें और अगला राउंड पूछें। जो प्रश्न किसी ऐसे दूसरे प्रश्न पर निर्भर है जो इस राउंड में अभी भी खुला है, वह इस राउंड का नहीं, बल्कि _बाद के_ राउंड का हिस्सा है।

_तथ्य_ खोजना आपका काम है, उपयोगकर्ता का नहीं। जब कोई फ्रंटियर प्रश्न पर्यावरण (फ़ाइल सिस्टम, टूल आदि) से किसी तथ्य की माँग करता है, तो उसे खोजने के लिए एक उप-एजेंट भेजें; उन चीज़ों के लिए उपयोगकर्ता से न पूछें जिन्हें आप स्वयं देख सकते हैं। उस पर रुकें नहीं: चल रही खोज एक अनसुलझी पूर्वापेक्षा है, इसलिए केवल उसके बाद आने वाले प्रश्न ही उप-एजेंट की रिपोर्ट की प्रतीक्षा करेंगे; शेष फ्रंटियर को अभी पूछें। _निर्णय_ उपयोगकर्ता के हैं: हर एक उनके सामने रखें और उत्तर की प्रतीक्षा करें।

सत्र तब पूरा होता है जब फ्रंटियर खाली हो जाए: डिज़ाइन ट्री की हर शाखा देखी जा चुकी हो, और कुछ भी चुपचाप मान न लिया गया हो। जब तक उपयोगकर्ता पुष्टि न करे कि आप साझा समझ तक पहुँच चुके हैं, तब तक उस पर कार्य न करें।

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
