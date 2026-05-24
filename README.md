# ArxivRoll / ArxivRollBench

ArxivRoll is a dynamic benchmark pipeline for auditing how much LLM evaluation
scores may be inflated by public benchmark contamination. The pipeline collects
fresh arXiv papers, converts them into private SCP tasks, evaluates models, and
then publishes expired benchmark rounds after they have been used once.

SCP means:

- `S`: Sequencing. Re-order shuffled text fragments.
- `C`: Cloze. Fill masked sentences with the correct candidate order.
- `P`: Prediction. Choose the correct next fragment.

This repository contains the crawler, benchmark construction scripts, evaluation
scripts, result aggregation helpers, plotting helpers, and raw/processed outputs
from prior rounds.

## Current Rounds

| Round | Intended paper window | Main raw directory | Main result directory | Public task group |
| --- | --- | --- | --- | --- |
| `2024b` | Apr 2024 to Sep 2024 | `robench2024b_all/` | older eval outputs | `arxivrollbench2024b` |
| `2025a` | Jan 2025 to Jun 2025 in this checkout | `robench2025a_test_all_category/` | `robench2025a_results/` | `arxivrollbench2025a` |
| `2026a` | planned: Sep 2025 to Apr 2026 | `robench2026a_test_all_category/` | `robench2026a_results/` | `arxivrollbench2026a` |

The code currently has several hardcoded `2025a` paths. For a new release, update
those constants before running the crawler, constructor, evaluator, parser, and
leaderboard copy steps.

## Repository Map

| Path | Purpose |
| --- | --- |
| `spider_arxiv.py` | Collect arXiv metadata and HTML article text by domain and month. |
| `1.run_vanilla_construct.py` | Build SCP JSONL benchmark files from collected paper text. |
| `constructor.py` | Construction engine, including `constructBenchmarksSCP` and Hugging Face upload helper. |
| `scp.py` | Core SCP task generator for Sequencing, Cloze, and Prediction. |
| `post_process_paper_text.py` | Cleans and segments paper text into usable fragments. |
| `SearchBySomething.py` | TF-IDF retrieval for distractor/neighbor search. |
| `Vectorize.py` | Text vectorization used by retrieval. |
| `data/INSTRUCTION.py` | Prompt templates used by the harness tasks. |
| `data/Benchmarks___alignpublicprivate.py` | Public/private domain alignment for RS-style comparisons. |
| `eval/test_new_models.sh` | Open-weight model evaluation script. |
| `eval/1.3.closeAI_newscripts_router.sh` | API/closed-model evaluation through OpenRouter-compatible chat completions. |
| `eval/1.parse_collect_exper_res.py` | Older aggregation script. Check it carefully before reuse; the 2025a local copy had parsing/name issues. |
| `file_trans.py` | Copies closed/API model results into the consolidated `robenchYYYYx_results/` directory. |
| `robench2025a_results/` | Consolidated raw 2025a `lm_eval` result JSONs and samples. |
| `private_overall_res_new_2025a.json` | Aggregated private 2025a scores in `[model_dict, acc_matrix, std_matrix]` format. |
| `private_overall_res_new_2025a.meta.json` | Metadata describing which raw result file was selected per model. |

## Environment

Use the conda environment if possible:

```bash
conda env create -f robench.yaml
conda activate robench
```

Or install with pip:

```bash
pip install -r re.txt
```

## Inspect AI Evaluation

This repository also provides an Inspect AI task for running public
ArxivRollBench releases:

```bash
pip install -e .
inspect eval arxivrollbench_inspect.py@arxivrollbench --model openai/gpt-5-nano
```

The default Inspect task evaluates the compact `2026a` split across all
domains and SCP task types. You can select the release, domain, task type, and
compact/full split with task parameters:

```bash
inspect eval arxivrollbench_inspect.py@arxivrollbench \
  --model openai/gpt-5-nano \
  -T release=2026a \
  -T domain=cs \
  -T task_type=s \
  -T split=compact
```

Supported task parameters:

- `release`: `2024b`, `2025a`, `2026a`, or `all`
- `domain`: `cs`, `q_fin`/`q-fin`, `math`, `physics`, `stat`,
  `q_bio`/`q-bio`, `econ`, `eess`, or `all`
