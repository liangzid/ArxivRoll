"""
======================================================================
POST_PROCESS_PAPER_TEXT ---

Post process the text of the paper.

    Author: XXXXXX <xxxxxx@xxxxxx>
    Copyright © 2024, XXXXXX, all rights reserved.
    Created: 24 October 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
# import pickle
# import os
# from os.path import join, exists
# from collections import Counter,OrderedDict
# from bisect import bisect
# from copy import deepcopy

from data.INSTRUCTION import INSTRUCTION


def paper2fragments(
        papertext: str,
        n_gram=1,
        minimal_char=80,
) -> List[str]:
    """transform a paper text into several paragraphs"""
    # WARN: NO UNIT TEST

    paragraphs = papertext.split("\n")
    para_ls = []
    for i in range(len(paragraphs)//n_gram-1):
        sub_candidates = paragraphs[i*n_gram:(i+1)*n_gram]
        para_text = "\n".join(sub_candidates)
        # print("Para Text: {}".format(para_text))
        if len(para_text) < minimal_char:
            pass
        else:
            para_ls.append(para_text)
    return para_ls
