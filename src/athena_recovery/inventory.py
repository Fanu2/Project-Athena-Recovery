"""
Athena workstation recovery inventory.
"""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path

from .paths import (
    find_athena_data,
    find_athena_source,
)


def _git_revision(
    source: Path | None,
) -> str | None:
    """
    Return Athena git revision.
    """

    if source is None:
        return None

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(source),
                "rev-parse",
                "HEAD",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception:
        pass

    return None


def _databases(
    data: Path | None,
) -> list[str]:
    """
    Find Athena databases.
    """

    if data is None:
        return []

    return [
        str(path.name)
        for path in data.rglob("*.db")
    ]


def _ollama_models() -> list[str]:
    """
    Return installed Ollama models.
    """

    try:
        result = subprocess.run(
            [
                "ollama",
                "list",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return []

        lines = result.stdout.splitlines()

        return [
            line.split()[0]
            for line in lines[1:]
            if line.strip()
        ]

    except Exception:
        return []


def create_inventory() -> dict:
    """
    Create workstation inventory.
    """

    source = find_athena_source()
    data = find_athena_data()

    return {
        "system": {
            "platform": platform.system(),
            "release": platform.release(),
            "python": sys.version,
        },
        "athena": {
            "source": (
                str(source)
                if source
                else None
            ),
            "git_revision": _git_revision(
                source
            ),
            "databases": _databases(
                data
            ),
        },
        "ai_runtime": {
            "ollama_models": _ollama_models(),
        },
    }


def save_inventory(
    destination: str,
) -> Path:
    """Save inventory snapshot as JSON."""

    import json

    output = Path(destination)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            create_inventory(),
            indent=2,
        )
    )

    return output
