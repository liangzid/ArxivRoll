"""
======================================================================
SCP ---

Functions of how we construct test cases.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created:  7 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict, Optional
import random
from pprint import pprint as ppp
import numpy as np
import math

from post_process_paper_text import paper2fragments as p2f
from utils import random_take_one
from Vectorize import getEmbed
from SearchBySomething import findSim
from utils import constructTestCase
from utils import constructSequencingTestCase
from utils import constructClozeTestCase


def SCP(
        paper: str, scp_type: str,
        n_gram=1, minimal_char=80,
) -> Optional[Dict[str, str], None]:
    """
    ------------------------------------------------------------------
    core function to generate test cases from a paper string.
    ------------------------------------------------------------------
    paper: a string of the arxiv paper.
    scp_type: s, c, or p.
    ------------------------------------------------------------------
    return: a selection dict like:
    ```python
        {
            "context": context,
            "A": choices[0],
            "B": choices[1],
            "C": choices[2],
            "D": choices[3],
            "label": text_label,
        }
    ```
    ------------------------------------------------------------------
    """
    assert scp_type in ["s", "c", "p"]

    # 1. split paper into fragments
    query_frags = p2f(paper, n_gram, minimal_char)

    if len(query_frags) <= 4:
        return None

    # 2. first select a fragment
    idx, gram = selectFragment(query_frags)

    # 3. then do SCP
    testCase = None
    if scp_type == "s":
        num_rerank_parts = 3
        split_symbol = ". "

        # now split `num_rerank_parts` for the `gram`.
        gram_sents = gram.split(split_symbol)
        if len(gram_sents) < num_rerank_parts:
            return None
        constructed_grams = []
        sent_num = math.floor(len(gram_sents)/num_rerank_parts)
        for i_idx in range(num_rerank_parts-1):
            constructed_grams.append(
                split_symbol.join(
                    gram_sents[sent_num*i_idx:sent_num*(i_idx+1)])
            )
        constructed_grams.append(
            split_symbol.join(gram_sents[sent_num*(num_rerank_parts-1):])
        )
        assert len(constructed_grams) == num_rerank_parts
        # then rerank it.
        shuffled_idx = list(range(num_rerank_parts))
        random.shuffle(shuffled_idx)

        testCase = constructSequencingTestCase(
            shuffled_idx,
            constructed_grams,
        )
    elif scp_type == "c":
        num_cloze = 3
        split_symbol = ". "

        # first split into several sub-sentences
        gram_sents = gram.split(split_symbol)
        if len(gram_sents) < num_rerank_parts:
            return None
        selected_idxes = np.random.choice(
            list(range(len(gram_sents))),
            num_cloze,
            replace=False,
        )
        testCase = constructClozeTestCase(
            selected_idxes,
            gram_sents,
        )
    elif scp_type == "p":
        embed_method = "tfidf"
        q_embeds = getEmbed(
            query_frags,
            embed_method)
        sim_idxes = findSim(
            idx, q_embeds, topk=4,
        )
        context = query_frags[idx-1]
        true_ans = query_frags[idx]
        false_anss = []
        for fidx in sim_idxes:
            if fidx == idx:
                continue
            false_cand = query_frags[fidx]
            false_anss.append(false_cand)
        testCase = constructTestCase(
            context,
            true_ans,
            false_anss,
            if_strucutured=True
        )
    else:
        return None
    return testCase


def selectFragment(frags: List[str]):
    return random_take_one(frags, no_first=True)
