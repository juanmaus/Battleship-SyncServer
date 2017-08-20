from battleshipsync import redis_store as redis
from battleshipsync.models.player import Player
import json


# ---------------------------------------------------------------------------------------
# METHOD REGISTER PLAYER
# ---------------------------------------------------------------------------------------
def register_player(player):
    """
        We keep a list of player in our redis in order to check things like ownership
        between player and user and to be able to enumerate all known players. This
        Redis key serves as an index 
        
        :param player: Dictionary of player
        :return: True player was successfully registered
    """
    players_data = redis.get('players')
    players = []
    # If there are no players, then we create an empty list
    if players_data is not None:
        players = json.loads(players_data)
    players.append(player)
    redis.set('players', json.dumps(players))
    # Release the memory allocation to keep low overhead
    players = None
    return True


# ---------------------------------------------------------------------------------------
# FUNCTION VERIFY OWNERSHIP
# ---------------------------------------------------------------------------------------
def verify_ownership(player_id, user_id):
    """
        Checks on the players index if a given player id is owned by the given user id. 
        :param player_id: The id of the player
        :param user_id:  The user who supposedly owns the given player id
        :return: 
    """
    players_data = redis.get('players')
    players = []
    # If there are no players, then we create an empty list
    if players_data is not None:
        players = json.loads(players_data)
    try:
        for player in players:
            if player['player_id'] is player_id and player['user_id'] is user_id:
                return True
        return False
    except:
        return False


# ---------------------------------------------------------------------------------------
# FUNCTION CLASS PLAYER
# ---------------------------------------------------------------------------------------
def get_player(player_id):
    player_data = redis.get(player_id)
    if player_data is not None:
        player = Player(None, None, redis)
        player.load()
        return player
    return None
