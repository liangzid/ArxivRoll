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


SEAL_scores = {
    "math": {
        "claude-3.5-sonnet": 96.60,
        "gpt-4o": 95.68,
        "llama-3.1-405b-instruct": 95.60,
        "claude-3-opus": 95.19,
        "gpt-4-turbo-preview": 95.10,
        "gemini-1.5-pro": 94.69,
        "mistral-large-2": 93.94,
        "claude-3-sonnet": 93.28,
        "llama3-70b-instruct": 90.12,
        "gemini-1.5-flash": 90.12,
        "mistral-large": 87.47,
        "gemini-1.0-pro": 79.83,
        "codellama-34b-instruct": 37.51,
    },
    "instruction_following": {
        "o1-preview": 87.32,
        "claude-3.5-sonnet": 87.09,
        "llama-3.1-405b-instruct": 86.01,
        "gpt-4o": 85.29,
        "gemini-1.5pro": 85.09,
        "gpt-4-turbo-preview": 83.87,
        "mistral-large-2": 83.72,
        "llama-3-70b-instruct": 81.85,
        "mistral-large": 80.49,
        "claude-3-opus": 80.03,
        "claude-4-sonnet": 78.24,
        "gemini-1.5-flash": 77.25,
        "gemini-1.0-pro": 67.97,
        "codellama-34b-instruct": 57.69,
    },
}

chatbot_arena_scores = {
    "overall": {
        "gemini-exp-1121": 1365,
        "gpt-4o-20241120": 1361,
        "o1-preview": 1334,
        "o1-mini": 1308,
        "gemini-1.5-pro-002": 1301,
        "grok-2-08-13": 1289,
        "yi-lightning": 1287,
        "gpt-4o-2024-0513": 1285,
        "claude-3.5-sonnet(2024-10-22)": 1282,
        "athene-v2-chat-72b": 1274,
        "glm-4-plus": 1274,
        "gpt-4o-mini-2024-07-18": 1273,
        "gemini-1.5-flash-002": 1271,
        "llama-3.1-nemotron-70b-instruct": 1269,
        "Qwen2.5-Coder-32b-instruct": 1220,
        "gemma-2-27b-it": 1219,
        "gemma-2-9b-it-simPO": 1216,
        "yi-large": 1213,
        "llama-3-70b-instruct": 1206,
        "Hunyuan-Standard-256K": 1188,
        "Qwen2-72b-instruct": 1187,
        "gpt-4": 1186,
        "jamba-1.5-mini": 1176,
        "meta-llama-3.1-8b-instruct": 1175,
        "gpt-4-0613": 1163,
        "yi-1.5-34b-chat": 1157,
        "llama-3-8b-instruct": 1152,
        "Qwen1.5-14b-chat": 1109,
        "meta-llama-3.2-3b-instruct": 1103,
        "mistral-7b-instruct-v0.2": 1072,
        "qwen1.5-7b-chat": 1070,
        "phi-3-mini-4k-instruct": 1066,
        "llama-2-13b-chat": 1063,
        "meta-llama-3.2-1b-instruct": 1054,
        "zephyr-7b-beta": 1053,
        "llama-2-7b-chat": 1037,
        "mistral-7b-instruct-v0.1": 1008,
        "llama-13b": 799,
    }
}
