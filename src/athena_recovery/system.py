"""
System information.
"""

from __future__ import annotations

import platform
import sys


def system_info() -> dict[str, str]:
    """
    Return system information.
    """

    return {
        "python": sys.version.split()[0],
        "system": platform.system(),
        "release": platform.release(),
    }
