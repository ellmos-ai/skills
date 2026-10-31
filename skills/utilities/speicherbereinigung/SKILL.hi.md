---
name: speicherbereinigung
version: 1.0.0
type: skill
author: Lukas Geiger und OpenAI Codex
created: 2026-08-04
updated: 2026-08-05
description: "साक्ष्य-आधारित Windows स्टोरेज-सफ़ाई, जिसमें नियंत्रित आपातकालीन मोड, भौतिक आवंटन का मापन, प्रक्रिया- और उत्पत्ति-फ़ॉरेंसिक तथा बार-बार स्टोरेज भरने वाले कारकों के विरुद्ध पलटने योग्य उपाय शामिल हैं।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: utilities
tags: [windows, storage, cleanup, forensics, onedrive, pagefile, logs]
language: hi
status: active
visibility: public
dependencies:
  tools: [powershell]
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: "~/.codex/skills/speicherbereinigung"
  origin_version: null
  origin_repo: null
  last_sync_from_origin: 2026-08-05
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6d44ad70bc2f7abc4086474c001d33a6727d9bb6f9793333d804ad3af4907661
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="speicherbereinigung banner">

# स्टोरेज-सफ़ाई

## उद्देश्य और परिणाम

यह Skill Windows पर नियंत्रित तरीके से स्टोरेज वापस पाती है और यह रोकती है
कि वही भरने वाला पथ डिस्क को तुरंत फिर से भर दे। यह तीन चरणों में काम करती है:
आपातकालीन मुक्ति, कारण-फ़ॉरेंसिक और स्थायी सीमांकन।

हर बदलाव (Mutation) एक ही प्रोटोकॉल का पालन करता है:

`Fund -> Entscheidung -> begrenzte Ausführung -> Readback -> Messung`
(अर्थात् खोज -> निर्णय -> सीमित निष्पादन -> Readback -> माप)

यदि उपयोगकर्ता कोई उच्च लक्ष्य नहीं बताता, तो कार्य तभी पूर्ण माना जाएगा जब
अंतिम बदलाव के बाद सिस्टम वॉल्यूम फिर से कम से कम 50 GB खाली स्टोरेज दिखाए।
पहली आपातकालीन सीमा के अतिरिक्त 10 GB केवल तीव्र स्थिति समाप्त करती है, पूरा
कार्य नहीं।

## कब सक्रिय करें

इस Skill का उपयोग इन स्थितियों में करें:

- सिस्टम डिस्क में कम जगह या बार-बार जगह का खत्म होना;
- असामान्य रूप से बड़े Logs, Caches, Pagefiles, Archives या Builds;
- डुप्लिकेट Clones, Backup-पीढ़ियाँ या स्थानीय Cloud-प्रतियाँ;
- Resource-Exhaustion Events या ऐसी प्रक्रियाएँ जिनका Commit तेज़ी से बढ़ रहा हो;
- इसका संदेह कि Scheduler, Watcher या Sync-Clients डेटा फिर से बना रहे हैं।

## सुरक्षा नियम

- हर बदलाव से पहले खाली स्टोरेज, Volume, प्रक्रिया-स्थिति, Locks, Reparse Points
  और हल किया गया पूर्ण लक्ष्य-पथ जाँचें।
- पुनरावर्ती क्रियाओं में जाँचें कि लक्ष्य चुनी गई स्पष्ट मूल-रूट के भीतर है।
  अजाँचे Variables या Globs को कभी हटाने का लक्ष्य न बनाएँ।
- किसी Volume-, उपयोगकर्ता-, Repository-, Cloud- या Project-रूट को न हटाएँ।
- सक्रिय स्रोत, बिना commit का कार्य, Secrets, टकराव-प्रतियाँ, बाहरी Locks,
  `.git` और एकमात्र पुनर्स्थापन-प्रति को सुरक्षित रखें।
- Recycle Bin, Quarantine, Compression या Cloud-Dehydration को प्राथमिकता दें।
  अपरिवर्तनीय हटाना केवल एक सटीक पहचाने गए, पुनः उत्पन्न हो सकने वाले खोज के
  लिए अनुमत है; पथ, आकार और पुनर्प्राप्ति का दस्तावेज़ीकरण करें।
- Pagefile, Hibernation, Services या प्रणाली-व्यापी सीमाएँ केवल आवश्यक अधिकारों,
  Rollback और पूर्ण Readback के साथ बदलें। `Zugriff
  verweigert` (पहुँच अस्वीकृत) कोई सफल उपाय नहीं है।
- स्थानीय स्थान खाली करने के लिए OneDrive के Cloud-ऑब्जेक्ट कभी न हटाएँ।
  Cloud-हटाना और स्थानीय Dehydration अलग-अलग क्रियाएँ हैं।

## चरण 1: आपातकालीन मुक्ति

### 1. आधार-रेखा

कम से कम यह एकत्र करें:

