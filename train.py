import numpy as np
import random
import json

import torch
import torch.nn as nn
from setuptools.command.test import test
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

ignore_words = ['?', '!', '(name)', '(', ')', ' ','name', 'list', 'date', 'time']
all_words = [w for w in all_words if w not in ignore_words]

#remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "cleaned words:", all_words)

#test change intent with variable
# test = ''
# for p in intents['intents']:
#     if p['tag'] == 'cancel':
#         for q in p['responses']:
#             test = q
# print(test)
# test = test.replace('(list)', 'อุดฟัน').replace('(date)', '24 กย').replace('(time)', '15.00')
# print(test)

X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words (สร้างคลังคำศัพท์ คำไม่ซ้ำกันสร้าง ID)
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    # y: ไม่ทำ one-hot(ทำข้อมูลเป็นคอลัมน์ย่อยๆ)
    label = tags.index(tag) #[0,1,2,...]
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters
batch_size = 8

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # dataset[index]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # len(dataset)
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=2)