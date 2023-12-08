package game.objects;

import java.lang.Math;

import game.config;
import game.config.player_status;

public class Player extends Sprite implements PhysicsObjectInterface, AnimatedSpriteInterface {
    
    public double x_pos;
    public double y_pos;

    private double x_velocity;
    private double y_velocity;
    private config.player_status status;
    private int move_cooldown = 0;
    private int hitbox_height;
    private int hitbox_width;

    private int animation_tick = 0;

    public Player(
        int object_id,
        int client_id,
        double x_pos,
        double y_pos,
        boolean direction,
        double x_velocity,
        double y_velocity,
        int hitbox_height,
        int hitbox_width,
        int sprite_height,
        int sprite_width,
        String character,
        double rotation
    ) {
        super(object_id,
        (int)Math.round(x_pos),
        (int)Math.round(y_pos),
        sprite_height,
        sprite_width,
        "./0.png"
        );
        this.x_pos = x_pos;
        this.y_pos = y_pos;
        this.x_velocity = x_velocity;
        this.y_velocity = y_velocity;
        this.hitbox_height = hitbox_height;
        this.hitbox_width = hitbox_width;
        status = player_status.APPEAR;
        
    }

    @Override
    public config.player_status process_physics() {
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

    @Override
    public void animate() {
        // TODO: Later
    }

    @Override
    public void reset_animation_tick() {
        animation_tick = 0;
    }
}
