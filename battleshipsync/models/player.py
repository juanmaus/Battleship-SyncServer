from enum import Enum


# ---------------------------------------------------------------------------------------
# ENUMERATION PLAYER TYPE
# ---------------------------------------------------------------------------------------
class PlayerType(Enum):
    """
        Determines the types of player available in the game. The human type is to be 
        used on a game client interface and the computer type is to be used by autonomous 
        program that connects to the server and plays automatically without any human 
        intervention
    """
    HUMAN = 1
    COMPUTER = 2


# ---------------------------------------------------------------------------------------
# CLASS PLAYER
# ---------------------------------------------------------------------------------------
class Player:
    def __init__(self):
        pass