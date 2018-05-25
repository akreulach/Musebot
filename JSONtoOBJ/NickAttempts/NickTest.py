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

#List declarations 
num_files = 5
json_data,songs = [],[]

#Json to list Management
for i in range(0,num_files):

    #parse and store JsonData
	json_data.append(open("examples/Midi" + str(i+1) + ".json").read())
	entire_parsed_json = json.loads(json_data[i], object_pairs_hook=OrderedDict)
	
    #Load in the tracks for the song
	tracks = entire_parsed_json["tracks"] # Extracts list of tracks

	#Store the notes in songs/notes
	for track in tracks:
		if track["notes"] != []:
			songs.append(track["notes"]) # Extracts list of notes variables

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

# replaces all string notes with integer notes
for j in range(0,len(songs)):
	for i in range(0,len(songs[j])):
		songs[j][i]["name"] = notes_to_int[songs[j][i]["name"]]
	

# remove labels, list of dict -> list of list
for j in range(0,len(songs)):
	for i in range(0,len(songs[j])):
		songs[j][i] = list(songs[j][i].values())
	#convert each song to numpy
	songs[j] = array(songs[j])
	#numpy.savetxt("song" + str(j) + ".csv", songs[j], delimiter = ",") TO convert to .csv

#Model Initialization 
model = Sequential()
model.add(Dense(5, input_dim=5, kernel_initializer='normal')) # X.shape[1],X.shape[2]
model.add(Dropout(0.2))
model.add(Dense(10, kernel_initializer='normal', activation='relu'))
model.add(Dense(5, kernel_initializer='normal'))
model.compile(loss='mean_squared_error', optimizer='adam')

#For improment purposes
filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list=[checkpoint]

#for loop going through all X and Y data
for j in range(0,len(songs)):
	X = songs[j]
	Y = numpy.roll(songs[j],-1,axis=0) 
	model.fit(X, Y, epochs=60, batch_size=128, callbacks=callbacks_list)
	
#Save model for later
model.save('NickM1.hdf5')

