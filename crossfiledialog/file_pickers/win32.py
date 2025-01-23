import os
from typing import Optional

from crossfiledialog import strings
from crossfiledialog.exceptions import (
    FileDialogException,
    NoImplementationFoundException,
)

try:
    import pywintypes  # type: ignore
    import win32con  # type: ignore
    import win32gui  # type: ignore
    from win32com.shell import shell, shellcon  # type: ignore

except ImportError:
    raise NoImplementationFoundException(
        "Running 'filedialog' on Windows requires the 'pywin32' package.",
    ) from None

from crossfiledialog.utils import BaseFileDialog


class Win32Exception(FileDialogException):
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


def error_handling_wrapper(struct, **kwargs):
    if "InitialDir" not in kwargs:
        kwargs["InitialDir"] = get_preferred_cwd()

    if "Flags" in kwargs:
        kwargs["Flags"] = kwargs["Flags"] | win32con.OFN_EXPLORER
    else:
        kwargs["Flags"] = win32con.OFN_EXPLORER

    try:
        file_name, custom_filter, flags = struct(**kwargs)
        return file_name

    except pywintypes.error:
        return None


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
        Open a file selection dialog for selecting a file using Windows API.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose a file'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]`, optional):
            The filter for file types to display. For an example, head to documentation the
            of `crossfiledialog.utils.filter_processor`.

        Returns:
        `Optional[str]`: The selected file's path.

        Example:
        result = open_file(title="Select a file", start_dir="/path/to/starting/directory", filter="*.txt")

        """
        win_kwargs = {"Title": title}

        last_cwd = get_preferred_cwd()
        if start_dir:
            win_kwargs["InitialDir"] = start_dir
        elif last_cwd:
            win_kwargs["InitialDir"] = last_cwd

        if filter:
            if isinstance(filter, str):
                # Filter is a single wildcard.
                win_kwargs["Filter"] = filter + "\0" + filter + "\0"
            elif isinstance(filter, list):
                if isinstance(filter[0], str):
                    # Filter is a list of wildcards.
                    win_kwargs["Filter"] = (
                        " ".join(filter) + "\0" + ";".join(filter) + "\0"
                    )
                elif isinstance(filter[0], list):
                    # Filter is a list of list with wildcards.
                    win_kwargs["Filter"] = "".join(
                        " ".join(f) + "\0" + ";".join(f) + "\0" for f in filter
                    )
                else:
                    raise ValueError("Invalid filter")
            elif isinstance(filter, dict):
                # Filter is a dictionary mapping descriptions to wildcards or lists of wildcards.
                filters = ""
                for key, value in filter.items():
                    if isinstance(value, str):
                        filters += "{}\0{}\0".format(key, value)
                    elif isinstance(value, list):
                        filters += "{}\0{}\0".format(key, ";".join(value))
                    else:
                        raise ValueError("Invalid filter")

                win_kwargs["Filter"] = filters
            else:
                raise ValueError("Invalid filter")

        file_name: Optional[str] = error_handling_wrapper(
            win32gui.GetOpenFileNameW,
            **win_kwargs,
        )

        if file_name:
            set_last_cwd(file_name)
        return file_name

    @staticmethod
    def open_multiple(  # noqa: C901
        title: str = strings.open_multiple,
        start_dir: Optional[str] = None,
        filter: Optional[
            str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
        ] = None,
    ) -> list[str]:
        """
        Open a file selection dialog for selecting multiple files using Windows API.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose one or more files'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]`, optional):
            The filter for file types to display. For an example, head to documentation the
            of `crossfiledialog.utils.filter_processor`.

        Returns:
        `list[str]`: A list of selected file paths.

        Example:
        result = open_multiple(title="Select multiple files",
        start_dir="/path/to/starting/directory", filter="*.txt")

        """
        win_kwargs = {"Title": title}

        last_cwd = get_preferred_cwd()
        if start_dir:
            win_kwargs["InitialDir"] = start_dir
        elif last_cwd:
            win_kwargs["InitialDir"] = last_cwd

        if filter:
            if isinstance(filter, str):
                # Filter is a single wildcard.
                win_kwargs["Filter"] = filter + "\0" + filter + "\0"
            elif isinstance(filter, list):
                if isinstance(filter[0], str):
                    # Filter is a list of wildcards.
                    win_kwargs["Filter"] = (
                        " ".join(filter) + "\0" + ";".join(filter) + "\0"
                    )
                elif isinstance(filter[0], list):
                    # Filter is a list of list with wildcards.
                    win_kwargs["Filter"] = "".join(
                        " ".join(f) + "\0" + ";".join(f) + "\0" for f in filter
                    )
                else:
                    raise ValueError("Invalid filter")
            elif isinstance(filter, dict):
                # Filter is a dictionary mapping descriptions to wildcards or lists of wildcards.
                filters = ""
                for key, value in filter.items():
                    if isinstance(value, str):
                        filters += "{}\0{}\0".format(key, value)
                    elif isinstance(value, list):
                        filters += "{}\0{}\0".format(key, ";".join(value))
                    else:
                        raise ValueError("Invalid filter")

                win_kwargs["Filter"] = filters
            else:
                raise ValueError("Invalid filter")

        file_names = error_handling_wrapper(
            win32gui.GetOpenFileNameW,
            **win_kwargs,
            Flags=win32con.OFN_ALLOWMULTISELECT,
        )

        if file_names:
            file_names_list: list[str] = file_names.split("\x00")
            if len(file_names_list) > 1:
                dirname = file_names_list[0]
                file_names_list_nodir = file_names_list[1:]
                file_names_list = [
                    os.path.join(dirname, file_name)
                    for file_name in file_names_list_nodir
                ]

            set_last_cwd(file_names_list[0])
            return file_names_list

        return []

    @staticmethod
    def save_file(
        title: str = strings.save_file,
        start_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Open a save file dialog using Windows API.

        Args:
        - title (`str`, optional): The title of the save file dialog.
            Default is 'Enter the name of the file to save to'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected file's path for saving.

        Example:
        result = save_file(title="Save file", start_dir="/path/to/starting/directory")

        """
        win_kwargs = {"Title": title}

        last_cwd = get_preferred_cwd()
        if start_dir:
            win_kwargs["InitialDir"] = start_dir
        elif last_cwd:
            win_kwargs["InitialDir"] = last_cwd

        file_name: Optional[str] = error_handling_wrapper(
            win32gui.GetSaveFileNameW,
            **win_kwargs,
            Flags=win32con.OFN_OVERWRITEPROMPT,
        )

        if file_name:
            set_last_cwd(file_name)
        return file_name

    @staticmethod
    def choose_folder(
        title: str = strings.choose_folder,
        start_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Open a folder selection dialog using Windows API.

        Args:
        - title (`str`, optional): The title of the folder selection dialog.
            Default is 'Choose a folder'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected folder's path.

        Example:
        result = choose_folder(title="Select folder", start_dir="/path/to/starting/directory")

        """
        last_cwd = get_preferred_cwd()
        if start_dir:
            start_pidl, _ = shell.SHParseDisplayName(start_dir, 0, None)
        elif last_cwd:
            start_pidl, _ = shell.SHParseDisplayName(last_cwd, 0, None)
        else:
            # default directory is the desktop
            start_pidl = shell.SHGetFolderLocation(0, shellcon.CSIDL_DESKTOP, 0, 0)
        pidl, display_name, image_list = shell.SHBrowseForFolder(
            win32gui.GetDesktopWindow(),
            start_pidl,  # type: ignore
            title,
            0,
            None,
            None,
        )

        if pidl:
            path: str = shell.SHGetPathFromIDListW(pidl)
            set_last_cwd(path)
            return path

        return None
