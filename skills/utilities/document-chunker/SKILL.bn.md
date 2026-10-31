---
name: document-chunker
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "RAG পাইপলাইন এবং LLM কনটেক্সট উইন্ডোর জন্য নথিকে ওভারল্যাপিং টোকেন চাঙ্কে ভাগ করে। শূন্য ডিপেনডেন্সি।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: a2795563043bfc5a0bd47e5f92600df6263f1daa31449313183c0cacc0323c50
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.751861+00:00"
---
<img src="banner.png" width="100%" alt="document-chunker banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# ডকুমেন্ট চাঙ্কার (Deutsch)

নথিকে ওভারল্যাপিং টোকেন চাঙ্কে ভাগ করে। RAG পাইপলাইন এবং LLM কনটেক্সট
উইন্ডোর জন্য অপ্টিমাইজড। শূন্য ডিপেনডেন্সি — শুধু Python stdlib + re।

## ব্যবহার

### লাইব্রেরি হিসেবে
```python
from document_chunker import DocumentChunker

chunker = DocumentChunker(chunk_size=400, overlap=80)
chunks = chunker.chunk_text("Long text...")

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['tokens']} tokens")
```

### একটি ফাইল চাঙ্ক করা
```python
chunks = chunker.chunk_document("document.md", source="My Project")
```

### একটি সম্পূর্ণ ডিরেক্টরি চাঙ্ক করা
```python
from document_chunker import chunk_corpus

chunks = chunk_corpus(["doc1.md", "doc2.txt"], source="Corpus")
```

### CLI
```bash
python document_chunker.py document.md    # Single file
python document_chunker.py ./docs/        # Entire directory
```


## প্যারামিটার

| প্যারামিটার | ডিফল্ট | বর্ণনা |
|-----------|---------|-------------|
| chunk_size | 400 | প্রতি চাঙ্কে সর্বোচ্চ টোকেন |
| overlap | 80 | চাঙ্কগুলোর মধ্যে ওভারল্যাপিং টোকেন |

## সমর্থিত ফাইল প্রকার

`.txt`, `.md`, `.py`, `.sh`

## পরিবর্তন লগ

### 1.0.0 (2026-03-12)
- BACH system/tools/document_chunker.py থেকে পোর্ট করা হয়েছে
