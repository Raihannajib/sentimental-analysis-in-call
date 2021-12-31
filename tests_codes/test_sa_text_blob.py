import pandas as pd 
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import nltk
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import re
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import string
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
import plotly.graph_objects as go
import plotly.express as px



nltk.download('stopwords')

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

data["Word_Tok"] = Aparole

################### Eliminer les stop words ##############
stop_words = set(stopwords.words('french'))

deselect_stop_words = ['n\'', 'ne','pas','plus','personne','aucun','ni','aucune','rien']
for w in deselect_stop_words:
    if w in stop_words:
        stop_words.remove(w)
        print(w)
    else:
        continue

Allfilteredparole=[]
for parole in data["Word_Tok"]:
    filteredparole = [w for w in parole if not ((w in stop_words) or (len(w) == 1))]
    Allfilteredparole.append(' '.join(filteredparole))

data["paroleAferPreproc"] = Allfilteredparole

for i in data["paroleAferPreproc"]:
    print(i)
senti_list = []
count_pos = 0
count_neg = 0
count_neut = 0

###### TextBlob donne une estimation des sentiments par polarité #################### pos si sup a 0 neg si inf a 0
for i in data["paroleAferPreproc"]:
    vs = tb(i).sentiment[0]
    print(i)
    if (vs > 0):
        senti_list.append('Positive')
        
    elif (vs < 0):
        senti_list.append('Negative')
        
    else:
        senti_list.append('Neutral')   

data["sentiment"] = senti_list
print(data.head())
########################################################
positif_words = ''
negatif_words = ''

# print('Fréquence des mots positifs: ', count_pos / total_mots)
# print('Fréquence des mots négatifs: ', count_neg / total_mots)

comment_words = ''
stopwords = set(STOPWORDS)

##############################################################################################################
for val in data["paroleAferPreproc"]:
    val = str(val)
 
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "

############## Création du word cloud 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()

############### Création du bar chart
data_bar = {'Positif': count_pos, 'Négatif': count_neg, 'Neutre': count_neut}
sentiments = list(data_bar.keys())
values = list(data_bar.values())

fig = plt.figure(figsize = (10, 5))

plt.bar(sentiments, values, color ='maroon',
        width = 0.4)
 
plt.xlabel("Sentiments")
plt.ylabel("Fréquences")
plt.title("Fréquences des differents sentiments des clients")
plt.show()


