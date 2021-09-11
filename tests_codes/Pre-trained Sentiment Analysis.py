from matplotlib.pyplot import stem
import pandas as pd 
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
import spacy
import re
import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# sid = SentimentIntensityAnalyzer()
# sid.polarity_scores(sentence)

nlp = spacy.load('fr_core_news_md')
nltk.download('stopwords')
nltk.download('vader_lexicon')

stop_words =  set(stopwords.words('french') + list(fr_stop))

data = pd.read_csv('C:/Users/AGENT/Documents/newproject/client.csv', encoding='ISO-8859-1', error_bad_lines=False)

# Se débarasser des lignes dont la valeur est nan
NAN = [(c, data[c].isna().mean()*100) for c in data]
NAN = pd.DataFrame(NAN, columns=["column_name", "percentage"])
NAN.sort_values("percentage", ascending=False)

data =data.dropna()

NAN = [(c, data[c].isna().mean()*100) for c in data]
NAN = pd.DataFrame(NAN, columns=["column_name", "percentage"])
NAN.sort_values("percentage", ascending=False)


data["paroles"] = data["paroles"].str.lower()


Aparole=[]

############# Tokenizing the words in each row
for parole in data["paroles"].apply(str):
    Word_Tok = []
    for word in  re.sub("\W"," ",parole ).split():
        Word_Tok.append(word)
    Aparole.append(Word_Tok)

tokenz = Aparole[0]

################### Eliminer les stop words ##############

text_no_stop_words =' '.join(map(str,[word for word in tokenz if word not in (stop_words)]))

##################### lemmatisation ou racinisation (stemming) ###########


stem_text = ""
doc = nlp(u""+text_no_stop_words)
for token in doc:
    stem_text = stem_text + token.lemma_ + " "
print(stem_text)


############## Création du word cloud 
# wordcloud = WordCloud(width = 800, height = 800,
#                 background_color ='white',
#                 stopwords = stop_words,
#                 min_font_size = 10).generate(stem_text)
 
# # plot the WordCloud image                      
# plt.figure(figsize = (8, 8), facecolor = None)
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.tight_layout(pad = 0)
 
# plt.show()


########################## sentimental analysis

import torch
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline


tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine", use_fast=True)
model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

nlp_s = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

result = nlp_s(stem_text)
print(result)




