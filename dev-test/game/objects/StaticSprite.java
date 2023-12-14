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

public class StaticSprite implements SpriteInterface {
 
    private Image image;

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
    

    public StaticSprite(
        int id,
        int x_pos,
        int y_pos,
        int height,
        int width,
        int image_height,
        int image_width,
        String path
    ) {
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

    @Override
    public void update_sprite(double x_pos, double y_pos) {
        this.x_display_pos = (int)(Math.round(x_pos));
        this.y_display_pos = config.field_height - (int)(Math.round(y_pos));
    }

    @Override
    public void paint(Graphics2D g2d) {
        int horizontal_multiplier = 1, vertical_multiplier = 1;
        if (flipped_horizontally) {
            horizontal_multiplier = -1;
            horizontal_flip_offset = image_width;
        }
        if (flipped_vertically) {
            vertical_multiplier = -1;
            vertical_flip_offset = image_height;
        }
        
        // g2d.drawImage(
        //     sprite_sheets.get(animation_value).get_sprite(progress),
        //     x_display_pos + horizontal_flip_offset,
        //     y_display_pos + vertical_flip_offset,
        //     image_width * horizontal_multiplier, image_height * vertical_multiplier,
        //     null
        // );
        horizontal_flip_offset = 0;
        vertical_flip_offset = 0;
    }

}
