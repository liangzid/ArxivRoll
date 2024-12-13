"""
======================================================================
RESULTS_AND_RANK --- 

Results and the rank for third part private benchmarks.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 26 November 2024
======================================================================
"""

# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp

from scipy.stats import pearsonr, spearmanr
from scipy.stats import kendalltau
# from pingouin import gamma_corr


def computeMetrics(vec1, vec2):

    pearson_corr, _ = pearsonr(vec1, vec2)
    spearman_corr, _ = spearmanr(vec1, vec2)
    kendall_corr, _ = kendalltau(vec1, vec2)
    # gamma_corr = gamma_corr(vec1, vec2,)

    res = {
        "pearson": pearson_corr,
        "spearman": spearman_corr,
        "kendall": kendall_corr,
        # "gamma": gamma_corr,
    }
    return res


def computeCorrelation():

    # Experiment results for Chatbot Arena
    chatbot_arena_scores = {
        "overall": {
            "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF": 1269,
            # "llama-3-70b-instruct": 1206,
            # "Qwen2-72b-instruct": 1187,
            "meta-llama/Llama-3.1-8B-Instruct": 1175,
            "01-ai/Yi-1.5-34B-Chat": 1157,
            "meta-llama/Meta-Llama-3-8B": 1152,
            # "meta-llama-3.2-3b-instruct": 1103,
            # "microsoft/Phi-3-mini-4k-instruct": 1066,
            "meta-llama/Llama-2-7b-chat-hf": 1037,
            "princeton-nlp/gemma-2-9b-it-SimPO": 1216,
            # "ai21labs/AI21-Jamba-1.5-Mini": 1176,
            # "Qwen/Qwen1.5-14B-Chat": 1109,
            "mistralai/Mistral-7B-Instruct-v0.2": 1072,
            "Qwen/Qwen1.5-7B-Chat": 1070,
            # "meta-llama/Llama-2-13b-chat-hf": 1063,
            "HuggingFaceH4/zephyr-7b-beta": 1053,
            "mistralai/Mistral-7B-Instruct-v0.1": 1008,
        }
    }

    robench_s = {
        "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF": 33.33,
        # "llama-3-70b-instruct": 1206,
        # "Qwen2-72b-instruct": 1187,
        "meta-llama/Llama-3.1-8B-Instruct": 28.48,
        "01-ai/Yi-1.5-34B-Chat": 28.11,
        "meta-llama/Meta-Llama-3-8B": 22.89,
        # "meta-llama-3.2-3b-instruct": 1103,
        "microsoft/Phi-3-mini-4k-instruct": 6.31,
        "meta-llama/Llama-2-7b-chat-hf": 7.47,
        "princeton-nlp/gemma-2-9b-it-SimPO": 25.75,
        # "ai21labs/AI21-Jamba-1.5-Mini": 1176,
        # "Qwen/Qwen1.5-14B-Chat": 1109,
        "mistralai/Mistral-7B-Instruct-v0.2": 23.50,
        "Qwen/Qwen1.5-7B-Chat": 11.29,
        # "meta-llama/Llama-2-13b-chat-hf": 1063,
        "HuggingFaceH4/zephyr-7b-beta": 18.08,
        "mistralai/Mistral-7B-Instruct-v0.1": 24.01,
    }

    robench_c = {
        "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF": 26.92,
        # "llama-3-70b-instruct": 1206,
        # "Qwen2-72b-instruct": 1187,
        "meta-llama/Llama-3.1-8B-Instruct": 26.20,
        "01-ai/Yi-1.5-34B-Chat": 19.81,
        "meta-llama/Meta-Llama-3-8B": 18.17,
        # "meta-llama-3.2-3b-instruct": 1103,
        "microsoft/Phi-3-mini-4k-instruct": 21.91,
        "meta-llama/Llama-2-7b-chat-hf": 3.15,
        "princeton-nlp/gemma-2-9b-it-SimPO": 26.54,
        # "ai21labs/AI21-Jamba-1.5-Mini": 1176,
        # "Qwen/Qwen1.5-14B-Chat": 1109,
        "mistralai/Mistral-7B-Instruct-v0.2": 22.21,
        "Qwen/Qwen1.5-7B-Chat": 3.57,
        # "meta-llama/Llama-2-13b-chat-hf": 1063,
        "HuggingFaceH4/zephyr-7b-beta": 17.12,
        "mistralai/Mistral-7B-Instruct-v0.1": 26.25,
    }

    robench_p = {
        "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF": 37.90,
        # "llama-3-70b-instruct": 1206,
        # "Qwen2-72b-instruct": 1187,
        "meta-llama/Llama-3.1-8B-Instruct": 29.46,
        "01-ai/Yi-1.5-34B-Chat": 31.30,
        "meta-llama/Meta-Llama-3-8B": 24.85,
        # "meta-llama-3.2-3b-instruct": 1103,
        "microsoft/Phi-3-mini-4k-instruct": 11.87,
        "meta-llama/Llama-2-7b-chat-hf": 13.67,
        "princeton-nlp/gemma-2-9b-it-SimPO": 38.02,
        # "ai21labs/AI21-Jamba-1.5-Mini": 1176,
        # "Qwen/Qwen1.5-14B-Chat": 1109,
        "mistralai/Mistral-7B-Instruct-v0.2": 20.78,
        "Qwen/Qwen1.5-7B-Chat": 0.03,
        # "meta-llama/Llama-2-13b-chat-hf": 1063,
        "HuggingFaceH4/zephyr-7b-beta": 22.96,
        "mistralai/Mistral-7B-Instruct-v0.1": 26.08,
    }

    modells = list(chatbot_arena_scores["overall"].keys())

    chatls = [chatbot_arena_scores["overall"][x] for x in modells]
    sls = [robench_s[x] for x in modells]
    cls = [robench_c[x] for x in modells]
    pls = [robench_p[x] for x in modells]

    res ={
            "S-Arena": computeMetrics(sls, chatls),
            "C-Arena": computeMetrics(cls, chatls),
            "P-Arena": computeMetrics(pls, chatls),
            "S-C": computeMetrics(sls, cls),
            "S-P": computeMetrics(sls, pls),
            "C-P": computeMetrics(sls, pls),
        }

    ppp(res)

    with open("CorrelationExperiments.json", 'w',encoding='utf8') as f:
        json.dump(res,f,ensure_ascii=False,indent=4)

        

if __name__=="__main__":
    computeCorrelation()
    
