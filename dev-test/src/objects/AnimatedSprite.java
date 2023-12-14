package src.objects;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;

import src.config;
import src.config.player_status;

public class AnimatedSprite extends Sprite {
    
    private ArrayList<SpriteSheet> sprite_sheets = new ArrayList<>();
    private ArrayList<Double> cycle_times = new ArrayList<>();
    private long cycle_start_time; // in seconds
    private int animation_value;
    private int frame;

    private long last_system_time;

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
        int animation
    ) {
        super(id, x_pos, y_pos, facing_right, height, width, image_height, image_width, path);
        animation_value = animation;
        cycle_start_time = System.nanoTime();
        this.last_system_time = System.nanoTime();
        load_sprite_sheets(image_width, image_height);
    }

    public void load_sprite_sheets(int width, int height) {
        cycle_times.add(0.30); // IDLE
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource("../.." +
                    this.path_to_texture +
                    player_status.IDLE.ordinal() +
                    "/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(2).
                with_size(width, height).
                with_display_size(sprite_width, sprite_height).
                with_rows(1).
                with_cols(2).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }
        cycle_times.add(0.50); // MOVING
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource("../.." +
                    this.path_to_texture +
                    player_status.MOVING.ordinal() +
                    "/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(4).
                with_display_size(sprite_width, sprite_height).
                with_rows(1).
                with_cols(4).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }  
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
        this.y_display_pos = config.field_height - (int)(Math.round(y_pos));
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
        
        if (current_time - last_system_time >=
        (cycle_length / sprite_sheets.get(animation_value).num_frames())) {
            frame += 1;
            if (frame >= sprite_sheets.get(animation_value).num_frames()) frame = 0;
            last_system_time = current_time;
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
