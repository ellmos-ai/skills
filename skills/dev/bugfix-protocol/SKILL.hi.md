---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "व्यवस्थित 6-चरण डिबगिंग प्रोटोकॉल। त्वरित जाँच, अलग-थलग परीक्षण, 20-मिनट नियम और बग रिपोर्ट टेम्पलेट के साथ बगों के लिए संरचित दृष्टिकोण।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/bugfix-protokoll.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 5deea0b6bd5cb1acc3495ebe481c63468b2231bb09d3e15f3da8163dde433e40
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.188911+00:00"
---
<img src="banner.png" width="100%" alt="bugfix-protocol banner">

# बगफिक्स-प्रोटोकॉल: व्यवस्थित 6-चरण डिबगिंग

बगों से निपटने का संरचित तरीका — लक्षण विश्लेषण से लेकर सत्यापन तक।
यह बेतरतीब प्रयोग से बचाता है और सुनिश्चित करता है कि फिक्स टिकाऊ हों।

---

## अवलोकन

| चरण | नाम | लक्ष्य | अधिकतम समय |
|-----|-----|--------|------------|
| 1 | त्वरित जाँच | स्पष्ट कारणों को बाहर करना | 2 मिनट |
| 2 | निदान | कारण का पता लगाना | 10 मिनट |
| 3 | अलग-थलग परीक्षण | बग को दोहराने योग्य बनाना | 5 मिनट |
| 4 | फिक्स | न्यूनतम सुधार | 10 मिनट |
| 5 | सत्यापन | फिक्स और दुष्प्रभावों की जाँच | 5 मिनट |
| 6 | दस्तावेज़ीकरण | ज्ञान को सुरक्षित करना | 2 मिनट |

**20-मिनट नियम:** यदि 20 मिनट बाद कोई प्रगति न हो → दृष्टिकोण बदलें या मदद लें।

---

## चरण 1: त्वरित जाँच (2 मिनट)

गहराई में जाने से पहले — सबसे आम कारणों की जाँच करें:

### जाँच-सूची

- [ ] **सिंटैक्स त्रुटि?** त्रुटि संदेश ध्यान से पढ़ें, पंक्ति जाँचें
- [ ] **इम्पोर्ट त्रुटि?** मॉड्यूल इंस्टॉल है? सही नाम है? सर्कुलर इम्पोर्ट?
- [ ] **टाइपिंग त्रुटि?** वेरिएबल/फ़ंक्शन नाम सही हैं?
- [ ] **गलत डेटा प्रकार?** Int की जगह String? जहाँ ऑब्जेक्ट अपेक्षित है वहाँ None?
- [ ] **पुराना कैश?** `__pycache__` हटाएँ, पुनः आरंभ करें
- [ ] **गलत वातावरण?** सही venv सक्रिय है? सही Python संस्करण?
- [ ] **एन्कोडिंग?** UTF-8 बनाम cp1252 (Windows की पुरानी समस्या)

### त्वरित क्रियाएँ

```bash
# Cache leeren
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# Imports pruefen
python -c "import modulname"

# Syntax pruefen
python -m py_compile datei.py
```

---

## चरण 2: निदान (10 मिनट)

### रणनीति: बाहर से अंदर की ओर

1. **त्रुटि संदेश का विश्लेषण करें** — Traceback को नीचे से ऊपर पढ़ें
2. **हाल के बदलावों की जाँच करें** — `git diff`, `git log --oneline -10`
3. **निदान उपकरण लगाएँ** — प्रोजेक्ट के अनुसार अपने निदान उपकरण उपयोग करें

### निदान उपकरण (उदाहरण)

प्रोजेक्ट के अनुसार विशेष निदान स्क्रिप्ट उपयोगी हो सकती हैं:

| उपकरण | उद्देश्य |
|-------|---------|
| `import_diagnose.py` | इम्पोर्ट समस्याओं का विश्लेषण |
| `method_analyzer.py` | मेथड सिग्नेचर की जाँच |
| `env_checker.py` | पर्यावरण चर/पथों का सत्यापन |

