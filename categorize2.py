import gensim
from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import spacy
import string
import json

from deep_translator import GoogleTranslator


import gensim.downloader as api
# print(list(gensim.downloader.info()['models'].keys()))´

wv = api.load('glove-twitter-50')

file = open("./output/novo_dic.json", encoding='utf-8')
dic = dict(json.load(file))
file.close()

wv = api.load('word2vec-google-news-300')

health_terms = [
    "Allergy",
    "Antibiotics",
    "Antioxidants",
    "Arthritis",
    "Asthma",
    "BMI (Body Mass Index)",
    "Cancer",
    "Cardiovascular",
    "Cholesterol",
    "Cold",
    "Depression",
    "Diabetes",
    "Diet",
    "Exercise",
    "Fever",
    "Flu",
    "Genetics",
    "Headache",
    "Heart disease",
    "Immune system",
    "Infection",
    "Inflammation",
    "Insomnia",
    "Mental health",
    "Nutrition",
    "Obesity",
    "Pain",
    "Pneumonia",
    "Prescription",
    "Rehabilitation",
    "Respiratory",
    "Stress",
    "Surgery",
    "Vaccination",
    "Virus",
    "Wellness"
]

sim = {}

for key in dic.keys():
    sim_cat = []
    new_key = GoogleTranslator(source='en', target='pt').translate(key)
    for entry in health_terms:
        if new_key in wv and entry in wv:
            similarity = float(wv.similarity(new_key, entry))
            sim_cat.append({entry: similarity})
    sim[key] = sim_cat

with open('sim.json', 'w', encoding="utf8") as file:
    json.dump(sim, file, ensure_ascii=False, indent=4)


# for key, value in sim.items():
#     if value != []:


