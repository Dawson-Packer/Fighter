import enum as Enum

class sprite_type:
    PLAYER = 0
    MAP = 1
    GUI = 2

class gui_overlay(Enum.Enum):
    NONE = 0
    MAIN_MENU = 1
    LOBBY = 2
    PAUSE_SCREEN = 3