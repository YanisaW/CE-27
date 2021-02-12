from flask import Flask, request, abort #abort ใช้รายงาน http
import requests
import json
import Line
from Line.configLine import *
from chat import *
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
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
        line_bot_api = LineBotApi(Line.configLine.Channel_access_token)
        profile = line_bot_api.get_profile(userID)
        # error handle
        # userName = payload['events'][0]['source']['displayName']
        # groupID = payload['events'][0]['source']['groupId']
        # print(groupID)
        #answer = 'สวัสดีค่ะ'
        answer = question(message, profile.display_name)
        #answer = answer1 +' ID :'+userID
        if answer == "ยิ้มสวยไม่เข้าใจค่ะ ลองถามใหม่อีกครั้งค่ะ":
            #PushMessage(Line.configLine.groupID, message, Line.configLine.Channel_access_token)
            noAnswer(Reply_token, Line.configLine.Channel_access_token)
        elif answer == "แผนที่":
            location(Reply_token, Line.configLine.Channel_access_token)
        elif "เบอร์โทร" in answer:
            contractAdmin(Reply_token, Line.configLine.Channel_access_token)
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
            "messages":[
                {
                "type":"text",
                "text":TextMessage
                },
                {
                    "type": "flex",
                    "altText": "เมนูช่วยเหลือ",
                    "contents":
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "image",
                                                        "url": "https://i.ibb.co/ZMp4czb/rich-menu-1.png",
                                                        "action": {
                                                            "type": "message",
                                                            "label": "action",
                                                            "text": "นัดจองคุณหมอ"
                                                        },
                                                        "size": "full",
                                                        "aspectRatio": "2:3",
                                                        "margin": "none"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "image",
                                                        "url": "https://i.ibb.co/NsqJyRC/rich-menu-2.png",
                                                        "position": "relative",
                                                        "aspectRatio": "2:3",
                                                        "action": {
                                                            "type": "uri",
                                                            "label": "action",
                                                            "uri": "https://liff.line.me/1655583873-GbO3xBzl"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "image",
                                                        "url": "https://i.ibb.co/kcrBMRk/rich-menu-3.png",
                                                        "aspectRatio": "2:3",
                                                        "action": {
                                                            "type": "message",
                                                            "label": "action",
                                                            "text": " ตรวจสอบนัด"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "type": "separator"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "image",
                                                        "url": "https://i.ibb.co/rGncDkj/rich-menu-4.png",
                                                        "aspectRatio": "2:3",
                                                        "action": {
                                                            "type": "message",
                                                            "label": "action",
                                                            "text": "สอบถามราคา"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "image",
                                                        "url": "https://i.ibb.co/2KrF1cJ/rich-menu-5.png",
                                                        "aspectRatio": "2:3",
                                                        "action": {
                                                            "type": "message",
                                                            "label": "action",
                                                            "text": "แผนที่"
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "contents": [
                                                    {
                                                        "type": "image",
                                                        "url": "https://i.ibb.co/mGR0RL6/rich-menu-6.png",
                                                        "aspectRatio": "2:3",
                                                        "action": {
                                                            "type": "message",
                                                            "label": "action",
                                                            "text": "ติดต่อพนักงาน"
                                                        }
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ],
                                "cornerRadius": "none"
                            }
                        }
                }
            ]
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

def noAnswer(Reply_token, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token)  ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken": Reply_token,
        "messages": [

            {
                "type": "flex",
                "altText": "ติดต่อสอบถามแอดมินได้ค่ะ",
                "contents":
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

            }

        ]
    }

    data = json.dumps(data)  ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200


def location(Reply_token, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "location",
                  "title": "คลินิกยิ้มสวย",
                  "address": "แขวง ลำปลาทิว เขตลาดกระบัง กรุงเทพมหานคร 10520",
                  "latitude": 13.729358702442287,
                  "longitude": 100.77553721017871
            }]
        }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200


def contractAdmin(Reply_token, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token)  ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    data = {
        "replyToken": Reply_token,
        "messages": [
            {
                "type": "flex",
                "altText": "เบอร์โทรและไลน์ติดต่อพนักงานค่ะ",
                "contents":
                    {
                        "type": "bubble",
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
                                    "text": "เบอร์โทรติดต่อ 08x-xxx-xxxx หรือ",
                                    "size": "md",
                                    "weight": "regular",
                                    "color": "#232323",
                                    "margin": "none"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": "สามารถติดต่อสอบถามไลน์แอดมินได้ค่ะ",
                                    "color": "#232323",
                                    "size": "md",
                                    "weight": "regular"
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
                                        "label": "ติดต่อไลน์แอดมิน",
                                        "uri": "https://lin.ee/4AhDoDQ"
                                    }
                                }
                            ]
                        }
                    }

            }


        ]
    }

    data = json.dumps(data)  ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200




# #flex msg จองนัด
# {
#   "type": "bubble",
#   "body": {
#     "type": "box",
#     "layout": "vertical",
#     "spacing": "md",
#     "action": {
#       "type": "uri",
#       "uri": "https://linecorp.com"
#     },
#     "contents": [
#       {
#         "type": "text",
#         "text": "คุณลูกค้าสามารถจองนัดทำฟันได้ค่ะ",
#         "size": "md",
#         "weight": "bold",
#         "color": "#232323",
#         "align": "center"
#       }
#     ]
#   },
#   "footer": {
#     "type": "box",
#     "layout": "vertical",
#     "contents": [
#       {
#         "type": "spacer",
#         "size": "xxl"
#       },
#       {
#         "type": "button",
#         "style": "primary",
#         "color": "#00ac00",
#         "action": {
#           "type": "uri",
#           "label": "คลิกเพื่อจองนัด",
#           "uri": "https://forms.gle/bk1x4c764HDPdFRM8"
#         }
#       }
#     ]
#   }
# }