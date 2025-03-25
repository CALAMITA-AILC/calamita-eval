def doc_to_text(doc):
    PRE_PROMPT = "The story is as follows: "
    POST_PROMPT = "The physical state that causes the conflict in the implausible story is: "

    instance = "The following story is implausible. Identify the physical state that causes the conflict in the story. These are the descriptions of each physical state: \nPower: Indicates whether an object is powered or not, relevant for electrical devices. \nLocation: Refers to the spatial position of an entity, either human or object. \nExist: Denotes whether an object is present or has disappeared. \nClean: Refers to the cleanliness of an entity, indicating whether it is clean or dirty. \nEdible: Identifies whether an object is fit for consumption. \nWet: Denotes whether an object or person is in a wet or dry state. \nFunctional: Refers to whether an object is in working condition or broken. \nWearing: Applies to humans, indicating whether they are dressed or not. \nOpen: Refers to whether an object (e.g., a door or container) is open or closed. \nConscious: Denotes whether a human is conscious or unconscious. \nTemperature: Refers to the relative temperature of an entity, e.g., hot or cold. \nSolid: Describes whether an object is in a solid state. \nOccupied: Indicates whether an object (e.g., a container) is occupied or contains something. \nIn pieces: Refers to whether an object is intact or has been broken into pieces. Select one of them after reading the story.\n"
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