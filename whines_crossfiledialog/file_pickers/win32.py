"""
Part of this codebase contains code from toga (https://github.com/beeware/toga).
Hereunder is the license for toga:

--- Start of Toga License ---

Modified BSD License

Copyright (c) 2014 Russell Keith-Magee.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Toga nor the names of its contributors may
       be used to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

--- End of Toga License ---

The rest of this codebase is written by Maikel Wever
(https://github.com/maikelwever) in the project crossfiledialog
(https://github.com/maikelwever/crossfiledialog), licensed under the GNU Lesser
General Public License. For more details, see the license text at
docs/LICENSE.md.

Snippets of code from toga (which might be modified by whinee
[https://github.com/whinee]) are enclosed in the following comment, as follows:

# --- Start of Toga code snippet ---

print("example Toga code snippet")

# --- End of Toga code snippet ---

"""

import os
from typing import Optional

from whines_crossfiledialog import strings
from whines_crossfiledialog.exceptions import (
    FileDialogException,
    NoImplementationFoundException,
)

try:
    # --- Start of Toga code snippet ---
    from _ctypes import COMError
    from ctypes import (
        HRESULT,
        POINTER,
        Structure,
        byref,
        c_int,
        c_uint,
        c_ulong,
        c_void_p,
        c_wchar_p,
        windll,
    )
    from ctypes.wintypes import DWORD, HWND, LPCWSTR, LPWSTR

    import comtypes
    import comtypes.client
    # --- End of Toga code snippet ---
    import pywintypes  # type: ignore
    import win32con  # type: ignore
    import win32gui  # type: ignore
    # --- Start of Toga code snippet ---
    from comtypes import COMMETHOD, GUID
    from comtypes.hresult import S_OK
    # --- End of Toga code snippet ---
except ImportError:
    raise NoImplementationFoundException(
        "Running 'filedialog' on Windows requires the 'pywin32' package.",
    ) from None

from collections.abc import Callable
from pathlib import Path
from typing import ClassVar, Union

from whines_crossfiledialog.utils import BaseFileDialog, filter_processor


# --- Start of Toga code snippet ---
class COMDLG_FILTERSPEC(Structure):  # noqa: N801
    _fields_: ClassVar = [  # type: ignore
        ("pszName", LPCWSTR),
        ("pszSpec", LPCWSTR),
    ]


IID_IShellItem = GUID("{43826D1E-E718-42EE-BC55-A1E261C37BFE}")
IID_IShellItemArray = GUID("{B63EA76D-1F85-456F-A19C-48159EFA858B}")
IID_IModalWindow = GUID("{B4DB1657-70D7-485E-8E3E-6FCB5A5C1802}")
IID_IFileDialog = GUID("{42F85136-DB7E-439C-85F1-E4075D135FC8}")
IID_IFileOpenDialog = GUID("{D57C7288-D4AD-4768-BE02-9D969532D960}")
CLSID_FileOpenDialog = GUID("{DC1C5A9C-E88A-4dde-A5A1-60F82A20AEF7}")


