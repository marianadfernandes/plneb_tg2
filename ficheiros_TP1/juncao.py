import json
from deep_translator import GoogleTranslator
import locale
from unidecode import unidecode
import re

locale.setlocale(locale.LC_ALL, '')

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

# print(covid)

# cópia do dicionário glossário de expressões de populares
# exps_copia = {}
# for key, value in exps.items():
#   exps_copia[key] = value

# # interseção de dicionario exp pop com covid 
# exps_covid = {}
# count = 0
# for key, value in covid.items():
#     if (key in exps.keys()):
#         count += 1
#         exps_covid[key] = {'Descrições:':{"desc_pt" : value['desc_pt'],
#                                         "exp pop" : exps[key]['Descrições']['exp pop'],
#                                         "desc_en": value['desc_en']},
#                         'Traduções':{"en" : key,
#                                     "fr" : value['fr'],
#                                     "ar" :  value['ar'],
#                                     "de" :  value['de'],
#                                     "es" :  value['es'],
#                                     "fr" :  value['fr'],
#                                     "ja" :  value['ja'],
#                                     "ko" :  value['ko'],
#                                     "ru" :  value['ru'],
#                                     "zh" :  value['zh']}}
            
# # print(count)

# # with open('int_3.json', 'w', encoding="utf8") as file:
# #     json.dump(exps_covid, file, ensure_ascii=False, indent=4)

# # interseção do dicionário de expressões populares com o das traduções en_pt
# exps_enpt = {}     
# count = 0
# for key, value in exps.items():
#     if key in obg.keys():
#         count += 1
#         exps_enpt[key] = {'Descrições':{"exp pop" : value['Descrições']['exp pop']},
#                           'Traduções':{"en" : obg[key]['en'],
#                                         "es" : obg[key]['es']}}
        
# # print(count)
        
# # with open('int_exps_enpt.json', 'w', encoding="utf8") as file:
# #     json.dump(exps_enpt, file, ensure_ascii=False, indent=4)

# # interseção do dicionário de covid com o das traduções en_pt
# covid_enpt = {}  
# count = 0   
# for key, value in covid.items():
#     if key in obg.keys():
#         count += 1
#         covid_enpt[key] = {'Descrições':{"desc_pt" : value['desc_pt'],
#                                         "desc_en": value['desc_en']},
#                             'Traduções':{"en" : obg[key]['en'],
#                                         "es" : obg[key]['es'],
#                                         "fr" : value['fr']}}
        
# # print(count)
        
# # with open('int_covid_enpt.json', 'w', encoding="utf8") as file:
# #     json.dump(covid_enpt, file, ensure_ascii=False, indent=4)

# # interseção dos três dicionários 
# count = 0
# for key, value in covid.items():
#     if key in exps_enpt.keys():
#         # print(key)
#         count += 1
#         exps_enpt[key] = {'Descrições':{"desc_pt" : covid[key]['desc_pt'],
#                                         "exp pop" : exps_enpt[key]['Descrições']['exp pop'],
#                                         "desc_en" : covid[key]['desc_en']},
#                     'Traduções':{"en" : exps_enpt[key]['Traduções']['en'],
#                                 "es" : exps_enpt[key]['Traduções']['es'],
#                                 "fr" : covid[key]['fr'],
#                                 "ar" :  covid[key]['ar'],
#                                 "de" :  covid[key]['de'],
#                                 "es" :  covid[key]['es'],
#                                 "fr" :  covid[key]['fr'],
#                                 "ja" :  covid[key]['ja'],
#                                 "ko" :  covid[key]['ko'],
#                                 "ru" :  covid[key]['ru'],
#                                 "zh" :  covid[key]['zh']}}
                    
# # print(count)

# # with open('int_3.json', 'w', encoding="utf8") as file:
# #     json.dump(exps_enpt, file, ensure_ascii=False, indent=4)
        
# # união do dicionário de expressões populares com o de covid
# for key, value in covid.items():
#     if key in exps_copia.keys():
#         exps_copia[key] = {"Descrições": {"desc_pt" :  value['desc_pt'],
#                                         "exp pop": exps_copia[key]['Descrições']['exp pop'],
#                                         "desc_en": value['desc_en']},
#                             'Traduções':{
#                                         "en" : key,
#                                         "fr" : value['fr']}}
#     else: 
#         exps_copia[key] = {'Descrições':{"desc_pt" :  value['desc_pt'],
#                                     "desc_en": value['desc_en']},
#                             'Traduções':{"en" : key,
#                                         "fr" : value['fr']}}
        
# # exps2 = sorted(exps_copia.items())

# # união do dicionário de covid com dicionario de exp populares + en_pt
# dic_final = {}
# count = 0
# for key, value in covid.items():
#     if key in exps_enpt.keys():
#         count += 1
#         dic_final[key] = {'Descrições': {"desc_pt" : value['desc_pt'],
#                                         "exp pop" : exps_enpt[key]['Descrições']['exp pop'],
#                                         "desc_en" : value['desc_en']},
#                         'Traduções': {"en" : exps_enpt[key]['Traduções']['en'],
#                                     "es" : exps_enpt[key]['Traduções']['es'],
#                                     "fr" : value['fr']}}
#     else:
#         count += 1
#         dic_final[key] = {'Descrições':{"desc_pt" : value['desc_pt'],
#                                         "desc_en" : value['desc_en']},
#                         'Traduções:':{"en" : value['en'],
#                                     "fr" : value['fr']}}
        
# for key, value in exps_enpt.items():
#     if key not in dic_final.keys():
#         count += 1
#         dic_final[key] = value
        
# # print(count)

# dic_final = sorted(dic_final.items())

# print(dic_final)

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
