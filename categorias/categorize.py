import nltk
import json
from nltk.corpus import wordnet

with open('./ficheiros_TP1/dicionario_final.json', 'r', encoding="utf8") as file:
    dic = dict(json.load(file))

new_dic = {}
# Get synsets for the word
for word in dic.keys():
    print("----")
    # Print synonyms for each synset and their categories
    synsets = wordnet.synsets(word, lang='por')  # Specify the language as 'por' for Portuguese

    # Print synonyms and hypernyms for each synset
    for synset in synsets:
        print("Word:", word)
        print("Synset:", synset.name())
        print("Definition:", synset.definition())
        print("Synonyms:", synset.lemma_names())

        # Get hypernyms (superordinate categories) for the synset
        hypernyms = synset.hypernyms()
        print("Hypernyms:")
        for hypernym in hypernyms:
            print(hypernym.name())

            hypernym_name = hypernym.name().split('.')[0]
            if hypernym_name in new_dic:
                new_dic[hypernym_name].append({word:dic[word]})
            else:
                new_dic[hypernym_name] = [{word:dic[word]}]

file = open("./output/dic_categorias.json","w", encoding="utf8")
json.dump(new_dic,file, ensure_ascii=False, indent = 4)
file.close()

        