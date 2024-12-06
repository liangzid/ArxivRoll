"""
======================================================================
POST_PROCESS_PAPER_TEXT ---

Post process the text of the paper.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 24 October 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict, Optional
import random
from pprint import pprint as ppp
# import pickle
# import os
# from os.path import join, exists
# from collections import Counter,OrderedDict
# from bisect import bisect
# from copy import deepcopy

from data.INSTRUCTION import INSTRUCTION

from collections import OrderedDict

def paper2fragments(
        papertext: str,
        n_gram=1,
        minimal_char=80,
) -> List[str]:
    """transform a paper text into several paragraphs"""
    # WARN: NO UNIT TEST
    papercontent = extract_document_content(papertext)
    paragraphs = context_cutter(papercontent)
    '''
        ### Change the paragraphs spliting, by '\n\n'
            and only keep the \begin to \end part into one gram
            
            By Yang
    '''
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

def extract_document_content(papertext:str ) -> str:
    start_tag = r"\begin{document}"
    end_tag = r"\end{document}"
    
    start_index = papertext.find(start_tag)
    end_index = papertext.find(end_tag)
    
    if start_index != -1 and end_index != -1:
        # Include the length of the end_tag to capture the entire section
        return papertext[start_index + len(start_tag):end_index]
    else:
        return papertext
    
def context_cutter(papercontent:str) -> List[str]:
    grams = []
    gram = ""
    start_index = 0
    end_index = 0
    probmode = "None"
    begins_count = 0
    problength = 8
    while end_index + problength <= len(papercontent):
        if (papercontent[end_index] == r"%")&(probmode != "hanged"):
            originalmode = probmode
            probmode = "hanged"
            if (gram != ""):
                grams.append(gram)
            gram = ""
            end_index += 1
            start_index = end_index
            end_index += 1
            continue
        if (papercontent[end_index] == "\n"):
            if (probmode == "None"):
                probmode = "newline_ready"
                gram += papercontent[start_index:end_index]
                start_index = end_index
                end_index += 1
                continue
            if (probmode == "hanged"):
                probmode = originalmode
                end_index += 1
                start_index = end_index
                continue
        if probmode == "newline_ready":
            if (papercontent[end_index] in (" ", "\t")):
                start_index += 1
                end_index += 1
                continue
            if (papercontent[end_index] == "\n")|(end_index + problength == len(papercontent)):
                if (gram != ""):
                    grams.append(gram)
                gram = ""
                end_index += 1
                start_index = end_index
                continue
            else:
                probmode = "None"
                end_index += 1
                continue
        if papercontent[end_index:end_index+len(r"\begin{")] == r"\begin{":
            begins_count += 1
            probmode = "begin"
            end_index += len(r"\begin{")
            continue
        if papercontent[end_index:end_index+len(r"\end{")] == r"\end{":
            begins_count -= 1
            if begins_count <= 0:
                probmode = "None"
                begins_count = 0
            end_index += len(r"\end{")
            continue
        end_index += 1
    return grams
    
    
if __name__ == "__main__":
    # --- this is a test of p2f
    
    from_pth = "./past_one_months_cache/overaltex.json"
    with open(from_pth,
              'r', encoding='utf8') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    test_paper = data[random.randint(1,100)]
    test_paper = paper2fragments(test_paper, n_gram=5, minimal_char=300)
    for i in range(20,40):
        print(f'Fragment-{i}:')
        print(test_paper[i:i+1])
        
    print('Every thing is done')