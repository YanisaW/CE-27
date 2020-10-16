from flask import Flask, request, abort #abort ใช้รายงาน http
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello',200

@app.route('/webhook',methods = ['POST','GET'])
def webhook():
    if request.method == 'POST': #ได้รับข้อมูลจาก Line
        print(request.json)
        return 200 #success
    elif request.method ==- 'GET': # GET การดูหน้าเว็บ
        return 'This is method GET',200