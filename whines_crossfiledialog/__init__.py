import sys
from shutil import which
from typing import Optional

from whines_crossfiledialog.exceptions import NoImplementationFoundException
from whines_crossfiledialog.utils import BaseFileDialog

# Global variable to store picker preferences
default_picker_preferences = ["kdialog", "pygobject", "qt", "zenity"]


def file_dialog(picker_preference: Optional[list[str]] = None) -> type[BaseFileDialog]:  # noqa: C901
    """
    From a list of (optional) file picker preferences, return the first available implementation. 

    Args:
    - picker_preference (`Optional[list[str]]`, optional): Order of precedence for picking the file picker implementations. Defaults to `None`.

    Raises:
    - `NoImplementationFoundException`: Raise when no implementation is found from the list of preferences
    - `NoImplementationFoundException`: Raise when no implementation is found for the current platform

    Returns:
    `BaseFileDialog`: File picker class.

    """
    if sys.platform == "linux":
        kdialog_binary = which("kdialog")
        zenity_binary = which("zenity")

        # Get preferences
        preferred_pickers = (
            picker_preference if picker_preference else default_picker_preferences
        )

        # Import pickers based on preferences
        for picker in preferred_pickers:
            if picker == "kdialog" and kdialog_binary:
                from whines_crossfiledialog.file_pickers.kdialog import (  # type: ignore[assignment]
                    FileDialog,
                )

                return FileDialog

            if picker == "pygobject":
                from whines_crossfiledialog.file_pickers.pygobject import (  # type: ignore[assignment]
                    FileDialog,
                )

                return FileDialog

            if picker == "qt":
                from whines_crossfiledialog.file_pickers.qt import (  # type: ignore[assignment]
                    FileDialog,
                )

                return FileDialog

            if picker == "zenity" and zenity_binary:
                from whines_crossfiledialog.file_pickers.zenity import (  # type: ignore[assignment]
                    FileDialog,
                )

                return FileDialog

        raise NoImplementationFoundException

    if sys.platform == "win32":
        from whines_crossfiledialog.file_pickers.win32 import (  # type: ignore[assignment]
            FileDialog,
        )

        return FileDialog

    raise NoImplementationFoundException
