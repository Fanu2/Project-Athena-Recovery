"""
Athena backup validation.
"""

from __future__ import annotations

import json
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
        "inventory": False,
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

            result["inventory"] = (
                names.count(
                    "inventory.json"
                ) == 1
            )

            if result["inventory"]:

                try:
                    data = archive.extractfile(
                        "inventory.json"
                    )

                    if data:
                        json.load(
                            data
                        )

                        result["inventory"] = True

                except Exception:

                    result["inventory"] = False


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


            excluded = any(
                (
                    name.startswith(
                        ".git/"
                    )
                    or "/__pycache__/" in name
                    or name.endswith(
                        ".pyc"
                    )
                )
                for name in names
            )

            result["excluded_content"] = (
                not excluded
            )

    except Exception:
        pass

    return result
