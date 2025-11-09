import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calamita_recalc import CalamitaTask
import pandas as pd
import re
import ast
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score


def macro_f1_score(y_true, y_pred, labels):
    return f1_score(y_true, y_pred, average='macro', labels=labels) if labels is not None else f1_score(y_true, y_pred, average='macro')

def f1_classes(y_true, y_pred, labels):
    return f1_score(y_true, y_pred, average=None, labels=labels) if labels is not None else f1_score(y_true, y_pred, average=None)# returns array with the scores for each class

# labels needed in binary classification (arg-component), but give error in multi-label classification

class AmeliaTask(CalamitaTask):
    def evaluate(self, subtask, samples_path):
        if 'arg-component' in subtask:
            return self._eval_component(samples_path)
        elif 'arg-premisetype' in subtask:
            return self._eval_others(task=subtask,samples_path=samples_path)
        elif 'arg-scheme' in subtask:
            return self._eval_others(task=subtask,samples_path=samples_path)
        else:
            raise ValueError(f"Unknown amelia subtask: {subtask}")
    
    def _eval_component(self, samples_path):
                labels = ['prem', 'conc']
                json_df = pd.read_json(samples_path, lines=True)
                y_true = list(json_df.target)
                y_pred = []
                for pred in list(json_df.resps):
                    pred = pred[0][0].lower() # the text is in a list that is in a list 
                    pred = pred.replace('premessa', 'prem').replace('premissa', 'prem').replace('premesso', 'prem').replace('conclusione', 'conc') # variants of prem and conc
                    if pred.split('.')[0].strip(' »') in labels: # resp is prem. additional text
                        y_pred.append(pred.split('.')[0].strip(' »'))
                    elif pred.split('(')[0].strip(' .»') in labels: # resp is prem (explanation)
                        y_pred.append(pred.split('(')[0].strip(' .»'))
                    elif 'prem o conc? risposta: ' in pred:  # resp is: prem o conc? risposta: prem
                        res = pred.split('prem o conc? risposta: ')[1]
                        if res.startswith('prem') or res.startswith('conc'):
                            y_pred.append(res[:4])
                        else:
                            y_pred.append('bad answer')
                    else: 
                        resp_lines = pred.split('\n')
                        resp_lines = [x.strip(' .»,"|') for x in resp_lines]
                        resp_ok = False
                        for resp_line in resp_lines:
                            if resp_line in labels: # resp is prem \n additional text
                                y_pred.append(resp_line)
                                resp_ok = True
                                break
                            elif 'risposta' in resp_line:
                                resp_with_risposta = re.split(r'risposta ?(?:corretta ?)?è?:?', resp_line) # resp is: la risposta (corretta) è: prem \n additional text
                                if resp_with_risposta[1].strip(' .,') in labels: 
                                    y_pred.append(resp_with_risposta[1].strip(' .,'))
                                    resp_ok = True
                                    break
                            elif 'questo testo è' in resp_line:
                                resp_with_questotesto = re.split(r'questo testo è:?', resp_line) # resp is: questo testo è: prem \n additional text
                                if resp_with_questotesto[1].strip(' .,') in labels: 
                                    y_pred.append(resp_with_questotesto[1].strip(' .,'))
                                    resp_ok = True
                                    break
                        if not resp_ok:
                            y_pred.append('bad answer')
        
                return {
                    'macro_f1_score': macro_f1_score(y_true, y_pred, labels=labels),
                    'f1_classes': dict(zip(labels, f1_classes(y_true, y_pred, labels=labels)))
                }
    
    def _eval_others(self, task, samples_path):
                json_df = pd.read_json(samples_path, lines=True)
                labels = ['F', 'L'] if 'premisetype' in task else ['Rule', 'Prec', 'Princ', 'Class', 'Itpr']
                labels.sort()
                y_true = list(json_df.target)
                y_true = [y_t.strip("'b") for y_t in y_true]
                y_true = [ast.literal_eval(x) for x in y_true] # conversion to list of lists, instead of list of string representations of lists
                y_pred = []
                for pred in list(json_df.resps):
                    pred = pred[0][0].replace('‘', "'").replace('’', "'").strip()
                    resp_lines = pred.split('\n')
                    resp_lines = [x.strip(' .»,"`)|\'') for x in resp_lines]
                    first_line = resp_lines[0]
                    if 'Output: ' in first_line:
                        first_line = first_line.split('Output: ')[1] # resp is Output: [expected list]
                    if 'Risposta: ' in first_line:
                        first_line = first_line.split('Risposta: ')[1] # resp is Risposta: [expected list]
                    first_line = first_line.strip()
                    if first_line.startswith('['):
                        if first_line.endswith(']') and ('(' in first_line or ')' in first_line): # tuples and explanations inside lists
                            y_pred.append(['bad answer'])
                        elif ']' in first_line:
                            if '(' in first_line and ')' in first_line: # expected list followed by (explanation)
                                first_line = first_line.split('(')[0].strip()
                            res = first_line.split(']')[0]+']' # more than one list, so split at first ] and append ] again
                            res = res.replace('[[', '[')
                            if "'" not in res and '"' not in res:  # no string delimiters for elements
                                res = str(res.replace('[', '').replace(']', '').split(', ')) 
                            try:
                                res_as_list = ast.literal_eval(res)
                                res_as_list = [i.strip() for i in res_as_list]
                                res_as_list = [x if x in labels else 'bad answer' for x in res_as_list] # check if list elements are all correct labels
                                if 'bad answer' in res_as_list:
                                    y_pred.append(['bad answer']) # choice: if at least one element is random text, it is a totally wrong answer
                                else:
                                    res_as_list = list(set(res_as_list)) # avoid duplicate elements and sort 
                                    res_as_list.sort()
                                    y_pred.append(res_as_list)
                            except (ValueError, AttributeError, SyntaxError):
                                y_pred.append(['bad answer'])
                        else:
                            y_pred.append(['bad answer'])
                    else:
                        y_pred.append(['bad answer'])

                mlb = MultiLabelBinarizer()
                mlb.fit([labels])
                y_true = mlb.transform(y_true)
                y_pred = mlb.transform(y_pred)

                return {
                    'macro_f1_score': macro_f1_score(y_true, y_pred, labels=None),
                    'f1_classes': dict(zip(labels, f1_classes(y_true, y_pred, labels=None)))
                }
