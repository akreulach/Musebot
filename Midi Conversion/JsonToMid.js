var MidiConvert = require("../MidiConvert")
var fs = require('fs'); 
var lineReader = require('readline').createInterface({
  input: require('fs').createReadStream('Jsons.txt')
});

lineReader.on('line', function (line) {
  console.log('Line from file:', line);
});

//Loop through Filenames in line 
lineReader.on('line', function (line) {
	
	//new midi each loop
	let midi = new Midi()
	
	//Read in each line 
	fs.readFile(line, "JSON", function(err, JSONF) {
		if (!err) {
			
		// Create JSON OBJ and Encode it 
		var obj = JSON.parse(fs.readFileSync(JSONF, 'utf8'));
		let encoded = midi.encode.apply(obj);
		midi.decode(encoded)
		
		//Write midi to new file
		fs.writeFileSync("Midi" + i + ".midi" , midi, function(err){
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
	
