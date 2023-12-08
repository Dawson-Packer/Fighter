package game;

import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class Interface implements WindowListener {
    
    public boolean IS_RUNNING = false;

    private JFrame frame;
    private int window_width;
    private int window_height;
    private Game.ObjectHandler.ActionHandler action_handler;
    private InputHandler input_handler;
    private Screen screen;

    public Interface(Game.ObjectHandler.ActionHandler action_handler, int window_height, int window_width) {

        this.action_handler = action_handler;
        this.input_handler = new InputHandler();
        this.screen = new Screen();
        this.window_width = window_width;
        this.window_height = window_height;
        IS_RUNNING = true;
        initialize_components();
    }

    private void initialize_components() {

        frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        frame.setSize(window_width, window_height);
        frame.setLocationRelativeTo(null);
        frame.addWindowListener(this);
        frame.addKeyListener(input_handler);
        
        frame.setVisible(true);

    }

    @Override
    public void windowOpened(WindowEvent e) {
        // DO NOTHING
    }

    @Override
    public void windowActivated(WindowEvent e) {
        // DO NOTHING
    }

    @Override
    public void windowDeactivated(WindowEvent e) {
        // DO NOTHING
    }

    @Override
    public void windowDeiconified(WindowEvent e) {
        // DO NOTHING
    }

    @Override
    public void windowIconified(WindowEvent e) {
        // DO NOTHING
    }

    @Override
    public void windowClosing(WindowEvent e) {
        IS_RUNNING = false;
    }    

    @Override
    public void windowClosed(WindowEvent e) {
        // DO NOTHING
    }

    private class InputHandler implements KeyListener {

        public InputHandler() {}

        @Override
        public void keyTyped(KeyEvent e) {
            // DO NOTHING
        }

        @Override
        public void keyPressed(KeyEvent e) {
            switch (e.getKeyCode()) {
                case KeyEvent.VK_A :
                    action_handler.move_left();
                    break;
                case KeyEvent.VK_D :
                    action_handler.move_right();
                    break;
                case KeyEvent.VK_SPACE :
                    action_handler.jump();
                    break;
            }
        }

        @Override
        public void keyReleased(KeyEvent e) {
            // DO NOTHING
        }       
    }

    // TODO: Maybe unnecessary
    private class Screen extends JPanel {

        public Screen() {}

        
    }
}
