"""
Athena recovery backup policy.

Defines what is included and excluded
from Athena backups.
"""

from __future__ import annotations


# Top-level directories to preserve.
INCLUDE_DIRECTORIES = (
    "src",
    "docs",
    "engineering",
    "scripts",
    "tools",
    "tests",
    ".github",
    "benchmarks",
)


# Individual files to preserve.
INCLUDE_FILES = (
    "README.md",
    "pyproject.toml",
)


# Generated or rebuildable content.
EXCLUDE_NAMES = (
    ".git",
    "build",
    "build-dir",
    "dist",
    "flatpak-venv",
    ".pytest_cache",
    "reports",
    "__pycache__",
    ".venv",
    "venv",
)


EXCLUDE_SUFFIXES = (
    ".pyc",
    ".pyo",
)


def should_exclude(
    parts: tuple[str, ...],
    filename: str,
) -> bool:
    """
    Return True if path should not be backed up.
    """

    if any(
        part in EXCLUDE_NAMES
        for part in parts
    ):
        return True

    if filename.endswith(
        EXCLUDE_SUFFIXES
    ):
        return True

    return False
