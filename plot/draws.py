"""
======================================================================
DRAWS --- 

functions to draw plots.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 25 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp

from matplotlib import pyplot as plt

print(plt.style.available)


def drawPieChartSCP(cate_samplenum_dict, labels, save_pth):
    plt.style.use("seaborn-v0_8-white")
    wedge_props = {
        "linewidth": 2,
        "edgecolor": "w",
    }
    textprops = {
        'fontsize': 16,
        # 'fontstyle': 'italic',
        # 'fontweight': 'bold',
    }
    color_ls = [
        "#C2E8F7",
        "#FCE0E1",
        "#F2F4C1",
        "#FFE2BB",
        "#CCE7CF",
        "#DBDFEF",
        "#F3F3F4",
        "#C5BEDF",
    ]
    fig, axs = plt.subplots(1, 3, figsize=(16, 5))
    key_ls = ["s", "c", "p"]
    for i, x in enumerate(key_ls):
        datals = cate_samplenum_dict[x]
        axs[i].pie(datals,
                   # explode=explode,
                   colors=color_ls,
                   labels=labels,
                   autopct='%1.1f%%',
                   textprops=textprops,
                   wedgeprops=wedge_props,
                   )
        axs[i].axis('equal')

    axs[0].set_title("(a) RoBench2024-S", fontsize=18,)
    axs[1].set_title("(b) RoBench2024-C", fontsize=18,)
    axs[2].set_title("(c) RoBench2024-P", fontsize=18,)
    # plt.show()
    plt.savefig(save_pth)
    print("save done.")


# running entry
if __name__ == "__main__":
    # main()
    print("EVERYTHING DONE.")
