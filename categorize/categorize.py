import json
from deep_translator import GoogleTranslator

file = open("categorize/dic_similarity.json", encoding='utf-8')
sim = dict(json.load(file))
file.close()

category_dic = {}

for key, values in sim.items():
    if not values:  # verifica casos de termos que não se encontravam presentes no modelo
        category = "No Category"
    else:
        max_value = float('-2')  # inicializa com um valor muito pequeno
        max_term = ""

        for item in values:
            for term, value in item.items():
                if value > max_value: 
                    max_value = value
                    max_term = term

        category = max_term

    if category not in category_dic:
        category_dic[category] = []

    category_dic[category].append(key)


with open('categorize/dic_categories.json', 'w', encoding="utf8") as out:
    json.dump(category_dic, out, ensure_ascii=False, indent=4)


file1 = open("./output/novo_dic.json", encoding='utf-8')
novo_dic = dict(json.load(file1))
file1.close()


#---------------------------------- Dicionário de categorias final para interface
dic_cat_final = {}

for key, values in category_dic.items():
    terms = []
    trans_key = GoogleTranslator(source='en', target='pt').translate(key)
    if key != "No Category":
        for value in values:
            for key1 in list(novo_dic.keys()):
                if value == key1:
                    terms.append({key1: novo_dic.get(key1)})
            dic_cat_final[trans_key] = terms


keys = list(dic_cat_final.keys())
keys = sorted(keys, key=lambda s: s.casefold())
sorted_dic = {i: dic_cat_final[i] for i in keys}

with open('./output/dic_categorias_final.json', 'w', encoding="utf8") as out2:
    json.dump(sorted_dic, out2, ensure_ascii=False, indent=4)