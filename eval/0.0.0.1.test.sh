#!/bin/bash
######################################################################
#0.0.0.1.TEST --- 

######################################################################

######################### Commentary ##################################
##  
######################################################################


echo "HOME: ${HOME}"
export python=${HOME}/anaconda3/base/bin/python3
# source activate robench
export TORCH_USE_CUDA_DSA="1"
export root_dir="${HOME}/arxivSpider/eval/"
export log_dir="${root_dir}/RES_OPENSOURCE/"


export model_ls=("meta-llama/Llama-3.2-1B")

export task_ls=(
    arxivrollbench2024b
)

#for public
export CUDA_VISIBLE_DEVICES=2,3,4,5

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



echo "RUNNING 0.0.0.1.test.sh DONE."
# 0.0.0.1.test.sh ends here
