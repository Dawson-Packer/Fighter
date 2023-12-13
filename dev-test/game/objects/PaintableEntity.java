package game.objects;

import java.awt.Graphics2D;
/**
 * PaintableEntity
 */
interface PaintableEntity {
    public void paint(Graphics2D g2d, long time);
}