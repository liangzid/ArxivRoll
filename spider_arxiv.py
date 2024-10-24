"""
======================================================================
SPIDER_ARXIV ---

Parse the ArXiv Documents.



    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 21 October 2024
======================================================================
"""

"""
                      Assert by the author: 
You MUST obey the requirements of Arxiv.org, when you use this code.
See the following urls for more details:

https://info.arxiv.org/help/api/tou.html

I copy them here:

Rate limits

Please note that the following rate limits apply to all of the machines
 under your control as a whole. You should not attempt to overcome these
 limits by increasing the number of machines used to make requests. If
your use-case requires a higher request rate, please contact our support
 team.

When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API),
make no more than one request every three seconds, and limit requests
to a single connection at a time. These limits may change in the future.

Things that you can (and should!) do

+ Retrieve, store, transform, and share descriptive metadata about arXiv e-prints.
+ Retrieve, store, and use the content of arXiv e-prints for your own personal use, or for research purposes.
+ Provide tools and services to users that helps them to discover or be notified about arXiv e-prints. For example:
+ A better search interface;
+ A mobile app that notifies users about e-prints that might be of interest to them;
+ A visualization of topics in arXiv e-prints over time;
+ A citation graph using bibliographic references from e-prints.
+ Build other kinds of interfaces that help users to interact with arXiv in new and useful ways, leveraging our APIs.
+ Direct users to arXiv.org to retrieve e-print content (PDF, source files, etc). We encourage you to link to the abstract page.

Things that you must not do

+ Store and serve arXiv e-prints (PDFs, source files, or other content)
from your servers, unless you have the permission of the copyright holder
or are permitted to do so by the license with which the e-print was submitted.
Note that a very small subset of arXiv e-prints are submitted with licenses
that permit redistribution.
+ Represent your project as endorsed or supported by arXiv.org without
our permission.
+ Attempt to circumvent rate limits.
+ Use someone else’s credentials to access arXiv APIs.
"""

# ------------------------ Code --------------------------------------

# normal import


from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import time
import datetime as dt
from bs4 import BeautifulSoup
import requests
from pprint import pprint as ppp
import random
from typing import List, Tuple, Dict
import json
from tqdm import tqdm
import fake_useragent # pip install fake-useragent
from fake_useragent import UserAgent
ARXIV_TAXONOMY_URL = "https://arxiv.org/category_taxonomy"

# List of ArXiv subject classifications (sets) with comments
ARXIV_CAT_SETS = [
    # Physics
    "physics:astro-ph",  # Astrophysics
    "physics:atom-ph",   # Atomic Physics
    # Computational Linguistics (Note: This is interdisciplinary)
    "physics:cmp-lg",
    "physics:cond-mat",  # Condensed Matter Physics
    "physics:data-an",   # Data Analysis, Statistics and Probability
    "physics:fluid-dyn",  # Fluid Dynamics
    "physics:gen-ph",    # General Physics
    "physics:gr-qc",     # General Relativity and Quantum Cosmology
    "physics:h-atom",    # History and Philosophy of Physics
    "physics:hep-ex",    # High Energy Physics - Experiment
    "physics:hep-lat",   # High Energy Physics - Lattice
    "physics:hep-ph",    # High Energy Physics - Phenomenology
    "physics:hep-th",    # High Energy Physics - Theory
    "physics:inst-ph",   # Instrumentation and Detectors
    "physics:math-ph",   # Mathematical Physics
    "physics:med-ph",    # Medical Physics
    "physics:nlin",      # Nonlinear Sciences
    "physics:optics",    # Optics
    "physics:pacs-cs",   # Physical and Chemical Systems at Surfaces and Interfaces
    "physics:plasm-ph",  # Plasma Physics
    "physics:pop-ph",    # Popular Physics
    "physics:quant-ph",  # Quantum Physics
    # Physics and Society (Note: This is interdisciplinary)
    "physics:soc-ph",
    "physics:stat-mech",  # Statistical Mechanics
    "physics:supr-con",  # Superconductivity

    # Mathematics
    "math:ag",           # Algebraic Geometry
    "math:ap",           # Analysis of PDEs
    "math:at",           # Algebraic Topology
    "math:ca",           # Category Theory
    "math:cg",           # Geometric Topology
    "math:co",           # Combinatorics
    "math:ct",           # Category Theory
    "math:cv",           # Complex Variables
    "math:dg",           # Differential Geometry
    "math:ds",           # Dynamical Systems
    "math:fa",           # Functional Analysis
    "math:gm",           # General Mathematics
    "math:gn",           # General Topology
    "math:gt",           # Geometric Topology
    "math:ho",           # History and Overview
    "math:it",           # Information Theory
    "math:kt",           # K-Theory and Homology
    "math:lo",           # Logic
    "math:mg",           # Metric Geometry
    "math:mp",           # Mathematical Physics
    "math:na",           # Numerical Analysis
    "math:nt",           # Number Theory
    "math:oa",           # Operator Algebras
    "math:oc",           # Optimization and Control
    "math:pr",           # Probability
    "math:qa",           # Quantum Algebra
    "math:rt",           # Representation Theory
    "math:sg",           # Symplectic Geometry
    "math:sp",           # Spectral Theory
    "math:st",           # Statistics Theory

    # Computer Science
    # Note: Computer Science classifications may be more specific,
    # and some may overlap with interdisciplinary sets like "physics:cmp-lg"
    "cs:ai",             # Artificial Intelligence
    "cs:cc",             # Computational Complexity
    "cs:cg",             # Computational Geometry
    "cs:cl",             # Computation and Language
    "cs:cr",             # Cryptography and Security
    "cs:cv",             # Computer Vision and Pattern Recognition
    "cs:db",             # Databases
    "cs:dc",             # Discrete Mathematics
    "cs:dl",             # Digital Libraries
    "cs:dm",             # Discrete Mathematics
    "cs:ds",             # Data Structures and Algorithms
    "cs:et",             # Emerging Technologies
    "cs:fl",             # Formal Languages and Automata Theory
    "cs:gl",             # General Literature
    "cs:gr",             # Graphics
    "cs:hc",             # Human-Computer Interaction
    "cs:ir",             # Information Retrieval
    "cs:it",             # Information Theory
    "cs:lg",             # Learning
    "cs:lo",             # Logic in Computer Science
    "cs:ma",             # Multiagent Systems
    "cs:mm",             # Multimedia
    "cs:ms",             # Mathematical Software
    "cs:ne",             # Neural and Evolutionary Computing
    "cs:ni",             # Networking and Internet Architecture
    "cs:oh",             # Other Computer Science
    "cs:os",             # Operating Systems
    "cs:pl",             # Programming Languages
    "cs:ro",             # Robotics
    "cs:sc",             # Symbolic Computation
    "cs:sd",             # Software Engineering
    "cs:si",             # Social and Information Networks
    "cs:sy",             # Systems and Control

    # Other interdisciplinary sets may also exist
]


