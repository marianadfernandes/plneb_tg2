import requests
from bs4 import BeautifulSoup
import json
from deep_translator import GoogleTranslator
import locale

# definir localização/internacionalização 
locale.setlocale(locale.LC_COLLATE, 'pt_PT.UTF-8')

url = "https://www.acog.org/womens-health/dictionary"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

divs = soup.find_all("div", class_="wysiwyg-content section-terms")

dic = {}

for div in divs:
    terms = div.find_all("span", class_="section-term")
    for term in terms:

        title = term.text.strip() # Termo

        description = term.find_next("span").text.strip() #Descrição
       

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
#dic = sorted(dic.items())
dic = dict(sorted(dic.items(), key=lambda x: locale.strxfrm(x[0])))
      
file = open("acog.json", "w",encoding="utf-8")
json.dump(dic, file, ensure_ascii=False, indent=4)
file.close()