---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "automation-self-care को लेटर हुक्स, प्रीफ्लाइट बूटलोडर, दस्तावेज़-ट्रैवर्सल नियमों और स्व-उपचार प्रॉम्प्ट-संदर्भ संवर्धन के साथ विस्तारित करता है, उन AI एजेंटों और CLIs के लिए जिनमें मूल, इवेंट-संचालित JSON लाइफ़साइकिल हुक्स नहीं हैं (जैसे Antigravity / Gemini CLI)। इसका उपयोग तब करें जब किसी एजेंट को प्रीफ्लाइट नियम इंजेक्ट करने हों, कार्य शुरू करने से पहले Memory/Gardener खंगालना हो, निर्देशिका-दस्तावेज़ पढ़ने की रणनीतियाँ (CLAUDE.md / AGENTS.md) लागू करनी हों, या साइडकार टास्क्स को गतिशील रूप से Skills और सुरक्षा प्रोटोकॉल की ओर रूट करना हो।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: hi
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: [agy_kontext_and_workflow_loader.py]
provenance:
  origin: "fork of automation-self-care"
  origin_path: "skills/infrastructure/automation-self-care"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: cb03d9a06cc52ced2695c952c855b3d57c168dc5b0a9ad1c412e72da13de1765
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:34:32.408049+00:00"
---
<img src="banner.png" width="100%" alt="letter-hooker banner">

# Letter-Hooker (प्रॉम्प्ट-स्तर प्रीफ्लाइट और गवर्नेंस इंजन)

**Letter-Hooker** Skill `automation-self-care` को उन AI एजेंट फ्रेमवर्क्स (जैसे **Antigravity / Gemini CLI**) के लिए विस्तारित करती है, जिनमें मूल, इवेंट-संचालित JSON लाइफ़साइकिल हुक लोडर नहीं होते (उदाहरण के लिए `~/.claude/settings.json` या `~/.codex/hooks.json`)।

निष्क्रिय, प्रति-कीस्ट्रोक हुक्स पर निर्भर रहने के बजाय, `letter-hooker` निर्धारित टास्क्स और मेंटेनर स्क्रिप्ट्स (`agy_kontext_and_workflow_loader.py`) के माध्यम से एक **सक्रिय प्रॉम्प्ट-स्तर प्रीफ्लाइट बूटलोडर और Letter-Hook इंजेक्शन लूप** चलाती है।

---

## मुख्य क्षमताएँ

1. **प्रीफ्लाइट बूटलोडर और दस्तावेज़-ट्रैवर्सल नियम**:
   - **ऊपर और नीचे की खोज**: एजेंटों के लिए सख़्त निर्देश लागू करती है कि वे वर्तमान कार्य-निर्देशिका स्तर पर `AGENTS.md`, `CLAUDE.md`, `START.md`, `RULES.md` और `README.md` की जाँच करें। यदि ये न मिलें, तो मिलने तक ऊपर की ओर ट्रैवर्स करें; फिर नीचे की ओर जाँच करें।
   - **Memory और Gardener प्रीफ्लाइट**: विनाशकारी या जटिल बदलाव करने से पहले `gardener` और `memoryhooker` पर अनिवार्य प्रीफ्लाइट क्वेरी।

2. **Letter-Hooks कैटलॉग और संदर्भ लिंक**:
   - `.md` के मॉड्यूलर निर्देश फ़ाइलें `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/` के अंतर्गत।
   - `sidecar.json` प्रॉम्प्ट-टेक्स्ट में सीधे स्पष्ट `file://` लिंक इंजेक्ट करती है, ताकि आह्वान पर एजेंट सटीक सुरक्षा और वर्कफ़्लो प्रोटोकॉल पढ़ सकें।

3. **दैनिक कीवर्ड सूची और स्व-उपचार प्रॉम्प्ट संवर्धन**:
   - सक्रिय/स्टैंडबाय टास्क्स से एक दैनिक `STICHWORTLISTE.json` बनाए रखती है।
   - त्रुटि पैटर्न (लापता संदर्भ, लापता वर्कफ़्लो मार्गदर्शन, अमान्य पथ) के लिए निष्पादन लॉग (`AUTOMATIONS-MEMORY.md`) का विश्लेषण करती है और टास्क प्रॉम्प्ट्स को गतिशील रूप से पैच करती है।

4. **Skill और Persona रूटिंग**:
   - टास्क कीवर्ड्स की जाँच करती है और उन्हें उपयुक्त `.SKILLS` से मैप करती है (जैसे `infrastructure/condition`, `semantic-persona-routing`, `orchestrator`, `think`, `decide`)।

---

## मुख्य Letter Hooks

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](hooks/path_validation_and_authority.md)

---

## वर्कफ़्लो एकीकरण

```bash
# Letter-Hooker-Wartungs-Engine ausführen
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **साइडकार स्कैन करें**: `~/.gemini/config/sidecars/` में सभी `sidecar.json` प्रॉम्प्ट-टेक्स्ट पढ़ें।
2. **कीवर्ड सूची अपडेट करें**: तकनीकी शब्द निकालें और `.SYNC/STICHWORTLISTE.json` में सहेजें।
3. **Letter Hooks इंजेक्ट करें**: बूटलोडर नियम और `file://` संदर्भ लिंक प्रॉम्प्ट्स में जोड़ें।
4. **परिणाम लॉग करें**: अपडेट `ANTIGRAVITY-LOG.txt` और `ANTIGRAVITY-REGISTRY.md` में दर्ज करें।
