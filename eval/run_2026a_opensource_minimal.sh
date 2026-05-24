#!/usr/bin/env bash
set -euo pipefail

# Minimal ArxivRollBench 2026a open-weight smoke run.
# Defaults are intentionally small: one 2026a -50 task, one sample per task,
# and two modest HF models. Override TASK/LIMIT/MODELS for larger runs.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LM_EVAL_BIN="${LM_EVAL_BIN:-${HOME}/anaconda3/envs/robench/bin/lm_eval}"

DATA_ROOT="${DATA_ROOT:-/data2/zi}"
export HF_HOME="${HF_HOME:-${DATA_ROOT}/huggingface}"
export HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-${HF_HOME}/datasets}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-${HF_HOME}/transformers}"
export TORCH_HOME="${TORCH_HOME:-${DATA_ROOT}/torch}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-${DATA_ROOT}/xdg_cache}"

RESULT_ROOT="${RESULT_ROOT:-${DATA_ROOT}/arxivrollbench_results/RES_OPENSOURCE_2026A_MINIMAL}"
REQUEST_CACHE_DIR="${REQUEST_CACHE_DIR:-${DATA_ROOT}/arxivrollbench_lm_eval_cache}"
TASK="${TASK:-robench2026a_all_setcsSCP-s-50}"
LIMIT="${LIMIT-1}"
BATCH_SIZE="${BATCH_SIZE:-auto}"
CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES-0,1,2,3}"
MODEL_ARGS_EXTRA="${MODEL_ARGS_EXTRA:-parallelize=True,dtype=bfloat16,trust_remote_code=True}"
DEVICE="${DEVICE:-}"

export CUDA_VISIBLE_DEVICES
export TORCH_USE_CUDA_DSA="${TORCH_USE_CUDA_DSA:-1}"
export TOKENIZERS_PARALLELISM="${TOKENIZERS_PARALLELISM:-false}"

mkdir -p "${RESULT_ROOT}" "${REQUEST_CACHE_DIR}" "${HF_HOME}" "${TORCH_HOME}" "${XDG_CACHE_HOME}"

if [[ "${MODELS:-}" == "" ]]; then
    model_ls=(
        "microsoft/Phi-3-mini-4k-instruct"
        "Qwen/Qwen2.5-7B-Instruct"
    )
else
    read -r -a model_ls <<< "${MODELS}"
fi

echo "repo: ${REPO_DIR}"
echo "lm_eval: ${LM_EVAL_BIN}"
echo "task: ${TASK}"
echo "limit: ${LIMIT}"
echo "cuda visible devices: ${CUDA_VISIBLE_DEVICES}"
echo "hf cache: ${HF_HOME}"
echo "results: ${RESULT_ROOT}"

for model in "${model_ls[@]}"; do
    safe_model="${model//\//__}"
    log_path="${RESULT_ROOT}/${safe_model}_${TASK}"
    response_cache="${REQUEST_CACHE_DIR}/${safe_model}_${TASK}.sqlite"

    echo "current evaluation task: ${TASK}"
    echo "current evaluation model: ${model}"

    device_args=()
    if [[ "${DEVICE}" != "" ]]; then
        device_args=(--device "${DEVICE}")
    fi

    limit_args=()
    if [[ "${LIMIT}" != "" ]]; then
        limit_args=(--limit "${LIMIT}")
    fi

    "${LM_EVAL_BIN}" \
        --model hf \
        --model_args "pretrained=${model},${MODEL_ARGS_EXTRA}" \
        --tasks "${TASK}" \
        --batch_size "${BATCH_SIZE}" \
        "${device_args[@]}" \
        "${limit_args[@]}" \
        --cache_requests true \
        --use_cache "${response_cache}" \
        --verbosity INFO \
        --log_samples \
        --output_path "${log_path}"
done

echo "RUNNING run_2026a_opensource_minimal.sh DONE."
