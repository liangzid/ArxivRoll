"""
======================================================================
TEST1 --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created:  6 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp

import os
import tarfile


def test_extract():
    save_dir = "./past_one_months_cache/"
    id_ = "1110.4507"
    path_name = f"{save_dir}{id_}.tar.gz"

    directory_name = save_dir+id_
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    with tarfile.open(path_name, "r:gz") as tar:
        tar.extractall(path=directory_name)
    print("Extracting files...DONE.")


def test_fileencoding():
    path = "./past_one_months_cache/1110.4507/main.tex"

    with open(path, 'rb') as f:
        text = f.read()
    print(text[:100])
    t2=text.decode("gbk")
    print(t2)


if __name__ == "__main__":
    # test_extract()
    test_fileencoding()
