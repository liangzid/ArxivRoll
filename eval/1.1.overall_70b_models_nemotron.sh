#!/bin/bash
######################################################################
#1.1.OVERALL_70B_MODELS --- 

# Author: XXXXXX <xxxxxx@xxxxxx>
# Copyright © 2024, XXXXXX, all rights reserved.
# Created: 18 November 2024
######################################################################

######################### Commentary ##################################
##  
######################################################################

echo "HOME: ${HOME}"
export python=${HOME}/anaconda3/envs/robench/bin/python3
source activate robench
# export TORCH_USE_CUDA_DSA="1"
export root_dir="${HOME}/arxivSpider/eval/"
export log_dir="${root_dir}/RES_OPENSOURCE/"

# export model_ls=("Qwen/Qwen2.5-72B-Instruct" "01-ai/Yi-1.5-34B-Chat" "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF" "meta-llama/Llama-3.1-70B-Instruct")
export model_ls=("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")

# export task_ls=("mmlu_pro_computer_science"\
# 		    "mmlu_college_computer_science" "mmlu_computer_security"\
# 		    "mmlu_high_school_computer_science" "mmlu_machine_learning"\
# 		    "mmlu_pro_economics" "mmlu_econometrics" "mmlu_high_school_microeconomics"\
# 		    "mmlu_high_school_macroeconomics"\
# 		    "mmlu_pro_engineering" "mmlu_electrical_engineering"\
# 		"mmlu_pro_math"\
# 		"mmlu_abstract_algebra"\
# 		"mmlu_college_mathematics"\
# 		"mmlu_elementary_mathematics"\
# 		"mmlu_formal_logic"\
# 		"mmlu_high_school_mathematics"\
# 		"gsm8k"\
# 		"gsm_plus"\
# 		"mmlu_pro_physics"\
# 		"mmlu_astronomy"\
# 		"mmlu_college_physics"\
# 		"mmlu_conceptual_physics"\
# 		"mmlu_high_school_physics"\
# 		"mmlu_pro_biology"\
# 		"mmlu_anatomy"\
# 		"mmlu_clinical_knowledge"\
# 		"mmlu_college_biology"\
# 		"mmlu_college_medicine"\
# 		"mmlu_high_school_biology"\
# 		"mmlu_pro_business"\
# 		"mmlu_business_ethics"\
# 		"mmlu_pro_math"\
# 		"mmlu_high_school_statistics"\
# 		"mmlu_pro_chemistry"\
# 		"mmlu_pro_health"\
# 		"mmlu_pro_history"\
# 		"mmlu_pro_law"\
# 		"mmlu_pro_other"\
# 		"mmlu_pro_philosophy"\
# 		"mmlu_pro_psychology"\
# 		"mmlu_other"\
# 		"mmlu_social_sciences"\
# 		"mmlu_humanities"\
# 		"mmlu_college_chemistry"\
# 		"mmlu_high_school_chemistry"\
# "mmlu_high_school_geography"\

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
# )

# export task_ls=("robench2024b_all_setcsSCP-s" \
#  "robench2024b_all_setcsSCP-c" \
#  "robench2024b_all_setcsSCP-p" \
#  "robench2024b_all_setq-finSCP-s" \
#  "robench2024b_all_setq-finSCP-c" \
#  "robench2024b_all_setq-finSCP-p" \
#  "robench2024b_all_setmathSCP-s" \
#  "robench2024b_all_setmathSCP-c" \
#  "robench2024b_all_setmathSCP-p" \
#  "robench2024b_all_seteessSCP-s" \
#  "robench2024b_all_seteessSCP-c" \
#  "robench2024b_all_seteessSCP-p" \
#  "robench2024b_all_setphysicsSCP-s" \
#  "robench2024b_all_setphysicsSCP-c" \
#  "robench2024b_all_setphysicsSCP-p" \
#  "robench2024b_all_setstatSCP-s" \
#  "robench2024b_all_setstatSCP-c" \
#  "robench2024b_all_setstatSCP-p" \
#  "robench2024b_all_setq-bioSCP-s" \
#  "robench2024b_all_setq-bioSCP-c" \
#  "robench2024b_all_setq-bioSCP-p" \
#  "robench2024b_all_seteconSCP-s" \
#  "robench2024b_all_seteconSCP-c" \
#  "robench2024b_all_seteconSCP-p")

export task_ls=("robench2024b_all_setcsSCP-s" \
 "robench2024b_all_setcsSCP-c" \
 "robench2024b_all_setcsSCP-p" \
 # "robench2024b_all_setq-finSCP-s" \
 # "robench2024b_all_setq-finSCP-c" \
 # "robench2024b_all_setq-finSCP-p" \
 # "robench2024b_all_setmathSCP-s" \
 # "robench2024b_all_setmathSCP-c" \
 "robench2024b_all_setmathSCP-p" \
 "robench2024b_all_seteessSCP-s" \
 "robench2024b_all_seteessSCP-c" \
 "robench2024b_all_seteessSCP-p" \
 "robench2024b_all_setphysicsSCP-s" \
 # "robench2024b_all_setphysicsSCP-c" \
 # "robench2024b_all_setphysicsSCP-p" \
 # "robench2024b_all_setstatSCP-s" \
 # "robench2024b_all_setstatSCP-c" \
 # "robench2024b_all_setstatSCP-p" \
 # "robench2024b_all_setq-bioSCP-s" \
 "robench2024b_all_setq-bioSCP-c" \
 # "robench2024b_all_setq-bioSCP-p" \
 # "robench2024b_all_seteconSCP-s" \
 # "robench2024b_all_seteconSCP-c" \
 # "robench2024b_all_seteconSCP-p"
 )

# export task_ls=("mmlu_pro_computer_science")
# export model_ls=("Qwen/Qwen2.5-72B-Instruct")


export CUDA_VISIBLE_DEVICES=1,2,3

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



echo "RUNNING 1.1.overall_70b_models.sh DONE."
# 1.1.overall_70b_models.sh ends here
