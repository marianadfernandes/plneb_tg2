import json
import locale

locale.setlocale(locale.LC_ALL, '')

with open ("url_cruzverde.json", "r", encoding="UTF8") as file:
    cv = json.load(file)

with open ("ficheiros_TP1/dicionario_final.json", "r", encoding="UTF8") as file:
    dic = json.load(file)

count = 0
for key, value in dic.items():
    if value.get('Descrições') is None and key in cv.keys():
        value['Descrições'] = {'desc_pt':"Cruz Verde - " + cv[key]}
    elif value.get('Descrições') is not None and key in cv.keys():
        value['Descrições']['desc_pt'] = "Cruz Verde - " + cv[key]

dic = dict(sorted(dic.items(), key=lambda x: locale.strxfrm(x[0])))

file = open("output/novo_dic.json", "w",encoding="utf-8")
json.dump(dic, file, ensure_ascii=False, indent=4)
file.close()




