import enum as Enum


class game_id:
    GAME_TEST = 0
    GAME_1V1 = 1
    GAME_COMPETITION = 2

class game_state(Enum.Enum):
    GAME_SETUP = 0
    GAME_WAIT_FOR_CLIENTS_TO_LOAD = 1
    GAME_WAIT_FOR_CLIENTS_TO_LOAD2 = 2
    GAME_STARTING = 3
    GAME_RUNNING = 4

class sprite_type:
    PLAYER = 0
    MAP = 1
    GUI = 2

class gui_overlay(Enum.Enum):
    NONE = 0
    MAIN_MENU = 1
    LOBBY = 2
    PAUSE_SCREEN = 3