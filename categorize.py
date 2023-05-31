import nltk
import json
from nltk.corpus import wordnet
import locale
from deep_translator import GoogleTranslator
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

# definir localização/internacionalização 
locale.setlocale(locale.LC_ALL, '')

with open('./output/novo_dic.json', 'r', encoding="utf8") as file:
    dic = dict(json.load(file))

new_dic = {}
for word in dic.keys():
    print("----")
    trans_key = GoogleTranslator(source='pt', target='en').translate(word)
    synsets = wordnet.synsets(trans_key, lang='eng')

    for synset in synsets:
        print("Word:", word)
        print("Synset:", synset.name())
        print("Definition:", synset.definition())
        print("Synonyms:", synset.lemma_names())
        print("Category:", synset.lexname())

        # ir buscar categoria associada ao termo
        hypernyms = synset.hypernyms()
        print("Hypernyms:")
        for hypernym in hypernyms:
            print(hypernym.name())

            if "_" in hypernym.name():
                hypernym_name = hypernym.name().split('.')[0].split('_')[0] + hypernym.name().split('.')[0].split('_')[1]
                hypernym_name = GoogleTranslator(source='en', target='pt').translate(hypernym_name)
            else:
                hypernym_name = GoogleTranslator(source='en', target='pt').translate(hypernym.name().split('.')[0])

            if hypernym_name in new_dic:
                # verifica se o termo já lá está para não duplicar
                existing_words = [item for item in new_dic[hypernym_name] if word in item]
                if not existing_words:
                    new_dic[hypernym_name].append({word: dic[word]})
            else:
                new_dic[hypernym_name] = [{word:dic[word]}]

new_dic = dict(sorted(new_dic.items(), key=lambda x: locale.strxfrm(x[0])))

# nlp = spacy.load("pt_core_news_md")
# nlp.add_pipe("spacy_wordnet", after='parser')

# new_dic = {}
# for key in dic.keys():
#     doc = nlp(key)
#     print("key:", key)
#     key_token = doc[0]  # Get the first token in the document (the whole key)
#     print("key token:", key_token)
#     for sense in key_token._.wordnet._Wordnet__synsets(key_token, 'por'):
#         hypernyms = sense.hypernyms()
#         if hypernyms:
#             print("Hypernyms for", key_token.text)
#             for hypernym in hypernyms:
#                 print(hypernym)
#                 if "_" in hypernym.name():
#                     hypernym_name = hypernym.name().split('.')[0].split('_')[0] + hypernym.name().split('.')[0].split('_')[1]
#                     hypernym_name = GoogleTranslator(source='en', target='pt').translate(hypernym_name)
#                 else:
#                     hypernym_name = GoogleTranslator(source='en', target='pt').translate(hypernym.name().split('.')[0])

#                 if hypernym_name in new_dic:
#                     # verifica se o termo já lá está para não duplicar
#                     existing_words = [item for item in new_dic[hypernym_name] if key_token in item]
#                     if not existing_words:
#                         new_dic[hypernym_name].append({key: dic[key]})
#                     else:
#                         new_dic[hypernym_name] = [{key:dic[key]}]

# new_dic = dict(sorted(new_dic.items(), key=lambda x: locale.strxfrm(x[0])))

file = open("./output/dic_categorias.json","w", encoding="utf8")
json.dump(new_dic,file, ensure_ascii=False, indent = 4)
file.close()

        