import requests
from sentiAnalyzer import *

def robertaSenti(payloadx):
    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {"Authorization": f"Bearer {HUG_BEARER_ID}"}


    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    return query(payloadx)        
    


def distillSenti(payloady):
    API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
    headers = {"Authorization": f"Bearer {HUG_BEARER_ID}"}


    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    return query(payloady)
    

def sentimentAnalyser(payload):
    try:
        bertSenti = robertaSenti(payload)
        distillSentix = distillSenti(payload)
        emotion_class = sentimentGetter(bertSenti,distillSentix)
        return emotion_class
    except:
        return []


