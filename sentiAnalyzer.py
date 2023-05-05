
# BASE ASSUMPTIONS:
# if 0 or 2 is >75% classify as is and get emotion
# if 1 is >50% check next
#       if the gap between 0&2 is <20 classify as neutral 
#       emotion check is not necessary 
# EMOTION ANALYSIS:
#   the state of emotion depends on the state, above...
#   if emotion is >90% classify as is
#   else go for the coupling with next max
#   if coupling is contradictory
#   other than   
#    0 -> {anger, sadness,fear}
#    2 -> {love,joy}
#   ignore the next max

#   if in case both state and emotion classification fails -> (values that are lower than 50% for state)
#   check immediate last classification and tally against state max
import math 


def emotion_classifier(state,list_of_emotions):
  phrase_emotion =""
  emotion_class =[]
  # extracting the state in the dictionary keys
  emotion_type_getter = list(state.keys())
  emotion_type = emotion_type_getter[0]


# temp for emotion contradictory analysis
  temp = 0
  temp_phrase_emotion = 0
# if positive cross validate with positive emotions
  if emotion_type == "positive":
    emotions_list = list_of_emotions[0]
    for counter,cur_emotion in enumerate(emotions_list):
      if (cur_emotion['label'] == 'joy' or cur_emotion['label'] == 'love'):
        if (cur_emotion["score"] >= 0.9):
          temp = cur_emotion["score"]
          temp_phrase_emotion = cur_emotion['label']
        elif(0.5 <= cur_emotion["score"]):
          temp = cur_emotion["score"]
          temp_phrase_emotion = cur_emotion['label']
    phrase_emotion = temp_phrase_emotion

  elif emotion_type == "negative":
    emotions_list = list_of_emotions[0]
    for counter,cur_emotion in enumerate(emotions_list):
      if (cur_emotion['label'] == 'anger' or cur_emotion['label'] == 'sadness'or cur_emotion['label'] == 'fear'):
        if (cur_emotion["score"] >= 0.9):
          temp = cur_emotion["score"]
          temp_phrase_emotion = cur_emotion['label']
        elif(0.5 <= cur_emotion["score"]):
          temp = cur_emotion["score"]
          temp_phrase_emotion = cur_emotion['label']
    phrase_emotion = temp_phrase_emotion
    # declare variables for phase emtions at the begining and an array 
    # to store state and phrase emotion which will be returned
  emotion_class = emotion_type,phrase_emotion


  return emotion_class     



# joy_emotion = 
# love_emotion = 
# anger_emotion = 
# sadness_emotion = 
# fear_emotion = 
# surprise_emotion = 

def sentimentGetter(resBert,resDistill):
  emotion_class = []
  # defining state variables
  negative_state = {"negative":resBert[0][0]['score']}
  neutral_state = {"neutral":resBert[0][1]['score']}
  positive_state = {"positive":resBert[0][2]['score']}

  # negative_state = {"negative" : 0.05}
  # neutral_state = {"neutral" : 0.05}
  # positive_state = {"positive" : 0.90}

  # state classification
  if (negative_state["negative"] >= 0.55 or positive_state["positive"]  >= 0.55 ):
    if(negative_state["negative"] > positive_state["positive"]):
      emotion_class = emotion_classifier(negative_state,resDistill)
    else:
      emotion_class = emotion_classifier(positive_state,resDistill)
      
      # continue to emotion classification


  elif (neutral_state["neutral"] >=0.50):
      # gap_of_negpos === gap of negative and positive states
    gap_of_negpos = negative_state["negative"] - positive_state["positive"]
    gap_of_negpos = math.sqrt(gap_of_negpos**2)
    if(gap_of_negpos > 0.2):
      if(negative_state["negative"] > positive_state["positive"]):
        emotion_class = emotion_classifier(negative_state,resDistill)
      else:
        emotion_class = emotion_classifier(positive_state,resDistill)

      # continue to emotion classification
      
  return emotion_class
      
