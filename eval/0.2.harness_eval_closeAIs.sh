#!/bin/bash
######################################################################
#0.2.HARNESS_EVAL_CLOSEAIS ---

# test the efficacy of close AIs.

# Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
# Copyright © 2024, ZiLiang, all rights reserved.
# Created: 26 October 2024
######################################################################

######################### Commentary ##################################
##  
######################################################################


echo "HOME: ${HOME}"
export python=${HOME}/anaconda3/envs/robench/bin/python3
# conda activate robench
export TORCH_USE_CUDA_DSA="1"
export root_dir="${HOME}/arxivSpider/eval/"
export log_dir="${root_dir}/0.2.closeAIs/"



## set variables
export device="1"
# export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")

# export model="meta-llama/Llama-3.1-8B-Instruct"
# export model="gpt-4o"
export model_ls=("gpt-4" "gpt-3.5-turbo" "o1-preview" "gpt-4o")
# export model="o1-preview-2024-09-12"
# export model="gpt-4o"
# export model="gpt-4"
# export model="gpt-3.5-turbo"
# export task="robench-2024b-testII-gen"
# export task="robench-2024b-testIII-scp-p"
# export task="tinyGSM8k"

# export log_path="${log_dir}1026_closeAI_res{model}-----{task}.log"

export task_ls=( "robench2024b_all_setcsSCP-s" \
 "robench2024b_all_setcsSCP-c" \
 "robench2024b_all_setcsSCP-p" \
 "robench2024b_all_setq-finSCP-s" \
 "robench2024b_all_setq-finSCP-c" \
 "robench2024b_all_setq-finSCP-p" \
 "robench2024b_all_setmathSCP-s" \
 "robench2024b_all_setmathSCP-c" \
 "robench2024b_all_setmathSCP-p" \
 "robench2024b_all_seteecsSCP-s" \
 "robench2024b_all_seteecsSCP-c" \
 "robench2024b_all_seteecsSCP-p" \
 "robench2024b_all_setphysicsSCP-s" \
 "robench2024b_all_setphysicsSCP-c" \
 "robench2024b_all_setphysicsSCP-p" \
 "robench2024b_all_setstatSCP-s" \
 "robench2024b_all_setstatSCP-c" \
 "robench2024b_all_setstatSCP-p" \
 "robench2024b_all_setq-bioSCP-s" \
 "robench2024b_all_setq-bioSCP-c" \
 "robench2024b_all_setq-bioSCP-p" \
 "robench2024b_all_seteconSCP-s" \
 "robench2024b_all_seteconSCP-c" \
 "robench2024b_all_seteconSCP-p")

# export task_ls=("mmlu_pro_computer_science")
# export model_ls=("meta-llama/Llama-3.1-8B-Instruct")


for model in ${model_ls[*]}
do
    for task in ${task_ls[*]}
    do
		echo "current evaluation task ${task}"
		echo "current evaluation model: ${model}"
		export log_path="${log_dir}${model}${task}"
	proxychains lm_eval\
			--model openai-chat-completions\
                        --apply_chat_template\
			--model_args model=${model}\
			--tasks ${task}\
			--device cuda:${device}\
			--verbosity DEBUG\
			--log_samples\
			--output_path ${log_path}
    done
done




echo "RUNNING 0.2.harness_eval_closeAIs.sh DONE."
# 0.2.harness_eval_closeAIs.sh ends here
