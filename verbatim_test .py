import codecs
from typing import Counter
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from operator import itemgetter
from wordcloud import WordCloud
from PIL import Image
import csv



def read_txt_lines(fileName):
    with codecs.open(fileName, "r", encoding='utf-8') as fileObj :
        words = []
        lines = fileObj.read().splitlines()
        words = lines
        fileObj.close()
        return words

def read_txt(fileName):
    with codecs.open(fileName, "r", encoding="utf-8") as fileObj :
        words = []
        for line in fileObj :
            for item in line.split(" "):
                words.append(item)
        fileObj.close()
        return words

d = dict()
max_verbatim = 10
root_path = 'C:/Users/AGENT/Documents/nicematin/'
words = read_txt(root_path + "client_cleaned.txt")
word_text = ' '.join(map(str,words))
verbatim_wc = read_txt_lines(root_path + "words/verba.txt")
verba_text = ' '.join(map(str,verbatim_wc))

count_words = len(words)


print("*************Search for verbatim occurences in text*******************")

verba = [word for word in verbatim_wc  if word_text.find(word) != -1]
# verba = verba + [word for word in words  for v_word in verbatim_wc  if v_word == word]
for word in verba:
    if word not in d.keys():
        d[word]= words.count(word) 


print("*************Dictionary*****************************")
for key in list(d.keys()):
    print(key, ":", d[key])


print("*********************freq Graph******************************************")
highest_dict = dict(sorted(d.items(), key = itemgetter(1), reverse = False)[:max_verbatim])
x_pos = np.arange(len(highest_dict))
plt.figure(figsize=(10, 6))
plt.bar(x_pos, highest_dict.values(), color='maroon')
plt.xticks(x_pos, highest_dict.keys())
plt.savefig(root_path+'png/freq_verb_all_clients.png')
plt.show()


print("*********************Wordcloud******************************************")
try:
    cloud_mask = np.array(Image.open("cloud.gif"))
    wordcloud_text = " ".join(word for word in list())
    wordcloud = WordCloud(mask=cloud_mask,width =500, height = 500,
                        background_color ='white',
                        min_font_size = 10).generate_from_frequencies(d)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.savefig(root_path+'png/wordcloud_verbatim_all_clients.png')
    plt.show()
except Exception as e :
    print(e)

