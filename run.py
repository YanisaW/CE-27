import torch
import json
from pythainlp import sent_tokenize, word_tokenize
import warnings
import pythainlp
from pythainlp.corpus import wordnet
import datetime
from pythainlp.util import thai_strftime
#
warnings.filterwarnings('ignore')


sentence_1 = "อยากทำฟัน นัดได้วันไหนบ้างคะ"
print("sent_tokenize:", sent_tokenize(sentence_1))
print("attacut:", word_tokenize(sentence_1, engine="attacut"))

#with open('intents.json', 'r') as json_data:
 #   intents = json.load(json_data)

#FILE = "data.pth"
#data = torch.load(FILE)