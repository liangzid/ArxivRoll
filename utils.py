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
from typing import List, Tuple, Dict
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


def constructClozeTestCase(
        selected_idxes: List[int],
        grams: List[str],
) -> Dict[str, str]:

    text_with_holes = ""
    masked_symbol = " <|MaskedSetence|> "
    for i, gram in enumerate(grams):
        if i not in selected_idxes:
            text_with_holes += gram + ". "
        else:
            text_with_holes += masked_symbol

    text_candidates = ""
    idx_Letter_map = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
    }
    for i, idx in enumerate(selected_idxes):
        text_candidates += f"**{idx_Letter_map[i]}**: {grams[idx]}. \n"

    correct_ans = ""
    sorted_idxes_indesls = get_sorted_indices(selected_idxes)
    for idx in sorted_idxes_indesls:
        correct_ans += idx_Letter_map[idx]
    I = 10000
    distractor1 = correct_ans
    distractor2 = correct_ans
    distractor3 = correct_ans
    # random generate three distractors.
    newshuffled_idx = list(range(len(selected_idxes)))
    i = 0
    while distractor1 == correct_ans and i < I:
        random.shuffle(newshuffled_idx)
        distractor1 = "".join([idx_Letter_map[x] for x in newshuffled_idx])
        i += 1
    newshuffled_idx = list(range(len(selected_idxes)))
    i = 0
    while distractor2 == correct_ans and i < I:
        random.shuffle(newshuffled_idx)
        distractor1 = "".join([idx_Letter_map[x] for x in newshuffled_idx])
        i += 1
    newshuffled_idx = list(range(len(selected_idxes)))
    i = 0
    while distractor3 == correct_ans and i < I:
        random.shuffle(newshuffled_idx)
        distractor1 = "".join([idx_Letter_map[x] for x in newshuffled_idx])
        i += 1

    # finally shuffle the selections:
    choices = [correct_ans, distractor1, distractor2, distractor3]
    choices_shuffledidx = list(range(4))
    random.shuffle(choices_shuffledidx)
    label_idx = -1
    for i, x in enumerate(choices_shuffledidx):
        if x == 0:
            label_idx = i
    return {
        "text_with_holes": text_with_holes,
        "text_candidates": text_candidates,
        "A": choices[choices_shuffledidx[0]],
        "B": choices[choices_shuffledidx[1]],
        "C": choices[choices_shuffledidx[2]],
        "D": choices[choices_shuffledidx[3]],
        "label": f"Selection {label_idx+1}",
    }


def get_sorted_indices(arr):
    indexed_list = list(enumerate(arr))
    indexed_list.sort(key=lambda x: x[1])
    sorted_indices = [index for index, value in indexed_list]
    return sorted_indices


def constructSequencingTestCase(
        shuffled_idx: List[int],
        grams: List[str],
) -> Dict[str, str]:

    idx_Letter_map = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
    }

    # serialize of the `Input`:
    overall_text = ""
    for i, idx in enumerate(shuffled_idx):
        overall_text += f"**{idx_Letter_map[i]}**: " +\
            f"{grams[idx]}"
    correct_ans = ""
    for idx in shuffled_idx:
        correct_ans += idx_Letter_map[idx]

    I = 10000
    distractor1 = correct_ans
    distractor2 = correct_ans
    distractor3 = correct_ans
    # random generate three distractors.
    newshuffled_idx = list(range(len(shuffled_idx)))
    i = 0
    while distractor1 == correct_ans and i < I:
        random.shuffle(newshuffled_idx)
        distractor1 = "".join([idx_Letter_map[x] for x in newshuffled_idx])
        i += 1
    i = 0
    while distractor2 == correct_ans and i < I:
        random.shuffle(newshuffled_idx)
        distractor2 = "".join([idx_Letter_map[x] for x in newshuffled_idx])
        i += 1
    i = 0
    while distractor3 == correct_ans and i < I:
        random.shuffle(newshuffled_idx)
        distractor3 = "".join([idx_Letter_map[x] for x in newshuffled_idx])
        i += 1

    # finally shuffle the selections:
    choices = [correct_ans, distractor1, distractor2, distractor3]
    random.shuffle(choices)

    labells = ["Selection 1", "Selection 2", "Selection 3", "Selection 4",]

    label_idx = -1
    for i, x in enumerate(choices):
        if x == correct_ans:
            label_idx = i
    return {
        "shuffled_text": overall_text,
        "A": choices[0],
        "B": choices[1],
        "C": choices[2],
        "D": choices[3],
        "label": labells[label_idx],
    }
