#!/usr/bin/env python3

from whines_crossfiledialog import file_dialog

CrossFileDialog = file_dialog(["pygobject"])

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
    # print(CrossFileDialog.open_file(
    #     start_dir="~",
    #     filter="*.py",
    # ))
    # print(CrossFileDialog.open_multiple())
    # print(CrossFileDialog.save_file())
    print(CrossFileDialog.choose_folder())


if __name__ == "__main__":
    test()
