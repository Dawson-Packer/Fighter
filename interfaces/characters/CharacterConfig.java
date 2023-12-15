package interfaces.characters;

import java.util.ArrayList;

import src.sprites.SpriteSheet;

public class CharacterConfig {
    
    public String name;

    public CharacterConfig() { }

    public void load_textures(
        ArrayList<SpriteSheet> sprite_sheets,
        ArrayList<Double> cycle_times,
        int sprite_width,
        int sprite_height
        ) { }
}
