import random
import json
import threading
import time

import torch

from model import NeuralNet
from utilities import bag_of_words, tokenize
from emmaUtils import *
from sentiApi import *
from sentiAnalyzer import *

# setting device to CUDA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# loading intents
with open('Data/Emma_Dataset.json', 'r') as json_data:
    intents = json.load(json_data)


FILE = "Final_Processed_Data.pth"
data = torch.load(FILE)

# Creating instance of NeuralNetwork
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# The Base function for replies
def baseEMMA(inputTxt):
    while True:
        
        user_input = inputTxt.lower()
        if user_input == "quit":
            continue

        # Tokenizing the input
        sentence = tokenize(user_input)
        
        # Generating the Proper paramaeters for the model
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        
        # Getting the classification output from the model
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        

        # Getting the tag from the tags list
        tag = tags[predicted.item()]
        # Getting the probability of the output
        probs = torch.softmax(output, dim=1)
        # Checking Prediction against 
        prob = probs[0][predicted.item()]



        # Checking if the probability against the threshold
        if prob.item() > 0.97:
            for intent in intents['intents']:
                # Checking if the tag is in the intents
                if tag == intent["tag"]:
                    modelResponse = random.choice(intent['responses'])
                    return (f"{modelResponse}")
                    # Analysing the User's sentiment
                    sentiment_Analysis = sentimentAnalyser(user_input)
                    #  Inserting the instance into the memory module
                    instanceMemoryModule(user_input,modelResponse,sentiment_Analysis)




        else:
            # Analysing the User's sentiment
            sentiment_Analysis = sentimentAnalyser(user_input)   
            response = modelIn(user_input,sentiment_Analysis)
            
            # actual final response from the model
            return (f"{response}")