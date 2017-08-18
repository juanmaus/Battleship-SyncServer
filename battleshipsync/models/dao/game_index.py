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


def add_player(game_id,player_type):
    """
        Adds a player to the game in the game dictionary
        Also, has the logic to change the game status when game is filled

        :param game: gameId
        :param player: a playerId
        :return: True game was successfully registered
    """
    games_data = redis.get('games')
    games = []
    newgames= []
    # If there are no games, then we create an empty list
    if games_data is not None:
        games = json.loads(games_data)
        key= None
        try:
            for game in games:
                if game_id == game["game_id"]:
                    key = __get_key_in_list(game["open_spots"], player_type)
                    if key is not None:
                        del game["open_spots"][key]
                    else:
                        return False
                    newgames.append(game)
                else:
                    newgames.append(game)
        except:
            return False
    games.append(game)
    redis.set('games', json.dumps(games))
    games = None
    return json.dumps(newgames, indent=4, sort_keys=True)

def __get_key_in_list(spots,match):     #Maybe needs to be redefined somewhere else, dunno
    for index, spot in enumerate(spots):
        print("huehuehe"+spot)
        if spot == match:
            return index