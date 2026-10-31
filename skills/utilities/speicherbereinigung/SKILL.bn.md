---
name: speicherbereinigung
version: 1.0.0
type: skill
author: Lukas Geiger und OpenAI Codex
created: 2026-08-04
updated: 2026-08-05
description: "উইন্ডোজের স্টোরেজ পরিষ্কারের জন্য প্রমাণ-ভিত্তিক পদ্ধতি, নিয়ন্ত্রিত জরুরি মোড, ভৌত ব্যবহার পরিমাপ, প্রক্রিয়া ও উৎপত্তি বিশ্লেষণ, এবং বারবার স্টোরেজ ভরাটকারীদের বিরুদ্ধে প্রত্যাবর্তনযোগ্য ব্যবস্থা।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: utilities
tags: [windows, storage, cleanup, forensics, onedrive, pagefile, logs]
language: bn
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
translated_at: "2026-10-15T11:49:46.444624+00:00"
---
<img src="banner.png" width="100%" alt="speicherbereinigung banner">

# Speicherbereinigung

## Zweck und Ergebnis

এই স্কিলটি উইন্ডোজে নিয়ন্ত্রিতভাবে স্টোরেজ পুনরুদ্ধার করে এবং নিশ্চিত করে যে একই ভরাট পথ ডিস্কটিকে অবিলম্বে আবার পূর্ণ করতে না পারে। এটি তিনটি ধাপে কাজ করে: জরুরি মুক্তকরণ, কারণ-বিশ্লেষণ এবং স্থায়ী সীমাবদ্ধতা।

প্রতিটি পরিবর্তন একই প্রোটোকল অনুসরণ করে:

`Fund -> Entscheidung -> begrenzte Ausführung -> Readback -> Messung`

যদি ব্যবহারকারী কোনো উচ্চতর লক্ষ্য উল্লেখ না করেন, তবে শেষ পরিবর্তনের পরে সিস্টেম ভলিউম আবার অন্তত 50 GB খালি স্টোরেজ জানালে তবেই কাজটিকে সম্পন্ন ধরা হবে। প্রথম জরুরি সীমা হিসেবে অতিরিক্ত 10 GB শুধুমাত্র তাৎক্ষণিক অবস্থা শেষ করে, সামগ্রিক কাজ নয়।

## Wann aktivieren

এই স্কিলটি ব্যবহার করুন:

- সীমিত সিস্টেম ডিস্ক বা বারবার স্থান হারানোর ক্ষেত্রে;
- অস্বাভাবিকভাবে বড় লগ, ক্যাশ, Pagefile, আর্কাইভ বা বিল্ডের ক্ষেত্রে;
- ডুপ্লিকেট ক্লোন, ব্যাকআপ প্রজন্ম বা স্থানীয় ক্লাউড কপির ক্ষেত্রে;
- রিসোর্স-নিঃশেষ ইভেন্ট বা দ্রুত বর্ধনশীল Commit সহ প্রক্রিয়ার ক্ষেত্রে;
- সন্দেহ হলে যে Scheduler, Watcher বা Sync-Client ডেটা পুনরায় তৈরি করছে।

## Sicherheitsregeln

- প্রতিটি পরিবর্তনের আগে খালি স্টোরেজ, ভলিউম, প্রক্রিয়ার অবস্থা, Locks, Reparse Points এবং সমাধান করা নিরঙ্কুশ লক্ষ্য পথ নির্ধারণ করুন।
- পুনরাবৃত্ত কাজে নিশ্চিত করুন যে লক্ষ্যটি স্পষ্টভাবে নির্বাচিত মূলের ভেতরে আছে। যাচাই ছাড়া ভেরিয়েবল বা Glob কখনো মুছে ফেলার লক্ষ্য হিসেবে ব্যবহার করবেন না।
- কোনো Volume-, Benutzer-, Repository-, Cloud- বা Projektmূল মুছবেন না।
- সক্রিয় সূত্র, অকমিট কাজ, Secrets, সংঘাতের কপি, বাইরের Locks, `.git` এবং একমাত্র পুনরুদ্ধার কপি সংরক্ষণ করুন।
- Papierkorb, Quarantäne, Kompression বা Cloud-Dehydrierung পছন্দ করুন। অপরিবর্তনীয় মোছা শুধুমাত্র সুনির্দিষ্টভাবে চিহ্নিত, পুনরুৎপাদনযোগ্য একটি ফলাফলের জন্য অনুমোদিত; পথ, আকার ও পুনরুদ্ধার নথিভুক্ত করুন।
- Pagefile, Ruhezustand, Dienste বা সিস্টেমব্যাপী সীমা শুধুমাত্র প্রয়োজনীয় অধিকার, Rollback এবং সম্পূর্ণ Readback সহ পরিবর্তন করুন। `Zugriff
  verweigert` কোনো সফল ব্যবস্থা নয়।
