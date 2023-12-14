package game.objects;

import java.awt.Graphics2D;
/**
 * Sprite
 */
interface SpriteInterface {

    public void flip_texture(boolean horizontally_flipped, boolean vertically_flipped);

    public void paint(Graphics2D g2d);

    public void update_sprite(double x_pos, double y_pos);
}