#!/usr/bin/env python3
"""AI-Portable Setup: Erstellt eine portable KI-Arbeitsumgebung auf einem Laufwerk."""

import os
import sys
import json
from pathlib import Path

STRUCTURE = {
    "models": ["llm", "embeddings", "tts"],
    "db": ["chroma", "sqlite"],
    "documents": ["code", "general"],
    "rag": [],
    "prompts": [],
    "templates": [],
}

PROMPTS = {
    "coding.txt": """\
Du bist ein erfahrener Softwareentwickler und hilfst beim Schreiben, Refaktorieren und
Erklaeren von Code. Du lieferst saubere, gut strukturierte Loesungen und erklaerst dein
Vorgehen nachvollziehbar.

Richtlinien:
- Schreibe klaren, gut lesbaren Code.
- Bevorzuge Sicherheit und Robustheit gegenueber cleveren, schwer lesbaren Tricks.
- Erklaere wichtige Entscheidungen in kurzen, praegnanten Saetzen.
- Mach keine Annahmen ueber geheime Daten, Passwoerter oder externe Systeme.
- Wenn Anforderungen unklar sind, schlage sinnvolle Optionen vor.

LIEFERE:
- Standardmaessig: Loesungsvorschlag + kurze Erklaerung.
- Auf Wunsch: Alternativen, Refactoring-Vorschlaege, Tests, Edge-Case-Hinweise.

Sprache: Wenn der Nutzer auf Deutsch schreibt, erklaere auf Deutsch.
""",
    "icf.txt": """\
Du bist ein Assistent, der bei der Strukturierung von Beobachtungen und Aufzeichnungen
im Rahmen der ICF (International Classification of Functioning, Disability and Health)
unterstuetzt. Du triffst KEINE klinischen Diagnosen, sondern hilfst nur bei der
Beschreibung von Funktionsbereichen, Aktivitaeten, Partizipation und Umweltfaktoren.

WICHTIG:
- Du ordnest Textstellen moeglichst passenden ICF-Bereichen zu (b, d, e, s), aber nur,
  wenn dies durch den Text ausreichend gestuetzt ist.
- Du erfindest KEINE Angaben und spekulierst nicht ueber Diagnosen oder medizinische Details.
- Du formulierst neutral, beschreibend, ohne Wertung.

LIEFERE:
1. Kurz-Zusammenfassung der wichtigsten Inhalte der Aufzeichnungen.
2. Tabelle mit: Textaussage | Vermuteter ICF-Bereich (b, d, e, s) | Kurzbeschreibung
3. Strukturierten Bericht: Koerperfunktionen (b), Aktivitaeten & Partizipation (d),
   Umweltfaktoren (e), Koerperstrukturen (s, falls relevant)
4. Kurze, neutrale Zusammenfassung (kein Behandlungsplan).
""",
    "rpg.txt": """\
Du bist Spielleiter eines Pen-and-Paper-Rollenspiels. Deine Aufgaben:
- Erzaehle eine immersive, lebendige Welt.
- Beschreibe Orte, Charaktere und Ereignisse bildhaft, aber nicht ueberladen.
- Gib den Spielern sinnvolle Entscheidungen und reagiere flexibel auf ihre Ideen.
- Vermeide Railroading, biete mehrere Handlungsoptionen.

WICHTIG:
- Keine sexualisierten Inhalte.
- Keine detaillierten Darstellungen von Gewalt oder Folter.
- Kein Spiel mit realen Traumata.

LIEFERE:
- Szenenbeschreibungen.
- Dialoge mit NPCs.
- Entscheidungsoptionen (3-5 Moeglichkeiten).
- Optionale Zufallsereignisse und Twists.
""",
}

RAG_INGEST = '''\
"""Dateien einlesen und in ChromaDB indexieren."""
import os
from chromadb import PersistentClient
from chromadb.config import Settings
from ollama import Client

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC_PATH = os.path.join(BASE, "documents")
DB_PATH = os.path.join(BASE, "db", "chroma")
EMBED_MODEL = "nomic-embed-text"

client = Client()

def embed(text):
    return client.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]

def ingest():
    db = PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))
    collection = db.get_or_create_collection("documents")
    count = 0
    for root, dirs, files in os.walk(DOC_PATH):
        for file in files:
            if file.endswith((".txt", ".md", ".py")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
                if not text.strip():
                    continue
                emb = embed(text)
                collection.upsert(documents=[text], embeddings=[emb], ids=[path])
                count += 1
                print(f"  Indexiert: {os.path.relpath(path, BASE)}")
    print(f"\\n{count} Dokument(e) indexiert.")

if __name__ == "__main__":
    ingest()
'''

