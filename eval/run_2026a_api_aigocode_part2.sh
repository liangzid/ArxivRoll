#!/usr/bin/env bash
set -euo pipefail

# ArxivRollBench 2026a-50 evaluation for Part-2 commercial/API LLMs via AiGoCode.
# AiGoCode docs:
#   OpenAI-compatible base URL: https://api.aigocode.com/v1
#   Chat completions path:     /chat/completions
#   Model list:                https://docs.aigocode.com/docs/api/models
#
# This runner uses the OpenAI-compatible chat-completions endpoint for all groups.
# Provider-specific key files are read at runtime and never printed.
#
# Required before paid runs:
#   CONFIRM_AIGOCODE_SPEND=YES
# Use DRY_RUN=1 to inspect commands without spending.

echo "HOME: ${HOME}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM_EVAL_BIN="${LM_EVAL_BIN:-${HOME}/anaconda3/envs/robench/bin/lm_eval}"
ROOT_DIR="${ROOT_DIR:-${SCRIPT_DIR}}"
LOG_DIR="${LOG_DIR:-${ROOT_DIR}/0721_newcloseAIs_2026A_AIGOCODE}"
CACHE_DIR="${CACHE_DIR:-${ROOT_DIR}/aigocode_cache_2026A}"
TASK="${TASK:-arxivrollbench2026a-50}"
AIGOCODE_BASE_URL="${AIGOCODE_BASE_URL:-https://api.aigocode.com/v1/chat/completions}"

AIGOCODE_CLAUDE_API_KEY_FILE="${AIGOCODE_CLAUDE_API_KEY_FILE:-${HOME}/mid-claude-api-keys.txt}"
AIGOCODE_OPENAI_API_KEY_FILE="${AIGOCODE_OPENAI_API_KEY_FILE:-${HOME}/mid-codex-openai-api-keys.txt}"
AIGOCODE_GEMINI_API_KEY_FILE="${AIGOCODE_GEMINI_API_KEY_FILE:-${HOME}/mid-gemini-api-keys.txt}"

DRY_RUN="${DRY_RUN:-0}"
MODEL_PART="${MODEL_PART:-2}"
MODEL_ONLY="${MODEL_ONLY:-}"
LIMIT="${LIMIT:-}"
MODEL_LIMIT="${MODEL_LIMIT:-}"
MAX_GEN_TOKS="${MAX_GEN_TOKS:-}"

export TORCH_USE_CUDA_DSA="${TORCH_USE_CUDA_DSA:-1}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"

mkdir -p "${LOG_DIR}"
mkdir -p "${CACHE_DIR}"

# Model IDs from AiGoCode docs as of 2026-05-22. Actual availability can still
# depend on each key's package, permissions, and upstream status.
model_part_2_claude=(
    "claude-opus-4-7"
    "claude-opus-4-6"
    "claude-sonnet-4-6"
    "claude-haiku-4-5-20251001"
)

model_part_2_openai=(
    "gpt-5.5"
    "gpt-5.4"
    "gpt-5.4-mini"
    "gpt-5.3-codex"
)

model_part_2_gemini=(
    "gemini-3.5-flash"
    "gemini-3.1-pro-preview"
    "gemini-3-flash-preview"
)

model_part_2=(
    "${model_part_2_claude[@]}"
    "${model_part_2_openai[@]}"
    "${model_part_2_gemini[@]}"
)

provider_for_model() {
    local model="$1"
    case "${model}" in
        claude-*) echo "claude" ;;
        gpt-*) echo "openai" ;;
        gemini-*) echo "gemini" ;;
        *)
            echo "ERROR: cannot infer AiGoCode provider for model '${model}'." >&2
            return 1
            ;;
    esac
}

key_file_for_provider() {
    local provider="$1"
    case "${provider}" in
        claude) echo "${AIGOCODE_CLAUDE_API_KEY_FILE}" ;;
        openai) echo "${AIGOCODE_OPENAI_API_KEY_FILE}" ;;
        gemini) echo "${AIGOCODE_GEMINI_API_KEY_FILE}" ;;
        *)
            echo "ERROR: unknown provider '${provider}'." >&2
            return 1
            ;;
    esac
}

env_key_for_provider() {
    local provider="$1"
    case "${provider}" in
        claude) echo "${AIGOCODE_CLAUDE_API_KEY:-}" ;;
        openai) echo "${AIGOCODE_OPENAI_API_KEY:-}" ;;
        gemini) echo "${AIGOCODE_GEMINI_API_KEY:-}" ;;
        *)
            echo "ERROR: unknown provider '${provider}'." >&2
            return 1
            ;;
    esac
}

