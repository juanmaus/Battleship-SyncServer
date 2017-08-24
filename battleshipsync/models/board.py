from enum import Enum
from battleshipsync.models.player import Player
from battleshipsync.extensions.game_board_extension import create_board
import json


def parse_board_id(board_id):
    """
        ---------------------------------------------------------------------------------   
        :param board_id: the id of the board. 
        :return: A dictionary with the player' id and game' id
        ---------------------------------------------------------------------------------
    """
    game_id, player_id = board_id.split("+")
    return {
        "game_id": game_id,
        "player_id": player_id
    }


# ---------------------------------------------------------------------------------------
# ENUMERATION SHOOT RESULT
# ---------------------------------------------------------------------------------------
class ShootResult(Enum):

    """
        ---------------------------------------------------------------------------------
        This enumeration defines the possible types of shooting results that can be produced 
        when shooting into given coordinates. 
        ---------------------------------------------------------------------------------
    """

    BAD_Y_COORDINATE = -102
    BAD_X_COORDINATE = -101
    UNINITIALIZED_BOARD = -100
    CARRIER = 5
    BATTLESHIP = 4
    CRUISE = 3
    SUBMARINE = 3
    DESTROYER = 2
    NOTHING = 0
    BOMBED = -1


# ---------------------------------------------------------------------------------------
# CLASS BOARD
# ---------------------------------------------------------------------------------------
class Board:

    """
        ---------------------------------------------------------------------------------
        Represents a board within a game. Boards are serialized into json objects and 
        persisted into REDIS key-value store so that it can be fetched when required.
        Each board is persisted using the following key construction mechanism:
        
        key: '[game_id]:[player_id]'
        value: {
            remaining_points: 12
            board:[
                 [0,0,0,5,5,5,5,5,0,0], 
                 [2,2,0,0,0,0,0,0,0,0], 
                 [0,0,1,0,0,0,4,0,0,0],
                 [0,0,0,0,0,0,4,0,0,0],
                 [0,0,0,0,0,0,4,0,0,0],
                 [0,0,0,0,0,0,4,0,0,0],
                 [0,0,2,0,1,0,0,0,0,0],
                 [0,0,2,0,0,0,0,0,3,0],
                 [0,0,0,0,0,0,0,0,3,0],
                 [3,3,3,0,0,0,0,0,3,0]
             ]
        }
                 
        This will only serialize an integer matrix that represents the board. The
        boats are represented as integers with a scalar value that corresponds to
        the size of the boat they form part of. This class will provide an interface
        with several methods that will allow easy interaction with the board and
        perform operations such as shooting and updating the board's state as 
        operations are performed to the board instance. 
        ---------------------------------------------------------------------------------
    """

    # -----------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # -----------------------------------------------------------------------------------

    __board = []
    __game_id = ""
    __player_id = ""
    __board_id = ""
    __persistence_provider = None

    # -----------------------------------------------------------------------------------
    # CONSTRUCTOR METHOD
    # -----------------------------------------------------------------------------------
    def __init__(self, player_id, game_id, persistence_provider):
        """
            -----------------------------------------------------------------------------
            Creates instances of Board class
            :param player_id: The id of the owner of the board
            :param game_id:  The if of the game
            -----------------------------------------------------------------------------
        """
        self.__player_id = player_id
        self.__game_id = game_id
        self.__board_id = self.__build_id()
        self.__persistence_provider = persistence_provider

    # -----------------------------------------------------------------------------------
    # METHOD SAVE
    # -----------------------------------------------------------------------------------
    def save(self):

        """
            Takes the current state of the board and saves it into the redis data structure 
            store. If the key already exists, then it updates its value. This method is used
            to create a board as well as an update method. 
            :return: Nothing
        """

        self.__persistence_provider.set(self.__board_id, self.json())

    # -----------------------------------------------------------------------------------
    # METHOD JSON
    # -----------------------------------------------------------------------------------
    def json(self):
        """
            This method get the current board state as a json string
            :return: json string representation of the current board status
        """
        return json.dumps(self.export_state())

    # -----------------------------------------------------------------------------------
    # METHOD BUILD ID
    # -----------------------------------------------------------------------------------
    def __build_id(self):
        """
            -----------------------------------------------------------------------------
            Computes the board's id value from the given player_id and game_id
            :return: string
            -----------------------------------------------------------------------------
        """
        return "" + self.__game_id + "+" + self.__player_id

    # -----------------------------------------------------------------------------------
    # GET PLAYER ID METHOD
    # -----------------------------------------------------------------------------------
    def get_player_id(self):

        """
            -----------------------------------------------------------------------------
            Gets the player_id of the player that owns this board
            :return: Uuid of the user owning the board
            -----------------------------------------------------------------------------
        """
        return self.__player_id

    # -----------------------------------------------------------------------------------
    # GET OWNER ID METHOD
    # -----------------------------------------------------------------------------------
    def get_owner_id(self):
        """
            -----------------------------------------------------------------------------
            Gets the id of the user that owns the player that owns this board
            :return: Uuid of the user that owns the player that owns this board
            -----------------------------------------------------------------------------
        """
        player = Player(None, None, self.__persistence_provider)
        player.load(self.__player_id)
        return player.get_owner()

    # -----------------------------------------------------------------------------------
    # GET GAME ID
    # -----------------------------------------------------------------------------------
    def get_game_id(self):
        """
            -----------------------------------------------------------------------------
            Gets the game to where the current board belongs
            :return:  uuid of the game to where the current board belongs
            -----------------------------------------------------------------------------
        """
        return self.__game_id

    # -----------------------------------------------------------------------------------
    # METHOD EXPAND
    # -----------------------------------------------------------------------------------
    def expand(self):
        """
            -----------------------------------------------------------------------------
            This method is used to expand a board for the first time and initialize all 
            its possible positions. 
            
            :return: None
            -----------------------------------------------------------------------------
        """
        self.__board = create_board()
        return

    # -----------------------------------------------------------------------------------
    # EXPORT_STATE METHOD
    # -----------------------------------------------------------------------------------
    def export_state(self):
        """
            -----------------------------------------------------------------------------
            :return: dictionary containing current game's state. This can be serialized 
                     into a json string in order to persist the state on a redis instance. 
            -----------------------------------------------------------------------------
        """
        state = {
            "player_id": self.__player_id,
            "game_id": self.__game_id,
            "board_id": self.__board_id,
            "board": self.__board,
            "size": len(self.__board)
        }
        return state

    # -----------------------------------------------------------------------------------
    # LOAD METHOD
    # -----------------------------------------------------------------------------------
    def load(self, board_data):

        """
            -----------------------------------------------------------------------------
            Given a json string that contains a persistent state of a board, deserializes
            it into a dictionary and reads all the properties in order to load board state
            into current class instance so updating the board's state can be done using the
            class' API abstraction. 
            
            :param board_data: json string containing the representation of the board's state
            :return: None
            -----------------------------------------------------------------------------
        """

        if board_data is not None:
            board_state = json.loads(board_data)
            size = board_state['size']
            for y in range(0, size):
                self.__board.append([])
                for x in range(0, size):
                    self.__board[y][x].append(board_state['board'][y][x])
            self.__player_id = board_state['player_id']
            self.__board_id = board_state['board_id']
            self.__game_id = board_state['game_id']

    # -----------------------------------------------------------------------------------
    # METHOD SHOOT
    # -----------------------------------------------------------------------------------
    def shoot(self, x, y):
        """
            -----------------------------------------------------------------------------
            Given two coordinate components (X, Y) this method will emulate a shooting
            in the given coordinates if the coordinates are within the valid range.
            :param x: The X coordinate of the point within the matrix where a bomb is
                      going to be sent.
            :param y: The y coordinate of the point within the matrix where a bomb is
                      going to be sent.
                      
            :return: Returns the ShootResult value corresponding to the 
            -----------------------------------------------------------------------------
        """
        result = 0
        # Check that board has been initialized correctly and elements have been loaded
        if self.__board is not None and len(self.__board) > 0:
            if len(self.__board) > y:
                if len(self.__board[x]) > x:
                    result = self.__board[y][x]
                    if result > 0:
                        self.__board[y][x] = int(ShootResult.BOMBED)
                else:
                    # Return invalid X coordinate
                    result = int(ShootResult.BAD_X_COORDINATE)
            else:
                # Return invalid Y coordinate
                result = int(ShootResult.BAD_Y_COORDINATE)
        else:
            # Return invalid coordinates code.
            result = int(ShootResult.UNINITIALIZED_BOARD)
        return result
