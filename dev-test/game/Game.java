package game;

import java.lang.Thread;

import game.config;

public class Game extends Thread {

    public boolean IS_RUNNING = false;
    

    protected config config;

    private long sleep_delay = 50;
    private int frame_height = 600;
    private int frame_width = 1000;
    private Interface window;
    private ObjectHandler object_handler;
    private UIHandler ui_handler;

    public Game() {

        object_handler = new ObjectHandler();
        ui_handler = new UIHandler();
        window = new Interface(object_handler.action_handler, frame_height, frame_width);
        this.IS_RUNNING = true;
    }

    @Override
    public void run() {
        while (IS_RUNNING) {

            
            // Try to sleep the tick
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

        public ActionHandler action_handler;
        public ObjectHandler() {
            action_handler = new ActionHandler();
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