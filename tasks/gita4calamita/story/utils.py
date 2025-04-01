def doc_to_text(doc):
    PRE_PROMPT = "The story is as follows:"
    POST_PROMPT = "Is the story plausible?"
    
    instance = ""
    instance += PRE_PROMPT + "\n"

    for sentence in doc["sentences"]:
        instance += f'{sentence} '

    instance += "\n"
    instance += POST_PROMPT

    return instance

def preprocess_dataset(dataset):
    import json
    # Calculate number of order, cloze
    num_order = 0
    num_cloze = 0

    for inst in dataset:
        if inst["type"] == "order":
            num_order += 1
        elif inst["type"] == "cloze":
            num_cloze += 1
        else:  
            pass

    num_non_plausibles = num_cloze + num_order
    dict_to_save = {
        "well_classified": None,
        "num_order": num_order,
        "num_cloze": num_cloze,
        "num_non_plausibles": num_non_plausibles,
        "num_plausibles": len(dataset) - num_non_plausibles,
    }

    with open("gita_story_predata.json","w") as story:
      json.dump(dict_to_save, story, indent=4)
    
    return dataset

def label_2_id(label):

    if isinstance(label, int):
        return label
    elif isinstance(label, str):
        return False if label.lower() == "false" else True
    else:
        raise ValueError(f"Unsupported label type: {type(label)}. Expected int, bool or str.")

def process_results(doc, results):
    import numpy as np
    target_label = doc["plausible"]
    target_id = label_2_id(target_label)
    lls, is_greedy = zip(*results)
    pred = np.argmax(lls)
    acc = float(pred == target_id)

    acc_idx = f"{acc}_{doc['example_id']}"

    return_dict =  {"accuracy": acc_idx, "accuracy_cloze": None, "accuracy_order": None, "accuracy_plausible": None}

    if doc["type"] == "cloze":
        return_dict["accuracy_cloze"] = acc
    elif doc["type"] == "order":
        return_dict["accuracy_order"] = acc
    else:
        return_dict["accuracy_plausible"] = acc

    return return_dict

def mean(items):
    import json
    with open('gita_story_predata.json', "r") as file:
        story_data = json.load(file)

    story_well_classified = []
    acc_values = []
    for i in range(len(items)):
        acc_value = float(items[i].split("_")[0])
        instance_id = items[i].split("_")[1]
        if acc_value == 1.0:
            story_well_classified.append(instance_id)
        acc_values.append(acc_value)

    with open("gita_story_data.json", "w") as file:
      story_data["well_classified"] = story_well_classified
      json.dump(story_data, file, indent=4)

    return sum(acc_values)/len(acc_values)

def mean_plausible(items):
    import json
    with open('gita_story_data.json', "r") as file:
        story_data = json.load(file)

    num_plausibles = story_data["num_plausibles"]
    
    plausible_items = []
    for i in range(len(items)):
        if items[i] is not None:
            plausible_items.append(items[i])
    if len(plausible_items) == 0:
        return 0
    return sum(plausible_items)/num_plausibles

def mean_cloze(items):
    import json
    with open('gita_story_data.json', "r") as file:
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
    with open('gita_story_data.json', "r") as file:
        story_data = json.load(file)

    num_order = story_data["num_order"]
    
    cloze_items = []
    for i in range(len(items)):
        if items[i] is not None:
            cloze_items.append(items[i])
    if len(cloze_items) == 0:
        return 0
    return sum(cloze_items)/num_order
