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

BASE_DIR=/leonardo_work/IscrC_CALAMITA
export TOKENIZERS_PARALLELISM=false
export HF_HOME=$BASE_DIR/calamita/huggingface
source venv/bin/activate
echo "This script has to be run only once with internet access"

module unload cuda
module load cuda/12.3

METRICS=( \
    bleu \
    comet \
    chrf \
)
for metric in "${METRICS[@]}"; do
    echo "Downloading metric ${metric}"
    python -c "from evaluate import load; load('${metric}')"
done

python -c "from evaluate import load; load("bleurt", module_type="metric", checkpoint="BLEURT-20")"
