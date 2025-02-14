#!/bin/bash
######################################################################
#0.1.TEST_LATEXVERSION --- 

# Author: XXXXXX <xxxxxx@xxxxxx>
# Copyright © 2024, XXXXXX, all rights reserved.
# Created:  7 November 2024
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
# export device="1"
export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")
# export llm_ls=("Qwen/Qwen2.5-72B-Instruct" "01-ai/Yi-1.5-34B-Chat" "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF" "meta-llama/Llama-3.1-70B-Instruct")

# # export model="01-ai/Yi-1.5-34B-Chat"
# export device="7"
# export model="meta-llama/Llama-3.1-8B-Instruct"
# export task="robench-2024b-test-latex-P"
# export log_path="${log_dir}1026_testlog-latex-P${model}${task}.log"

# lm_eval\
#     --model hf\
#     --model_args pretrained=${model}\
#     --tasks ${task}\
#     --device cuda:${device}\
#     --verbosity DEBUG\
#     --log_samples\
#     --output_path ${log_path}


export models=("gpt-4o" "gpt-4" "gpt-3.5-turbo" "o1-preview")
export model="gpt-4o"
# export model="gpt-4"
# export model="gpt-3.5-turbo"
export task="robench-2024b-test-latex-P"

export log_path="${log_dir}1026_closeAI_res{model}-----{task}.log"
# this will raise an error, because lm_eval doesn't support o1 now.
# now supported. But hte results is not that fullfilment.

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



echo "RUNNING 0.1.test_latexversion.sh DONE."
# 0.1.test_latexversion.sh ends here
