from flask import Flask, render_template, request
import json
import re
from deep_translator import GoogleTranslator


app = Flask(__name__)


file = open("./output/novo_dic.json", encoding='utf-8')
db = json.load(file)
print("tamanho dicionário final: ", len(db))
file.close()

file_cat = open("./output/dic_categorias_final.json", encoding='utf-8')
cat = json.load(file_cat)
print("tamanho dicionário categorias: ", len(cat))
file_cat.close()

# file_img = open("./output/img_elements.json", encoding='utf-8')
# imgs = json.load(file_img)
# print("tamanho dicionário imagens: ",  len(imgs))
# file_img.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/terms")
def terms():
    return render_template("terms.html", designations=db.keys())


@app.route("/term/<designation>", methods=["DELETE"])
def deleteTerm(designation):
    desc = db[designation]
    if designation in db:
        print(designation)
        del db[designation] 
        print(db.get(designation))
        file_save = open("./output/terms_changed.json","w", encoding="utf-8")
        json.dump(db, file_save, ensure_ascii=False, indent=4)
        file_save.close()
        
    return {designation: {"desc": desc}}


@app.route("/term/<t>")
def term(t):
    return render_template("term.html", designation=t, value=db.get(t, "None"))


@app.route("/categories")
def categories():
    return render_template("categories.html", categories=cat.items())


@app.route("/table")
def table():
    return render_template("table.html", designations=db.items())



@app.route("/terms/search")
def search():

    text = request.args.get("text")
    lista = []
    msg = ""

    if text:
        for designation, description in db.items():
            if re.search(text, designation, flags=re.I):
                    lista.append((designation, description))
                
            else:
                # percorre as chaves do dicionário grande, ou seja Descrições / Traduções
                for value in description.values():
                        for item in list(value.values()):
                            if re.search(text, item, flags=re.I):
                                lista.append((designation, description))
        
    category = request.args.get("category")
    cat_dic = {}

    if category:
        for key in cat:
            if re.search(category, key, flags=re.I):
                cat_dic[key] = cat[key]


    if (len(lista) == 0 and cat_dic == {}) and (text or category):
        msg = "O conteúdo pesquisado não existe. Pesquise de novo"
    
    return render_template("search.html", matched = lista, matched_cat = cat_dic, message = msg)



@app.route("/add-term")
def add():
    return render_template("add_term.html", designations=db.keys())


@app.route("/term", methods=["POST"])
def addTerm():
    # print(request.form)
    designation = request.form["designation"]
    desc_pt = request.form["desc_pt"]

    if designation not in db:
        info_message = "Termo Adicionado"
    else:
        info_message = "Termo Atualizado!"

    desc_en = GoogleTranslator(source='pt', target='en').translate(desc_pt)
    en = GoogleTranslator(source='pt', target='en').translate(designation)
    es = GoogleTranslator(source='pt', target='es').translate(designation)
    fr = GoogleTranslator(source='pt', target='fr').translate(designation)
    ar = GoogleTranslator(source='pt', target='ar').translate(designation)
    de = GoogleTranslator(source='pt', target='de').translate(designation)
    ja = GoogleTranslator(source='pt', target='ja').translate(designation)
    ko = GoogleTranslator(source='pt', target='ko').translate(designation)
    ru = GoogleTranslator(source='pt', target='ru').translate(designation)
    zh = GoogleTranslator(source='pt', target='zh-CN').translate(designation)


    db[designation] = {
        "Descrições": {
            "desc_pt": desc_pt,
            "exp pop": "",
            "desc_en": desc_en,
            "syn": ""
        },
        "Traduções": {
            "en": en,
            "es": es,
            "fr": fr,
            "ar": ar,
            "de": de,
            "ja": ja,
            "ko": ko,
            "ru": ru,
            "zh": zh
        }
    }

    # voltar a ordenar o dicionário depois de adicionar o novo termo
    myKeys = list(db.keys())
    myKeys = sorted(myKeys, key=lambda s: s.casefold())
    sorted_db = {i: db[i] for i in myKeys}

    file_save = open("./output/terms_changed.json","w", encoding="utf-8")
    json.dump(sorted_db, file_save, ensure_ascii=False, indent=4)
    file_save.close()

    return render_template("term.html", designation=designation, value=sorted_db.get(designation), message = info_message)





#--------------------- Case study: Saúde da Mulher ---------------------

file = open("./output/dic_mulher_final.json", encoding='utf-8')
mulher = json.load(file)
print("tamanho dicionário mulher: ", len(mulher))
file.close()

@app.route("/terms-woman")
def terms_woman():
    return render_template("terms_woman.html", designations=mulher.keys())


@app.route("/term-woman/<t>")
def term_woman(t):
    keys_list = list(mulher.keys())
    index = keys_list.index(t)
    
    # images=imgs
    return render_template("term_woman.html", designation=t, value=mulher.get(t, "None"), index=index)


@app.route("/terms-woman/search")
def search_woman():

    text = request.args.get("text")
    lista = []
    msg = ""

    if text:
        for designation, description in mulher.items():
            if re.search(text, designation, flags=re.I):
                if designation not in lista:
                    lista.append((designation, description))
            
            else:
                # percorre as chaves do dicionário grande, ou seja Descrições / Traduções
                for value in description.values():
                    for item in list(value.values()):
                        if re.search(text, item, flags=re.I):
                            if designation not in lista:
                                lista.append((designation, description))
    
    
    if len(lista) == 0 and text:
        msg = "O conteúdo pesquisado não existe. Pesquise de novo"
    
    designations = mulher.keys()
    
    return render_template("terms_woman.html", matched = lista, message = msg, designations=designations)


@app.route("/term-woman/<designation>", methods=["DELETE"])
def deleteTerm_woman(designation):
    desc = mulher[designation]
    if designation in mulher:
        print(designation)
        del mulher[designation] 
        print(mulher.get(designation))
        file_save = open("./output/terms_changed_woman.json","w", encoding="utf-8")
        json.dump(db, file_save, ensure_ascii=False, indent=4)
        file_save.close()
        
    return {designation: {"desc": desc}}


app.run(host="localhost", port=4000, debug=True)