> **नोट:** प्रोजेक्ट के अनुसार अपने निदान उपकरण बनाएँ या मौजूदा
> प्रोजेक्ट उपकरणों का उपयोग करें। महत्वपूर्ण है व्यवस्थित तरीका, न कि
> कोई विशेष उपकरण।

### डिबगिंग तकनीकें

```python
# 1. Print-Debugging (schnell aber effektiv)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. Breakpoint (interaktiv)
breakpoint()  # Python 3.7+

# 3. Traceback erweitern
import traceback
traceback.print_exc()

# 4. Logging statt Print
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## चरण 3: अलग-थलग परीक्षण (5 मिनट)

### न्यूनतम पुनरुत्पादन योग्य उदाहरण (MRE)

लक्ष्य: न्यूनतम कोड से बग को दोहराना।

```python
# test_bug.py — Minimaler Reproduktions-Test
"""
Bug: [Kurze Beschreibung]
Erwartet: [Was sollte passieren]
Tatsaechlich: [Was passiert stattdessen]
"""

# Minimaler Setup
# ... nur das Noetigste

# Bug-Ausloeser
# ... exakter Code der den Bug triggert

# Erwartetes Ergebnis
# assert result == expected, f"Got {result}"
```

### अलगाव रणनीतियाँ

1. **नई फ़ाइल:** बग को अपनी फ़ाइल में दोहराएँ
2. **निर्भरताएँ हटाएँ:** एक-एक करके, जब तक बग गायब न हो
3. **आधा करें:** कोड ब्लॉक को आधा करें, जाँचें कि किस हिस्से में बग है
4. **Git Bisect:** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## चरण 4: फिक्स (10 मिनट)

### सिद्धांत

1. **न्यूनतम:** जितना कम हो सके उतना बदलें
2. **समझें:** कभी अंधाधुंध फिक्स न करें — समझें कि यह क्यों टूटा
3. **एक बात:** एक कमिट में एक फिक्स, एक साथ कई समस्याएँ नहीं
4. **पिछली-संगतता:** मौजूदा कार्यक्षमता न तोड़ें

### फिक्स पैटर्न

```python
# SCHLECHT: Symptom behandeln
try:
    result = broken_function()
except:  # Alles schlucken
    result = default_value

# GUT: Ursache beheben
def broken_function():
    if input_data is None:  # Eigentliche Ursache: None-Check fehlte
        return default_value
    return process(input_data)
```

### सामान्य फिक्स श्रेणियाँ

| श्रेणी | विशिष्ट फिक्स |
|--------|--------------|
| None/Null | गार्ड-क्लॉज़: `if x is None: return default` |
| इंडेक्स त्रुटि | सीमा जाँच: `if i < len(lst)` |
| टाइप त्रुटि | स्पष्ट रूपांतरण: `str(x)`, `int(x)` |
| इम्पोर्ट त्रुटि | पथ सुधारें, पैकेज इंस्टॉल करें |
| एन्कोडिंग | UTF-8 स्पष्ट रूप से दें: `encoding='utf-8'` |
| रेस कंडीशन | Lock/Mutex, या क्रम बदलें |
| स्टेट-बग | प्रारंभीकरण जाँचें, रीसेट जोड़ें |

---

## चरण 5: सत्यापन (5 मिनट)

### जाँच-सूची

- [ ] **बग ठीक हुआ:** मूल समस्या अब नहीं होती
- [ ] **MRE उत्तीर्ण:** अलग-थलग परीक्षण सफल चलता है
- [ ] **कोई प्रतिगमन नहीं:** मौजूदा परीक्षण अभी भी चलते हैं
- [ ] **किनारे के मामले:** खाली इनपुट, None, बड़े डेटा का परीक्षण
- [ ] **प्रोजेक्ट उपकरण:** प्रोजेक्ट-उपकरण निर्देशिका में देखें कि कोई प्रासंगिक परीक्षण/सत्यापन उपकरण है या नहीं

### परीक्षण कमांड

```bash
# Unit-Tests
python -m pytest tests/ -v

