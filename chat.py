import random
import json
import torch
import datetime
from model import NeuralNet
from nlp_utils import bag_of_words, tokenize

from firebase import firebase
url_fb = 'https://yimsuay-db-default-rtdb.firebaseio.com/'
fb_Data = firebase.FirebaseApplication(url_fb)

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
with open('json/intents.json', encoding="utf8") as json_data:
    intents = json.load(json_data)

with open('json/Dental_lists.json', encoding="utf8") as json_data:
    dental_lists = json.load(json_data)

with open('json/Dentist.json', encoding="utf8") as json_data:
    dentist = json.load(json_data)

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

# # Test the bot
# # userID = 'U43cfd551cb59bd993ccf46fec4762e55' #ไหม
# userID = 'U246b21848ae17fc7fdef81e75abe1eb4' #เอิร์น
# # userID = 'U0654c13b6cced7934ea2eb3208fa370b' #แม่ไหม
# userName = 'ลูกค้า'
# bot_name = "ยิ้มสวย"
#
# print("สวัสดีจ้า ยิ้มสวยยินดีให้บริการจ้า ^-^ (พิมพ์ 'ออก')")
# while True:
#     # sentence = "do you use credit cards?"
#     sentence = input("You: ")
#     if sentence == "ออก":
#         print(f"{bot_name}: ขอบคุณที่ใช้บริการยิ้มสวยนะคะ")
#         break
#
#     sentence = tokenize(sentence)
#     ignore_words = ['?', '!', '.','"','@','#','^','=','-',',','/','*','$','&','(',')',' ']
#     sentence = [w for w in sentence if w not in ignore_words]
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
#     if prob.item() > 0.9:
#         print(prob.item())
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 # print(tag)
#                 answer = random.choice(intent['responses'])
#                 result = None
#                 if tag == 'cancel' or tag == 'postpone':
#                     result = fb_Data.get('/members', '/' + userID + '/appointment')
#                     if result is None:
#                         answer = 'คุณ(customer_name) ยังไม่ได้ทำการจองนัดหมายกรุณาจองนัดก่อนค่ะ \nคลิกที่เมนูเพื่อจองนัด'
#                         tag = 'appointment'
#
#                 if '(name)' in answer:
#                     name = ""
#                     for dent in dentist['Dentist']:
#                         for dayWeek in dent['OnDuty']:
#                             if dayWeek == datetime.datetime.now().strftime("%a"):  # วันตรงกัน
#                                 name = name + "คุณหมอ" + dent['Name'] + " "
#                     answer = answer.replace('(name)', name)
#                 if '(customer_name)' in answer:
#                     answer = answer.replace('(customer_name)', userName)
#                 if '(date)' in answer or '(time)' in answer:
#                     if result is not None:
#                         for i, day in enumerate(result):
#                             if i + 1 == (len(result)):
#                                 time_str = result[day]['time']
#                                 date_time_str = result[day]['date']
#                                 date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
#                                 date_time_format = date_time_obj.strftime('%d-%m-%Y')
#
#                         answer = answer.replace('(date)', date_time_format).replace('(time)', time_str)
#                     else:
#                         time = datetime.datetime.now()
#                         answer = answer.replace('(date)', time.strftime("%x")).replace('(time)', time.strftime("%X"))
#                 if '(list)' in answer or '(price)' in answer:
#                     for dental in dental_lists["dental_lists"]:
#                         for a in dental["homonyms"]:
#                             if a in sentence:
#                                 list1 = (dental["homonyms"][0])
#                                 price = (dental["cost"])
#                                 print(list1, price)
#                                 answer = answer.replace('(list)', list1).replace('(price)', str(price))
#                                 break
#                     if '(list)' in answer or '(price)' in answer:
#                         answer = 'ราคา'
#                 print(f"{bot_name}: {answer}")
#     else:
#         print(f"{bot_name}: ยิ้มสวยไม่เข้าใจค่ะ ลองใหม่อีกครั้งค่ะ")


