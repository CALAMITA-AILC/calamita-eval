#!/bin/bash

module unload cuda
module load cuda

BASE_DIR=/leonardo_work/IscrC_CALAMITA
export HF_HOME=$BASE_DIR/calamita/huggingface

source venv/bin/activate

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Error: Both arguments must be provided."
    echo "Usage: $0 <start_task> <task_file>"
    exit 1
fi


echo Downloading all datasets for tasks from $1 to $2:
tasks=$(cat $1 | tr '\n' ',' | sed 's/,$//')
echo $tasks

mkdir -p $2

python lm-evaluation-harness/scripts/save_local.py \
    --tasks $tasks \
    --include_path tasks \
    --local_base_dir $2