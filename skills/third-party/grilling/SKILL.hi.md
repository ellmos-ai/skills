---
name: grilling
description: "किसी योजना, निर्णय या विचार के बारे में उपयोगकर्ता से लगातार तीखे प्रश्न पूछें। जब उपयोगकर्ता अपनी सोच को परखना चाहे, “grill me” या “grill-me” कहे (पुराने /grill-me कमांड की जगह अब /grilling है), या “grill” वाला कोई अन्य ट्रिगर वाक्यांश कहे—जर्मन “grill mich”, “grill mich zu diesem Plan”, “zerpflück meinen Plan im Grill-Modus” और हिंदी “मुझे ग्रिल करो”, “इस योजना पर मुझे ग्रिल करो”, “ग्रिल मोड में मेरी योजना की धज्जियाँ उड़ाओ” सहित—तब इसका उपयोग करें। योजना-सत्र समाप्त होने पर उपयोगकर्ता पूछे कि क्या कुछ अभी खुला है, तब भी इसका उपयोग करें।"
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: hi
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
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

## स्थानीय पूरक नियम

ये नियम मूल पद्धति को बढ़ाते हैं; उसे बदलते नहीं हैं।

1. **जो पहले से लिखा है, उसी से शुरुआत करें।** पहले दौर से पहले योजना और वह स्थान पढ़ें जहाँ परियोजना अपने निर्णय दर्ज करती है। हर उस बिंदु को इकट्ठा करें जो अभी खुला, प्रस्तावित या अपुष्ट है। तय हो चुके बिंदु को फिर न पूछें; उसके रिकॉर्ड का संदर्भ दें।
2. **अगले दौर से पहले हर उत्तर दर्ज करें।** परियोजना के निर्णय-रिकॉर्ड में हर उत्तर को तारीख और स्रोत के साथ तय निर्णय के रूप में लिखें। जो उत्तर केवल चैट में है, वह अगला संदर्भ रीसेट होने पर खो जाता है।
3. **रुकावट पर विराम दें, फिर से शुरू न करें।** यदि उपयोगकर्ता पहले कोई दूसरा काम करने को कहे, तो वह करें और फिर बाकी खुले प्रश्नों से आगे बढ़ें। तय प्रश्न तय ही रहते हैं।
4. **हर सिफारिश के पीछे एक कारण दें।** अनुशंसित उत्तर और उसके आधार में मौजूद एक तथ्य या नियम बताएं। उपयोगकर्ता की पुष्टि तक सिफारिश निर्णय नहीं होती।
5. **जाँचे गए तथ्य दिखाएं।** यदि कोई प्रश्न वातावरण से खोजी गई जानकारी पर निर्भर है, तो निष्कर्ष और उसका स्रोत बताएं, ताकि उपयोगकर्ता प्रमाण के आधार पर निर्णय ले।
6. **उपयोगकर्ता की भाषा में पूछें।** प्रश्न और सिफारिशें उपयोगकर्ता की भाषा में हों; पहचानकर्ता जस के तस रहें।
7. **अंत में निर्णय-सूची दें।** फ्रंटियर खाली होने पर तय हुई बातों और जानबूझकर खुली छोड़ी गई बातों को सूचीबद्ध करें, फिर साझा समझ की पुष्टि मांगें।

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Improved fork. Modifications vs. upstream:
- `description`: German trigger phrases ("grill mich"), the "grill me" /
  "grill-me" phrases, and the end-of-planning trigger were added.
- `category`, `language` and this comment were added (local convention).
- "Local additions" (rules 1-7) were appended after the upstream body. The
  upstream body above that heading is unchanged, so a resync only needs to
  replace that part.

Adopted 2026-08-24 per Ticket T-20260824-594031458, together with the thin
entry point skills/third-party/grill-me/ (upstream
skills/productivity/grill-me, `disable-model-invocation: true`, body
"Call the Skill tool with grilling"). On 2026-10-25 grill-me was removed at
the user's request: one skill instead of two, the phrase triggers moved into
this description. The native /grill-me command no longer exists; /grilling
replaces it. The description only adds semantic matching and registers no
alias command. Rules 1-7 come from a planning session of the same day.
-->
