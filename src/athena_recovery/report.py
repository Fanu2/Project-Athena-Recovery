"""
Athena recovery reports.
"""

from __future__ import annotations

import json
from pathlib import Path


def create_restore_report(
    destination: Path,
    archive: str,
    file_count: int,
    output: Path,
) -> Path:
    """
    Create restore report.
    """

    report = {
        "status": "success",
        "archive": archive,
        "destination": str(destination),
        "restored_files": file_count,
        "manifest_present": (
            (destination / "manifest.json").exists()
        ),
        "inventory_present": (
            (destination / "inventory.json").exists()
        ),
    }

    output.write_text(
        json.dumps(
            report,
            indent=2,
        )
    )

    return output
