import os
import sys
from shutil import which

from crossfiledialog.exceptions import NoImplementationFoundException

if sys.platform == "linux":
    probably_kde = (
        os.environ.get("DESKTOP_SESSION", "").lower() == "kde"
        or os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "kde"
    )

    kdialog_binary = which("kdialog")
    zenity_binary = which("zenity")

    if kdialog_binary and (probably_kde or not zenity_binary):
        from crossfiledialog.kdialog import *  # noqa: F403
    elif zenity_binary:
        from crossfiledialog.zenity import *  # noqa: F403
    else:
        try:
            from crossfiledialog.qt import *  # noqa: F403
        except ImportError:
            raise NoImplementationFoundException from None

elif sys.platform == "win32":
    from crossfiledialog.win32 import *  # noqa: F403

else:
    raise NoImplementationFoundException


__all__ = ["choose_folder", "open_file", "open_multiple", "save_file"]  # noqa: F405
