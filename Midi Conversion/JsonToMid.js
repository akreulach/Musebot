var MidiConvert = require("../MidiConvert")
var fs = require('fs'); 
let i = 0;
var lineReader = require('readline').createInterface({
  input: require('fs').createReadStream('Jsons.txt')
});

lineReader.on('line', function (line) {
  console.log('Line from file:', line);
});

//Loop through Filenames in line 
lineReader.on('line', function (line) {
	
	//new midi each loop
	//let midi = MidiConvert.create()
	
	//Read in each line 
	fs.readFile(line, "utf8", function(err, JSONF) {
		if (!err) {
			
		// Create JSON OBJ and Encode it
		let midi = MidiConvert.create()
		let pp = JSON.parse(JSONF);
		midi = MidiConvert.fromJSON(pp);
		let encoded =  midi.encode(pp);
		console.log(pp);
		i++;
		
		//Write midi to new file
		fs.writeFileSync("Midi" + i + ".midi" ,	encoded ,"binary", function(err){
			if(err) {
				return console.log(err);
			}
			else 
				console.log("saved!");
			})
		}
		//error Handling
		else 
			console.log("Can't find the file.");
			console.log(line);
		})
		
})
	
