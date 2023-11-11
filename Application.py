from Window import *
from ProgramLogic import *
from AnimationHandler import *

class Application:
    def __init__(self, title: str, dim_width: int, dim_height: int):
        """
        @brief    Application class for communicating between Events, program logic, and the
                  renderer.
        @param title    The title to use on the titlebar of the window.
        @param dim_width    The width of the window to display.
        @param dim_height    The height of the window to display.
        """
        self.title = title
        self.dimensions = (dim_width, dim_height)
        self.wd = Window(title, (200, 200, 200), self.dimensions[0], self.dimensions[1])
        self.pl = ProgramLogic(dim_width, dim_height, (0, 0))
        self.an = AnimationHandler()
        self.isRunning = self.wd.isRunning
        self.isPaused = False
        self.delay = 0.050 # seconds
        self.game_tick = 0
        self.window_tick = 0
    
    def tick(self):
        """
        @brief    Executes actions on a gameloop. This function itself does not loop, but is called
                  outside of the class.
        """
        
        self.game_tick += 1
        self.window_tick += 1
        
        
        self.an.animation_tick()
        if self.game_tick == 1 and not self.isPaused:
            self.process_events()
            self.an.animate_sprite(self.pl.player_1, "s")
            if self.pl.player_1.x_velocity != 0.0: self.an.animate_sprite(self.pl.player_1, "w")
            self.an.animate_sprite(self.pl.player_2, "s")
            if self.pl.player_2.x_velocity != 0.0: self.an.animate_sprite(self.pl.player_2, "w")

            self.pl.tick(self.game_tick * self.delay)
            self.game_tick = 0
        if not self.isRunning: return
        if self.window_tick == 1 and not self.isPaused:
            self.wd.update(self.pl.sprites_list)
            self.window_tick = 0

    def process_events(self):
        """
        @brief    Pings events like system calls and user input, and executes actions depending
                  on the type.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.pl.player_1.move(0)
        if keys[pygame.K_d]:
            self.pl.player_1.move(1)
        if keys[pygame.K_w]:
            self.pl.player_1.move(2)

    def quit(self):
        """
        @brief    Ends the Window process and cleans up upon exit.
        """
        self.wd.quit()
        self.isRunning = False
