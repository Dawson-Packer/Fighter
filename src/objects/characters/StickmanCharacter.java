package src.objects.characters;

import src.config.characters.StickmanCharacterConfig;
import src.objects.Player;

public class StickmanCharacter extends Player {
    
    public StickmanCharacter(
        int object_id,
        int client_id,
        double x_pos,
        double y_pos,
        boolean facing_right,
        double x_velocity,
        double y_velocity,
        int sprite_height,
        int sprite_width,
        double rotation
    ) {
        super(
            object_id,
            client_id,
            x_pos,
            y_pos,
            facing_right,
            x_velocity,
            y_velocity,
            100,
            20,
            sprite_height,
            sprite_width,
            new StickmanCharacterConfig(),
            rotation
            );
        
    }

    @Override
    public void tick() {

        // prepare_animation();

        update_status(process_physics());

        ping();

        update_sprite(x_pos, y_pos + sprite_height);
        // reset_status();
    }

    
}
