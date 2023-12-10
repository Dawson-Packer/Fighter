package game.objects;

public interface AnimatedSpriteInterface {
    
    public void animate(String dir, int divisor, int cycle_end, boolean facing_right);

    public void reset_animation_tick();
}
