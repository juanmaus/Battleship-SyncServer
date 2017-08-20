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


def move_to_next_player(game_id):
    """
        Updates a game to move to the next player to play

        :param game: gameId
        :return: Next player id to move or None if error
    """
    games_data = redis.get('games')
    if not games_data:
        return None

    games = json.loads(games_data)
    game = __find_game(game_id, games)

    if not game:
        return None

    current_player = game["moves_next"]
    current_player_index = game["players"].index(current_player)
    last_index_of_players = len(game["players"]) - 1
    next_player_index = (current_player_index + 1) if current_player_index < last_index_of_players else 0
    next_player = game["players"][next_player_index]
    game["moves_next"] = next_player

    redis.set('games', json.dumps(games))

    return next_player

def __get_key_in_list(spots,match):     #Maybe needs to be redefined somewhere else, dunno
    for index, spot in enumerate(spots):
        print("huehuehe"+spot)
        if spot == match:
            return index

def __find_game(game_id, games):
    for game in games:
        if game_id == game['game_id']:
            return game

    return None
