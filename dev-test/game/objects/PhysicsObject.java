package game.objects;

import game.config;
import game.config.player_status;

public class PhysicsObject extends Object {
    
    private double x_velocity;
    private double y_velocity;
    private int move_cooldown = 0;

    /**
     * @param id The ID of the Object
     * @param x_pos The x-position of the Object
     * @param y_pos The y-position of the Object
     * @param x_velocity The x-velocity of the PhysicsObject
     * @param y_velocity The y-velocity of the PhysicsObject
     */
    public PhysicsObject(
        int id,
        double x_pos,
        double y_pos,
        double x_velocity,
        double y_velocity
    ) {
        super(id, x_pos, y_pos);
        this.x_velocity = x_velocity;
        this.y_velocity = y_velocity;

    }

    public config.player_status process_physics(config.player_status status,
    int hitbox_height, int hitbox_width) {
        boolean status_change_available = true;
        if (status.equals(player_status.PUNCHING) || status.equals(player_status.KICKING)) {
            status_change_available = false;
        }
        if (move_cooldown == 0) {
            if (y_velocity != 0.0) {
                if (status_change_available) status = player_status.IN_AIR;
            y_pos += y_velocity;
            }
            if (y_pos < config.ground_level) {
                y_pos = config.ground_level;
                y_velocity = 0.0;
            }
            if (y_pos > config.ground_level) {
                y_velocity -= 9.8;
            }

            if (y_velocity == 0.0 && x_velocity != 0.0) {
                if (!status.equals(player_status.MOVING_SLOW) && status_change_available) {
                    status = player_status.MOVING;
                }
                x_pos += x_velocity;
            } else if (y_velocity == 0.0 && x_velocity == 0.0 &&
            !status.equals(player_status.DUCKING) && status_change_available) {
                status = player_status.IDLE;
            }
            x_velocity = 0.0;
        }
        
        if (x_pos - (hitbox_width / 2) < 0.0) x_pos = 0.0 + (hitbox_width / 2);
        else if (x_pos + (hitbox_width / 2) > 1000.0) x_pos = 1000.0 - (hitbox_width / 2);

        return status;
    }
}
