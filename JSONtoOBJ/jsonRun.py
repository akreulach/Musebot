import json
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

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
int_to_notes = dict((c,i) for c, i in enumerate(note_names))
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

model = Sequential()
model.add(Dense(5, input_dim=(seq_length * num_features), kernel_initializer='normal')) # X.shape[1],X.shape[2]
model.add(Dropout(0.2))
model.add(Dense(10, kernel_initializer='normal', activation='relu'))
model.add(Dense(5, kernel_initializer='normal'))

# load the network weights
filename = "NickM1.hdf5"
model.load_weights(filename)
model.compile(loss='mean_squared_error', optimizer='adam')

# pick a random seed
start = numpy.random.randint(0, len(dataX)-100)
pattern = dataX[start]
output = []
shenanigan = []

# generate notes
for i in range(100):
    x = numpy.reshape(pattern, (1, seq_length * num_features))
    prediction = model.predict(x, verbose=0)
    shenanigan = prediction.tolist()[0]
    pattern.append(shenanigan)
    pattern = pattern[1:len(pattern)]
    output.append(shenanigan)

g = open('NM1.txt','w')
g.write("\"notes\":[")
for r in range(len(output)):
    output[r][0] = int_to_notes[int(output[r][0])]
    output[r][1] = int(output[r][1]) + 12
    g.write('{')
    for q in range(5):
        if(q == 0):
            g.write("\"name\":\"")
        if(q == 1):
            g.write("\"midi\":")
        if(q == 2):
            g.write("\"time\":")
        if(q == 3):
            g.write("\"velocity\":")
        if(q == 4):
            g.write("\"duration\":")
        g.write(str(output[r][q]))
        if(q == 0):
            g.write("\"")
        if(q != 4):
            g.write(',')
    if(r != len(output)-1):
        g.write('},')
    else:
        g.write('}')
g.write("],")
g.close()
print("\nDone.")
# Input: {"name":"E4","midi":64,"time":9.309090909090909,"velocity":0.5748031496062992,"duration":0.5250000000000004}
