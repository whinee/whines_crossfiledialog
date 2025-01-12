#!/usr/bin/env python3

from crossfiledialog import file_dialog

CrossFileDialog = file_dialog(["zenity"])

def test():
    # print(CrossFileDialog.open_file(
    #     start_dir="~",
    #     filter={"PDF-Files": "*.pdf", "Python Project": ["*.py", "*.md"]},
    # ))
    # print(CrossFileDialog.open_file(
    #     start_dir="~",
    #     filter=[{"PDF-Files": "*.pdf"}, ["*.py", "*.txt"], "*.jpg"],
    # ))
    # print(CrossFileDialog.open_file(
    #     start_dir="~",
    #     filter=["*.py", "*.md"],
    # ))
    print(CrossFileDialog.open_file(
        start_dir="~",
        filter="*.py",
    ))
    # print(CrossFileDialog.open_multiple())
    # print(CrossFileDialog.save_file())
    # print(CrossFileDialog.choose_folder())
    # i = CrossFileDialog.open_file()
    # print(i, type(i))


if __name__ == "__main__":
    test()
