import json
import locale

locale.setlocale(locale.LC_ALL, '')

with open ("acog.json", "r", encoding="UTF8") as file:
    acog = json.load(file)

with open ("elara.json", "r", encoding="UTF8") as file:
    elara = json.load(file)

dic_mulher = {}

for key, value in acog.items():
    dic_mulher[key] = {'Descrições' :
                       {'desc_pt': "Google Tradutor - " + value['desc_pt'],
                       'desc_en': "ACOG - " + value['desc_en']},
                       'Traduções' : {'en': value['en']}}

for key, value in elara.items():
    if key not in dic_mulher.keys():
        dic_mulher[key] = {'Descrições' :
                            {'desc_pt': "Google Tradutor - " + elara.get(key)['desc_pt'],
                            'desc_en': "Elara Care - " + elara.get(key)['desc_en']},
                            'Traduções' : {'en': elara.get(key)['en']}}



dic_mulher = dict(sorted(dic_mulher.items(), key=lambda x: locale.strxfrm(x[0])))

file = open("../output/dic_mulher_final.json", "w",encoding="utf-8")
json.dump(dic_mulher, file, ensure_ascii=False, indent=4)
file.close()