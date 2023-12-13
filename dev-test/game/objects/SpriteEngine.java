package game.objects;

public class SpriteEngine {
    
    private int frames_per_second;
    private Long cycle_start_time;
    private double cycle_progress;

    public SpriteEngine(int fps) {
        frames_per_second = fps;
        cycle_start_time = System.currentTimeMillis();
    }

    public int get_fps() {
        return frames_per_second;
    }

    public double get_cycle_progress() {
        return cycle_progress;
    }

    protected void reset() {
        cycle_progress = 0;
    }

    // TODO: Timer

}
