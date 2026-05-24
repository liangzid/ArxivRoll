"""Inspect AI task for ArxivRollBench.

ArxivRollBench is a rolling arXiv benchmark for scientific text reasoning.
The default task evaluates the compact 2026a split across all domains and SCP
task types. Use task parameters to select a release, domain, task type, or the
full split.
"""

import re
from typing import Any, Literal

import datasets
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice

from arxivrollbench_hf_revisions import HF_REVISIONS

Release = Literal["2024b", "2025a", "2026a", "all"]
Domain = Literal[
    "cs",
    "q_fin",
    "q-fin",
    "math",
    "physics",
    "stat",
    "q_bio",
    "q-bio",
    "econ",
    "eess",
    "all",
]
TaskType = Literal["s", "c", "p", "all"]
Split = Literal["compact", "full"]

DOMAINS: list[tuple[str, str]] = [
    ("cs", "cs"),
    ("q_fin", "q-fin"),
    ("math", "math"),
    ("physics", "physics"),
    ("stat", "stat"),
    ("q_bio", "q-bio"),
    ("econ", "econ"),
    ("eess", "eess"),
]
RELEASES = ["2024b", "2025a", "2026a"]
TASK_TYPES = ["s", "c", "p"]
DOMAIN_ALIASES = {
    "q-fin": "q_fin",
    "q-bio": "q_bio",
}
TASK_TYPE_NAMES = {
    "s": "sequencing",
    "c": "cloze",
    "p": "prediction",
}

MULTIPLE_CHOICE_TEMPLATE = """Answer the following scientific text reasoning question.
The last line of your response must be exactly: ANSWER: $LETTER
where LETTER is one of {letters}.

Question:
{question}

Options:
{choices}
"""


def normalize_domain(domain: str) -> str:
    return DOMAIN_ALIASES.get(domain, domain)


def dataset_path(release: str, hf_domain: str, task_type: str, split: Split) -> str:
    suffix = "-50" if split == "compact" else ""
    if release == "2024b":
        return f"liangzid/robench2024b_all_set{hf_domain}SCP-{task_type}{suffix}"
    return f"liangzid/robench{release}_test_all_category_set{hf_domain}SCP-{task_type}{suffix}"


def selection_to_letter(label: Any) -> str:
    match = re.search(r"\bselection\s*([1-4])\b", str(label), re.IGNORECASE)
    if match:
        return chr(ord("A") + int(match.group(1)) - 1)
    return str(label).strip().upper()


def iter_subset_keys(
    release: Release,
    domain: Domain,
    task_type: TaskType,
    split: Split,
) -> list[tuple[str, str, str, str]]:
    selected_releases = RELEASES if release == "all" else [release]
    normalized_domain = normalize_domain(domain)
    selected_domains = (
        DOMAINS
        if normalized_domain == "all"
        else [(normalized_domain, normalized_domain.replace("_", "-"))]
    )
    selected_task_types = TASK_TYPES if task_type == "all" else [task_type]

    keys = [
        (selected_release, selected_domain, selected_task_type, split)
        for selected_release in selected_releases
        for selected_domain, _ in selected_domains
        for selected_task_type in selected_task_types
    ]
    missing = [key for key in keys if key not in HF_REVISIONS]
    if missing:
        raise ValueError(f"Unsupported ArxivRollBench subset(s): {missing}")
    return keys


def record_to_sample(
    record: dict[str, Any],
    release: str,
    domain: str,
    task_type: str,
    index: int,
) -> Sample:
    if task_type == "p":
        question = (
            "Given the context, select the text that is the next sequence.\n\n"
            f"Context:\n{record['context']}"
        )
        target = str(record["label"]).strip().upper()
    else:
        question = (
            "Select the option that correctly completes the sequencing or cloze task.\n\n"
            f"{record['shuffled_text']}"
        )
        target = selection_to_letter(record["label"])

    return Sample(
        id=f"{release}_{domain}_{task_type}_{index}",
        input=question,
        choices=[str(record[letter]).strip() for letter in ["A", "B", "C", "D"]],
        target=target,
        metadata={
            "release": release,
            "domain": domain,
            "task_type": task_type,
            "task_type_name": TASK_TYPE_NAMES[task_type],
            "source_label": record["label"],
        },
    )


def arxivrollbench_dataset(
    release: Release = "2026a",
    domain: Domain = "all",
    task_type: TaskType = "all",
    split: Split = "compact",
) -> list[Sample]:
    samples: list[Sample] = []
    domain_lookup = dict(DOMAINS)
    for (
        selected_release,
        selected_domain,
        selected_task_type,
        selected_split,
    ) in iter_subset_keys(release, domain, task_type, split):
        hf_domain = domain_lookup[selected_domain]
        dataset = datasets.load_dataset(
            dataset_path(
                selected_release, hf_domain, selected_task_type, selected_split
            ),
            split="train",
            revision=HF_REVISIONS[
                (selected_release, selected_domain, selected_task_type, selected_split)
            ],
        )
        assert isinstance(dataset, datasets.Dataset)
        for index, record in enumerate(dataset):
            samples.append(
                record_to_sample(
                    record, selected_release, selected_domain, selected_task_type, index
                )
            )
    return samples


@task
def arxivrollbench(
    release: Release = "2026a",
    domain: Domain = "all",
    task_type: TaskType = "all",
    split: Split = "compact",
) -> Task:
    """Inspect AI implementation of ArxivRollBench.

    Args:
        release: Benchmark release to evaluate, or "all".
        domain: arXiv domain to evaluate, or "all".
        task_type: SCP task type: "s" sequencing, "c" cloze, "p" prediction, or "all".
        split: "compact" for the lightweight -50 datasets, or "full".
    """
    return Task(
        dataset=arxivrollbench_dataset(
            release=release, domain=domain, task_type=task_type, split=split
        ),
        solver=multiple_choice(template=MULTIPLE_CHOICE_TEMPLATE, shuffle=False),
        scorer=choice(),
        version="1.0.0",
        metadata={
            "release": release,
            "domain": domain,
            "task_type": task_type,
            "split": split,
            "paper": "https://ojs.aaai.org/index.php/AAAI/article/view/41098",
            "website": "https://arxivrollbench.github.io/",
        },
    )
