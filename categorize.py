import nltk
import json
from nltk.corpus import wordnet

with open('./ficheiros/dicionario_final.json', 'r', encoding="utf8") as file:
    dic = dict(json.load(file))

# Get synsets for the word
for word in dic.keys():
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
        
        print("----")