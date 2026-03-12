# -*- coding: utf-8 -*-
"""
Naming Convention Policy.

Validates and enforces naming conventions for Python projects:
- Modules: snake_case.py
- Classes: PascalCase
- Functions: snake_case
- Constants: SCREAMING_SNAKE_CASE
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class NamingViolation:
    """A naming convention violation."""
    name: str
    expected_style: str
    actual_pattern: str
    message: str


class NamingPolicy:
    """Validates naming conventions.

    Usage:
        policy = NamingPolicy()
        violations = policy.check_module_name("myBadName.py")
        violations = policy.check_class_name("bad_class")
    """

    PATTERNS = {
        "snake_case": re.compile(r"^[a-z][a-z0-9_]*$"),
        "PascalCase": re.compile(r"^[A-Z][a-zA-Z0-9]*$"),
        "SCREAMING_SNAKE": re.compile(r"^[A-Z][A-Z0-9_]*$"),
    }

    def check_module_name(self, filename: str) -> List[NamingViolation]:
        """Check if a Python module filename follows snake_case."""
        name = filename.replace(".py", "")
        if name.startswith("__") and name.endswith("__"):
            return []  # dunder modules are fine
        if not self.PATTERNS["snake_case"].match(name):
            return [NamingViolation(
                name=filename,
                expected_style="snake_case",
                actual_pattern=name,
                message=f"Module '{filename}' should be snake_case",
            )]
        return []

    def check_class_name(self, name: str) -> List[NamingViolation]:
        """Check if a class name follows PascalCase."""
        if not self.PATTERNS["PascalCase"].match(name):
            return [NamingViolation(
                name=name,
                expected_style="PascalCase",
                actual_pattern=name,
                message=f"Class '{name}' should be PascalCase",
            )]
        return []

    def check_function_name(self, name: str) -> List[NamingViolation]:
        """Check if a function name follows snake_case."""
        if name.startswith("__") and name.endswith("__"):
            return []  # dunder methods
        clean = name.lstrip("_")
        if clean and not self.PATTERNS["snake_case"].match(clean):
            return [NamingViolation(
                name=name,
                expected_style="snake_case",
                actual_pattern=name,
                message=f"Function '{name}' should be snake_case",
            )]
        return []

    def check_constant_name(self, name: str) -> List[NamingViolation]:
        """Check if a constant follows SCREAMING_SNAKE_CASE."""
        if not self.PATTERNS["SCREAMING_SNAKE"].match(name):
            return [NamingViolation(
                name=name,
                expected_style="SCREAMING_SNAKE_CASE",
                actual_pattern=name,
                message=f"Constant '{name}' should be SCREAMING_SNAKE_CASE",
            )]
        return []
