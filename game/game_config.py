import enum as Enum


class object_type(Enum.Enum):
    PLAYER = 0
    PROJECTILE = 1
    PLATFORM = 2

class game_state(Enum.Enum):
    GAME_SETUP = 0
    GAME_WAIT_FOR_CLIENTS_TO_LOAD = 1
    GAME_WAIT_FOR_CLIENTS_TO_LOAD2 = 2
    GAME_STARTING = 3
    GAME_RUNNING = 4

class stats:
    PUNCH_DAMAGE = 1.0
    KICK_DAMAGE = 5.0

# TODO: Change from enum back to regular int and propagate through code
class player_status(Enum.Enum):
    STANDING = 0
    WALKING = 1
    JUMPING = 2
    PUNCHING = 3
    KICKING = 4
    DUCKING = 5
    CROUCHING = 6
    DEFENDING = 7
    MOVE1 = 8
    MOVE2 = 9
    MOVE3 = 10
    ULTIMATE = 11
    DROPPING_IN = 12