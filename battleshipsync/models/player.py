from battleshipsync.models.board import ShootResult
from battleshipsync.models.dao.player_index import register_player
from enum import Enum
import json
import uuid


# ---------------------------------------------------------------------------------------
# ENUMERATION PLAYER TYPE
# ---------------------------------------------------------------------------------------
class PlayerType(Enum):
    """
        Determines the types of player available in the game. The human type is to be 
        used on a game client interface and the computer type is to be used by autonomous 
        program that connects to the server and plays automatically without any human 
        intervention.
    """
    HUMAN = 1
    COMPUTER = 2


# ---------------------------------------------------------------------------------------
# CLASS PLAYER
# ---------------------------------------------------------------------------------------
class Player:
    """
         A player establishes a relationship between a user of the game and an specific
         instance of Game. The player model has the responsibility of keeping player's
         scores such as the amount of points gained and the amount of fleet value 
         remaining in his board. Player also stores the associated nickname with a player
    """

    # -----------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # -----------------------------------------------------------------------------------

    __player_id = ""
    __user_id = None
    __game_id = None
    __points_gained = 0
    __current_fleet_value = 0
    __nick_name = ""
    __alive = None
    __redis = None

    # -----------------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------------------------------------
    def __init__(self, user_id, game_id, redis):
        """
            To create an instance of player it is only necessary to provide the id of the 
            game and the id of the user who owns the player's instance. 
            :param user_id: 
            :param game_id: 
        """
        self.__user_id = user_id
        self.__game_id = game_id
        self.__player_id = str(uuid.uuid4())

    # -----------------------------------------------------------------------------------
    # METHOD REGISTER
    # -----------------------------------------------------------------------------------
    def register(self, nickname):
        """
            Registers a new player on a given game instance
            :param nickname: The nickname that the player will be using
            :return: True if the player was registered successfully
        """
        self.__nick_name = nickname
        carrier = int(ShootResult.CARRIER)
        cruise = int(ShootResult.CRUISE)
        destroyer = int(ShootResult.DESTROYER)
        submarine = int(ShootResult.SUBMARINE)
        battleship = int(ShootResult.BATTLESHIP)
        self.__current_fleet_value = carrier + destroyer + cruise + submarine + battleship
        self.__points_gained = 0
        self.__alive = True
        if self.save():
            register_player(self.static_metadata())

    # -----------------------------------------------------------------------------------
    # METHOD EXPORT STATE
    # -----------------------------------------------------------------------------------
    def export_state(self):
        """
            Returns a dictionary with the current player's state so it can be serialized
            and persisted.
            :return: dictionary with current instance of player state
        """
        return {
            "player_id": self.__player_id,
            "user_id": self.__user_id,
            "game_id": self.__game_id,
            "points_gained": self.__points_gained,
            "current_fleet_value": self.__current_fleet_value,
            "nickname": self.__nick_name,
            "alive": self.__alive
        }

    # -----------------------------------------------------------------------------------
    # METHOD STATIC METADATA
    # -----------------------------------------------------------------------------------
    def static_metadata(self):
        """
            Returns a dictionary with the current player's state so it can be serialized
            and persisted.
            :return: dictionary with current instance of player state
        """
        return {
            "player_id": self.__player_id,
            "user_id": self.__user_id,
            "game_id": self.__game_id,
            "nickname": self.__nick_name,
        }

    # -----------------------------------------------------------------------------------
    # METHOD JSON
    # -----------------------------------------------------------------------------------
    def json(self):
        """
            Creates a json string representation of current instance of player. 
            :return: json string
        """
        return json.dumps(self.export_state())

    # -----------------------------------------------------------------------------------
    # METHOD LOAD
    # -----------------------------------------------------------------------------------
    def load(self, player_id):
        """
            Loads an instance of player with the data retrieved from redis in case the 
            player_id provided is valid 
            :param player_id: The player's id
            :return: True if loaded and false if not loaded
        """
        if self.__redis is not None and player_id is not None:
            player_data = self.__redis.get(player_id)
            player = json.loads(player_data)
            self.__player_id = player_id
            self.__nick_name = player['nickname']
            self.__current_fleet_value = player['current_fleet_value']
            self.__points_gained = player['points_gained']
            self.__game_id = player['game_id']
            self.__user_id = player['user_id']
            self.__alive = player['alive']
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD SAVE
    # -----------------------------------------------------------------------------------
    def save(self):
        """
            Persists current player's state into the REDIS Store  
            :param redis: reference to redis store client instance
            :return: 
        """
        if self.__redis is not None:
            self.__redis.set(self.__player_id, self.json())
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD IS OWNED BY
    # -----------------------------------------------------------------------------------
    def is_owned_by(self, user_id):
        """
            Determines if current instance of player is owned by the given user_id
            :param user_id: The user id of the challenger
            :return: True if it is
        """
        if user_id == self.__user_id:
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD UPLOAD FLEET VALUE
    # -----------------------------------------------------------------------------------
    def update_fleet_value(self, amount):
        """
            Updates the current player's fleet value when someone shoots to his/her board 
            and hits one of his ships.
            :param amount: The amount of damage received in terms of fleet value
            :return: True if updated successfully 
        """
        if self.__current_fleet_value >= amount:
            self.__current_fleet_value = (self.__current_fleet_value - amount)
            if self.__current_fleet_value is 0:
                self.__alive = False
            return self.save()
        return False

    # -----------------------------------------------------------------------------------
    # METHOD ADD POINTS
    # -----------------------------------------------------------------------------------
    def add_points(self, amount):
        """
            Updates current player's amount of points gained
            :param amount: the amount of points that should be added to current points
            :return: True if updated the points and False if couldn't
        """
        self.__points_gained = (self.__points_gained + amount)
        return self.save()
