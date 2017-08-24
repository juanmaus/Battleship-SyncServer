from enum import Enum
from flask import json
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
    # CLASS ATTRIBUTES
    # -----------------------------------------------------------------------------------

    __game_id = ""
    __persistence_provider = None

    # -----------------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------------------------------------
    def __init__(self, mode, player_layout, persistence_provider):
        """
            :param mode: GameMode type. Can be 4PLAYER mode or 2PLAYER mode
            :param player_layout: A list of the player types that can join the game.
        """
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.datetime.now()
        self.game_status = GameStatus.WAITING_FOR_PLAYERS
        self.owner = ""
        self.moves_next = ""
        self.mode = mode
        self.player_layout = player_layout
        self.players = []
        self.__persistence_provider = persistence_provider

    # -----------------------------------------------------------------------------------
    # METHOD SAVE
    # -----------------------------------------------------------------------------------
    def save(self):
        """
            Takes the current state of the game and saves it into the redis data structure
            store. If the key already exists, then it updates its value. This method is used
            to create a game as well as an update method.
            :return: Nothing
        """
        if self.__persistence_provider is not None:
            self.__persistence_provider.set(self.id, self.json())
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD JSON
    # -----------------------------------------------------------------------------------
    def json(self):
        """
            This method gets the game state as a json string
            :return: json string representation of the current game status
        """
        return json.dumps(self.export_state())

    # -----------------------------------------------------------------------------------
    # METHOD JOIN PLAYER
    # -----------------------------------------------------------------------------------
    def join_player(self, player_id, player_type):
        if player_id in self.players or player_type not in self.player_layout:
            return False

        if self.first_join():
            self.owner = player_id
            self.moves_next = player_id
        self.player_layout.remove(player_type)
        self.players.append(player_id)

        if self.last_join():
            self.game_status = GameStatus.ACTIVE


        self.save()
        return True


    # -----------------------------------------------------------------------------------
    # METHOD CHECK FIRST JOIN
    # -----------------------------------------------------------------------------------
    def first_join(self):
        """
            This method gets if the game has no current players
            :return: Bool true if the player count is 0
        """
        if len(self.players) == 0:
            return True
        else:                   #Redundant else but legible blablabla..
            return False

    # -----------------------------------------------------------------------------------
    # METHOD CHECK LAST JOIN
    # -----------------------------------------------------------------------------------
    def last_join(self):
        """
            This method gets if the game has reached the player limit
            :return: Bool true if the player layout count is 0
        """
        if len(self.player_layout) == 0:
            return True
        else:  # Redundant else but legible blablabla..
            return False

    # -----------------------------------------------------------------------------------
    # METHOD REGISTER
    # -----------------------------------------------------------------------------------
    def register(self):
        from battleshipsync.models.dao.game_index import register_game
        """
            Registers a new game on a game index for filtering purposes
            :return: True if the player was registered successfully
        """
        if self.save():
            return register_game(self.static_metadata())
        return False

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
            "id": self.id,
            "timestamp": str(self.timestamp),
            "game_status": str(self.game_status),
            "mode": str(self.mode),
            "owner": self.owner,
            "moves_next": self.moves_next,
            "player_layout": self.player_layout,
            "players": self.players
        }
        return state

    # -----------------------------------------------------------------------------------
    # METHOD STATIC METADATA
    # -----------------------------------------------------------------------------------
    def static_metadata(self):
        """
            Returns a dictionary with the current game's state so it can be serialized
            and persisted.
            :return: dictionary with current instance of game state
        """
        return {
            "game_id": self.id,
            "mode": str(self.mode),
            "open_spots": self.player_layout,
            "game_status": str(self.game_status),
            "moves_next": self.moves_next,
            "players": self.players
        }

    # -----------------------------------------------------------------------------------
    # LOAD METHOD
    # -----------------------------------------------------------------------------------
    def load(self, game_id):

        """
            -----------------------------------------------------------------------------
            Given a game id, which loads from redis a json string that contains a persistent
            state of a game, deserializes  it into a dictionary and reads all the properties
            in order to load board state into current class instance so updating the games's
            state can be done using the class' API abstraction.

            :param game_id: game id
            :return: None
            -----------------------------------------------------------------------------
        """
        redis_data = self.__persistence_provider.get(game_id)
        if redis_data is None:
            return None

        game_data = json.loads(redis_data)
        if game_data is not None:
            self.id = game_data['id']
            self.timestamp = game_data['timestamp']
            self.game_status = game_data['game_status']
            self.mode = game_data['mode']
            self.owner = game_data['owner']
            self.moves_next = game_data['moves_next']
            self.player_layout = game_data['player_layout']
            self.players = game_data['players']
            return 0
        else:
            return None
