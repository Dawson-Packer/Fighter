package game;

import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.awt.Container;
import java.awt.Rectangle;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JComponent;

import game.objects.*;

public class WindowGraphics extends JComponent implements WindowListener {
    
    public boolean IS_RUNNING = false;

    private JFrame frame;
    private int window_width;
    private int window_height;
    private Game.ObjectHandler.ActionHandler action_handler;
    private InputHandler input_handler;
    private Container container;

    public WindowGraphics(Game.ObjectHandler.ActionHandler action_handler, int window_height, int window_width) {

        this.action_handler = action_handler;
        this.input_handler = new InputHandler();
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
        frame.getContentPane().setBackground(null);
        frame.setLayout(null);
        container = frame.getContentPane();

        
        frame.setVisible(true);

    }

    // TODO: Find a library to do this
    public void update(ArrayList<Sprite> sprite_list) {
        // System.out.println(Integer.toString(sprite_list.size()));
        for (int i = 0; i < sprite_list.size(); ++i) {
            JPanel panel = new JPanel();
            
            Rectangle bounds = new Rectangle(sprite_list.get(i).get_display_x(),
            sprite_list.get(i).get_display_y(),
            sprite_list.get(i).image_width,
            sprite_list.get(i).image_height);
            panel.setBounds(bounds);
            bounds = null;
            panel.setBackground(null);
            container.add(panel);

            JLabel image_label = new JLabel();
            image_label.setIcon(sprite_list.get(i).image);
            panel.add(image_label);
            image_label = null;
            panel = null;

        }
        // frame.setVisible(true);
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
}
