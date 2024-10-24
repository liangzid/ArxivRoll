"""
======================================================================
SEARCHBYTITLE --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 22 October 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

import faiss


def findSimCross(query_embeds, cand_embeds, topk):
    """
    the term `Cross` denotes that the user will provide two parameters,
    the query and the candidates.
    """
    # WARN: NO UNIT TEST

    # normalize all vectors
    faiss.normalize_L2(query_embeds)
    faiss.normalize_L2(cand_embeds)

    numq, d = query_embeds.shape
    numc, dc = cand_embeds.shape
    assert dc == d
    # print(num,d)

    # make index
    anns_idxes = faiss.IndexFlatIP(d)
    anns_idxes.add(cand_embeds)

    Distances, Indexes = anns_idxes.search(
        query_embeds, topk)

    print("Distance: ", Distances)
    print("Indexes: ", Indexes)

    # Indexls = Indexes[0]
    return Indexes


def findSim(idx, embedls, topk):
    # normalize all vectors
    faiss.normalize_L2(embedls)

    num, d = embedls.shape
    # print(num,d)

    # make index
    anns_idxes = faiss.IndexFlatIP(d)
    anns_idxes.add(embedls)

    query = embedls[idx:idx+1]

    Distances, Indexes = anns_idxes.search(query, topk)

    print("Distance: ", Distances)
    print("Indexes: ", Indexes)

    Indexls = Indexes[0]
    return Indexls


def main():
    from Vectorize import getEmbed
    text1 = "This is the first document."
    text2 = "This is the second document."
    text3 = "Hello world. This is the third document."
    text4 = "Anyway This THis This This is the last document."

    embeds = getEmbed([text1, text2, text3, text4])
    # print(embeds)
    # print(type(embeds))

    idxes = findSim(0, embeds, 4)


# running entry
if __name__ == "__main__":
    main()
    print("EVERYTHING DONE.")
