package game.objects;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.IOException;

import javax.imageio.ImageIO;

import org.imgscalr.Scalr;

import game.config;

public class StaticSprite extends Sprite {
 
    private BufferedImage image;

    public StaticSprite(
        int id,
        int x_pos,
        int y_pos,
        boolean facing_right,
        int height,
        int width,
        int image_height,
        int image_width,
        String path
    ) {
        super(id, x_pos, y_pos, facing_right, height, width, image_height, image_width, path);
        this.image = null;
        set_texture(this.path_to_texture);
    }

    public void set_texture(String path) {
        System.out.println(path);
        try {
            this.image = ImageIO.read(
                StaticSprite.class.getResource("../.." + path)
            );
        } catch (IOException e) {
            System.out.println(e);
        }
        image = Scalr.resize(image, Scalr.Method.BALANCED, sprite_width, sprite_height);
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
            horizontal_flip_offset = sprite_width;
        }
        if (flipped_vertically) {
            vertical_multiplier = -1;
            vertical_flip_offset = sprite_height;
        }
        System.out.println("Hello!");
        g2d.drawImage(
            this.image,
            x_display_pos + horizontal_flip_offset,
            y_display_pos + vertical_flip_offset,
            sprite_width * horizontal_multiplier, sprite_height * vertical_multiplier,
            null
        );
        horizontal_flip_offset = 0;
        vertical_flip_offset = 0;
    }
}
