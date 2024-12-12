"""
======================================================================
TMP --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 12 December 2024
======================================================================
"""

# ------------------------ Code --------------------------------------

## normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
from collections import OrderedDict


def main():
    with open("./Results--Radar.json", "r", encoding="utf8") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    modells = list(data.keys())

    new_private_avg_dict = {}
    new_rs1_avg_dict={}
    for model in modells:
        private_robench_ls = [v for _, v in data[model]["RobenchAveragedScore"].items()]
        new_private_avg_dict[model] = sum(private_robench_ls) / len(private_robench_ls)
        rs_ls = [v for _, v in data[model]["RS1"].items()]
        new_rs1_avg_dict[model] = sum(rs_ls) / len(rs_ls)
    print("----------------------------------------------------------")
    ppp(new_private_avg_dict)
    print("----------------------------------------------------------")
    print("----------------------------------------------------------")
    ppp(new_rs1_avg_dict)



## running entry
if __name__ == "__main__":
    main()
    print("EVERYTHING DONE.")