```powershell
Get-PSDrive -Name C | Select-Object Used, Free
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID, Size, FreeSpace
Get-Process | Sort-Object PrivateMemorySize64 -Descending |
  Select-Object -First 15 Name, Id, PrivateMemorySize64, WorkingSet64
```

समय, प्रारंभिक मान और लक्ष्य दर्ज करें। `PrivateMemory` या Commit को
`WorkingSet` से अलग समझें: कोई प्रक्रिया Working Set में कम RAM दिखा सकती
है और फिर भी Pagefile को भारी मात्रा में घेर सकती है।

### 2. सीमित सूची-निर्माण

ज्ञात स्थानीय रूटों और हाल की परिवर्तन-अवधियों से शुरू करें। सभी Cloud- या
उपयोगकर्ता-निर्देशिकाओं में अंधाधुंध पुनरावर्ती खोज न करें। उपयुक्त उम्मीदवार हैं:

- स्पष्ट रूप से पुनः उत्पन्न होने योग्य Model-, Package- और Build-Caches;
- पुराने, पूर्ण हो चुके Build-आउटपुट;
- घुमाए जा सकने वाले Application-Logs;
- सत्यापित Archive- या Backup-पीढ़ियाँ;
- पूरी तरह सिंक्रोनाइज़्ड स्थानीय Cloud-प्रतियाँ।

Sparse, संपीड़ित और Cloud-प्लेसहोल्डर फ़ाइलों में फ़ाइल-लंबाई भौतिक आवंटन नहीं
है। NTFS-Allocation (`GetCompressedFileSizeW`), `compact` या समकक्ष उपकरण
का उपयोग करें और पहले/बाद के खाली स्थान की तुलना करें।

### 3. एक खोज पर कार्य

हर माप-चरण में ठीक एक खोज पर काम करें। उसके बाद जाँचें:

- वास्तव में प्राप्त बाइट्स;
- त्रुटियाँ, खुले Handles और शेष Locks;
- संरक्षित स्रोत का बने रहना;
- पुनर्स्थापन-योग्यता या पुनः उत्पन्न होने की क्षमता;
- क्या कोई प्रक्रिया उसे तुरंत फिर से बना देती है।

आपातकालीन मोड तभी समाप्त होता है जब अतिरिक्त 10 GB सिद्ध हो जाएँ। उसके बाद
प्रवाह सीधे फ़ॉरेंसिक में चला जाता है।

## चरण 2: भरने वाली प्रक्रियाओं और उत्पत्ति का फ़ॉरेंसिक निर्धारण

### 1. संसाधन-समाप्ति और Pagefile

वर्तमान और ऐतिहासिक साक्ष्य एक साथ पढ़ें:

```powershell
Get-CimInstance Win32_ComputerSystem |
  Select-Object AutomaticManagedPagefile
Get-CimInstance Win32_PageFileUsage |
  Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage
Get-WinEvent -FilterHashtable @{LogName='System'; Id=2004} -MaxEvents 20
```

Windows Resource Exhaustion Detector का Event 2004 घटना-समय पर सबसे अधिक
Commit वाली प्रक्रियाएँ दर्ज करता है। PID, प्रक्रिया-नाम, समय-चिह्न और बाइट्स
को आज की प्रक्रियाओं से मिलाएँ। किसी बड़ी `pagefile.sys` का होना अकेले यह
सिद्ध नहीं करता कि फ़ाइल स्वयं दोषी है; खोज उस प्रक्रिया की है जिसने Commit
ट्रिगर किया।

### 2. फ़ाइल-वृद्धि

नई या बदली फ़ाइलों को इनके अनुसार समूहित करें:

- निर्माण- और परिवर्तन-घंटा;
- मूल-पथ और एक्सटेंशन;
- स्वामी या उत्पन्न करने वाली प्रक्रिया;
- फ़ाइलों और भौतिक रूप से आवंटित बाइट्स में दैनिक दर।

Log-, Cache-, Sync-, Backup-, Build-, Download- और Session-निर्देशिकाओं की विशेष
जाँच करें। यदि कोई Client प्रतिदिन कई GB लिखता है और Volume छोटा है, तो सात
दिन की Retention अनुपयुक्त है।

### 3. स्वचालन

Task Scheduler, Services, Watchers और Startup-Programs की आवृत्ति, Retention और
सफलता जाँचें:

```powershell
Get-ScheduledTask | Where-Object State -ne 'Disabled'
Get-ScheduledTaskInfo -TaskName '<task-name>'
```

क्रिया, Trigger, दोहराव-अंतराल, अंतिम Return-Code और अगला रन-समय अलग-अलग
सत्यापित करें। किसी मौजूदा Task का होना इसका प्रमाण नहीं कि Retention या
आवृत्ति वास्तविक वृद्धि को नियंत्रित कर रही है।

## चरण 3: स्थायी सीमांकन

सबसे छोटा प्रभावी और पलटने योग्य उपाय चुनें:

