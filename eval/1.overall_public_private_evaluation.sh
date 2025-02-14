#!/bin/bash
######################################################################
#1.OVERALL_PUBLIC_PRIVATE_EVALUATION --- 

# Author: XXXXXX <xxxxxx@xxxxxx>
# Copyright © 2024, XXXXXX, all rights reserved.
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

# export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")
# export model_ls=("meta-llama/Llama-2-7b-chat-hf" "meta-llama/Llama-2-13b-chat-hf" "Neko-Institute-of-Science/LLaMA-7B-HF")
export model_ls=("microsoft/phi-1" "microsoft/phi-1_5" "microsoft/phi-2" "microsoft/Phi-3-mini-4k-instruct")
# export llm_ls=("Qwen/Qwen2.5-72B-Instruct" "01-ai/Yi-1.5-34B-Chat" "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF" "meta-llama/Llama-3.1-70B-Instruct")

export task_ls=("mmlu_pro_computer_science"\
		    "mmlu_college_computer_science" "mmlu_computer_security"\
		    "mmlu_high_school_computer_science" "mmlu_machine_learning"\
		    "mmlu_pro_economics" "mmlu_econometrics" "mmlu_high_school_microeconomics"\
		    "mmlu_high_school_macroeconomics"\
		    "mmlu_pro_engineering" "mmlu_electrical_engineering"\
		"mmlu_pro_math"\
		"mmlu_abstract_algebra"\
		"mmlu_college_mathematics"\
		"mmlu_elementary_mathematics"\
		"mmlu_formal_logic"\
		"mmlu_high_school_mathematics"\
		"gsm8k"\
		"gsm_plus"\
		"mmlu_pro_physics"\
		"mmlu_astronomy"\
		"mmlu_college_physics"\
		"mmlu_conceptual_physics"\
		"mmlu_high_school_physics"\
		"mmlu_pro_biology"\
		"mmlu_anatomy"\
		"mmlu_clinical_knowledge"\
		"mmlu_college_biology"\
		"mmlu_college_medicine"\
		"mmlu_high_school_biology"\
		"mmlu_pro_business"\
		"mmlu_business_ethics"\
		"mmlu_pro_math"\
		"mmlu_high_school_statistics"\
		"mmlu_pro_chemistry"\
		"mmlu_pro_health"\
		"mmlu_pro_history"\
		"mmlu_pro_law"\
		"mmlu_pro_other"\
		"mmlu_pro_philosophy"\
		"mmlu_pro_psychology"\
		"mmlu_other"\
		"mmlu_social_sciences"\
		"mmlu_humanities"\
		"mmlu_college_chemistry"\
		"mmlu_high_school_chemistry"\
 "mmlu_high_school_geography"

# "liangzid/robench2024b_all_setcsSCP-s"\
# "liangzid/robench2024b_all_setcsSCP-c"\
# "liangzid/robench2024b_all_setcsSCP-p"\
# "liangzid/robench2024b_all_setq-finSCP-s"\
# "liangzid/robench2024b_all_setq-finSCP-c"\
# "liangzid/robench2024b_all_setq-finSCP-p"\
# "liangzid/robench2024b_all_setmathSCP-s"\
# "liangzid/robench2024b_all_setmathSCP-c"\
# "liangzid/robench2024b_all_setmathSCP-p"\
# "liangzid/robench2024b_all_seteecsSCP-s"\
# "liangzid/robench2024b_all_seteecsSCP-c"\
# "liangzid/robench2024b_all_seteecsSCP-p"\
# "liangzid/robench2024b_all_setphysicsSCP-s"\
# "liangzid/robench2024b_all_setphysicsSCP-c"\
# "liangzid/robench2024b_all_setphysicsSCP-p"\
# "liangzid/robench2024b_all_setstatSCP-s"\
# "liangzid/robench2024b_all_setstatSCP-c"\
# "liangzid/robench2024b_all_setstatSCP-p"\
# "liangzid/robench2024b_all_setq-bioSCP-s"\
# "liangzid/robench2024b_all_setq-bioSCP-c"\
# "liangzid/robench2024b_all_setq-bioSCP-p"\
# "liangzi/robench2024b_all_seteconSCP-s"\
# "liangzid/robench2024b_all_seteconSCP-c"\
# "liangzid/robench2024b_all_seteconSCP-p"

)

# export task_ls=("mmlu_pro_computer_science")
# export model_ls=("meta-llama/Llama-3.1-8B-Instruct")

export device="0"

for model in ${model_ls[*]}
do
    for task in ${task_ls[*]}
    do
	echo "current evaluation task ${task}"
	echo "current evaluation model: ${model}"
        export log_path="${log_dir}${model}${task}"

	lm_eval\
	    --model hf\
	    --model_args pretrained=${model}\
	    --tasks ${task}\
	    --device cuda:${device}\
	    --verbosity DEBUG\
	    --log_samples\
	    --output_path ${log_path}
    done
done


echo "RUNNING 1.overall_public_private_evaluation.sh DONE."
# 1.overall_public_private_evaluation.sh ends here
