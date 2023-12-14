package game.objects;

import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;

import game.config;
import game.config.player_status;

public class AnimatedSprite implements SpriteInterface {
 
    private Image image;
    
    private ArrayList<SpriteSheet> sprite_sheets = new ArrayList<>();
    private ArrayList<Double> cycle_times = new ArrayList<>();
    private long cycle_start_time; // in seconds
    private int animation_value;

    public int id;
    public int image_width;
    public int image_height;

    private boolean flipped_vertically;
    private int vertical_flip_offset;
    private boolean flipped_horizontally;
    private int horizontal_flip_offset;
    private int x_display_pos;
    private int y_display_pos;
    public String path_to_texture;

    private long last_system_time;
    

    public AnimatedSprite(
        int id,
        int x_pos,
        int y_pos,
        int height,
        int width,
        int image_height,
        int image_width,
        String path,
        int animation
    ) {
        animation_value = animation;
        cycle_start_time = System.nanoTime();
        this.last_system_time = System.nanoTime();
        this.x_display_pos = x_pos;
        this.y_display_pos = y_pos;
        this.image_height = height;
        this.image_width = width;
        this.path_to_texture = path;
        this.image = null;
        this.flipped_vertically = false;
        this.vertical_flip_offset = 0;
        this.flipped_horizontally = false;
        this.horizontal_flip_offset = 0;

        load_sprite_sheets(image_width, image_height);
        set_texture();
    }

    public void load_sprite_sheets(int width, int height) {
        cycle_times.add(0.45); // IDLE
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
                with_display_size(image_width, image_height).
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
            System.out.println("../.." +
                    this.path_to_texture +
                    player_status.MOVING.ordinal() +
                    "/sprites.png");
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(4).
                with_display_size(image_width, image_height).
                with_rows(1).
                with_cols(4).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }



        
    }

    public void set_texture(String...path) {
        // String image_path = path.length > 0 ? path[0] : "null";
        // // if (image_loaded) image.flush();
        // if (image_path != "null") {
        //     image = null;
        //     image = new ImageIcon(getClass().getResource(image_path)).getImage();
        //     image = image.getScaledInstance(image_width, image_height, java.awt.Image.SCALE_SMOOTH);
        // }
        // else {
        //     image = null;
        //     image = new ImageIcon(getClass().getResource(path_to_texture)).getImage();
        //     image = image.getScaledInstance(image_width, image_height, java.awt.Image.SCALE_SMOOTH);
        // }

        // image_loaded = true;
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
        double progress = (current_time - cycle_start_time) / cycle_length;
        if (current_time - cycle_start_time >= cycle_length) {
            cycle_start_time = last_system_time;
        }
        if (progress > 1.0) progress = 0.125;
        if (progress < 0.0) progress = -progress;
        int horizontal_multiplier = 1, vertical_multiplier = 1;
        if (flipped_horizontally) {
            horizontal_multiplier = -1;
            horizontal_flip_offset = image_width;
        }
        if (flipped_vertically) {
            vertical_multiplier = -1;
            vertical_flip_offset = image_height;
        }
        
        g2d.drawImage(
            sprite_sheets.get(animation_value).get_sprite(progress),
            x_display_pos + horizontal_flip_offset,
            y_display_pos + vertical_flip_offset,
            image_width * horizontal_multiplier, image_height * vertical_multiplier,
            null
        );
        last_system_time = current_time;
        horizontal_flip_offset = 0;
        vertical_flip_offset = 0;
    }

}