- Log-rotation बार-बार चलाएँ और साथ में आकार-सीमा भी लगाएँ;
- किसी संदिग्ध Client को नियंत्रित रूप से पुनः आरंभ करें और उसका Commit मापें;
- Terminal Scrollback या Debug-Logging को उचित मान तक सीमित करें;
- पुराने, पुनः उत्पन्न होने योग्य Caches हटाएँ और उनके स्वचालित पुनर्निर्माण
  का अवलोकन करें;
- सत्यापित Cloud-सामग्री को “स्थान खाली करें” से Dehydrate करें;
- Scheduler-आवृत्ति और Retention को अनुभवजन्य दैनिक दर के अनुसार रखें;
- Pagefile- या Hibernation-बदलाव केवल प्रशासनिक रूप से, Reboot- और Rollback-योजना
  के साथ करें।

Windows Terminal के लिए सीमित डिफ़ॉल्ट Scrollback, उदाहरण के रूप में, ऐसा दिख
सकता है:

```json
{
  "profiles": {
    "defaults": {
      "historySize": 2000
    }
  }
}
```

मौजूदा सेटिंग्स सुरक्षित रखें और बदलाव के बाद JSON-फ़ाइल को मान्य करें।

### OneDrive-विशिष्ट गेट

Dehydration से पहले Sync-स्थिति और लंबित Uploads की जाँच होनी चाहिए। Cloud-
Filter-जागरूक फ़ाइल-प्रबंधक या Explorer-कमांड “स्थान खाली करें” का उपयोग करें।
Dehydration Cloud-सामग्री को नहीं हटाता।

स्थानीय OneDrive-Log क्षेत्र `$env:LOCALAPPDATA\Microsoft\OneDrive\logs` के अंतर्गत अलग से जाँचें। यदि
कोई उप-क्षेत्र प्रतिदिन Gigabytes उत्पन्न करता है, तो समय-आधारित Retention को
एक कठोर आकार-सीमा और पर्याप्त बार-बार चलने वाले निर्धारित रन के साथ जोड़ें।
बहुत नई या खुली फ़ाइलों की रक्षा करें और रन के बाद Task-स्थिति तथा शेष आकार
दोनों जाँचें।

## अंतिम जाँच और रिपोर्ट

अंतिम बदलाव के बाद:

1. Cloud- या हटाने की अतुल्यकालिक क्रियाओं के पूरे होने तक प्रतीक्षा करें।
2. खाली स्टोरेज और प्रक्रिया-Commit फिर से पढ़ें।
3. बदली गई कॉन्फ़िगरेशन, Tasks और Log-आकार Readback से जाँचें।
4. एक संक्षिप्त पुनःपरीक्षण चलाएँ: क्या अवलोकन-अवधि में फिर से अत्यधिक स्टोरेज
   उत्पन्न हो रहा है?
5. प्रारंभिक मान, हर खोज और उसका निर्णय, भौतिक रूप से प्राप्त बाइट्स, भरने
   वाली प्रक्रियाएँ, स्थायी समायोजन, Rollbacks, शेष जोखिम और अंतिम मान रिपोर्ट करें।

उपयुक्त वर्तमान Readback के बिना सफ़ाई, प्रक्रिया-सीमा या 50-GB-लक्ष्य की प्राप्ति
का दावा न करें।

## ज्ञात सीमाएँ

- प्रशासनिक अधिकारों के बिना Pagefile-, Hibernation- या Service-बदलाव अवरुद्ध
  रह सकते हैं। शेष सटीक चरण का दस्तावेज़ीकरण करें।
- ऐतिहासिक प्रक्रिया-Events एक पूर्ववर्ती भरने वाले को सिद्ध करते हैं; वर्तमान
  स्थिति के लिए प्रक्रिया- और फ़ाइल-वृद्धि के आँकड़े भी चाहिए।
- एक नियोजित Backup-अवधारणा Backup नहीं है। स्थानांतरण या हटाने के लिए वर्तमान
  लक्ष्य-पहचान, Manifest या Hash, Restore-प्रमाण और Mount आवश्यक हैं।
- अस्पष्ट स्वामित्व, चल रहे बाहरी कार्य या अज्ञात लक्ष्य की स्थिति में निर्णय
  `nichts` (अर्थात् कुछ नहीं) लागू होता है।

## Changelog

### 1.0.0 (2026-08-05)

- केंद्रीय Skill-संग्रह के लिए पोर्टेबल प्रारंभिक संस्करण।
- संसाधन-समाप्ति, Pagefile- और प्रक्रिया-फ़ॉरेंसिक जोड़ी गई।
- भौतिक NTFS-आवंटन और OneDrive-Dehydration स्पष्ट रूप से अलग किए गए।
- समय- और आकार-सीमा के साथ OneDrive-Log-rotation शामिल की गई।
- Readback के साथ कठोर आपातकालीन और अंतिम गेट परिभाषित किए गए।
