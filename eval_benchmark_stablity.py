"""
======================================================================
EVAL_BENCHMARK_STABLITY ---

Evaluate the stablity of the benchmark generation methods.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 26 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import os
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
from collections import OrderedDict

from constructor import push2HF
from constructor import constructBenchmarksSCP


def multitimeGenerateBenches(
        scp_type="s",
        times=10,):
    save_dir = "./multiTimeEvalBackup/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for time in range(times):
        dataset_from_path = "./robench2024b_all/recent6months_html_setcs.json"
        with open(dataset_from_path,
                  'r', encoding='utf8') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
        papers = data["text"]
        print(f"All paper Number: {len(papers)}")

        save_path = f"{save_dir}Experiments_Time{time}_SCP-{scp_type}.jsonl"
        constructBenchmarksSCP(
            papers,
            hf_style_save_path=save_path,
            scp_type="s",
            n_gram=2,
            minimal_char=250,
        )
        newdatasetname = f"robench-eval-Time{time}-{scp_type}"
        push2HF(save_path, name=newdatasetname)


def main():
    multitimeGenerateBenches("s", 32)
    multitimeGenerateBenches("c", 32)
    multitimeGenerateBenches("p", 32)


if __name__ == "__main__":
    main()
