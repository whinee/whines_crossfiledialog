import os
import sys
from typing import Optional

try:
    from PyQt6.QtWidgets import QApplication, QFileDialog
except ImportError:
    from PyQt5.QtWidgets import (  # type: ignore[assignment, no-redef]
        QApplication,
        QFileDialog,
    )

from crossfiledialog import strings
from crossfiledialog.exceptions import FileDialogException
from crossfiledialog.utils import BaseFileDialog, filter_processor

app = QApplication(sys.argv)


class QtException(FileDialogException):
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


class FileDialog(BaseFileDialog):
    @staticmethod
    def open_file(
        title: str = strings.open_file,
        start_dir: Optional[str] = None,
        filter: Optional[
            str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
        ] = None,
    ) -> Optional[str]:
        r"""
        Open a file selection dialog for selecting a file using QT5/6.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose a file'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`Optional[str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]]`, optional):
            The filter for file types to display. For an example, head to documentation the
            of `crossfiledialog.utils.filter_processor`.

        Returns:
        `str`: The selected file's path.

        Example:
        result = open_file(title="Select a file", start_dir="/path/to/starting/directory", filter="*.txt")

        """

        kwargs = {}

        preferred_cwd = get_preferred_cwd()
        if not start_dir and preferred_cwd:
            kwargs["directory"] = preferred_cwd
        else:
            kwargs["directory"] = start_dir

        if filter:
            processed_filter = kwargs["filter"] = filter_processor(
                filter,
                (" ", "{} ({})"),
                ";;",
            )
            kwargs["initialFilter"] = processed_filter[0]

        file_path, _ = QFileDialog.getOpenFileName(
            None,
            caption=title,
            **kwargs,
        )
        return file_path if file_path != "" else None

    @staticmethod
    def open_multiple(
        title: str = strings.open_multiple,
        start_dir: Optional[str] = None,
        filter: Optional[
            str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
        ] = None,
    ) -> list[str]:
        """
        Open a file selection dialog for selecting multiple files using QT5/6.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose one or more files'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`Optional[str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]]`, optional):
            The filter for file types to display. For an example, head to the documentation
            of `crossfiledialog.utils.filter_processor`.

        Returns:
        `list[str]`: A list of selected file paths.

        Example:
        result = open_multiple(title="Select multiple files",
        start_dir="/path/to/starting/directory", filter="*.txt")

        """

        kwargs = {}

        preferred_cwd = get_preferred_cwd()
        if not start_dir and preferred_cwd:
            kwargs["directory"] = preferred_cwd
        else:
            kwargs["directory"] = start_dir

        if filter:
            processed_filter = kwargs["filter"] = filter_processor(
                filter,
                (" ", "{} ({})"),
                ";;",
            )
            kwargs["initialFilter"] = processed_filter[0]

        file_paths: list[str]
        file_paths, _ = QFileDialog.getOpenFileNames(
            None,
            caption=title,
            **kwargs,
        )
        return file_paths

    @staticmethod
    def save_file(title=strings.save_file, start_dir=None) -> Optional[str]:
        """
        Open a save file dialog using QT5/6.

        Args:
            title (str, optional): The title of the save file dialog.
                Default is 'Enter the name of the file to save to'
            start_dir (str, optional): The starting directory for the dialog.

        Returns:
            `Optional[str]`: The selected file's path for saving.

        Example:
        result = save_file(title="Save file", start_dir="/path/to/starting/directory")

        """

        kwargs = {}

        preferred_cwd = get_preferred_cwd()
        if not start_dir and preferred_cwd:
            kwargs["directory"] = preferred_cwd
        else:
            kwargs["directory"] = start_dir

        file_path, _ = QFileDialog.getSaveFileName(
            None,
            caption=title,
            # **kwargs,
        )
        return file_path if file_path != "" else None

    @staticmethod
    def choose_folder(
        title: str = strings.choose_folder,
        start_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Open a folder selection dialog using QT5/6.

        Args:
        - title (`str`, optional): The title of the folder selection dialog.
            Default is 'Choose a folder'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `Optional[str]`: The selected folder's path.

        Example:
        result = choose_folder(title="Select folder", start_dir="/path/to/starting/directory")

        """

        kwargs = {}

        preferred_cwd = get_preferred_cwd()
        if not start_dir and preferred_cwd:
            kwargs["directory"] = preferred_cwd
        else:
            kwargs["directory"] = start_dir

        op = QFileDialog.getExistingDirectory(
            None,
            caption=title,
            # **kwargs,
        )

        return op if op != "" else None