- `task_type`: `s` for sequencing, `c` for cloze, `p` for prediction, or
  `all`
- `split`: `compact` for the lightweight `-50` datasets, or `full`

The Inspect task loads the Hugging Face datasets with explicit pinned
revisions for reproducibility.

You also need the evaluation harness that defines the ArxivRollBench tasks:

```bash
git clone https://github.com/liangzid/harness-4-arxivrollbench
cd harness-4-arxivrollbench
pip install -e .
```

Required credentials depend on the step:

```bash
export HF_TOKEN=...              # needed when push2HF uploads datasets
export OPENROUTER_API_KEY=...    # needed for eval/1.3.closeAI_newscripts_router.sh
```

The constructor imports `HF_TOKEN` at module import time, so set it before running
`1.run_vanilla_construct.py`.

## Important arXiv Access Rules

This project queries arXiv. Respect arXiv's API and access rules.

- Keep one connection at a time.
- Do not try to bypass rate limits.
- The helper `termOfUse()` currently sleeps for 10 seconds between larger steps.
- Do not redistribute PDFs/source files unless the paper license permits it.
- This repository primarily stores metadata and extracted HTML text for research evaluation.

## Benchmark Release Naming

Use one release label everywhere:

```text
robench2026a_test_all_category/
robench2026a_results/
robench2026a_all_setcsSCP-s
arxivrollbench2026a
arxivrollbench2026a-50
private_overall_res_new_2026a.json
```

The expected private task grid is:

```text
cs, q-fin, math, eess, physics, stat, q-bio, econ
```

and for each domain:

```text
SCP-s, SCP-c, SCP-p
```

That gives 24 private tasks per full release.

## End-to-End Runbook for a New Benchmark Round

This section is the operational checklist for creating a fresh round such as
`2026a`.

### 1. Choose the Release Window

For the planned `2026a` round, use:

```text
2025-09-01 through 2026-04-30
```

Use valid month end dates. Do not blindly use `-30` for February.

Recommended month ranges:

```text
2025-09-01 to 2025-09-30
2025-10-01 to 2025-10-31
2025-11-01 to 2025-11-30
2025-12-01 to 2025-12-31
2026-01-01 to 2026-01-31
2026-02-01 to 2026-02-28
2026-03-01 to 2026-03-31
2026-04-01 to 2026-04-30
```

### 2. Update the Crawler Constants

Edit `spider_arxiv.py`, function `main3_allCategorys6Months()`.

Set the output directory:

```python
save_dir = "./robench2026a_test_all_category/"
```

Keep the domain set:

```python
set_specs = [
    "cs",
    "econ",
    "eess",
    "math",
    "physics",
    "q-bio",
    "q-fin",
    "stat",
]
```

Replace the current `year_month_ls` loop with explicit valid ranges. The current
code builds dates as `f"{ym}-01"` to `f"{ym}-30"`, which is not safe for February
or 31-day months. For a new release, prefer a list of `(from_date, until_date)`
pairs:

```python
date_ranges = [
    ("2025-09-01", "2025-09-30"),
    ("2025-10-01", "2025-10-31"),
    ("2025-11-01", "2025-11-30"),
    ("2025-12-01", "2025-12-31"),
    ("2026-01-01", "2026-01-31"),
    ("2026-02-01", "2026-02-28"),
    ("2026-03-01", "2026-03-31"),
    ("2026-04-01", "2026-04-30"),
]

for from_date, until_date in date_ranges:
    temp_ids = queryArxiv(
        set_spec=set_spec,
        from_date=from_date,
        until_date=until_date,
    )
    ids.extend(temp_ids)
    termOfUse()
```

The crawler writes one HTML-text JSON per domain:

```text
robench2026a_test_all_category/recent6months_html_setcs.json
robench2026a_test_all_category/recent6months_html_setecon.json
...
```

Each file has the structure:

```json
{
  "title": [],
  "abstract": [],
  "keywords": [],
  "text": []
}
```

### 3. Run the Crawler

Run from the repository root:

```bash
python spider_arxiv.py
```

For a long collection job, prefer a log:

