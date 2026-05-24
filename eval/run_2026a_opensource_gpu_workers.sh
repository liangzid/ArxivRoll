#!/usr/bin/env bash
set -u

# Efficient 2026a open-weight run for shared multi-GPU machines.
# It runs one lm_eval process per physical GPU for single-GPU-sized models.
# Per-model failures are logged and do not stop the other queues.

LM_EVAL_BIN="${LM_EVAL_BIN:-${HOME}/anaconda3/envs/robench/bin/lm_eval}"
DATA_ROOT="${DATA_ROOT:-/data2/zi}"
TASK="${TASK:-arxivrollbench2026a}"
RESULT_ROOT="${RESULT_ROOT:-${DATA_ROOT}/arxivrollbench_results/RES_OPENSOURCE_2026A_GPU_WORKERS}"
RUN_LOG_DIR="${RUN_LOG_DIR:-${DATA_ROOT}/arxivrollbench_logs/gpu_workers_2026a}"
BATCH_SIZE="${BATCH_SIZE:-8}"
MODEL_ARGS_EXTRA="${MODEL_ARGS_EXTRA:-dtype=bfloat16,trust_remote_code=True}"
GPU_LIST="${GPU_LIST:-3 4 5}"

export HF_HOME="${HF_HOME:-${DATA_ROOT}/huggingface}"
export HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-${HF_HOME}/datasets}"
export TORCH_HOME="${TORCH_HOME:-${DATA_ROOT}/torch}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-${DATA_ROOT}/xdg_cache}"
export TORCH_USE_CUDA_DSA="${TORCH_USE_CUDA_DSA:-1}"
export TOKENIZERS_PARALLELISM="${TOKENIZERS_PARALLELISM:-false}"
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"

mkdir -p "${RESULT_ROOT}" "${RUN_LOG_DIR}" "${HF_HOME}" "${TORCH_HOME}" "${XDG_CACHE_HOME}"

# Skip older .bin-only checkpoints here; this environment blocks torch.load for
# those unless Torch is upgraded to >=2.6. Large 70B+/MoE models should be run
# in a separate sharded pass.
model_ls=(
    "microsoft/Phi-3-mini-4k-instruct"
    "microsoft/Phi-3.5-mini-instruct"
    "microsoft/Phi-4-reasoning"
    "microsoft/Phi-4-reasoning-plus"
    "meta-llama/Llama-3.1-8B"
    "meta-llama/Llama-3.1-8B-Instruct"
    "meta-llama/Llama-3.2-1B"
    "meta-llama/Llama-3.2-1B-Instruct"
    "meta-llama/Llama-3.2-3B"
    "meta-llama/Llama-3.2-3B-Instruct"
    "Qwen/Qwen2-7B-Instruct"
    "Qwen/Qwen2.5-7B"
    "Qwen/Qwen2.5-7B-Instruct"
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
    "google/gemma-3-1b-it"
    "google/gemma-3-4b-it"
    "google/gemma-3-12b-it"
    "google/gemma-3-27b-it"
    "google/gemma-4-31B-it"
    "mistralai/Mistral-7B-Instruct-v0.1"
    "mistralai/Mistral-7B-Instruct-v0.2"
    "mistralai/Mistral-7B-Instruct-v0.3"
    "01-ai/Yi-1.5-34B-Chat"
    "tiiuae/Falcon3-10B-Instruct"
    "recursal/QRWKV6-32B-Instruct-Preview-v0.1"
)

if [[ "${MODELS:-}" != "" ]]; then
    read -r -a model_ls <<< "${MODELS}"
fi

read -r -a gpu_ls <<< "${GPU_LIST}"

run_worker() {
    local worker_id="$1"
    local gpu="$2"
    local worker_log="${RUN_LOG_DIR}/worker_${worker_id}_gpu${gpu}.log"

    echo "worker ${worker_id} using physical GPU ${gpu}" | tee -a "${worker_log}"

    local i model safe_model log_path status
    for i in "${!model_ls[@]}"; do
        if (( i % ${#gpu_ls[@]} != worker_id )); then
            continue
        fi

        model="${model_ls[$i]}"
        safe_model="${model//\//__}"
        log_path="${RESULT_ROOT}/${safe_model}_${TASK}"

        {
            echo "============================================================"
            echo "timestamp: $(date -Is)"
            echo "worker: ${worker_id}"
            echo "gpu: ${gpu}"
            echo "task: ${TASK}"
            echo "model: ${model}"
            echo "output: ${log_path}"
        } >> "${worker_log}"

        CUDA_VISIBLE_DEVICES="${gpu}" "${LM_EVAL_BIN}" \
            --model hf \
            --model_args "pretrained=${model},${MODEL_ARGS_EXTRA}" \
            --tasks "${TASK}" \
            --batch_size "${BATCH_SIZE}" \
            --verbosity INFO \
            --log_samples \
            --output_path "${log_path}" \
            >> "${worker_log}" 2>&1

        status=$?
        echo "timestamp: $(date -Is) status: ${status} model: ${model}" >> "${worker_log}"
    done

    echo "worker ${worker_id} done at $(date -Is)" >> "${worker_log}"
}

echo "task: ${TASK}"
echo "gpu list: ${GPU_LIST}"
echo "results: ${RESULT_ROOT}"
echo "logs: ${RUN_LOG_DIR}"

for worker_id in "${!gpu_ls[@]}"; do
    run_worker "${worker_id}" "${gpu_ls[$worker_id]}" &
done

wait
echo "all workers done at $(date -Is)"
