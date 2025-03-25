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
    with open('gita_conflict_results.json') as file:
      story_results = json.load(file)
    # story results contains the accuracy from the previous step
    # the order of the task is the same
    #dataset = dataset.select([i for i in range(10)])
    print(dataset)
    dataset = dataset.filter(lambda example, idx: story_results[idx], with_indices=True)
    print(dataset)
    dataset = dataset.select([i for i in range(len(dataset)) if not dataset[i]["plausible"]])
    return dataset