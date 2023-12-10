package game.objects;

import game.config;

public class Background extends Sprite {
    
    public int map_id;

    public Background(
        int object_id,
        int map_id,
        double x_pos,
        double y_pos,
        int sprite_height,
        int sprite_width
    ) {
        super(
            object_id,
            (int)Math.round(x_pos),
            config.field_height - (int)Math.round(y_pos),
            sprite_height,
            sprite_width,
            "/assets/textures/background/" + map_id + ".png"
        );
        this.map_id = map_id;
    }
}
