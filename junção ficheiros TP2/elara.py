import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import locale
import json

# definir localização/internacionalização 
locale.setlocale(locale.LC_COLLATE, 'pt_PT.UTF-8')

url = "https://elara.care/culture/female-health-glossary/"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

# Encontrar todos os elementos <li> dentro da seção
li_elements = soup.select('section.gh-content li')

dic = {}

# Iterar sobre os elementos <li> e extrair os termos e descrições
for li in li_elements:
    title, description = li.text.split(":")

    translator = GoogleTranslator(source='en', target='pt')
    translated_title = translator.translate(title)
    translated_description = translator.translate(description)

    dic[translated_title] = {
        "desc_pt": translated_description,
        "en": title,
        "desc_en": description
        }
    
    print(dic)

# Ordenar o dicionário por ordem alfabética
dic = dict(sorted(dic.items(), key=lambda x: locale.strxfrm(x[0])))
      
file = open("elara.json", "w",encoding="utf-8")
json.dump(dic, file, ensure_ascii=False, indent=4)
file.close()
  
