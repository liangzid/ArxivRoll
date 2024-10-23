"""
======================================================================
VECTORIZE ---

Transform a list of texts into a list of representations.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 22 October 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def getEmbed(textls, method="tfidf"):

    if method=="tfidf":
        vectors = TfidfVectorizer().fit_transform(textls)
    elif method=="bert-large":
        vectors = TfidfVectorizer().fit_transform(textls)
        pass

    return vectors

def _test_tfidf():
    text1="This is the first document."
    text2="This is the second document."

    vectorizer=TfidfVectorizer().fit_transform([text1,text2])
    cosine_sim=cosine_similarity(vectorizer[0:1],vectorizer[1:2])
    print(f"Cosine Similarity: {cosine_sim}")

# running entry
if __name__ == "__main__":
    # main()
    _test_tfidf()
    print("EVERYTHING DONE.")
