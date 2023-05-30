from flask import Flask, render_template, request, redirect
import json
import re

app = Flask(__name__)

file = open("./input/terms.json", encoding='utf-8')
db = json.load(file)
print(len(db))
file.close()

file_cat = open("./output/dic_categorias.json", encoding='utf-8')
cat = json.load(file_cat)
print(len(cat))
file_cat.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/terms")
def terms():
    return render_template("terms.html", designations=db.keys())


@app.route("/term/<t>")
def term(t):
    return render_template("term.html", designation=t, value=db.get(t, "None"))


@app.route("/add-term")
def add():
    return render_template("add_term.html", designations=db.keys())


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


@app.route("/terms/search")
def search_cat():
    
    category = request.args.get("category")
    cat_dic = {}
    msg1 = ""

    if category:
        if category in cat:
            cat_dic[category] = cat[category]

    if cat_dic == {}:
        msg1 = "O conteúdo pesquisado não existe. Pesquise de novo"

    return render_template("search.html", matched_cat = cat_dic, message1 = msg1)



@app.route("/term", methods=["POST"])
def addTerm():
    # print(request.form)
    designation = request.form["designation"]
    en = request.form["en"]
    es = request.form["es"]
    exp_pop = request.form["exp pop"]

    if designation not in db:
        info_message = "Termo Adicionado"
    else:
        info_message = "Termo Atualizado!"

    db[designation] = {"exp pop": exp_pop, "en": en, "es": es}

    # voltar a ordenar o dicionário depois de adicionar o novo termo
    myKeys = list(db.keys())
    myKeys = sorted(myKeys, key=lambda s: s.casefold())
    sorted_db = {i: db[i] for i in myKeys}

    file_save = open("./output/terms_changed.json","w", encoding="utf-8")
    json.dump(sorted_db, file_save, ensure_ascii=False, indent=4)
    file_save.close()

    return render_template("terms.html", designations=sorted_db.keys(), message = info_message)



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
        
    return {designation: {"exp pop": desc['exp pop']}}



@app.route("/categories")
def categories():
    return render_template("categories.html", categories=cat.items())


app.run(host="localhost", port=4000, debug=True)
