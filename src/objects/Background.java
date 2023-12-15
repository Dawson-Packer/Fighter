package src.objects;

import interfaces.config.FieldSettings;
import src.sprites.StaticSprite;

public class Background extends StaticSprite {
    
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
            (int)Math.round(x_pos) - (sprite_width / 2),
            FieldSettings.field_height - (int)Math.round(y_pos) - sprite_height,
            true,
            sprite_height,
            sprite_width,
            1024,
            640,
            "/assets/textures/background/" + Integer.toString(map_id) + ".png"
        );
        this.map_id = map_id;
    }
}
