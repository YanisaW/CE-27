import torch
import json
from pythainlp import sent_tokenize, word_tokenize
from torchtext import data

print(torch.__version__)
sentence_1 = "หีบมากมายหลายหีบยกหีบหนี หีบมากมีหนีหีบหนีบหนีหาย เห็นหนีหีบหนีบหนีกันมกกมาย เห็นหีบหายหลายหีบหนีบหนีเอย"
print("sent_tokenize:", sent_tokenize(sentence_1))
print("attacut:", word_tokenize(sentence_1, engine="attacut"))

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)