"""
======================================================================
BENCHMARKS___ALIGNPUBLICPRIVATE --- 

    Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
    Copyright © 2024, ZiLiang, all rights reserved.
    Created: 12 November 2024
======================================================================
"""


# ------------------------ Code --------------------------------------

private_public_align_dict = {
    "cs": [
        "mmlu_pro_computer_science",

        "mmlu_college_computer_science",
        "mmlu_computer_security",
        "mmlu_high_school_computer_science",
        "mmlu_machine_learning",

    ],
    "econ": [
        "mmlu_pro_economics",

        "mmlu_econometrics",
        "mmlu_high_school_microeconomics",
        "mmlu_high_school_macroeconomics",
    ],
    "eess": [
        "mmlu_pro_engineering",

        "mmlu_electrical_engineering",
    ],
    "math": [
        "mmlu_pro_math",

        "mmlu_abstract_algebra",
        "mmlu_college_mathematics",
        "mmlu_elementary_mathematics",
        "mmlu_formal_logic",
        "mmlu_high_school_mathematics",

        "gsm8k",
        "gsm_plus",
    ],
    "physics": [
        "mmlu_pro_physics",

        "mmlu_astronomy",
        "mmlu_college_physics",
        "mmlu_conceptual_physics",
        "mmlu_high_school_physics",
    ],
    "q-bio": [
        "mmlu_pro_biology",

        "mmlu_anatomy",
        "mmlu_clinical_knowledge",
        "mmlu_college_biology",
        "mmlu_college_medicine",
        "mmlu_high_school_biology",

    ],
    "fin": [
        "mmlu_pro_business",

        "mmlu_business_ethics",
    ],
    "stat": [
        "mmlu_pro_math",

        "mmlu_high_school_statistics",
    ],
}

unmatched_public_benchmarks = [
    "mmlu_pro_chemistry",
    "mmlu_pro_health",
    "mmlu_pro_history",
    "mmlu_pro_law",
    "mmlu_pro_other",
    "mmlu_pro_philosophy",
    "mmlu_pro_psychology",
    # ---------------------------
    "mmlu_other",
    "mmlu_social_sciences",
    "mmlu_humanities",

    "mmlu_college_chemistry",
    "mmlu_high_school_chemistry",
    "mmlu_high_school_geography",
]

unmatched_private_benchmarks = [
]
