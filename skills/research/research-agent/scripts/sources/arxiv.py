"""
arXiv-Integration (Basis-Implementierung).

Nutzt die arXiv API (Atom/XML).
Dokumentation: https://info.arxiv.org/help/api/index.html

Status: Funktionsfaehig, aber als sekundaere Quelle gedacht.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Optional

from .base import Article, SearchResult, Source

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

REQUEST_TIMEOUT = 15


class ArxivSource(Source):
    """arXiv-Quelle via Atom API."""

    @property
    def name(self) -> str:
        return "arXiv"

    def search(self, query: str, max_results: int = 10, **kwargs) -> SearchResult:
        """
        arXiv-Suche.

        Kwargs:
            category: arXiv-Kategorie (z.B. 'cs.AI', 'q-bio')
            sort_by: 'relevance', 'lastUpdatedDate', 'submittedDate'
        """
        errors: List[str] = []
        articles: List[Article] = []
        total_count = 0

        try:
            search_query = query
            category = kwargs.get("category")
            if category:
                search_query = f"cat:{category} AND all:{query}"
            else:
                search_query = f"all:{query}"

            params = {
                "search_query": search_query,
                "start": "0",
                "max_results": str(max_results),
                "sortBy": kwargs.get("sort_by", "relevance"),
                "sortOrder": "descending",
            }

            url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers={"User-Agent": "ResearchAgent/0.1.0"})
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                data = resp.read()

            root = ET.fromstring(data)

            # Total results
            total_elem = root.find(f"{ATOM_NS}totalResults")
            if total_elem is None:
                # opensearch namespace fallback
                total_elem = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
            total_count = int(total_elem.text) if total_elem is not None else 0

            for entry in root.findall(f"{ATOM_NS}entry"):
                article = self._parse_entry(entry)
                if article:
                    articles.append(article)

        except urllib.error.URLError as e:
            errors.append(f"Netzwerkfehler: {e.reason}")
        except ET.ParseError as e:
            errors.append(f"XML-Parse-Fehler: {e}")
        except Exception as e:
            errors.append(f"Unerwarteter Fehler: {type(e).__name__}: {e}")

        return SearchResult(
            query=query,
            source=self.name,
            articles=articles,
            total_count=total_count,
            errors=errors,
        )

    def get_article(self, article_id: str) -> Optional[Article]:
        """Einzelnen Artikel via arXiv-ID abrufen."""
        try:
            params = {"id_list": article_id}
            url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers={"User-Agent": "ResearchAgent/0.1.0"})
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                data = resp.read()

            root = ET.fromstring(data)
            entry = root.find(f"{ATOM_NS}entry")
            if entry is not None:
                return self._parse_entry(entry)
        except Exception:
            pass
        return None

    def is_available(self) -> bool:
        """Prueft ob arXiv-API erreichbar ist."""
        try:
            url = f"{ARXIV_API}?search_query=all:test&max_results=1"
            req = urllib.request.Request(url, headers={"User-Agent": "ResearchAgent/0.1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except Exception:
            return False

    def _parse_entry(self, entry: ET.Element) -> Optional[Article]:
        """Parst ein Atom-Entry-Element."""
        # ID (arXiv URL -> ID extrahieren)
        id_text = entry.findtext(f"{ATOM_NS}id", "")
        arxiv_id = id_text.replace("http://arxiv.org/abs/", "").strip()

        title = entry.findtext(f"{ATOM_NS}title", "").strip().replace("\n", " ")

        # Abstract (summary)
        abstract = entry.findtext(f"{ATOM_NS}summary", "").strip().replace("\n", " ")

        # Autoren
        authors = []
        for author in entry.findall(f"{ATOM_NS}author"):
            name = author.findtext(f"{ATOM_NS}name", "")
            if name:
                authors.append(name.strip())

        # Datum
        published = entry.findtext(f"{ATOM_NS}published", "")
        date = published[:10] if published else ""  # YYYY-MM-DD

        # DOI (optional)
        doi = entry.findtext(f"{ARXIV_NS}doi")

        # Kategorie (primaer)
        primary_cat = entry.find(f"{ARXIV_NS}primary_category")
        category = primary_cat.get("term", "") if primary_cat is not None else ""

        return Article(
            id=arxiv_id,
            title=title,
            authors=authors,
            abstract=abstract,
            source=self.name,
            date=date,
            url=f"https://arxiv.org/abs/{arxiv_id}",
            doi=doi,
            metadata={"category": category},
        )