RAG_QUERY = '''\
"""RAG-Abfragen mit Modus-Auswahl."""
import os
import sys
from chromadb import PersistentClient
from chromadb.config import Settings
from ollama import Client

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "db", "chroma")
PROMPTS_PATH = os.path.join(BASE, "prompts")
LLM_MODEL = "mistral:instruct"
EMBED_MODEL = "nomic-embed-text"

client = Client()

def load_prompt(name):
    path = os.path.join(PROMPTS_PATH, f"{name}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Du bist ein hilfreicher Assistent. Nutze den Kontext, um die Frage zu beantworten."

def embed(text):
    return client.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]

def query_rag(question, mode="default", n_results=5):
    db = PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))
    collection = db.get_or_create_collection("documents")

    q_emb = embed(question)
    results = collection.query(query_embeddings=[q_emb], n_results=n_results)

    if not results["documents"] or not results["documents"][0]:
        print("Keine Dokumente gefunden. Erst Dokumente indexieren: python rag/ingest.py")
        return

    context = "\\n\\n---\\n\\n".join(results["documents"][0])
    system_prompt = load_prompt(mode) if mode != "default" else load_prompt("default")

    prompt = f"""{system_prompt}

KONTEXT:
{context}

FRAGE:
{question}

ANTWORT:"""

    response = client.generate(model=LLM_MODEL, prompt=prompt)
    print(response["response"])

if __name__ == "__main__":
    args = sys.argv[1:]
    mode = "default"
    if len(args) >= 2 and args[0] == "--mode":
        mode = args[1]
        question = " ".join(args[2:])
    else:
        question = " ".join(args)

    if not question:
        print("Nutzung: python query.py [--mode icf|coding|rpg] \\"Frage...\\"")
        sys.exit(1)

    query_rag(question, mode=mode)
'''

RAG_PIPELINE = '''\
"""Haupt-RAG-Pipeline: Embed + Query + LLM."""
import os
from chromadb import PersistentClient
from chromadb.config import Settings
from ollama import Client

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "db", "chroma")
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "mistral:instruct"

client = Client()

def embed(texts):
    return client.embeddings(model=EMBED_MODEL, prompt=texts)["embedding"]

def load_chroma():
    return PersistentClient(path=DB_PATH, settings=Settings(anonymized_telemetry=False))

def query_rag(question, n_results=5):
    db = load_chroma()
    collection = db.get_or_create_collection("documents")
    q_emb = embed(question)
    results = collection.query(query_embeddings=[q_emb], n_results=n_results)
    context = "\\n\\n".join(results["documents"][0])

    prompt = f"""Nutze den folgenden Kontext, um die Frage zu beantworten:

Kontext:
{context}

Frage:
{question}

Antwort:"""
    response = client.generate(model=LLM_MODEL, prompt=prompt)
    return response["response"]
'''


def create_structure(base_path: Path):
    """Erstellt die komplette AI-Portable Verzeichnisstruktur."""
    print(f"Erstelle AI-Portable Struktur in: {base_path}")
    print("=" * 50)

    # Verzeichnisse
    for parent, children in STRUCTURE.items():
        parent_path = base_path / parent
        parent_path.mkdir(parents=True, exist_ok=True)
        print(f"  [DIR] {parent}/")
        for child in children:
            (parent_path / child).mkdir(exist_ok=True)
            print(f"  [DIR] {parent}/{child}/")

    # Prompts
    for filename, content in PROMPTS.items():
        prompt_path = base_path / "prompts" / filename
        prompt_path.write_text(content, encoding="utf-8")
        print(f"  [FILE] prompts/{filename}")

    # RAG-Scripts
    rag_files = {
        "ingest.py": RAG_INGEST,
        "query.py": RAG_QUERY,
        "pipeline.py": RAG_PIPELINE,
    }
    for filename, content in rag_files.items():
        file_path = base_path / "rag" / filename
        file_path.write_text(content, encoding="utf-8")
        print(f"  [FILE] rag/{filename}")

    # README
    readme = base_path / "README.txt"
    readme.write_text(
        "AI-Portable -- Lokale KI-Arbeitsumgebung\n"
        "==========================================\n\n"
        "Voraussetzungen:\n"
        "  - Python 3.10+\n"
        "  - Ollama (mit mistral:instruct und nomic-embed-text)\n\n"
        "Setup:\n"
        "  python -m venv venv\n"
        "  venv\\Scripts\\activate  (Windows) / source venv/bin/activate (Linux)\n"
        "  pip install chromadb ollama\n\n"
        "Nutzung:\n"
        "  1. Dokumente in documents/ ablegen\n"
        "  2. python rag/ingest.py        (Indexierung)\n"
        "  3. python rag/query.py \"Frage\" (Abfrage)\n"
        "  4. python rag/query.py --mode icf \"Beobachtungen...\" (ICF-Modus)\n",
        encoding="utf-8",
    )
    print(f"  [FILE] README.txt")

    print("=" * 50)
    print(f"Fertig! {base_path}")
    print(f"\nNaechste Schritte:")
    print(f"  cd {base_path}")
    print(f"  python -m venv venv")
    print(f"  pip install chromadb ollama")


def main():
    if len(sys.argv) < 2:
        print("Nutzung: python setup_portable.py <zielpfad>")
        print("Beispiel: python setup_portable.py E:\\AI-Portable")
        sys.exit(1)

    target = Path(sys.argv[1])
    if target.exists() and any(target.iterdir()):
        print(f"WARNUNG: {target} existiert bereits und ist nicht leer.")
        answer = input("Fortfahren? (j/n): ").strip().lower()
        if answer != "j":
            print("Abgebrochen.")
            sys.exit(0)

    create_structure(target)


if __name__ == "__main__":
    main()
