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
z_train = []

#for (homonym_sentence, type) in homonyms:
    #bag_ = bag_of_words(homonyms, all_words)

for (pattern_sentence, tag) in xy:
    #for (homonym_sentence, type) in homonyms:
        # X: bag of words (สร้างคลังคำศัพท์ คำไม่ซ้ำกันสร้าง ID)
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)
        # y: ไม่ทำ one-hot(ทำข้อมูลเป็นคอลัมน์ย่อยๆ)
        label = tags.index(tag) #[0,1,2,...]
        y_train.append(label)

        # z


X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters
num_epochs = 1000
batch_size = 8
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags) # number of different class
print(input_size, tags)

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
                          num_workers=0)

# กรณีมี GPU ถ้าไม่มีให้ใช้ CPU แทน
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# actual training loop
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device=device, dtype=torch.int64)

        # forward
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad() # empty the gradient first
        loss.backward() # to calculate the back propagration
        optimizer.step()

    # print it
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# print final loss after the training loop
print(f'final loss, Loss: {loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "hidden_size": hidden_size,
    "output_size": output_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')