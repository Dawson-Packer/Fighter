from Window import *
from Game import *

class Application:
    """Application class for communicating between Events, program logic, and the
        renderer."""
    def __init__(self, title: str, dim_width: int, dim_height: int):
        """
        Initializes an Application object.

        :param title: The title to use on the titlebar of the window.
        :param dim_width: The width of the window to display.
        :param dim_height: The height of the window to display.
        """
        self.title = title
        self.dimensions = (dim_width, dim_height)
        self.wd = Window(title, (200, 200, 200), self.dimensions[0], self.dimensions[1])
        self.game = Game(dim_width, dim_height, (0, 0))
        self.IS_RUNNING = self.wd.IS_RUNNING
        self.IS_PAUSED = False
        self.delay = 0.050 # seconds
        self.game_tick = 0
        self.window_tick = 0
    
    def tick(self):
        """
        Executes actions on a gameloop. This function itself does not loop, but is called
        outside of the class.
        """

        self.game_tick += 1
        self.window_tick += 1
        
        if self.game_tick == 1 and not self.IS_PAUSED:
            self.process_events()
            self.game.run()
            self.game_tick = 0
        if not self.IS_RUNNING: return
        if self.window_tick == 1 and not self.IS_PAUSED:
            self.wd.update(self.game.sprites_list)
            self.window_tick = 0

    def process_events(self):
        """
        Pings events like system calls and user input, and executes actions depending
        on the type.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return
            mouse_buttons_state = pygame.mouse.get_pressed(num_buttons=3)
            if mouse_buttons_state[0]:
                self.game.check_buttons(pygame.mouse.get_pos(), True)
        keys = pygame.key.get_pressed()
        KEY_PRESSED = False
        # if keys[pygame.K_w]: self.game.send_input('W')
        # if keys[pygame.K_a]: self.game.send_input('A')
        # if keys[pygame.K_s]: self.game.send_input('S')
        # if keys[pygame.K_d]: self.game.send_input('D')
        # if keys[pygame.K_SPACE]: self.game.send_input('SPACE')
        # if keys[pygame.K_LSHIFT]: self.game.send_input('LSHIFT')
        # if keys[pygame.K_LCTRL]: self.game.send_input('LCTRL')
        # if keys[pygame.K_UP]: self.game.send_input('UP')
        # if keys[pygame.K_DOWN]: self.game.send_input('DOWN')
        # if keys[pygame.K_RIGHT]: self.game.send_input('RIGHT')
        # if keys[pygame.K_LEFT]: self.game.send_input('LEFT')
        # if keys[pygame.K_a] and not keys[pygame.K_LSHIFT]:
        #     KEY_PRESSED = True
        #     # self.pl.player_1.move(0)
        #     pass
        # if keys[pygame.K_d] and not keys[pygame.K_LSHIFT]:
        #     KEY_PRESSED = True
        #     # self.pl.player_1.move(1)
        #     pass
        # if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
        #     KEY_PRESSED = True
        #     # self.pl.player_1.crouch()
        #     # self.pl.player_1.move(0)
        #     pass
        # if keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
        #     KEY_PRESSED = True
        #     # self.pl.player_1.crouch()
        #     # self.pl.player_1.move(1)
        #     pass
        # if keys[pygame.K_SPACE]:
        #     KEY_PRESSED = True
        #     # self.pl.player_1.move(2)
        #     pass
        # if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and not keys[pygame.K_LSHIFT]:
        #     KEY_PRESSED = True
        #     if keys[pygame.K_LEFT]: 
        #         # self.pl.player_1.punch(-1,
        #         #                         self.pl.player_2,
        #         #                         player_stats.PUNCH_DAMAGE)
        #         pass
        #     if keys[pygame.K_RIGHT]: 
        #         # self.pl.player_1.punch(1,
        #         #                         self.pl.player_2,
        #         #                         player_stats.PUNCH_DAMAGE)
        #         pass
        # if keys[pygame.K_LSHIFT] and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
        #     KEY_PRESSED = True
        #     if keys[pygame.K_LEFT]: 
        #         # self.pl.player_1.kick(-1,
        #         #                         self.pl.player_2,
        #         #                         player_stats.KICK_DAMAGE)
        #         pass
        #     if keys[pygame.K_RIGHT]: 
        #         # self.pl.player_1.kick(1,
        #         #                         self.pl.player_2,
        #         #                         player_stats.KICK_DAMAGE)
        #         pass
        # if keys[pygame.K_LSHIFT] and not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and\
        #     not (keys[pygame.K_a] or keys[pygame.K_d]):
        #     KEY_PRESSED = True
        #     # self.pl.player_1.duck()
        #     pass       

        # if not KEY_PRESSED: self.pl.player_1.reset_status()     


    def quit(self):
        """Ends the Window process and cleans up upon exit."""
        self.wd.quit()
        self.game.host_thread.join()
        self.game.hosted_game.server.incoming_log.terminate()
        self.game.hosted_game.server.outgoing_log.terminate()
        # self.pl.game.log.terminate()
        self.IS_RUNNING = False