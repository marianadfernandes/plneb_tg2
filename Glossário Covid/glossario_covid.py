import re
import json
from deep_translator import GoogleTranslator

with open ("Glossário Covid/WIPOPearl_COVID-19_Glossary.xml","r", encoding="UTF8") as file:
    lines = file.read()

# Remover
lines = re.sub(r"</?text.*?>", "",lines)
lines = re.sub(r"</?page.*>", "", lines)
lines = re.sub(r'(<b> </b>)?<\/?i.*?>', "", lines)
lines = re.sub(r'<fontspec[^>]*>',"", lines)

#eliminar todo o texto até à página em que começa o glossário
eliminar = lines.find('<b>A </b>')
if eliminar != -1:
    lines=lines[eliminar:]

lines= re.sub(r"<b>[A-Z] </b>", "", lines)


lines = re.sub(r'\n', "", lines)
lines = re.sub(r'COVID-19 Glossary\s+\d+', "", lines)

# eliminar desde tradução àrabe até tradução francesa (exclusive)
# lines = re.sub(r'<b>\s*AR\s*</b>.*?(<b>F)', r'\1', lines)

# eliminar tradução japonesa e coreana
# lines = re.sub(r'<b>\s*JA\s*</b>.*?(<b>P)', r'\1', lines)

# fica-se com: termo, descrição, tradução FR, tradução PT, tradução RU e tradução ZH

# eliminar tradução russa e zh
# lines = re.sub(r'<b>\s*RU\s*</b>.*?(<b>[a-z])', r'\1', lines)

# fica-se com: termo, descrição, tradução FR e tradução PT

# eliminar lixo que permanece no documento original, como <b> </b> a separar frases
lines = re.sub(r'<b> </b>', r' ', lines)
lines = re.sub(r'</b><b>', r'', lines)

# eliminar os sinónimos quer nos termos quer nas descrições/traduções
# utilização de OU lógico "|"
# lines = re.sub(r',?\s?\(syn\.\).*?\s+([A-Z][a-z]|<b>)', r'\1', lines) 

# eliminar o que está depois das traduções e antes do termo seguinte (ex: MEDI, ...)
# lines = re.sub(r'\.\s+[A-Z].*?<', r'. <', lines)
# lines = re.sub(r'<b>MEDI.*?(<b)', r'\1', lines)

#corrigir simbolos
lines = re.sub(r'&gt;', r'>', lines)
lines = re.sub(r'&lt;', r'<', lines)
lines = re.sub(r'&amp;', r'&', lines)


alt = open("Glossário Covid/alterado.xml", "w", encoding="UTF8")
alt.write(lines)
alt.close()


# obtenção dos tuplos para posterior criação do dicionário
entries = re.findall(r"<b>\s*(.*?)\s*<\/b>(.*?)<b>\s*AR\s*<\/b>\s*(.*?)\s*<b>DE\s*<\/b>\s*(.*?)<b>ES\s*<\/b>\s*(.*?)<b>FR\s*<\/b>\s*(.*?)<b>JA\s*<\/b>\s*(.*?)<b>KO\s*<\/b>\s*(.*?)<b>PT\s*<\/b>\s*(.*?)<b>RU\s*<\/b>\s*(.*?)<b>ZH\s*<\/b>\s*(.*?)(?=<b>|\Z)", lines, re.DOTALL)

entries = [(term.strip(), desc.strip(), ar.strip().rstrip(), de.strip().rstrip(), es.strip().rstrip(), fr.strip().rstrip(), ja.strip().rstrip(), ko.strip().rstrip(), pt.strip().rstrip(), ru.strip().rstrip(), zh.strip().rstrip(),) for term, desc, ar, de, es, fr, ja, ko, pt, ru, zh in entries]


# formatação das entries para o dicionário
new_entries = [(term, ({"desc": desc, "ar": ar, "de": de, "es": es, "fr": fr, "ja": ja, "ko": ko, "pt": pt, "ru": ru, "zh": zh}))
                for term, desc, ar, de, es, fr, ja, ko, pt, ru, zh in entries]

dic = dict(new_entries)

for key, value in dic.items():
    dic[key] = {"desc_pt" : GoogleTranslator(source='en', target='pt').translate(value['desc']),
                  "desc_en" : value['desc'],
                "ar" : value['ar'],
                "de" : value['de'],
                "es" : value['es'],
                "fr" : value['fr'],
                "ja" : value['ja'],
                "ko" : value['ko'],
                "pt" : value['pt'],
                "ru" : value['ru'],
                "zh" : value['zh'],
}
         
with open('ficheiros_TP1/glos_covid.json', 'w', encoding="UTF8") as f:
    json.dump(dic, f, ensure_ascii=False, indent=4)