from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import re

from deep_translator import GoogleTranslator

import gensim.downloader as api

file = open("./output/novo_dic.json", encoding='utf-8')
dic = dict(json.load(file))
file.close()

wv = api.load('word2vec-google-news-300') # modelo escolhido

# categorias escolhidas
categories = ["Allergy", "Antibiotics", "Antioxidants", "Arthritis", "Asthma", "BMI (Body Mass Index)",
    "Cancer", "Cardiovascular", "Cholesterol", "Cold", "Condition", "COVID-19", "Depression", "Diabetes",
    "Diet", "Disease", "Exercise", "Fever", "Flu", "Genetics", "Headache", "Heart disease", "Illness",
    "Immune system", "Infection", "Inflammation", "Insomnia", "Mental health", "Nutrition",
    "Obesity", "Pain", "Pneumonia", "Prescription", "Rehabilitation", "Respiratory", "Stress",
    "Surgery", "Symptom", "Vaccination", "Virus", "Wellness", "Woman"]

sim = {}

for key, value in dic.items():
    sim_cat = []
    # verificar se já existe alguma tradução em inglês
    if value.get("Traduções") is not None:
        if value['Traduções'].get('en') is not None:
            new_key = value['Traduções']['en'].split(",")[0]
            new_key = re.sub(r'\(.*\)', '', new_key)
            
            print("Original:", new_key)
    else: # caso não haja, traduz-se a chave
        new_key = GoogleTranslator(source='pt', target='en').translate(key)
        print("Traduzida:", new_key)
    
    # cálculo da similaridade e criação do dicionário com termo - categoria - similaridade
    for entry in categories:
        if new_key in wv and entry in wv:
            similarity = float(wv.similarity(new_key, entry))
            sim_cat.append({entry: similarity})
    sim[key] = sim_cat

with open('categorize/dic_similarity.json', 'w', encoding="utf8") as file:
    json.dump(sim, file, ensure_ascii=False, indent=4)