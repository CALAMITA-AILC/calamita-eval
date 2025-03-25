def doc_to_text(doc):
    PRE_PROMPT = "The story is as follows: "
    POST_PROMPT = "The conflicting sentence and the breakpoint are:"

    instance = "The following story is implausible. Identify the breakpoint, and then select the sentence responsible for the implausibility. Please identify the breakpoint sentence and the conflicting sentence.\n"
    instance += PRE_PROMPT + "\n"

    for i, sentence in enumerate(doc["sentences"]):
        instance += f'{i}. {sentence}\n'

    instance += "\n"
    instance += POST_PROMPT

    return instance

def doc_to_target(doc):
    return f"{doc['confl_sents'][0]} and {doc['breakpoint']}"

def preprocess_dataset(dataset):
    import json
    with open('gita_story_results.json') as file:
      story_results = json.load(file)
    # story results contains the accuracy from the previous step
    # the order of the task is the same
    #dataset = dataset.select([i for i in range(10)])
    print(dataset)
    dataset = dataset.filter(lambda example, idx: story_results[idx], with_indices=True)
    print(dataset)
    dataset = dataset.select([i for i in range(len(dataset)) if dataset[i]["breakpoint"] != -1])
    return dataset

def mean(items):
    import json
    print(items)
    # items -> [1.0,0.0,1.0]
    '''
    Il task "gita4calamita" prevede il salvataggio dei risultati ottenuti dall'esecuzione di questo task (conflict) affinchè questi possano essere usati nei task successivi. Il codice seguente salva i risultati nel file temporaneo "gita_conflict_results.json"
    '''
    with open('gita_story_results.json') as file:
      story_results = json.load(file)

    indice_conflict_results = 0
    for i in range(len(story_results)):
      if story_results[i]:
        if items[indice_conflict_results]:
          pass
        else:
          story_results[i] = 0
        indice_conflict_results += 1

    print(indice_conflict_results == len(items))
    print(story_results)

    with open("gita_conflict_results.json","w") as conflict:
      json.dump(story_results, conflict, indent=4)
    return sum(items)/len(items)