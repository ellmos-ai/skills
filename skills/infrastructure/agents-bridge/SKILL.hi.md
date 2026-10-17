---
name: agents-bridge
version: 3.0.1
type: skill
author: Lukas Geiger + Codex
created: 2026-07-04
updated: 2026-08-22
description: "agents-bridge — the Lifeboat, उर्फ़: Time Capsule। पोर्टेबल, प्रदाता-तटस्थ फ़ाइल ब्रिज, जो बूटस्ट्रैप सतहों, सत्य-पॉइंटर, अलग मेमोरी साइलो, मैसेजिंग, प्रेज़ेंस, सहकारी लॉक और उलटने योग्य होस्ट रिकवरी के लिए है।"
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [multi-agent, bootstrap, recovery, messaging, memory, provider-neutral]
language: hi
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
translated_from_sha256: 332b9782849063f2901c750f364f3d66446b1f1f236d8fd8a6f5b67e9757e2f5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:10.357571+00:00"
---
<img src="banner.png" width="100%" alt="agents-bridge banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# AGENTS-BRIDGE — the Lifeboat, उर्फ़: Time Capsule (हिन्दी)

> **उपनाम „Lifeboat" (जर्मन में Rettungsboot, यानी बचाव नाव) और „Time Capsule":** agents-bridge
> एजेंट नियम-फ़ाइलों (CLAUDE.md/
> GEMINI.md/GPT.md/AGENTS.md) का पुनर्स्थापना-सेट है — यह कार्य पहले किसी पहचानने योग्य नाम के बिना होता था। „Lifeboat" ब्रिज वाले रूपक के नौचालन-नाम परिवार (Wheelhouse, Deep-Diver, Lower Decks) में बैठता है; „Time Capsule" उसी कार्य के दूसरे पक्ष पर ज़ोर देता है — एक सीलबंद, हैश-सत्यापित स्थिति जिसे बाद में अक्षुण्ण रूप से बहाल किया जा सकता है। कोई पुनर्नामकरण नहीं: तकनीकी नाम `agents-bridge` ही रहता है, दोनों उपनाम अर्थपूर्ण समानार्थी हैं।

इस स्किल का उपयोग एक छोटे फ़ाइल-आधारित मल्टी-प्रदाता सिस्टम को कैप्चर, जाँचने, स्थानांतरित करने या पुनर्स्थापित करने के लिए करें। प्रति इंस्टेंस ठीक एक स्पष्ट रूप से चुनी गई मुख्य प्रदाता-फ़ाइल होती है। कोई प्रदाता, फ़ाइल-नाम, होस्ट या क्लाउड-डायरेक्टरी अंतर्निहित रूप से प्रामाणिक नहीं है।

## कार्यप्रवाह और कार्यविधि

1. स्रोत और लक्ष्य के सभी स्थानीय निर्देश, लॉक और गोपनीयता-नियम पढ़ें। बाहरी परिवर्तनों को सुरक्षित रखें।
2. `python scripts/bridge.py discover --root <instanz>` चलाएँ। `discover` केवल एक स्पष्ट मार्कर `agents-bridge-primary: true` ग्रहण कर सकता है। कोई दावा न होने या एक से अधिक दावे होने पर वर्कफ़्लो एक निर्णय-ब्रीफ़िंग के साथ रुक जाता है; फ़ाइल-नाम का कोई डिफ़ॉल्ट नहीं है।
3. `references/profile-v3.schema.json` के अनुसार एक प्रोफ़ाइल बनाएँ। इसमें मुख्य सतह, प्रदाता-सतहें, सत्य-स्रोत, पॉइंटर-ग्राफ़, रिकवरी, मेमोरी-साइलो, मैसेंजर, प्रेज़ेंस, लॉक तथा गोपनीयता-Includes/-Excludes का नाम होता है।
4. प्रोफ़ाइल जाँचें और स्रोत में बदलाव किए बिना इंस्टेंस कैप्चर करें:

   ```text
   python scripts/bridge.py profile-validate --profile <profil.json>
   python scripts/bridge.py capture --profile <profil.json> --root <quelle> --output <neues-paket>
   ```

5. `doctor` से पैकेज जाँचें और `--apply` के बिना `plan` या `restore` से एक पूर्वावलोकन बनाएँ। मौजूदा फ़ाइलें कभी अंधाधुंध अधिलेखित नहीं होतीं।
6. `--apply --yes --backup-dir
   <backup> --receipt <receipt.json>` से जाँच के बाद ही रीस्टोर लागू करें। इसके बाद `verify` और Claude, Codex/GPT, Gemini या तटस्थ प्रदाता के लिए एक वास्तविक नेटिव पठन-परीक्षण करें।
7. त्रुटियों पर: ड्रिफ़्ट स्पष्ट करें या `rollback --yes` से ठीक वही रसीद वापस रोल करें। दूसरा रीस्टोर `idempotent` रिपोर्ट करना चाहिए।
8. `message send|ack|status`, `memory`, `presence` और `lock claim|release|status` का उपयोग केवल छोटे फ़ाइल-अनुबंधों के रूप में करें। मैसेंजर न तो Ticket-Master की जगह लेता है, न Scheduler की; मेमोरी-साइलो कभी स्वचालित रूप से मर्ज नहीं होते।

## सुरक्षा सीमाएँ

- लोडर या रीडायरेक्ट को प्राथमिकता दी जाती है। प्रोजेक्शन तभी स्वीकार्य है जब नेटिव संदर्भ काम न करें; उसमें स्रोत-हैश, उत्पत्ति, `generated_at` और एक ड्रिफ़्ट-पहचानकर्ता शामिल होता है। नियंत्रित पुनर्निर्माण केवल `capture --regenerate-projections` के साथ एक नए पैकेज में होता है।
- सभी प्रोफ़ाइल-पथ UTF-8-एन्कोडेड, सापेक्ष और प्लेटफ़ॉर्म-तटस्थ हैं। एक्सपोर्ट मैनिफ़ेस्ट-युक्त और Includes/Excludes तक सीमित हैं।
- Secrets, Credentials और व्यक्तिगत निरपेक्ष पथ फ़ेल-क्लोज़्ड रूप से अस्वीकार किए जाते हैं या स्पष्ट `redact`-मोड में लॉग करके बदले जाते हैं।
- यदि Controlroom मौजूद है, तो समन्वय का अधिकार वही रहता है। `agents-bridge` तब केवल बूटस्ट्रैप-, रिकवरी- और फ़ाइल-एडाप्टर है और कोई केंद्रीय रनटाइम नहीं दोहराता।

अनुबंध और उदाहरण `references/contracts.de.md`, `references/truth-topologies.md`, `references/inventory-contract.md` और `references/migration-2-to-3.de.md` में हैं। अंग्रेज़ी संस्करण `SKILL.en.md` है।