class IShellItem(comtypes.IUnknown):  # type: ignore[misc]
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItem
    _methods_: ClassVar = [  # type: ignore
        COMMETHOD(
            [],
            HRESULT,
            "BindToHandler",
            (["in"], POINTER(comtypes.IUnknown), "pbc"),
            (["in"], POINTER(GUID), "bhid"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetParent",
            (["out"], POINTER(POINTER(comtypes.IUnknown)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetDisplayName",
            (["in"], c_ulong, "sigdnName"),
            (["out"], POINTER(LPWSTR), "ppszName"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAttributes",
            (["in"], c_ulong, "sfgaoMask"),
            (["out"], POINTER(c_ulong), "psfgaoAttribs"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "Compare",
            (["in"], POINTER(comtypes.IUnknown), "psi"),
            (["in"], c_ulong, "hint"),
            (["out"], POINTER(c_int), "piOrder"),
        ),
    ]
    QueryInterface: Callable[[GUID, comtypes.IUnknown], int]  # type: ignore
    AddRef: Callable[[], int]  # type: ignore
    Release: Callable[[], int]  # type: ignore
    BindToHandler: Callable[[comtypes.IUnknown, GUID, GUID, c_void_p], int]
    GetParent: Callable[[], comtypes.IUnknown]
    GetDisplayName: Callable[[Union[c_ulong, int]], str]
    GetAttributes: Callable[[Union[c_ulong, int]], int]
    Compare: Callable[[comtypes.IUnknown, c_ulong, c_int], int]


class IShellItemArray(comtypes.IUnknown):  # type: ignore[misc]
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IShellItemArray
    _methods_: ClassVar = [  # type: ignore
        COMMETHOD(
            [],
            HRESULT,
            "BindToHandler",
            (["in"], POINTER(comtypes.IUnknown), "pbc"),
            (["in"], POINTER(GUID), "bhid"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyStore",
            (["in"], c_ulong, "flags"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetPropertyDescriptionList",
            (["in"], POINTER(GUID), "keyType"),
            (["in"], POINTER(GUID), "riid"),
            (["out"], POINTER(c_void_p), "ppv"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetAttributes",
            (["in"], c_ulong, "attribFlags"),
            (["in"], c_ulong, "sfgaoMask"),
            (["out"], POINTER(c_ulong), "psfgaoAttribs"),
        ),
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(c_uint), "pdwNumItems")),
        COMMETHOD(
            [],
            HRESULT,
            "GetItemAt",
            (["in"], c_uint, "dwIndex"),
            (["out"], POINTER(POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "EnumItems",
            (["out"], POINTER(POINTER(comtypes.IUnknown)), "ppenumShellItems"),
        ),
    ]
    QueryInterface: Callable[[GUID, comtypes.IUnknown], int]  # type: ignore
    AddRef: Callable[[], int]  # type: ignore
    Release: Callable[[], int]  # type: ignore
    BindToHandler: Callable[[comtypes.IUnknown, GUID, GUID], int]
    GetPropertyStore: Callable[[int, GUID], c_void_p]
    GetPropertyDescriptionList: Callable[[GUID, GUID], c_void_p]
    GetAttributes: Callable[[int, int], int]
    GetCount: Callable[[], int]
    GetItemAt: Callable[[Union[int, int]], IShellItem]
    EnumItems: Callable[[], comtypes.IUnknown]


class IFileOpenDialog(comtypes.IUnknown):  # type: ignore[misc]
    _case_insensitive_: bool = True
    _iid_: GUID = IID_IFileOpenDialog
    _methods_: ClassVar = [  # type: ignore
        COMMETHOD([], HRESULT, "Show", (["in"], HWND, "hwndParent")),
        COMMETHOD(
            [],
            HRESULT,
            "SetFileTypes",
            (["in"], c_uint, "cFileTypes"),
            (["in"], POINTER(c_void_p), "rgFilterSpec"),
        ),
        COMMETHOD([], HRESULT, "SetFileTypeIndex", (["in"], c_uint, "iFileType")),
        COMMETHOD(
            [],
            HRESULT,
            "GetFileTypeIndex",
            (["out"], POINTER(c_uint), "piFileType"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "Advise",
            (["in"], POINTER(comtypes.IUnknown), "pfde"),
            (["out"], POINTER(DWORD), "pdwCookie"),
        ),
        COMMETHOD([], HRESULT, "Unadvise", (["in"], DWORD, "dwCookie")),
        COMMETHOD([], HRESULT, "SetOptions", (["in"], c_uint, "fos")),
        COMMETHOD([], HRESULT, "GetOptions", (["out"], POINTER(DWORD), "pfos")),
        COMMETHOD(
            [],
            HRESULT,
            "SetDefaultFolder",
            (["in"], POINTER(IShellItem), "psi"),
        ),
        COMMETHOD([], HRESULT, "SetFolder", (["in"], POINTER(IShellItem), "psi")),
        COMMETHOD(
            [],
            HRESULT,
            "GetFolder",
            (["out"], POINTER(POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetCurrentSelection",
            (["out"], POINTER(POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD([], HRESULT, "SetFileName", (["in"], LPCWSTR, "pszName")),
        COMMETHOD([], HRESULT, "GetFileName", (["out"], POINTER(LPWSTR), "pszName")),
        COMMETHOD([], HRESULT, "SetTitle", (["in"], LPCWSTR, "pszTitle")),
        COMMETHOD([], HRESULT, "SetOkButtonLabel", (["in"], LPCWSTR, "pszText")),
        COMMETHOD([], HRESULT, "SetFileNameLabel", (["in"], LPCWSTR, "pszLabel")),
        COMMETHOD(
            [],
            HRESULT,
            "GetResult",
            (["out"], POINTER(POINTER(IShellItem)), "ppsi"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "AddPlace",
            (["in"], POINTER(IShellItem), "psi"),
            (["in"], c_int, "fdap"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetDefaultExtension",
            (["in"], LPCWSTR, "pszDefaultExtension"),
        ),
        COMMETHOD([], HRESULT, "Close", (["in"], HRESULT, "hr")),
        COMMETHOD([], HRESULT, "SetClientGuid", (["in"], POINTER(GUID), "guid")),
        COMMETHOD([], HRESULT, "ClearClientData"),
        COMMETHOD(
            [],
            HRESULT,
            "SetFilter",
            (["in"], POINTER(comtypes.IUnknown), "pFilter"),
        ),  # IShellItemFilter
        COMMETHOD(
            [],
            HRESULT,
            "GetResults",
            (["out"], POINTER(POINTER(IShellItemArray)), "ppenum"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "GetSelectedItems",
            (["out"], POINTER(POINTER(IShellItemArray)), "ppsai"),
        ),
    ]
    Show: Callable[[Union[int, HWND]], int]
    SetFileTypes: Callable[[Union[c_uint, int], c_void_p], int]
    SetFileTypeIndex: Callable[[c_uint], int]
    GetFileTypeIndex: Callable[[], int]
    Advise: Callable[[Union[comtypes.IUnknown, comtypes.COMObject]], int]
    Unadvise: Callable[[int], int]
    SetOptions: Callable[[Union[int, int]], int]
    GetOptions: Callable[[], int]
    SetDefaultFolder: Callable[[IShellItem], int]
    SetFolder: Callable[[IShellItem], int]
    GetFolder: Callable[[], IShellItem]
    GetCurrentSelection: Callable[[], IShellItem]
    SetFileName: Callable[[str], int]
    GetFileName: Callable[[], str]
    SetTitle: Callable[[str], int]
    SetOkButtonLabel: Callable[[str], int]
    SetFileNameLabel: Callable[[str], int]
    GetResult: Callable[[], IShellItem]
    AddPlace: Callable[[IShellItem, c_int], int]
    SetDefaultExtension: Callable[[str], int]
    Close: Callable[[HRESULT], int]
    SetClientGuid: Callable[[GUID], int]
    ClearClientData: Callable[[], int]
    SetFilter: Callable[[comtypes.IUnknown], int]
    GetResults: Callable[[], IShellItemArray]
    GetSelectedItems: Callable[[], IShellItemArray]
# --- End of Toga code snippet ---

class Win32Exception(FileDialogException):
    pass


last_cwd: Optional[str] = None
DESKTOP_PATH = os.path.expanduser("~/Desktop")


def get_preferred_cwd():
    possible_cwd = os.environ.get("FILEDIALOG_CWD", "")
    if possible_cwd:
        return possible_cwd

    global last_cwd
    if last_cwd:
        return last_cwd

    return DESKTOP_PATH


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
            of `whines_crossfiledialog.utils.filter_processor`.

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
        else:
            win_kwargs["InitialDir"] = DESKTOP_PATH

        if filter:
            filter_items = []
            for i in filter_processor(filter):
                if len(i) == 1:
                    filter_value = i[0]
                    filter_name = "; ".join(filter_value)
                else:
                    filter_name, filter_value = i

                filter_items.append(filter_name + "\0" + ";".join(filter_value) + "\0")

            win_kwargs["Filter"] = "".join(filter_items)

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
            of `whines_crossfiledialog.utils.filter_processor`.

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
        else:
            win_kwargs["InitialDir"] = DESKTOP_PATH

        if filter:
            filter_items = []
            for i in filter_processor(filter):
                if len(i) == 1:
                    filter_value = i[0]
                    filter_name = "; ".join(filter_value)
                else:
                    filter_name, filter_value = i

                filter_items.append(filter_name + "\0" + ";".join(filter_value) + "\0")

            win_kwargs["Filter"] = "".join(filter_items)

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
        else:
            win_kwargs["InitialDir"] = DESKTOP_PATH

        file_name: Optional[str] = error_handling_wrapper(
            win32gui.GetSaveFileNameW,
            **win_kwargs,
            Flags=win32con.OFN_OVERWRITEPROMPT,
        )

        if file_name:
            set_last_cwd(file_name)
        return file_name

    @staticmethod
    def choose_folder(  # noqa: C901
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
            pass
        elif last_cwd:
            start_dir = last_cwd
        else:
            start_dir = DESKTOP_PATH

        # --- Start of Toga code snippet ---
        native: IFileOpenDialog = comtypes.client.CreateObject(
            CLSID_FileOpenDialog,
            interface=IFileOpenDialog,
        )

        native.SetTitle(title)

        if start_dir is not None:
            folder_path: Path = Path(start_dir).resolve()
            if folder_path.is_dir():  # sourcery skip: extract-method
                sh_create_item_from_parsing_name = (
                    windll.shell32.SHCreateItemFromParsingName
                )
                sh_create_item_from_parsing_name.argtypes = [
                    c_wchar_p,  # LPCWSTR (wide string, null-terminated)
                    POINTER(
                        comtypes.IUnknown,
                    ),  # IBindCtx* (can be NULL, hence POINTER(IUnknown))
                    POINTER(
                        GUID,
                    ),  # REFIID (pointer to the interface ID, typically GUID)
                    POINTER(
                        POINTER(IShellItem),
                    ),  # void** (output pointer to the requested interface)
                ]
                sh_create_item_from_parsing_name.restype = HRESULT
                shell_item = POINTER(IShellItem)()
                hr = sh_create_item_from_parsing_name(
                    str(folder_path),
                    None,
                    IShellItem._iid_,
                    byref(shell_item),
                )
                if hr == S_OK:
                    native.SetFolder(shell_item)  # type: ignore[arg-type]

        native.SetOptions(0x00000020)  # FOS_PICKFOLDERS = 0x00000020

        hwnd = HWND(0)
        try:
            new_hr: int = native.Show(hwnd)
        except COMError as e:
            if e.hresult == -2147023673:  # User canceled the dialog
                return None  # Return None instead of raising an error
            raise e  # Re-raise unexpected errors
        if new_hr == S_OK:
            new_shell_item: IShellItem = native.GetResult()
            display_name: str = new_shell_item.GetDisplayName(
                0x80058000,
            )  # SIGDN_FILESYSPATH
            return display_name
        # --- End of Toga code snippet ---
        return None
