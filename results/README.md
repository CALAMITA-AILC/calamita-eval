# Leaderboard
<br>


| **Parent** | **Task** | **Metric** | [sapienzanlp/Minerva-7B-instruct-v1.0](https://huggingface.co/sapienzanlp/Minerva-7B-instruct-v1.0) | [swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA](https://huggingface.co/swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA) | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | [meta-llama/Llama-3.1-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct) |
|-|-|-|-|-|-|-|
| [**ABRICOT**](small_task_description/abricot.md)
|  | abs | pearson | -0.03 | 0.50 | 0.29 | 0.44 |
|  | inc | pearson | -0.20 | 0.14 | 0.18 | **0.25** |  
| [**AMELIA**](small_task_description/amelia.md)
|  | arg-component-fewshot | f1 | 0.23 | 0.41 | 0.48 | **0.86** |  
|  | arg-component-zeroshot | f1 | 0.00 | 0.44 | 0.47 | **0.71** |  
|  | arg-premisetype-fewshot | f1 | 0.48 | 0.60 | 0.74 | **0.86** |  
|  | arg-premisetype-zeroshot | f1 | 0.57 | 0.57 | 0.39 | **0.85** |  
|  | arg-scheme-fewshot | f1 | 0.27 | 0.28 | 0.42 | **0.57** |  
|  | arg-scheme-zeroshot | f1 | 0.16 | 0.21 | 0.34 | **0.42** |  
| [**BEEP**](small_task_description/beep.md)
|  | beep | accuracy | 0.52 | 0.62 | 0.65 | **0.84** |  
| [**BLM-It**](small_task_description/blm-it.md)
|  | agr1_0shots | f1 | 0.03 | 0.14 | 0.10 | **0.33** |  
|  | agr1_1shots | f1 | 0.07 | 0.18 | 0.26 | **0.41** |  
|  | agr2_0shots | f1 | 0.02 | 0.20 | 0.11 | **0.35** |  
|  | agr2_1shots | f1 | 0.09 | 0.30 | 0.24 | **0.41** |  
|  | caus1_0shots | f1 | 0.03 | 0.05 | 0.05 | **0.09** |  
|  | caus1_1shots | f1 | 0.09 | 0.08 | 0.13 | **0.18** |  
|  | caus2_0shots | f1 | 0.03 | 0.07 | 0.06 | **0.08** |  
|  | caus2_1shots | f1 | 0.09 | 0.12 | 0.13 | **0.19** |  
|  | od1_0shots | f1 | 0.03 | 0.06 | 0.06 | **0.07** |  
|  | od1_1shots | f1 | 0.09 | 0.09 | 0.13 | **0.27** |  
|  | od2_0shots | f1 | 0.03 | 0.06 | 0.06 | **0.07** |  
|  | od2_1shots | f1 | 0.10 | 0.10 | 0.12 | **0.20** |  
| [**DIMMI**](small_task_description/dimmi.md)
|  | global | accuracy | 0.07 | **0.34** | 0.31 | **0.34** |  
|  | p1-molecule | accuracy | 0.01 | 0.64 | 0.86 | **0.87** | 
|  | p1-usage | accuracy | 0.08 | 0.12 | **0.19** | **0.19** | 
|  | p1-drug_interaction | accuracy | 0.12 | 0.21 | **0.43** | 0.39 |  
|  | p1-posology | accuracy | 0.17 | 0.16 | 0.17 | **0.18** |  
|  | p1-side_effect | accuracy | 0.01 | 0.07 | **0.16** | 0.15 |  
|  | p2-molecule | accuracy | 0.00 | 0.84 | 0.76 | 0.87 |  
|  | p2-usage | accuracy| 0.07 | 0.15 | **0.22** | 0.16 |
|  | p2-drug_interaction | 0.11 | 0.45 | 0.36 | **0.40** |
|  | p2-posology | accuracy | 0.16 | 0.14 | 0.15 | **0.20** |
|  | p2-side_effect | accuracy | 0.00 | 0.08 | 0.05 | **0.06** | 
| [**ECWCA**](small_task_description/ecwca.md)
|  | hint | f1 | 0.52 | 0.10 | 0.42 | **0.67** |
|  | no-hint | f1 | 0.54 | 0.08 | 0.43 | **0.66** |
| [**EurekaRebus**](small_task_description/eurekarebus.md)
|  | eureka_hints | accuracy | 0.00 | 0.00 | 0.07 | **0.32** | 
|  | eureka_original | accuracy | 0.00 | 0.00 | 0.10 | **0.36** |
| [**GATTINA**](small_task_description/gattina.md)
|  | ansa | sbert_score | 0.07 | 0.17 | 0.33 | **0.59** |
|  | galileo | sbert_score | 0.21 | 0.21 | 0.22 | **0.26** |
| [**GEESE**](small_task_description/geese.md)
|  | anon_anita | accuracy | 0.57 | 0.83 | 0.66 | **0.89** |
|  | anon_dummy | accuracy | 0.49 | 0.54 | 0.49 | **0.61** |
|  | anon_gold | accuracy | 0.58 | 0.71 | 0.62 | **0.82** |
|  | anon_llama | accuracy | 0.57 | 0.79 | 0.60 | **0.86** |
|  | noexp | accuracy | 0.49 | 0.47 | 0.50 | **0.57** |
| [**GFG**](small_task_description/gfg.md)
|  | task_1_1 | bert_f1 | 0.49 | 0.55 | 0.66 | **0.59** |
|  | task_1_2 | bert_f1 | 0.17 | 0.45 | 0.50 | **0.53** |
|  | task_2_1 | acc_gente | 0.53 | 0.51 | 0.18 | **0.61** |
|  | task_2_2 | cwa | 0.45 | 0.54 | 0.53 | **0.73** |
|  | task_2_3 | acc_gente | 0.33 | 0.50 | 0.21 | **0.54** |
|  | task_3_1 | cwa | 0.28 | 0.35 | 0.42 | **0.58** | 
|  | task_3_2 | acc_gente | 0.59 | 0.57 | **0.61** | 0.56 |
| [**GITA4Calamita**](small_task_description/gita.md)
|  | conflict_consistency | accuracy | 0.02 | 0.18 | 0.29 | **0.65** |
|  | physical_verifiability | accuracy | 0.00 | 0.08 | 0.14 | **0.36** |
|  | story_class_accuracy | accuracy | 0.38 | 0.59 | 0.72 | **0.88** |
| [**INVALSI**](small_task_description/invalsi.md)
|  | ita | accuracy | 0.38 | 0.71 | 0.71 | **0.89** |
|  | ita_binarie | accuracy | 0.59 | 0.65 | 0.61 | **0.74** |
|  | ita_multipla | accuracy | 0.35 | 0.72 | 0.73 | **0.91** | 
|  | mate | accuracy | 0.34 | 0.47 | 0.51 | **0.72** |
|  | mate_multipla | accuracy | 0.30 | 0.41 | 0.45 | **0.70** |
|  | mate_numero | accuracy | 0.27 | 0.54 | 0.59 | **0.78** | 
|  | mate_verofalso | accuracy | 0.59 | 0.61 | 0.59 | **0.65** | 
| [**ITA-SENSE**](small_task_description/ita-sense.md)
|  | gen-no-translation | rougeBertScore | 0.26 | 0.26 | **0.32** | 0.31 | 
|  | gen-with-translation | rougeBertScore | 0.25 | 0.26 | **0.32** | 0.31 |
|  | ml-no-translation | extract_answer | 0.22 | 0.51 | 0.41 | **0.63** |
|  | ml-with-translation | extract_answer | 0.20 | 0.48 | 0.39 | **0.58** | 
| [**ItaEval**](small_task_description/itaeval.md)
|  | ami_2020_aggressiv. | f1 | 0.44 | 0.48 | **0.60** | 0.52 |
|  | ami_2020_misogyny | f1 | 0.52 | 0.73 | 0.73 | **0.85** |
|  | gente_rephrasing | accuracy | 0.26 | 0.35 | 0.31 | **0.43** |
|  | haspeede2_hs | f1 | 0.52 | 0.70 | 0.70 | **0.73** |
|  | haspeede2_stereo | f1 | 0.46 | 0.62 | 0.60 | **0.67** |
|  | hatecheck_ita | f1 | 0.71 | 0.81 | 0.83 | **0.89** |
|  | honest_ita | accuracy | **1.00** | **1.00** | **1.00** | **1.00** |
|  | ironita_irony | f1 | 0.42 | 0.69 | 0.67 | **0.79** | 
|  | ironita_sarcasm | f1 | 0.42 | 0.46 | 0.52 | **0.61** |
|  | itacola | accuracy | 0.74 | 0.69 | 0.82 | **0.88** |
|  | news_sum_fanpage | rouge1 | 0.29 | 0.30 | **0.33** | 0.31 | 
|  | news_sum_ilpost | rouge1 | 0.28 | 0.29 | **0.32** | 0.27 | 
|  | sentipolc | f1 | 0.44 | 0.50 | 0.49 | **0.57** | 
| [**MACID**](small_task_description/macid.md)
|  | macid | accuracy | 0.27 | 0.43 | 0.43 | **0.58** | 
| [**MAGNET**](small_task_description/magnet.md)
|  | en_it_public | bleu | 0.28 | 0.25 | 0.27 | **0.32** | 
|  | IT_en_it_private | bleu | 0.43 | 0.35 | 0.41 | **0.51** |
|  | it_en_public | bleu | 0.33 | 0.31 | 0.35 | **0.38** | 
|  | IT_it_en_private | bleu | 0.47 | 0.33 | 0.47 | **0.53** |
|  | UK_en_it_private | bleu | 0.42 | 0.31 | 0.40 | **0.50** |
|  | UK_it_en_private | bleu | 0.47 | 0.32 | 0.49 | **0.54** |
|  | US_en_it_private | bleu | 0.33 | 0.24 | 0.30 | **0.34** |
|  | US_it_en_private | bleu | 0.37 | 0.26 | 0.40 | **0.43** | 
| [**MULT-It**](small_task_description/mult-it.md)
|  | multi-it-a | accuracy | 0.39 | 0.62 | 0.65 | **0.84** |
|  | multi-it-c | accuracy | 0.50 | 0.63 | 0.66 | **0.81** |
| [**PejorativITy**](small_task_description/pejorativity.md)
|  | misogyny | accuracy | 0.61 | 0.67 | 0.46 | **0.75** |
|  | misogyny-context | accuracy | 0.66 | 0.79 | **0.82** | 0.80 |
|  | standard | accuracy | 0.43 | 0.51 | 0.44 | **0.59** | 
| [**PERSEID**](small_task_description/perseid.md) | task_0 | f1 | 0.32 | 0.34 | 0.49 | **0.50** |
|  | task_1 | f1 | 0.38 | 0.29 | 0.50 | **0.50** | 
|  | task_2 | f1 | 0.35 | 0.31 | 0.50 | **0.50** |
|  | task_3 | f1 | 0.39 | 0.23 | 0.50 | **0.49** | 
| [**TERMite**](small_task_description/termite.md)
|  | ita-text-to-sql | exec_accuracy | 0.04 | 0.38 | 0.36 | **0.46** | 
| [**TRACE-it**](small_task_description/trace-it.md)
|  | traceIT | accuracy | 0.63 | 0.70 | 0.72 | **0.85** |
| [**VERYf-IT**](small_task_description/verifyit)
|  | enriched | accuracy | **0.57** | 0.43 | 0.52 | 0.56 |
|  | full | accuracy | **0.59** | 0.41 | 0.52 | **0.59** |
|  | small | accuracy | **0.57** | 0.43 | 0.52 | 0.56 |

::: ::::
