#!/usr/bin/env bash
set -euo pipefail

unset TRANSFORMERS_CACHE

export DATA_ROOT=/data2/zi
export HF_HOME=/home/zi/.cache/huggingface
export HF_DATASETS_CACHE=/data2/zi/huggingface/datasets
export TORCH_HOME=/data2/zi/torch
export XDG_CACHE_HOME=/data2/zi/xdg_cache
export HF_HUB_DISABLE_XET=1

export GPU_LIST="3 4 5"
export TASK=arxivrollbench2026a
export BATCH_SIZE=8
export RESULT_ROOT=/data2/zi/arxivrollbench_results/RES_OPENSOURCE_2026A_QWEN_FIXED_BS8
export RUN_LOG_DIR=/data2/zi/arxivrollbench_logs/qwen_fixed_bs8_workers_2026a
export LM_EVAL_BIN=/home/zi/anaconda3/envs/robench/bin/lm_eval

export MODELS="Qwen/Qwen2.5-7B-Instruct Qwen/Qwen2.5-7B Qwen/Qwen2-7B-Instruct Qwen/Qwen2.5-Math-7B Qwen/Qwen2.5-Math-7B-Instruct Qwen/Qwen3-4B Qwen/Qwen3-8B Qwen/Qwen3-14B Qwen/Qwen3-32B Qwen/Qwen3.5-9B"

exec /home/zi/ArxivRollBench/arxivSpider/eval/run_2026a_opensource_gpu_workers.sh
