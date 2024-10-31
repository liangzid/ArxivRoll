#!/bin/bash
######################################################################
#0.1.VANILLA_HARNESS_TEST ---

# For Unit Test

# Do not execute this file.

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
export log_path="${log_dir}1026_testlog.log"
export device="1"
export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")
export llm_ls=("Qwen/Qwen2.5-72B-Instruct" "01-ai/Yi-1.5-34B-Chat" "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF" "meta-llama/Llama-3.1-70B-Instruct")

export model="01-ai/Yi-1.5-34B-Chat"
export task="robench-2024b-testII-gen"

lm_eval\
    --model hf\
    --model_args pretrained=${model}\
    --tasks ${task}\
    --device cuda:${device}\
    --verbosity DEBUG\
    --log_samples\
    --output_path ${log_path}



echo "RUNNING 0.1.vanilla_harness_test.sh DONE."
# 0.1.vanilla_harness_test.sh ends here
