from arxivrollbench_inspect import (
    arxivrollbench,
    arxivrollbench_dataset,
    dataset_path,
    iter_subset_keys,
    normalize_domain,
    record_to_sample,
    selection_to_letter,
)


def test_dataset_path_compact_and_full():
    assert (
        dataset_path("2026a", "cs", "s", "compact")
        == "liangzid/robench2026a_test_all_category_setcsSCP-s-50"
    )
    assert (
        dataset_path("2024b", "q-fin", "p", "full")
        == "liangzid/robench2024b_all_setq-finSCP-p"
    )


def test_selection_to_letter():
    assert selection_to_letter("Selection 1") == "A"
    assert selection_to_letter("selection 4") == "D"
    assert selection_to_letter("A") == "A"
    assert selection_to_letter("1") == "1"


def test_domain_aliases_and_subset_keys():
    assert normalize_domain("q-bio") == "q_bio"
    assert iter_subset_keys("2026a", "q-bio", "s", "compact") == [
        ("2026a", "q_bio", "s", "compact")
    ]


def test_record_to_sample_prediction():
    record = {
        "context": "The introduction describes a new method.",
        "A": "A candidate",
        "B": "B candidate",
        "C": "C candidate",
        "D": "D candidate",
        "label": "C",
    }

    sample = record_to_sample(record, "2026a", "cs", "p", 0)

    assert sample.target == "C"
    assert sample.choices == [
        "A candidate",
        "B candidate",
        "C candidate",
        "D candidate",
    ]
    assert sample.metadata["task_type_name"] == "prediction"


def test_record_to_sample_selection():
    record = {
        "shuffled_text": "Paragraph with a blank.",
        "A": "A candidate",
        "B": "B candidate",
        "C": "C candidate",
        "D": "D candidate",
        "label": "Selection 2",
    }

    sample = record_to_sample(record, "2026a", "math", "s", 0)

    assert sample.target == "B"
    assert sample.metadata["task_type_name"] == "sequencing"


def test_load_small_dataset_subset():
    samples = arxivrollbench_dataset(
        release="2026a", domain="cs", task_type="s", split="compact"
    )

    assert len(samples) > 0
    assert samples[0].choices is not None
    assert samples[0].target in ["A", "B", "C", "D"]


def test_task_constructs():
    task = arxivrollbench(release="2026a", domain="cs", task_type="s", split="compact")

    assert task.dataset is not None
    assert task.scorer is not None
