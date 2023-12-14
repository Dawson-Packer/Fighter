package src.objects;

import java.util.ArrayList;
import java.util.List;
import java.awt.image.BufferedImage;

public class SpriteSheet {


    private int current_frame;
    private final List<BufferedImage> sprites;

    public SpriteSheet(List<BufferedImage> sprites) {

        this.current_frame = 0;
        this.sprites = new ArrayList<>(sprites);
    }

    public int num_frames() {
        return this.sprites.size();
    }

    public BufferedImage get_sprite(int frame) {
        return this.sprites.get(frame);   
    }

}