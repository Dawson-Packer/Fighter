package src.objects;

import java.lang.Math;

import src.config;
import src.config.player_status;

public class Player extends AnimatedSprite implements PhysicsObjectInterface {
    
    public double x_pos;
    public double y_pos;

    private double x_velocity;
    private double y_velocity;
    private boolean direction;
    private config.player_status status;
    private config.player_status last_status;
    private int move_cooldown = 0;
    private int hitbox_height;
    private int hitbox_width;
    private String character_name;

    private int animation_tick;

    public Player(
        int object_id,
        int client_id,
        double x_pos,
        double y_pos,
        boolean facing_right,
        double x_velocity,
        double y_velocity,
        int hitbox_height,
        int hitbox_width,
        int sprite_height,
        int sprite_width,
        String character,
        double rotation
    ) {
        super(
            object_id,
            (int)Math.round(x_pos),
            config.field_height - (int)Math.round(y_pos) + sprite_height,
            true,
            sprite_height,
            sprite_width,
            256,
            256,
            "/assets/textures/player/stickman/",
            player_status.IDLE.ordinal()
        );
        this.x_pos = x_pos;
        this.y_pos = y_pos;
        this.x_velocity = x_velocity;
        this.y_velocity = y_velocity;
        this.direction = facing_right;
        this.hitbox_height = hitbox_height;
        this.hitbox_width = hitbox_width;
        this.character_name = character;
        this.move_cooldown = 0;
        status = player_status.IDLE;

        reset_animation_tick();
        
    }

    public void tick() {

        // prepare_animation();

        update_sprite(x_pos, y_pos + sprite_height);
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

    // private void prepare_animation() {
    //     config.player_status current_status = status;
    //     if (last_status != current_status) reset_animation_tick();
    //     if (status == player_status.IDLE) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 4, 7, direction);
    //     }
    //     else if (status == player_status.MOVING) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 2, 7, direction);
    //         status = player_status.IDLE;
    //     }
    //     else if (status == player_status.IN_AIR) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 4, direction);
    //         status = player_status.IDLE;
    //     }
    //     else if (status == player_status.PUNCHING) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 3, direction);
    //         if (animation_tick == 0) status = player_status.IDLE;
    //     }
    //     else if (status == player_status.KICKING) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 3, direction);
    //         if (animation_tick == 0) status = player_status.IDLE;
    //     }
    //     else if (status == player_status.DUCKING) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 1, direction);
    //         status = player_status.IDLE;
    //     }
    //     else if (status == player_status.MOVING_SLOW) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 4, 15, direction);
    //         status = player_status.IDLE;
    //     }
    //     else if (status == player_status.DEFENDING) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 1, direction);
    //     }
    //     else if (status == player_status.MOVE1) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 1, direction);
    //         if (animation_tick == 0) status = player_status.IDLE;
    //     }
    //     else if (status == player_status.MOVE2) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 1, direction);
    //         if (animation_tick == 0) status = player_status.IDLE;
    //     }
    //     else if (status == player_status.MOVE3) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 1, direction);
    //         if (animation_tick == 0) status = player_status.IDLE;
    //     }
    //     else if (status == player_status.ULTIMATE) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 1, direction);
    //         if (animation_tick == 0) status = player_status.IDLE;
    //     }
    //     else if (status == player_status.APPEAR) {
    //         animate("/assets/textures/player/" + character_name + "/" + status.ordinal() + "/", 1, 1, direction);
    //         if (animation_tick == 0) status = player_status.IDLE;
    //     }

    //     last_status = current_status;
    // }

    public void reset_animation_tick() {
        animation_tick = 0;
    }
}
