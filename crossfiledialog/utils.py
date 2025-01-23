from typing import Literal, Optional, overload

from crossfiledialog import strings

Filter = Optional[
    str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
]


class BaseFileDialog:
    @staticmethod
    def open_file(
        title: str = strings.open_file,
        start_dir: Optional[str] = None,
        filter: Optional[Filter] = None,
    ) -> Optional[str]:
        """
        Open a file selection dialog for selecting a file.

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

        raise NotImplementedError

    @staticmethod
    def open_multiple(
        title: str = strings.open_multiple,
        start_dir: Optional[str] = None,
        filter: Optional[
            str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]
        ] = None,
    ) -> Optional[list[str]]:
        """
        Open a file selection dialog for selecting multiple files.

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
        raise NotImplementedError

    @staticmethod
    def save_file(title=strings.save_file, start_dir=None) -> Optional[str]:
        """
        Open a save file dialog.

        Args:
        - title (`str`, optional): The title of the save file dialog.
            Default is 'Enter the name of the file to save to'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected file's path for saving.

        Example:
        result = save_file(title="Save file", start_dir="/path/to/starting/directory")

        """
        raise NotImplementedError

    @staticmethod
    def choose_folder(title=strings.choose_folder, start_dir=None) -> Optional[str]:
        """
        Open a folder selection dialog.

        Args:
        - title (`str`, optional): The title of the folder selection dialog.
            Default is 'Choose a folder'
        - start_dir (`str`, optional): The starting directory for the dialog.

        Returns:
        `str`: The selected folder's path.

        Example:
            result = choose_folder(title="Select folder", start_dir="/path/to/starting/directory")

        """
        raise NotImplementedError


@overload
def filter_item_preprocessor(
    item: str | list[str],
    item_seperator: str,
) -> tuple[str]: ...


@overload
def filter_item_preprocessor(
    item: str | list[str],
    item_seperator: Literal[None] = None,
) -> tuple[list[str]]: ...


@overload
def filter_item_preprocessor(
    item: dict[str, str] | dict[str, str | list[str]],
    item_seperator: str,
) -> tuple[str, str]: ...


@overload
def filter_item_preprocessor(
    item: dict[str, str] | dict[str, str | list[str]],
    item_seperator: Literal[None] = None,
) -> tuple[str, list[str]]: ...


def filter_item_preprocessor(  # noqa: C901
    item: str | list[str] | dict[str, str] | dict[str, str | list[str]],
    item_seperator: Optional[str] = None,
) -> tuple[str] | tuple[list[str]] | tuple[str, str | list[str]]:
    """
    Processes filter objects that are not strings and turns them into a tuple of a
    string or two strings which correspond to an unnamed filter and named filter,
    which can then be processed by `filter_processor`.

    Args:
    - item (`str | list[str] | dict[str, str] | dict[str, str | list[str]]`):
        item filter object
    - item_seperator (`str`): The string that seperates items in a singular filter

    Raises:
    - `ValueError`: Raises an error if the filter item is invalid.
        This is raised when a dictionary is inside a dictionary, which should not be
        possible.
    - `ValueError`: Raises an error if the filter item is invalid.

    Returns:
    `tuple[str] | tuple[list[str]] | tuple[str, str | list[str]]`:
        - `tuple[str]`: A tuple of a string that corresponds to an unnamed filter.
            Returned when `item_seperator` is not `None`.
        - `tuple[list[str]]`: A tuple of a list of strings that corresponds to an
            unnamed filter. Returned when `item_seperator` is `None`.
        - `tuple[str, str]`: A tuple of two strings that corresponds to a named filter.
            Returned when `item_seperator` is not `None`.
        - `tuple[str, list[str]]`: A tuple of a string and a list of strings that
            corresponds to a named filter. Returned when `item_seperator` is `None`.

    """

    if isinstance(item, str):
        if item_seperator is None:
            return ([item],)
        return (item,)

    if isinstance(item, list) and all(isinstance(i, str) for i in item):
        if item_seperator is None:
            return (item,)
        return (item_seperator.join(item),)

    if isinstance(item, dict):
        key = next(iter(item.keys()))
        value = next(iter(item.values()))
        if isinstance(value, dict):
            raise ValueError(
                "Invalid filter item. Dictionary should not be placed inside a dictionary.",
            )

        return (
            key,
            filter_item_preprocessor(value, item_seperator)[0],
        )

    raise ValueError("Invalid filter item")


