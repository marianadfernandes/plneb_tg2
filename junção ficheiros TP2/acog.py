import requests
from bs4 import BeautifulSoup
import json
from deep_translator import GoogleTranslator
import locale
import re
 
locale.setlocale(locale.LC_COLLATE, 'pt_PT.UTF-8')

url = "https://www.acog.org/womens-health/dictionary"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")

divs = soup.find_all("div", class_="wysiwyg-content section-terms")

dic = {}
final_dic = {}

for div in divs:

    ps = div.find_all("p")

    for p in ps:
        termo = p.find("span", class_="section-term")
        if termo:
            t = termo.text
            t = re.sub('/', ',', t)
            descricao = p.find("span", class_="section-term-definition")
            if descricao:
                desc = descricao.text

                dic[t] = desc
    
                translator = GoogleTranslator(source='en', target='pt')
                translated_title = translator.translate(t)
                translated_description = translator.translate(desc)

                final_dic[translated_title] = {
                    "desc_pt": translated_description,
                    "en": t,
                    "desc_en": desc
                }


# Ordenar o dicionário por ordem alfabética
final_dic = dict(sorted(final_dic.items(), key=lambda x: locale.strxfrm(x[0])))

      
file = open("acog.json", "w",encoding="utf-8")
json.dump(final_dic, file, ensure_ascii=False, indent=4)
file.close()