```bash
nohup python spider_arxiv.py > 2026a_spider_arxiv.log 2>&1 &
```

Monitor progress:

```bash
tail -f 2026a_spider_arxiv.log
```

Validate raw collection:

```bash
python - <<'PY'
import json, glob
for p in sorted(glob.glob("robench2026a_test_all_category/recent6months_html_set*.json")):
    data = json.load(open(p))
    print(p, len(data.get("text", [])))
PY
```

Expected outcome: all 8 domain JSON files exist, and each has enough papers to
construct the benchmark. If a domain is too small, inspect crawler errors and
arXiv HTML availability for that domain/window.

### 4. Construct Full SCP Benchmarks

Edit `1.run_vanilla_construct.py`.

For full private benchmarks, use `main()` and set:

```python
directory = "./robench2026a_test_all_category/"
```

At the bottom of the file, run:

```python
if __name__ == "__main__":
    main()
```

Then run:

```bash
export HF_TOKEN=...
python 1.run_vanilla_construct.py
```

The construction parameters are currently:

| Task | `scp_type` | `n_gram` | `minimal_char` | Meaning |
| --- | --- | ---: | ---: | --- |
| Sequencing | `s` | 2 | 250 | Pick a multi-sentence passage and shuffle 3 chunks. |
| Cloze | `c` | 5 | 400 | Mask 3 sentences inside a longer passage. |
| Prediction | `p` | 1 | 100 | Choose the true next fragment among retrieved alternatives. |

Outputs are JSONL files next to each raw domain JSON:

```text
recent6months_html_setcs.jsonSCP-s.jsonl
recent6months_html_setcs.jsonSCP-c.jsonl
recent6months_html_setcs.jsonSCP-p.jsonl
...
```

The script also calls `push2HF(save_path, name=newdatasetname)`. Dataset names
are derived from the path, for example:

```text
robench2026a_test_all_category_setcsSCP-s
```

Check these names before uploading. If the harness expects names like
`robench2026a_all_setcsSCP-s`, either adjust the generated name logic or rename
the Hugging Face datasets after upload.

### 5. Construct Small API Subsets

Closed/API model evaluations often use a 50-sample version for cost control.

Edit `1.run_vanilla_construct.py`:

```python
directory = "./robench2026a_test_all_category/"
```

At the bottom:

```python
if __name__ == "__main__":
    mainSubset()
```

Then run:

```bash
export HF_TOKEN=...
python 1.run_vanilla_construct.py
```

This creates:

```text
recent6months_html_setcs.jsonSCP-s-50.jsonl
recent6months_html_setcs.jsonSCP-c-50.jsonl
recent6months_html_setcs.jsonSCP-p-50.jsonl
...
```

### 6. Validate the Constructed JSONL Files

Run:

```bash
python - <<'PY'
import glob, json
for p in sorted(glob.glob("robench2026a_test_all_category/*.jsonl")):
    n = 0
    bad = 0
    with open(p, encoding="utf8") as f:
        for line in f:
            n += 1
            try:
                row = json.loads(line)
                if "label" not in row:
                    bad += 1
            except Exception:
                bad += 1
    print(f"{p}\trows={n}\tbad={bad}")
PY
```

Inspect examples:

```bash
head -1 robench2026a_test_all_category/recent6months_html_setcs.jsonSCP-s.jsonl
head -1 robench2026a_test_all_category/recent6months_html_setcs.jsonSCP-c.jsonl
head -1 robench2026a_test_all_category/recent6months_html_setcs.jsonSCP-p.jsonl
```

Look for:

- Empty or broken text.
- Duplicate choices that make a task ambiguous.
- Labels outside the expected options.
- Very short fragments caused by HTML extraction failures.

### 7. Register the New Task Group in the Harness

The evaluator uses `lm_eval`, so the new benchmark must exist in the installed
ArxivRollBench harness.

For a full round, the expected task group is:

```text
arxivrollbench2026a
```

For the 50-sample API subset:

```text
arxivrollbench2026a-50
```

Update the harness repository so those groups point to the 24 uploaded datasets.
Then reinstall it:

```bash
cd harness-4-arxivrollbench
pip install -e .
```

Smoke-test task discovery:

