"""
Abstrakte Basis-Klasse und Datenstrukturen fuer Research Sources.

Definiert das gemeinsame Interface, das alle Quellen (PubMed, arXiv, ...)
implementieren muessen.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Article:
    """Ein einzelner Forschungsartikel."""

    id: str
    title: str
    authors: List[str]
    abstract: str
    source: str
    date: Optional[str] = None
    url: str = ""
    doi: Optional[str] = None
    journal: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "source": self.source,
            "date": self.date,
            "url": self.url,
            "doi": self.doi,
            "journal": self.journal,
            "metadata": self.metadata,
        }

    def to_markdown(self) -> str:
        authors_str = ", ".join(self.authors[:3])
        if len(self.authors) > 3:
            authors_str += " et al."
        lines = [
            f"### {self.title}",
            f"**Autoren:** {authors_str}",
        ]
        if self.journal:
            lines.append(f"**Journal:** {self.journal}")
        if self.date:
            lines.append(f"**Datum:** {self.date}")
        if self.doi:
            lines.append(f"**DOI:** {self.doi}")
        if self.url:
            lines.append(f"**URL:** {self.url}")
        if self.abstract:
            lines.append(f"\n> {self.abstract[:300]}{'...' if len(self.abstract) > 300 else ''}")
        return "\n".join(lines)


@dataclass
class SearchResult:
    """Ergebnis einer Quellensuche."""

    query: str
    source: str
    articles: List[Article]
    total_count: int
    timestamp: str = ""
    errors: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "source": self.source,
            "total_count": self.total_count,
            "returned_count": len(self.articles),
            "timestamp": self.timestamp,
            "articles": [a.to_dict() for a in self.articles],
            "errors": self.errors,
        }

    def to_markdown(self) -> str:
        lines = [
            f"## Suchergebnisse: {self.query}",
            f"**Quelle:** {self.source} | **Treffer:** {self.total_count} | "
            f"**Angezeigt:** {len(self.articles)}",
            f"**Zeitpunkt:** {self.timestamp}",
            "",
        ]
        for i, article in enumerate(self.articles, 1):
            lines.append(f"---\n**{i}.** {article.to_markdown()}\n")
        if self.errors:
            lines.append("\n**Fehler:**")
            for err in self.errors:
                lines.append(f"- {err}")
        return "\n".join(lines)


class Source(ABC):
    """Abstrakte Basisklasse fuer Forschungsquellen."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name der Quelle (z.B. 'PubMed', 'arXiv')."""
        ...

    @abstractmethod
    def search(self, query: str, max_results: int = 10, **kwargs) -> SearchResult:
        """
        Suche in der Quelle.

        Args:
            query: Suchbegriff(e)
            max_results: Maximale Anzahl Ergebnisse
            **kwargs: Quellenspezifische Parameter

        Returns:
            SearchResult mit gefundenen Artikeln
        """
        ...

    @abstractmethod
    def get_article(self, article_id: str) -> Optional[Article]:
        """
        Einzelnen Artikel anhand seiner ID abrufen.

        Args:
            article_id: Quellenspezifische Artikel-ID

        Returns:
            Article oder None wenn nicht gefunden
        """
        ...

    def is_available(self) -> bool:
        """Prueft ob die Quelle erreichbar ist."""
        return True
