"""
PubMed-Integration ueber NCBI E-utilities.

Nutzt die oeffentliche API (kein API-Key noetig fuer <3 req/s).
Dokumentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
"""

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

from .base import Article, SearchResult, Source

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov"

# Timeout fuer HTTP-Anfragen (Sekunden)
REQUEST_TIMEOUT = 15


class PubMedSource(Source):
    """PubMed-Quelle via NCBI E-utilities API."""

    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        """
        Args:
            email: Kontakt-E-Mail (empfohlen von NCBI, nicht zwingend)
            api_key: NCBI API-Key (erhoet Rate-Limit auf 10 req/s)
        """
        self._email = email
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "PubMed"

    def _build_params(self, extra: Dict[str, str]) -> Dict[str, str]:
        params = dict(extra)
        if self._email:
            params["email"] = self._email
        if self._api_key:
            params["api_key"] = self._api_key
        return params

    def _http_get(self, url: str) -> bytes:
        req = urllib.request.Request(url, headers={"User-Agent": "ResearchAgent/0.1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read()

    def search(self, query: str, max_results: int = 10, **kwargs) -> SearchResult:
        """
        PubMed-Suche via esearch + efetch.

        Kwargs:
            min_date: Startdatum (YYYY/MM/DD)
            max_date: Enddatum (YYYY/MM/DD)
            sort: Sortierung ('relevance' oder 'pub_date')
        """
        errors: List[str] = []
        articles: List[Article] = []
        total_count = 0

        try:
            # Phase 1: esearch -- IDs finden
            ids, total_count = self._esearch(query, max_results, **kwargs)

            if ids:
                # Phase 2: efetch -- Details abrufen
                articles = self._efetch(ids)

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
        """Einzelnen Artikel via PMID abrufen."""
        try:
            articles = self._efetch([article_id])
            return articles[0] if articles else None
        except Exception:
            return None

    def is_available(self) -> bool:
        """Prueft ob PubMed erreichbar ist."""
        try:
            url = f"{EUTILS_BASE}/einfo.fcgi?db=pubmed&retmode=json"
            data = self._http_get(url)
            result = json.loads(data)
            return "einforesult" in result
        except Exception:
            return False

    # --- Interne Methoden ---

    def _esearch(self, query: str, max_results: int, **kwargs) -> tuple:
        """
        NCBI esearch: Sucht PubMed-IDs.

        Returns:
            (list_of_ids, total_count)
        """
        params = self._build_params({
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": str(max_results),
            "sort": kwargs.get("sort", "relevance"),
        })

        if "min_date" in kwargs:
            params["mindate"] = kwargs["min_date"]
            params["datetype"] = "pdat"
        if "max_date" in kwargs:
            params["maxdate"] = kwargs["max_date"]
            params["datetype"] = "pdat"

        url = f"{EUTILS_BASE}/esearch.fcgi?{urllib.parse.urlencode(params)}"
        data = self._http_get(url)
        result = json.loads(data)

        esearch = result.get("esearchresult", {})
        ids = esearch.get("idlist", [])
        total_count = int(esearch.get("count", 0))

        return ids, total_count

    def _efetch(self, pmids: List[str]) -> List[Article]:
        """
        NCBI efetch: Ruft Artikel-Details ab.

        Args:
            pmids: Liste von PubMed-IDs

        Returns:
            Liste von Article-Objekten
        """
        params = self._build_params({
            "db": "pubmed",
            "id": ",".join(pmids),
            "rettype": "xml",
            "retmode": "xml",
        })

        url = f"{EUTILS_BASE}/efetch.fcgi?{urllib.parse.urlencode(params)}"
        data = self._http_get(url)
        root = ET.fromstring(data)

        articles = []
        for article_elem in root.findall(".//PubmedArticle"):
            article = self._parse_article(article_elem)
            if article:
                articles.append(article)

        return articles

    def _parse_article(self, elem: ET.Element) -> Optional[Article]:
        """Parst ein PubmedArticle XML-Element."""
        medline = elem.find("MedlineCitation")
        if medline is None:
            return None

        # PMID
        pmid_elem = medline.find("PMID")
        pmid = pmid_elem.text if pmid_elem is not None else ""

        article_elem = medline.find("Article")
        if article_elem is None:
            return None

        # Titel
        title_elem = article_elem.find("ArticleTitle")
        title = self._get_text(title_elem)

        # Abstract
        abstract_parts = []
        abstract_elem = article_elem.find("Abstract")
        if abstract_elem is not None:
            for text in abstract_elem.findall("AbstractText"):
                label = text.get("Label", "")
                content = self._get_text(text)
                if label:
                    abstract_parts.append(f"{label}: {content}")
                else:
                    abstract_parts.append(content)
        abstract = " ".join(abstract_parts)

        # Autoren
        authors = []
        author_list = article_elem.find("AuthorList")
        if author_list is not None:
            for author in author_list.findall("Author"):
                last = author.findtext("LastName", "")
                fore = author.findtext("ForeName", "")
                if last:
                    authors.append(f"{last} {fore}".strip())

        # Journal
        journal_elem = article_elem.find("Journal")
        journal = ""
        if journal_elem is not None:
            journal = journal_elem.findtext("Title", "")
            if not journal:
                journal = journal_elem.findtext("ISOAbbreviation", "")

        # Datum
        date = ""
        date_elem = article_elem.find(".//PubDate")
        if date_elem is not None:
            year = date_elem.findtext("Year", "")
            month = date_elem.findtext("Month", "")
            day = date_elem.findtext("Day", "")
            date = f"{year}"
            if month:
                date += f"-{month}"
            if day:
                date += f"-{day}"

        # DOI
        doi = None
        for id_elem in elem.findall(".//ArticleId"):
            if id_elem.get("IdType") == "doi":
                doi = id_elem.text

        return Article(
            id=pmid,
            title=title,
            authors=authors,
            abstract=abstract,
            source=self.name,
            date=date,
            url=f"{PUBMED_URL}/{pmid}/",
            doi=doi,
            journal=journal,
        )

    @staticmethod
    def _get_text(elem: Optional[ET.Element]) -> str:
        """Extrahiert Text inkl. verschachtelter Elemente."""
        if elem is None:
            return ""
        # itertext() holt auch Text aus Sub-Elementen (z.B. <i>, <b>)
        return "".join(elem.itertext()).strip()
