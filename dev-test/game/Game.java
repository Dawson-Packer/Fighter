package game;

import java.lang.Thread;
import java.util.ArrayList;

import game.objects.*;

import game.config;

public class Game extends Thread {

    public boolean IS_RUNNING = false;
    

    protected config config;

    private long sleep_delay = 100;
    private int frame_height = game.config.window_height;
    private int frame_width = game.config.window_width;
    private WindowGraphics window;
    private ObjectHandler object_handler;
    private UIHandler ui_handler;

    public int i;

    public Game() {
        i = 0;

        object_handler = new ObjectHandler();
        ui_handler = new UIHandler();
        window = new WindowGraphics(object_handler.action_handler, frame_height, frame_width);
        this.IS_RUNNING = true;

        object_handler.load_game();
    }

    @Override
    public void run() {
        while (IS_RUNNING) {
            ++i;
            object_handler.tick();            
            

            if (i % 20 == 0) {
                System.out.println("say so");
                // object_handler.player_list.get(0).set_texture("/assets/textures/player/stickman/2/2.png");
            }
            if (i % 20 == 10) {
                // object_handler.player_list.get(0).set_texture("/assets/textures/player/stickman/2/2.png");
            }
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

        private int available_object_id;

        private ArrayList<Player> player_list;

        public ActionHandler action_handler;
        public ObjectHandler() {
            available_object_id = -1;
            action_handler = new ActionHandler();
            sprite_list = new ArrayList<Sprite>();
            player_list = new ArrayList<Player>();
        }

        private int next_object_id() {

            ++available_object_id;
            return available_object_id;
        }

        public void load_game() {
            try {

                Background background = new Background(
                    next_object_id(),
                    0,
                    game.config.window_width / 2,
                    0.0,
                    game.config.window_height,
                    game.config.window_width
                    );
                sprite_list.add(background);

                Player player1 = new Player(0, 0, 200.0, game.config.ground_level, true, 0.0, 0.0, 160, 160, 160, 160, "stickman", 0.0);
                sprite_list.add(player1);
                player_list.add(player1);
                player1 = null;
            } catch (Exception e) {
                System.out.println("Game graphics failed to load");
                System.out.println(e);
            }
        
        }

        public void tick() {

            for (int i = 0; i < player_list.size(); ++i) {
                player_list.get(i).tick();
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