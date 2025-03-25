def doc_to_text(doc):
    PRE_PROMPT = "The story is as follows:"
    POST_PROMPT = "Is the story plausible?"
    
    instance = "Please read the following story and answer if the story is plausible taking into account the order of the events. Please answer with true or false.\n"
    instance += PRE_PROMPT + "\n"

    for sentence in doc["sentences"]:
        instance += f'{sentence} '

    instance += "\n"
    instance += POST_PROMPT

    return instance

def mean(items):
    import json
    # items -> [1.0,0.0,1.0]
    print(items)
    '''
    Il task "gita4calamita" prevede il salvataggio dei risultati ottenuti dall'esecuzione di questo task (story) affinchè questi possano essere usati nei task successivi. Il codice seguente salva i risultati nel file temporaneo "gita_story_results.json"
    '''
    with open("gita_story_results.json","w") as story:
      json.dump(items, story, indent=4)
    return sum(items)/len(items)

#def preprocess_dataset(dataset):
#    dataset = dataset.select([i for i in range(10)])
#    return dataset
