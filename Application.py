import threading as th
from Window import *
from ProgramLogic import *
from config import *
import Comm as com

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
        self.isRunning = self.wd.isRunning
        self.app_stage = 0
        self.isPaused = False
        self.delay = 0.050 # seconds
        self.game_tick = 0
        self.window_tick = 0

        self.cmm = com.Communication()
        self.cmm.listen_for_connections()

        # self.cmm_conn = th.Thread(target=self.cmm.listen_for_connections)
        # self.cmm_conn.start()
    
    def tick(self):
        """
        @brief    Executes actions on a gameloop. This function itself does not loop, but is called
                  outside of the class.
        """
        self.cmm.receive()

        if self.app_stage == 0:
            direct_connect = input("Direct connect to IP:")
            self.cmm.direct_connect(direct_connect)
            self.app_stage += 1
        elif self.app_stage == 1:

            self.game_tick += 1
            self.window_tick += 1
            
            if self.game_tick == 1 and not self.isPaused:
                self.process_events()
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
        KEY_PRESSED = False
        if keys[pygame.K_a] and not keys[pygame.K_LSHIFT]:
            KEY_PRESSED = True
            self.pl.player_1.move(0)
        if keys[pygame.K_d] and not keys[pygame.K_LSHIFT]:
            KEY_PRESSED = True
            self.pl.player_1.move(1)
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
            KEY_PRESSED = True
            self.pl.player_1.crouch()
            self.pl.player_1.move(0)
        if keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
            KEY_PRESSED = True
            self.pl.player_1.crouch()
            self.pl.player_1.move(1)
        if keys[pygame.K_SPACE]:
            KEY_PRESSED = True
            self.pl.player_1.move(2)
        if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and not keys[pygame.K_LSHIFT]:
            KEY_PRESSED = True
            if keys[pygame.K_LEFT]: 
                self.pl.player_1.punch(-1,
                                        self.pl.player_2,
                                        player_stats.PUNCH_DAMAGE)
            if keys[pygame.K_RIGHT]: 
                self.pl.player_1.punch(1,
                                        self.pl.player_2,
                                        player_stats.PUNCH_DAMAGE)
        if keys[pygame.K_LSHIFT] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            KEY_PRESSED = True
            if keys[pygame.K_LEFT]: 
                self.pl.player_1.kick(-1,
                                        self.pl.player_2,
                                        player_stats.KICK_DAMAGE)
            if keys[pygame.K_RIGHT]: 
                self.pl.player_1.kick(1,
                                        self.pl.player_2,
                                        player_stats.KICK_DAMAGE)
        if keys[pygame.K_LSHIFT] and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and\
            not (keys[pygame.K_a] or keys[pygame.K_d]):
            KEY_PRESSED = True
            self.pl.player_1.duck()       

        if not KEY_PRESSED: self.pl.player_1.reset_status()     


    def quit(self):
        """
        @brief    Ends the Window process and cleans up upon exit.
        """
        # self.cmm_conn.join()
        self.wd.quit()
        self.isRunning = False
