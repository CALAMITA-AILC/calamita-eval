"""
calamita_recalc.py

A utility script to recalculate results where the strategies implemented by lm_eval_harness 
were not satisfactory for the task.

This script reprocesses sample files produced by lm_eval_harness. Files follow the convention:
    samples_{task}-{subtask}_{timestamp}.jsonl

The script expects a "tasks/" folder containing Python files, one per task.
Each file must define a class subclassing CalamitaTask.

EXAMPLE STRUCTURE:
    ./calamita_recalc.py
    ./tasks/amelia.py
    ./tasks/dimmi.py
    ./results_calamita_2024/
        model_name/
            samples_amelia-arg-component-fewshot_2024-12-26T01-21-13.412024.jsonl
            samples_dimmi-p1-drug_interaction_2025-04-04T03-15-20.920244.jsonl

By default, the script recalculates results ONLY for tasks having a corresponding script in tasks/.

Each task script must subclass CalamitaTask and implement evaluate(subtask, samples_path).
"""

import os
import json
import importlib.util
import argparse
from calamita_task import CalamitaTask


def load_task_registry(tasks_folder='tasks'):
    registry = {}
    
    for filename in os.listdir(tasks_folder):
        if filename.endswith('.py') and not filename.startswith('_'):
            task_name = filename[:-3]
            filepath = os.path.join(tasks_folder, filename)
            
            spec = importlib.util.spec_from_file_location(task_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, CalamitaTask) and attr != CalamitaTask:
                    registry[task_name] = attr()
                    break
    
    return registry


def find_all_samples(base_path):
    for model_folder in os.listdir(base_path):
        model_path = os.path.join(base_path, model_folder)
        if not os.path.isdir(model_path):
            continue
            
        for filename in os.listdir(model_path):
            if not filename.startswith('samples_') or not filename.endswith('.jsonl'):
                continue
            
            parts = filename.replace('samples_', '').split('_')
            timestamp = '_'.join(parts[1:]).replace('.jsonl', '')
            #task_subtask = parts[0].split('-', 1)
            #task = task_subtask[0]
            #subtask = task_subtask[1] if len(task_subtask) > 1 else 'global'
            task=filename.split('samples_')[1].split('-')[0]
            subtask="-".join(filename.split('samples_')[1].split('-')[1:]).split('_20')[0]
            #print(filename)
            yield (model_folder, task, subtask, timestamp, os.path.join(model_path, filename))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples', default='results_calamita_2024')
    parser.add_argument('--output', default='calamita_results.json')
    parser.add_argument('--tasks-folder', default='tasks')
    
    args = parser.parse_args()
    
    registry = load_task_registry(args.tasks_folder)
    results = []
    
    for model, task, subtask, timestamp, filepath in find_all_samples(args.samples):
        if task not in registry:
            continue
        
        try:
            handler = registry[task]
            metrics = handler.evaluate(subtask, filepath)
            results.append({
                'model': model,
                'task': task,
                'subtask': subtask,
                'timestamp': timestamp,
                **metrics
            })
        except Exception as e:
            print(f"Errore: {model} {task} {subtask}: {e}")
    
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
