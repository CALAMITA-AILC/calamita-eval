#!/bin/bash
#SBATCH --job-name=download_dataset
#SBATCH --output=./logs/job.%A.out
#SBATCH --time=04:00:00
#SBATCH --partition=lrd_all_serial
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --account=IscrC_ItaLLM_0
#SBATCH --mem=30000M

set -e

BASE_DIR=$FAST/ga_files
export TOKENIZERS_PARALLELISM=false
export HF_HOME=$BASE_DIR/huggingface
source venv/bin/activate
echo "This script has to be run only once with internet access"

MODELS=( \
    meta-llama/Llama-3.1-70B-Instruct \
    sapienzanlp/Minerva-7B-instruct-v1.0 \
    sapienzanlp/Minerva-7B-instruct-v1.0 \
    meta-llama/Llama-3.1-8B-Instruct \
)

# Download models, tokenizers, and config files
for model in "${MODELS[@]}"; do
    python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='${model}')"
done