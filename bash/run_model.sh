#!/bin/bash
#SBATCH --job-name=calamita
#SBATCH --output=logs/%A.out
#SBATCH --partition=boost_usr_prod
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-node=4
#SBATCH --time=04:00:00
#SBATCH --mem-per-gpu=32G
#SBATCH --account=IscrC_CALAMITA


if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <model> <tasks_file>"
	exit 1
fi

BASE_DIR=$FAST/ga_files
export TOKENIZERS_PARALLELISM=false
export HF_HOME=$BASE_DIR/huggingface
export TRANSFORMERS_OFFLINE="1"
export HF_DATASETS_OFFLINE="1"
export HF_EVALUATE_OFFLINE="1"
export BLEURT_CHECKPOINT=$BASE_DIR/BLEURT-20

source venv/bin/activate
MODEL=$1

BATCH_SIZE=auto
OUTPUT_DIR=$BASE_DIR/results_calamita

module unload cuda
module load cuda/12.3

echo Evaluating model $MODEL on tasks from $2:
tasks=$(cat $2 | tr '\n' ',' | sed 's/,$//')
echo "Total tasks: $(echo $tasks | tr ',' '\n' | wc -l)"
echo "Tasks:"
echo $tasks

NUM_GPUS=$SLURM_GPUS_PER_NODE
NUM_GPUS=4
echo "NUM_GPUS: $NUM_GPUS"

# accelerate launch \
    # --num_machines 1 \
    # --num_processes 1 \
    # -m 
# lm_eval --model hf \
    # --model_args pretrained=${MODEL},dtype=float16,parallelize=True \

# export CUDA_VISIBLE_DEVICES=0

lm_eval --model vllm \
    --model_args pretrained=${MODEL},dtype=bfloat16,gpu_memory_utilization=0.8,max_model_len=3072,tensor_parallel_size=$NUM_GPUS \
    --tasks ${tasks} \
    --output_path ${OUTPUT_DIR} \
    --batch_size $BATCH_SIZE \
    --log_samples \
    --write_out \
    --use_cache $OUTPUT_DIR/cache/${MODEL//\//__} \
    --cache_requests "true" \
    --include_path ./tasks \
    --load_local \
    --local_base_dir $BASE_DIR/local_datasets \
    --unload_lm_before_eval