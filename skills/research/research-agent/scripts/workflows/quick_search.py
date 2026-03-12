"""
Schnell-Recherche Workflow.

Fuehrt eine schnelle Suche ueber eine oder mehrere Quellen durch
und liefert die Top-Ergebnisse als strukturiertes Resultat.
Entspricht dem "Schnell-Recherche (5 Min)" Workflow aus BACH.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..sources.base import Article, SearchResult, Source


@dataclass
class QuickSearchResult:
    """Ergebnis einer Schnell-Recherche."""

    query: str
    source_results: List[SearchResult]
    top_articles: List[Article]
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    @property
    def total_found(self) -> int:
        return sum(r.total_count for r in self.source_results)

    @property
    def has_errors(self) -> bool:
        return any(r.errors for r in self.source_results)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "timestamp": self.timestamp,
            "total_found": self.total_found,
            "top_articles": [a.to_dict() for a in self.top_articles],
            "sources": [r.to_dict() for r in self.source_results],
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Schnell-Recherche: {self.query}",
            f"**Zeitpunkt:** {self.timestamp}",
            f"**Treffer gesamt:** {self.total_found}",
            "",
        ]
        for result in self.source_results:
            lines.append(f"## {result.source}")
            lines.append(f"Treffer: {result.total_count}")
            if result.errors:
                for err in result.errors:
                    lines.append(f"- FEHLER: {err}")
            lines.append("")

        if self.top_articles:
            lines.append("## Top-Ergebnisse\n")
            for i, article in enumerate(self.top_articles, 1):
                lines.append(f"### {i}. {article.title}")
                authors = ", ".join(article.authors[:3])
                if len(article.authors) > 3:
                    authors += " et al."
                lines.append(f"**Autoren:** {authors}")
                if article.journal:
                    lines.append(f"**Journal:** {article.journal}")
                if article.date:
                    lines.append(f"**Datum:** {article.date}")
                if article.url:
                    lines.append(f"**URL:** {article.url}")
                if article.abstract:
                    short = article.abstract[:200]
                    if len(article.abstract) > 200:
                        short += "..."
                    lines.append(f"\n> {short}\n")
                lines.append("")

        return "\n".join(lines)


class QuickSearch:
    """
    Schnell-Recherche: Sucht in einer oder mehreren Quellen und
    liefert die besten Treffer.
    """

    def __init__(self, sources: List[Source]):
        self._sources = sources

    def run(self, query: str, max_results: int = 5, **kwargs) -> QuickSearchResult:
        """
        Fuehrt die Schnell-Recherche durch.

        Args:
            query: Suchbegriff
            max_results: Maximale Ergebnisse pro Quelle
            **kwargs: Werden an jede Quelle weitergegeben
        """
        source_results: List[SearchResult] = []

        for source in self._sources:
            result = source.search(query, max_results=max_results, **kwargs)
            source_results.append(result)

        # Top-Artikel aus allen Quellen zusammenführen (Reihenfolge beibehalten)
        top_articles: List[Article] = []
        for result in source_results:
            top_articles.extend(result.articles)

        return QuickSearchResult(
            query=query,
            source_results=source_results,
            top_articles=top_articles[:max_results * len(self._sources)],
        )
