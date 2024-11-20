
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

export model_ls=("EleutherAI/gpt-j-6B" "microsoft/Phi-3.5-mini-instruct" "Qwen/Qwen2-7B-Instruct" "meta-llama/Meta-Llama-3-8B" "meta-llama/Llama-3.1-8B-Instruct")

export task_ls=("robench2024b_all_setcsSCP-s" \
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
"liangzi/robench2024b_all_seteconSCP-s" \
"robench2024b_all_seteconSCP-c" \
"robench2024b_all_seteconSCP-p")

# export task_ls=("mmlu_pro_computer_science")
# export model_ls=("meta-llama/Llama-3.1-8B-Instruct")

export device="3"

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
