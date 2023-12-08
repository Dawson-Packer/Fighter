package game.objects;

import java.awt.Image;
import javax.swing.ImageIcon;

public class Sprite {
 
    public ImageIcon image;
    public int id;
    public int image_width;
    public int image_height;

    private int x_display_pos;
    private int y_display_pos;
    private String path_to_texture;
    

    public Sprite(
        int id,
        int x_pos,
        int y_pos,
        int height,
        int width,
        String path
    ) {
        this.x_display_pos = x_pos;
        this.y_display_pos = y_pos;
        this.image_height = height;
        this.image_width = width;
        this.path_to_texture = path;
        load_image();
    }

    private void load_image() {
        ImageIcon image = new ImageIcon(this.path_to_texture);
        // this.image = image_icon.getImage();
        // this.image_width = this.image.getWidth(null);
        // this.image_height = this.image.getHeight(null);
        // image_icon = null;
    }

    public int get_display_x() { return x_display_pos; }
    public int get_display_y() { return y_display_pos; }

}
