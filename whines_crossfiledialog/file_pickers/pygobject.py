import os
from typing import Optional

import gi

from whines_crossfiledialog import strings
from whines_crossfiledialog.exceptions import FileDialogException
from whines_crossfiledialog.utils import BaseFileDialog, filter_processor

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # type: ignore # noqa: E402


class PygobjectException(FileDialogException):
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
    def open_file(  # noqa: C901
        title: str = strings.open_file,
        start_dir: Optional[str] = None,
        filter: Optional[
            str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
        ] = None,
    ) -> Optional[str]:
        """
        Open a file selection dialog for selecting a file using Pygobject.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose a file'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]`, optional):
            The filter for file types to display. For an example, head to documentation the
            of `whines_crossfiledialog.utils.filter_processor`.

        Returns:
        `Optional[str]`: The selected file's path.

        Example:
        result = open_file(title="Select a file", start_dir="/path/to/starting/directory", filter="*.txt")

        """

        dialog = Gtk.FileChooserDialog(
            title,
            None,
            Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            "Select",
            Gtk.ResponseType.OK,
        )

        preferred_cwd = get_preferred_cwd()
        print(preferred_cwd)
        if start_dir:
            dialog.set_current_folder(start_dir)
        elif preferred_cwd:
            dialog.set_current_folder(preferred_cwd)

        if filter:
            print(filter_processor(filter))
            for i in filter_processor(filter):
                gtk_file_filter = Gtk.FileFilter()

                if len(i) == 1:
                    filter_value = i[0]
                    filter_name = " ".join(filter_value)
                else:
                    filter_name, filter_value = i

                gtk_file_filter.set_name(filter_name)

                for j in filter_value:
                    gtk_file_filter.add_pattern(j)
                dialog.add_filter(gtk_file_filter)

        response = dialog.run()
        result = None
        if response == Gtk.ResponseType.OK:
            result = dialog.get_filename()
            set_last_cwd(result)

        dialog.destroy()
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
        Open a file selection dialog for selecting multiple files using Pygobject.

        Args:
        - title (`str`, optional): The title of the file selection dialog.
            Default is 'Choose one or more files'
        - start_dir (`str`, optional): The starting directory for the dialog.
        - filter (`str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]`, optional):
            The filter for file types to display. For an example, head to documentation the
            of `whines_crossfiledialog.utils.filter_processor`.

        Returns:
        `list[str]`: A list of selected file paths.

        Example:
        result = open_multiple(title="Select multiple files",
        start_dir="/path/to/starting/directory", filter="*.txt")

        """
        dialog = Gtk.FileChooserDialog(
            title,
            None,
            Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            "Select",
            Gtk.ResponseType.OK,
        )
        dialog.set_select_multiple(True)

        preferred_cwd = get_preferred_cwd()
        print(preferred_cwd)
        if start_dir:
            dialog.set_current_folder(start_dir)
        elif preferred_cwd:
            dialog.set_current_folder(preferred_cwd)

        if filter:
            print(filter_processor(filter))
            for i in filter_processor(filter):
                gtk_file_filter = Gtk.FileFilter()

                if len(i) == 1:
                    filter_value = i[0]
                    filter_name = " ".join(filter_value)
                else:
                    filter_name, filter_value = i

                gtk_file_filter.set_name(filter_name)

                for j in filter_value:
                    gtk_file_filter.add_pattern(j)
                dialog.add_filter(gtk_file_filter)

        response = dialog.run()
        result = []
        if response == Gtk.ResponseType.OK:
            result = dialog.get_filenames()
            set_last_cwd(result[0])

        dialog.destroy()
        return result

    @staticmethod
    def save_file(
        title: str = strings.save_file,
        start_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Open a save file dialog using Pygobject.

        Args:
        - title (`str`, optional): The title of the save file dialog.
            Default is 'Enter the name of the file to save to'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected file's path for saving.

        Example:
        result = save_file(title="Save file", start_dir="/path/to/starting/directory")

        """

        dialog = Gtk.FileChooserDialog(
            title,
            None,
            Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            "Select",
            Gtk.ResponseType.OK,
        )
        dialog.set_select_multiple(True)

        preferred_cwd = get_preferred_cwd()
        print(preferred_cwd)
        if start_dir:
            dialog.set_current_folder(start_dir)
        elif preferred_cwd:
            dialog.set_current_folder(preferred_cwd)

        response = dialog.run()
        result = None
        if response == Gtk.ResponseType.OK:
            result = dialog.get_filename()
            set_last_cwd(result)

        dialog.destroy()
        return result

    @staticmethod
    def choose_folder(
        title: str = strings.choose_folder,
        start_dir: Optional[str] = None,
    ) -> Optional[str]:
        """
        Open a folder selection dialog using Pygobject.

        Args:
        - title (`str`, optional): The title of the folder selection dialog.
            Default is 'Choose a folder'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected folder's path.

        Example:
        result = choose_folder(title="Select folder", start_dir="/path/to/starting/directory")

        """
        dialog = Gtk.FileChooserDialog(
            title,
            None,
            Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            "Select",
            Gtk.ResponseType.OK,
        )
        dialog.set_select_multiple(True)

        preferred_cwd = get_preferred_cwd()
        if start_dir:
            dialog.set_current_folder(start_dir)
        elif preferred_cwd:
            dialog.set_current_folder(preferred_cwd)

        response = dialog.run()
        result = None
        if response == Gtk.ResponseType.OK:
            result = dialog.get_filename()
            set_last_cwd(result)

        dialog.destroy()
        return result
