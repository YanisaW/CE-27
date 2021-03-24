import numpy as np
import random
import json

import torch
import torch.nn as nn
from setuptools.command.test import test
from torch.utils.data import Dataset, DataLoader

from nlp_utils import bag_of_words, tokenize
from model import NeuralNet

from pythainlp import word_tokenize, Tokenizer
from pythainlp.util import dict_trie
from pythainlp.corpus.common import thai_words


#Analyze Accuracy
# from torch.utils.tensorboard import SummaryWriter


# โหลดไฟล์ intents.json
with open('json/intents.json', encoding="utf8") as f:
    intents = json.load(f)

# โหลดไฟล์ dental_list.json
with open('json/Dental_lists.json', encoding="utf8") as d:
    dental_lists = json.load(d)

all_words = []
tags = []
xy = []
# types = []
homonyms = []

# for dental_list in dental_lists['dental_lists']:
#     type = dental_list['type']
#     types.append(type)
#     print("type: ", type, " || homonyms: ",dental_list['homonyms'])
#     for h in dental_list['homonyms']:
#         ht = tokenize(h)
#         homonyms.append((ht, type))

# Add word to Dictionary
words = [
 "สวีดัด", "หวัดดี",
 "วีเนียร์", "วีเนีย", "วิเนียร์", "วิเนีย",
 "จัดฟัน", "ดัดฟัน", "เหล็กดัด",
 "เอกซเรย์", "เอ็กซเรย์", "สแกน","แสกน",
 "พิมพ์ปาก", "พิมพ์ฟัน",
 "รีเทนเนอร์", "รีเทนเนอ",
 "ฟอกฟัน", "ฟอกสีฟัน",
 "ขูดหินปูน", "แอร์โฟลว์", "แอร์โฟล", "แอร์โฟ", "แอร์โฟร์",
 "โรคเหงือก",
 "เลเซอร์เหงือก", "เลเซอร์", "เลเซอเหงือก", "เลเสอเหงือก", "เลเสอร์เเหงือก", "เลเซอร์เหงือกชมพู", "เลเซอเหงือกชมพู", "เลเสอเหงือกชมพูู", "เลเสอร์เเหงือกชมพู",
 "ศัลยกรรมเหงือก", "ตกแต่งเหงือก", "ศัลย์เหงือก", "ผ่าเหงือก", "ตัดเหงือก", "ตกแต่ง", "ศัลยกรรม",
 "รักษารากฟัน",
 "อุดฟัน",
 "ถอนฟัน",
 "ผ่าฟันคุด", "ฟันคุด", "ถอนฟันคุด"
]
custom_words_list = set(thai_words())
## add multiple words
custom_words_list.update(words)
## add word
trie = dict_trie(dict_source=custom_words_list)
custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm')


# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']

    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        # w = tokenize(pattern)
        w = custom_tokenizer.word_tokenize(pattern)

        # add to our words list
        all_words.extend(w)

        # add to xy pair
        xy.append((w, tag))


ignore_words = ['?', '!', 'n','a','m','e', '(', ')', ' ', 'd','t', 'l','i','s','t']
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

        #for (homonym_sentence, type) in homonyms:
            #for i in range(0, len(pattern_sentence)): # ลูป i
                #if pattern_sentence[i] in homonym_sentence: #ดูว่ามีคำที่เหมือนใน homonym แค่ไหน แล้วจะเป็น type อะไร



X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters
num_epochs = 1500
batch_size = 32
learning_rate = 0.0001
input_size = len(X_train[0])
hidden_size = 32
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
#device =torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#writer = SummaryWriter(f'runs/MNIST/tryingout_tensorboard')

# step = 0
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

        #calculate running accuracy
        # _, predictions = outputs.max(1)
        # num_correct = (predictions == labels).sum()
        # running_train_acc = float(num_correct)/float(words.shape[0])
        #
        # writer.add_scalar('Training loss', loss, global_step=step)
        # writer.add_scalar('Training Accuracy',running_train_acc, global_step=step)
        # step+=1

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
    # "types": types
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')
