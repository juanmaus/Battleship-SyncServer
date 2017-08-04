from enum import Enum
import datetime
import uuid


# ---------------------------------------------------------------------------------------
# ENUMERATION GAME STATUS
# ---------------------------------------------------------------------------------------
class GameStatus(Enum):

    """
        This enumeration defines the possible status in which a game can be. Initially all
        games are created with WAITING_FOR_PLAYERS status and can be set to active as soon
        as the required amount of players according to the game's mode have joined the game.
    """

    ACTIVE = 1
    WAITING_FOR_PLAYERS = 0
    FINISHED = -1


# ---------------------------------------------------------------------------------------
# ENUMERATION GAME MODE
# ---------------------------------------------------------------------------------------
class GameMode(Enum):

    """
        Defines the mode in which a game should be created. The game mode determines the 
        amount of players required to get the game started and the amount of boards that 
        need to be generated.
    """
    PLAYER_2v2 = 2
    PLAYER_4v4 = 4


# ---------------------------------------------------------------------------------------
# CLASS GAME
# ---------------------------------------------------------------------------------------
class Game:
    """ 
        This class represents a game in the system. Every time a new game is created, a 
        unique uuid4 identifier is assigned to the game so it can be uniquely referenced.
        Game instances are persisted using REDIS in-memory data structure storage so that
        the game state is persistent across multiple http requests originated by different
        player. 
        
        A game can be created by any registered player in the system an can be created in 
        two different modes: 2-player mode and 4-player mode. Initially games are created
        with WAITING_FOR_PLAYERS status which sets the game in waiting mode until the 
        required amount of players have joined the game. 
    """

    # -----------------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------------------------------------
    def __init__(self, mode, owner, player_layout):
        """
            :param mode: GameMode type. Can be 4PLAYER mode or 2PLAYER mode
            :param owner: The id of the user that created the game.
            :param player_layout: A list of the player types that can join the game. 
        """
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.datetime.now
        self.game_status = GameStatus.WAITING_FOR_PLAYERS
        self.mode = mode
        self.owner = owner
        self.moves_next = owner
        self.player_layout = player_layout
        self.players = []

    # -----------------------------------------------------------------------------------
    # METHOD JOIN PLAYER
    # -----------------------------------------------------------------------------------
    def join_player(self, player):
        # 1) Validate player is not already present in the game and that is type matches
        # one of the available types in the player_layout attribute.
        # 2) Create a board for the new player using the current game's spec and initialize
        # stats
        # 3) Add the board id to player and add the player to the player's list.
        # TODO!!!
        self.players.append(player)
        return True

