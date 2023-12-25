package src;

import java.lang.Thread;
import java.util.ArrayList;

import interfaces.config.WindowSettings;
import src.objects.*;
import src.objects.characters.StickmanCharacter;
import src.sprites.Sprite;
import interfaces.config.FieldSettings;

public class Game extends Thread {

    public boolean IS_RUNNING = false;

    private long sleep_delay = 32;
    private int frame_height = WindowSettings.window_height;
    private int frame_width = WindowSettings.window_width;
    private WindowGraphics window;
    private ObjectHandler object_handler;
    private UIHandler ui_handler;

    private int i;

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
            object_handler.action_handler.process_inputs();           
            

            if (i % 20 == 0) {
                // System.out.println("say so");
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
                    WindowSettings.window_width / 2,
                    0.0,
                    WindowSettings.window_height,
                    WindowSettings.window_width
                    );
                sprite_list.add(background);

                Player player1 = new StickmanCharacter(0, 0, 50.0, FieldSettings.ground_level, true, 0.0, 0.0, 140, 140, 0.0);
                sprite_list.add(player1);
                player_list.add(player1);
                player1 = null;
            } catch (Exception e) {
                System.out.println("Game graphics failed to load");
                System.out.println(e);
                e.printStackTrace();
            }
        
        }

        public void tick() {

            for (int i = 0; i < player_list.size(); ++i) {
                player_list.get(i).tick();
            }
        }

        public class ActionHandler {

            public boolean KEY_A_PRESSED = false;
            public boolean KEY_D_PRESSED = false;
            public boolean KEY_SPACE_PRESSED = false;
            public boolean KEY_SHIFT_PRESSED = false;
            public boolean KEY_RIGHT_PRESSED = false;
            public boolean KEY_LEFT_PRESSED = false;

            public ActionHandler() {}

            public void process_inputs() {

                if (KEY_SHIFT_PRESSED) duck();
                else stop_duck();
                if (KEY_A_PRESSED) move_left();
                if (KEY_D_PRESSED) move_right();
                if (KEY_SPACE_PRESSED) jump();
                if (KEY_RIGHT_PRESSED || KEY_LEFT_PRESSED) interact();
            }

            private void move_left() {
                player_list.get(0).move(false, KEY_SHIFT_PRESSED);
            }

            private void move_right() {
                player_list.get(0).move(true, KEY_SHIFT_PRESSED);
            }

            private void jump() {
                player_list.get(0).jump();
            }

            private void interact() {
                if (!KEY_SHIFT_PRESSED) {
                    if (KEY_RIGHT_PRESSED) player_list.get(0).punch(true);
                    if (KEY_LEFT_PRESSED) player_list.get(0).punch(false);
                }
                if (KEY_SHIFT_PRESSED) {
                    if (KEY_RIGHT_PRESSED) player_list.get(0).kick(true);
                    if (KEY_LEFT_PRESSED) player_list.get(0).kick(false);
                }

            }

            private void duck() {
                player_list.get(0).duck();
            }

            private void stop_duck() {
                player_list.get(0).stop_duck();
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