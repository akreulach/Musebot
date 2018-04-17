import java.io.*;

public class Format {
	public static void main(String args[]){
		int count = 1;
		String inName = "MIDI";
		inName += count;
		inName+=".txt";
		String outName= inName + " Table.txt";
		try{
			workFile(inName, outName);
		}catch(IOException e){}
	}
	
	private static void workFile(String file, String outFile, int lineLen) throws IOException {
	    	BufferedReader reader = new BufferedReader(new FileReader (file));
	    	String         line = null;
	    	StringBuilder  stringBuilder = new StringBuilder();
	    	String         ls = System.getProperty("line.separator");
	    	PrintWriter out = new PrintWriter(outFile);
		String temp = "";
	    
	    	try {
	        	while((line = reader.readLine()) != null) {
				if(line.contains("On " || "Off ")
					temp = line.substring(
		        		stringBuilder.append(line.substring(0,line.substring(0,lineLen).lastIndexOf(" ")));
            				out.print(stringBuilder.toString());
					out.print(ls);
            				line = line.substring(line.substring(0,lineLen).lastIndexOf(" ")+1);
					lineLength = line.length();
				}
            			stringBuilder = new StringBuilder();
			}
	    	} finally {
	        	reader.close();
	        	out.close();
	    	}
	}
}