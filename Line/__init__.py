from flask import Flask, request, abort #abort ใช้รายงาน http
import requests
import json
import Line
from Line.configLine import *
from chat import *
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello', 200

@app.route('/webhook', methods = ['POST', 'GET'])
def webhook():
    if request.method == 'POST': #ได้รับข้อมูลจาก Line
        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        userID = payload['events'][0]['source']['userId']
        print(userID)
        # groupID = payload['events'][0]['source']['groupId']
        # print(groupID)
        #answer = 'สวัสดีค่ะ'
        answer = question(message)
        #answer = answer1 +' ID :'+userID
        if answer == "ยิ้มสวยไม่เข้าใจค่ะ ลองถามใหม่อีกครั้งค่ะ":
            #PushMessage(Line.configLine.groupID, message, Line.configLine.Channel_access_token)
            contactAdmin(Reply_token, Line.configLine.Channel_access_token)
        else:
            ReplyMessage(Reply_token, answer, Line.configLine.Channel_access_token)
        return request.json, 200 #success
    elif request.method == 'GET': # GET การดูหน้าเว็บ
        return 'This is method GET',200
    else:
        abort(400)

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    if TextMessage == 'ราคา':
        data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "image",
                "originalContentUrl": "https://i.ibb.co/7zMvYQw/price-bigl.jpg",
                "previewImageUrl": "https://i.ibb.co/7zMvYQw/price-bigl.jpg"
            }]
        }

    else:
        data = {
            "replyToken":Reply_token,
            "messages":[{
                "type":"text",
                "text":TextMessage
            }]
        }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200

# def PushMessage(id, TextMessage, Line_Acees_Token):
#     LINE_API = 'https://api.line.me/v2/bot/message/push'
#
#     Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
#     print(Authorization)
#     headers = {
#         'Content-Type': 'application/json; charset=UTF-8',
#         'Authorization': Authorization
#     }
#
#     data = {
#         "to": id,
#         "messages": [{
#             "type": "text",
#             "text": TextMessage
#             }]
#         }
#
#
#     data = json.dumps(data) ## dump dict >> Json Object
#     r = requests.post(LINE_API, headers=headers, data=data)
#     return 200

def contactAdmin(Reply_token, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
            "replyToken":Reply_token,
            "messages":[
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://i.ibb.co/PxRtXZc/image.png",
                        "size": "full",
                        "aspectRatio": "2:1",
                        "aspectMode": "cover",
                        "action": {
                            "type": "uri",
                            "uri": "https://linecorp.com"
                        },
                        "margin": "none",
                        "align": "end",
                        "gravity": "center",
                        "offsetTop": "none",
                        "offsetEnd": "none",
                        "offsetBottom": "none",
                        "offsetStart": "none"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "action": {
                            "type": "uri",
                            "uri": "https://linecorp.com"
                        },
                        "contents": [
                            {
                                "type": "text",
                                "text": "ยิ้มสวยไม่เข้าใจค่ะ ",
                                "size": "lg",
                                "weight": "bold",
                                "color": "#232323"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": []
                            },
                            {
                                "type": "text",
                                "text": "สามารถติดต่อสอบถามแอดมินได้ค่ะ",
                                "color": "#636463",
                                "size": "md"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "spacer",
                                "size": "xxl"
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "color": "#00ac00",
                                "action": {
                                    "type": "uri",
                                    "label": "ติดต่อแอดมิน",
                                    "uri": "https://lin.ee/4AhDoDQ"
                                }
                            }
                        ]
                    }
                }
            ]
        }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200