read_key_for_provider() {
    local provider="$1"
    local key
    key="$(env_key_for_provider "${provider}")"
    if [[ -z "${key}" ]]; then
        local key_file
        key_file="$(key_file_for_provider "${provider}")"
        if [[ ! -r "${key_file}" ]]; then
            echo "ERROR: key file for provider '${provider}' is not readable: ${key_file}" >&2
            return 1
        fi
        IFS= read -r key < "${key_file}"
    fi
    if [[ -z "${key}" ]]; then
        echo "ERROR: empty API key for provider '${provider}'." >&2
        return 1
    fi
    printf '%s' "${key}"
}

case "${MODEL_PART}" in
    2|all)
        model_ls=("${model_part_2[@]}")
        ;;
    2_claude|claude)
        model_ls=("${model_part_2_claude[@]}")
        ;;
    2_openai|openai)
        model_ls=("${model_part_2_openai[@]}")
        ;;
    2_gemini|gemini)
        model_ls=("${model_part_2_gemini[@]}")
        ;;
    *)
        echo "ERROR: MODEL_PART must be 2, all, 2_claude, 2_openai, or 2_gemini; got '${MODEL_PART}'." >&2
        exit 1
        ;;
esac

echo "MODEL_PART: ${MODEL_PART}"
echo "AIGOCODE_BASE_URL: ${AIGOCODE_BASE_URL}"

if [[ -n "${MODEL_ONLY}" ]]; then
    filtered_model_ls=()
    for model in "${model_ls[@]}"; do
        if [[ "${model}" == "${MODEL_ONLY}" ]]; then
            filtered_model_ls+=("${model}")
        fi
    done
    if [[ "${#filtered_model_ls[@]}" -eq 0 ]]; then
        echo "ERROR: MODEL_ONLY='${MODEL_ONLY}' is not in MODEL_PART='${MODEL_PART}'." >&2
        exit 1
    fi
    model_ls=("${filtered_model_ls[@]}")
fi

echo "MODEL_ONLY: ${MODEL_ONLY:-<unset>}"
echo "MODEL_COUNT: ${#model_ls[@]}"

if [[ "${DRY_RUN}" != "1" && "${CONFIRM_AIGOCODE_SPEND:-}" != "YES" ]]; then
    echo "ERROR: refusing to run paid AiGoCode evaluation without CONFIRM_AIGOCODE_SPEND=YES." >&2
    echo "Set DRY_RUN=1 to inspect commands without spending." >&2
    exit 1
fi

run_count=0
for model in "${model_ls[@]}"; do
    if [[ -n "${MODEL_LIMIT}" && "${run_count}" -ge "${MODEL_LIMIT}" ]]; then
        break
    fi
    run_count=$((run_count + 1))

    provider="$(provider_for_model "${model}")"
    echo "current evaluation task: ${TASK}"
    echo "current evaluation provider: ${provider}"
    echo "current evaluation model: ${model}"

    log_path="${LOG_DIR}/${provider}/${model}${TASK}"
    cache_path="${CACHE_DIR}/${provider}__${model//\//__}_${TASK}.sqlite"
    mkdir -p "$(dirname "${log_path}")"

    limit_args=()
    if [[ -n "${LIMIT}" ]]; then
        limit_args=(--limit "${LIMIT}")
    fi

    gen_kwargs_args=()
    if [[ -n "${MAX_GEN_TOKS}" ]]; then
        gen_kwargs_args=(--gen_kwargs "max_gen_toks=${MAX_GEN_TOKS}")
    fi
    model_args="model=${model},base_url=${AIGOCODE_BASE_URL}"
    if [[ "${provider}" == "claude" ]]; then
        model_args="${model_args},omit_temperature=True"
    fi

    if [[ "${DRY_RUN}" == "1" ]]; then
        echo "DRY_RUN: provider=${provider} ${LM_EVAL_BIN} --model local-chat-completions --apply_chat_template --model_args ${model_args} --tasks ${TASK} --device cuda:0 --verbosity DEBUG --log_samples --use_cache ${cache_path} --output_path ${log_path} ${gen_kwargs_args[*]} ${limit_args[*]}"
        continue
    fi

    provider_key="$(read_key_for_provider "${provider}")"
    export OPENAI_API_KEY="${provider_key}"

    "${LM_EVAL_BIN}" \
        --model local-chat-completions \
        --apply_chat_template \
        --model_args "${model_args}" \
        --tasks "${TASK}" \
        --device "cuda:0" \
        --verbosity DEBUG \
        --log_samples \
        --use_cache "${cache_path}" \
        "${gen_kwargs_args[@]}" \
        --output_path "${log_path}" \
        "${limit_args[@]}"
done

echo "RUNNING run_2026a_api_aigocode_part2.sh DONE."
