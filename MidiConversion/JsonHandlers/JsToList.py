#import calls
import json
import numpy
from collections import OrderedDict

#List declarations 
num_files = 2
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


#Input initializaiton 
num_features = 5
dataX = []
dataY = []

'''
#Get all the notes
for i in range(0, num_notes-1, 1):
    seq_in = notes[i]
    seq_out = notes[i+1]
    dataX.append(seq_in)
    dataY.append(seq_out)
n_patterns = len(dataX)
'''