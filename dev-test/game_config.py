import enum as Enum


class game_id:
    GAME_TEST = 0
    GAME_1V1 = 1
    GAME_COMPETITION = 2
    
class object_type:
    BACKGROUND = "background"
    STICKMAN = "stickman"

class player_stats:
    PUNCH_DAMAGE = 1.0
    KICK_DAMAGE = 5.0

class player_status(Enum.Enum):
    PLAYER_STANDING = 0
    PLAYER_WALKING = 1
    PLAYER_JUMPING = 2
    PLAYER_PUNCHING = 3
    PLAYER_KICKING = 4
    PLAYER_DUCKING = 5
    PLAYER_CROUCHING = 6
    PLAYER_DEFENDING = 7
    PLAYER_MOVE1 = 8
    PLAYER_MOVE2 = 9
    PLAYER_MOVE3 = 10
    PLAYER_ULTIMATE = 11