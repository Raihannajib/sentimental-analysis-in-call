from matplotlib.pyplot import stem, step
from numpy import number
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

# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# sid = SentimentIntensityAnalyzer()
# sid.polarity_scores(sentence)

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
        return words

def Array_to_string(s):
    return ' '.join(map(str,s))




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

text_no_stop_words =Array_to_string([word for word in tokenz if word not in (stop_words) and  len(word) > 3])

##################### lemmatisation ou racinisation (stemming) ###########


stem_text = ""
doc = nlp(u""+text_no_stop_words)
for token in doc:
    stem_text = stem_text + token.lemma_ + " "

#########################################################################
with open('text_cleaned\\client_cleaned.txt', 'w' , encoding='utf-8-sig') as output:
        print(stem_text, file=output)

stem_text_list = stem_text.split(" ")
############## Création du word cloud 
####### pos

pos_list = readFile("words\\pos.txt")
pos = [word for word in stem_text_list  for p_word in pos_list if word.find(p_word) != -1]
print(pos)

if len(pos) > 0 :

    wordcloud_p = WordCloud(width = 300, height = 300,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 10).generate(Array_to_string(pos))
    
    # plot the WordCloud image                      
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud_p)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    plt.show()

####### neg

neg_list = readFile("words\\neg.txt")
neg = [word for word in stem_text_list for n_word in neg_list if word.find(n_word) != -1]
print(neg)

if len(neg) > 0 :
    wordcloud_n = WordCloud(width = 300, height = 300,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 10).generate(Array_to_string(neg))
    
    # plot the WordCloud image                      
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud_n)
    plt.axis("off")
    plt.tight_layout(pad = 0)
 
    plt.show()

###### verbatim

verba_list = readFile("words\\verbatim.txt")
verba = [word for word in stem_text_list for v_word in verba_list if word.find(v_word) != -1 ]

if len(verba) > 0 :
    wordcloud_v = WordCloud(width = 300, height = 300,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 10).generate(Array_to_string(verba))
    
    # plot the WordCloud image                      
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud_v)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    plt.show()


########################## sentimental analysis

# import torch
# from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
# from transformers import pipeline


# tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine", use_fast=True)
# model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

# nlp_s = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# result = nlp_s(stem_text)
# print(result)




