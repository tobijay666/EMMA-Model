import random
import time
import shutil
import os
import datetime
import json

text_list = [
    "Ahh...",
    "mm...",
    "hmm...",
    "well...",
    "mmm..."
]

def jsonCopyFile():
    # copy the current_convo.json to the archive folder
    # get the current date and time
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

    filename = "current_convo.json"
    # Create a new filename with the date and extension
    new_filename = f"{filename}_{date_string}.json"

    # Open the original file and read its contents
    with open(filename, 'r') as f:
        data = json.load(f)

    # Create a new file with the new filename and write the data to it
    with open(new_filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Clear the contents of the dictionary
    data.clear()

    # Open the file again and write the empty dictionary to it
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def delayed_text_function():
    # time.sleep(2)
    random_index = random.randint(0, len(text_list)-1)
    random_text = text_list[random_index]
    return random_text

def responseCreator(req):
    return req.split(':')

def userInputCheck(user_input):
    # check for  '.'|'?'|'!' at the very end of the message.
    # if non of the above charcters are found at the end of the input add '.' at the end.
    character_list = [ '.','?','!']
    input_list = user_input.split()

    if input_list[-1].endswith(tuple(character_list)):
        return user_input
    else:
        input_list.append('.')
        mod_userInput = ' '.join(str(word) for word in input_list )
        return mod_userInput

    # Time Complexity : O(n)
    # Space Complexity : O(1)

# def instanceMemoryModule(user_input,generated_reply,sentiment,userName):
    # with open('current_convo.json','r+') as file:
    #       # First we load existing data into a dict.
    #     if len(sentiment) == 0 :
    #         try:
    #             file_data = json.load(file)
    #             file_data[userName].append(user_input)
    #             file_data["EMMA"].append(generated_reply)
    #             file_data["Emotion"].append(0)
    #         except:
    #             file_data = {
    #             userName : [0,0,0,user_input],
    #             "EMMA" : [0,0,0,generated_reply],
    #             "Emotion" : [0,0,0,0]
    #             }
    #     else:
    #         try:
    #             file_data = json.load(file)
    #             file_data[userName].append(user_input)
    #             file_data["EMMA"].append(generated_reply)
    #             file_data["Emotion"].append(sentiment[1])
    #         except:
    #             file_data = {
    #             userName : [0,0,0,user_input],
    #             "EMMA" : [0,0,0,generated_reply],
    #             "Emotion" : [0,0,0,sentiment[1]]
    #             }

    #     # Sets file's current position at offset.
    #     file.seek(0)
    #     # convert back to json.
    #     json.dump(file_data, file, indent = 4)

    ##new one
    # with open('current_convo.json', 'r+') as file:
    #     try:
    #         file_data = json.load(file)
    #     except:
    #         file_data = {
    #             userName : [0,0,0,user_input],
    #             "EMMA" : [0,0,0,generated_reply],
    #             "Emotion" : [0,0,0,0]
    #         }
            
    #     if len(sentiment) == 0:
    #         file_data[userName].append(user_input)
    #         file_data["EMMA"].append(generated_reply)
    #         file_data["Emotion"].append(0)
    #     else:
    #         file_data[userName].append(user_input)
    #         file_data["EMMA"].append(generated_reply)
    #         file_data["Emotion"].append(sentiment[1])
            
    #     file.seek(0)
    #     json.dump(file_data, file, indent=4)

def instanceMemoryModule(user_input,generated_reply,sentiment,userName):
    filename = f"{userName}_convo.json"
        try:
            with open(filename, 'r+') as file:
                file_data = json.load(file)
        except:
            file_data = {
                userName : [0,0,0,user_input],
                "EMMA" : [0,0,0,generated_reply],
                "Emotion" : [0,0,0,0]
            }
            
        if len(sentiment) == 0:
            file_data[userName].append(user_input)
            file_data["EMMA"].append(generated_reply)
            file_data["Emotion"].append(0)
        else:
            file_data[userName].append(user_input)
            file_data["EMMA"].append(generated_reply)
            file_data["Emotion"].append(sentiment[1])
            
        file.seek(0)
        json.dump(file_data, file, indent=4)

def previousDialogues():
    # load the current_convo.json 
    # list the conversations
    # get the last 4 dialogs both user and emma
    import json
    with open('current_convo.json','r+') as file:
          # First we load existing data into a dict.
        try:
            file_data = json.load(file)
            dialog_length = len(file_data[userName])
            
            # getting the dialogs into lists
            userInputs = file_data[userName]
            emmaOutputs = file_data["EMMA"]
            # reversing the dialogs 
            reversedUser = userInputs[::-1]
            reversedEMMA = emmaOutputs[::-1]
            # print(reversedUser,reversedEMMA)

            # getting the last 4 dialogs
            latestUser = reversedUser[:4]
            latestEMMA = reversedEMMA[:4]

            # fixing dialog direction 
            latestUser = latestUser[::-1]
            latestEMMA = latestEMMA[::-1]
            
            dialogList = zip(latestUser,latestEMMA)
            pairedDialogList = [item for pair in dialogList for item in pair]



            return pairedDialogList


        except:
            return 0
        

def modelIn( user_input,sentiment,userName):
    user_input = userInputCheck(user_input)
    
    # Base Prompt Optimization 1 - adding user sentiment to the prompt
    if len(sentiment) != 0:
        prompt = f"Your name is Emma.You are having a conversation with your friend {userName}. He is {sentiment[0]} and feeling {sentiment[1]}.You are empathetic,kind and You should make {userName} feel happy :"
    
    else:
        prompt = f"Your name is Emma..You are having a conversation with {userName}.You are empathetic,kind and You should make {userName} feel happy:"

    
    
    # initialize the model
    import os
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"

    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, set_seed, AutoModel

    import torch
    torch.set_default_tensor_type(torch.FloatTensor)

    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-560m")


    model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-560m")

    set_seed(424242)

    #     # append user input to the prompt
    #     # edited_prompt = prompt + user_input
    # 
    #     # 1. initial/customized prompt
    #     # 2. user_input
    #     # 3. previous conversation

    previous_Dialogues = previousDialogues()

    # Base Prompt Optimization 2 - Including Previous Dialogues
    if (previous_Dialogues != 0):
        Feeding_Prompt = f"{prompt} \n {userName}: {previous_Dialogues[0]}  \n You:{previous_Dialogues[1]}\n {userName}: {previous_Dialogues[2]}  \n You:{previous_Dialogues[3]}\n {userName}: {previous_Dialogues[4]}  \n You:{previous_Dialogues[5]}\n {userName}: {previous_Dialogues[6]}  \n You:{previous_Dialogues[7]} \n {userName}: {user_input} \n You:"
    else:
        Feeding_Prompt = f"{prompt} \n {userName}: {user_input} \n You:"

    # rest of the bloom model

    # tokenizeing the input prompt
    input_ids = tokenizer(Feeding_Prompt, return_tensors='pt').to('cpu')

    # generating a reply in numerial tensor format
    sample = model.generate(**input_ids, max_length=150, top_k=1, temperature=0.9, repetition_penalty = 2.0)

    # printing the generated and decoded reply
    # print(tokenizer.decode(sample[0]))

    # decoding the generated reply
    fullResponse = (tokenizer.decode(sample[0], truncate_before_pattern = [r"\n\n^#","^\n"]))
    # print(fullResponse)

    # dividing the generated data into lines
    dividedResponse = fullResponse.split("\n")

    ## divided response into a seperate function
    print(dividedResponse, '\n',sentiment)

    reply = responseCreator( dividedResponse[10])

    instanceMemoryModule(user_input,reply[1],sentiment,userName)

    # reply contains a list consists of generative texts
    return reply[1]