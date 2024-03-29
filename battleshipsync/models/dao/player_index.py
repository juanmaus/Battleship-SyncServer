from battleshipsync import redis_store as redis
from battleshipsync.models.board import Board
from battleshipsync import app
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
        players = json.loads(players_data.decode('utf-8'))
    players.append(player)
    redis.set('players', json.dumps(players))
    # Now we create a board for the player once it has been registered on a game
    board = Board(
        player_id=player['player_id'],
        game_id=player['game_id'],
        board_id=player['board_id'],
        persistence_provider=redis
    )
    board.expand()
    board.save()
    # Release the memory allocation to keep low overhead
    board = None
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
        app.logger.info('Reading players data... for player: [' + player_id + '] with user: ['+user_id+']')
        players = json.loads(players_data)
        app.logger.info('Players loaded... List: ' + json.dumps(players))
    try:
        for player in players:
            if player['player_id'] == player_id and player['user_id'] == user_id:
                return True
        return False
    except:
        return False

def update_player_index(player_id, player_info):
    """
        Updates the persistence provider, removing a spot from it

        :param player_id: Player id
        :param player_info: full static metadata of a player
        :return: True if game was successfully updated
    """
    players_data = redis.get('players')
    players = []
    newplayers = []
    # If there are no games, then we create an empty list
    if players_data is not None:
        players = json.loads(players_data.decode('utf-8'))
        key = None
        try:
            for player in players:
                if player_id == player["player_id"]:
                    newplayers.append(player_info)
                else:
                    newplayers.append(player)
        except:
            return False
    redis.set('players', json.dumps(newplayers))
    players = None
    newplayers = None
    return True