```bash
lm_eval --tasks list | grep arxivrollbench2026a
```

### 8. Evaluate Open-Weight Models

Edit `eval/test_new_models.sh`.

Set:

```bash
export log_dir="${root_dir}/RES_OPENSOURCE_2026A/"
export task_ls=(
    "arxivrollbench2026a" \
)
```

Set `model_ls` to the open-weight models to evaluate. Be careful with Bash
arrays: do not put commas between items.

Correct:

```bash
export model_ls=("Qwen/Qwen3-8B" "meta-llama/Llama-3.1-8B-Instruct")
```

Incorrect:

```bash
export model_ls=("Qwen/Qwen3-8B", "meta-llama/Llama-3.1-8B-Instruct")
```

Run:

```bash
bash eval/test_new_models.sh
```

Result layout should look like:

```text
eval/RES_OPENSOURCE_2026A/<model><task>/<model_sanitized>/results_<timestamp>.json
```

### 9. Evaluate Closed/API Models

Edit `eval/1.3.closeAI_newscripts_router.sh`.

Set:

```bash
export log_dir="${root_dir}/0721_newcloseAIs_2026A/"
export task_ls=(
    "arxivrollbench2026a-50" \
)
```

Set `model_ls` to the desired OpenRouter model IDs. Then run:

```bash
export OPENROUTER_API_KEY=...
bash eval/1.3.closeAI_newscripts_router.sh
```

Result layout should look like:

```text
eval/0721_newcloseAIs_2026A/<provider>/<model>arxivrollbench2026a-50/<provider>__<model>/results_<timestamp>.json
```

### 10. Consolidate Result Files

Create a release result directory:

```bash
mkdir -p robench2026a_results
```

Copy open-weight and closed/API result directories into it. `file_trans.py`
currently contains hardcoded `2025a` paths; update it before use:

```python
task = "arxivrollbench2026a-50"
destination = "/home/zi/arxivSpider/robench2026a_results"
source = f"/home/zi/arxivSpider/eval/0721_newcloseAIs_2026A/{model}{task}"
```

For open-weight runs, copy from `eval/RES_OPENSOURCE_2026A/`.

Validate consolidated raw results:

```bash
python - <<'PY'
import json, glob, os
count = 0
models = set()
for p in glob.glob("robench2026a_results/*/*/results_*.json"):
    data = json.load(open(p))
    model = data.get("model_name") or p
    tasks = [k for k in data.get("results", {}) if k.startswith("robench2026a")]
    print(model, len(tasks), p)
    models.add(model)
    count += 1
print("raw result files:", count)
print("unique models:", len(models))
PY
```

Each complete full or subset result should have 24 private tasks.

### 11. Aggregate Private Scores

The older `eval/1.parse_collect_exper_res.py` is path-sensitive and has had
model-name parsing issues. For a new round, aggregate directly from raw result
JSONs using the same output format:

```python
[
  res_model_dict,
  res_acc_lss,
  res_std_lss,
]
```

For `2026a`, write:

```text
private_overall_res_new_2026a.json
eval/private_overall_res_new_2026a.json
private_overall_res_new_2026a.meta.json
```

When aggregating API subset tasks, normalize `-50` suffixes back to base task
names. For example:

```text
robench2026a_all_setcsSCP-s-50 -> robench2026a_all_setcsSCP-s
```

Validation:

```bash
python - <<'PY'
import json
p = "private_overall_res_new_2026a.json"
model_dict, accs, stds = json.load(open(p))
print("models", len(model_dict))
print("rows", len(accs))
print("cols", len(accs[0]) if accs else 0)
print("negative acc", sum(x < 0 for row in accs for x in row))
PY
```

Expected:

```text
cols = 24
negative acc = 0
```

### 12. Publish to the Leaderboard

The leaderboard repository expects public JSON files to be model-keyed objects,
not the full three-element aggregate list.

Convert the aggregate:

```bash
node - <<'NODE'
const fs = require('fs');
const src = '/home/zi/arxivSpider/private_overall_res_new_2026a.json';
const dest = '/home/zi/arxivbenchleaderboard/public/2026a.json';
const payload = JSON.parse(fs.readFileSync(src, 'utf8'));
const modelDict = Array.isArray(payload) ? payload[0] : payload;
fs.writeFileSync(dest, JSON.stringify(modelDict, null, 2) + '\n');
console.log(`wrote ${dest} models=${Object.keys(modelDict).length}`);
NODE
```

