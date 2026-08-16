"""
Athena recovery manifest generation.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .paths import (
    find_athena_data,
    find_athena_source,
)

from .system import (
    system_info,
)


def _count_files(
    path: Path | None,
) -> int:
    """
    Count files under path.
    """

    if path is None or not path.exists():
        return 0

    return sum(
        1
        for item in path.rglob("*")
        if item.is_file()
    )


def _find_databases(
    path: Path | None,
) -> list[str]:
    """
    Find database files.
    """

    if path is None or not path.exists():
        return []

    return sorted(
        str(item.relative_to(path))
        for item in path.rglob("*.db")
        if item.is_file()
    )


def create_manifest() -> dict:
    """
    Create Athena recovery manifest.
    """

    source = find_athena_source()
    data = find_athena_data()

    return {
        "created": (
            datetime.now()
            .isoformat()
        ),

        "athena_source": (
            str(source)
            if source
            else None
        ),

        "athena_data": (
            str(data)
            if data
            else None
        ),

        "source_files": _count_files(
            source
        ),

        "data_files": _count_files(
            data
        ),

        "databases": _find_databases(
            data
        ),

        "system": system_info(),
    }


def save_manifest(
    destination: Path,
) -> Path:
    """
    Save manifest JSON.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_text(
        json.dumps(
            create_manifest(),
            indent=2,
        )
    )

    return destination
