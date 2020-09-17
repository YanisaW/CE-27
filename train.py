import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from nlp_utils import bag_of_words, tokenize
#from model import NeuralNet


# โหลดไฟล์ intents.json
with open('intents.json', encoding="utf8") as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

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

ignore_words = ['?', '!', '(name)', '(', ')', ' ']
all_words = [w for w in all_words if w not in ignore_words]

#remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "cleaned words:", all_words)