#!/usr/bin/env bash
set -euo pipefail

# ArxivRollBench 2026a-50 evaluation for commercial/API LLMs via OpenRouter.
# Task group: arxivrollbench2026a-50
# Model list refreshed on 2026-05-18 from https://openrouter.ai/api/v1/models.
#
# Required:
#   export OPENROUTER_API_KEY=...
#
# This script is intentionally not launched by default; review model availability,
# pricing, and quota before running.

echo "HOME: ${HOME}"

LM_EVAL_BIN="${LM_EVAL_BIN:-${HOME}/anaconda3/envs/robench/bin/lm_eval}"
ROOT_DIR="${ROOT_DIR:-${HOME}/arxivSpider/eval}"
LOG_DIR="${LOG_DIR:-${ROOT_DIR}/0721_newcloseAIs_2026A}"
TASK="${TASK:-arxivrollbench2026a-50}"
OPENROUTER_BASE_URL="${OPENROUTER_BASE_URL:-https://openrouter.ai/api/v1/chat/completions}"

export TORCH_USE_CUDA_DSA="${TORCH_USE_CUDA_DSA:-1}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
    echo "ERROR: OPENROUTER_API_KEY is not set." >&2
    exit 1
fi
export OPENAI_API_KEY="${OPENROUTER_API_KEY}"

mkdir -p "${LOG_DIR}"

# Default: representative current commercial/frontier APIs plus strong cheaper
# comparison models. Remove expensive entries before running large sweeps.
model_ls=(
    # OpenAI
    "openai/gpt-5.5-pro"
    "openai/gpt-5.5"
    "openai/gpt-5.4-pro"
    "openai/gpt-5.4"
    "openai/gpt-5.4-mini"
    "openai/gpt-5.3-chat"
    "openai/gpt-5"
    "openai/gpt-5-mini"
    "openai/gpt-4o"

    # Anthropic
    "anthropic/claude-opus-4.7"
    "anthropic/claude-opus-4.7-fast"
    "anthropic/claude-sonnet-4.6"
    "anthropic/claude-opus-4.6"
    "anthropic/claude-sonnet-4.5"
    "anthropic/claude-haiku-4.5"
    "anthropic/claude-sonnet-4"
    "anthropic/claude-opus-4"

    # Google
    "google/gemini-3.1-pro-preview"
    "google/gemini-3.1-flash-lite"
    "google/gemini-2.5-pro"
    "google/gemini-2.5-flash"
    "google/gemini-2.0-flash-001"

    # xAI
    "x-ai/grok-4.3"
    "x-ai/grok-4.20"

    # DeepSeek
    "deepseek/deepseek-v4-pro"
    "deepseek/deepseek-v4-flash"
    "deepseek/deepseek-v3.2"
    "deepseek/deepseek-v3.2-speciale"
    "deepseek/deepseek-chat-v3.1"
    "deepseek/deepseek-r1-0528"
    "deepseek/deepseek-chat-v3-0324"

    # Moonshot/Kimi
    "moonshotai/kimi-k2.6"
    "moonshotai/kimi-k2.5"
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

for model in "${model_ls[@]}"; do
    echo "current evaluation task: ${TASK}"
    echo "current evaluation model: ${model}"
    log_path="${LOG_DIR}/${model}${TASK}"

    "${LM_EVAL_BIN}" \
        --model local-chat-completions \
        --apply_chat_template \
        --model_args "model=${model},base_url=${OPENROUTER_BASE_URL}" \
        --tasks "${TASK}" \
        --device "cuda:0" \
        --verbosity DEBUG \
        --log_samples \
        --output_path "${log_path}"
done

echo "RUNNING run_2026a_api_openrouter.sh DONE."
