import json
from deep_translator import GoogleTranslator
import locale
from unidecode import unidecode
import re

locale.setlocale(locale.LC_COLLATE, 'pt_PT.UTF-8')

with open('ficheiros_TP1/glossario_exppop.json', 'r', encoding="utf8") as file:
    exps = dict(json.load(file))

with open('ficheiros_TP1/glos_covid.json', 'r', encoding="utf8") as file:
    covid_original = dict(json.load(file))

with open('ficheiros_TP1/dicionario_obrigatorio.json', 'r', encoding="utf8") as file:
    obg = dict(json.load(file))
    
# formatação do dicionário glossário de expressões de populares
for key, value in exps.items():
    exps[key] = {"Descrições": {"exp pop" : value}}

# formatação do dicionário de covid - chave em pt
covid = {}
for key, value in covid_original.items():
    pt_value = value.pop("pt")
    if "syn." in pt_value:
        pt_value = pt_value.split(",")[0].strip()
    value["en"] = key
    covid[pt_value] = value

obg_new = {}
for key, value in obg.items():
    key = re.sub(r'\s*\([^()]+\)', '', key)
    key = re.sub(r'/(-[a-zA-Z])', r'(\1)', key)
    key = re.sub(r'\(.*\)', '', key)
    obg_new[key.strip()] = value

exps_new = {unidecode(key): value for key, value in exps.items()}
covid_new = {unidecode(key): value for key, value in covid.items()}

# união dos três dicionários
dic_uniao = {}
count = 0
for key, value in obg_new.items():
    # união do dicionário do dicionário obrigatório com os outros dois
    if unidecode(key) in exps_new.keys() and unidecode(key) in covid_new.keys():
        dic_uniao[key] = {'Descrições': {"desc_pt" : "Google Translator - " + covid_new[unidecode(key)]['desc_pt'],
                                        "exp pop" : "Expressão Popular - " + exps_new[unidecode(key)]['Descrições']['exp pop'],
                                        "desc_en" : covid_new[unidecode(key)]['desc_en'],
                                        "syn" : covid_new[unidecode(key)]['syn']},
                        'Traduções': {"en" : value['en'],
                                    "es" :  value['es'],
                                    "fr" : covid_new[unidecode(key)]['fr'],
                                    "ar" :  covid_new[unidecode(key)]['ar'],
                                    "de" :  covid_new[unidecode(key)]['de'],
                                    "fr" :  covid_new[unidecode(key)]['fr'],
                                    "ja" :  covid_new[unidecode(key)]['ja'],
                                    "ko" :  covid_new[unidecode(key)]['ko'],
                                    "ru" :  covid_new[unidecode(key)]['ru'],
                                    "zh" :  covid_new[unidecode(key)]['zh']}}
    elif unidecode(key) in exps_new.keys() and unidecode(key) not in covid_new.keys():
        dic_uniao[key] = {'Descrições':{"exp pop" : "Expressão Popular - " + exps_new[unidecode(key)]['Descrições']['exp pop']},
                          'Traduções':{"en" : value['en'],
                                        "es" : value['es']}}
    elif unidecode(key) in covid_new.keys() and unidecode(key) not in exps_new.keys():
        dic_uniao[key] = {'Descrições':{"desc_pt" : "Google Translator - "+ covid_new[unidecode(key)]['desc_pt'],
                                        "desc_en": covid_new[unidecode(key)]['desc_en'],
                                        "syn" : covid_new[unidecode(key)]['syn']},
                            'Traduções':{"en" : value['en'],
                                        "es" : value['es'],
                                        "fr" : covid_new[unidecode(key)]['fr'],
                                        "ar" :  covid_new[unidecode(key)]['ar'],
                                        "de" :  covid_new[unidecode(key)]['de'],
                                        "fr" :  covid_new[unidecode(key)]['fr'],
                                        "ja" :  covid_new[unidecode(key)]['ja'],
                                        "ko" :  covid_new[unidecode(key)]['ko'],
                                        "ru" :  covid_new[unidecode(key)]['ru'],
                                        "zh" :  covid_new[unidecode(key)]['zh']}}
    elif unidecode(key) not in covid_new.keys() and unidecode(key) not in exps_new.keys():
        dic_uniao[key] = {'Traduções':{"en" : value['en'],
                                        "es" : value['es']}}  
        
dic_uniao_new = {unidecode(key): value for key, value in dic_uniao.items()}

for key, value in exps.items():
    if unidecode(key) not in dic_uniao_new.keys():
        dic_uniao[key] = {"Descrições": {'exp pop': "Expressão Popular - " + value['Descrições']['exp pop']}}

for key, value in covid.items():
    if unidecode(key) not in dic_uniao_new.keys():
        dic_uniao[key] = {'Descrições':{'desc_pt': "Google Translator - " + value['desc_pt'],
                                        'desc_en': value['desc_en'],
                                        "syn" : value['syn']},
                        'Traduções':{'en': value['en'],
                                    'fr': value['fr'],
                                    "ar" : value['ar'],
                                    "de" : value['de'],
                                    "es" : value['es'],
                                    "fr" : value['fr'],
                                    "ja" : value['ja'],
                                    "ko" : value['ko'],
                                    "ru" : value['ru'],
                                    "zh" : value['zh']}}

dic_uniao = dict(sorted(dic_uniao.items(), key=lambda x: locale.strxfrm(x[0])))

with open('ficheiros_TP1/dicionario_final.json', 'w', encoding="utf8") as file:
    json.dump(dict(dic_uniao), file, ensure_ascii=False, indent=4)
