package game.objects;

import java.util.ArrayList;
import java.util.List;
import java.awt.image.BufferedImage;

public class SpriteSheet {

    private final List<BufferedImage> sprites;

    public SpriteSheet(List<BufferedImage> sprites) {

        this.sprites = new ArrayList<>(sprites);
    }

    public int num_sprites() {
        return this.sprites.size();
    }

    public BufferedImage get_sprite(double progress) {
        int frame = (int)(num_sprites() * progress);
        return this.sprites.get(frame);
    }

}