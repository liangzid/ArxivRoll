# 🚀 ArxivBench
*“Fresh from ArXiv, served once, and never reheated.”*

> 📌 TL;DR: ArxivBench tells you **“How much of your score is real, and how much is cheating?”**  

---

## 1. 📊 What is ArxivBench?

ArxivBench is a **dynamic, one-time-pad-inspired evaluation framework** 🛡️ that **audits** how much Large Language Models (LLMs) **over-estimate** their true abilities on public benchmarks.  

### ⚠️ Key Problems ArxivBench Tackles  
- **📥 Data contamination**  
  Public benchmarks (MMLU, GSM8K, etc.) often sneak into pre-training data → inflated scores.  
- **🎯 Biased overtraining**  
  Developers may “teach to the test,” tuning models only on popular domains.  
- **🕵️ Transparency crisis**  
  Private leaderboards (SEAL, Chatbot Arena) are opaque & hard to reproduce.

---

### 🧪 How ArxivBench Works  

1. **🌱 Fresh Test Cases**  
   Every 6 months we scrape **latest ArXiv preprints** (Apr–Sep 2024 → ArxivBench-2024b).  
   > 🏷️ Domains: CS, Math, Physics, Bio, Econ, Finance, Statistics, EE.

2. **🎲 SCP Tasks**  
   Articles are auto-converted into three symbolic tasks:  
   - **Sequencing** 🔀 → Re-order shuffled sentences.  
   - **Cloze** 🕳️ → Fill masked sentences.  
   - **Prediction** 🔮 → Choose the correct next sentence.  

3. **📈 Rugged Scores (RS)**  
   - **RS-I** 🧪 = % inflation on public vs. private benchmarks.  
   - **RS-II** ⚖️ = performance variance across domains (biased training detector).

---

### 🌟 Unique Features  
- **🕐 One-Time Use**: private benchmarks are **used once**, then **expired & open-sourced**.  
- **✅ High Quality**: filtered for length, complexity, minimal math/tables.  
- **🌍 Broad Coverage**: 8 domains, ~100-word contexts, 1 k+ samples per domain.

---

## 👩‍💻 2. How Do I Evaluate my Model?

The most easy way is to use `llm-eval-harness`

Just install `lm-eval` from [here](https://github.com/liangzid/harness-4-arxivbench),
and then evaluate a huggingface model with:

```sh

export task_ls=(
    "arxivbench2024b_all_setcsSCP-s" \
    "arxivbench2024b_all_setcsSCP-c" \
    "arxivbench2024b_all_setcsSCP-p" \
    "arxivbench2024b_all_setq-finSCP-s" \
    "arxivbench2024b_all_setq-finSCP-c" \
    "arxivbench2024b_all_setq-finSCP-p" \
    "arxivbench2024b_all_setmathSCP-s" \
    "arxivbench2024b_all_setmathSCP-c" \
    "arxivbench2024b_all_setmathSCP-p" \
    "arxivbench2024b_all_seteessSCP-s" \
    "arxivbench2024b_all_seteessSCP-c" \
    "arxivbench2024b_all_seteessSCP-p" \
    "arxivbench2024b_all_setphysicsSCP-s" \
    "arxivbench2024b_all_setphysicsSCP-c" \
    "arxivbench2024b_all_setphysicsSCP-p" \
    "arxivbench2024b_all_setstatSCP-s" \
    "arxivbench2024b_all_setstatSCP-c" \
    "arxivbench2024b_all_setstatSCP-p" \
    "arxivbench2024b_all_setq-bioSCP-s" \
    "arxivbench2024b_all_setq-bioSCP-c" \
    "arxivbench2024b_all_setq-bioSCP-p" \
    "arxivbench2024b_all_seteconSCP-s" \ 
    "arxivbench2024b_all_seteconSCP-c" \
    "arxivbench2024b_all_seteconSCP-p" 
)
	lm_eval\
	    --model hf\
	    --model_args pretrained=your-model-name,parallelize=True\
	    --tasks any-arxivbench-task\
	    --verbosity DEBUG\
	    --log_samples\
	    --output_path your-log-path
```

You can also evaluate LLM via APIs with examples detailed in `./eval/`.




## 👩‍💻 3. How to Use & Read the Code

---

### 📦 1. Install Environment

#### Via pip
```bash
pip install -r re.txt
```

#### Via conda (recommended)
```bash
conda env create -f robench.yaml
conda activate robench
```

#### Clone & editable install
```bash
git clone https://github.com/XXXXXX/harness-4-robench/tree/robench
cd harness-4-robench
pip install -e .
```

---

### 🗂️ 2. File Map – “Where is what?”

| 📁 Path | 🎯 Purpose |
|---------|------------|
| `./1.run_vanilla_construct.py` | 🏗️ **One-click generator** of your **private benchmark** from fresh ArXiv papers. |
| `constructor.py` | 🔧 **Engine room**: all SCP logic (Sequencing / Cloze / Prediction) lives here. |
| `data/` | 📚 **Static assets** |
| &nbsp;&nbsp;&nbsp;&nbsp;`./data/INSTRUCTION.py` | 📝 Prompt templates fed into the LLM during evaluation. |
| `eval/` | 🧪 **Evaluation scripts** |
| &nbsp;&nbsp;&nbsp;&nbsp;`./eval/0.1.vanilla_harness_test.sh` | 🤗 Evaluate **open-source HuggingFace models**. |
| &nbsp;&nbsp;&nbsp;&nbsp;`./eval/0.2.harness_eval_closeAIs.sh` | 🔐 Evaluate **OpenAI / Claude / Gemini APIs**. |
| `post_process_paper_text.py` | ✂️ Clean & segment raw ArXiv LaTeX → plain English sentences. |
| `spider_arxiv.py` | 🕷️ Crawler that **downloads** the latest ArXiv PDFs & abstracts. |
| `SearchBySomething.py` | 🔍 TF-IDF retriever to mine distractor sentences for Prediction tasks. |
| `Vectorize.py` | 🧮 Convert any text into dense embeddings for retrieval. |
| `utils.py` | 🧰 Tiny helpers (date parsing, logging, helpers, etc.). |

---

### 🚀 3. Quick Start – 3 Commands to Glory

#### ① Download ArXiv articles
```bash
python spider_arxiv.py
```
> 🗂️ Drops papers into `./data/raw/`.

#### ② Build a private benchmark
```bash
python 1.run_vanilla_construct.py
```
> 🎲 Generates **Sequencing / Cloze / Prediction** tasks → `./benchmarks/`.

#### ③ Reproduce our Results
```bash
# Open-source models (Llama, Qwen, ...)
bash ./eval/0.1.vanilla_harness_test.sh

# Proprietary APIs (GPT-4, Claude, Gemini, ...)
bash ./eval/0.2.harness_eval_closeAIs.sh
```
> 📊 Results saved as JSON + auto-plot RS scores.

---

Happy benchmarking! 🪄













