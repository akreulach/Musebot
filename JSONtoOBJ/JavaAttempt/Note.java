public class Note{
	String name;
	int midi;
	double time, velocity, duration;
	public Note(String n, int mid, double t, double vel, double dur){
		name = n;
		midi = mid;
		time = t;
		velocity = vel;
		duration = dur;
	}

	Json marshal() {
		Json ob = Json.newObject();
		ob.add("name", name);
		ob.add("midi", midi);
		ob.add("time", time);
		ob.add("velocity", velocity);
		ob.add("duration", duration);
		return ob;
	}
	public void print(){
		System.out.println(name);
	}
}