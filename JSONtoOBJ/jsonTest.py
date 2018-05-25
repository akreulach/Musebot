import json
import numpy
import pandas
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

num_files = 5
json_data = []
notes = []

# load JSON songs and extract all notes
for i in range(0,num_files):
    json_data.append(open("examples/Midi" + str(i+1) + ".json").read())

    entire_parsed_json = json.loads(json_data[i])
    tracks = entire_parsed_json["tracks"] # Extracts list of tracks

    for track in tracks:
        notes = notes + track["notes"] # Extracts list of notes variables

num_notes = len(notes)

# Converts names to integers
raw_notes = []
this_note = []
for i in range(0,num_notes):
    this_note = notes[i]
    raw_notes.append(this_note["name"])

note_names = sorted(list(set(raw_notes)))
notes_to_int = dict((c,i) for i, c in enumerate(note_names))
n_names = len(raw_notes)
n_vocab = len(note_names)

# replaces all string notes with integer notes
for i in range(0,num_notes):
    notes[i]["name"] = notes_to_int[notes[i]["name"]]

# remove labels, list of dict -> list of list
for i in range(0,num_notes):
    notes[i] = list(notes[i].values())

seq_length = 50
num_features = 5
dataX = []
dataY = []
for i in range(0, num_notes - seq_length, 1):
    seq_in = notes[i:i + seq_length]
    seq_out = notes[i+ seq_length]
    dataX.append(seq_in)
    dataY.append(seq_out)
n_patterns = len(dataX)

X = numpy.reshape(dataX, (n_patterns, seq_length * num_features))

Y = numpy.reshape(dataY, (n_patterns, num_features))

#Model Creation
model = Sequential()
model.add(Dense(5, input_dim=(seq_length * num_features), kernel_initializer='normal')) # X.shape[1],X.shape[2]
model.add(Dropout(0.2))
model.add(Dense(10, kernel_initializer='normal', activation='relu'))
model.add(Dense(5, kernel_initializer='normal'))
model.compile(loss='mean_squared_error', optimizer='adam')

filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list=[checkpoint]

model.fit(X, Y, epochs=20, batch_size=128, callbacks=callbacks_list)
