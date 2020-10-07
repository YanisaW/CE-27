import numpy as np
import random
import json

import torch
import torch.nn as nn
from setuptools.command.test import test
from torch.utils.data import Dataset, DataLoader

from nlp_utils import bag_of_words, tokenize
from model import NeuralNet


# โหลดไฟล์ intents.json
with open('json/intents.json', encoding="utf8") as f:
    intents = json.load(f)

# โหลดไฟล์ dental_list.json
with open ('json/Dental_lists.json', encoding="utf8") as d:
    dental_lists = json.load(d)

all_words = []
tags = []
xy = []
types = []
homonyms = []

for dental_list in dental_lists['dental_lists']:
    type = dental_list['type']
    types.append(type)
    print("type: ", type, " || homonyms: ",dental_list['homonyms'])
    for h in dental_list['homonyms']:

        ht = tokenize(h)
        homonyms.append((ht, type))
print(homonyms)

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']

    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern)

        # add to our words list
        all_words.extend(w)

        # add to xy pair
        xy.append((w, tag))

ignore_words = ['?', '!', 'name', '(', ')', ' ', 'date', 'list', 'time']
all_words = [w for w in all_words if w not in ignore_words]

#remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))
#print(xy)
#print(len(xy), "patterns")
#print(len(tags), "tags:", tags)
#print(len(all_words), "cleaned words:", all_words)