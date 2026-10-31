---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "wttr.in के माध्यम से किसी स्थान या निर्देशांकों के लिए मौसम संबंधी प्रश्नों के उत्तर देता है (मुफ़्त, किसी API कुंजी की आवश्यकता नहीं)। वर्तमान मौसम + 3-दिन का पूर्वानुमान। स्थान उपयोगकर्ता के अनुरोध या प्राथमिकताओं से आता है; वैकल्पिक संक्षिप्त कैश।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: hi
status: active
visibility: public
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 77159e7ab4dc0541cb58d038cfb353076dc2d32699dba8cd2e69761042b86b8c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.555977+00:00"
---
<img src="banner.png" width="100%" alt="wetter banner">

# मौसम

दैनिक उपयोग के लिए तेज़, कुंजी-मुक्त मौसम जानकारी।

## उद्देश्य

बिना API कुंजी के „मौसम कैसा रहेगा?" जैसे प्रश्नों के उत्तर देता है (डेटा स्रोत: wttr.in)।
वर्तमान मौसम (तापमान, महसूस होने वाला तापमान, हवा, आर्द्रता, UV) के साथ एक संक्षिप्त
3-दिन का पूर्वानुमान प्रदान करता है। **उपयोगकर्ता-तटस्थ:** कोड में कोई निश्चित स्थान नहीं है — स्थान
अनुरोध से आता है या `assist/prefs.json` (`wetter_default_location`) से, जिसे LLM उपयोगकर्ता के साथ
इंटरैक्टिव रूप से भरता है।

## ट्रिगर

| उपयोगकर्ता इनपुट | कार्रवाई |
|---|---|
| „पॉट्सडैम का मौसम?" / „हैम्बर्ग में मौसम कैसा रहेगा?" | `wetter_core.py "<Ort>"` |
| „कल का मौसम?" (बिना स्थान के) | `wetter_core.py --default` (प्राथमिकताओं से स्थान) |
| „मेरा डिफ़ॉल्ट मौसम स्थान पॉट्सडैम है" | `wetter_core.py --set-default "Potsdam"` |
| निर्देशांक ज्ञात हैं | `wetter_core.py <lat> <lon>` |

## कार्यप्रवाह

```
1. Ort bestimmen: aus Anfrage; sonst prefs.json (wetter_default_location);
   sonst Nutzer interaktiv fragen + optional als Default speichern.
2. wetter_core.py abfragen (wttr.in, 2 Versuche, 30-min-Cache).
3. Lesbaren Wetter-Text + 3-Tage-Vorschau praesentieren.
```

## CLI प्रवेश (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # Ort
python wetter_core.py 52.6789 13.5878   # Koordinaten
python wetter_core.py --default         # Ort aus prefs.json
python wetter_core.py --set-default "Potsdam"
```

## स्टोर (वैकल्पिक)

- **कोई अनिवार्य स्टोर नहीं।** वैकल्पिक अल्पकालिक कैश `assist/wetter/.cache.json`
  (TTL 30 मिनट, सर्वोत्तम प्रयास) — बार-बार नेटवर्क अनुरोधों से बचाता है।
- स्थान प्राथमिकता `assist/prefs.json` में संग्रहीत (`wetter_default_location`)।

## दृष्टिकोण

हम wttr.in को कुंजी-मुक्त डिफ़ॉल्ट स्रोत के रूप में उपयोग करते हैं, लेकिन यदि उपयोगकर्ता चाहे तो
अन्य मौसम बैकएंड (जैसे DWD/OpenWeather) के लिए भी खुले हैं।

## डेटा गोपनीयता

- केवल स्थान का नाम/निर्देशांक wttr.in को भेजे जाते हैं (अनुरोध के लिए आवश्यक)।
- कोई टेलीमेट्री नहीं, कोई खाता नहीं। कैश और प्राथमिकता स्थानीय रहते हैं।

## संबंधित संसाधन

- `assist/AGENTS.md` — अंब्रेला राउटर
- `assist/reiseroute/` — यात्रा योजना के लिए मौसम का उपयोग कर सकता है (नियोजित)

## परिवर्तन लॉग

### 0.1.0 (2026-06-22)
- प्रारंभिक संस्करण। BACH `hub/_services/weather/weather_service.py` (MIT) से पोर्ट किया गया।
- विस्तारित: स्थान नाम समर्थन (केवल निर्देशांक नहीं), 3-दिन का पूर्वानुमान,
  वैकल्पिक कैश, प्राथमिकता-आधारित डिफ़ॉल्ट स्थान। उपयोगकर्ता-तटस्थ।
