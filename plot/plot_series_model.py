"""
======================================================================
PLOT_SERIES_MODEL --- 

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


import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from sklearn import metrics
import sklearn
from collections import OrderedDict


def scatters_series_model():

    x1ls = [4.21, 12.04, 12.71]
    y1ls = [1.21, 0.82, 1.27]

    x2ls = [8.34, 21.83, 26.94]
    y2ls = [1.14, 0.74, 0.67]

    x3ls = [28.20, 28.95]
    y3ls = [0.69, 0.70]

    robench__series_models_dict = OrderedDict(
        {
            "Phi": {
                "Phi-1": 4.21,
                "Phi-1.5": 12.04,
                # "Phi-2": 21.78,
                "Phi-3-mini": 12.71,
                # "Phi-3.5-mini": 17.02,
            },
            "Llama": {
                "Llama2-7b": 8.34,
                "Llama3-8b": 21.83,
                "Llama3.1-8b": 26.94,
                # "Llama3.2": 0.00,
            },
            "Qwen": {
                # "Qwen1.5-7B":4.67,
                "Qwen2-7B": 28.20,
                "Qwen2.5-7B": 28.95,
            },
        }
    )

    rs__series_models_dict = OrderedDict(
        {
            "Phi": {
                "Phi-1": 1.21,
                "Phi-1.5": 0.82,
                "Phi-2": 0.62,
                "Phi-3-mini": 1.27,
                "Phi-3.5-mini": 1.07,
            },
            "Llama": {
                "Llama2-7b": 1.14,
                "Llama3-8b": 0.74,
                "Llama3.1-8b": 0.67,
                # "Llama3.2": 0.00,
            },
            "Qwen": {
                "Qwen2-7B": 0.69,
                "Qwen2.5-7B": 0.70,
            },
        }
    )

    marker_dict = {
        "Phi-1": "d",
        "Phi-1.5": "d",
        "Phi-2": "d",
        "Phi-3-mini": "d",
        "Phi-3.5-mini": "d",
        "Llama2-7b": "o",
        "Llama3-8b": "o",
        "Llama3.1-8b": "o",
        "Llama3.2": "o",
        # "Finnish-to-English": "H",
        "Qwen2-7B": "s",
        "Qwen2.5-7B": "s",
    }
    cls = [
        "#66C2A5",
        "#FC8D62",
        "#8DA0CB",
        "#E78AC3",
        "#A6D854",
        "#FFD92F",
        "#E5C494",
        "#B3B3B3",
    ]
    color_dict = {
        "Phi-1": "#f6cbed",
        "Phi-1.5": "#e774ce",
        "Phi-2": "#d025ab",
        "Phi-3-mini": "#791564",
        "Phi-3.5-mini": "#23061c",
        # "Llama2-7b": "#d5e8eb",
        # "Llama3-8b": "#90c3c8",
        # "Llama3.1-8b": "#4e9ba6",
        # "Llama3.2": "#2e5a61",
        "Llama2-7b": "#90c3c8",
        "Llama3-8b": "#4e9ba6",
        "Llama3.1-8b": "#2e5a61",
        "Qwen-7B": "#f1c40f",
        "Qwen1.5-7B": "#f39c12",
        "Qwen2-7B": "#e67e22",
        "Qwen2.5-7B": "#d35400",
    }

    # color_dict = {
    #     "Phi-1": cls[0],
    #     "Phi-1.5": cls[0],
    #     "Phi-2": cls[0],
    #     "Phi-3-mini": cls[0],
    #     "Phi-3.5-mini": cls[0],

    #     "Llama2-7b": cls[1],
    #     "Llama3-8b": cls[1],
    #     "Llama3.1-8b": cls[1],
    #     "Llama3.2": cls[1],
    #     # "Finnish-to-English": cls[0],
    #     "Qwen2-7B": cls[2],
    #     "Qwen2.5-7B": cls[2],
    # }

    plt.style.use("seaborn-v0_8-dark")
    # plt.style.use("Solarize_Light2")
    fig, axs = plt.subplots(1, 1, figsize=(5.5, 4.3))
    fig.subplots_adjust(wspace=0.01, hspace=0.5)

    fs = 13
    axs.grid(True)
    compact_dict = OrderedDict({})

    # axs.plot(
    #     y1ls,
    #     x1ls,
    #     color="red",
    #     marker=".",
    #     markersize=0.1,
    #     markerfacecolor="red",
    #     alpha=0.6,
    # )

    # axs.plot(
    #     y2ls,
    #     x2ls,
    #     color="green",
    #     marker=".",
    #     markersize=0.1,
    #     markerfacecolor="green",
    #     alpha=0.6,
    # )

    # axs.plot(
    #     y3ls,
    #     x3ls,
    #     color="orange",
    #     marker=".",
    #     markersize=0.1,
    #     markerfacecolor="orange",
    #     alpha=0.9,
    # )

    for domain_key in robench__series_models_dict.keys():
        for task_key in robench__series_models_dict[domain_key].keys():
            y = robench__series_models_dict[domain_key][task_key]
            x = rs__series_models_dict[domain_key][task_key]
            compact_dict[task_key] = [x, y]
    for task in compact_dict.keys():
        x = compact_dict[task][0]
        y = compact_dict[task][1]
        axs.scatter(
            x,
            y,
            s=240,
            c=color_dict[task],
            # c="#EAEAF2",
            # facecolors=color_dict[task],
            # edgecolors=color_dict[task],
            linewidths=0.0,
            marker=marker_dict[task],
            alpha=1.0,
            label=task,
        )

    font1 = {
        "weight": "normal",
        "size": 9,
    }
    plt.legend(
        # loc=(0.02, 0.03),
        loc="best",
        prop=font1,
        ncol=2,
        # frameon=True,
        markerscale=0.5,
        handletextpad=0.0,
        handlelength=1.2,
    )  # 设置信息框

    # axs.set_yticks([0, 1, 2, 3, 4,])
    # axs.set_xticks([0, 1, 2])
    # axs.set_yticklabels(local_ls, fontsize=fs-2, rotation=45,)
    # axs.set_xticklabels(victim_ls, fontsize=fs-2,)
    axs.set_ylabel(
        "Avg. Acc. on Robench",
        fontsize=fs,
        fontfamily="DejaVu Sans",
        fontweight="normal",
    )
    axs.set_xlabel(
        "RS$_I$",
        fontsize=fs,
        fontfamily="DejaVu Sans",
        fontweight="normal",
    )
    # axs.set_xlim(0.835, 1.00)

    # for (i,j), value in np.ndenumerate(res_mat):
    #     axs[0].text(j,i,"{:.2f}".format(value),
    #              ha="center",
    #              va="center",
    #              color="white",
    #              fontsize=fs+2,)

    save_path = "seriesmodel-results.pdf"
    plt.savefig(save_path, pad_inches=0.1)
    print("SAVE DONE.")


if __name__ == "__main__":
    scatters_series_model()
