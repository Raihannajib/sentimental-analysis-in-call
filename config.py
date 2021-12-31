from matplotlib.pyplot import stem, step
from numpy import number, positive
import pandas as pd 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
import spacy
import re
import nltk
import codecs
from typing import Counter
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from operator import itemgetter
import random


ROOT = 'C:/Users/AGENT/Documents/nicematin/'



nlp = spacy.load('fr_core_news_md')
nltk.download('stopwords')
nltk.download('vader_lexicon')
months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet"," août", "septembre", "octobre"," novembre"," décembre"]
numbers = ["zéro","quatre","huit","un","cinq","neuf","deux","six","dix"] 
s_w_list = []             
with open('words\\stopwords.txt') as file:
    for line in file:
        s_w_list.append(line.rstrip())

        
stop_words =  set(stopwords.words('french') + list(fr_stop) + months + numbers + s_w_list)



def readFile(fileName):
    with codecs.open(fileName,'r',encoding='utf-8-sig') as fileObj:
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return set(words)

def Array_to_string(s):
    return ' '.join(map(str,s))


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return f"hsl({random.randint(0, 33)}, 83%, 43%)" 



pos_list = readFile("words\\pos.txt")
neg_list = readFile("words\\neg1.txt")
verba_list = readFile("words\\verba.txt")