"""
======================================================================
1.PARSE_COLLECT_EXPER_RES ---

parse the results of `lm_eval` and collect them to compute the RS score.

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
import os
from collections import OrderedDict


def main():
    model_ls = [
        "EleutherAI/gpt-j-6B",
        "microsoft/phi-1",
        "microsoft/phi-1_5",
        "microsoft/phi-2",
        "microsoft/Phi-3-mini-4k-instruct",
        "microsoft/Phi-3.5-mini-instruct",
        "Qwen/Qwen2-7B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "meta-llama/Llama-2-7b-chat-hf",
        "meta-llama/Meta-Llama-3-8B",
        "meta-llama/Llama-3.1-8B-Instruct",
        "Qwen/Qwen2.5-72B-Instruct",
        "01-ai/Yi-1.5-34B-Chat",
        "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
        "meta-llama/Llama-3.1-70B-Instruct",
    ]

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
        "robench2024b_all_seteessSCP-s",
        "robench2024b_all_seteessSCP-c",
        "robench2024b_all_seteessSCP-p",
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

    unmatched_private_benchmarks = []

    overall_dataset_ls = []
    for ky in private_public_align_dict:
        for ele in private_public_align_dict[ky]:
            overall_dataset_ls.append(ele)
    overall_dataset_ls.extend(unmatched_public_benchmarks)
    overall_dataset_ls.extend(unmatched_private_benchmarks)
    overall_dataset_ls.extend(private_benchmark_ls)

    parseCompRes(
        model_ls,
        overall_dataset_ls,
        result_save_pth="overall_res.json",
    )


def main2():
    model_ls = [
        # "EleutherAI/gpt-j-6B", "microsoft/Phi-3.5-mini-instruct", "Qwen/Qwen2-7B-Instruct" ,
        # "meta-llama/Meta-Llama-3-8B",
        # "meta-llama/Llama-3.1-8B-Instruct",
        # "microsoft/phi-1",
        # "microsoft/phi-1_5",
        # "microsoft/phi-2",
        # "microsoft/Phi-3-mini-4k-instruct",
        # "meta-llama/Llama-2-7b-chat-hf",
        # "meta-llama/Llama-2-13b-chat-hf",
        # "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen2.5-72B-Instruct",
        "01-ai/Yi-1.5-34B-Chat",
        "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
        "meta-llama/Llama-3.1-70B-Instruct",
    ]
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
        "robench2024b_all_seteessSCP-s",
        "robench2024b_all_seteessSCP-c",
        "robench2024b_all_seteessSCP-p",
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

    parseCompRes(
        model_ls,
        private_benchmark_ls,
        result_save_pth="private_overall_res.json",
    )


def main3():
    model_ls = [
        "EleutherAI/gpt-j-6B",
        "microsoft/phi-1",
        "microsoft/phi-1_5",
        "microsoft/phi-2",
        "microsoft/Phi-3-mini-4k-instruct",
        "microsoft/Phi-3.5-mini-instruct",
        "Qwen/Qwen2-7B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "meta-llama/Llama-2-7b-chat-hf",
        "meta-llama/Meta-Llama-3-8B",
        "meta-llama/Llama-3.1-8B-Instruct",
        "Qwen/Qwen2.5-72B-Instruct",
        "01-ai/Yi-1.5-34B-Chat",
        "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
        "meta-llama/Llama-3.1-70B-Instruct",

        # for those only `cs` has been executed.
        "princeton-nlp/gemma-2-9b-it-SimPO",
        "ai21labs/AI21-Jamba-1.5-Mini",
        "mistralai/Mistral-7B-Instruct-v0.2",
        "Qwen/Qwen1.5-7B-Chat",
        "HuggingFaceH4/zephyr-7b-beta",
        "mistralai/Mistral-7B-Instruct-v0.1",
    ]

    private_benchmark_ls = [
        "robench2024b_all_setcsSCP-s",
        "robench2024b_all_setcsSCP-c",
        "robench2024b_all_setcsSCP-p",
        # "robench2024b_all_setq-finSCP-s",
        # "robench2024b_all_setq-finSCP-c",
        # "robench2024b_all_setq-finSCP-p",
        # "robench2024b_all_setmathSCP-s",
        # "robench2024b_all_setmathSCP-c",
        # "robench2024b_all_setmathSCP-p",
        # "robench2024b_all_seteessSCP-s",
        # "robench2024b_all_seteessSCP-c",
        # "robench2024b_all_seteessSCP-p",
        # "robench2024b_all_setphysicsSCP-s",
        # "robench2024b_all_setphysicsSCP-c",
        # "robench2024b_all_setphysicsSCP-p",
        # "robench2024b_all_setstatSCP-s",
        # "robench2024b_all_setstatSCP-c",
        # "robench2024b_all_setstatSCP-p",
        # "robench2024b_all_setq-bioSCP-s",
        # "robench2024b_all_setq-bioSCP-c",
        # "robench2024b_all_setq-bioSCP-p",
        # "robench2024b_all_seteconSCP-s",
        # "robench2024b_all_seteconSCP-c",
        # "robench2024b_all_seteconSCP-p",
    ]

    parseCompRes(
        model_ls,
        private_benchmark_ls,
        result_save_pth="private_openmodels_res.json",
    )

def main4():
    model_ls = [
        # "EleutherAI/gpt-j-6B", "microsoft/Phi-3.5-mini-instruct", "Qwen/Qwen2-7B-Instruct" ,
        # "meta-llama/Meta-Llama-3-8B",
        # "meta-llama/Llama-3.1-8B-Instruct",
        # "microsoft/phi-1",
        # "microsoft/phi-1_5",
        # "microsoft/phi-2",
        # "microsoft/Phi-3-mini-4k-instruct",
        # "meta-llama/Llama-2-7b-chat-hf",
        # "meta-llama/Llama-2-13b-chat-hf",
        # "Qwen/Qwen2.5-7B-Instruct",
        "gpt-4o", "gpt-3.5-turbo", "gpt-4",
    ]
    private_benchmark_ls = [
        "robench2024b_all_setcsSCP-s-50",
        "robench2024b_all_setcsSCP-c-50",
        "robench2024b_all_setcsSCP-p-50",
        "robench2024b_all_setq-finSCP-s-50",
        "robench2024b_all_setq-finSCP-c-50",
        "robench2024b_all_setq-finSCP-p-50",
        "robench2024b_all_setmathSCP-s-50",
        "robench2024b_all_setmathSCP-c-50",
        "robench2024b_all_setmathSCP-p-50",
        "robench2024b_all_seteessSCP-s-50",
        "robench2024b_all_seteessSCP-c-50",
        "robench2024b_all_seteessSCP-p-50",
        "robench2024b_all_setphysicsSCP-s-50",
        "robench2024b_all_setphysicsSCP-c-50",
        "robench2024b_all_setphysicsSCP-p-50",
        "robench2024b_all_setstatSCP-s-50",
        "robench2024b_all_setstatSCP-c-50",
        "robench2024b_all_setstatSCP-p-50",
        "robench2024b_all_setq-bioSCP-s-50",
        "robench2024b_all_setq-bioSCP-c-50",
        "robench2024b_all_setq-bioSCP-p-50",
        "robench2024b_all_seteconSCP-s-50",
        "robench2024b_all_seteconSCP-c-50",
        "robench2024b_all_seteconSCP-p-50",
    ]

    parseCompRes(
        model_ls,
        private_benchmark_ls,
        result_save_pth="overall_res_closeAIs.json",
    )



def parseCompRes(
    model_ls,
    dataset_ls,
    parsed_log_dir="./eval/0.2.closeAIs/",
    result_save_pth="overall_res_closeAIs.json",
):

    res_acc_lss = []
    res_std_lss = []
    res_model_dict = {}

    for model in model_ls:
        temp_acc_ls = []
        temp_std_ls = []
        res_model_dict[model] = {}
        for task in dataset_ls:
            try:
                log_pth = (
                    parsed_log_dir + str(model) + task + f"/" + model.replace("/", "__")
                )
                files = os.listdir(log_pth)
                find_flag = 0
                for fi in files:
                    print(log_pth)
                    if fi.endswith(".json") and "results" in fi:
                        find_flag = 1
                        break
                assert find_flag == 1
                logpth = log_pth + "/" + fi
                with open(logpth, "r", encoding="utf8") as f:
                    data = json.load(f, object_pairs_hook=OrderedDict)
                res_dict = data["results"][task]
                print(res_dict)
                res_acc = -1.0
                res_std = -1.0
                for ky in res_dict.keys():
                    if "acc," in ky or "exact_match," in ky:
                        res_acc = res_dict[ky]
                    if "exact_match_stderr," in ky or "acc_stderr," in ky:
                        res_std = res_dict[ky]
                assert res_acc >= 0.0
                assert res_std >= 0.0
            except Exception as e:
                res_acc = -1.0
                res_std = -1.0

            temp_acc_ls.append(res_acc)
            temp_std_ls.append(res_std)
            res_model_dict[model][task] = {
                "acc": res_acc,
                "std": res_std,
            }
        res_acc_lss.append(temp_acc_ls)
        res_std_lss.append(temp_std_ls)

    with open(result_save_pth, "w", encoding="utf8") as f:
        json.dump(
            [
                res_model_dict,
                res_acc_lss,
                res_std_lss,
            ],
            f,
            ensure_ascii=False,
            indent=4,
        )
    print(f"Save DONE. Save to {result_save_pth}.")
    print("---------------------------------------------------------")
    from pprint import pprint

    print(res_model_dict)
    print("---------------------------------------------------------")
    pprint(res_model_dict)


if __name__ == "__main__":
    # main()
    # main2()
    main4()
