#!/bin/bash
######################################################################
######################################################################

######################### Commentary ##################################
##  
######################################################################


echo "HOME: ${HOME}"
export python=${HOME}/anaconda3/envs/robench/bin/python3
# conda activate robench
export TORCH_USE_CUDA_DSA="1"
export root_dir="${HOME}/arxivSpider/eval/"
export log_dir="${root_dir}/0721_newcloseAIs/"


## set variables
export device="1"

export model_ls=(
    "anthropic/claude-3.5-sonnet" \
	"anthropic/claude-3.7-sonnet" \
	"anthropic/claude-sonnet-4" \
	"anthropic/claude-opus-4" \
	"google/gemini-2.0-flash-001" \
	"google/gemini-2.5-flash" \
	"google/gemini-2.5-pro" \
	"deepseek/deepseek-chat-v3-0324" \
	"deepseek/deepseek-r1-0528" \
	"moonshotai/kimi-k2" \
	)

# echo "OPENROUTER_API_KEY: ${OPENROUTER_API_KEY}"

# export model_ls=("deepseek/deepseek-chat-v3-0324")

# export log_path="${log_dir}1026_closeAI_res{model}-----{task}.log"

# export task_ls=( 
#  "robench2024b_all_setcsSCP-s-50" \
#  )

export task_ls=( 
 "robench2024b_all_setcsSCP-s-50" \
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
 "robench2024b_all_setstatSCP-s-50" 
 "robench2024b_all_setstatSCP-c-50" \
 "robench2024b_all_setstatSCP-p-50" \
 "robench2024b_all_setq-bioSCP-s-50" \
 "robench2024b_all_setq-bioSCP-c-50" \
 "robench2024b_all_setq-bioSCP-p-50" \
 "robench2024b_all_seteconSCP-s-50" \
 "robench2024b_all_seteconSCP-c-50" \
  "robench2024b_all_seteconSCP-p-50"
 )

# export task_ls=("mmlu_pro_computer_science")
# export model_ls=("meta-llama/Llama-3.1-8B-Instruct")

                        # --apply_chat_template\
# chat-

for model in ${model_ls[*]}
do
    for task in ${task_ls[*]}
    do
		echo "current evaluation task ${task}"
		echo "current evaluation model: ${model}"
		export log_path="${log_dir}${model}${task}"
		export OPENAI_API_KEY=${OPENROUTER_API_KEY}
	lm_eval\
			--model local-chat-completions\
                        --apply_chat_template\
			--model_args model=${model},base_url="https://openrouter.ai/api/v1/chat/completions"\
			--tasks ${task}\
			--device cuda:${device}\
			--verbosity DEBUG\
			--log_samples\
			--output_path ${log_path}
    done
done




echo "RUNNING 0.2.harness_eval_closeAIs.sh DONE."
# 0.2.harness_eval_closeAIs.sh ends here









