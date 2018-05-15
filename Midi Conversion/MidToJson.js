//File stream
var fs = require('fs');
//Path
var path = require('path');
//Midiconvert
var MidiConvert = require("../MidiConvert")
// midi file
var midi;
var i = 0;

//Load in file
var stuff = fs.readFileSync('midis.txt').toString();
var array = stuff.split("\n");  

var lineReader = require('readline').createInterface({
  input: require('fs').createReadStream('midis.txt')
});

lineReader.on('line', function (line) {
  console.log('Line from file:', line);
});

//Loop through Filenames in array 
lineReader.on('line', function (line) {
		
		//Append check
		console.log(line);
		
		//Read In file with given txt name
		fs.readFile(line, "binary", function(err, midiBlob) {
		if (!err) {
			
			//Convert the midi to temp midi file then JSON
			midi = MidiConvert.parse(midiBlob)
			var content = JSON.stringify(midi);
			i++;
			
			//Write Json file to a .json with the midi name 
			console.log(i);
			fs.writeFileSync("Midi" + i + ".json" , content, function(err){
				if(err) {
					return console.log(err);
				}
				else 
					console.log("saved!");
			})
		}
		else 
			console.log("Can't find the file.");
			console.log(line);
		})
})



