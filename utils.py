"""
======================================================================
UTILS ---

Some easy-to-used tools.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 24 October 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
# import json
# from typing import List, Tuple, Dict
import random
# from pprint import pprint as ppp

from data.INSTRUCTION import INSTRUCTION


def random_take_one(
        ls,
        no_first=False,
        no_end=False,
):
    assert len(ls) != 0

    if no_first or no_end:
        assert len(ls) > 1
    if no_first and no_end:
        assert len(ls) > 2

    bg_idx = 0 if not no_first else 1
    ed_idx = len(ls)-1 if not no_end else len(ls)-2

    idx = random.randint(bg_idx, ed_idx)
    return idx, ls[idx]


def constructTestCase(
        context,
        true_answer,
        false_answers,
        instruction=None,
) -> (str, str):

    if instruction is None:
        instruction = INSTRUCTION

    # 1. shuffle the choices

    choices = false_answers
    choices.append(true_answer)
    random.shuffle(choices)

    # find the index.
    label_idx = -1
    for i, x in enumerate(choices):
        if x == true_answer:
            label_idx = i
            break
    assert label_idx != -1

    idx_Selection_map = {
        0: "A", 1: "B", 2: "C", 3: "D",
    }

    text_label = idx_Selection_map[label_idx]

    # 2. Serialization
    Input = f"## Instruction:\n{INSTRUCTION}\n## Context:\n {context}\n## Choice:\n**A** {choices[0]}\n**B** {choices[1]}\n**C** {choices[2]}\n**D** {choices[3]}"

    return Input, text_label
