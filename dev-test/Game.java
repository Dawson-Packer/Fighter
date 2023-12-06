import java.lang.Thread;
import java.awt.EventQueue;

public class Game extends Thread {

    public boolean IS_RUNNING = false;
    



    private long sleep_delay = 50;
    private int frame_height = 600;
    private int frame_width = 1000;
    private Window window;

    public Game() {

        window = new Window(frame_height, frame_width);
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

    public static void main(String[] args) {
        Game game = new Game();
        game.start();
    }
}