# Nur betroffene Tests
python -m pytest tests/test_modul.py -v -k "test_name"

# Type-Check
python -m mypy datei.py

# Lint
python -m flake8 datei.py
```

---

## चरण 6: दस्तावेज़ीकरण (2 मिनट)

### बग-रिपोर्ट टेम्पलेट

```markdown
## Bug-Report: [Kurztitel]

**Datum:** YYYY-MM-DD
**Schwere:** kritisch / hoch / mittel / niedrig
**Komponente:** [Modul/Datei]

### Symptom
[Was der User sieht / Fehlermeldung]

### Ursache
[Technische Root-Cause]

### Fix
[Was geaendert wurde + warum]

### Betroffene Dateien
- `datei1.py` — [Aenderung]
- `datei2.py` — [Aenderung]

### Praevention
[Wie kann dieser Bug-Typ in Zukunft vermieden werden?]
```

### कमिट-संदेश प्रारूप

```
fix: [Kurze Beschreibung des Fixes]

Ursache: [Root-Cause in einem Satz]
Fix: [Was geaendert wurde]
Test: [Wie verifiziert]
```

---

## PyQt6 / GUI डिबगिंग — सामान्य जाल

> यह खंड PyQt6/PySide6 के साथ डेस्कटॉप GUI प्रोजेक्ट्स के लिए प्रासंगिक है।

### PyQt6 के शीर्ष 5 जाल

| जाल | समस्या | समाधान |
|-----|--------|--------|
| **Signal-Slot डिस्कनेक्ट** | Signal जुड़ा है पर हैंडलर नहीं चलता | हैंडलर में `print`, सिग्नेचर जाँचें |
| **थ्रेड-सुरक्षा** | Worker-थ्रेड से GUI अपडेट | `QMetaObject.invokeMethod` या Signal का उपयोग करें |
| **Layout-कैस्केड** | विजेट अदृश्य/गलत स्थान पर | `widget.show()`, Layout-पदानुक्रम जाँचें |
| **Event-Loop ब्लॉक** | GUI जम जाता है | दीर्घकालिक कार्य QThread में भेजें |
| **Garbage Collection** | विजेट अचानक गायब हो जाता है | संदर्भ को `self.widget` के रूप में रखें |

### PyQt6 डिबग सहायक

```python
# Widget-Hierarchie ausgeben
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# Signal-Debugging
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## त्वरित संदर्भ

```
BUG GEFUNDEN?
     │
     ▼
[Phase 1: Schnell-Checks]  ──── Offensichtlich? → FIX
     │
     ▼
[Phase 2: Diagnose]  ────────── Ursache klar? → Phase 4
     │
     ▼
[Phase 3: Isolierter Test]  ── Reproduzierbar? → Phase 4
     │                              │
     │                         Nicht reproduzierbar?
     │                              │
     │                         Logging einbauen,
     │                         auf erneutes Auftreten warten
     ▼
[Phase 4: Fix]  ─────────────── Minimal + verstanden
     │
     ▼
[Phase 5: Verifikation]  ────── Tests gruen? → Phase 6
     │                              │
     │                         Tests rot? → Zurueck zu Phase 4
     ▼
[Phase 6: Dokumentation]  ───── Bug-Report + Commit
```

### 20-मिनट नियम

यदि 20 मिनट बाद अटक जाएँ:

1. **दृष्टिकोण बदलें** — कोई अन्य डिबगिंग तकनीक आज़माएँ
2. **रबर डक** — समस्या ज़ोर से समझाएँ (या लिखें)
3. **विराम** — 5 मिनट दूर जाएँ, फिर ताज़ा नज़र से देखें
4. **मदद लें** — सहकर्मी से पूछें, Stack Overflow, दस्तावेज़ीकरण
5. **रीसेट करें** — `git stash`, पूरी तरह से नए सिरे से शुरू करें
