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

    not_imported = True

    # if all([kdialog_binary, (probably_kde or not zenity_binary), not_imported]):
    #     from crossfiledialog.kdialog import choose_folder, open_file, open_multiple, save_file
    #     not_imported = False

    # if zenity_binary and not_imported:
    #     from crossfiledialog.zenity import choose_folder, open_file, open_multiple, save_file

    if not_imported:
        try:
            from crossfiledialog.qt import choose_folder, open_file, open_multiple, save_file  # noqa: F403
        except ImportError:
            raise NoImplementationFoundException from None

elif sys.platform == "win32":
    from crossfiledialog.win32 import choose_folder, open_file, open_multiple, save_file  # noqa: F403

else:
    raise NoImplementationFoundException


__all__ = ["choose_folder", "open_file", "open_multiple", "save_file"]  # noqa: F405
