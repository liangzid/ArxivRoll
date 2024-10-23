"""
======================================================================
CONSTRUCTOR ---

Constructing Test Cases Automatically Based On the Arxiv Articles.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 22 October 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
from SearchBySomething import findSim
from Vectorize import getEmbed

import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
from collections import OrderedDict

METHOD_LS = [
    "byTitle",
    "byAbs",
    "byKWls",
    "byText",
]
EMBED_METHOD = [
    "tfidf",
    "bert-large",
]


def intersect(lss: List[List[int]]):
    intersection = set.intersection(*map(set, lss))
    return list(intersection)


def retrievalSimIndexes(pool_path: str, filters=["byText"],
                        TopK=3,
                        temp_index_save_path=None,
                        embed_method="tfidf",
                        ):
    with open(pool_path, 'r', encoding='utf8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    titlels = data["title"]
    absls = data["abstract"]
    kwls = data["keywords"]
    textls = data["text"]

    embed_titlels = getEmbed(textls=titlels, method=embed_method)
    embed_absls = getEmbed(absls, embed_method)
    embed_kwls = getEmbed(kwls, embed_method)
    embed_textls = getEmbed(textls, embed_method)

    assert embed_method in EMBED_METHOD

    numCand = TopK*20

    assert filters != []
    for x in filters:
        assert x in METHOD_LS

    retrieval_candidate_dict = {}
    for i in range(len(titlels)):

        candidx_title = []
        candidx_abs = []
        candidx_kw = []
        candidx_text = []

        if "byTitle" in filters:
            candidx_title = findSim(i, embed_titlels, numCand)
        if "byAbs" in filters:
            candidx_abs = findSim(i, embed_absls, numCand)
        if "byKWls" in filters:
            candidx_kw = findSim(i, embed_kwls, numCand)
        if "byText" in filters:
            candidx_text = findSim(i, embed_textls, numCand)

        # intersect operation
        final_cand_idxls = intersect(
            [
                candidx_title,
                candidx_abs,
                candidx_kw,
                candidx_text,
            ]
        )

        # filter the current index.
        final_cand_idxls1 = []
        for idx in final_cand_idxls:
            if idx == i:
                pass
            else:
                final_cand_idxls1.append(idx)

        assert len(final_cand_idxls1) >= TopK

        retrieval_candidate_dict[i] = final_cand_idxls1

    if temp_index_save_path is None:
        temp_index_save_path = pool_path+"-----save_index.json"

    with open(temp_index_save_path, 'w', encoding='utf8') as f:
        json.dump(retrieval_candidate_dict,
                  f, ensure_ascii=False, indent=4)
    print(f"Save DONE. Save to {temp_index_save_path}.")
    return data, retrieval_candidate_dict


# running entry
if __name__ == "__main__":
    # main()
    print("EVERYTHING DONE.")
