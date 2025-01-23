import os
import sys
from subprocess import PIPE, Popen
from typing import Optional

from crossfiledialog import strings
from crossfiledialog.exceptions import FileDialogException
from crossfiledialog.utils import BaseFileDialog, filter_processor


class ZenityException(FileDialogException):
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


def run_zenity(*args, **kwargs) -> str:
    cmdlist = ["zenity"]
    cmdlist.extend("--{}".format(arg) for arg in args)
    cmdlist.extend("--{}={}".format(k, v) for k, v in kwargs.items())

    extra_kwargs = {}
    preferred_cwd = get_preferred_cwd()
    if preferred_cwd:
        extra_kwargs["cwd"] = preferred_cwd

    process = Popen(cmdlist, stdout=PIPE, stderr=PIPE, **extra_kwargs)  # noqa: S603
    stdout, stderr = process.communicate()

    if process.returncode == -1:
        raise ZenityException("Unexpected error during zenity call")

    stdout, stderr = stdout.decode(), stderr.decode()  # type: ignore

    if stderr.strip():
        sys.stderr.write(stderr)

    return stdout.strip()  # type: ignore[no-any-return]


class FileDialog(BaseFileDialog):
    @staticmethod
    def open_file(  # noqa: C901
        title: str = strings.open_file,
        start_dir: Optional[str] = None,
        filter: Optional[
            str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
        ] = None,
    ) -> Optional[str]:
        """
        Open a file selection dialog for selecting a file using Zenity.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose a file'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`Optional[str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]]`, optional):
            The filter for file types to display. For an example, head to documentation the
            of `crossfiledialog.utils.filter_processor`.

        Returns:
        `Optional[str]`: The selected file's path.

        Example:
        result = open_file(title="Select a file", start_dir="/path/to/starting/directory", filter="*.txt")

        """
        zenity_args: list[str] = []
        zenity_kwargs = {"title": title}

        if start_dir:
            # If the path doesn't end with a backslash, Zenity only
            # starts in the parent directory and selects the directory.
            if start_dir[-1] != "/":
                start_dir += "/"
            zenity_kwargs["filename"] = start_dir

        if filter:
            for i in filter_processor(filter, (" ", "{} | {}")):
                zenity_args.append("file-filter={}".format(i))

        result = run_zenity("file-selection", *zenity_args, **zenity_kwargs)
        if result:
            set_last_cwd(result)
        return result

    @staticmethod
    def open_multiple(  # noqa: C901
        title: str = strings.open_multiple,
        start_dir: Optional[str] = None,
        filter: Optional[
            str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
        ] = None,
    ) -> list[str]:
        """
        Open a file selection dialog for selecting multiple files using Zenity.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose one or more files'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`Optional[str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]]`, optional):
            The filter for file types to display. For an example, head to documentation the
            of `crossfiledialog.utils.filter_processor`.

        Returns:
        `list[str]`: A list of selected file paths.

        Example:
            result = open_multiple(title="Select multiple files",
            start_dir="/path/to/starting/directory", filter="*.txt")

        """
        zenity_args: list[str] = []
        zenity_kwargs = {"title": title}

        if start_dir:
            # If the path doesn't end with a backslash, Zenity only starts in the parent directory
            # and selects the directory in the dialog.
            if start_dir[-1] != "/":
                start_dir += "/"
            zenity_kwargs["filename"] = start_dir

        if filter:
            for i in filter_processor(filter, (" ", "{} | {}")):
                zenity_args.append("file-filter={}".format(i))

        result = run_zenity("file-selection", "multiple", *zenity_args, **zenity_kwargs)
        split_result = result.split("|")
        if split_result:
            set_last_cwd(split_result[0])
            return split_result
        return []

    @staticmethod
    def save_file(
        title: str = strings.save_file,
        start_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Open a save file dialog using Zenity.

        Args:
        - title (`str`, optional): The title of the save file dialog.
            Default is 'Enter the name of the file to save to'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected file's path for saving.

        Example:
        result = save_file(title="Save file", start_dir="/path/to/starting/directory")

        """
        zenity_args = ["file-selection", "save", "confirm-overwrite"]
        zenity_kwargs = {"title": title}

        if start_dir:
            # If the path doesn't end with a backslash, Zenity only starts in the parent directory
            # and selects the directory in the dialog.
            if start_dir[-1] != "/":
                start_dir += "/"
            zenity_kwargs["filename"] = start_dir

        result = run_zenity(*zenity_args, **zenity_kwargs)
        if result:
            set_last_cwd(result)
        return result

    @staticmethod
    def choose_folder(
        title: str = strings.choose_folder,
        start_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Open a folder selection dialog using Zenity.

        Args:
        - title (`str`, optional): The title of the folder selection dialog.
            Default is 'Choose a folder'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected folder's path.

        Example:
            result = choose_folder(title="Select folder", start_dir="/path/to/starting/directory")

        """
        zenity_kwargs = {"title": title}

        if start_dir:
            # If the path doesn't end with a backslash, Zenity only starts in the parent directory
            # and selects the directory in the dialog.
            if start_dir[-1] != "/":
                start_dir += "/"
            zenity_kwargs["filename"] = start_dir

        result = run_zenity("file-selection", "directory", **zenity_kwargs)
        if result:
            set_last_cwd(result)
        return result
