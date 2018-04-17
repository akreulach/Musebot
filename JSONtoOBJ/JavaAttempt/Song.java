import java.util.ArrayList;

public class Song {
	ArrayList<Note> notes;
	
	Song(Json ob){
		notes = new ArrayList<Note>();
		Json tracks = ob.get("tracks");
		
		for(int t = 0; t < tracks.size(); t++){
			Json track = tracks.get(t);
			Json tmpList = null;
			try {
				tmpList = track.get("notes");
			} catch(Exception e){
				e.printStackTrace();
			}
			if(tmpList != null)
			for(int i = 0; i < tmpList.size(); i++){
				Json tmp = tmpList.get(i);

				String name = tmp.getString("name");
				int midi = (int)tmp.getLong("midi");
				double time = tmp.getDouble("time");
				double velocity = tmp.getDouble("velocity");
				double duration = tmp.getDouble("duration");
				
				notes.add(new Note(name,midi,time,velocity,duration));
			}
		}
	}
	Json marshal() {
		Json ob = Json.newObject();
		Json tmpList = Json.newList();
		ob.add("notes", tmpList);
		for(int i = 0; i < notes.size(); i++)
			tmpList.add(notes.get(i).marshal());
		return ob;
	}

	public void print(){
		for(int i = 0; i < notes.size();i++)
			notes.get(i).print();
	}
}