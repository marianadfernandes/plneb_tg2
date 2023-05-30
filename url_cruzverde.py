import requests
from bs4 import BeautifulSoup
import json

url = "http://www.cruzverde.pt/apoio-cliente/glossario-saude"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")
divs = soup.find_all("div", class_="tab-content")

lista = []
for div in divs:
    terms = div.find_all("h2") # Obter todos os elementos h2 dentro da div

    for i, term in enumerate(terms):
        if i == len(terms) - 1:  # Ignorar o último elemento
            continue

        title = term.text.strip() # Título do termo
        description = term.find_next("p").text.strip() # Descrição do termo

        lista.append({title: description})

# Imprimir a lista completa
print(lista)

file = open("url_cruzverde.json", "w",encoding="utf-8")
json.dump(lista, file, ensure_ascii=False, indent=4)
file.close()



