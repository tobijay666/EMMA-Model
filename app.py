from flask import Flask,request
from flask_restful import Api,Resource
from baseEMMA import *
from Report_gen import *
from send_mail import *
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

@app.route('/report', methods=['POST'])
def get_report():
    creds = request.json
    user_name = creds["username"]
    user_email = creds["email"]
    report = Report(userName=user_name)
    report.gen_Report()
    generate_report_pdf(report)
    send_email_with_pdf(user_name,user_email)
    return "Report sent to your email"