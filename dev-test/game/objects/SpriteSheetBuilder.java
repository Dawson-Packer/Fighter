package game.objects;

import java.awt.image.BufferedImage;
import java.util.ArrayList;

import org.imgscalr.Scalr;

public class SpriteSheetBuilder {
    
    private BufferedImage sprite_sheet;
    private int rows, columns;
    private int sprite_width, sprite_height;
    private int image_width, image_height;
    private int sprite_count;

    public SpriteSheetBuilder using(BufferedImage image) {
        this.sprite_sheet = image;
        return this;
    }

    public SpriteSheetBuilder with_rows(int rows) {
        this.rows = rows;
        return this;
    }

    public SpriteSheetBuilder with_cols(int cols) {
        this.columns = cols;
        return this;
    }

    public SpriteSheetBuilder with_size(int width, int height) {
        this.image_width = width;
        this.image_height = height;
        return this;
    }

    public SpriteSheetBuilder with_display_size(int width, int height) {
        this.sprite_width = width;
        this.sprite_height = height;
        return this;
    }
    
    public SpriteSheetBuilder with_count(int count) {
        this.sprite_count = count;
        return this;
    }

    protected int num_sprites() {
        return this.sprite_count;
    }

    protected int num_rows() {
        return this.rows;
    }

    protected int num_columns() {
        return this.columns;
    }

    protected int get_sprite_width() {
        return this.image_width;
    }

    protected int get_sprite_height() {
        return this.image_height;
    }

    protected BufferedImage get_sprite_sheet() {
        return this.sprite_sheet;
    }

    public SpriteSheet build() {
        int count = num_sprites();
        int rows = num_rows();
        int columns = num_columns();
        if (count == 0) {
            count = rows * columns;
        }

        BufferedImage sheet = get_sprite_sheet();

        int width = get_sprite_width();
        int height = get_sprite_height();
        if (width == 0) {
            width = sheet.getWidth() / columns;
        }
        if (height == 0) {
            height = sheet.getHeight() / rows;
        }

        int x = 0;
        int y = 0;
        ArrayList<BufferedImage> sprites = new ArrayList<>(count);

        for (int i = 0; i < count; ++i) {
            BufferedImage frame = sheet.getSubimage(x, y, width, height);
            frame = Scalr.resize(frame, Scalr.Method.BALANCED, sprite_width, sprite_height);
            sprites.add(frame);
            x += width;
            if (x >= width * columns) {
                x = 0;
                y += height;
            }
        }

        return new SpriteSheet(sprites);
    }
}