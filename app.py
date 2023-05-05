from flask import Flask,request
from flask_restful import Api,Resource
from baseEMMA import *
import json

app = Flask(__name__)

@app.route('/sayhi', methods=['GET'])
def get_text2():
    return "Hello "

@app.route('/text', methods=['POST'])
def get_text():
    text = request.json
    input_txt = text["message"]
    user_name = text["sender"]
    reply = baseEMMA(input_txt,user_name)
    response = {'sender': 'EMMA', 'message': reply}
    return response

