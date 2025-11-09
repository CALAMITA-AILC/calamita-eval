def get_prefix():
    import os
    prefix = os.getenv("GITA4CALAMITA_PREFIX")
    if prefix is None:
        raise ValueError("GITA4CALAMITA_PREFIX not set, please set it before running the script.")
    return prefix

def doc_to_text(doc):
    PRE_PROMPT = "The story is as follows: "
    POST_PROMPT = "The conflicting sentence and the breakpoint are:"

    instance = ""
    instance += PRE_PROMPT + "\n"

    for i, sentence in enumerate(doc["sentences"]):
        instance += f'{i}. {sentence}\n'

    instance += "\n"
    instance += POST_PROMPT

    return instance

def doc_to_target(doc):
    return f"{doc['confl_sents'][0]} and {doc['breakpoint']}"

def preprocess_dataset(dataset):
    
    get_prefix() # Get the prefix for the temporary files

    import json
    prefix = get_prefix()
    with open(f"{prefix}_story_data.json", "r") as file:
      story_results = json.load(file)
    well_classified = set(story_results["well_classified"])
    dataset = dataset.filter(lambda x: x["example_id"] in well_classified)
    dataset = dataset.filter(lambda x: x["breakpoint"] != -1) # filter out plausible instances

    return dataset

def label_2_id(label):

    return {
        "0 and 1": 0,
        "2 and 4": 1,
        "1 and 2": 2,
        "0 and 4": 3,
        "3 and 4": 4,
        "0 and 3": 5,
        "1 and 4": 6,
        "2 and 3": 7,
        "0 and 2": 8,
        "1 and 3": 9
    }[label]

def process_results(doc, results):
    import numpy as np
    target_label = doc_to_target(doc)
    target_id = label_2_id(target_label)

    lls, is_greedy = zip(*results)
    pred = np.argmax(lls)
    acc = float(pred == target_id)

    acc_idx = f"{acc}_{doc['example_id']}"

    return_dict =  {"consistency": acc_idx, "consistency_cloze": None, "consistency_order": None}

    if doc["type"] == "cloze":
        return_dict["consistency_cloze"] = acc
    elif doc["type"] == "order":
        return_dict["consistency_order"] = acc

    return return_dict

def mean(items):
    import json
    prefix = get_prefix()
    with open(f"{prefix}_story_data.json", "r") as file:
        story_data = json.load(file)

    num_non_plausibles = story_data["num_non_plausibles"]

    conflict_well_classified = []
    acc_values = []
    for i in range(len(items)):
        acc_value = float(items[i].split("_")[0])
        instance_id = items[i].split("_")[1]
        if acc_value == 1.0:
            conflict_well_classified.append(instance_id)
        acc_values.append(acc_value)

    prefix = get_prefix()
    with open(f"{prefix}_conflict_data.json","w") as conflict:
      story_data["well_classified"] = conflict_well_classified
      json.dump(story_data, conflict, indent=4)
    if len(acc_values) == 0:
        return 0
    return sum(acc_values)/num_non_plausibles

def mean_cloze(items):
    import json
    prefix = get_prefix()
    with open(f"{prefix}_story_data.json", "r") as file:
        story_data = json.load(file)

    num_cloze = story_data["num_cloze"]
    
    cloze_items = []
    for i in range(len(items)):
        if items[i] is not None:
            cloze_items.append(items[i])
    if len(cloze_items) == 0:
        return 0
    return sum(cloze_items)/num_cloze

def mean_order(items):
    import json
    prefix = get_prefix()
    with open(f"{prefix}_story_data.json", "r") as file:
        story_data = json.load(file)

    num_order = story_data["num_order"]
    
    order_items = []
    for i in range(len(items)):
        if items[i] is not None:
            order_items.append(items[i])
    if len(order_items) == 0:
        return 0
    return sum(order_items)/num_order
    
    
