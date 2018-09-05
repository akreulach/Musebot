#imports
import json
import numpy
import pandas
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
notes_to_int = np.load('KeyNotesDict.npy').item()
Scaler = np.load('NoteScaler.npy').item()


'''Load in Test Data'''



'''Pass through model test'''


# pick a random seed
start = numpy.random.randint(0, len(TestX)-100)
pattern = Scaler.transform(TestX[start:start+5])
output,convPrediction = [],[]

# generate notes
for i in range(5):
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
