
#!/bin/bash
######################################################################
#1.OVERALL_PUBLIC_PRIVATE_EVALUATION --- 

# Author: Zi Liang <zi1415926.liang@connect.polyu.hk>
# Copyright © 2024, ZiLiang, all rights reserved.
# Created: 13 November 2024
######################################################################

######################### Commentary ##################################
##  
######################################################################

echo "HOME: ${HOME}"
export python=${HOME}/anaconda3/envs/robench/bin/python3
source activate robench
export TORCH_USE_CUDA_DSA="1"
export root_dir="${HOME}/arxivSpider/eval/"
export log_dir="${root_dir}/RES_OPENSOURCE/"

#export model_ls=("microsoft/phi-1" "microsoft/phi-1_5" "microsoft/phi-2" "microsoft/Phi-3-mini-4k-instruct")
#export model_ls=("meta-llama/Llama-2-7b-chat-hf" "meta-llama/Llama-2-13b-chat-hf" "Neko-Institute-of-Science/LLaMA-7B-HF")
#export model_ls=("Qwen/Qwen2.5-7B-Instruct" "meta-llama/Llama-3.2-3B-Instruct")

#export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")
# export model_ls=("EleutherAI/gpt-j-6B" "microsoft/phi-1" "microsoft/phi-1_5" "microsoft/phi-2" "microsoft/Phi-3-mini-4k-instruct" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "Qwen/Qwen2.5-7B-Instruct" "meta-llama/Llama-2-7b-chat-hf" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")
#export model_ls=("princeton-nlp/gemma-2-9b-it-SimPO" "ai21labs/AI21-Jamba-1.5-Mini" "mistralai/Mistral-7B-Instruct-v0.2" "Qwen/Qwen1.5-7B-Chat" "HuggingFaceH4/zephyr-7b-beta" "mistralai/Mistral-7B-Instruct-v0.1")
#export model_ls=("Qwen/QwQ-32B-Preview" "meta-llama/Llama-3.2-1B-Instruct"  "meta-llama/Llama-3.2-3B-Instruct" "meta-llama/Llama-3.3-70B-Instruct" "mistralai/Mistral-7B-Instruct-v0.1" "mistralai/Mistral-7B-Instruct-v0.2" "mistralai/Mistral-7B-Instruct-v0.3" "mistralai/Mixtral-8x7B-Instruct-v0.1" "deepseek-ai/DeepSeek-V2.5-1210" "tiiuae/Falcon3-10B-Instruct" "recursal/QRWKV6-32B-Instruct-Preview-v0.1")

export model_ls=("meta-llama/Llama-3.2-1B-Instruct"  "meta-llama/Llama-3.2-3B-Instruct" "mistralai/Mistral-7B-Instruct-v0.1" "mistralai/Mistral-7B-Instruct-v0.2" "mistralai/Mistral-7B-Instruct-v0.3" "tiiuae/Falcon3-10B-Instruct")

# export task_ls=(
# 	"mmlu_pro_computer_science"\
# 	"mmlu_college_computer_science" "mmlu_computer_security"\
# 	"mmlu_high_school_computer_science" "mmlu_machine_learning"\
# 	"mmlu_pro_economics" "mmlu_econometrics" "mmlu_high_school_microeconomics"\
# 	"mmlu_high_school_macroeconomics"\
# 	"mmlu_pro_engineering" "mmlu_electrical_engineering"\
# 	"mmlu_pro_math"\
# 	"mmlu_abstract_algebra"\
# 	"mmlu_college_mathematics"\
# 	"mmlu_elementary_mathematics"\
# 	"mmlu_formal_logic"\
# 	"mmlu_high_school_mathematics"\
# 	"gsm8k"\
# 	"gsm_plus"\
# 	"mmlu_pro_physics"\
# 	"mmlu_astronomy"\
# 	"mmlu_college_physics"\
# 	"mmlu_conceptual_physics"\
# 	"mmlu_high_school_physics"\
# 	"mmlu_pro_biology"\
# 	"mmlu_anatomy"\
# 	"mmlu_clinical_knowledge"\
# 	"mmlu_college_biology"\
# 	"mmlu_college_medicine"\
# 	"mmlu_high_school_biology"\
# 	"mmlu_pro_business"\
# 	"mmlu_business_ethics"\
# 	"mmlu_pro_math"\
# 	"mmlu_high_school_statistics"\
# 	"mmlu_pro_chemistry"\
# 	"mmlu_pro_health"\
# 	"mmlu_pro_history"\
# 	"mmlu_pro_law"\
# 	"mmlu_pro_other"\
# 	"mmlu_pro_philosophy"\
# 	"mmlu_pro_psychology"\
# 	"mmlu_other"\
# 	"mmlu_social_sciences"\
# 	"mmlu_humanities"\
# 	"mmlu_college_chemistry"\
# 	"mmlu_high_school_chemistry"\
# 	"mmlu_high_school_geography"
# )


export task_ls=(
    "robench2024b_all_setcsSCP-s" \
    "robench2024b_all_setcsSCP-c" \
    "robench2024b_all_setcsSCP-p" \
    "robench2024b_all_setq-finSCP-s" \
    "robench2024b_all_setq-finSCP-c" \
    "robench2024b_all_setq-finSCP-p" \
    "robench2024b_all_setmathSCP-s" \
    "robench2024b_all_setmathSCP-c" \
    "robench2024b_all_setmathSCP-p" \
    "robench2024b_all_seteessSCP-s" \
    "robench2024b_all_seteessSCP-c" \
    "robench2024b_all_seteessSCP-p" \
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
    "robench2024b_all_seteconSCP-p" 
)


# export task_ls=("mmlu_pro_computer_science")
# export model_ls=("meta-llama/Llama-3.1-8B-Instruct")


# for private
# export device="0"

# for model in ${model_ls[*]}
# do
#     for task in ${task_ls[*]}
#     do
# 	echo "current evaluation task ${task}"
# 	echo "current evaluation model: ${model}"
#         export log_path="${log_dir}${model}${task}"

# 	lm_eval\
# 	    --model hf\
# 	    --model_args pretrained=${model}\
# 	    --tasks ${task}\
# 	    --device cuda:${device}\
# 	    --verbosity DEBUG\
# 	    --log_samples\
# 	    --output_path ${log_path}
#     done
# done

#for public
export CUDA_VISIBLE_DEVICES=3

for model in ${model_ls[*]}
do
    for task in ${task_ls[*]}
    do
	echo "current evaluation task ${task}"
	echo "current evaluation model: ${model}"
        export log_path="${log_dir}${model}${task}"

	lm_eval\
	    --model hf\
	    --model_args pretrained=${model},parallelize=True\
	    --tasks ${task}\
	    --verbosity DEBUG\
	    --log_samples\
	    --output_path ${log_path}
    done
done

echo "RUNNING 1.overall_public_private_evaluation.sh DONE."
# 1.overall_public_private_evaluation.sh ends here
