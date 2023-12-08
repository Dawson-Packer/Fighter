package game.objects;

import game.config;
import game.config.player_status;

public class Object {
    
    public int id;

    protected config.player_status status;

    protected double x_pos;
    protected double y_pos;

    /**
     * @param id The id of the Object
     * @param x_pos The x-position of the Object
     * @param y_pos The y-position of the Object
     */
    public Object(
        int id,
        double x_pos,
        double y_pos
    ) {
        this.x_pos = x_pos;
        this.y_pos = y_pos;
        this.status = player_status.IDLE;
    }

    public double get_x() { return this.x_pos; }
    public double get_y() { return this.y_pos; }


}
