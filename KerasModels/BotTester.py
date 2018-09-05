#imports
import json
import numpy
import pandas
import keras
from collections import OrderedDict
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import MinMaxScaler

'''Load in Dicts/Scales/Model'''
notes_to_int = numpy.load('KeyNotesDict.npy').item()
Scaler = numpy.load('NoteScaler.npy').item()
int_to_notes = numpy.load('RKeyNotesDict.npy').item()
model = keras.models.load_model('MuseBotM1.hdf5')
TestData,TestX,json_data = [],[],[]

'''Load in Test Data'''

#Json to list Management
for i in range(95,100):

    #parse and store JsonData
	json_data.append(open("JMids/Midi" + str(i+1) + ".json").read())
	entire_parsed_json = json.loads(json_data[i-95], object_pairs_hook=OrderedDict)
	
    #Load in the tracks for the song
	tracks = entire_parsed_json["tracks"] # Extracts list of tracks	
	
	#for test Data
	for track in tracks:
		TestData.append(track["notes"]) # Extracts list of notes variables

# replaces all string notes with integer notes	
for j in range(0,len(TestData)):
	for i in range(0,len(TestData[j])):
		TestData[j][i]["name"] = notes_to_int[TestData[j][i]["name"]]
	
for j in range(0,len(TestData)):
	for i in range(0,len(TestData[j])):
		TestX.append(list(TestData[j][i].values()))		

		

'''Pass through model test'''
# pick a random seed
start = numpy.random.randint(0, len(TestX)-100)
pattern = Scaler.transform(TestX[start:start+5])
output,convPrediction = [],[]

# generate notes
for i in range(50):
	prediction = model.predict(pattern, verbose = 0)
	convPrediction = (Scaler.inverse_transform(numpy.reshape(prediction.tolist(),(1,-1))))
	pattern = numpy.concatenate((pattern,convPrediction))
	pattern = pattern[1:len(pattern)]
	output.append(convPrediction[0].tolist())	
	
	
'''Format Data into .json'''
out = open('template.json','w')
out.write("{\"header\":{\"PPQ\":384,\"bpm\":117.000117000117,\"name\":\"\"},\"startTime\":0,\"duration\":128.17294874999942,\"tracks\":[{\"startTime\":0,\"duration\":128.17294874999942,\"length\":679,")
out.write("\"notes\":[")
for r in range(len(output)):
    output[r][0] = int_to_notes[int(output[r][0])]
    output[r][1] = int(output[r][1]) + 12
    out.write('{')
    for q in range(5):
        if(q == 0):
            out.write("\"name\":\"")
        if(q == 1):
            out.write("\"midi\":")
        if(q == 2):
            out.write("\"time\":")
        if(q == 3):
            out.write("\"velocity\":")
        if(q == 4):
            out.write("\"duration\":")
        out.write(str(output[r][q]))
        if(q == 0):
            out.write("\"")
        if(q != 4):
            out.write(',')
    if(r != len(output)-1):
        out.write('},')
    else:
        out.write('}')
out.write("],\"controlChanges\":{\"64\":[]},\"id\":0,\"name\":\"\",\"channelNumber\":0,\"isPercussion\":false}]}")
out.close()

print("\nDone.")
# Input: {"name":"E4","midi":64,"time":9.309090909090909,"velocity":0.5748031496062992,"duration":0.5250000000000004}
