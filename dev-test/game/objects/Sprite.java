package game.objects;

import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.geom.AffineTransform;
import javax.swing.ImageIcon;

public class Sprite {
 
    private Image image;
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
        this.image = null;
        load_image();
    }

    public void draw(Graphics2D graphics) {
        System.out.println("Drawing");
        AffineTransform old_transform = graphics.getTransform();
        graphics.translate(x_display_pos, y_display_pos);
        graphics.drawImage(image, 0, 0, null);
        graphics.setTransform(old_transform);
    }

    private void load_image() {
        this.image = new ImageIcon(getClass().getResource(path_to_texture)).getImage();
        // this.image = 
        // this.image = image_icon.getImage();
        // this.image_width = this.image.getWidth(null);
        // this.image_height = this.image.getHeight(null);
        // image_icon = null;
    }

    public int get_display_x() { return x_display_pos; }
    public int get_display_y() { return y_display_pos; }

}
