package game.objects;

import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.geom.AffineTransform;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import javax.swing.ImageIcon;

import game.config;

public class Sprite implements PaintableEntity {
 
    private Image image;
    
    private SpriteSheet sprite_sheet;
    private ArrayList<SpriteSheet> sprite_sheets = new ArrayList<>();
    private ArrayList<Double> cycle_times = new ArrayList<>();
    private long cycle_start_time; // in seconds
    private int animation_value;

    private boolean image_loaded;
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
    

    public Sprite(
        int id,
        int x_pos,
        int y_pos,
        int height,
        int width,
        String path
    ) {
        cycle_start_time = System.nanoTime();
        this.image_loaded = false;
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
        set_texture();
    }

    public void load_sprite_sheets() {
        cycle_times.add(0.5); // IDLE
        cycle_times.add(1.0); // MOVING

        
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

    protected void flip_texture(boolean horizontally_flipped, boolean vertically_flipped) {
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

    protected void update_sprite(double x_pos, double y_pos) {
        this.x_display_pos = (int)(Math.round(x_pos));
        this.y_display_pos = config.field_height - (int)(Math.round(y_pos));
    }

    @Override
    public void paint(Graphics2D g2d, long time) {
        double cycle_length = cycle_times.get(animation_value) * (1.0e9);
        double progress = (time - cycle_start_time) / cycle_length;
        if (progress < 0) progress = -progress;
        g2d.drawImage(
            sprite_sheets.get(animation_value).get_sprite(progress),
            x_display_pos,
            y_display_pos,
            null
        );
    }

}
