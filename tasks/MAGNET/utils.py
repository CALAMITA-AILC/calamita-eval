import datasets

from evaluate import load
import os
import numpy as np
from tqdm import tqdm
from functools import partial

# bleu_metric = load("bleu")
# chrf_metric = load("chrf")
# comet_metric = load("comet")
# bleurt = load("bleurt", module_type="metric", checkpoint="BLEURT-20")

def preprocess_dataset(dataset: datasets.Dataset) -> datasets.Dataset:
    # dataset = dataset.select([i for i in range(4)])      # selecting 4 rows for DEBUG
    return dataset


# post-processing the results
def _search_delimiters(model_output: str) -> str:
    left_delimiter = '<'
    right_delimiter = '>'
    start: int = 0
    end: int = len(model_output)
    if left_delimiter in model_output:
        start = model_output.find(left_delimiter)
    if right_delimiter in model_output:
        end = model_output.find(right_delimiter)

    if len(model_output) < 1:
        return "---"  # empty string as a replacement
    return model_output[start:end].replace('<', '').replace('>', '').strip()

def _check_error_input(whatever_str):
    """
    Returns True if the input is not valid (empty or None)
    """
    if whatever_str:
        if len(whatever_str) < 1:
            return True
    else:
        return True
    return False


def single_bleu(ref: str, pred: str) -> float:
    # interrupt and return lowest score
    if _check_error_input(ref):
        print(f"Error with: {ref = }")
        return 0
    if _check_error_input(pred):
        print(f"Error with: {pred = }")
        return 0

    bleu_metric = load("bleu")
    bleu_score = bleu_metric.compute(predictions=[pred], references=[[ref]])
    return bleu_score["bleu"]

def sigle_chrf(ref: str, pred: str) -> float:
    # interrupt and return lowest score
    if _check_error_input(ref):
        print(f"Error with: {ref = }")
        return 0
    if _check_error_input(pred):
        print(f"Error with: {pred = }")
        return 0
    chrf_metric = load("chrf")
    chrf_score = chrf_metric.compute(predictions=[pred], references=[[ref]])
    return chrf_score["score"]


def single_bleurt(ref: str, pred: str) -> float:
    # interrupt and return lowest score
    if _check_error_input(ref):
        print(f"Error with: {ref = }")
        return 0
    if _check_error_input(pred):
        print(f"Error with: {pred = }")
        return 0
    
    try:
        from bleurt import score
        checkpoint = os.getenv("BLEURT_CHECKPOINT")
        bleurt_scorer = score.BleurtScorer(checkpoint)
        bleurt_type = "official"
    except ImportError:
        bleurt_scorer = load("bleurt", module_type="metric", checkpoint="BLEURT-20")
        bleurt_type = "evaluate"
    
    if bleurt_type == "official":    
        scores = bleurt_scorer.score(references=[ref], candidates=[pred])
        score = scores[0]
    else:
        result = bleurt_scorer.compute(predictions=[pred], references=[ref])
        score = result["scores"][0]
    return score

def single_comet(source: str, ref: str, pred: str) -> float:
    # interrupt and return lowest score
    if _check_error_input(source):
        print(f"Error with: {source = }")
        return 0
    if _check_error_input(ref):
        print(f"Error with: {ref = }")
        return 0
    if _check_error_input(pred):
        print(f"Error with: {pred = }")
        return 0
    comet_metric = load("comet")
    comet_score = comet_metric.compute(predictions=[pred], references=[ref], sources=[source])
    return comet_score["scores"][0]


# def _get_metrics(
#     model_input: str,
#     reference_out: str,
#     completition: str
#     ) -> dict[str, float]:
#     """
#     Compute the metrics for the MT_CALAMITA task
#     """

#     # clean completion
#     completition = _search_delimiters(completition)

#     # BLEU
#     bleu_score = single_bleu(ref=reference_out, pred=completition)
#     # CHRF
#     chrf_score = sigle_chrf(ref=reference_out, pred=completition)
#     # BLEURT
#     bleurt_score = single_bleurt(ref=reference_out, pred=completition)
#     # COMET
#     comet_score = single_comet(source=model_input, ref=reference_out, pred=completition)

#     return {
#         "bleu_score": bleu_score,
#         "chrf_score": chrf_score,
#         "bleurt_score": bleurt_score,
#         "comet_score": comet_score,
#     }


# def process_results_it_en(doc, results):
#     """
#     Process the results of the model and return the metrics. Implementation for the **italian to english** task
#     Args:
#         - doc: the document containing the input and output (keys are the variables from the prompt_template)
#         - results: the output of the model (still dunnow why its a list but it doesn't depend on the batchsize)
#     Returns:
#         - a dictionary containing the metrics (metric_name: metric_value)
#     """

#     completion = results[0]
#     model_input, reference_out = doc["italian"], doc["english"]

#     return _get_metrics(
#         model_input=model_input, 
#         reference_out=reference_out, 
#         completition=completion,
#     )

def process_results(doc, results, src_col, ref_col):
    """
    Process the results of the model and return the metrics. Implementation for the **english to italian** task
    Args:
        - doc: the document containing the input and output (keys are the variables from the prompt_template)
        - results: the output of the model (still dunnow why its a list but it doesn't depend on the batchsize)
    Returns:
        - a dictionary containing the metrics (metric_name: metric_value)
    """

    completion = results[0]
    model_input, reference_out = doc[src_col], doc[ref_col]
    items = [reference_out, completion, model_input]
    items = [
        i if i is not None else "" for i in items
    ]

    return {
        "bleu": items[:2],
        "chrf": items[:2],
        "comet_22_da": items,
        "bleurt": items[:2],
    }


process_results_en_it = partial(process_results, src_col="english", ref_col="italian")
process_results_it_en = partial(process_results, src_col="italian", ref_col="english")


def bleurt_agg(items):
    from bleurt_pytorch import BleurtConfig, BleurtForSequenceClassification, BleurtTokenizer
    import torch

    config = BleurtConfig.from_pretrained("lucadiliello/BLEURT-20")
    model = BleurtForSequenceClassification.from_pretrained("lucadiliello/BLEURT-20")
    tokenizer = BleurtTokenizer.from_pretrained("lucadiliello/BLEURT-20")
    model.eval()

    refs = list(zip(*items))[0]
    preds = list(zip(*items))[1]
    batch_size = 4
    ref_batches = np.array_split(refs, len(refs) // batch_size)
    pred_batches = np.array_split(preds, len(preds) // batch_size)

    with torch.no_grad():
        results = list()
        for ref_batch, pred_batch in tqdm(zip(ref_batches, pred_batches), desc="Batch BLEURT", total=len(ref_batches)):
            inputs = tokenizer(list(ref_batch), list(pred_batch), padding='longest', return_tensors='pt')
            # move the inputs to the GPU
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
            # compute the logits
            res = model(**inputs).logits.flatten().tolist()
            results.extend(res)

    return np.mean(results)


def bleurt(items):  # This is a passthrough function
    return items


def comet_22_da_agg(items):
    from comet import download_model, load_from_checkpoint
    import torch
    
    model_path = download_model("Unbabel/wmt22-comet-da")
    model = load_from_checkpoint(model_path)

    refs = list(zip(*items))[0]
    preds = list(zip(*items))[1]
    sources = list(zip(*items))[2]
    batch_size = 4

    data = [
        {"src": src, "mt": mt, "ref": ref}
        for src, mt, ref in zip(sources, preds, refs)
    ]
    output = model.predict(data, batch_size=batch_size, gpus=1)
    return output.system_score

def comet_22_da(items):  # This is a passthrough function
    return items
