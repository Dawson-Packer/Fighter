package game.objects;

import java.awt.Graphics2D;

public class Sprite {

    public int id;
    public int sprite_height;
    public int sprite_width;

    protected boolean flipped_horizontally;
    protected int horizontal_flip_offset;
    protected boolean flipped_vertically;
    protected int vertical_flip_offset;

    protected int x_display_pos;
    protected int y_display_pos;
    protected String path_to_texture;



    /**
     * @param id The id of the Sprite object
     * @param x_pos The x-position of the Sprite
     * @param y_pos The y-position of the Sprite
     * @param facing_right True if the Sprite is directed toward the right
     * @param height The rendered height of the Sprite
     * @param width The rendered width of the Sprite
     * @param image_height The actual height of the Sprite texture
     * @param image_width The actual width of the Sprite texture
     * @param path The path to the Sprite's texture(s)
     */
    public Sprite(
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
        this.id = id;
        this.x_display_pos = x_pos;
        this.y_display_pos = y_pos;
        this.sprite_height = height;
        this.sprite_width = width;
        this.path_to_texture = path;
        this.flipped_horizontally = !facing_right;
        this.flipped_vertically = false;
        this.horizontal_flip_offset = 0;
        this.vertical_flip_offset = 0;
    }


    /**
     * @param horizontally_flipped Set to true to flip the texture horizontally
     * @param vertically_flipped Set to true to flip the texture vertically
     */
    public void flip_texture(boolean horizontally_flipped, boolean vertically_flipped) { }

    /**
     * @param g2d The Graphics2D object to load the Sprite into
     */
    public void paint(Graphics2D g2d) { }

    /**
     * @param x_pos The actual x-position of the Object
     * @param y_pos The actual y-position of the Object
     */
    public void update_sprite(double x_pos, double y_pos) { }
}