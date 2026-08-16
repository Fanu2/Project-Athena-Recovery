"""
Athena backup creation.
"""

from __future__ import annotations

import io
import json
import tarfile
from pathlib import Path

from .manifest import (
    create_manifest,
)

from .inventory import (
    create_inventory,
)

from .paths import (
    find_athena_data,
    find_athena_source,
)

from .policy import (
    INCLUDE_DIRECTORIES,
    INCLUDE_FILES,
    should_exclude,
)


def _add_file(
    archive: tarfile.TarFile,
    file: Path,
    arcname: Path,
) -> None:
    """
    Add file to archive.
    """

    archive.add(
        file,
        arcname=str(arcname),
    )


def _add_source(
    archive: tarfile.TarFile,
    source: Path,
) -> None:
    """
    Add approved Athena source files.
    """

    for name in INCLUDE_FILES:

        file = source / name

        if file.exists():

            _add_file(
                archive,
                file,
                Path("source") / name,
            )

    for directory in INCLUDE_DIRECTORIES:

        root = source / directory

        if not root.exists():
            continue

        for item in root.rglob("*"):

            if not item.is_file():
                continue

            if should_exclude(
                item.parts,
                item.name,
            ):
                continue

            _add_file(
                archive,
                item,
                Path("source")
                / item.relative_to(source),
            )


def _add_user_data(
    archive: tarfile.TarFile,
    data: Path,
) -> None:
    """
    Add Athena user data.
    """

    for item in data.rglob("*"):

        if item.is_file():

            _add_file(
                archive,
                item,
                Path("user-data")
                / item.relative_to(data.parent),
            )



def _add_inventory(
    archive: tarfile.TarFile,
) -> None:
    """
    Add workstation inventory.
    """

    content = json.dumps(
        create_inventory(),
        indent=2,
    ).encode()

    info = tarfile.TarInfo(
        "inventory.json"
    )

    info.size = len(content)

    archive.addfile(
        info,
        fileobj=io.BytesIO(content),
    )


def _add_manifest(
    archive: tarfile.TarFile,
) -> None:
    """
    Add manifest once.
    """

    content = json.dumps(
        create_manifest(),
        indent=2,
    ).encode()

    info = tarfile.TarInfo(
        "manifest.json"
    )

    info.size = len(content)

    archive.addfile(
        info,
        fileobj=io.BytesIO(content),
    )


def create_backup(
    destination: Path,
) -> Path:
    """
    Create Athena backup archive.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with tarfile.open(
        destination,
        "w:gz",
    ) as archive:

        _add_manifest(
            archive
        )

        _add_inventory(
            archive
        )

        source = find_athena_source()

        if source:

            _add_source(
                archive,
                source,
            )

        data = find_athena_data()

        if data:

            _add_user_data(
                archive,
                data,
            )

    return destination