def question(sentence,userName, userID):
    sentence = tokenize(sentence)
    ignore_words = ['?', '!', '.', '"', '@', '#', '^', '=', '-', ',', '/', '*', '$', '&', '(', ')', ' ']
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
        print(prob.item())
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # print(tag)
                answer = random.choice(intent['responses'])
                result = None
                if tag == 'cancel' or tag == 'postpone':
                    result = fb_Data.get('/members', '/' + userID + '/appointment')
                    if result is None:
                        answer = 'คุณ(customer_name) ยังไม่ได้ทำการจองนัดหมายกรุณาจองนัดก่อนค่ะ \nคลิกที่เมนูเพื่อจองนัด'
                        tag = 'appointment'
                if '(name)' in answer:
                    name = ""
                    for dent in dentist['Dentist']:
                        for dayWeek in dent['OnDuty']:
                            if dayWeek == datetime.datetime.now().strftime("%a"): #วันตรงกัน
                                name = name + "คุณหมอ" + dent['Name'] + " "
                    answer = answer.replace('(name)', name)
                if '(customer_name)' in answer:
                    answer = answer.replace('(customer_name)', userName)
                if '(date)' in answer or '(time)' in answer:
                    if result is not None:
                        for i, day in enumerate(result):
                            if i + 1 == (len(result)):
                                time_str = result[day]['time']
                                date_time_str = result[day]['date']
                                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
                                date_time_format = date_time_obj.strftime('%d-%m-%Y')
                        answer = answer.replace('(date)', date_time_format).replace('(time)', time_str)
                    else:
                        time = datetime.datetime.now()
                        answer = answer.replace('(date)', time.strftime("%x")).replace('(time)', time.strftime("%X"))
                if '(list)' in answer or '(price)' in answer:
                    for dental in dental_lists["dental_lists"]:
                        for a in dental["homonyms"]:
                            if a in sentence:
                                list1 = (dental["homonyms"][0])
                                price = (dental["cost"])
                                print(list1, price)
                                answer = answer.replace('(list)', list1).replace('(price)', str(price))
                                break
                    if '(list)' in answer or '(price)' in answer:
                        answer = 'ราคา'

                return answer, tag
    else:
        return "ยิ้มสวยไม่เข้าใจค่ะ ลองถามใหม่อีกครั้งค่ะ", ""

# # test case
# test1 = ['สวัสดี', 'สวัสดีครับผม', "สบายดีไหม"]
# test2 = ['นัดทำฟัน', 'ขอทำฟัน', 'ขอไม่นัดหมอนะ']
## test3 = ['นัดอุดฟัน', 'อยากทำวีเนียร์', 'อยากจัดฟัน', 'ถอนฟัน', 'นัดเอ็กซเรย์', 'ทำฟันปลอมค่ะ', 'จะฟอกฟัน', 'ทำแอร์โฟลว', 'นัดทำเลเซอร์','นัดทั่วไป', 'ทำรากฟันเทียม', 'ฟันคุดค่ะ', 'พิมพ์ปากถ่ายรูป', 'ไม่นัดทำเอกซเรย์แล้ว']
# test4 = ['สอบถามราคา', 'จัดฟันราคาเท่าไหร่', 'ขัดหินปูนราคาเท่าไหร่', 'ตกแต่งเหงือกแพงมั้ย', 'ทำฟันปลอมกี่บาท']
# test5 = ['จัดฟันต้องทำยังไง', 'ขอคำปรึกษาหน่อยค่า', 'ไม่ปรึกษา']
# test6 = ['ขอยกเลิกการนัด','อยากยกเลิกนัด','ไม่ทำแล้ว','ไม่อยากทำ']
# test7 = ['ไม่ว่างไปทำฟันในวันนัด', 'ย้ายวันนัด', 'ไม่ว่าง จะยกเลิก']
# test8 = ['ผ่อนชำระได้ไหมคะ', 'จ่ายบัตรเครดิตได้มั้ย']
# test9 = ['คลีนิกเปิดกี่โมง', 'คลีนิกเปิดวันไหนบ้าง']
# test10 = ['อาเระ', 'skfdsokf','ทำไมตอบได้แล้ว','วันนี้วันอะไร']
# for i in test10:
#     print('You : ' + i)
#     print('Bot : ' + question(i))
#     print()