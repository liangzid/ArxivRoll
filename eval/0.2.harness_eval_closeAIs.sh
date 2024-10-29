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
source activate robench
export TORCH_USE_CUDA_DSA="1"
export root_dir="${HOME}/arxivSpider/eval/"
export log_dir="${root_dir}/logs/"

## set variables
export log_path="${log_dir}1026_closeAI_res.log"
export device="1"
# export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")

# export model="meta-llama/Llama-3.1-8B-Instruct"
export model="gpt-4o-mini"
# export task="robench-2024b-testII-gen"
export task="tinyGSM8k"


    # --model openai-completions\
proxychains lm_eval\
    --model openai-chat-completions\
    --model_args model=${model}\
    --apply_chat_template\
    --tasks ${task}\
    --device cuda:${device}\
    --verbosity DEBUG\
    --log_samples\
    --output_path ${log_path}



echo "RUNNING 0.2.harness_eval_closeAIs.sh DONE."
# 0.2.harness_eval_closeAIs.sh ends here
