import json
import locale
from unidecode import unidecode

locale.setlocale(locale.LC_COLLATE, 'pt_PT.UTF-8')

with open ("junção ficheiros TP2/acog.json", "r", encoding="UTF8") as file:
    acog = json.load(file)

with open ("junção ficheiros TP2/elara.json", "r", encoding="UTF8") as file:
    elara = json.load(file)

# dicionário c/ chave unidecode e lower para posterior correta comparação
acog_new = {unidecode(key): value for key, value in acog.items()}
elara_new = {unidecode(key): value for key, value in elara.items()}

dic_mulher = {}

# junção de todos os termos no dicionário acog
for key, value in acog.items():
    dic_mulher[key.lower()] = {'Descrições' :
                       {'desc_pt': "Google Tradutor - " + value['desc_pt'],
                       'desc_en': "ACOG - " + value['desc_en']},
                       'Traduções' : {'en': value['en']}}

# verificar quais chaves de elara ainda não estavam no dicionário anterior, para juntar
for key, value in elara.items():
    if unidecode(key) not in dic_mulher.keys():
        dic_mulher[key.lower()] = {'Descrições' :
                            {'desc_pt': "Google Tradutor - " + elara_new.get(unidecode(key))['desc_pt'],
                            'desc_en': "Elara Care - " + elara_new.get(unidecode(key))['desc_en']},
                            'Traduções' : {'en': elara_new.get(unidecode(key))['en']}}

dic_mulher = dict(sorted(dic_mulher.items(), key=lambda x: locale.strxfrm(x[0])))

file = open("output/dic_mulher_final.json", "w",encoding="utf-8")
json.dump(dic_mulher, file, ensure_ascii=False, indent=4)
file.close()