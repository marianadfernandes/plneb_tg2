import requests
from bs4 import BeautifulSoup

url = "https://www.acog.org/womens-health/dictionary"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

sections = soup.find_all("section", class_="term-list-section")
lista = []
for section in sections:
    terms = section.find_all("h4", class_="term-title")
    for term in terms:
        title = term.text.strip() # Título do termo
        lista.append(title)

# Imprimir a lista completa de termos
print(lista)
