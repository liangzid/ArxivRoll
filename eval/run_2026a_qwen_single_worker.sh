#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
    echo "usage: $0 GPU MODEL [MODEL ...]" >&2
    exit 2
fi

GPU="$1"
shift

unset TRANSFORMERS_CACHE

LM_EVAL_BIN="${LM_EVAL_BIN:-/home/zi/anaconda3/envs/robench/bin/lm_eval}"
TASK="${TASK:-arxivrollbench2026a}"
BATCH_SIZE="${BATCH_SIZE:-8}"
RESULT_ROOT="${RESULT_ROOT:-/data2/zi/arxivrollbench_results/RES_OPENSOURCE_2026A_QWEN_FIXED_BS8}"
MODEL_ARGS_EXTRA="${MODEL_ARGS_EXTRA:-dtype=bfloat16,trust_remote_code=True}"
GEN_KWARGS="${GEN_KWARGS:-max_gen_toks=32}"

export HF_HOME="${HF_HOME:-/home/zi/.cache/huggingface}"
export HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-/data2/zi/huggingface/datasets}"
export TORCH_HOME="${TORCH_HOME:-/data2/zi/torch}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/data2/zi/xdg_cache}"
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
export TOKENIZERS_PARALLELISM="${TOKENIZERS_PARALLELISM:-false}"

mkdir -p "${RESULT_ROOT}" "${HF_DATASETS_CACHE}" "${TORCH_HOME}" "${XDG_CACHE_HOME}"

echo "worker gpu=${GPU} task=${TASK} batch_size=${BATCH_SIZE}"
echo "hf_home=${HF_HOME}"
echo "results=${RESULT_ROOT}"
echo "gen_kwargs=${GEN_KWARGS}"

for model in "$@"; do
    safe_model="${model//\//__}"
    log_path="${RESULT_ROOT}/${safe_model}_${TASK}"

    echo "============================================================"
    echo "timestamp=$(date -Is)"
    echo "gpu=${GPU}"
    echo "model=${model}"
    echo "output=${log_path}"

    CUDA_VISIBLE_DEVICES="${GPU}" "${LM_EVAL_BIN}" \
        --model hf \
        --model_args "pretrained=${model},${MODEL_ARGS_EXTRA}" \
        --tasks "${TASK}" \
        --batch_size "${BATCH_SIZE}" \
        --gen_kwargs "${GEN_KWARGS}" \
        --verbosity INFO \
        --log_samples \
        --output_path "${log_path}"

    status=$?
    echo "timestamp=$(date -Is) status=${status} model=${model}"
done

echo "worker gpu=${GPU} done at $(date -Is)"
