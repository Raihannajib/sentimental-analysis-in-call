from config import *




data = pd.read_csv(ROOT+'agents_all.csv', encoding='utf-8', error_bad_lines=False)
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
with open('agent_cleaned.txt', 'w' , encoding='utf-8') as output:
        print(text_no_stop_words, file=output)

stem_text_list = text_no_stop_words.split(" ")
############## Création du word cloud 
# ####### pos

pos_list = readFile("words\\pos.txt")
neg_list = readFile("words\\neg1.txt")


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
    plt.savefig(ROOT+'png/wordcloud_pos_all_agents.png')
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
    plt.imshow(wordcloud_n)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig(ROOT+'png/wordcloud_neg_all_agents.png')
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
comportement = result[0]['score']*100
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
    value = comportement , 
    mode = "gauge+number",
    title = {'text': "Comportement d'agent"},
    gauge = {'axis': {'range': [None, 100]},
            'bar': {'color': 'orange'},
             'steps' : [
                 {'range': [0, comportement ], 'color':color_2},
                 {'range': [comportement ,100], 'color': color_1 }],
             'threshold' : {'line': {'color': "red", 'width': 4}, 
             'thickness': 1, 'value': comportement }}))

fig.write_image("png/behavior_agent.png")

#  install -c conda-forge python-kaleido



