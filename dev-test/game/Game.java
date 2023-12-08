package game;

import java.lang.Thread;
import java.util.ArrayList;

import game.objects.*;

import game.config;

public class Game extends Thread {

    public boolean IS_RUNNING = false;
    

    protected config config;

    private long sleep_delay = 50;
    private int frame_height = 600;
    private int frame_width = 1000;
    private WindowGraphics window;
    private ObjectHandler object_handler;
    private UIHandler ui_handler;

    public Game() {

        object_handler = new ObjectHandler();
        ui_handler = new UIHandler();
        window = new WindowGraphics(object_handler.action_handler, frame_height, frame_width);
        this.IS_RUNNING = true;

        object_handler.load_media();
    }

    @Override
    public void run() {
        while (IS_RUNNING) {

            
            


            window.update(object_handler.sprite_list);
            try {
            Thread.sleep(sleep_delay);
            } catch (Exception e) {
                System.out.println(e);
            }
            if (!window.IS_RUNNING) IS_RUNNING = false;
        }
        quit();
    }

    private void quit() {

        System.out.println("Program exiting...");
        System.exit(0);
    }

    public class ObjectHandler {

        public ArrayList<Sprite> sprite_list;

        public ActionHandler action_handler;
        public ObjectHandler() {
            action_handler = new ActionHandler();
            sprite_list = new ArrayList<Sprite>();
        }

        public void load_media() {
            try {
                Player player1 = new Player(0, 0, 300.0, 500.0, true, 0.0, 0.0, 10, 10, 10, 10, "blank", 0.0);
                sprite_list.add(player1);
                player1 = null;
            } catch (Exception e) {
                System.out.println("Media failed to load");
                System.out.println(e);
            }
        
        }

        public class ActionHandler {

            public ActionHandler() {}

            public void move_left() {
                System.out.println("Moved left");
            }

            public void move_right() {
                System.out.println("Moved right");
            }

            public void jump() {
                System.out.println("Jumped");
            }
        }
    }

    public class UIHandler {

        public UIHandler() {

        }
    }

    public static void main(String[] args) {
        Game game = new Game();
        game.start();
    }
}