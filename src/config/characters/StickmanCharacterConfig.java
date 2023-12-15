package src.config.characters;

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;

import interfaces.characters.CharacterConfig;
import src.sprites.AnimatedSprite;
import src.sprites.SpriteSheet;
import src.sprites.SpriteSheetBuilder;

public class StickmanCharacterConfig extends CharacterConfig{

    public StickmanCharacterConfig() {
        name = "stickman";
    }

    @Override
    public void load_textures(
        ArrayList<SpriteSheet> sprite_sheets,
        ArrayList<Double> cycle_times,
        int sprite_width,
        int sprite_height
        ) {
        int width = 256;
        int height = 256;
        cycle_times.add(0.30); // IDLE
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource(
                    "../../assets/textures/player/stickman/idle/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(2).
                with_size(width, height).
                with_display_size(sprite_width, sprite_height).
                with_rows(1).
                with_cols(2).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }
        cycle_times.add(0.50); // MOVING
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource(
                    "../../assets/textures/player/stickman/moving/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(4).
                with_display_size(sprite_width, sprite_height).
                with_rows(1).
                with_cols(4).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }  
    }

}