def termOfUse():
    # sleep three seconds to obey the term of use.
    time.sleep(10)


def getArxivIDs(
        term="Large Language Models",
        subject="cs",
        date_from="2024-09-01",
        date_to="2024-10-01",
        size=200,
):
    # url = f"https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term={term}&terms-0-field=all&classification-physics=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={date_from}&date-to_date={date_to}&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first"
    url = f"https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term={term}&terms-0-field=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date={date_from}&date-to_date={date_to}&date-date_type=submitted_date&abstracts=show&size={size}&order=-announced_date_first"

    ids = []
    try:
        source = requests.get(url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, "html.parser")
        papers = soup.find("ol", class_="breathe-horizontal")\
            .find_all("li", class_="arxiv-result")
        for paper in papers:
            title = paper.find("p", class_="title is-5 mathjax").text[8:-10]
            # abstract = paper.find("p",
            #                       class_="abstract mathjax")\
            #     .find("span",
            #           class_="abstract-full has-text-grey-dark mathjax").text[:-7]
            # author = paper.find("p", class_="authors")\
            #               .text[10:].replace(
            #     "\n", "").replace("    ", "")
            print(title)
            id_ = paper.find("p", class_="list-title is-inline-block").a.text
            id_ = paper.find("p", class_="list-title is-inline-block").a.text
            ids.append(id_)
    except Exception as e:
        print("Error {}".format(e))

    ids = [x.replace("arXiv:", "") for x in ids]
    print(f"parsed IDS: {ids}")
    return ids


def htmlSourceSpider(
        url,
        fmt="html",
        save_pth="./recent_papers",
):

    html = requests.get(url)

    print(html.text)


