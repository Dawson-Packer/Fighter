package src.sprites;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;

import javax.imageio.ImageIO;

import interfaces.config.PlayerSettings;
import src.objects.Player;
import interfaces.characters.CharacterConfig;
import interfaces.config.FieldSettings;

public class AnimatedSprite extends Sprite {
    
    private ArrayList<SpriteSheet> sprite_sheets = new ArrayList<>();
    private ArrayList<Double> cycle_times = new ArrayList<>();
    private int animation_value;
    private int frame;

    private long previous_time;

    public AnimatedSprite(
        int id,
        int x_pos,
        int y_pos,
        boolean facing_right,
        int height,
        int width,
        int image_height,
        int image_width,
        String path,
        int animation,
        CharacterConfig character
    ) {
        super(id, x_pos, y_pos, facing_right, height, width, image_height, image_width, path);
        animation_value = animation;
        this.previous_time = System.nanoTime();
        load_sprite_sheets(character);
    }

    public void load_sprite_sheets(CharacterConfig config) {
        config.load_textures(sprite_sheets, cycle_times, sprite_width, sprite_height);
    }

    public int get_display_x() { return x_display_pos; }
    public int get_display_y() { return y_display_pos; }

    @Override
    public void flip_texture(boolean horizontally_flipped, boolean vertically_flipped) {
        if (horizontally_flipped) {
            if (flipped_horizontally) flipped_horizontally = false;
            else flipped_horizontally = true;
        }
        if (vertically_flipped) {
            if (flipped_vertically) flipped_vertically = false;
            else flipped_vertically = true;
        }
    }

    protected void set_animation_value(int val) {
        animation_value = val;
    }

    @Override
    public void update_sprite(double x_pos, double y_pos) {
        this.x_display_pos = (int)(Math.round(x_pos));
        this.y_display_pos = FieldSettings.field_height - (int)(Math.round(y_pos));
    }

    @Override
    public void paint(Graphics2D g2d) {
        long current_time = System.nanoTime();
        double cycle_length = cycle_times.get(animation_value) * (1.0e9);
        int horizontal_multiplier = 1, vertical_multiplier = 1;
        if (flipped_horizontally) {
            horizontal_multiplier = -1;
            horizontal_flip_offset = sprite_width;
        }
        if (flipped_vertically) {
            vertical_multiplier = -1;
            vertical_flip_offset = sprite_height;
        }
        
        if (current_time - previous_time >=
        (cycle_length / sprite_sheets.get(animation_value).num_frames())) {
            frame += 1;
            if (frame >= sprite_sheets.get(animation_value).num_frames()) frame = 0;
            previous_time = current_time;
        }
        g2d.drawImage(
            sprite_sheets.get(animation_value).get_sprite(frame),
            x_display_pos + horizontal_flip_offset,
            y_display_pos + vertical_flip_offset,
            sprite_width * horizontal_multiplier, sprite_height * vertical_multiplier,
            null
        );
        horizontal_flip_offset = 0;
        vertical_flip_offset = 0;
    }
}