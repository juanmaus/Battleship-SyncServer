from battleshipsync.models.dao.player_index import register_player
import json
import uuid


# ---------------------------------------------------------------------------------------
# CLASS PLAYER
# ---------------------------------------------------------------------------------------
class Player:

    """
        -----------------------------------------------------------------------------
         A player establishes a relationship between a user of the game and an specific
         instance of Game. The player model has the responsibility of keeping player's
         scores such as the amount of points gained and the amount of fleet value 
         remaining in his board. Player also stores the associated nickname with a player
         -----------------------------------------------------------------------------
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
    __is_human = False
    __persistence_provider = None

    # -----------------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------------------------------------
    def __init__(self, user_id, game_id, persistence_provider):
        """
            -----------------------------------------------------------------------------
            To create an instance of player it is only necessary to provide the id of the 
            game and the id of the user who owns the player's instance. 
            :param user_id: 
            :param game_id: 
            -----------------------------------------------------------------------------
        """
        self.__user_id = user_id
        self.__game_id = game_id
        self.__player_id = str(uuid.uuid4())
        self.__persistence_provider = persistence_provider

    # -----------------------------------------------------------------------------------
    # METHOD HUMAN
    # -----------------------------------------------------------------------------------
    def human(self):
        """
            -----------------------------------------------------------------------------
            Checks if the player is human or computer
            :return: True if it is human player, false if it is a computer player.
            -----------------------------------------------------------------------------
        """
        if self.__is_human:
            return "HUMAN"
        else:
            return "COMPUTER"

    # -----------------------------------------------------------------------------------
    # METHOD REGISTER
    # -----------------------------------------------------------------------------------
    def register(self, nickname, is_human):
        """
            -----------------------------------------------------------------------------
            Registers a new player on a given game instance
            :param is_human: Used to determined if the player is a computer or human
            :param nickname: The nickname that the player will be using
            :return: True if the player was registered successfully
            -----------------------------------------------------------------------------
        """
        from battleshipsync.models.dao.game_index import add_player
        from battleshipsync.models.board import ShootResult
        self.__nick_name = nickname
        carrier = int(ShootResult.CARRIER.value)
        battleship = int(ShootResult.BATTLESHIP.value)
        cruise = int(ShootResult.CRUISE.value)
        submarine = int(ShootResult.SUBMARINE.value)
        destroyer = int(ShootResult.DESTROYER.value)

        self.__current_fleet_value = carrier + destroyer + (cruise * 2) + submarine + battleship
        self.__points_gained = 0
        self.__alive = True
        self.__is_human = is_human
        if self.save() and add_player(self.__game_id, self.__player_id, self.human()):
            return register_player(self.static_metadata())
        return False

    # -----------------------------------------------------------------------------------
    # METHOD EXPORT STATE
    # -----------------------------------------------------------------------------------
    def export_state(self):
        """
            -----------------------------------------------------------------------------
            Returns a dictionary with the current player's state so it can be serialized
            and persisted.
            :return: dictionary with current instance of player state
            -----------------------------------------------------------------------------
        """
        return {
            "player_id": self.__player_id,
            "user_id": self.__user_id,
            "game_id": self.__game_id,
            "points_gained": self.__points_gained,
            "current_fleet_value": self.__current_fleet_value,
            "nickname": self.__nick_name,
            "alive": self.__alive,
            "is_human": self.__is_human
        }

    # -----------------------------------------------------------------------------------
    # METHOD STATIC METADATA
    # -----------------------------------------------------------------------------------
    def static_metadata(self):
        """
            -----------------------------------------------------------------------------
            Returns a dictionary with the current player's state so it can be serialized
            and persisted.
            :return: dictionary with current instance of player state
            -----------------------------------------------------------------------------
        """
        return {
            "player_id": self.__player_id,
            "user_id": self.__user_id,
            "game_id": self.__game_id,
            "nickname": self.__nick_name,
            "is_human": self.__is_human
        }

    # -----------------------------------------------------------------------------------
    # METHOD JSON
    # -----------------------------------------------------------------------------------
    def json(self):
        """
            -----------------------------------------------------------------------------
            Creates a json string representation of current instance of player. 
            :return: json string
            -----------------------------------------------------------------------------
        """
        return json.dumps(self.export_state())

    # -----------------------------------------------------------------------------------
    # METHOD LOAD
    # -----------------------------------------------------------------------------------
    def load(self, player_id):
        """
            -----------------------------------------------------------------------------
            Loads an instance of player with the data retrieved from redis in case the 
            player_id provided is valid 
            :param player_id: The player's id
            :return: True if loaded and false if not loaded
            -----------------------------------------------------------------------------
        """
        if self.__persistence_provider is not None and player_id is not None:
            player_data = self.__persistence_provider.get(player_id)
            player = json.loads(player_data)
            self.__player_id = player_id
            self.__nick_name = player['nickname']
            self.__current_fleet_value = player['current_fleet_value']
            self.__points_gained = player['points_gained']
            self.__game_id = player['game_id']
            self.__user_id = player['user_id']
            self.__alive = player['alive']
            self.__is_human = player['is_human']
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD GET OWNER
    # -----------------------------------------------------------------------------------
    def get_owner(self):
        """
            -----------------------------------------------------------------------------
            Gets the owner of the player. 
            :return: 
            -----------------------------------------------------------------------------
        """
        return self.__user_id
        
    # -----------------------------------------------------------------------------------
    # METHOD GET PLAYER ID
    # -----------------------------------------------------------------------------------
    def get_player_id(self):
        """
            -----------------------------------------------------------------------------
            Gets the id of the player. 
            :return: 
            -----------------------------------------------------------------------------
        """
        return self.__player_id
        
    # -----------------------------------------------------------------------------------
    # METHOD GET GAME ID
    # -----------------------------------------------------------------------------------
    def get_game_id(self):
        """
            -----------------------------------------------------------------------------
            Gets the id of the game. 
            :return: 
            -----------------------------------------------------------------------------
        """
        return self.__game_id

    # -----------------------------------------------------------------------------------
    # METHOD SAVE
    # -----------------------------------------------------------------------------------
    def save(self):
        """
            -----------------------------------------------------------------------------
            Persists current player's state into the REDIS Store  
            :param redis: reference to redis store client instance
            :return: 
            -----------------------------------------------------------------------------
        """
        if self.__persistence_provider is not None:
            self.__persistence_provider.set(self.__player_id, self.json())
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD IS OWNED BY
    # -----------------------------------------------------------------------------------
    def is_owned_by(self, user_id):
        """
            -----------------------------------------------------------------------------
            Determines if current instance of player is owned by the given user_id
            :param user_id: The user id of the challenger
            :return: True if it is
            -----------------------------------------------------------------------------
        """
        if user_id == self.__user_id:
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD UPLOAD FLEET VALUE
    # -----------------------------------------------------------------------------------
    def update_fleet_value(self, amount):
        """
            -----------------------------------------------------------------------------
            Updates the current player's fleet value when someone shoots to his/her board 
            and hits one of his ships.
            :param amount: The amount of damage received in terms of fleet value
            :return: True if updated successfully 
            -----------------------------------------------------------------------------
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
            -----------------------------------------------------------------------------
            Updates current player's amount of points gained
            :param amount: the amount of points that should be added to current points
            :return: True if updated the points and False if couldn't
            -----------------------------------------------------------------------------
        """
        self.__points_gained = (self.__points_gained + amount)
        return self.save()
