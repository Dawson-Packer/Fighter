package src.objects;

import java.lang.Math;

import interfaces.Physics;
import interfaces.config.PlayerSettings;
import interfaces.config.FieldSettings;
import src.config.characters.CharacterConfig;
import src.sprites.AnimatedSprite;

public class Player extends AnimatedSprite implements Physics {
    
    public double x_pos;
    public double y_pos;

    private double x_velocity;
    private double y_velocity;
    private double speed;
    private boolean direction;
    private boolean last_direction;
    protected PlayerSettings.player_status status;
    protected PlayerSettings.player_status last_status;
    private int move_cooldown = 0;
    private int punch_cooldown = 0;
    private int punch_timer = 0;
    private int kick_cooldown = 0;
    private int kick_timer = 0;
    private int hitbox_height;
    private int hitbox_width;
    private String character_name;

    private boolean IS_PUNCHING = false;
    private boolean IS_KICKING = false;
    private boolean IS_DUCKING = false;

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
        CharacterConfig character,
        double rotation
    ) {
        super(
            object_id,
            (int)Math.round(x_pos),
            FieldSettings.field_height - (int)Math.round(y_pos) + sprite_height,
            true,
            sprite_height,
            sprite_width,
            256,
            256,
            "/assets/textures/player/stickman/",
            PlayerSettings.player_status.IDLE.ordinal(),
            character
        );
        this.x_pos = x_pos;
        this.y_pos = y_pos;
        speed = 12.0;
        this.x_velocity = x_velocity;
        this.y_velocity = y_velocity;
        this.direction = facing_right;
        this.last_direction = direction;
        this.hitbox_height = hitbox_height;
        this.hitbox_width = hitbox_width;
        this.character_name = character.name;
        this.move_cooldown = 0;
        status = PlayerSettings.player_status.IDLE;
        
    }

    public void tick() { }

    @Override
    public PlayerSettings.player_status process_physics() {
        boolean status_change_available = true;
        PlayerSettings.player_status new_status = status;
        if (status.equals(PlayerSettings.player_status.PUNCHING) ||
        status.equals(PlayerSettings.player_status.KICKING)) {
            status_change_available = false;
        }
        if (y_velocity != 0.0) {
            if (status_change_available) new_status = PlayerSettings.player_status.IN_AIR;
        y_pos += y_velocity;
        }
        if (y_pos < FieldSettings.ground_level) {
            y_pos = FieldSettings.ground_level;
            y_velocity = 0.0;
            new_status = PlayerSettings.player_status.IDLE;
        }
        if (y_pos > FieldSettings.ground_level) {
            y_velocity -= 6.5;
        }

        if (y_velocity == 0.0 && x_velocity != 0.0) {
            if (!status.equals(PlayerSettings.player_status.MOVING_SLOW) &&
            status_change_available) {
                new_status = PlayerSettings.player_status.MOVING;
            }
            x_pos += x_velocity;
        } else if (y_velocity == 0.0 && x_velocity == 0.0 &&
        !status.equals(PlayerSettings.player_status.DUCKING) && status_change_available) {
            new_status = PlayerSettings.player_status.IDLE;
        }
            x_velocity = 0.0;
        
        if (x_pos - (hitbox_width / 2) < 0.0) x_pos = 0.0 + (hitbox_width / 2);
        else if (x_pos + (hitbox_width / 2) > 1024.0) x_pos = 1024.0 - (hitbox_width / 2);

        return new_status;
    }

    public void update_status(PlayerSettings.player_status new_status) {
        if (last_direction != direction) {
            flip_texture(true, false);
            last_direction = direction;
        }
        if (!status.equals(new_status)) set_animation_value(new_status.ordinal());
        status = new_status;
    }

    protected void reset_status() { update_status(PlayerSettings.player_status.IDLE); }

    protected void ping() {

        if (last_direction != direction)
        flip_texture(true, false);

        if (punch_timer == 0 && IS_PUNCHING) {
            update_status(PlayerSettings.player_status.IDLE);
            IS_PUNCHING = false;
        }

        if (kick_timer == 0 && IS_KICKING) {
            update_status(PlayerSettings.player_status.IDLE);
            IS_KICKING = false;
        }


        last_direction = direction;
        if (punch_timer > 0) punch_timer -= 1;
        if (kick_timer > 0) kick_timer -= 1;
        if (punch_cooldown > 0) punch_cooldown -= 1;
        if (kick_cooldown > 0) kick_cooldown -= 1;
        if (move_cooldown > 0) move_cooldown -= 1;

        if (last_status != status) last_status = status;
    }

    public void jump() {
        if (y_pos == FieldSettings.ground_level && move_cooldown == 0) {
            y_velocity = 31.0;
            update_status(PlayerSettings.player_status.IN_AIR);
        }
    }

    public void move(boolean IS_FACING_RIGHT, boolean IS_CROUCHING) {

        if (IS_FACING_RIGHT != direction) direction = IS_FACING_RIGHT;

        if (IS_FACING_RIGHT && y_pos == FieldSettings.ground_level && move_cooldown == 0) {
            if (IS_CROUCHING) {
                x_velocity = 0.5 * speed;
                update_status(PlayerSettings.player_status.MOVING_SLOW);
            }
            else x_velocity = speed;
        }
        else if (!IS_FACING_RIGHT && y_pos == FieldSettings.ground_level && move_cooldown == 0) {
            if (IS_CROUCHING) {
                x_velocity = 0.5 * -speed;
                update_status(PlayerSettings.player_status.MOVING_SLOW);
            }
            else x_velocity = -speed;
        }

    }

    public void punch(boolean IS_FACING_RIGHT) {
        if (IS_FACING_RIGHT != direction) direction = IS_FACING_RIGHT;

        if (punch_cooldown == 0) {
            IS_PUNCHING = true;
            update_status(PlayerSettings.player_status.PUNCHING);
            move_cooldown = 5;
            punch_cooldown = 8;
            punch_timer = 3;
        }
    }

    public void kick(boolean IS_FACING_RIGHT) {
        if (IS_FACING_RIGHT != direction) direction = IS_FACING_RIGHT;

        if (kick_cooldown == 0 && !IS_KICKING) {
            IS_KICKING = true;
            update_status(PlayerSettings.player_status.KICKING);
            move_cooldown = 8;
            kick_cooldown = 10;
            kick_timer = 5;
        }
    }

    public void duck() {
        if (!status.equals(PlayerSettings.player_status.IN_AIR) &&
        !status.equals(PlayerSettings.player_status.MOVING_SLOW) &&
        !status.equals(PlayerSettings.player_status.PUNCHING) &&
        !status.equals(PlayerSettings.player_status.KICKING)) {
            IS_DUCKING = true;
            hitbox_height = 60;
            update_status(PlayerSettings.player_status.DUCKING);
        }
    }

    public void stop_duck() {
        if (IS_DUCKING) {
            IS_DUCKING = false;
            hitbox_height = 100;
            update_status(PlayerSettings.player_status.IDLE);
        }
    }
}
