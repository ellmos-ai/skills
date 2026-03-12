"""
ResearchAgent -- Eigenstaendige Forschungspipeline.

Usage:
    from ResearchAgent import ResearchAgent

    agent = ResearchAgent()
    results = agent.search("CRISPR gene therapy")
"""

from .agent import ResearchAgent

__version__ = "0.1.0"
__all__ = ["ResearchAgent"]
