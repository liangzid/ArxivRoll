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
from constructor import constructBenchmarksSCP


def test_Latex():
    from_pth = "./past_one_months_cache/overaltex.json"
    with open(from_pth,
              'r', encoding='utf8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    papers = data
    print(f"All paper Number: {len(papers)}")

    cases = retrievalFragments2Myself(
        papers4Q=papers,
        structure_data_save_path_type2="latex_testcases_pastonemonthsTYPE2.jsonl",
        structure_data_save_path="latex_testcases_pastonemonths.jsonl",
        save_path="latex_test_cases_for_past_one_monthss_papers.json",
        topk=3,
        embed_method="tfidf",
    )

    # Step 2: Push to Huggingface.
    testcase_path = "latex_testcases_pastonemonthsTYPE2.jsonl"
    push2HF(testcase_path, name="robench_2024b-test-latex-P")


def test_SCP_S():
    # Step 1: Load papers from the SPIDERED FILE.
    from_pth = "./recent_save_articles.json"
    with open(from_pth,
              'r', encoding='utf8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    papers = data["text"]
    print(f"All paper Number: {len(papers)}")
    
    # from_pth = "./past_one_months_cache/overaltex.json"
    # with open(from_pth,
    #           'r', encoding='utf8') as f:
    #     data = json.load(f, object_pairs_hook=OrderedDict)
    # papers = data
    # print(f"All paper Number: {len(papers)}")

    # # ---------------------------------------------------------------
    # cases = constructBenchmarksSCP(
    #     papers,
    #     hf_style_save_path="past_one_month_latex_hf_SCP_s.jsonl",
    #     scp_type="s",
    #     n_gram=2,
    #     minimal_char=250,
    #     )

    # # Step 2: Push to Huggingface.
    # testcase_path = "past_one_month_latex_hf_SCP_s.jsonl"
    # push2HF(testcase_path, name="robench_2024b-test-scp-s")

    # ---------------------------------------------------------------
    cases = constructBenchmarksSCP(
        papers,
        hf_style_save_path="past_one_month_latex_hf_SCP_c.jsonl",
        scp_type="c",
        n_gram=5,
        minimal_char=400,
        )

    # Step 2: Push to Huggingface.
    testcase_path = "past_one_month_latex_hf_SCP_c.jsonl"
    push2HF(testcase_path, name="robench_2024b-test-scp-c")

    # # ---------------------------------------------------------------
    # cases = constructBenchmarksSCP(
    #     papers,
    #     hf_style_save_path="past_one_month_latex_hf_SCP_p.jsonl",
    #     scp_type="p",
    #     n_gram=1,
    #     minimal_char=100,
    #     )

    # # Step 2: Push to Huggingface.
    # testcase_path = "past_one_month_latex_hf_SCP_p.jsonl"
    # push2HF(testcase_path, name="robench_2024b-test-scp-p")
    # # ---------------------------------------------------------------

    pass


def main_old():
    """
    the first main function for the construction of the retrieval.
    """

    # TARGET: test the effecacy of the CASES of self-contained choices
    # that is, the =false choice= comes from the same paper from the
    # correct answers.

    # Step 1: Load papers from the SPIDERED FILE.

    from_pth = "./recent_save_articles.json"
    with open(from_pth,
              'r', encoding='utf8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    papers = data["text"]
    print(f"All paper Number: {len(papers)}")

    cases = retrievalFragments2Myself(
        papers4Q=papers,
        structure_data_save_path_type2="testcases_pastonemonthsTYPE2.jsonl",
        structure_data_save_path="testcases_pastonemonths.jsonl",
        save_path="test_cases_for_past_one_monthss_papers.json",
        topk=3,
        embed_method="tfidf",
    )

    # Step 2: Push to Huggingface.
    testcase_path = "testcases_pastonemonthsTYPE2.jsonl"
    push2HF(testcase_path, name="robench_2024b-testII")


if __name__ == "__main__":
    # main_old()
    # test_Latex()
    test_SCP_S()
