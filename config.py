import enum as Enum

class player_stats:
    PUNCH_DAMAGE = 5.0
    KICK_DAMAGE = 10.0

class player_status(Enum.Enum):
    PLAYER_STANDING = 0
    PLAYER_WALKING = 1
    PLAYER_JUMPING = 2
    PLAYER_PUNCHING = 3
    PLAYER_KICKING = 4
    PLAYER_DEFENDING = 5
    PLAYER_MOVE1 = 6
    PLAYER_MOVE2 = 7
    PLAYER_MOVE3 = 8
    PLAYER_ULTIMATE = 9