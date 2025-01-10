#!/usr/bin/env python3

import crossfiledialog


def test():
    # print(crossfiledialog.open_file(
    #     start_dir="~",
    #     filter={"PDF-Files": "*.pdf", "Python Project": ["*.py", "*.md"]},
    # ))
    # print(crossfiledialog.open_file(
    #     start_dir="~",
    #     filter=[{"PDF-Files": "*.pdf"}, ["*.py", "*.txt"], "*.jpg"],
    # ))
    # print(crossfiledialog.open_file(
    #     start_dir="~",
    #     filter=["*.py", "*.md"],
    # ))
    # print(crossfiledialog.open_file(
    #     start_dir="~",
    #     filter="*.py",
    # ))
    # print(crossfiledialog.open_multiple())
    print(crossfiledialog.save_file())
    # print(crossfiledialog.choose_folder())


if __name__ == "__main__":
    test()
