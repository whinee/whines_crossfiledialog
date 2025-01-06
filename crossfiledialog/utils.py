def filter_item_preprocessor(
    item: str | list[str] | dict[str, str] | dict[str, str | list[str]],
    item_seperator: str,
    no_of_iterations: int = 0,
) -> tuple[str] | tuple[str, str]:

    if (no_of_iterations == 0):
        raise ValueError("Invalid filter item")

    if isinstance(item, str):
        return (item,)

    if isinstance(item, list) and all(isinstance(i, str) for i in item):
        return (item_seperator.join(item),)

    if isinstance(item, dict):
        key = next(iter(item.keys()))
        value = next(iter(item.values()))
        return (
            key,
            filter_item_preprocessor(value, item_seperator, no_of_iterations + 1)[0],
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
            - a list of wildcards (e.g.: `["*.py", "*.md"]`, all files are displayed ending either .py or .md)
            - a list of list optional one or more wildcards (e.g.: `[["*.py", "*.md"], ["*.txt"]]`,
            user can switch between (.py, .md) and (.txt))
            - a list of list or a list of str (e.g.: `[["*.py", "*.md"], "*.txt"]`, user can switch between (.py, .md) and .txt)
            - a dictionary mapping descriptions to wildcards (e.g.: `{"PDF-Files": "*.pdf", "Python Project": ["\*.py", "*.md"]}`)
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
