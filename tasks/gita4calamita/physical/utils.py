def get_prefix():
    import os
    prefix = os.getenv("GITA4CALAMITA_PREFIX")
    if prefix is None:
        raise ValueError("GITA4CALAMITA_PREFIX not set, please set it before running the script.")
    return prefix

def doc_to_text(doc):
    PRE_PROMPT = "The story is as follows: "
    POST_PROMPT = "The physical state that causes the conflict in the implausible story is: "

    instance = ""
    instance += PRE_PROMPT + "\n"

    for sentence in doc["sentences"]:
        instance += f'{sentence} '

    instance += "\n"
    instance += POST_PROMPT

    return instance

def preprocess_dataset(dataset):
    
    import json
    prefix = get_prefix()
    with open(f'{prefix}_conflict_data.json', "r") as file:
        conflict_results = json.load(file)

    well_classified = set(conflict_results["well_classified"])
    dataset = dataset.filter(lambda x: x["example_id"] in well_classified)
    dataset = dataset.filter(lambda x: not x["plausible"]) # filter out plausible instances

    return dataset

def label_2_id(label):

    return {
        "power": 0,
        "location": 1,
        "exist": 2,
        "clean": 3,
        "edible": 4,
        "wet": 5,
        "functional": 6,
        "wearing": 7,
        "open": 8,
        "conscious": 9,
        "temperature": 10,
        "solid": 11,
        "occupied": 12,
        "in pieces": 13,
    }[label]

def process_results(doc, results):
    import numpy as np
    target_label = doc["states"]
    target_id = label_2_id(target_label)

    lls, is_greedy = zip(*results)
    pred = np.argmax(lls)
    acc = float(pred == target_id)

    return_dict =  {"verifiability": acc, "verifiability_cloze": None, "verifiability_order": None}

    if doc["type"] == "cloze":
        return_dict["verifiability_cloze"] = acc
    elif doc["type"] == "order":
        return_dict["verifiability_order"] = acc

    return return_dict

def mean(items):
    import json
    prefix = get_prefix()
    with open(f"{prefix}_conflict_data.json", "r") as file:
        conflict_data = json.load(file)

    num_non_plausibles = conflict_data["num_non_plausibles"]
    return sum(items)/num_non_plausibles

def mean_cloze(items):

    import json
    prefix = get_prefix()
    with open(f"{prefix}_conflict_data.json", "r") as file:
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
    with open(f"{prefix}_conflict_data.json", "r") as file:
        story_data = json.load(file)

    num_order = story_data["num_order"]
    
    order_items = []
    for i in range(len(items)):
        if items[i] is not None:
            order_items.append(items[i])
    if len(order_items) == 0:
        return 0
    return sum(order_items)/num_order