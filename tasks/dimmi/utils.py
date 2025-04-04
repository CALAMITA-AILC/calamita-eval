import ast
import re
from typing import List, Dict, Optional, Union, Callable
import re
import ast
import json
import sys
#Funzione di DEBUG: Se True prendo solo un numero limitato di esempi
debug=False
def preprocess_dataset(dataset):
        if debug:
            dataset = dataset.select([i for i in range(1,10)])
        return dataset
"""
#Non più necessaria dopo la modifica del formato del dataset
# Postprocessing function per estrarre le liste dalla risposta del modello

def parse_answer(response: str) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    
    # Estrai solo la lista della molecola
    pattern = r"molecule: (\[.*?\])(?=\n|$)"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        try:
            list_str = match.group(1).strip()
            result["molecule"] = ast.literal_eval(list_str)
        except:
            result["molecule"] = []
    else:
        result["molecule"] = []
        
    return result

# The post-processing function to be applied to every model output.
POSTPROCESSING_FUNC = parse_answer
"""
"""
#Non più necessaria dopo la modifica del formato del dataset
def crea_lista(stringa):
    # Funzione per estrarre la lista, anche se ci sono apostrofi
    lista=[]
    try:
        stringa=stringa.replace('"',"'") #In questo modo gestisco anche situazioni del tipo ["testo"] invece di ['testo']
        for elem in re.search(r'\[(.*)\]', stringa).group(1).split("','"):
            try:
                lista.append(elem.strip("'"))
            except:
                pass
    except:
        pass
         
    return lista
def f1_passthrough(input):
    return input
"""

TARGET_COLUMNS = ["molecule", "drug_interaction", "usage", "side_effect", "posology"]
def global_prompt(dataset):
    #Preparo il "target" di dimmi-global, ovvero, il dizionario con tutte le liste target   
    return {k: v for k, v in dataset.items() if k in TARGET_COLUMNS} 
    
def calculate_list_f1(pred_list: List[str], ref_list: List[str]) -> float:
    try:
        pred_set = {item.lower().strip() for item in pred_list}
    except:
        try:
            pred_set={str(item).lower().strip() for item in pred_list} #Risoluzione al volo di un bug
        except:
            pred_set={}
    try:
        ref_set = {item.lower().strip() for item in ref_list}
    except:
        try:
            ref_set={str(item).lower().strip() for item in ref_list}
        except:
            ref_set={}
    
    common_items = pred_set.intersection(ref_set)
    
    precision = len(common_items) / len(pred_set) if pred_set else 0
    recall = len(common_items) / len(ref_set) if ref_set else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return f1

def regex_findfield(stringa, target):
    #Funzione per trovare una stringa del tipo field: [...] nel testo generato
    match = re.search(fr"{target}:\s*(\[.*?\])", stringa)
    if match:
        return match.group(1)
    return []

def compute_results(input_,field):   
    ref=eval(input_[0])[field]
    gen=input_[1]

    if type(ref)==type(""):
        ref=[ref]
    elif type(ref)==type([]):
        pass
    else:
        ref=[]
    field_f1_scores: List[float] = []
    try:
        gen_list=ast.literal_eval(regex_findfield(gen,field))
    except:
        gen_list=[]
    f1score=calculate_list_f1(gen_list,ref)
    #print(f"Sto calcolando lo score f1 tra la referenza {ref} e il generato {gen_list}")
    return f1score
    """
    for gen, ref in zip(generations, references):
        #print("Questa è la reference: ",ref)
        #print("Questo è il tipo della reference: ",type(ref))
        
        ATTENZIONE!
            A causa di problemi con gli apostrofi ho modificato la logica con cui la stringa che
            rappresenta la lista viene convertita in stringa. Necessaria revisione da parte degli 
            autori.
        
        #ref_field = crea_lista(ref)
        #gen_field = crea_lista(gen)
        ref_field=ref
        try:
            gen_field=ast.literal_eval(regex_findfield(gen,field))
        except:
            gen_field=[]
            #print(f"Errore! {gen}")
        print(f"Obiettivo {type(ref_field)} {ref_field}, Generata {type(gen_field)} {gen_field}")
        f1: float = calculate_list_f1(gen_field, ref_field)
        field_f1_scores.append(f1)
    
    avg_f1: float = sum(field_f1_scores) / len(field_f1_scores) if field_f1_scores else 0
    #results[f"{field}_f1"] = avg_f1
    fieldname=field+'_f1'
    return avg_f1
    return results
"""
def molecule(input_):
    field = "molecule"
    return compute_results(input_,field)
    
    
def side_effect(input_):
    field = "side_effect"
    return compute_results(input_,field)
def usage(input_):
    field = "usage"
    return compute_results(input_,field)
def posology(input_):
    field = "posology"
    return compute_results(input_,field)
def drug_interaction(input_):
    field = "drug_interaction"
    return compute_results(input_,field)
def overall_f1(input_):
     accumulation=0
     for field in TARGET_COLUMNS:
         accumulation+=compute_results(input_,field)
     return accumulation/len(TARGET_COLUMNS)
    
"""
#Funzioni non più necessarie: erano necessarie quando si faceva aggregazione alla fine della eval
# Ora viene calcolato l'f1 volta per volta e poi fatta la media
def molecule_f1(*args):
    print("Prima di scompattare la lista, item corrisponde a:")
    for arg in args:
        print("ARGOMENTO:")
        print(arg)
    unzipped_list=list(zip(*items))
    generations=unzipped_list[1]
    references=unzipped_list[0]
    field = "molecule"
    return compute_results(generations,references,field)
def side_effect_f1(items):
    print("Prima di scompattare la lista, item corrisponde a:")
    print(items)    
    unzipped_list=list(zip(*items))
    generations=unzipped_list[1]
    references=unzipped_list[0]
    field = "side_effect"
    return compute_results(generations,references,field)
    
def usage_f1(items):
    print("Prima di scompattare la lista, item corrisponde a:")
    print(items)    
    unzipped_list=list(zip(*items))
    generations=unzipped_list[1]
    references=unzipped_list[0]
    field = "usage"
    return compute_results(generations,references,field)
    
def posology_f1(items):
    print("Prima di scompattare la lista, item corrisponde a:")
    print(items)    
    unzipped_list=list(zip(*items))
    generations=unzipped_list[1]
    references=unzipped_list[0]
    field = "posology"
    return compute_results(generations,references,field)
    
def drug_interaction_f1(items):
    unzipped_list=list(zip(*items))
    generations=unzipped_list[1]
    references=unzipped_list[0]
    field = "drug_interaction"
    return compute_results(generations,references,field)
"""
      

