public class JsonParser {
	private static Song[] songs;
	public static void main(String[] args){
		songs = new Song[5];
		for(int i = 1; i < 6; i++){
			Json ob = Json.load("Midi" + i + ".json");
			songs[i-1] = new Song(ob);
		}
	}
}