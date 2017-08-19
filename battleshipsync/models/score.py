from battleshipsync.models.board import ShootResult
from battleshipsync.models.dao.player_index import register_player
import json
import uuid


# ---------------------------------------------------------------------------------------
# CLASS PLAYER
# ---------------------------------------------------------------------------------------
class Score:
    """
         A Score represents the final score obtained by a Player after a game has ended.
    """

    # -----------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # -----------------------------------------------------------------------------------

    __score_id = ""
    __player_id = None
    __value = 0
    __persistence_provider = None

    # -----------------------------------------------------------------------------------
    # CLASS CONSTRUCTOR
    # -----------------------------------------------------------------------------------
    def __init__(self, player_id, value, persistence_provider):
        """
            In order to create an instance of Score, we only need to know the player_id
            and the value of the score.
            :param user_id: 
            :param game_id: 
        """
        self.__score_id = str(uuid.uuid4())
        self.__player_id = player_id
        self.__value = value
        self.__persistence_provider = persistence_provider

    # -----------------------------------------------------------------------------------
    # METHOD EXPORT STATE
    # -----------------------------------------------------------------------------------
    def export_state(self):
        """
            Returns a dictionary with the current score's state so it can be serialized
            and persisted.
            :return: dictionary with current instance of score state
        """
        return {
            "score_id": self.__score_id,
            "player_id": self.__player_id,
            "value": self.__value,
        }

    # -----------------------------------------------------------------------------------
    # METHOD STATIC METADATA
    # -----------------------------------------------------------------------------------
    def static_metadata(self):
        """
            Returns a dictionary with the current player's state so it can be serialized
            and persisted.
            :return: dictionary with current instance of player state
            TODO: Indentify if this method does the same as the export_state, is not clear
        """
        return {
            "score_id": self.__score_id,
            "player_id": self.__player_id,
            "value": self.__value,
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
    def load(self, score_id):
        """
            Loads an instance of score with the data retrieved from redis in case the 
            score_id provided is valid 
            :param score_id: The score's id
            :return: True if loaded and false if not loaded
            TODO: I don't see any reason to keep this method. Please consider removal.
        """
        if self.__persistence_provider is not None and score_id is not None:
            score_data = self.__persistence_provider.get(score_id)
            score = json.loads(score_data)
            self.__score_id = score_id
            self.__player_id = player['player_id']
            self.__value = player['value']
            return True
        return False

    # -----------------------------------------------------------------------------------
    # METHOD SAVE
    # -----------------------------------------------------------------------------------
    def save(self):
        """
            Persists current score's state into the REDIS Store  
            :param redis: reference to redis store client instance
            :return: 
        """
        if self.__persistence_provider is not None:
            self.__persistence_provider.set(self.__score_id, self.json())
            return True
        return False