"""
======================================================================
PLOT_BOX_STABILITY ---

Plot the box for stability for 32 repeated times.

    Author: XXXXXX <xxxxxx@xxxxxx>
    Copyright © 2024, XXXXXX, all rights reserved.
    Created: 12 December 2024
======================================================================
"""

# ------------------------ Code --------------------------------------

## normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp

import matplotlib.pyplot as plt
import numpy as np


def plot_boxplot(data1, data2, data3, labels, stdls):
    """
    Plot a boxplot for three datasets.

    Parameters:
        data1, data2, data3: list or numpy arrays
            The three datasets to visualize.
        labels: list of str
            The labels for the datasets.
    """
    # Combine the data into a list for boxplot
    data = [data1, data2, data3]

    plt.figure(figsize=(8, 5))

    boxprops = dict(color="black")
    # whiskerprops = dict(color="#f78fb3")
    # capprops = dict(color="#3867d6")
    medianprops = dict(color="#eb3b5a", linewidth=2)
    # meanprops = dict(marker="o", color="#f78fb3", markersize=9)

    pb=plt.boxplot(
        data,
        labels=labels,
        # patch_artist=True,
        showmeans=True,
        boxprops=boxprops,
        # whiskerprops=whiskerprops,
        # capprops=capprops,
        medianprops=medianprops,
        # meanprops=meanprops,
    )
    # plt.boxplot(data, labels=labels, patch_artist=True, showmeans=True)
    for i, std in enumerate(stdls):
        plt.text(i + 1.25, max(data[i]) - 0.005, f"Std: {std:.4f}",
                 ha='center', fontsize=13, color='black')

    # Create the boxplot

    # Add titles and labels
    # plt.title("Variants Among Multiple-times Generation", fontsize=14)
    plt.xlabel("Robench's Generation Strategies", fontsize=16)
    plt.ylabel("Accuracy", fontsize=16)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    # Show the plot
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    # plt.show()
    plt.savefig("box_stability.pdf")


def main():

    data_dict = {
        "p": {
            0: 0.32191563590231526,
            1: 0.33111322549952427,
            2: 0.33238185854741514,
            3: 0.3269901680938788,
            4: 0.3288931176657152,
            5: 0.33079606723755156,
            6: 0.3203298445924516,
            7: 0.32191563590231526,
            8: 0.31810973675864257,
            9: 0.31906121154456074,
            10: 0.32191563590231526,
            11: 0.3330161750713606,
            12: 0.31144941325721537,
            13: 0.33238185854741514,
            14: 0.3333333333333333,
            15: 0.31525531240088805,
            16: 0.31557247066286076,
            17: 0.3108150967332699,
            18: 0.3133523628290517,
            19: 0.32603869330796065,
            20: 0.3133523628290517,
            21: 0.31652394544877893,
            22: 0.3111322549952426,
            23: 0.32952743418966063,
            24: 0.3143038376149699,
            25: 0.31271804630510625,
            26: 0.31018078020932444,
            27: 0.30034887408817,
            28: 0.33206470028544244,
            29: 0.31240088804313354,
            30: 0.3051062480177609,
            31: 0.3228671106882334,
        },
        "c": {
            "0": 0.32191563590231526,
            "1": 0.33111322549952427,
            "2": 0.33238185854741514,
            "3": 0.3269901680938788,
            "4": 0.3288931176657152,
            "5": 0.33079606723755156,
            "6": 0.3203298445924516,
            "7": 0.32191563590231526,
            "8": 0.31810973675864257,
            "9": 0.31906121154456074,
            "10": 0.32191563590231526,
            "11": 0.3330161750713606,
            "12": 0.31144941325721537,
            "13": 0.33238185854741514,
            "14": 0.3333333333333333,
            "15": 0.31525531240088805,
            "16": 0.31557247066286076,
            "17": 0.3108150967332699,
            "18": 0.3133523628290517,
            "19": 0.32603869330796065,
            "20": 0.3133523628290517,
            "21": 0.31652394544877893,
            "22": 0.3111322549952426,
            "23": 0.32952743418966063,
            "24": 0.3143038376149699,
            "25": 0.31271804630510625,
            "26": 0.31018078020932444,
            "27": 0.30034887408817,
            "28": 0.33206470028544244,
            "29": 0.31240088804313354,
            "30": 0.3051062480177609,
            "31": 0.3228671106882334,
        },
        "s": {
            "0": 0.26791808873720135,
            "1": 0.24334470989761092,
            "2": 0.2501706484641638,
            "3": 0.2515358361774744,
            "4": 0.24769703172978505,
            "5": 0.24803821221426134,
            "6": 0.2658703071672355,
            "7": 0.24292050494711703,
            "8": 0.24701467076083247,
            "9": 0.23071672354948805,
            "10": 0.25963834868645513,
            "11": 0.25861480723302627,
            "12": 0.2412146025247356,
            "13": 0.24292050494711703,
            "14": 0.2541794609348345,
            "15": 0.2514500170590242,
            "16": 0.25656772432616853,
            "17": 0.26475605595359947,
            "18": 0.2440273037542662,
            "19": 0.24530876833845103,
            "20": 0.2569089048106448,
            "21": 0.2517911975435005,
            "22": 0.25571867531580744,
            "23": 0.24675767918088737,
            "24": 0.24744027303754265,
            "25": 0.24974411463664278,
            "26": 0.2572500852951211,
            "27": 0.2573378839590444,
            "28": 0.23643807574206754,
            "29": 0.2610030706243603,
            "30": 0.25656772432616853,
            "31": 0.24513485831341755,
        },
    }

    newdatadict = {}
    newdatadict["s"] = [v for k, v in data_dict["s"].items()]
    newdatadict["c"] = [v for k, v in data_dict["c"].items()]
    newdatadict["p"] = [v for k, v in data_dict["p"].items()]

    data1 = newdatadict["s"][10:]
    data2 = newdatadict["c"][10:]
    data3 = newdatadict["p"][10:]

    stdls = [
        np.std(data1, ddof=1),
        np.std(data2, ddof=1),
        np.std(data3, ddof=1),
    ]

    # Labels for the datasets
    labels = ["Sequencing", "Cloze", "Prediction"]

    # Plot the boxplot
    plot_boxplot(
        data1,
        data2,
        data3,
        labels,
        stdls,
    )


if __name__ == "__main__":
    main()
