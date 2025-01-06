import os
import sys
from subprocess import PIPE, Popen
from typing import Optional

from crossfiledialog import strings
from crossfiledialog.exceptions import FileDialogException


class KDialogException(FileDialogException):
    pass


last_cwd: Optional[str] = None


def get_preferred_cwd():
    possible_cwd = os.environ.get("FILEDIALOG_CWD", "")
    if possible_cwd:
        return possible_cwd

    global last_cwd
    if last_cwd:
        return last_cwd


def set_last_cwd(cwd):
    global last_cwd
    last_cwd = os.path.dirname(cwd)


def run_kdialog(*args, **kwargs):  # noqa: C901
    cmdlist = ["kdialog"]
    cmdlist.extend("--{}".format(arg) for arg in args)

    if "start_dir" in kwargs:
        cmdlist.append(kwargs.pop("start_dir"))

    if "filter" in kwargs:
        cmdlist.append(kwargs.pop("filter"))

    for k, v in kwargs.items():
        cmdlist.append("--{}".format(k))
        cmdlist.append(v)

    extra_kwargs = {}
    preferred_cwd = get_preferred_cwd()
    if preferred_cwd:
        extra_kwargs["cwd"] = preferred_cwd

    process = Popen(cmdlist, stdout=PIPE, stderr=PIPE, **extra_kwargs)  # noqa: S603
    stdout, stderr = process.communicate()

    if process.returncode == -1:
        raise KDialogException("Unexpected error during kdialog call")

    stdout, stderr = stdout.decode(), stderr.decode()  # type: ignore
    if stderr.strip():
        sys.stderr.write(stderr)

    return stdout.strip()


def open_file(  # noqa: C901
    title: str = strings.open_file,
    start_dir: Optional[str] = None,
    filter: Optional[str | list[str | list[str]] | dict[str, str | list[str]]] = None,
):
    r"""
    Open a file selection dialog for selecting a file using KDialog.

    Args:
        title (str, optional): The title of the file selection dialog.
            Default is 'Choose a file'
        start_dir (str, optional): The starting directory for the dialog.
        filter (str, list, dict, optional): The filter for file types to display. It can be either:
            - a single wildcard (e.g.: `"*.py"`, all files are displayed ending .py)
            - a list of wildcards (e.g.: `["*.py", "*.md"]`, all files are displayed ending either .py or .md)
            - a list of list optional one or more wildcards (e.g.: `[["*.py", "*.md"], ["*.txt"]]`,
            user can switch between (.py, .md) and (.txt))
            - a dictionary mapping descriptions to wildcards (e.g.: `{"PDF-Files": "*.pdf", "Python Project": ["\*.py", "*.md"]}`)

    Returns:
        str: The selected file's path.

    Example:
        result = open_file(title="Select a file", start_dir="/path/to/starting/directory", filter="*.txt")

    """
    kdialog_kwargs = {"title": title}

    if start_dir:
        kdialog_kwargs["start_dir"] = start_dir

    if filter:
        if isinstance(filter, str):
            # Filter is a single wildcard.
            kdialog_kwargs["filter"] = filter
        elif isinstance(filter, list):
            if isinstance(filter[0], str):
                # Filter is a list of wildcards.
                kdialog_kwargs["filter"] = " ".join(filter)
            elif isinstance(filter[0], list):
                # Filter is a list of lists with wildcards.
                kdialog_kwargs["filter"] = " | ".join(" ".join(f) for f in filter)
            else:
                raise ValueError("Invalid filter")
        elif isinstance(filter, dict):
            # Filter is a dictionary mapping descriptions to wildcards or lists of wildcards.
            filters = []
            for key, value in filter.items():
                if isinstance(value, str):
                    filters.append("{} ({})".format(key, value))
                elif isinstance(value, list):
                    filters.append("{} ({})".format(key, " ".join(value)))
                else:
                    raise ValueError("Invalid filter")

            kdialog_kwargs["filter"] = " | ".join(
                filters,
            )
        else:
            raise ValueError("Invalid filter")

    result = run_kdialog("getopenfilename", **kdialog_kwargs)
    if result:
        set_last_cwd(result)
    return result


def open_multiple(  # noqa: C901
    title=strings.open_multiple,
    start_dir=None,
    filter=None,
):
    """
    Open a file selection dialog for selecting multiple files using KDialog.

    Args:
        title (str, optional): The title of the file selection dialog.
            Default is 'Choose one or more files'
        start_dir (str, optional): The starting directory for the dialog.
        filter (optional): The filter for file types to display.

    Returns:
        list[str]: A list of selected file paths.

    Example:
        result = open_multiple(title="Select multiple files",
        start_dir="/path/to/starting/directory", filter="*.txt")

    """
    kdialog_kwargs = {"title": title}

    if start_dir:
        kdialog_kwargs["start_dir"] = start_dir

    if filter:
        if isinstance(filter, str):
            # Filter is a single wildcard.
            kdialog_kwargs["filter"] = filter
        elif isinstance(filter, list):
            if isinstance(filter[0], str):
                # Filter is a list of wildcards.
                kdialog_kwargs["filter"] = " ".join(filter)
            elif all(isinstance(i, list) for i in filter) and all(
                all(isinstance(j, str) for j in i) for i in filter
            ):
                # Filter is a list of lists with wildcards.
                kdialog_kwargs["filter"] = " | ".join(" ".join(f) for f in filter)
            else:
                raise ValueError("Invalid filter")
        elif isinstance(filter, dict):
            # Filter is a dictionary mapping descriptions to wildcards or lists of wildcards.
            filters = []
            for key, value in filter.items():
                if isinstance(value, str):
                    filters.append("{} ({})".format(key, value))
                elif isinstance(value, list):
                    filters.append("{} ({})".format(key, " ".join(value)))
                else:
                    raise ValueError("Invalid filter")

            kdialog_kwargs["filter"] = " | ".join(
                filters,
            )
        else:
            raise ValueError("Invalid filter")

    result = run_kdialog("getopenfilename", "multiple", **kdialog_kwargs)
    result_list = list(map(str.strip, result.split(" ")))
    if result_list:
        set_last_cwd(result_list[0])
        return result_list
    return []


def save_file(title=strings.save_file, start_dir=None):
    """
    Open a save file dialog using KDialog.

    Args:
        title (str, optional): The title of the save file dialog.
            Default is 'Enter the name of the file to save to'
        start_dir (str, optional): The starting directory for the dialog.

    Returns:
        str: The selected file's path for saving.

    Example:
        result = save_file(title="Save file", start_dir="/path/to/starting/directory")

    """
    kdialog_args = ["getsavefilename"]
    kdialog_kwargs = {"title": title}

    if start_dir:
        kdialog_kwargs["start_dir"] = start_dir

    result = run_kdialog(*kdialog_args, **kdialog_kwargs)
    if result:
        set_last_cwd(result)
    return result


def choose_folder(title=strings.choose_folder, start_dir=None):
    """
    Open a folder selection dialog using KDialog.

    Args:
        title (str, optional): The title of the folder selection dialog.
            Default is 'Choose a folder'
        start_dir (str, optional): The starting directory for the dialog.

    Returns:
        str: The selected folder's path.

    Example:
        result = choose_folder(title="Select folder", start_dir="/path/to/starting/directory")

    """
    kdialog_kwargs = {"title": title}

    if start_dir:
        kdialog_kwargs["start_dir"] = start_dir

    result = run_kdialog("getexistingdirectory", **kdialog_kwargs)
    if result:
        set_last_cwd(result)
    return result


__all__ = ["choose_folder", "open_file", "open_multiple", "save_file"]
