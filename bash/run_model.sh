#!/bin/bash
#SBATCH --job-name=calamita
#SBATCH --output=logs/%A.out
#SBATCH --partition=boost_usr_prod
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-node=4
#SBATCH --time=01:00:00
#SBATCH --mem-per-gpu=32G
#SBATCH --account=IscrC_CALAMITA


if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <model> <tasks_file>"
	exit 1
fi

BASE_DIR=/leonardo_work/IscrC_CALAMITA
export TOKENIZERS_PARALLELISM=false
export HF_HOME=$BASE_DIR/calamita/huggingface
export TRANSFORMERS_OFFLINE="1"
export HF_DATASETS_OFFLINE="1"

source venv/bin/activate
MODEL=$1

BATCH_SIZE=1
OUTPUT_DIR=$BASE_DIR/tests_calamita

module unload cuda
module load cuda/12.3

echo Evaluating model $MODEL on tasks from $2:
tasks=$(cat $2 | tr '\n' ',' | sed 's/,$//')
echo "Total tasks: $(echo $tasks | tr ',' '\n' | wc -l)"
echo "Tasks:"
echo $tasks

NUM_GPUS=$SLURM_GPUS_PER_NODE
echo "NUM_GPUS: $NUM_GPUS"

# accelerate launch \
    # --num_machines 1 \
    # --num_processes 1 \
    # -m 
# lm_eval --model lm \
#     --model_args pretrained=${MODEL},dtype=float16,parallelize=True \
lm_eval --model vllm \
    --model_args pretrained=${MODEL},dtype=float16,tensor_parallel_size=$NUM_GPUS,gpu_memory_utilization=0.9,max_model_len=2048 \
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
    --limit 100