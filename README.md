# CALAMITA Evaluation

<div>
  <img src="/img/logo_calamita.png" alt="CALAMITA LOGO" style="width: 40%; height: auto;">
</div>

<!--
[![Paper](https://img.shields.io/badge/Paper-CLiC%20IT-red)](https://clic2024.ilc.cnr.it/wp-content/uploads/2024/12/116_calamita_preface_long.pdf)
[![Leaderboard](https://img.shields.io/badge/Leaderboard-live-yellow)](https://calamita-ailc.github.io/calamita2024/)
-->


This repository contains scripts and utilities to run and reproduce the CALAMITA results.

## Getting started

Create an isolated Python environment and install the submodule `lm-eval-harness`. We use a fork of the official lm-eval-harness offering additional functionalities, including local dataset loading, cleaning up VRAM after generation to make room for eval code that uses LLMs, and specifying custom aggregation functions. Then, install the requirements listed under `requirements.txt`.

Assuming your environment is a virtualenv/uv environment called `venv`, the commands after the env creation should resemble:

```bash
source venv/bin/activate
pip install -e './lm-eval-harness[vllm]'
pip install -r requirements.txt
```

### (optional) Prepare Files Locally

If your computing environment does not have internet access, use the two scripts `bash/download_datasets.sh` and `bash/download_models.sh` to download task data and models locally.

> [!IMPORTANT]
> Note: at the time of writing, a small number of the CALAMITA (sub)tasks are not formatted as Hugging Face datasets and require local loading. Please see the task-specific instructions below to run them.

## Running a model on a task

1. Select a list of subtasks and put them into a txt file, one per line, e.g., in a `tasks.txt` (you can find an example file in the root directory).
2. Schedule the job through SLURM, e.g.,

```bash
sbatch ./bash/run_model.sh meta-llama/Llama-3.1-70B-Instruct tasks.txt
```

If you do not use SLURM, the file `./bash/run_model.sh` requires minimal adaptation. Please open an issue if you need troubleshooting.

## Task-specific instructions

All task configurations are stored under `./tasks` in a separate folder. Each task can be composed of multiple subtasks, listed in a `group` key. For example, Eureka Rebus (`./tasks/eureka_rebus/defaul.yaml`) is composed of `eureka_original` and `eureka_hints` subtasks.
You can specify a single subtask or a group name, which will schedule all subtasks belonging to it. 

For example, to run Eureka Rebus and Abricot, including all their subtasks, create a text file as:
```txt
abricot
eureka_rebus
```

and schedule a job with the command indicated in the previous question.



