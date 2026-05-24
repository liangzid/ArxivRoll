#!/usr/bin/env bash
set -euo pipefail

# ArxivRollBench 2026a-50 evaluation for commercial/API LLMs via OpenRouter.
# Task group: arxivrollbench2026a-50
# Model list refreshed on 2026-05-18 from https://openrouter.ai/api/v1/models.
#
# Required:
#   export OPENROUTER_API_KEY=...
# or keep the key in:
#   ~/privacy_secret_openrouter_API_key.txt
#
# This script is intentionally not launched by default; review model availability,
# pricing, and quota before running.

echo "HOME: ${HOME}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM_EVAL_BIN="${LM_EVAL_BIN:-${HOME}/anaconda3/envs/robench/bin/lm_eval}"
ROOT_DIR="${ROOT_DIR:-${SCRIPT_DIR}}"
LOG_DIR="${LOG_DIR:-${ROOT_DIR}/0721_newcloseAIs_2026A}"
CACHE_DIR="${CACHE_DIR:-${ROOT_DIR}/openrouter_cache_2026A}"
TASK="${TASK:-arxivrollbench2026a-50}"
OPENROUTER_BASE_URL="${OPENROUTER_BASE_URL:-https://openrouter.ai/api/v1/chat/completions}"
OPENROUTER_API_KEY_FILE="${OPENROUTER_API_KEY_FILE:-${HOME}/privacy_secret_openrouter_API_key.txt}"
DRY_RUN="${DRY_RUN:-0}"
MODEL_PART="${MODEL_PART:-all}"
LIMIT="${LIMIT:-}"
MODEL_LIMIT="${MODEL_LIMIT:-}"
MAX_GEN_TOKS="${MAX_GEN_TOKS:-}"

export TORCH_USE_CUDA_DSA="${TORCH_USE_CUDA_DSA:-1}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"

if [[ -z "${OPENROUTER_API_KEY:-}" && -r "${OPENROUTER_API_KEY_FILE}" ]]; then
    IFS= read -r OPENROUTER_API_KEY < "${OPENROUTER_API_KEY_FILE}"
fi

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
    echo "ERROR: OPENROUTER_API_KEY is not set." >&2
    exit 1
fi
export OPENAI_API_KEY="${OPENROUTER_API_KEY}"

if [[ "${DRY_RUN}" != "1" && "${CONFIRM_OPENROUTER_SPEND:-}" != "YES" ]]; then
    echo "ERROR: refusing to run paid OpenRouter evaluation without CONFIRM_OPENROUTER_SPEND=YES." >&2
    echo "Set DRY_RUN=1 to inspect commands without spending." >&2
    exit 1
fi

mkdir -p "${LOG_DIR}"
mkdir -p "${CACHE_DIR}"

# Accessible OpenRouter models from the 2026-05-18 probe.
# MODEL_PART=1 is split by a 2026-05-19 three-prompt probe:
# - 1_plain: visible text on all probe prompts, no reasoning_tokens reported.
# - 1_thinking: null visible content and/or reasoning_tokens observed.
model_part_1_plain=(
    # xAI
    "x-ai/grok-4.20"

    # DeepSeek
    "deepseek/deepseek-v3.2"
    "deepseek/deepseek-chat-v3.1"
    "deepseek/deepseek-chat-v3-0324"
)

model_part_1_thinking=(
    # xAI
    "x-ai/grok-4.3"

    # DeepSeek
    "deepseek/deepseek-v4-pro"
    "deepseek/deepseek-v4-flash"
    "deepseek/deepseek-v3.2-speciale"
    "deepseek/deepseek-r1-0528"

    # Moonshot/Kimi
    "moonshotai/kimi-k2.6"
    "moonshotai/kimi-k2.5"
)

model_part_1=("${model_part_1_plain[@]}" "${model_part_1_thinking[@]}")

model_part_2=(
    # Moonshot/Kimi
    "moonshotai/kimi-k2-thinking"
    "moonshotai/kimi-k2"

    # Qwen commercial/OpenRouter endpoints
    "qwen/qwen3.6-max-preview"
    "qwen/qwen3.6-plus"
    "qwen/qwen3.6-flash"
    "qwen/qwen3.6-35b-a3b"
    "qwen/qwen3.5-397b-a17b"
    "qwen/qwen3.5-122b-a10b"
    "qwen/qwen3.5-35b-a3b"
    "qwen/qwen3-235b-a22b"
)

case "${MODEL_PART}" in
    1)
        model_ls=("${model_part_1[@]}")
        ;;
    1_plain)
        model_ls=("${model_part_1_plain[@]}")
        ;;
    1_thinking)
        model_ls=("${model_part_1_thinking[@]}")
        ;;
    2)
        model_ls=("${model_part_2[@]}")
        ;;
    all)
        model_ls=("${model_part_1[@]}" "${model_part_2[@]}")
        ;;
    *)
        echo "ERROR: MODEL_PART must be 1, 2, or all; got '${MODEL_PART}'." >&2
        exit 1
        ;;
esac

echo "MODEL_PART: ${MODEL_PART}"
echo "MODEL_COUNT: ${#model_ls[@]}"

run_count=0
for model in "${model_ls[@]}"; do
    if [[ -n "${MODEL_LIMIT}" && "${run_count}" -ge "${MODEL_LIMIT}" ]]; then
        break
    fi
    run_count=$((run_count + 1))

    echo "current evaluation task: ${TASK}"
    echo "current evaluation model: ${model}"
    log_path="${LOG_DIR}/${model}${TASK}"
    cache_path="${CACHE_DIR}/${model//\//__}_${TASK}.sqlite"
    mkdir -p "$(dirname "${log_path}")"

    limit_args=()
    if [[ -n "${LIMIT}" ]]; then
        limit_args=(--limit "${LIMIT}")
    fi
    gen_kwargs_args=()
    if [[ -n "${MAX_GEN_TOKS}" ]]; then
        gen_kwargs_args=(--gen_kwargs "max_gen_toks=${MAX_GEN_TOKS}")
    fi

    if [[ "${DRY_RUN}" == "1" ]]; then
        echo "DRY_RUN: ${LM_EVAL_BIN} --model local-chat-completions --apply_chat_template --model_args model=${model},base_url=${OPENROUTER_BASE_URL} --tasks ${TASK} --device cuda:0 --verbosity DEBUG --log_samples --output_path ${log_path} --use_cache ${cache_path} ${gen_kwargs_args[*]} ${limit_args[*]}"
        continue
    fi

    "${LM_EVAL_BIN}" \
        --model local-chat-completions \
        --apply_chat_template \
        --model_args "model=${model},base_url=${OPENROUTER_BASE_URL}" \
        --tasks "${TASK}" \
        --device "cuda:0" \
        --verbosity DEBUG \
        --log_samples \
        --use_cache "${cache_path}" \
        "${gen_kwargs_args[@]}" \
        --output_path "${log_path}" \
        "${limit_args[@]}"
done

echo "RUNNING run_2026a_api_openrouter.sh DONE."
