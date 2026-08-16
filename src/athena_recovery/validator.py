"""
Athena backup validation.
"""

from __future__ import annotations

import tarfile


def validate_backup(
    archive_path: str,
) -> dict[str, bool]:
    """
    Validate Athena backup archive.
    """

    result = {
        "archive": False,
        "manifest": False,
        "source": False,
        "user_data": False,
        "excluded_content": False,
    }

    try:
        with tarfile.open(
            archive_path,
            "r:gz",
        ) as archive:

            names = archive.getnames()

            result["archive"] = True

            result["manifest"] = (
                names.count(
                    "manifest.json"
                ) == 1
            )

            result["source"] = any(
                name.startswith(
                    "source/"
                )
                for name in names
            )

            result["user_data"] = any(
                name.startswith(
                    "user-data/"
                )
                for name in names
            )

            excluded = (
                ".git/"
                in names
                or any(
                    "/__pycache__/"
                    in name
                    for name in names
                )
                or any(
                    name.endswith(".pyc")
                    for name in names
                )
            )

            result["excluded_content"] = (
                not excluded
            )

    except Exception:
        pass

    return result
