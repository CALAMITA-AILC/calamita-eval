# CALAMITA Evaluation

<div>
  <img src="/img/logo_calamita.png" alt="CALAMITA LOGO" style="width: 40%; height: auto;">
</div>

[![Paper](https://img.shields.io/badge/Paper-CLiC%20IT-red)](https://clic2024.ilc.cnr.it/wp-content/uploads/2024/12/116_calamita_preface_long.pdf)
[![Leaderboard](https://img.shields.io/badge/Leaderboard-live-yellow)](https://calamita-ailc.github.io/calamita2024/)

This repository contains scripts and utilities to run and reproduce the CALAMITA results.

## Getting started

Create an isolated python environment and install the submodule `lm-eval-harness`.
This repository is a fork of the official lm-eval-harness that supports neat additional functionalities, e.g., running tasks on local datasets, cleaning up VRAM after generation to make room for eval code that uses LLMs, specify custom aggregation functions.
Then, install the requirements listed under `requirements.txt`.

```bash
pip install -e './lm-eval-harness[vllm]'
pip install -r requirements.txt
```


### (optional) Prepare Files Locally

If your computing environment does not have internet access, use the two scripts `bash/download_datasets.sh` and `bash/download_models.sh` to download task data and models locally.

> [!IMPORTANT]
> Note that some CALAMITA 2024 tasks require private data not accessible online. For full reproducibility, get in touch with the task authors and request for those files.

## Running a model on a task

1. Select a list of subtasks and put them into a txt file, one per line, e.g., in a `tasks.txt` (you can find an example file in the root directory).
2. Schedule the job through SLURM, e.g.,

```bash
sbatch ./bash/run_model meta-llama/Llama-3.1-70B-Instruct tasks.txt
```

