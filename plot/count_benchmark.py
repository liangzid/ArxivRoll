"""
======================================================================
COUNT_BENCHMARK --- 

Obtain some statistic information from the benchmark.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 25 November 2024
======================================================================
"""

# ------------------------ Code --------------------------------------

import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
import statistics

from datasets import load_dataset

from draws import draw_pieChart


def obtain_statistic_info():
    private_benchmark_ls = [
        "robench2024b_all_setcsSCP-s",
        "robench2024b_all_setcsSCP-c",
        "robench2024b_all_setcsSCP-p",
        "robench2024b_all_setq-finSCP-s",
        "robench2024b_all_setq-finSCP-c",
        "robench2024b_all_setq-finSCP-p",
        "robench2024b_all_setmathSCP-s",
        "robench2024b_all_setmathSCP-c",
        "robench2024b_all_setmathSCP-p",
        "robench2024b_all_seteecsSCP-s",
        "robench2024b_all_seteecsSCP-c",
        "robench2024b_all_seteecsSCP-p",
        "robench2024b_all_setphysicsSCP-s",
        "robench2024b_all_setphysicsSCP-c",
        "robench2024b_all_setphysicsSCP-p",
        "robench2024b_all_setstatSCP-s",
        "robench2024b_all_setstatSCP-c",
        "robench2024b_all_setstatSCP-p",
        "robench2024b_all_setq-bioSCP-s",
        "robench2024b_all_setq-bioSCP-c",
        "robench2024b_all_setq-bioSCP-p",
        "robench2024b_all_seteconSCP-s",
        "robench2024b_all_seteconSCP-c",
        "robench2024b_all_seteconSCP-p",
    ]
    overalldict = {}

    for private_bench in private_benchmark_ls:

        overalldict[private_bench] = getStat(
            private_bench, scp_type=private_bench[-1])

    category_ls = [
        "cs",
        "q-fin",
        "math",
        "eecs",
        "physics",
        "stat",
        "q-bio",
        "econ",
    ]
    categorylabel_ls = [
        "CS",
        "Q-Fin",
        "Math",
        "EEcs",
        "Physics",
        "Stat",
        "Q-Bio",
        "Econ",
    ]

    # 1. A fan map to illustrate the sample number distribution.
    cate_sampelnum_dict={}
    for scptype in ["s","c","p"]:
        cate_sample_num_ls=[]
        for cate in category_ls:
            keyname=f"robench2024b_all_set{cate}SCP-{scptype}"
            datadict=overalldict[keyname]
            key1=list(datadict.keys())[0]
            num=datadict[key1]["num"]
            cate_sample_num_ls.append(num)
        cate_sampelnum_dict[scptype]=cate_sample_num_ls
    for ky in cate_sampelnum_dict:
        save_pth=f"./num_pie_{ky}.pdf"
        draw_pieChart(
            cate_sampelnum_dict[ky],
            categorylabel_ls,
            save_pth)
        
        
        


def getStat(dataset_name, scp_type="s"):
    dataset = load_dataset(
        dataset_name,
        "train",
    )
    if scp_type == "s":
        shuffled_text = dataset["shuffled_text"]
        return {
            "shuffled_text": _getLen(shuffled_text),
        }
    elif scp_type == "c":
        text_with_holes = dataset["text_with_holes"]
        text_candidates = dataset["text_candidates"]

        return {
            "text_with_holes": _getLen(text_with_holes),
            "text_candidates": _getLen(text_candidates),
        }
    elif scp_type == "p":
        context = dataset["context"]
        A = dataset["A"]
        B = dataset["B"]
        C = dataset["C"]
        D = dataset["D"]

        return {
            "context": _getLen(context),
            "A": _getLen(A),
            "B": _getLen(B),
            "C": _getLen(C),
            "D": _getLen(D),
        }
    else:
        print("ERROR. Unseen scp type.")
        return None


def _getLen(textls):
    sample_num = len(textls)

    textlengthls = [len(x.split(" ")) for x in textls]

    max_text_len = max(textlengthls)
    min_text_len = min(textlengthls)
    avg_text_len = sum(textlengthls) / len(textlengthls)
    var_text_len = statistics.pvariance(textlengthls)
    median_text_len = statistics.median(textlengthls)

    return {
        "num": sample_num,
        "max": max_text_len,
        "min": min_text_len,
        "avg": avg_text_len,
        "median": median_text_len,
        "var": var_text_len,
    }



## running entry
if __name__ == "__main__":
    # main()
    print("EVERYTHING DONE.")
