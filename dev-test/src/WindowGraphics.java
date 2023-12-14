package src;

import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.awt.image.BufferedImage;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JComponent;

import src.objects.*;

public class WindowGraphics extends JComponent implements WindowListener {
    
    public boolean IS_RUNNING = false;

    private JFrame frame;
    private Panel panel;
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
        panel = new Panel(window_height, window_width);
        frame.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        frame.setSize(window_width, window_height);
        frame.setLocationRelativeTo(null);
        frame.addWindowListener(this);
        frame.addKeyListener(input_handler);
        frame.setLayout(new BorderLayout());
        // container = frame.getContentPane();
        frame.add(panel);
        // frame.pack();

        
        frame.setVisible(true);

    }

    public void update(ArrayList<Sprite> sprite_list) {
        panel.paintComponent(panel.graphics);

        panel.load_background();
        for (int i = 0; i < sprite_list.size(); ++i) {
            sprite_list.get(i).paint(panel.graphics);
        }
        panel.render();
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

    private class Panel extends JPanel {

        private Graphics2D graphics;
        private BufferedImage image;
        private ArrayList<AnimatedSprite> sprite_list;

        private int panel_height;
        private int panel_width;
        private final int TARGET_DELAY = (int)(1000 / 60.0); // Target delay in milliseconds

        public Panel(int height, int width) {
            panel_height = height;
            panel_width = width;

            image = new BufferedImage(panel_width, panel_height, BufferedImage.TYPE_INT_ARGB);
            graphics = image.createGraphics();
            graphics.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
            RenderingHints.VALUE_ANTIALIAS_ON);
            graphics.setRenderingHint(RenderingHints.KEY_INTERPOLATION,
            RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        }

        public void load_background() {
            graphics.setColor(Color.WHITE);
            graphics.fillRect(0, 0, panel_width, panel_height);
        }

        public void load_objects(ArrayList<AnimatedSprite> sprites) {
            this.sprite_list = sprites;
        }

        public void render() {
            Graphics g = getGraphics();
            g.drawImage(image, 0, 0, null);
            g.dispose();
        }

        @Override
        public void paintComponent(Graphics g) {
            super.paintComponent(graphics);
            // Graphics2D g2d = (Graphics2D) g.create();
            
            // for (int i = 0; i < sprite_list.size(); ++i) {
            //     BufferedImage sprite = sprite_list.get(i);
            // }
            // BufferedImage sprite = spriteSheet.getSprite(spriteEngine.getCycleProgress());
            // int x = (getWidth() - sprite.getWidth()) / 2;
            // int y = (getHeight() - sprite.getHeight()) / 2;
            // g2d.drawImage(sprite, x, y, this);
            // g2d.dispose();
        }

    }
}
