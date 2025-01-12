import os
import sys
from shutil import which
from typing import Optional

from crossfiledialog.exceptions import NoImplementationFoundException

# Global variable to store picker preferences
default_picker_preferences = ["gtk", "zenity", "kdialog", "qt"]


def file_dialog(picker_preference: Optional[list[str]] = None):  # noqa: C901
    if sys.platform == "linux":
        probably_kde = (
            os.environ.get("DESKTOP_SESSION", "").lower() == "kde"
            or os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "kde"
        )

        kdialog_binary = which("kdialog")
        zenity_binary = which("zenity")

        # Get preferences
        preferred_picklers = (
            picker_preference if picker_preference else default_picker_preferences
        )

        # Import pickers based on preferences
        for picker in preferred_picklers:
            if (
                picker == "kdialog"
                and kdialog_binary
                and (probably_kde or not zenity_binary)
            ):
                print("kdialog")
                from crossfiledialog.file_pickers.kdialog import (  # type: ignore[assignment]
                    FileDialog,
                )

                return FileDialog
            if picker == "zenity" and zenity_binary:
                print("zenity")
                from crossfiledialog.file_pickers.zenity import (  # type: ignore[assignment]
                    FileDialog,
                )

                return FileDialog
            if picker == "qt":
                print("qt")
                from crossfiledialog.file_pickers.qt import (  # type: ignore[assignment]
                    FileDialog,
                )

                return FileDialog

        raise NoImplementationFoundException

    if sys.platform == "win32":
        print("win32")
        from crossfiledialog.file_pickers.win32 import FileDialog

        return FileDialog

    raise NoImplementationFoundException
