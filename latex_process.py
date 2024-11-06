"""
======================================================================
LATEX_PROCESS ---

Candy for a latex project.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created:  5 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------
import os
from typing import List


def combine2ASimpleLatexFile(directory_name):
    """
    ------------------------------------------------------------------
    Input: the directory path of a Latex Project.
    Output: A str of latex contents.
    ------------------------------------------------------------------
    Func: this function will combine all latex resources within a
    latex project, and return the combined content with a str.
    If failed, it will return None.
    ------------------------------------------------------------------
    """
    fnames = os.listdir(directory_name)

    find_flag = 0
    find_name = None
    for x in fnames:
        if x.endswith(".tex"):
            fine_name = x
            find_flag += 1
    # Condition I: return None if no tex file
    if find_flag == 0:
        return None
    # Condition II:  return the content of a single file if there is
    # only one tex file
    if find_flag == 1:
        fpth = directory_name+"/"+fine_name
        with open(fpth, "r", encoding="utf8") as f:
            lines = f.readlines()
        lines = _filterUselessLines(lines)
        return "\n".join(lines)
    # Condition III: combine different tex file into a single file.
    if find_flag > 1:

        # 1. find the main file.
        main_file_name = None
        for fname in fnames:
            if fname == "main.tex" or\
               _findBeginDoc(directory_name+fname) or\
               _findDocClass(directory_name+fname):
                main_file_name = fname
                break
        if main_file_name is None:
            return None
        # 2. compress to a single file.
        fpth = directory_name+"/"+fine_name
        with open(fpth, "r", encoding="utf8") as f:
            lines = f.readlines()
        lines = _filterUselessLines(lines)
        for fname in fnames:
            if fname == main_file_name:
                continue
            head = fname.split(".")[0]
            lines = _insert_replace(lines, head, directory_name+fname)
        return "\n".join(lines)

    return None


def _insert_replace(lines, headname, fpath):
    """
    ------------------------------------------------------------------
    lines: List[str], line list.
    headname: filename of a slave tex file. such as `intro.tex`.
    fpath: filepath we want to embed to the lines.
    ------------------------------------------------------------------
    This function will match the fname in the main file's `lines`,
    once found, we will embed the content with in `fname` into `lines`.
    ------------------------------------------------------------------
    """
    with open(fpath, "r", encoding="utf8") as f:
        lines2 = f.readlines()

    idx = -1
    for i, line in enumerate(lines):
        if headname in line:
            # find it.
            idx = i
    if idx == -1:
        return lines
    else:
        newlines = lines[:idx].copy()
        newlines.extend(lines2)
        if idx != len(lines)-1:
            newlines.extend(lines[idx+1:])
        return newlines
    return lines


def _filterUselessLines(lines: List[str]):
    """
    filter useless lines
    """
    newlines = []
    for line in lines:
        if line.startswith("%"):
            continue
        newlines.append(line)
    return newlines


def _findBeginDoc(fname):
    """return true if it contains \\begin{document}"""
    with open(fname, "r", encoding="utf8") as f:
        content = f.read()
    if "begin{document}" in content or\
       "end{document}" in content:
        return True
    else:
        return False


def _findDocClass(fname):
    """return true if it contains \\documentclass"""
    with open(fname, "r", encoding="utf8") as f:
        content = f.read()

    if "documentclass" in content:
        return True
    else:
        return False


# running entry
if __name__ == "__main__":
    print("EVERYTHING DONE.")
