import enum as Enum

class sprite_type:
    PLAYER = 0
    COLLIDABLE = 1
    MAP = 2
    GUI = 3
    PARTICLE = 4

class gui_overlay(Enum.Enum):
    NONE = 0
    MAIN_MENU = 1
    LOBBY = 2
    PAUSE_SCREEN = 3