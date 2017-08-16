from battleshipsync import redis_store as redis
import json


# ---------------------------------------------------------------------------------------
# METHOD REGISTER GAME
# ---------------------------------------------------------------------------------------
def register_game(game):
    """
        We keep a list of games in our redis in order to check things open spots in gamep
        and to be able to enumerate all known games. This
        Redis key serves as an index 
        
        :param game: Dictionary of game
        :return: True game was successfully registered
    """
    games_data = redis.get('games')
    games = []
    # If there are no games, then we create an empty list
    if games_data is not None:
        games = json.loads(games_data)
    games.append(game)
    redis.set('games', json.dumps(games))
    games = None
    return True


# ---------------------------------------------------------------------------------------
# CLASS PLAYER
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
