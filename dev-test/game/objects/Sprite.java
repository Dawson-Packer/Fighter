package game.objects;

import java.awt.Image;
import javax.swing.ImageIcon;

public class Sprite {
 
    public int id;

    private int x_pos;
    private int y_pos;
    private String path_to_texture;
    private Image image;
    private int image_width;
    private int image_height;

    public Sprite(
        int id,
        int x_pos,
        int y_pos,
        String path
    ) {
        this.x_pos = x_pos;
        this.y_pos = y_pos;
        this.path_to_texture = path;
        load_image();
    }

    private void load_image() {
        ImageIcon image_icon = new ImageIcon(this.path_to_texture);
        this.image = image_icon.getImage();
        this.image_width = this.image.getWidth(null);
        this.image_height = this.image.getHeight(null);
        image_icon = null;
    }


}
