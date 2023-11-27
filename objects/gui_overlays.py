from .GameObjects import *
from client_config import *

class menu:
    def __init__(self):
        self.objects_list = []
        self.buttons_list = []

    def load_elements(self):
        return self.objects_list, self.buttons_list

class main_menu(menu):
    def __init__(self):
        super().__init__()
        self.background = Map(-1, "snow_blur")
        self.objects_list.append(self.background)
        self.host_game_button = Button(-1, 50, 100, 200, 300, "Host Game", button_type.HOST_GAME)
        self.buttons_list.append(self.host_game_button)
        self.direct_connect_button = Button(-1, 50, 100, 600, 300, "Direct Connect", button_type.DIRECT_CONNECT)
        self.buttons_list.append(self.direct_connect_button)

class lobby(menu):
    def __init__(self):
        super().__init__()
        self.background = Map(-1, "snow_blur")
        self.objects_list.append(self.background)
        self.IS_HOST = False
        self.start_game_button = Button(-1, 50, 100, 500, 300, "Start Game", button_type.START_GAME)

    def set_host_state(self, IS_HOST: bool):
        self.IS_HOST = IS_HOST
        if IS_HOST:
            self.buttons_list.append(self.start_game_button)
    
class pause_screen(menu):
    pass

class character_pick(menu):
    def __init__(self):
        super().__init__()
        self.background = Map(-1, "snow_blur")
        self.objects_list.append(self.background)
        self.stickman_button = Button(-1, 50, 100, 50, 100, "Stickman",
                                      button_type.STICKMAN_CHARACTER)
        self.buttons_list.append(self.stickman_button)