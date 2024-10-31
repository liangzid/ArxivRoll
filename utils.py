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
import re
import random
# from pprint import pprint as ppp

from data.INSTRUCTION import INSTRUCTION


def notMath(text: str):
    SEN_FREQUENCY = 5

    sen_words = [
        "italic",
        "SUBSCRIPT", "SUPERSCRIPT",
        "subscript",
        "_", "=", "+", "*", "∘", "\\", "^", "|",
        "λ", "ρ⁢", "⁢∑", "ϑ", "𝑥", "Ω⁢",
        ]

    for sw in sen_words:
        # count = len(re.findall(sw, text))
        count = text.count(sw)
        if count >= SEN_FREQUENCY:
            return False
    return True


def otherFilters(text: str):
    if re.search(r"^Figure \d+:*", text) is not None:
        return False
    if re.search(r"^[a-z]", text) is not None:
        return False
    return True


def random_take_one(
        ls,
        no_first=False,
        no_end=False,
        filter_math=True,
):
    assert len(ls) != 0

    if no_first or no_end:
        assert len(ls) > 1
    if no_first and no_end:
        assert len(ls) > 2

    bg_idx = 0 if not no_first else 1
    ed_idx = len(ls)-1 if not no_end else len(ls)-2

    if not filter_math:
        idx = random.randint(bg_idx, ed_idx)
    else:
        count = 0
        while count < 10000:
            count += 1
            idx = random.randint(bg_idx, ed_idx)
            if notMath(ls[idx]) and notMath(ls[idx]) \
               and otherFilters(ls[idx]) and otherFilters(ls[idx-1]):
                break

    return idx, ls[idx]


def constructTestCase(
        context,
        true_answer,
        false_answers,
        instruction=None,
        if_strucutured=False,
) -> (str, str):

    if instruction is None:
        instruction = INSTRUCTION

    # 1. shuffle the choices

    choices = false_answers[:3]
    choices.append(true_answer)
    random.shuffle(choices)

    # print("--------------------------------------------------------")
    # print(len(false_answers))
    # print(len(choices))

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

    if not if_strucutured:
        # 2. Serialization
        Input = f"## Instruction:\n{INSTRUCTION}\n## Context:\n {context}\n## Choice:\n**A** {choices[0]}\n**B** {choices[1]}\n**C** {choices[2]}\n**D** {choices[3]}"

        return Input, text_label
    else:
        return {
            "context": context,
            "A": choices[0],
            "B": choices[1],
            "C": choices[2],
            "D": choices[3],
            "label": text_label,
        }