def queryArxiv(
        verb="ListRecords",
        metadataPrefix="arXiv",
        set_spec="cs",
        from_date=None,
        until_date=None,
):
    if from_date is None:
        from_date = (datetime.now() - timedelta(days=30)
                     ).strftime("%Y-%m-%d")
    if until_date is None:
        until_date = datetime.now().strftime("%Y-%m-%d")
    # Build the query string
    params = {
        'verb': verb,
        'metadataPrefix': metadataPrefix,
        'set': set_spec,
        'from': from_date,
        'until': until_date
    }

    print(f"Parameters: {params}.")

    ids = []

    # ArXiv OAI-PMH base URL
    oai_url = "http://export.arxiv.org/oai2"
    old_prefix_url = "http://www.openarchives.org/OAI/2.0/"
    PREFIX_URL = "http://arxiv.org/OAI/arXiv/"

    try:
        # Send the request
        response = requests.get(oai_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        # termOfUse()
        print(response.text)

        soup = BeautifulSoup(response.text, "xml",
                             # features="xml",
                             )

        records = soup.find("OAI-PMH").find("ListRecords").find_all("record")
        for record in tqdm(records):
            metadata = record.find("metadata")
            id_ = metadata.find("id").text
            title = metadata.find("title").text
            catgory = metadata.find("categories").text
            print("----------------------------------------")
            print(f"id: {id_}\ntitle:{title}\ncat:{catgory}")
            ids.append(id_)

        # # Parse the XML response
        # root = ET.fromstring(response.content)
        # print(root)
        # # Extract records
        # for record in tqdm(
        #         root.findall('.//{'+PREFIX_URL + '}record'),
        #         desc="Processing:",
        # ):
        #     header = record.find(
        #         './/{'+PREFIX_URL + '}header')
        #     identifier = header.find(
        #         './/{'+PREFIX_URL + '}identifier').text
        #     metadata = record.find(
        #         './/{'+PREFIX_URL + '}metadata/arxiv/arxiv-meta')
        #     title = metadata.find('.//title').text
        #     print(f"Title: {title}\nID: {identifier}\n")
        #     ids.append(identifier)
    except Exception as e:
        print(f"Error: {e}.")
    return ids


def downloadArxivViaIds(id_ls, save_path="./recent_save_articles.json"):
    ua = UserAgent()
    res_dict = {
        "title": [],
        "abstract": [],
        "keywords": [],
        "text": [],
    }
    total_num = len(id_ls)
    hit_num = 0
    for id_ in tqdm(id_ls):
        download_url = f"https://arxiv.org/html/{id_}"
        # "https://arxiv.org/html/2410.13825v1"
        try:
            source = requests.get(download_url,
                                  headers={
                                      "User-Agent": ua.random
                                  })
            source.raise_for_status()
            soup = BeautifulSoup(source.text, "html.parser")
            papers = soup.find("article", class_="ltx_document")
            title = papers.find(
                "h1", class_="ltx_title ltx_title_document")
            # print("raw titile:", title)
            title = title.text
            if '"' in title:
                title = title.split('"')[1]
            abstract = papers.find("div", class_="ltx_abstract",)\
                .find("p", class_="ltx_p")
            abstract = abstract.text
            # print("raw abstract:", abstract)
            if '"' in abstract:
                abstract = abstract.split('"')[1]
            keywords = papers.find("div", class_="ltx_keywords")
            if keywords is not None:
                # print("raw keyword:",keywords)
                keywords = keywords.text
                if '</button>' in keywords:
                    keywords = keywords.split("</button>")[1]
                    if '"' in keywords:
                        keywords = keywords.split('"')[1]
                if "; " in keywords:
                    keywords = keywords.split("; ")
                elif ", " in keywords:
                    keywords = keywords.split(", ")
                else:
                    keywords = [keywords]
            else:
                keywords = [""]

            maintextls = papers.find_all(
                "section",
                class_="ltx_section",
            )
            html_text = ""
            for maintext in maintextls:
                html_text += maintext.text

            # print("==================================================")
            # print(title)
            # print("==================================================")
            # print(abstract)
            # print("==================================================")
            # print(keywords)
            # print("==================================================")
            # print(html_text)
            # print("==================================================")

            res_dict["title"].append(title)
            res_dict["abstract"].append(abstract)
            res_dict["keywords"].append(keywords)
            res_dict["text"].append(html_text)
            hit_num += 1
        except Exception as e:
            print(f"Error: {e}.")
        termOfUse()

    with open(save_path, 'w', encoding='utf8') as f:
        json.dump(res_dict,
                  f, ensure_ascii=False, indent=4)
    print(
        f"NUMS THAT SUCCESSFULLLY SPIDERED: {hit_num}\nTOTAL NUM: {total_num}")
    print(f"Save DONE. Save to {save_path}.")


def main():
    # url = "https://arxiv.org/list/cs.AI/recent?skip=0&show=2000"
    # htmlSourceSpider(url)
    # ids = getArxivIDs()
    ids = queryArxiv(from_date="2024-09-01", until_date="2024-10-01")
    # ids = ids[:100]
    print(f"IDs: {ids}")
    downloadArxivViaIds(ids, save_path="./recent_save_articles.json")


def main2():
    print("Spider the corpus of the past ONE year.")
    ids = []
    for i in range(4, 11):
        temp_ids = queryArxiv(
            from_date=f"2024-0{i}-01",
            until_date="2024-0{i}-30")
        ids.extend(temp_ids)
        termOfUse()

    downloadArxivViaIds(
        ids, save_path="./recent6months_saved_articles.json")


# running entry
if __name__ == "__main__":
    # main()
    main2()
    print("EVERYTHING DONE.")
