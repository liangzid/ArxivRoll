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
from SearchBySomething import findSim, findSimCross
from Vectorize import getEmbed
from post_process_paper_text import paper2fragments as p2f
from utils import random_take_one
from utils import constructTestCase

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


def retrievalFragments(
        papers4Q,
        papers4C,
        save_path,
        topk=3,
        embed_method="tfidf",
):
    """
    Given the papers used for query and the papers used for candidates,
    the author will use them to create test cases.
    """
    n_gram = 1
    minimal_char = 80
    query_fragss = [p2f(x, n_gram, minimal_char)
                    for x in papers4Q]
    cand_fragss = [p2f(x, n_gram, minimal_char)
                   for x in papers4C]
    query_frags = [random_take_one(x, no_first=True)
                   for x in query_fragss]
    query_idxs, query_frags = zip(*query_frags)
    cand_frags = []
    for x in cand_fragss:
        cand_frags.extend(x)

    # Step 1: Begin the search process.

    q_frags_embeds = getEmbed(query_frags, embed_method)
    c_frags_embeds = getEmbed(cand_frags, embed_method)

    candidate_idx = findSimCross(
        q_frags_embeds,
        c_frags_embeds,
        topk,
    )

    # Step 2: Construct the test process
    test_case_ls = []
    for i in range(len(query_frags)):
        context = query_fragss[i][query_idxs[i-1]]
        true_ans = query_frags[i]
        false_idx = candidate_idx[i]
        false_anss = []
        for fidx in false_idx:
            acand = cand_frags[fidx]
            false_anss.append(acand)

        testCase = constructTestCase(
            context,
            true_ans,
            false_anss,
        )
        test_case_ls.append(testCase)

    # Step 3: save the task
    with open(save_path,
              'w', encoding='utf8') as f:
        json.dump(test_case_ls,
                  f, ensure_ascii=False, indent=4)
    return test_case_ls


def retrievalFragments2Myself(
        papers4Q,
        save_path,
        topk=3,
        embed_method="tfidf",
):
    """
    Retrieval within the articles.
    """
    n_gram = 1
    minimal_char = 80
    query_fragss = [p2f(x, n_gram, minimal_char)
                    for x in papers4Q]

    # filter the empty papers.
    new_query_fragss = []
    # print(f"Min length in the list: {min([len(x) for x in query_fragss])}")
    for i, x in enumerate(query_fragss):
        if len(x) <= 2:
            pass
            # print(papers4Q[i])
            # print(query_fragss[i])
            # print("================================================")
        else:
            new_query_fragss.append(query_fragss[i])
    query_fragss = new_query_fragss
    # print(query_fragss[0])
    query_frags = [random_take_one(x, no_first=True)
                   for x in query_fragss]
    query_idxs, query_frags = zip(*query_frags)

    # Step 1: Begin the search process.

    # Step 2: Construct the test process
    test_case_ls = []
    for i in range(len(query_frags)):
        query_idx = query_idxs[i]
        q_frags_embeds = getEmbed(
            query_fragss[i],
            embed_method)
        sim_idxes = findSim(
            query_idx,
            q_frags_embeds,
            topk=topk+1,
        )
        # print(f"query index: {query_idxs[i]}")
        # print(f"length of query_fraggs[i]: {len(query_fragss[i])}")
        context = query_fragss[i][query_idxs[i]-1]
        true_ans = query_frags[i]
        false_idx = sim_idxes
        false_anss = []
        for fidx in false_idx:
            if fidx == query_idx:
                continue
            acand = query_fragss[i][fidx]
            false_anss.append(acand)

        testCase = constructTestCase(
            context,
            true_ans,
            false_anss,
        )
        test_case_ls.append(testCase)

    # Step 3: save the task
    with open(save_path,
              'w', encoding='utf8') as f:
        json.dump(test_case_ls,
                  f, ensure_ascii=False, indent=4)
    print(f"Test Cases Save DONE. Save to {save_path}.")
    return test_case_ls


def intersect(lss: List[List[int]]):
    intersection = set.intersection(*map(set, lss))
    return list(intersection)


def retrievalSimIndexes(
    pool_path: str,
    filters=["byText"],
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
