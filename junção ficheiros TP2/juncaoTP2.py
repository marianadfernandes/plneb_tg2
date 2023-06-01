import json
import locale
from unidecode import unidecode

locale.setlocale(locale.LC_ALL, '')

with open ("junção ficheiros TP2/url_cruzverde.json", "r", encoding="UTF8") as file:
    cv = json.load(file)

with open ("ficheiros_TP1/dicionario_final.json", "r", encoding="UTF8") as file:
    dic = json.load(file)

with open ("output/dic_mulher_final.json", "r", encoding="UTF8") as file:
    dic_mulher = json.load(file)

cv_new = {unidecode(key.lower()): value for key, value in cv.items()}
dic_mulher_new = {unidecode(key.lower()): value for key, value in dic_mulher.items()}
dic_new = {unidecode(key.lower()): value for key, value in dic.items()}

# 1º fase - junção do dicionário final TP1 com dicionário Cruz Verde
for key, value in dic_new.items():
    if value.get('Descrições') is None and unidecode(key.lower()) in cv_new.keys():
        value['Descrições'] = {'desc_pt':"Cruz Verde - " + cv_new[key]}
    elif value.get('Descrições') is not None and unidecode(key.lower()) in cv_new.keys():
        value['Descrições']['desc_pt'] = "Cruz Verde - " + cv_new[key]

# 2º fase - junção com o dicionário da mulher
for key, value in dic_mulher.items():
    if unidecode(key) not in dic_new.keys():
        dic[key] = value

for key, value in dic.items():
    if value.get('Descrições') is None and unidecode(key.lower()) in dic_mulher_new.keys():
        value['Descrições'] = {'desc_pt':dic_mulher_new[unidecode(key.lower())]['Descrições']['desc_pt'], 'desc_en':dic_mulher_new[unidecode(key.lower())]['Descrições']['desc_en']}
    elif value.get('Descrições') is not None and value['Descrições'].get('desc_pt') is None and unidecode(key.lower()) in dic_mulher_new.keys():
        value['Descrições']['desc_pt'] = dic_mulher_new[unidecode(key.lower())]['Descrições']['desc_pt']
        value['Descrições']['desc_en'] = dic_mulher_new[unidecode(key.lower())]['Descrições']['desc_en']

    if value.get('Traduções') is None and unidecode(key.lower()) in dic_mulher_new.keys():
        value['Traduções'] = {'en':dic_mulher_new[unidecode(key.lower())]['Traduções']['en']}

dic = dict(sorted(dic.items(), key=lambda x: locale.strxfrm(x[0])))

print(dic.keys())

file = open("output/novo_dic.json", "w",encoding="utf-8")
json.dump(dic, file, ensure_ascii=False, indent=4)
file.close()




