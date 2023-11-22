from client.Sprites import *
from client_config import *

class main_menu:
    def __init__(self):
        self.background = Map("snow_blur")
        self.buttons_list = []
        self.host_game_button = Button(50, 100, 200, 300, "Host Game", button_type.HOST_GAME)
        self.buttons_list.append(self.host_game_button)
        self.direct_connect_button = Button(50, 100, 600, 300, "Direct Connect", button_type.DIRECT_CONNECT)
        self.buttons_list.append(self.direct_connect_button)


    def load_elements(self):
        return (self.background, self.host_game_button, self.direct_connect_button),\
            (self.host_game_button, self.direct_connect_button)