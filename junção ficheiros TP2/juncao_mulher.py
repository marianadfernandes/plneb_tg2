import json
import locale

locale.setlocale(locale.LC_ALL, '')

with open ("junção ficheiros TP2/acog.json", "r", encoding="UTF8") as file:
    acog = json.load(file)

with open ("junção ficheiros TP2/elara.json", "r", encoding="UTF8") as file:
    elara = json.load(file)

dic_mulher = {}

for key, value in acog.items():
    dic_mulher[key] = {'desc_pt':"ACOG - " + value}

for key, value in elara.items():
    if key not in dic_mulher.keys():
        dic_mulher[key] = {'desc_pt':"Elara Care - " + elara.get(key)}



dic_mulher = dict(sorted(dic.items(), key=lambda x: locale.strxfrm(x[0])))

file = open("output/novo_dic.json", "w",encoding="utf-8")
json.dump(dic, file, ensure_ascii=False, indent=4)
file.close()