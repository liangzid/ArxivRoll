"""
======================================================================
RS ---

Metric: rugged score.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 13 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------
# normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp

import numpy as np


def getRSI_absolute(
        paired_scores,
        unmatched_pub_scores,
        unmatched_pri_scores,
):
    part1_ls = [a-b for a, b in paired_scores]
    avg_part1 = sum(part1_ls)/len(part1_ls)

    avg_part2 = sum(unmatched_pub_scores)/len(unmatched_pub_scores)\
        - sum(unmatched_pri_scores)/len(unmatched_pri_scores)

    return avg_part1 + avg_part2


def _getRelSorting(a2darray):
    rowranks = np.argsort(a2darray, axis=0)
    return rowranks[:, ::-1]+1


def getRSIAbsolute4AllModels(
        pair_ss,
        upubss,
        upriss,
):
    overall_res = []
    for i in range(len(pair_ss)):
        overall_res.append(getRSI_absolute(
            pair_ss[i],
            upubss[i],
            upriss[i],
        ))
    return overall_res


def getRSIRelative4AllModels(
        paired_scores,
        unmatched_pub_scores,
        unmatched_pri_scores,
):

    # 1. first transform the absolute results into their relative ranks.
    paired_pub_ss = []
    paired_pri_ss = []
    for permodells in paired_scores:
        ppubs = []
        ppris = []
        for perbenchmark in permodells:
            ppubs.append(perbenchmark[0])
            ppris.append(perbenchmark[1])
        paired_pub_ss.append(ppubs)
        paired_pri_ss.append(ppris)

    paired_pub_ss = np.array(paired_pub_ss)
    paired_pri_ss = np.array(paired_pri_ss)
    unmatched_pub_scores = np.array(unmatched_pub_scores)
    unmatched_pri_scores = np.array(unmatched_pri_scores)

    rppubss = _getRelSorting(paired_pub_ss)
    rppriss = _getRelSorting(paired_pri_ss)
    rumpubss = _getRelSorting(unmatched_pub_scores)
    rumpriss = _getRelSorting(unmatched_pri_scores)

    rss = []

    # 2. then compute the RS score for all of the models:
    for i_model in range(len(rppubss)):
        rppubs = rppubss[i_model]
        rppris = rppriss[i_model]
        rumpubs = rumpubss[i_model]
        rumpris = rumpriss[i_model]
        pairls = list(zip(rppubs, rppris))
        rs = getRSI_absolute(
            pairls,
            rumpubs,
            rumpris,
        )
        rss.append(rs)
    return rss


def getRSIIAbsoluteScore4AllModels(pairedss, upri_ss):

    # 0. extract private datasets
    paired_pri_ss = []
    for permodells in pairedss:
        ppris = []
        for perbenchmark in permodells:
            ppris.append(perbenchmark[1])
        paired_pri_ss.append(ppris)

    overall_private_ss = []
    for i_model in range(len(pairedss)):
        templs = upri_ss[i_model]
        templs.extend(paired_pri_ss[i_model])
        overall_private_ss.append(templs)
    overall_private_ss = np.array(overall_private_ss)
    var = np.var(overall_private_ss, axis=1, ddof=1)
    return var


def main():

    # # one model: -- i.e., at sample level

    # paired_scores = [
    #     (0.9, 0.1), (0.7, 0.69)
    # ]
    # pubs = [0.7, 0.5, 0.9]
    # pris = [0.2,]
    # abs_rs = getRSI_absolute(paired_scores, pubs, pris)
    # print(f"Absolute RS: {abs_rs}.")

    # -------------------------------------------------------------

    paired_scores = [
        [[0.9, 0.1], [0.72, 0.69]],
        [[0.4, 0.8], [0.7, 0.71]],
    ]
    pubss = [
        [0.92, 0.97],
        [0.90, 0.91],
    ]
    priss = [
        [0.87],
        [0.91],
    ]

    rank_idx = _getRelSorting(paired_scores[0])
    print(rank_idx)

    abs_rs = getRSIAbsolute4AllModels(paired_scores, pubss, priss)
    print(f"Absolute RS: {abs_rs}.")

    rel_rs = getRSIRelative4AllModels(paired_scores, pubss, priss)
    print(f"Relative RS: {rel_rs}")

    abs_rsII = getRSIIAbsoluteScore4AllModels(paired_scores, priss)
    print(f"RS II, Absolute: {abs_rsII}.")


if __name__ == "__main__":
    main()
