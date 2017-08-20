from battleshipsync import redis_store as persistence_provider
from battleshipsync.models.game import Game
import json


# ---------------------------------------------------------------------------------------
# METHOD REGISTER GAME
# ---------------------------------------------------------------------------------------
def register_game(game):
    """
        We keep a list of games in our persistence_provider in order to check things open spots in game
        and to be able to enumerate all known games. This
        game
        persistence_provider key serves as an index
        :param game: Dictionary of game
        :return: True game was successfully registered
    """
    games_data = persistence_provider.get('games')
    games = []
    # If there are no games, then we create an empty list
    if games_data is not None:
        games = json.loads(games_data)
    games.append(game)
    persistence_provider.set('games', json.dumps(games, sort_keys=False, indent=2))
    games = None
    return True


def add_player(game_id, player_id, player_type):
    """
        Adds a player to the game in the game dictionary
        Also, has the logic to change the game status when game is filled

        :param game_id: gameId
        :param player_type: a player_type
        :param player_id: a player_id
        :return: True game was successfully added
    """
    game = Game(None, None, persistence_provider=persistence_provider)  # instance as null to later load from id
    game.load(game_id)
    if game.join_player(player_id=player_id):
        update_open_spots(game_id=game_id, player_type=player_type)
        return True
    else:
        return False


def update_open_spots(game_id, player_type):
    """
        Updates the persistence provider, removing a spot from it

        :param game_id: Game id
        :param player_type: a type of player
        :return: True if spot is successful remove, False is no open spot available
    """
    games_data = persistence_provider.get('games')
    games = []
    newgames = []
    # If there are no games, then we create an empty list
    if games_data is not None:
        games = json.loads(games_data)
        key = None
        try:
            for game in games:
                if game_id == game["game_id"]:
                    key = get_key_in_list(game["open_spots"], player_type)
                    if key is not None:
                        del game["open_spots"][key]
                        newgames.append(game)
                    else:
                        return False
                else:
                    newgames.append(game)
        except:
            return False
    persistence_provider.set('games', json.dumps(newgames))
    games = None
    newgames = None
    return True

def get_key_in_list(spots, match):
  for index, spot in enumerate(spots):
        if spot == match:
            return index

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

def __find_game(game_id, games):
    for game in games:
        if game_id == game['game_id']:
            return game
    return None
