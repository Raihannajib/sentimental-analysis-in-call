from config import *


data = pd.read_csv(ROOT+'clients_all.csv', encoding='utf-8', error_bad_lines=False)
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


# stem_text = ""
# doc = nlp(u""+text_no_stop_words)
# for token in doc:
#     stem_text = stem_text + token.lemma_ + " "
# print(stem_text)
#########################################################################
with open('client_cleaned.txt', 'w' , encoding='utf-8') as output:
        print(text_no_stop_words, file=output)

stem_text_list = text_no_stop_words.split(" ")
############## Création du word cloud 
# ####### pos


verba_list_adapter = readFile("words\\verba_1.txt")


pos = [word for word in pos_list  if text_no_stop_words.find(word) != -1]
pos = [word for word in stem_text_list  for p_word in pos_list  if p_word == word]
print(pos)

if len(pos) > 0 :

    wordcloud_p = WordCloud(width = 500, height = 500,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 10).generate(Array_to_string(pos))
    
    # plot the WordCloud image                      
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud_p)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig(ROOT+'png/wordcloud_pos_all_clients.png')
    plt.show()

# ####### neg

neg = [word for word in neg_list if text_no_stop_words.find(word) != -1]
# neg =  [word for word in stem_text_list  for n_word in neg_list  if n_word == word]

print(neg)

if len(neg) > 0 :
    wordcloud_n = WordCloud(width = 500, height = 500,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 10).generate(Array_to_string(neg))
    
    # plot the WordCloud image                      
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud_n.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig(ROOT+'png/wordcloud_neg_all_clients.png')
    plt.show()

# ###### verbatim client speech
verba =  [word for word in stem_text_list  for word_v in verba_list if word.find(word_v) != -1 and word in verba_list]
verba_0  =  verba + [word for word in verba_list if text_no_stop_words.find(word) != -1 ]
length = len(verba_0)

# verba =  [word for word in stem_text_list  for v_word in verba_list  if v_word == word]


if len(verba) > 0 :
    wordcloud_v = WordCloud(width = 500, height = 500,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 10).generate(Array_to_string(verba_0))
    
    # plot the WordCloud image                      
    plt.figure(figsize = (4, 4), facecolor = None)
    plt.imshow(wordcloud_v)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig(ROOT+'png/wordcloud_verbatim_all_clients.png')
    plt.show()

print("*************Search for verbatim occurences in text*******************")

################ adaptation

motif_verba = [word for word in verba_0 for aword in verba_list_adapter if word.find(aword) != -1 ]

########    Categories
motifs = dict()
motifs["demandes"]=["demand","information"]
motifs["délais livraison"]=["délais","livr","journal","mal","paiement","suspens"]
motifs["point relais"]=["point","relais","kiosque","accès","disponib","vente","probl","site","revue"]
motifs["abonnement"]=["cher","trimistriel","abonn","annul","rembour"]
motifs["prix"]=["tarif","prix"]
motifs["changement d'adresse"]=["change","adres","tempor"]


########    find words inside category
d_motif = [0]*6
index=0
for key  in motifs :
    items = motifs[key] 
    for word in motif_verba:
        for item in items :
            if word.find(item) != -1:
                d_motif[index] += 1
    index+=1
f_motif = list(map(lambda x : x/length * 100,  d_motif ))

d=dict()
i=0
for key in motifs :
    d[key] = f_motif[i]
    i+=1



print("*********************freq Graph******************************************")
highest_dict = dict(sorted(d.items(), key = itemgetter(1), reverse = True)[:5])
x_pos = np.arange(len(highest_dict))
plt.figure(figsize=(10, 6))
plt.bar(x_pos, highest_dict.values(), color='maroon')
plt.xticks(x_pos, highest_dict.keys())
plt.savefig(ROOT+'png/freq_verb_all_clients.png')
plt.show()


########################## sentimental analysis
import torch
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
import plotly.graph_objects as go
import plotly.io as pio
import os


tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine", use_fast=True)
model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

nlp_s = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

result = nlp_s(text_no_stop_words)
print(result)
# [{'label': 'positive', 'score': 0.8461698889732361}]
sentiment = result[0]['label']
sentiment_p = result[0]['score']*100
color_2 = "red"
color_1 = "green"
if sentiment == "POSITIVE" :
    color_2 = "green"
    if color_2 == "green"  :
        color_1 = "red"


png_renderer = pio.renderers["png"]
png_renderer.width = 500
png_renderer.height = 500

pio.renderers.default = "png"

fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value =sentiment_p , 
    mode = "gauge+number",
    title = {'text': "Satisfaction"},
    gauge = {'axis': {'range': [None, 100]},
            'bar': {'color': 'orange'},
             'steps' : [
                 {'range': [0, sentiment_p ], 'color':color_2},
                 {'range': [sentiment_p ,100], 'color': color_1 }],
             'threshold' : {'line': {'color': "red", 'width': 4}, 
             'thickness': 1, 'value': sentiment_p }}))

fig.write_image("png/sentiment_clients.png")

#  install -c conda-forge python-kaleido