- স্থানীয় স্টোরেজ মুক্ত করতে কখনো OneDrive-Cloudobjekte মুছবেন না। Cloud-Löschung এবং lokale Dehydrierung ভিন্ন অপারেশন।

## Phase 1: Notfallfreigabe

### 1. Baseline

ন্যূনতম এগুলো সংগ্রহ করুন:

```powershell
Get-PSDrive -Name C | Select-Object Used, Free
Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" |
  Select-Object DeviceID, Size, FreeSpace
Get-Process | Sort-Object PrivateMemorySize64 -Descending |
  Select-Object -First 15 Name, Id, PrivateMemorySize64, WorkingSet64
```

সময়, প্রারম্ভিক মান এবং লক্ষ্য লিখে রাখুন। `PrivateMemory` এবং `WorkingSet`-এর Commit আলাদা করুন: কোনো প্রক্রিয়া Working Set-এ কম RAM দেখাতে পারে, তবুও Pagefile-এ বড় পরিমাণ দখল করতে পারে।

### 2. Begrenzt inventarisieren

পরিচিত স্থানীয় মূল এবং সাম্প্রতিক পরিবর্তনের সময়সীমা দিয়ে শুরু করুন। সমস্ত Cloud- বা Benutzerverzeichnisে অন্ধভাবে পুনরাবৃত্তি করে খুঁজবেন না। উপযুক্ত প্রার্থী হলো:

- স্পষ্টভাবে পুনরুৎপাদনযোগ্য Modell-, Paket- ও Build-Caches;
- পুরোনো, সম্পন্ন Buildausgaben;
- ঘূর্ণনযোগ্য Anwendungslogs;
- যাচাইকৃত Archiv- বা Backup-Generationen;
- সম্পূর্ণভাবে সিঙ্ক্রোনাইজড স্থানীয় Cloudkopien।

Sparse, সংকুচিত এবং Cloud-Platzhalter ফাইলে ফাইলের দৈর্ঘ্য ভৌত দখল নয়। NTFS-Allocation (`GetCompressedFileSizeW`), `compact` বা সমতুল্য টুল ব্যবহার করুন এবং আগে-পরে খালি স্থান তুলনা করুন।

### 3. Einen Fund bearbeiten

প্রতি মাপের ধাপে ঠিক একটি ফলাফল প্রক্রিয়া করুন। এরপর যাচাই করুন:

- প্রকৃতপক্ষে কত বাইট অর্জিত হলো;
- ত্রুটি, খোলা Handles এবং অবশিষ্ট Locks;
- সুরক্ষিত সূত্রের অস্তিত্ব অক্ষুণ্ণ আছে কি না;
- পুনরুদ্ধারযোগ্যতা বা পুনরুৎপাদনযোগ্যতা;
- কোনো প্রক্রিয়া ফলাফলটি সঙ্গে সঙ্গে পুনরায় তৈরি করছে কি না।

জরুরি মোড শুধুমাত্র প্রমাণিত অতিরিক্ত 10 GB-এর পরে শেষ হয়। এরপর প্রক্রিয়া সরাসরি বিশ্লেষণে চলে যায়।

## Phase 2: Füllende Prozesse und Entstehung forensisch bestimmen

### 1. Ressourcenerschöpfung und Pagefile

