package game;

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

    public static double ground_level = 175;

    public player_status player_status;

    public config() {
    }
}
