echo "HOME: ${HOME}"
export python=${HOME}/anaconda3/envs/robench/bin/python3
# conda activate robench
export TORCH_USE_CUDA_DSA="1"
export root_dir="${HOME}/arxivSpider/eval/"
export log_dir="${root_dir}/0.4.claude/"



## set variables
export device="1"
# export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")

# export model="meta-llama/Llama-3.1-8B-Instruct"
# export model="gpt-4o"
export model_ls=("claude-3-haiku-20240307" "claude-3-5-sonnet-latest" "claude-3-opus-latest")
# export model="o1-preview-2024-09-12"
# export model="gpt-4o"
# export model="gpt-4"
# export model="gpt-3.5-turbo"
# export task="robench-2024b-testII-gen"
# export task="robench-2024b-testIII-scp-p"
# export task="tinyGSM8k"

# export log_path="${log_dir}1026_closeAI_res{model}-----{task}.log"

export task_ls=( "robench2024b_all_setcsSCP-s-50" \
 "robench2024b_all_setcsSCP-c-50" \
 "robench2024b_all_setcsSCP-p-50" \
 "robench2024b_all_setq-finSCP-s-50" \
 "robench2024b_all_setq-finSCP-c-50" \
 "robench2024b_all_setq-finSCP-p-50" \
 "robench2024b_all_setmathSCP-s-50" \
 "robench2024b_all_setmathSCP-c-50" \
 "robench2024b_all_setmathSCP-p-50" \
 "robench2024b_all_seteessSCP-s-50" \
 "robench2024b_all_seteessSCP-c-50" \
 "robench2024b_all_seteessSCP-p-50" \
 "robench2024b_all_setphysicsSCP-s-50" \
 "robench2024b_all_setphysicsSCP-c-50" \
 "robench2024b_all_setphysicsSCP-p-50" \
 "robench2024b_all_setstatSCP-s-50" \
 "robench2024b_all_setstatSCP-c-50" \
 "robench2024b_all_setstatSCP-p-50" \
 "robench2024b_all_setq-bioSCP-s-50" \
 "robench2024b_all_setq-bioSCP-c-50" \
 "robench2024b_all_setq-bioSCP-p-50" \
 "robench2024b_all_seteconSCP-s-50" \
 "robench2024b_all_seteconSCP-c-50" \
 "robench2024b_all_seteconSCP-p-50")

# export task_ls=("mmlu_pro_computer_science")
# export model_ls=("meta-llama/Llama-3.1-8B-Instruct")


for model in ${model_ls[*]}
do
    for task in ${task_ls[*]}
    do
		echo "current evaluation task ${task}"
		echo "current evaluation model: ${model}"
		export log_path="${log_dir}${model}${task}"
		
	lm_eval\
			--model anthropic-chat-completions --apply_chat_template\
			--model_args model=${model}\
			--tasks ${task}\
			--device cuda:${device}\
			--verbosity DEBUG\
			--log_samples\
			--output_path ${log_path}
    done
done

echo "RUNNING 0.4.claude_test.sh DONE."