#import calls
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

#Variable declarations 
num_files = 2
start_test = 95
json_data,songs,notes,TestData,TestX = [],[],[],[],[]
Scaler = MinMaxScaler(feature_range=(0,1))


'''Data Management '''


#Json to list Management
for i in range(0,num_files):

    #parse and store JsonData
	json_data.append(open("JMids/Midi" + str(i+1) + ".json").read())
	entire_parsed_json = json.loads(json_data[i], object_pairs_hook=OrderedDict)
	
    #Load in the tracks for the song
	tracks = entire_parsed_json["tracks"] # Extracts list of tracks

	#Store the notes in songs/notes
	for track in tracks:
		if track["notes"] != [] and i < start_test:
			songs.append(track["notes"]) # Extracts list of notes variables
			'''TODO: if track has left and right, put and sort them together'''
		#for test Data
		elif track["notes"] != [] and i >= start_test:
			TestData.append(track["notes"]) # Extracts list of notes variables

# Isolate notes into own lists
raw_notes,this_note,raw_songs,all_notes = [],[],[],[]
for j in range(0,len(songs)):
	raw_notes.clear()
	
	for i in range(0,len(songs[j])):
		this_note = songs[j][i]
		raw_notes.append(this_note["name"])	
		all_notes.append(this_note["name"])		
	raw_songs.append(list(raw_notes))
	
#convert to ints
note_names = sorted(list(set(all_notes)))
notes_to_int = dict((c,i) for i, c in enumerate(note_names))

#Save Dict for future use in Testing 
numpy.save('KeyNotesDict.npy', notes_to_int) 


'''
To Load Back a numpy dict
read_dictionary = np.load('my_file.npy').item()
print(read_dictionary['hello']) # displays "world"
.csv Method
numpy.savetxt("song" + str(j) + ".csv", songs[j], delimiter = ",") TO convert to .csv
'''


# replaces all string notes with integer notes
for j in range(0,len(songs)):
	for i in range(0,len(songs[j])):
		songs[j][i]["name"] = notes_to_int[songs[j][i]["name"]]
		
for j in range(0,len(TestData)):
	for i in range(0,len(TestData[j])):
		TestData[j][i]["name"] = notes_to_int[TestData[j][i]["name"]]
	

# remove labels, list of dict -> list of list
for j in range(0,len(songs)):
	for i in range(0,len(songs[j])):
		songs[j][i] = list(songs[j][i].values())
		notes.append(songs[j][i])
		
	#convert each song to numpy
	songs[j] = array(songs[j])
	
for j in range(0,len(TestData)):
	for i in range(0,len(TestData[j])):
		TestX.append(list(TestData[j][i].values()))		
		

		
'''	MODEL CODE '''



#Model Initialization 
model = Sequential()
model.add(Dense(5, input_dim=5, kernel_initializer='normal',activation='relu')) # X.shape[1],X.shape[2]
model.add(Dropout(0.2))
model.add(Dense(100, kernel_initializer='normal', activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(1,input_dim = 5, kernel_initializer='normal')) #only the output has to match input dim 
model.compile(loss='mean_squared_error', optimizer='adam') #Makes the model, measures accuracy(loss), Optimizer

#For saving as we go purposes
#filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
#checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
#callbacks_list=[checkpoint]

#Fit the transform scalar to the array of notes
Scaler.fit_transform(notes)

#for loop going through all Song data
for j in range(0,len(songs)):
	X = songs[j]
	ScaledX = Scaler.transform(X)
	
	for i in range(6,len(songs[j])):
		model.fit(ScaledX[i-6:i-1], ScaledX[i], epochs=60, batch_size=128)
	
	
#Save model for later
model.save('MuseBotM1.hdf5')

'''Model Test'''
'''
# pick a random seed
start = numpy.random.randint(0, len(TestX)-100)
pattern = Scaler.transform(TestX[start:start+50])
output,shenanigan = [],[]

# generate notes
for i in range(100):
	x =	pattern
	prediction = model.predict(x, verbose=0)
	print(prediction.tolist()[0])
	shenanigan = list(Scaler.inverse_transform(numpy.reshape(prediction.tolist()[0],(1,-1))))
	print(pattern.shape)
	print(pattern)
	print(shenanigan)
	pattern.append(numpy.array(shenanigan))
	pattern = pattern[1:len(pattern)]
	output.append(shenanigan)
	
	
'''
'''Save Outcome'''

'''
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
'''
