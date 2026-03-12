"""
Literatur-Review Workflow.

Erstellt einen strukturierten Plan fuer einen Literatur-Review und
fuehrt die Suchphase automatisch durch. Entspricht dem
"Standard-Review (30 Min)" Workflow aus BACH.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..sources.base import Article, SearchResult, Source


@dataclass
class ReviewStep:
    """Einzelner Schritt im Review-Plan."""

    phase: str
    description: str
    status: str = "pending"  # pending, running, done, skipped
    results: Optional[SearchResult] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "phase": self.phase,
            "description": self.description,
            "status": self.status,
        }
        if self.results:
            d["results"] = self.results.to_dict()
        return d


@dataclass
class ReviewPlan:
    """Plan fuer einen Literatur-Review."""

    topic: str
    years: int
    steps: List[ReviewStep]
    created: str = ""
    status: str = "planned"  # planned, in_progress, completed

    def __post_init__(self):
        if not self.created:
            self.created = datetime.now().isoformat()

    @property
    def total_articles(self) -> int:
        count = 0
        for step in self.steps:
            if step.results:
                count += len(step.results.articles)
        return count

    @property
    def all_articles(self) -> List[Article]:
        articles = []
        seen_ids = set()
        for step in self.steps:
            if step.results:
                for article in step.results.articles:
                    key = (article.source, article.id)
                    if key not in seen_ids:
                        seen_ids.add(key)
                        articles.append(article)
        return articles

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "years": self.years,
            "created": self.created,
            "status": self.status,
            "total_articles": self.total_articles,
            "steps": [s.to_dict() for s in self.steps],
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Literatur-Review: {self.topic}",
            f"**Zeitraum:** Letzte {self.years} Jahre",
            f"**Erstellt:** {self.created}",
            f"**Status:** {self.status}",
            f"**Artikel gesamt:** {self.total_articles}",
            "",
        ]

        for i, step in enumerate(self.steps, 1):
            status_icon = {"pending": "[ ]", "running": "[~]", "done": "[x]", "skipped": "[-]"}
            icon = status_icon.get(step.status, "[ ]")
            lines.append(f"## {i}. {step.phase} {icon}")
            lines.append(f"{step.description}")
            if step.results:
                lines.append(f"\nTreffer: {step.results.total_count} "
                             f"(angezeigt: {len(step.results.articles)})")
                if step.results.errors:
                    for err in step.results.errors:
                        lines.append(f"- FEHLER: {err}")
            lines.append("")

        articles = self.all_articles
        if articles:
            lines.append("## Gefundene Artikel\n")
            for i, article in enumerate(articles, 1):
                lines.append(f"{i}. **{article.title}**")
                if article.authors:
                    authors = ", ".join(article.authors[:3])
                    if len(article.authors) > 3:
                        authors += " et al."
                    lines.append(f"   {authors}")
                if article.journal:
                    lines.append(f"   *{article.journal}* ({article.date or '?'})")
                if article.url:
                    lines.append(f"   {article.url}")
                lines.append("")

        return "\n".join(lines)


class LiteratureReview:
    """
    Literatur-Review: Erstellt einen Review-Plan und fuehrt die
    Suchschritte automatisch durch.
    """

    def __init__(self, sources: List[Source]):
        self._sources = sources

    def create_plan(self, topic: str, years: int = 5) -> ReviewPlan:
        """
        Erstellt einen Review-Plan (ohne Ausfuehrung).

        Args:
            topic: Forschungsthema
            years: Zeitraum in Jahren
        """
        source_names = ", ".join(s.name for s in self._sources)

        steps = [
            ReviewStep(
                phase="Ueberblick",
                description=f"Breitbandsuche nach '{topic}' in {source_names}",
            ),
            ReviewStep(
                phase="Fokussierte Suche",
                description=f"Gezielte Suche mit verfeinerten Begriffen",
            ),
            ReviewStep(
                phase="Abstract-Screening",
                description="Relevante Abstracts identifizieren und filtern",
            ),
            ReviewStep(
                phase="Synthese",
                description="Ergebnisse zusammenfassen, Gaps identifizieren",
            ),
        ]

        return ReviewPlan(
            topic=topic,
            years=years,
            steps=steps,
        )

    def execute_plan(
        self,
        plan: ReviewPlan,
        max_results_per_source: int = 10,
        additional_queries: Optional[List[str]] = None,
    ) -> ReviewPlan:
        """
        Fuehrt den Review-Plan aus (Suchschritte).

        Args:
            plan: Der auszufuehrende Plan
            max_results_per_source: Max. Ergebnisse pro Quelle pro Schritt
            additional_queries: Zusaetzliche Suchbegriffe fuer Phase 2
        """
        plan.status = "in_progress"
        current_year = datetime.now().year
        min_date = f"{current_year - plan.years}/01/01"

        # Phase 1: Ueberblick -- Breitbandsuche
        if len(plan.steps) > 0:
            step = plan.steps[0]
            step.status = "running"

            # Erste Quelle fuer Ueberblick nutzen
            if self._sources:
                result = self._sources[0].search(
                    plan.topic,
                    max_results=max_results_per_source,
                    min_date=min_date,
                )
                step.results = result

            step.status = "done"

        # Phase 2: Fokussierte Suche -- alle Quellen
        if len(plan.steps) > 1:
            step = plan.steps[1]
            step.status = "running"

            queries = [plan.topic]
            if additional_queries:
                queries.extend(additional_queries)

            all_articles = []
            total = 0
            errors = []

            for source in self._sources:
                for q in queries:
                    result = source.search(
                        q,
                        max_results=max_results_per_source,
                        min_date=min_date,
                    )
                    all_articles.extend(result.articles)
                    total += result.total_count
                    errors.extend(result.errors)

            # Deduplizierung nach ID+Source
            seen = set()
            unique = []
            for a in all_articles:
                key = (a.source, a.id)
                if key not in seen:
                    seen.add(key)
                    unique.append(a)

            from ..sources.base import SearchResult as SR
            step.results = SR(
                query=f"{plan.topic} (fokussiert)",
                source="Multi-Source",
                articles=unique,
                total_count=total,
                errors=errors,
            )
            step.status = "done"

        # Phase 3+4: Screening und Synthese sind manuelle Schritte
        for step in plan.steps[2:]:
            step.status = "pending"
            step.description += " (manueller Schritt)"

        plan.status = "completed" if not any(
            s.results and s.results.errors for s in plan.steps[:2]
        ) else "in_progress"

        return plan
