import random
import json
import torch
import datetime
from model import NeuralNet
from nlp_utils import bag_of_words, tokenize

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
with open('json/intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)

with open('json/Dental_lists.json', encoding="utf8") as json_data:
    dental_lists = json.load(json_data)


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

# Test the bot
# bot_name = "ยิ้มสวย"
# print("สวัสดีจ้า ยิ้มสวยยินดีให้บริการจ้า ^-^ (พิมพ์ 'ออก')")
# while True:
#     # sentence = "do you use credit cards?"
#     sentence = input("You: ")
#     if sentence == "ออก":
#         print(f"{bot_name}: ขอบคุณที่ใช้บริการยิ้มสวยนะคะ")
#         break
#
#     sentence = tokenize(sentence)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)
#
#     output = model(X)
#     _, predicted = torch.max(output, dim=1)
#
#     tag = tags[predicted.item()]
#     print(sentence)
#
#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 print(tag)
#                 answer = random.choice(intent['responses'])
#                 if '(name)' in answer:
#                     answer = answer.replace('(name)', 'สมหมาย')
#                 if '(customer_name)' in answer:
#                     answer = answer.replace('(customer_name)', 'ลูกค้า')
#                 if '(date)' in answer or '(time)' in answer:
#                     time = datetime.datetime.now()
#                     answer = answer.replace('(date)', time.strftime("%x")).replace('(time)', time.strftime("%X"))
#                 if '(list)' in answer or '(price)' in answer:
#                 #         list1 = random.choice(dental_lists["type"])
#                 #         price = random.choice(dental_lists["type"])
#                 #         print(f"{list1} & {price}")
#                     for dental in dental_lists["dental_lists"]:
#                         for a in dental["homonyms"]:
#                             if a in sentence:
#                                 list1 = (dental["homonyms"][0])
#                                 price = (dental["cost"])
#                                 print(list1, price)
#                                 answer = answer.replace('(list)', list1).replace('(price)', str(price))
#                                 break
#                             else:
#                                 answer = 'ราคา'
#
#
#
#                 print(f"{bot_name}: {answer}")
#     else:
#         print(f"{bot_name}: ยิ้มสวยไม่เข้าใจค่ะ ลองใหม่อีกครั้งค่ะ")

def question(sentence):
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                #print(tag)
                answer = random.choice(intent['responses'])
                if '(name)' in answer:
                    answer = answer.replace('(name)', 'สมหมาย')
                if '(customer_name)' in answer:
                    answer = answer.replace('(customer_name)', 'ลูกค้า')
                if '(date)' in answer or '(time)' in answer:
                    time = datetime.datetime.now()
                    answer = answer.replace('(date)', time.strftime("%x")).replace('(time)', time.strftime("%X"))
                if '(list)' in answer or '(price)' in answer:
                #         list1 = random.choice(dental_lists["type"])
                #         price = random.choice(dental_lists["type"])
                #         print(f"{list1} & {price}")
                    for dental in dental_lists["dental_lists"]:
                        for a in dental["homonyms"]:
                            if a in sentence:
                                list1 = (dental["homonyms"][0])
                                price = (dental["cost"])
                                print(list1, price)
                                answer = answer.replace('(list)', list1).replace('(price)', str(price))
                                break
                            else:
                                answer = 'ราคา'
                return answer
    else:
        return ("ยิ้มสวยไม่เข้าใจค่ะ ลองถามใหม่อีกครั้งค่ะ")