# -*- coding: utf-8 -*-
"""
devSoftAgent Policies.

Standalone policy definitions for code quality enforcement:
- Naming conventions (file, class, function, variable naming)
- Encoding standards (UTF-8, BOM handling, line endings)
- Path rules (normalization, forbidden patterns)

These policies can be used standalone or integrated into
code analysis and review workflows.
"""

from .naming import NamingPolicy
from .encoding import EncodingPolicy
from .paths import PathPolicy

__all__ = ["NamingPolicy", "EncodingPolicy", "PathPolicy"]
