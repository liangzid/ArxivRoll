"""
======================================================================
RS ---

Metric: rugged score.

    Author: XXXXXX <xxxxxx@xxxxxx>
    Copyright © 2024, XXXXXX, all rights reserved.
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
from collections import OrderedDict


def getRSI_absolute(
    paired_scores,
    unmatched_pub_scores,
    unmatched_pri_scores,
):
    part1_ls = [2 * (a - b) / (a + b) for a, b in paired_scores]
    avg_part1 = sum(part1_ls) / len(part1_ls)

    if len(unmatched_pub_scores) == 0:
        avg_pub = 0.0
    else:
        avg_pub = sum(unmatched_pub_scores) / len(unmatched_pub_scores)

    if len(unmatched_pri_scores) == 0:
        avg_pri = 0.0
    else:
        avg_pri = sum(unmatched_pri_scores) / len(unmatched_pri_scores)

    if avg_pri == 0.0:
        avg_part2 = 0.0
    else:
        avg_part2 = 2 * (avg_pub - avg_pri) / (avg_pub + avg_pri)

    return avg_part1 + avg_part2


def _getRelSorting(a2darray):
    rowranks = np.argsort(a2darray, axis=0)
    return rowranks[:, ::-1] + 1


def getRSIAbsolute4AllModels(
    pair_ss,
    upubss,
    upriss,
):
    overall_res = []
    for i in range(len(pair_ss)):
        overall_res.append(
            getRSI_absolute(
                pair_ss[i],
                upubss[i],
                upriss[i],
            )
        )
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
    # var = np.var(overall_private_ss, axis=1, ddof=1)
    std = np.std(overall_private_ss, axis=1, ddof=1)
    return std


def getRSIINORMAILIZEDScore4AllModels(pairedss, upri_ss):

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
    # var = np.var(overall_private_ss, axis=1, ddof=1)
    mean = np.mean(overall_private_ss, axis=1)
    std = np.std(overall_private_ss, axis=1, ddof=1)
    normalized_std = std / mean
    return normalized_std


def parseResdict2PairedUnpariedLists(
    readpath="overall_res.json",
    RS_res_save_path="ruggedscore_overall.json",
):
    with open(readpath, "r", encoding="utf8") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    data = data[0]

    modells = list(data.keys())
    overall_taskls = list(data[modells[0]].keys())

    unmatched_pri_scores = [[] for m in modells]

    # obtain the values of unmatched public benchmarks
    unmatched_pub_scores = []
    unmatched_public_benchmarks = [
        "mmlu_pro_chemistry",
        "mmlu_pro_health",
        "mmlu_pro_history",
        "mmlu_pro_law",
        "mmlu_pro_other",
        "mmlu_pro_philosophy",
        "mmlu_pro_psychology",
        # ---------------------------
        "mmlu_other",
        "mmlu_social_sciences",
        "mmlu_humanities",
        "mmlu_college_chemistry",
        # "mmlu_high_school_chemistry",
        # "mmlu_high_school_geography",
    ]
    for model in modells:
        templs = []
        for upb in unmatched_public_benchmarks:
            templs.append(data[model][upb]["acc"])
        unmatched_pub_scores.append(templs)

    # obtain the values of paired public and private benchmarks

    private_benchname_key_dict = {
        "robench2024b_all_setcsSCP-s": "cs",
        "robench2024b_all_setcsSCP-c": "cs",
        "robench2024b_all_setcsSCP-p": "cs",
        "robench2024b_all_setq-finSCP-s": "fin",
        "robench2024b_all_setq-finSCP-c": "fin",
        "robench2024b_all_setq-finSCP-p": "fin",
        "robench2024b_all_setmathSCP-s": "math",
        "robench2024b_all_setmathSCP-c": "math",
        "robench2024b_all_setmathSCP-p": "math",
        "robench2024b_all_seteessSCP-s": "eess",
        "robench2024b_all_seteessSCP-c": "eess",
        "robench2024b_all_seteessSCP-p": "eess",
        "robench2024b_all_setphysicsSCP-s": "physics",
        "robench2024b_all_setphysicsSCP-c": "physics",
        "robench2024b_all_setphysicsSCP-p": "physics",
        "robench2024b_all_setstatSCP-s": "stat",
        "robench2024b_all_setstatSCP-c": "stat",
        "robench2024b_all_setstatSCP-p": "stat",
        "robench2024b_all_setq-bioSCP-s": "q-bio",
        "robench2024b_all_setq-bioSCP-c": "q-bio",
        "robench2024b_all_setq-bioSCP-p": "q-bio",
        "robench2024b_all_seteconSCP-s": "econ",
        "robench2024b_all_seteconSCP-c": "econ",
        "robench2024b_all_seteconSCP-p": "econ",
    }

    private_key_benchname_dict = {
        "cs": [
            "robench2024b_all_setcsSCP-s",
            "robench2024b_all_setcsSCP-c",
            "robench2024b_all_setcsSCP-p",
        ],
        "fin": [
            "robench2024b_all_setq-finSCP-s",
            "robench2024b_all_setq-finSCP-c",
            "robench2024b_all_setq-finSCP-p",
        ],
        "math": [
            "robench2024b_all_setmathSCP-s",
            "robench2024b_all_setmathSCP-c",
            "robench2024b_all_setmathSCP-p",
        ],
        "econ": [
            "robench2024b_all_seteconSCP-s",
            "robench2024b_all_seteconSCP-c",
            "robench2024b_all_seteconSCP-p",
        ],
        "eess": [
            "robench2024b_all_seteessSCP-s",
            "robench2024b_all_seteessSCP-c",
            "robench2024b_all_seteessSCP-p",
        ],
        "physics": [
            "robench2024b_all_setphysicsSCP-s",
            "robench2024b_all_setphysicsSCP-c",
            "robench2024b_all_setphysicsSCP-p",
        ],
        "stat": [
            "robench2024b_all_setstatSCP-s",
            "robench2024b_all_setstatSCP-c",
            "robench2024b_all_setstatSCP-p",
        ],
        "q-bio": [
            "robench2024b_all_setq-bioSCP-s",
            "robench2024b_all_setq-bioSCP-c",
            "robench2024b_all_setq-bioSCP-p",
        ],
    }

    domain_ls = list(private_key_benchname_dict.keys())

    private_public_align_dict = {
        "cs": [
            "mmlu_pro_computer_science",
            "mmlu_college_computer_science",
            "mmlu_computer_security",
            "mmlu_high_school_computer_science",
            "mmlu_machine_learning",
        ],
        "econ": [
            "mmlu_pro_economics",
            "mmlu_econometrics",
            "mmlu_high_school_microeconomics",
            "mmlu_high_school_macroeconomics",
        ],
        "eess": [
            "mmlu_pro_engineering",
            "mmlu_electrical_engineering",
        ],
        "math": [
            "mmlu_pro_math",
            "mmlu_abstract_algebra",
            "mmlu_college_mathematics",
            "mmlu_elementary_mathematics",
            "mmlu_formal_logic",
            "mmlu_high_school_mathematics",
            "gsm8k",
            "gsm_plus",
        ],
        "physics": [
            "mmlu_pro_physics",
            "mmlu_astronomy",
            "mmlu_college_physics",
            "mmlu_conceptual_physics",
            "mmlu_high_school_physics",
        ],
        "q-bio": [
            "mmlu_pro_biology",
            "mmlu_anatomy",
            "mmlu_clinical_knowledge",
            "mmlu_college_biology",
            "mmlu_college_medicine",
            "mmlu_high_school_biology",
        ],
        "fin": [
            "mmlu_pro_business",
            "mmlu_business_ethics",
        ],
        "stat": [
            "mmlu_pro_math",
            "mmlu_high_school_statistics",
        ],
    }

    matched_pub_priv_scores = []
    for model in modells:
        templs = []
        for domain in domain_ls:
            related_public_benchls = private_public_align_dict[domain]
            related_priviate_benchls = private_key_benchname_dict[domain]
            avg_pub = []
            for rpb in related_public_benchls:
                value = data[model][rpb]["acc"]
                if value < 0:
                    continue
                else:
                    avg_pub.append(value)
            if len(avg_pub) == 0:
                avg_pub = 0.0
                print(f"model: {model}\n domain: {domain}")
            else:
                avg_pub = sum(avg_pub) / len(avg_pub)
            avg_pri = []
            for rpb in related_priviate_benchls:
                value = data[model][rpb]["acc"]
                assert value >= 0
                avg_pri.append(value)
            avg_pri = sum(avg_pri) / len((avg_pri))
            templs.append([avg_pub, avg_pri])
        matched_pub_priv_scores.append(templs)

    unmatched_pub_scores = [[] for m in modells]

    # print("Matched Public and Private Scores:")
    # print(matched_pub_priv_scores)

    # compute the results for RS-I and RS-II.
    absolute_RS1_res = getRSIAbsolute4AllModels(
        matched_pub_priv_scores,
        unmatched_pub_scores,
        unmatched_pri_scores,
    )
    relative_RS1_res = getRSIRelative4AllModels(
        matched_pub_priv_scores,
        unmatched_pub_scores,
        unmatched_pri_scores,
    )
    RS2_res = getRSIIAbsoluteScore4AllModels(
        matched_pub_priv_scores,
        unmatched_pri_scores,
    )
    RS2_norm_res = getRSIINORMAILIZEDScore4AllModels(
        matched_pub_priv_scores,
        unmatched_pri_scores,
    )

    # finally: merge into three dicts.
    abs_rs1_dict = {}
    rel_rs1_dict = {}
    rs2_dict = {}
    rs2_norm_dict = {}
    private_dict = {}
    for i, model in enumerate(modells):
        abs_rs1_dict[model] = absolute_RS1_res[i]
        rel_rs1_dict[model] = relative_RS1_res[i]
        rs2_dict[model] = RS2_res[i]
        rs2_norm_dict[model] = RS2_norm_res[i]
        private_dict[model] = mean([x[1] for x in matched_pub_priv_scores[i]])

    with open(RS_res_save_path, "w", encoding="utf8") as f:
        json.dump(
            {
                "abs-rs1": abs_rs1_dict,
                "rel-rs1": rel_rs1_dict,
                "rs2": rs2_dict,
                "norm-rs2": rs2_norm_dict,
                "pub_pri_performance": private_dict,
            },
            f,
            ensure_ascii=False,
            indent=4,
        )
    print(f"Save DONE. Save to {RS_res_save_path}...")


def mean(xls):
    return sum(xls) / len(xls)


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
    # main()
    parseResdict2PairedUnpariedLists()
