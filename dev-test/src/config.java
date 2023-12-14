package src;

public class config {
    
    public enum player_status {
        IDLE,
        MOVING,
        IN_AIR,
        PUNCHING,
        KICKING,
        DUCKING,
        MOVING_SLOW,
        DEFENDING,
        MOVE1,
        MOVE2,
        MOVE3,
        ULTIMATE,
        APPEAR
    }

    public static final int window_height = 640;
    public static final int window_width = 1024;

    public static final int field_height = 640;
    public static final int field_width = 1024;

    public static final double ground_level = 175;

    public player_status player_status;

    public config() {
    }
}
