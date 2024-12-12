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
            "microsoft/Phi-3-mini-4k-instruct": 1066,
            "meta-llama/Llama-2-7b-chat-hf": 1037,

            "princeton-nlp/gemma-2-9b-it-SimPO": 1216,
            "ai21labs/AI21-Jamba-1.5-Mini": 1176,
            # "Qwen/Qwen1.5-14B-Chat": 1109,
            "mistralai/Mistral-7B-Instruct-v0.2": 1072,
            "Qwen/Qwen1.5-7B-Chat": 1070,
            # "meta-llama/Llama-2-13b-chat-hf": 1063,
            "HuggingFaceH4/zephyr-7b-beta": 1053,
            "mistralai/Mistral-7B-Instruct-v0.1": 1008,
        }
    }

    
