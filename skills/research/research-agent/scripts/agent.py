"""
ResearchAgent v0.1.0 -- Forschungspipeline.

Orchestriert wissenschaftliche Recherche-Workflows:
- Schnell-Recherche (PubMed, arXiv)
- Literatur-Review mit strukturiertem Plan
- Suchhistorie und Ergebnis-Speicherung

Standalone-faehig. Optional: BACH-Integration via bach_api.

Usage:
    from ResearchAgent import ResearchAgent

    agent = ResearchAgent()
    results = agent.search("CRISPR gene therapy")
    plan = agent.create_review_plan("autism interventions", years=5)
    status = agent.get_status()
"""

import json
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .sources import PubMedSource, ArxivSource, Source
from .workflows import QuickSearch, QuickSearchResult, LiteratureReview, ReviewPlan

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Standard-Output: Neben dem Modul-Verzeichnis
_MODULE_DIR = Path(__file__).parent
_DEFAULT_OUTPUT = _MODULE_DIR / "output"
_DEFAULT_CACHE = _MODULE_DIR / "cache"


class ResearchAgent:
    """
    Forschungspipeline -- orchestriert Quellen und Workflows.

    Kann standalone oder mit BACH-Integration betrieben werden.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        cache_dir: Optional[Path] = None,
        sources: Optional[List[Source]] = None,
        pubmed_email: Optional[str] = None,
        pubmed_api_key: Optional[str] = None,
        use_bach: bool = False,
    ):
        """
        Args:
            output_dir: Verzeichnis fuer Reports/Ergebnisse
            cache_dir: Verzeichnis fuer Suchhistorie/Cache
            sources: Liste von Source-Instanzen (Default: PubMed + arXiv)
            pubmed_email: Kontakt-E-Mail fuer NCBI (empfohlen)
            pubmed_api_key: NCBI API-Key (optional, erhoet Rate-Limit)
            use_bach: BACH-Integration aktivieren (wenn bach_api verfuegbar)
        """
        self.output_dir = output_dir or _DEFAULT_OUTPUT
        self.cache_dir = cache_dir or _DEFAULT_CACHE
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Quellen initialisieren
        if sources:
            self._sources = sources
        else:
            self._sources = [
                PubMedSource(email=pubmed_email, api_key=pubmed_api_key),
                ArxivSource(),
            ]

        # Suchhistorie laden
        self._history = self._load_history()

        # Optionale BACH-Integration
        self._bach = None
        if use_bach:
            self._init_bach()

    # --- Oeffentliche API ---

    def search(
        self,
        query: str,
        max_results: int = 5,
        sources: Optional[List[str]] = None,
        **kwargs,
    ) -> QuickSearchResult:
        """
        Schnell-Recherche ueber konfigurierte Quellen.

        Args:
            query: Suchbegriff(e)
            max_results: Max. Ergebnisse pro Quelle
            sources: Quellenfilter (z.B. ['PubMed']). None = alle.
            **kwargs: Werden an Quellen weitergegeben (z.B. min_date)

        Returns:
            QuickSearchResult mit Artikeln aus allen Quellen
        """
        active_sources = self._filter_sources(sources)
        workflow = QuickSearch(active_sources)
        result = workflow.run(query, max_results=max_results, **kwargs)

        # Suchhistorie aktualisieren
        self._add_to_history({
            "type": "quick_search",
            "query": query,
            "timestamp": result.timestamp,
            "sources": [s.name for s in active_sources],
            "total_found": result.total_found,
            "returned": len(result.top_articles),
        })

        return result

    def create_review_plan(
        self,
        topic: str,
        years: int = 5,
        execute: bool = False,
        additional_queries: Optional[List[str]] = None,
    ) -> ReviewPlan:
        """
        Erstellt einen Literatur-Review-Plan.

        Args:
            topic: Forschungsthema
            years: Zeitraum in Jahren (Default: 5)
            execute: Plan direkt ausfuehren? (Default: False)
            additional_queries: Zusaetzliche Suchbegriffe

        Returns:
            ReviewPlan (mit oder ohne Suchergebnisse)
        """
        workflow = LiteratureReview(self._sources)
        plan = workflow.create_plan(topic, years)

        if execute:
            plan = workflow.execute_plan(
                plan,
                additional_queries=additional_queries,
            )

        # Suchhistorie aktualisieren
        self._add_to_history({
            "type": "review_plan",
            "topic": topic,
            "years": years,
            "timestamp": plan.created,
            "executed": execute,
            "articles_found": plan.total_articles,
        })

        return plan

    def get_status(self) -> Dict[str, Any]:
        """Agent-Status mit Suchhistorie."""
        return {
            "agent": "ResearchAgent",
            "version": self.VERSION,
            "status": "active",
            "sources": [s.name for s in self._sources],
            "searches_total": len(self._history),
            "last_search": self._history[-1] if self._history else None,
            "output_dir": str(self.output_dir),
            "cache_dir": str(self.cache_dir),
            "bach_connected": self._bach is not None,
        }

    def save_result(
        self,
        result: Any,
        filename: Optional[str] = None,
        fmt: str = "markdown",
    ) -> Path:
        """
        Speichert ein Ergebnis als Datei.

        Args:
            result: QuickSearchResult oder ReviewPlan
            filename: Dateiname (auto-generiert wenn None)
            fmt: Format ('markdown' oder 'json')

        Returns:
            Pfad zur gespeicherten Datei
        """
        if filename is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            if hasattr(result, "query"):
                slug = result.query[:30].replace(" ", "_")
            elif hasattr(result, "topic"):
                slug = result.topic[:30].replace(" ", "_")
            else:
                slug = "result"
            ext = ".md" if fmt == "markdown" else ".json"
            filename = f"{ts}_{slug}{ext}"

        filepath = self.output_dir / filename

        if fmt == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        else:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(result.to_markdown())

        return filepath

    def get_source(self, name: str) -> Optional[Source]:
        """Einzelne Quelle nach Name abrufen."""
        for source in self._sources:
            if source.name.lower() == name.lower():
                return source
        return None

    # --- BACH-Integration ---

    def _init_bach(self):
        """Versucht BACH-Integration zu laden."""
        try:
            # bach_api muss im Python-Pfad sein
            import bach_api  # type: ignore
            self._bach = bach_api
        except ImportError:
            self._bach = None

    def log_to_bach(self, message: str, level: str = "info"):
        """Loggt in BACH (wenn verbunden)."""
        if self._bach and hasattr(self._bach, "logs"):
            self._bach.logs.add(f"[ResearchAgent] {message}", level=level)

    # --- Interne Methoden ---

    def _filter_sources(self, names: Optional[List[str]]) -> List[Source]:
        """Filtert Quellen nach Namen."""
        if names is None:
            return self._sources
        name_set = {n.lower() for n in names}
        return [s for s in self._sources if s.name.lower() in name_set]

    def _load_history(self) -> List[Dict[str, Any]]:
        history_file = self.cache_dir / "search_history.json"
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def _save_history(self):
        history_file = self.cache_dir / "search_history.json"
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(self._history[-200:], f, indent=2, ensure_ascii=False)

    def _add_to_history(self, entry: Dict[str, Any]):
        self._history.append(entry)
        self._save_history()


def main():
    """CLI-Einstiegspunkt."""
    import argparse

    parser = argparse.ArgumentParser(
        description=f"ResearchAgent v{ResearchAgent.VERSION}"
    )
    sub = parser.add_subparsers(dest="command")

    # search
    sp_search = sub.add_parser("search", help="Schnell-Recherche")
    sp_search.add_argument("query", help="Suchbegriff")
    sp_search.add_argument("-n", "--max-results", type=int, default=5)
    sp_search.add_argument("-s", "--sources", nargs="*", help="Quellen (PubMed, arXiv)")
    sp_search.add_argument("--save", action="store_true", help="Ergebnis speichern")

    # review
    sp_review = sub.add_parser("review", help="Literatur-Review")
    sp_review.add_argument("topic", help="Forschungsthema")
    sp_review.add_argument("-y", "--years", type=int, default=5)
    sp_review.add_argument("--execute", action="store_true", help="Plan ausfuehren")
    sp_review.add_argument("--save", action="store_true", help="Ergebnis speichern")

    # status
    sub.add_parser("status", help="Agent-Status")

    args = parser.parse_args()
    agent = ResearchAgent()

    if args.command == "search":
        result = agent.search(args.query, max_results=args.max_results, sources=args.sources)
        print(result.to_markdown())
        if args.save:
            path = agent.save_result(result)
            print(f"\nGespeichert: {path}")

    elif args.command == "review":
        plan = agent.create_review_plan(
            args.topic, years=args.years, execute=args.execute
        )
        print(plan.to_markdown())
        if args.save:
            path = agent.save_result(plan)
            print(f"\nGespeichert: {path}")

    elif args.command == "status":
        status = agent.get_status()
        print(f"ResearchAgent v{status['version']}")
        print(f"Status: {status['status']}")
        print(f"Quellen: {', '.join(status['sources'])}")
        print(f"Suchen gesamt: {status['searches_total']}")
        print(f"BACH verbunden: {status['bach_connected']}")
        print(f"Output: {status['output_dir']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
