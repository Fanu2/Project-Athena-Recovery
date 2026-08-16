"""
Recovery foundation smoke tests.
"""

from pathlib import Path

from athena_recovery.manifest import (
    create_manifest,
)

from athena_recovery.validator import (
    validate_backup,
)


def test_manifest_creation():

    manifest = create_manifest()

    assert (
        "system"
        in manifest
    )

    assert (
        "created"
        in manifest
    )


def test_backup_validation():

    backup = Path(
        "/home/jasvir/Backups/athena-rule-test.tar.gz"
    )

    if not backup.exists():
        return

    result = validate_backup(
        str(backup)
    )

    assert result["archive"]
    assert result["manifest"]
    assert result["source"]
