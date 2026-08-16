"""
Athena Recovery CLI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .backup import create_backup
from .manifest import create_manifest
from .paths import find_athena_data, find_athena_source
from .system import system_info
from .validator import validate_backup
from .restore import restore_backup
from .inventory import create_inventory, save_inventory


def info_command() -> None:
    print("Athena Recovery Utility")
    print()

    print("Athena Source:")
    print(find_athena_source() or "Not found")

    print()

    print("Athena Data:")
    print(find_athena_data() or "Not found")

    print()

    info = system_info()

    print(f"Python: {info['python']}")
    print(f"System: {info['system']} {info['release']}")


def manifest_command() -> None:
    output = Path("athena-manifest.json")

    output.write_text(
        json.dumps(
            create_manifest(),
            indent=2,
        )
    )

    print("Manifest created:")
    print(output.resolve())


def backup_command(
    destination: str,
) -> None:

    output = create_backup(
        Path(destination).expanduser()
    )

    print("Backup created:")
    print(output)


def validate_command(
    archive: str,
) -> None:

    result = validate_backup(
        archive,
    )

    print("Athena Backup Validation")
    print()

    for name, passed in result.items():

        status = (
            "PASS"
            if passed
            else "FAIL"
        )

        print(
            f"{name}: {status}"
        )


def restore_command(
    archive: str,
    destination: str,
) -> None:

    output = restore_backup(
        archive,
        destination,
    )

    print("Restore completed:")
    print(output)


def inventory_command() -> None:

    print("Athena Recovery Inventory")
    print()

    inventory = create_inventory()

    for section, values in inventory.items():

        print(f"{section}:")

        if isinstance(values, dict):

            for key, value in values.items():
                print(
                    f"  {key}: {value}"
                )

        else:
            print(
                f"  {values}"
            )

        print()


def main() -> None:

    if len(sys.argv) < 2:
        info_command()
        return

    command = sys.argv[1]

    if command == "info":

        info_command()

    elif command == "manifest":

        manifest_command()

    elif command == "backup":

        if len(sys.argv) < 3:
            print(
                "Usage: backup <destination>"
            )
            return

        backup_command(
            sys.argv[2]
        )

    elif command == "validate":

        if len(sys.argv) < 3:
            print(
                "Usage: validate <archive>"
            )
            return

        validate_command(
            sys.argv[2]
        )

    elif command == "restore":

        if len(sys.argv) < 4:
            print(
                "Usage: restore <archive> <destination>"
            )
            return

        restore_command(
            sys.argv[2],
            sys.argv[3],
        )

    elif command == "inventory":

        if "--output" in sys.argv:

            index = sys.argv.index(
                "--output"
            )

            if len(sys.argv) > index + 1:

                output = save_inventory(
                    sys.argv[index + 1]
                )

                print(
                    "Inventory saved:"
                )

                print(output)

                return

        inventory_command()

    else:

        print(
            f"Unknown command: {command}"
        )


if __name__ == "__main__":
    main()
