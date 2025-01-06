def filter_item_preprocessor(
    item: str | list[str] | dict[str, str] | dict[str, str | list[str]],
    item_seperator: str,
) -> tuple[str] | tuple[str, str]:
    """
    Processes filter objects that are not strings and turns them into a tuple of a
    string or two strings which correspond to an unnamed filter and named filter,
    which can then be processed by `filter_processor`.

    Args:
    - item (`str | list[str] | dict[str, str] | dict[str, str  |  list[str]]`): filter object
    - item_seperator (`str`): The string that seperates items in a singular filter

    Raises:
    - `ValueError`: Raises an error if the filter item is invalid. This is raised when a dictionary is inside a dictionary, which should not be possible.
    - `ValueError`: Raises an error if the filter item is invalid.

    Returns:
    `tuple[str] | tuple[str, str]`: A tuple of a string or two strings that corresponds to an unnamed filter and named filter, which can then be processed by `filter_processor`.

    """

    print(type(item),)

    if isinstance(item, str):
        return (item,)

    if isinstance(item, list) and all(isinstance(i, str) for i in item):
        return (item_seperator.join(item),)

    if isinstance(item, dict):
        key = next(iter(item.keys()))
        value = next(iter(item.values()))
        if isinstance(value, dict):
            raise ValueError("Invalid filter item. Dictionary should not be placed inside a dictionary.")
        return (
            key,
            filter_item_preprocessor(value, item_seperator)[0],
        )

    raise ValueError("Invalid filter item")


def filter_processor(  # noqa: C901
    filter: str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]],
    item_seperator: str,
    key_value_format: str,
    filter_seperator: str,
) -> str:
    r"""
    Processes filter objects and turns them into a singular string that programs can
    understand.

    Args:
    - filter (`str | list[str | list[str] | dict[str, str]] | dict[str, str | list[str]]`):
        It can be either:
            - a single wildcard (e.g.: `"*.py"`, all files are displayed ending .py)
            - a list of wildcards (e.g.: `["*.py", "*.md"]`, all files are displayed
                ending either .py or .md)
            - a list containing wildcards, lists of wildcards, and/or dictionaries of
                named filters (e.g.: `[{"PDF-Files": "*.pdf"}, ["*.py", "*.md"], "*.txt"]`,
                user can switch between PDF files, [.py, .md], and .txt). Note that when
                one uses a dictionary inside, the first key and value is used as the
                entry and the rest of the items in said dictionary are ignored.
            - a dictionary mapping descriptions to wildcards
                (e.g.: `{"PDF-Files": "*.pdf", "Python Project": ["\*.py", "*.md"]}`)
    - item_seperator (`str`): The string that seperates items in a singular filter
    - key_value_format (`str`): The format to which the named filters should be formatted
    - filter_seperator (`str`): The string that seperates filters

    Raises:
    - `ValueError`: Raises an error if the filter type is invalid

    Returns:
    `str`: The processed filter

    """

    if isinstance(filter, str):
        return filter

    filter1: list[tuple[str] | tuple[str, str]] = []
    if isinstance(filter, list):
        for item in filter:
            filter1.append(filter_item_preprocessor(item, item_seperator))
    elif isinstance(filter, dict):
        for key, value in filter.items():
            print(key, value)
            filter1.append((key, filter_item_preprocessor(value, item_seperator)[0]))
    else:
        raise ValueError("Invalid filter")

    output_filters = []
    for i in filter1:
        if len(i) == 1:
            output_filters.append(i[0])
        else:
            key, value = i
            output_filters.append(key_value_format.format(key, value))

    return filter_seperator.join(output_filters)
