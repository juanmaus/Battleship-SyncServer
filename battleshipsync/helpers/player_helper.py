from battleshipsync import redis_store as redis
from battleshipsync.models.player import Player


# ---------------------------------------------------------------------------------------
# FUNCTION GET PLAYER
# ---------------------------------------------------------------------------------------
def get_player(player_id):
    """
        Searches the REDIS index and loads the instance of player associated to
        the given player id.
        :param player_id: The id of the player to load
    """
    player_data = redis.get(player_id)
    if player_data is not None:
        player = Player(None, None, redis)
        player.load(player_id)
        return player
    return None