@overload
def filter_processor(
    filter: str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]],
    item_seperator_key_value_format: tuple[str, str],
    filter_seperator: str,
) -> str: ...


@overload
def filter_processor(
    filter: str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]],
    item_seperator_key_value_format: tuple[str, str],
    filter_seperator: Literal[None] = None,
) -> list[str]: ...


@overload
def filter_processor(
    filter: str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]],
    item_seperator_key_value_format: None = None,
    filter_seperator: Literal[None] = None,
) -> list[tuple[list[str]]] | list[tuple[list[str]] | tuple[str, list[str]]]: ...


def filter_processor(  # noqa: C901
    filter: str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]],
    item_seperator_key_value_format: Optional[tuple[str, str]] = None,
    filter_seperator: Optional[str] = None,
) -> (
    str
    | list[str]
    | list[tuple[list[str]]]
    | list[tuple[list[str]] | tuple[str, list[str]]]
):
    r"""
    Processes filter objects and turns them into a singular string that programs can
    understand.

    Args:
    - filter (`str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]`):
        It can be either:
        - a single wildcard (e.g.: `"*.py"`, all files are displayed ending .py)
        - a list of wildcards (e.g.: `["*.py", "*.md"]`, all files are displayed ending
        either .py or .md)
        - a list containing wildcards, lists of wildcards, and/or dictionaries of named
            filters (e.g.: `[{"PDF-Files": "*.pdf"}, ["*.py", "*.md"], "*.txt"]`, user
            can switch between PDF files, [.py, .md], and .txt). Note that when one uses
            a dictionary inside, the first key and value is used as the entry and the
            rest of the items in said dictionary are ignored.
        - a dictionary mapping descriptions to wildcards
            (e.g.: `{"PDF-Files": "*.pdf", "Python Project": ["*.py", "*.md"]}`)
    - item_seperator (`str`): The string that seperates items in a singular filter
    - key_value_format (`str`): The format to which the named filters should be formatted
    - filter_seperator (`Optional[str]`): The string that seperates filters.
        When no value is provided, the filter is returned as a list of strings.

    Raises:
    - `ValueError`: Raises an error if the filter type is invalid

    Returns:
    `str | list[str] | list[tuple[list[str]]] | list[tuple[list[str]] | tuple[str, list[str]]]`:
        Processed filter. Below is an explanation of each of return types:
        - `str`: Concatenated filters. Returned when `item_seperator_key_value_format` and
            `filter_seperator` is not `None`.
        - `list[str]`: Filters not joined by a string. Returned when
            `item_seperator_key_value_format` is not `None` and `filter_seperator` is
            `None`.
        - `list[tuple[list[str]]] | list[tuple[list[str]] | tuple[str, list[str]]]`:
            Returned when `item_seperator_key_value_format` is `None`.

    """

    filter_item_preprocessor_args = []

    if item_seperator_key_value_format is None:
        unnamed_filter_func = named_filter_func = lambda x: x
    else:
        item_seperator, key_value_format = item_seperator_key_value_format
        filter_item_preprocessor_args.append(item_seperator)

        def unnamed_filter_func(x):
            return x[0]

        def named_filter_func(x):
            key, value = x
            return key_value_format.format(key, value)

    if isinstance(filter, str):
        if filter_seperator is not None:
            return filter

        return [([filter],)]

    filter1: list[tuple[str] | tuple[str, str]] = []
    if isinstance(filter, list):
        for item in filter:
            filter1.append(
                filter_item_preprocessor(item, *filter_item_preprocessor_args),
            )
    elif isinstance(filter, dict):
        for key, value in filter.items():
            filter1.append(
                (
                    key,
                    filter_item_preprocessor(value, *filter_item_preprocessor_args)[0],
                ),
            )
    else:
        raise ValueError("Invalid filter")

    output_filters = []
    for i in filter1:
        if len(i) == 1:
            processed_item = unnamed_filter_func(i)
        else:
            processed_item = named_filter_func(i)
        output_filters.append(processed_item)

    if filter_seperator is not None:
        return filter_seperator.join(output_filters)

    return output_filters
