package src.config.characters;

import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;

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
        int image_width,
        int image_height,
        int sprite_width,
        int sprite_height
        ) {

        // * IDLE
        cycle_times.add(0.30);
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
                with_size(image_width, image_height).
                with_display_size(sprite_width, sprite_height).
                with_rows(1).
                with_cols(2).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }

        // * MOVING
        cycle_times.add(0.30);
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
                with_size(image_width, image_height).
                with_display_size(sprite_width, sprite_height).
                with_rows(1).
                with_cols(4).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }

        // * IN_AIR
        cycle_times.add(0.25);
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource(
                    "../../assets/textures/player/stickman/in_air/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(4).
                with_size(image_width, image_height).
                with_display_size(sprite_width, sprite_height).
                with_rows(4).
                with_cols(1).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }

        // * PUNCHING
        cycle_times.add(0.25);
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource(
                    "../../assets/textures/player/stickman/punching/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(3).
                with_size(image_width, image_height).
                with_display_size(sprite_width, sprite_height).
                with_rows(3).
                with_cols(1).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }

        // * KICKING
        cycle_times.add(0.15);
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource(
                    "../../assets/textures/player/stickman/kicking/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(3).
                with_size(image_width, image_height).
                with_display_size(sprite_width, sprite_height).
                with_rows(3).
                with_cols(1).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }

        // * DUCKING
        cycle_times.add(1.0);
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource(
                    "../../assets/textures/player/stickman/ducking/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(1).
                with_size(image_width, image_height).
                with_display_size(sprite_width, sprite_height).
                with_rows(1).
                with_cols(1).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }

        // * MOVING_SLOW
        cycle_times.add(1.0);
        try {
            BufferedImage sheet = ImageIO.read(
                AnimatedSprite.class.getResource(
                    "../../assets/textures/player/stickman/moving_slow/sprites.png"
                )
            );
            sprite_sheets.add(
                new SpriteSheetBuilder().
                using(sheet).
                with_count(4).
                with_size(image_width, image_height).
                with_display_size(sprite_width, sprite_height).
                with_rows(4).
                with_cols(1).
                build()
            );
        } catch (IOException e) {
            System.out.println(e);
        }
    }

}
