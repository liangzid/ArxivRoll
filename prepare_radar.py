"""
======================================================================
PREPARE_RADAR ---

Provide the data for the radar.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 12 December 2024
======================================================================
"""

# ------------------------ Code --------------------------------------

import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
from collections import OrderedDict

from rs import *


def parseOverAllFileForRADAR(
    readpath="overall_res.json",
):
    with open(readpath, "r", encoding="utf8") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
        data = data[0]

    modells = list(data.keys())
    overall_taskls = list(data[modells[0]].keys())

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
    overall_results = {}
    for model in modells:
        templs = []
        scorePub_dict = {}
        scorePri_dict = {}
        scoreRSI_dict = {}
        scoreRSII = -1.0
        scoreNRSII = -1.0
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
            scorePub_dict[domain] = avg_pub
            scorePri_dict[domain] = avg_pri
            scoreRSI_dict[domain] = avg_pub - avg_pri
        overall_results[model] = {
            "PublicAveragedScore": scorePub_dict,
            "RobenchAveragedScore": scorePri_dict,
            "RS1": scoreRSI_dict,
        }
        matched_pub_priv_scores.append(templs)
    # then
    unmatched_pri_scores = [[] for m in modells]
    RS2_res = getRSIIAbsoluteScore4AllModels(
        matched_pub_priv_scores,
        unmatched_pri_scores,
    )
    RS2_norm_res = getRSIINORMAILIZEDScore4AllModels(
        matched_pub_priv_scores,
        unmatched_pri_scores,
    )

    for i, model in enumerate(modells):
        overall_results[model]["RS_II"] = RS2_res[i]
        overall_results[model]["N-RS_II"] = RS2_norm_res[i]

    with open("Results--Radar.json", "w", encoding="utf8") as f:
        json.dump(overall_results, f, ensure_ascii=False, indent=4)


def _getRelSorting(a2darray):
    rowranks = np.argsort(a2darray, axis=0)
    return rowranks[:, ::-1] + 1


if __name__ == "__main__":
    parseOverAllFileForRADAR()
