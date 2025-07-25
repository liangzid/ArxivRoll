"""
======================================================================
TMP_UPDATE_ARXIVBENCH2024B --- 

======================================================================
"""


# ------------------------ Code --------------------------------------

import os
from constructor import push2HF
import time


def temp_update_benchmarks():
    dir_prefix="./robench2024b_all/"

    for suffix in os.listdir(dir_prefix):
        pth=dir_prefix+suffix

        newdatasetname = pth.replace("./", "")\
            .replace(".jsonl", "")\
            .replace("/", "_").replace(".json", "")\
            .replace("recent6months_html_", "")\
            .replace("robench","arxivroll")

        print(f"read_path: {pth}")
        print(f"new dataset name: {newdatasetname}")

        push2HF(pth, name=newdatasetname)

        print("Sleep five seconds...")
        time.sleep(5)
        
    
if __name__=="__main__":
    temp_update_benchmarks()

