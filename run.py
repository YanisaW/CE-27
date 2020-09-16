import torch
from pythainlp import sent_tokenize, word_tokenize
print(torch.__version__)
sentence_1 = "หีบมากมายหลายหีบยกหีบหนี หีบมากมีหนีหีบหนีบหนีหาย เห็นหนีหีบหนีบหนีกันมกกมาย เห็นหีบหายหลายหีบหนีบหนีเอย"
print("sent_tokenize:", sent_tokenize(sentence_1))
print("attacut:", word_tokenize(sentence_1, engine="attacut"))