বর্তমান ও ঐতিহাসিক প্রমাণ একসাথে পড়ুন:

```powershell
Get-CimInstance Win32_ComputerSystem |
  Select-Object AutomaticManagedPagefile
Get-CimInstance Win32_PageFileUsage |
  Select-Object Name, AllocatedBaseSize, CurrentUsage, PeakUsage
Get-WinEvent -FilterHashtable @{LogName='System'; Id=2004} -MaxEvents 20
```

Windows Resource Exhaustion Detector-এর Event 2004 ঘটনার সময়ে সর্বোচ্চ Commit-এর প্রক্রিয়াগুলো ধারণ করে। PID, প্রক্রিয়ার নাম, সময়চিহ্ন এবং বাইট আজকের প্রক্রিয়াগুলোর সাথে মেলান। একটি বড় `pagefile.sys` একাই প্রমাণ করে না যে ফাইলটি নিজেই কারণ; খুঁজতে হবে সেই প্রক্রিয়া যা Commit ঘটিয়েছে।

### 2. Dateiwachstum

নতুন বা পরিবর্তিত ফাইল এভাবে দলবদ্ধ করুন:

- তৈরি ও পরিবর্তনের ঘণ্টা;
- মূল পথ ও এক্সটেনশন;
- মালিক বা উৎপাদক প্রক্রিয়া;
- ফাইল সংখ্যা ও ভৌতভাবে দখল করা বাইটে দৈনিক হার।

Log-, Cache-, Sync-, Backup-, Build-, Download- ও Session-Verzeichnisse বিশেষভাবে পরীক্ষা করুন। যদি কোনো Client প্রতিদিন কয়েক GB লেখে এবং ভলিউম ছোট হয়, তবে সাত দিনের Retention অনুপযুক্ত।

### 3. Automationen

Aufgabenplanung, Dienste, Watcher ও Startprogramme-এ ফ্রিকোয়েন্সি, Retention ও সাফল্য পরীক্ষা করুন:

```powershell
Get-ScheduledTask | Where-Object State -ne 'Disabled'
Get-ScheduledTaskInfo -TaskName '<task-name>'
```

অ্যাকশন, Trigger, পুনরাবৃত্তি ব্যবধান, শেষ Rückgabecode এবং পরবর্তী চালানোর সময় আলাদাভাবে যাচাই করুন। একটি বিদ্যমান Task এটা প্রমাণ করে না যে Retention বা Frequenz প্রকৃত বৃদ্ধি নিয়ন্ত্রণ করছে।

## Phase 3: Dauerhafte Begrenzung

সবচেয়ে ছোট কার্যকর, প্রত্যাবর্তনযোগ্য ব্যবস্থা বেছে নিন:

- Logrotation ঘন ঘন চালান এবং একটি Größenlimit যোগ করুন;
- কোনো আপত্তিকর Client নিয়ন্ত্রিতভাবে পুনরায় চালু করুন এবং তার Commit মাপুন;
- Terminal-Scrollback বা Debug-Logging উপযুক্ত মানে সীমিত করুন;
- পুরোনো, পুনরুৎপাদনযোগ্য Caches সরান এবং তাদের স্বয়ংক্রিয় পুনর্নির্মাণ পর্যবেক্ষণ করুন;
- যাচাইকৃত Cloudinhalte-কে „Speicherplatz freigeben“ দিয়ে Dehydrieren করুন;
- Scheduler-Frequenz ও Retention-কে পরীক্ষামূলক দৈনিক হারের সাথে মিলিয়ে নির্ধারণ করুন;
- Pagefile- বা Ruhezustand-পরিবর্তন শুধুমাত্র প্রশাসনিকভাবে, Reboot- ও Rollbackপরিকল্পনা সহ করুন।

Windows Terminal-এর জন্য একটি সীমিত Standard-Scrollback উদাহরণস্বরূপ এমন হতে পারে:

```json
{
  "profiles": {
    "defaults": {
      "historySize": 2000
    }
  }
}
```

বিদ্যমান সেটিংস সংরক্ষণ করুন এবং পরিবর্তনের পরে JSON-Datei যাচাই করুন।

