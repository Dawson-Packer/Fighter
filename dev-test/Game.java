import java.lang.Thread;
import javax.swing.JFrame;
import javax.swing.WindowConstants;
import java.awt.EventQueue;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;

public class Game {

    public boolean IS_RUNNING = false;
    



    private long sleep_delay = 50;
    private int frame_height = 600;
    private int frame_width = 1000;
    private Window window;

    public Game() {

        window = new Window(frame_height, frame_width);
        this.IS_RUNNING = true;
    }

    public void tick() {
        // while (IS_RUNNING) {

            
        //     // Try to sleep the tick
        //     try {
        //     Thread.sleep(sleep_delay);
        //     } catch (Exception e) {
        //         System.out.println(e);
        //     }
        //     if (!window.IS_RUNNING) IS_RUNNING = false;
        // }
        // quit();
    }



    private void quit() {

        System.out.println("Program exiting...");
        System.exit(0);
    }

    public static void main(String[] args) {
        EventQueue.invokeLater(() -> {
            Game game = new Game();
            game.tick();
        });
        
    }
}