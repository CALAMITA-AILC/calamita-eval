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
echo $tasks

NUM_GPUS=$SLURM_GPUS_PER_NODE
NUM_GPUS=2

accelerate launch \
    --num_machines 1 \
    --num_processes $NUM_GPUS \
    -m lm_eval --model hf \
    --model_args pretrained=${MODEL},dtype=float16,parallelize=True \
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