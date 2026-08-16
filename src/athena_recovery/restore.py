"""
Athena backup restore with safety checks.
"""

from __future__ import annotations

import tarfile
from pathlib import Path

from .report import create_restore_report


def _validate_archive(
    archive: tarfile.TarFile,
) -> None:
    """
    Validate archive structure.
    """

    names = archive.getnames()

    if names.count(
        "manifest.json"
    ) != 1:
        raise ValueError(
            "Invalid backup: manifest missing or duplicated"
        )

    for name in names:

        if name.startswith(
            "/"
        ):
            raise ValueError(
                "Unsafe archive path"
            )

        if ".." in Path(name).parts:
            raise ValueError(
                "Path traversal detected"
            )


def restore_backup(
    archive_path: str,
    destination: str,
) -> Path:
    """
    Safely restore Athena backup.
    """

    archive_file = Path(
        archive_path
    ).expanduser()

    if not archive_file.exists():
        raise FileNotFoundError(
            archive_file
        )

    target = Path(
        destination
    ).expanduser()

    if target.exists():

        if any(
            target.iterdir()
        ):
            raise ValueError(
                "Restore destination is not empty"
            )

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    with tarfile.open(
        archive_file,
        "r:gz",
    ) as archive:

        _validate_archive(
            archive
        )

        archive.extractall(
            target
        )

    report = create_restore_report(
        destination=target,
        archive=str(archive_file),
        file_count=len(
            list(
                target.rglob("*")
            )
        ),
        output=(
            target
            / "restore-report.json"
        ),
    )

    return target
