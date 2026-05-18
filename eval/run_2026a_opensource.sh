#!/usr/bin/env bash
set -euo pipefail

# ArxivRollBench 2026a evaluation for locally loaded Hugging Face/open-weight LLMs.
# Task group: arxivrollbench2026a
# Model list refreshed on 2026-05-18 from Hugging Face Hub/API plus prior 2025a runs.
#
# This script is intentionally not launched by default; review the model list and
# CUDA settings before running. Large models below may require multi-GPU sharding,
# quantized checkpoints, or local cache access approvals.

echo "HOME: ${HOME}"

LM_EVAL_BIN="${LM_EVAL_BIN:-${HOME}/anaconda3/envs/robench/bin/lm_eval}"
ROOT_DIR="${ROOT_DIR:-${HOME}/arxivSpider/eval}"
LOG_DIR="${LOG_DIR:-${ROOT_DIR}/RES_OPENSOURCE_2026A}"
TASK="${TASK:-arxivrollbench2026a}"

export TORCH_USE_CUDA_DSA="${TORCH_USE_CUDA_DSA:-1}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0,1,2,3}"

mkdir -p "${LOG_DIR}"

# Default: broad open-weight coverage across historical baselines, 2025a models,
# and current 2026 frontier/local families. Remove entries that do not fit your
# hardware, or run one family at a time by editing this array.
model_ls=(
    # Historical and small baselines
    "EleutherAI/gpt-j-6B"
    "microsoft/phi-1"
    "microsoft/phi-1_5"
    "microsoft/phi-2"
    "microsoft/Phi-3-mini-4k-instruct"
    "microsoft/Phi-3.5-mini-instruct"
    "microsoft/Phi-4-reasoning"
    "microsoft/Phi-4-reasoning-plus"

    # Meta Llama family
    "meta-llama/Llama-2-7b-chat-hf"
    "meta-llama/Llama-2-13b-chat-hf"
    "meta-llama/Meta-Llama-3-8B"
    "meta-llama/Llama-3.1-8B"
    "meta-llama/Llama-3.1-8B-Instruct"
    "meta-llama/Llama-3.1-70B-Instruct"
    "meta-llama/Llama-3.2-1B"
    "meta-llama/Llama-3.2-1B-Instruct"
    "meta-llama/Llama-3.2-3B"
    "meta-llama/Llama-3.2-3B-Instruct"
    "meta-llama/Llama-3.3-70B-Instruct"
    "meta-llama/Llama-4-Scout-17B-16E-Instruct"
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"

    # Qwen family
    "Qwen/Qwen2-7B-Instruct"
    "Qwen/Qwen2.5-7B"
    "Qwen/Qwen2.5-7B-Instruct"
    "Qwen/Qwen2.5-72B-Instruct"
    "Qwen/Qwen2.5-Math-7B"
    "Qwen/Qwen2.5-Math-7B-Instruct"
    "Qwen/Qwen3-4B"
    "Qwen/Qwen3-8B"
    "Qwen/Qwen3-14B"
    "Qwen/Qwen3-32B"
    "Qwen/Qwen3.5-9B"
    "Qwen/Qwen3.5-27B"
    "Qwen/Qwen3.5-35B-A3B"
    "Qwen/Qwen3.6-27B"
    "Qwen/Qwen3.6-35B-A3B"

    # Google Gemma family
    "google/gemma-3-1b-it"
    "google/gemma-3-4b-it"
    "google/gemma-3-12b-it"
    "google/gemma-3-27b-it"
    "google/gemma-4-31B-it"

    # Mistral / Mixtral
    "mistralai/Mistral-7B-Instruct-v0.1"
    "mistralai/Mistral-7B-Instruct-v0.2"
    "mistralai/Mistral-7B-Instruct-v0.3"
    "mistralai/Mixtral-8x7B-Instruct-v0.1"
    "mistralai/Mixtral-8x22B-Instruct-v0.1"

    # Other open-weight coverage from prior rounds / common deployments
    "01-ai/Yi-1.5-34B-Chat"
    "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"
    "tiiuae/Falcon3-10B-Instruct"
    "recursal/QRWKV6-32B-Instruct-Preview-v0.1"
)

for model in "${model_ls[@]}"; do
    echo "current evaluation task: ${TASK}"
    echo "current evaluation model: ${model}"
    log_path="${LOG_DIR}/${model}${TASK}"

    "${LM_EVAL_BIN}" \
        --model hf \
        --model_args "pretrained=${model},parallelize=True,trust_remote_code=True" \
        --tasks "${TASK}" \
        --batch_size auto \
        --verbosity DEBUG \
        --log_samples \
        --output_path "${log_path}"
done

echo "RUNNING run_2026a_opensource.sh DONE."