### OneDrive-spezifisches Gate

Dehydrierung-এর আগে Sync-Status ও অপেক্ষমাণ Uploads পরীক্ষিত হতে হবে। Cloudfilter-সচেতন Dateimanager বা Explorer-এর Befehl „Speicherplatz freigeben“ ব্যবহার করুন। Dehydrierung Cloudinhalt মুছবে না।

স্থানীয় OneDrive-Logbereich unter `$env:LOCALAPPDATA\Microsoft\OneDrive\logs` আলাদাভাবে পরীক্ষা করুন। কোনো উপভাগ দৈনিক Gigabytes তৈরি করলে, সময়ভিত্তিক Retention-কে একটি কঠোর আকার-সীমা এবং যথেষ্ট ঘন ঘন নির্ধারিত চালানোর সাথে যুক্ত করুন। খুব নতুন বা খোলা ফাইল রক্ষা করুন এবং চালানোর পরে Taskstatus ও অবশিষ্ট আকার উভয়ই যাচাই করুন।

## Abschlussprüfung und Bericht

শেষ পরিবর্তনের পরে:

1. অ্যাসিনক্রোনাস Cloud- বা মুছে ফেলার অপারেশন শেষ হওয়া পর্যন্ত অপেক্ষা করুন।
2. খালি স্টোরেজ ও প্রক্রিয়া-Commit আবার পড়ুন।
3. Readback দিয়ে পরিবর্তিত কনফিগারেশন, Tasks ও লগের আকার যাচাই করুন।
4. একটি সংক্ষিপ্ত রিটেস্ট চালান: পর্যবেক্ষণ জানালার মধ্যে আবার অতিরিক্ত স্টোরেজ তৈরি হচ্ছে কি না?
5. প্রারম্ভিক মান, প্রতিটি ফলাফল ও তার সিদ্ধান্ত, ভৌতভাবে অর্জিত বাইট, ভরাটকারী প্রক্রিয়াসমূহ, স্থায়ী সমন্বয়, Rollbacks, অবশিষ্ট ঝুঁকি এবং শেষ মান প্রতিবেদন করুন।

উপযুক্ত বর্তমান Readback ছাড়া কোনো পরিষ্কার, প্রক্রিয়া-সীমা বা 50-GB-লক্ষ্য অর্জনের দাবি করবেন না।

## Bekannte Grenzen

- প্রশাসনিক অধিকার ছাড়া Pagefile-, Ruhezustand- বা Dienständerungen অবরুদ্ধ থাকতে পারে। সঠিক অবশিষ্ট ধাপ নথিভুক্ত করুন।
- ঐতিহাসিক প্রক্রিয়া-Events একটি পূর্ববর্তী ভরাটকারী প্রমাণ করে; বর্তমান অবস্থার জন্য প্রক্রিয়া ও ফাইল-বৃদ্ধির ডেটাও প্রয়োজন।
- একটি পরিকল্পিত ব্যাকআপ-ধারণা কোনো ব্যাকআপ নয়। স্থানান্তর বা মোছা বর্তমান লক্ষ্য-পরিচয়, Manifest বা Hash, Restore-প্রমাণ এবং Mount-এর উপর নির্ভর করে।
- অস্পষ্ট মালিকানা, চলমান অন্যের কাজ বা অজানা লক্ষ্যের ক্ষেত্রে সিদ্ধান্ত হবে `nichts`।

## Changelog

### 1.0.0 (2026-08-05)

- কেন্দ্রীয় স্কিল-লাইব্রেরির জন্য পোর্টেবল প্রথম সংস্করণ।
- রিসোর্স-নিঃশেষ, Pagefile ও প্রক্রিয়া-বিশ্লেষণ যুক্ত।
- ভৌত NTFS-দখল ও OneDrive-Dehydrierung স্পষ্টভাবে আলাদা করা হয়েছে।
- সময় ও আকার-সীমা সহ OneDrive-Logrotation যুক্ত।
- Readback সহ কঠোর জরুরি ও সমাপ্তি-Gates সংজ্ঞায়িত।
