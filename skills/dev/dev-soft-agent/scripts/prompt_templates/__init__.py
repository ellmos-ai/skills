# -*- coding: utf-8 -*-
"""
devSoftAgent Prompt Templates.

Provides standardized prompt templates for automated development sessions.
Templates use {{VARIABLE}} placeholders for dynamic content.

Available templates:
    - task_prompt.txt:     Task execution prompt
    - review_prompt.txt:   Code review prompt
    - analysis_prompt.txt: Project analysis prompt
"""

from pathlib import Path
from typing import Dict

_TEMPLATE_DIR = Path(__file__).parent


def load_template(name: str) -> str:
    """Load a prompt template by name.

    Args:
        name: Template name (without .txt extension)

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template does not exist
    """
    path = _TEMPLATE_DIR / f"{name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def render_template(name: str, variables: Dict[str, str]) -> str:
    """Load and render a template with variable substitution.

    Args:
        name: Template name (without .txt extension)
        variables: Dict of {{KEY}}: value pairs

    Returns:
        Rendered template string
    """
    content = load_template(name)
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        content = content.replace(placeholder, str(value))
    return content


def list_templates():
    """List available template names."""
    return [p.stem for p in _TEMPLATE_DIR.glob("*.txt")]
