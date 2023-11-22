import enum as Enum

class window_properties:
    HEIGHT = 600
    WIDTH = 1000

class button_type(Enum.Enum):
    HOST_GAME = 0
    DIRECT_CONNECT = 1
    START_GAME = 2