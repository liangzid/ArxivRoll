"""
======================================================================
1.RUN_VANILLA_CONSTRUCT ---

Vanilla version of test cases generation.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 24 October 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
from collections import OrderedDict


from constructor import retrievalFragments
from constructor import retrievalFragments2Myself
from constructor import push2HF


def main1():
    """
    the first main function for the construction of the retrieval.
    """

    # TARGET: test the effecacy of the CASES of self-contained choices
    # that is, the =false choice= comes from the same paper from the
    # correct answers.

    # # Step 1: Load papers from the SPIDERED FILE.

    # from_pth = "./recent_save_articles.json"
    # with open(from_pth,
    #           'r', encoding='utf8') as f:
    #     data = json.load(f, object_pairs_hook=OrderedDict)
    # papers = data["text"]
    # print(f"All paper Number: {len(papers)}")

    # cases = retrievalFragments2Myself(
    #     papers4Q=papers,
    #     structure_data_save_path="testcases_pastonemonths.jsonl",
    #     save_path="test_cases_for_past_one_monthss_papers.json",
    #     topk=3,
    #     embed_method="tfidf",
    # )

    # print(cases[-1])

    # Step 2: Push to Huggingface.
    testcase_path="testcases_pastonemonths.jsonl"
    push2HF(testcase_path)


if __name__ == "__main__":
    main1()
