"""
======================================================================
EVAL_BENCHMARK_STABLITY ---

Evaluate the stablity of the benchmark generation methods.

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 26 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

# normal import
import os
import json
from typing import List, Tuple, Dict
import random
from pprint import pprint as ppp
from collections import OrderedDict
from tqdm import tqdm

import torch

from constructor import push2HF
from constructor import constructBenchmarksSCP


def intrisicInfer(
        modelname,
        save_path,
        scp_type="s",
        max_length=2048,
):
    # 1. load model
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers import pipeline

    model = AutoModelForCausalLM.from_pretrained(
        modelname,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    )
    tokenizer = AutoTokenizer\
        .from_pretrained(modelname)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    text_gen = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=max_length,
        max_new_tokens=20,
        do_sample=False,
    )
    print("Loading Done.")

    # 2. load test set
    assert scp_type in ["s", "c", "p"]
    # assert scp_type in ["s",]
    time_ls = list(range(32))
    # time_ls = list(range(2))

    overall_dict = {}

    for time in time_ls:
        fpth = f"./multiTimeEvalBackup/Experiments_Time{time}_SCP-{scp_type}.jsonl"

        datals = []
        # from collections import OrderedDict
        with open(fpth, 'r', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                if line.endswith("\n"):
                    line = line[:-1]
                data = json.loads(line)
                datals.append(data)
        print("Now for generation.")
        # Now for inference
        hit = 0.
        for data in tqdm(datals, desc="Test Cases",):
            if scp_type == "s":
                shuffled_text = data["shuffled_text"]
                A = data["A"]
                B = data["B"]
                C = data["C"]
                D = data["D"]
                label = data["label"]
                inp = f"""## Instruction:\n Given a **shuffled text** composed of sentences A, B, and C, your task is to select the correct order from four available selections. Avoid providing any additional information (such as explanations of your choice) or restating the sentences in your answer. Simply provide your selection: Selection 1, Selection 2, Selection 3, or Selection 4.\n## Shuffled text:\n{shuffled_text}\n## Choice:\n**Selection 1** {A}\n**Selection 2** {B}\n**Selection 3** {C}\n**Selection 4** {D}\nAnswer:"""
                output = text_gen(inp, num_return_sequences=1,
                                  return_full_text=False,)
                output = output[0]["generated_text"]
                if label in output:
                    hit += 1
                    print(">>>>> HITTED.")
                print(f"label: {label}")
                print("output", output)

            elif scp_type == "c":
                text_with_holes = data["text_with_holes"]
                text_candidates = data["text_candidates"]
                A = data["A"]
                B = data["B"]
                C = data["C"]
                D = data["D"]
                label = data["label"]
                inp = f"""## Instruction:\n Given a **masked paragraph** with three masked sentences marked as '<|MaskedSentence|>' and candidate sentences labeled A, B, and C, your task is to fill in the correct sentences to the masked positions by selecting the appropriate answers from four provided selections. Avoid providing any additional information (such as explanations of your choice) or restating the sentences in your answer. Simply provide your selection: Selection 1, Selection 2, Selection 3, or Selection 4.\n## Masked paragraph:\n{text_with_holes}\n## {text_candidates}\n ## Choice:\n**Selection 1** {A}\n**Selection 2** {B}\n**Selection 3** {C}\n**Selection 4** {D}\nAnswer:"""
                output = text_gen(inp, num_return_sequences=1,
                                  return_full_text=False,)
                output = output[0]["generated_text"]
                if label in output:
                    hit += 1
                print(f"label: {label}")
                print("output", output)
            elif scp_type == "p":
                context = data["context"]
                A = data["A"]
                B = data["B"]
                C = data["C"]
                D = data["D"]
                label = data["label"]
                inp = f"""## Instruction:\n Given a context, and four choices marked as A, B, C, and D, your task is to select the correct text which is the next sequence of the provided context. Avoid providing any additional information (such as explanations of your choice) or restating the choice in your answer. Simply provide one of the four letters: A, B, C, or D.\n## Context:\n{context}\n## Choice:\n**A** {A}\n**B** {B}\n**C** {C}\n**D** {D}\nAnswer:"""
                output = text_gen(inp, num_return_sequences=1,
                                  return_full_text=False,)
                output = output[0]["generated_text"]
                if label in output:
                    hit += 1
                print(f"label: {label}")
                print("output", output)
        overall_dict[time] = hit/len(datals)

    print(overall_dict)
    with open(save_path, 'w', encoding='utf8') as f:
        json.dump(overall_dict,
                  f, ensure_ascii=False, indent=4)
    print("Results save done.")


def multitimeGenerateBenches(
        scp_type="s",
        times=10,):
    save_dir = "./multiTimeEvalBackup/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for time in range(times):
        dataset_from_path = "./robench2024b_all/recent6months_html_setcs.json"
        with open(dataset_from_path,
                  'r', encoding='utf8') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
        papers = data["text"]
        print(f"All paper Number: {len(papers)}")

        save_path = f"{save_dir}Experiments_Time{time}_SCP-{scp_type}.jsonl"
        constructBenchmarksSCP(
            papers,
            hf_style_save_path=save_path,
            scp_type=scp_type,
            n_gram=2,
            minimal_char=250,
        )
        newdatasetname = f"robench-eval-Time{time}-{scp_type}"
        push2HF(save_path, name=newdatasetname)


def main():
    # multitimeGenerateBenches("s", 32)
    multitimeGenerateBenches("c", 32)
    multitimeGenerateBenches("p", 32)


if __name__ == "__main__":
    main()

    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    save_pth_prefix = "stability_benchmark_eval_"

    # intrisicInfer(
    #     "meta-llama/Llama-3.1-8B-Instruct",
    #     save_path=save_pth_prefix+"s.json",
    #     scp_type="s",
    # )

    # intrisicInfer(
    #     "meta-llama/Llama-3.1-8B-Instruct",
    #     save_path=save_pth_prefix+"s.json",
    #     scp_type="c",
    # )
    # intrisicInfer(
    #     "meta-llama/Llama-3.1-8B-Instruct",
    #     save_path=save_pth_prefix+"s.json",
    #     scp_type="p",
    # )
