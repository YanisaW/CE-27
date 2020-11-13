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
        #answer = 'สวัสดีค่ะ'
        answer = question(message)
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
            "replyToken":Reply_token,
            "messages":[{
                "type":"text",
                "text":TextMessage
            }]
        }
    else:
        data = {
            "replyToken": Reply_token,
            "messages": [{
                "type": "image",
                "originalContentUrl": "https://lh3.googleusercontent.com/proxy/BuPNo1xpalsU3Dia9QZWHYBSeAciffsnQa4MaQ07qKlQnlg-0-P7AVWO5EHaoIHOl8vzTPnD9FT-yay6HIoxbmcTk0YDgg",
                "previewImageUrl": "https://lh3.googleusercontent.com/proxy/BuPNo1xpalsU3Dia9QZWHYBSeAciffsnQa4MaQ07qKlQnlg-0-P7AVWO5EHaoIHOl8vzTPnD9FT-yay6HIoxbmcTk0YDgg"
            }]
        }


    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200