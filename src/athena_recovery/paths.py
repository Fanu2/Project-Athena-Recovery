"""
Athena path detection.
"""

from __future__ import annotations

from pathlib import Path


def find_athena_source() -> Path | None:
    """
    Find Athena source directory.
    """

    candidates = [
        Path.home() / "Project-Athena",
        Path.cwd().parent / "Project-Athena",
    ]

    for path in candidates:
        if (
            path.exists()
            and (path / "src").exists()
        ):
            return path

    return None


def find_athena_data() -> Path | None:
    """
    Find Athena user data directory.
    """

    path = (
        Path.home()
        / ".athena"
    )

    if path.exists():
        return path

    return None
