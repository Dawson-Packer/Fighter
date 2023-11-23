from graphics.Sprites import *
from client_config import *

class main_menu:
    def __init__(self):
        self.objects_list = []
        self.background = Map(-1, "snow_blur")
        self.objects_list.append(self.background)
        self.buttons_list = []
        self.host_game_button = Button(-1, 50, 100, 200, 300, "Host Game", button_type.HOST_GAME)
        self.buttons_list.append(self.host_game_button)
        self.direct_connect_button = Button(-1, 50, 100, 600, 300, "Direct Connect", button_type.DIRECT_CONNECT)
        self.buttons_list.append(self.direct_connect_button)


    def load_elements(self):
        return self.objects_list, self.buttons_list

class lobby:
    def __init__(self):
        self.objects_list = []
        self.background = Map(-1, "snow_blur")
        self.objects_list.append(self.background)
        self.IS_HOST = False
        self.buttons_list = []
        self.start_game_button = Button(-1, 50, 100, 500, 300, "Start Game", button_type.START_GAME)

    def set_host_state(self, IS_HOST: bool):
        self.IS_HOST = IS_HOST
        if IS_HOST:
            self.buttons_list.append(self.start_game_button)

    def load_elements(self):
        return self.objects_list, self.buttons_list