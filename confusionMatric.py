import random
import json
import torch
import datetime
from model import NeuralNet
from nlp_utils import bag_of_words, tokenize

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
with open('json/intents_test.json', encoding="utf8") as json_data:
    intents = json.load(json_data)

# with open('json/Dental_lists.json', encoding="utf8") as json_data:
#     dental_lists = json.load(json_data)
#
# with open('json/Dentist.json', encoding="utf8") as json_data:
#     dentist = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

y_Actual = []
y_Predicted = []
for intent in intents["intents"]:
    for sentence in intent["patterns"]:
        y_Actual.append(intent["tag"])
        sentence = tokenize(sentence)
        ignore_words = ['?', '!', '.','"','@','#','^','=','-',',','/','*','$','&','(',')',' ']
        sentence = [w for w in sentence if w not in ignore_words]
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.9:
            y_Predicted.append(tag)
        else:
            y_Predicted.append("none")

# print(len(y_Actual), len(y_Predicted))
print(y_Actual)
print(y_Predicted)
tag_none = tags
tag_none.append("none")
data = {'y_Actual':   y_Actual,
        'y_Predicted': y_Predicted
        }

df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
confusion_matrix = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Actual'], colnames=['Predicted'])

sn.heatmap(confusion_matrix, annot=True)
plt.show()