########################## sentimental analysis

import torch
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline


tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine", use_fast=True)
model = TFAutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine")

nlp_s = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

result = nlp_s(stem_text)
print(result)