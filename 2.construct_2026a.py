"""
Construct and upload ArxivRollBench 2026a datasets.

This mirrors the 2025a construction flow in 1.run_vanilla_construct.py:
for each arXiv top-level category, build SCP-s, SCP-c, and SCP-p JSONL files,
plus their -50 subsets, then push each file to Hugging Face.
"""

import argparse
import json
import os
from collections import OrderedDict
from pathlib import Path

from constructor import constructBenchmarksSCP, push2HF


DEFAULT_DIRECTORY = Path("./robench2026a_test_all_category/")
SCP_CONFIGS = {
    "s": {"n_gram": 2, "minimal_char": 250},
    "c": {"n_gram": 5, "minimal_char": 400},
    "p": {"n_gram": 1, "minimal_char": 100},
}


def dataset_name(save_path: Path) -> str:
    return (
        str(save_path)
        .replace("./", "")
        .replace(".jsonl", "")
        .replace("/", "_")
        .replace(".json", "")
        .replace("recent6months_html_", "")
    )


def load_papers(path: Path):
    with path.open("r", encoding="utf8") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    papers = data["text"]
    print(f"{path}: {len(papers)} papers")
    return papers


def construct_one(raw_path: Path, scp_type: str, dataset_number, force: bool):
    suffix = f"SCP-{scp_type}"
    if dataset_number is not None:
        suffix += f"-{dataset_number}"
    save_path = Path(f"{raw_path}{suffix}.jsonl")

    if save_path.exists() and not force:
        print(f"Skip existing {save_path}")
        return save_path

    papers = load_papers(raw_path)
    config = SCP_CONFIGS[scp_type]
    construct_kwargs = {
        "papers4Q": papers,
        "hf_style_save_path": str(save_path),
        "scp_type": scp_type,
        "n_gram": config["n_gram"],
        "minimal_char": config["minimal_char"],
    }
    if dataset_number is not None:
        construct_kwargs["dataset_number"] = dataset_number
    constructBenchmarksSCP(**construct_kwargs)
    return save_path


def push_one(save_path: Path, skip_push: bool):
    name = dataset_name(save_path)
    print(f"Dataset name: {name}")
    if not skip_push:
        push2HF(str(save_path), name=name)


def raw_files(directory: Path):
    return sorted(
        path
        for path in directory.iterdir()
        if path.name.endswith(".json") and not path.name.endswith(".jsonl")
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default=str(DEFAULT_DIRECTORY))
    parser.add_argument("--skip-push", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--only-subset", action="store_true")
    parser.add_argument("--only-full", action="store_true")
    args = parser.parse_args()

    if args.only_subset and args.only_full:
        raise ValueError("--only-subset and --only-full are mutually exclusive")

    directory = Path(args.directory)
    if not directory.exists():
        raise FileNotFoundError(directory)

    if not args.skip_push and "HF_TOKEN" not in os.environ:
        raise RuntimeError("HF_TOKEN is required unless --skip-push is set")

    for raw_path in raw_files(directory):
        for scp_type in ("s", "c", "p"):
            if not args.only_subset:
                save_path = construct_one(raw_path, scp_type, None, args.force)
                push_one(save_path, args.skip_push)
            if not args.only_full:
                save_path = construct_one(raw_path, scp_type, 50, args.force)
                push_one(save_path, args.skip_push)


if __name__ == "__main__":
    main()