Then update the leaderboard frontend to include the new version in its data URL
map and version selector, mirroring the `2025a` work.

Validate:

```bash
cd ~/arxivbenchleaderboard
npm ci
npm run lint
npm run build
npm run dev -- --hostname 127.0.0.1
```

Open:

```text
http://127.0.0.1:3000
```

Switch to the new benchmark tab and check:

- The table has the expected number of models.
- The top score matches the aggregate script.
- Domain tabs show nonzero rows.
- Radar charts load top models.

## Result Summary Commands

Use this to summarize any round directly from raw result JSONs:

```bash
python - <<'PY'
import json, glob, os, re

ROUND = "2026a"
ROOT = f"robench{ROUND}_results"

def metric(v):
    for k, val in v.items():
        if k.startswith("exact_match,") or k.startswith("acc,"):
            return float(val)
    return None

def normalize(k):
    return k[:-3] if k.endswith("-50") else k

runs = []
for p in glob.glob(f"{ROOT}/*/*/results_*.json"):
    data = json.load(open(p))
    model = data.get("model_name") or p
    task_scores = {}
    for k, v in data.get("results", {}).items():
        nk = normalize(k)
        if nk.startswith(f"robench{ROUND}_all_"):
            task_scores[nk] = metric(v)
    if len(task_scores) == 24:
        ts = re.search(r"results_(.+)\.json$", os.path.basename(p)).group(1)
        runs.append((model, ts, p, task_scores))

latest = {}
for model, ts, p, scores in runs:
    if model not in latest or ts > latest[model][0]:
        latest[model] = (ts, p, scores)

rows = []
for model, (_, _, scores) in latest.items():
    vals = list(scores.values())
    rows.append((sum(vals) / len(vals), model))

for score, model in sorted(rows, reverse=True)[:20]:
    print(f"{score * 100:5.2f}\t{model}")
PY
```

## Known Fragile Points

- `spider_arxiv.py` and `1.run_vanilla_construct.py` are not parameterized yet;
  release names and directories are edited in code.
- `queryArxiv()` uses OAI-PMH. If arXiv returns no records, inspect the XML and
  date range before assuming the domain has no papers.
- `downloadArxivViaIds()` depends on arXiv HTML pages. Some papers may not have
  usable HTML and will be skipped.
- The constructor imports `HF_TOKEN` immediately. Missing `HF_TOKEN` can fail
  before useful work begins.
- `eval/test_new_models.sh` currently contains a Bash array example with commas;
  remove commas before running.
- `eval/1.parse_collect_exper_res.py` should be reviewed before reuse; prefer a
  raw-result aggregation script for new rounds.
- API models may produce near-zero scores if they fail to follow the requested
  output format. Inspect `samples_*.jsonl` before treating such scores as model
  capability.
- The 50-sample subset should be reported separately or normalized carefully; do
  not mix task names with and without `-50` unless the aggregation script makes
  that normalization explicit.

## Minimal 2026A Checklist

1. Edit `spider_arxiv.py` for `robench2026a_test_all_category/` and date ranges
   from `2025-09-01` through `2026-04-30`.
2. Run `python spider_arxiv.py`.
3. Validate 8 raw domain JSON files.
4. Edit `1.run_vanilla_construct.py` for `robench2026a_test_all_category/`.
5. Run full construction with `main()`.
6. Run subset construction with `mainSubset()`.
7. Register `arxivrollbench2026a` and `arxivrollbench2026a-50` in the harness.
8. Evaluate open-weight models into `eval/RES_OPENSOURCE_2026A/`.
9. Evaluate closed/API models into `eval/0721_newcloseAIs_2026A/`.
10. Copy all raw result folders into `robench2026a_results/`.
11. Aggregate to `private_overall_res_new_2026a.json`.
12. Convert and copy to `~/arxivbenchleaderboard/public/2026a.json`.
13. Build the leaderboard and check the new tab.
