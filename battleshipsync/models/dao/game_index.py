from battleshipsync import redis_store as persistence_provider
import json


# ---------------------------------------------------------------------------------------
# METHOD REGISTER GAME
# ---------------------------------------------------------------------------------------
def register_game(game):
    """
        We keep a list of games in our persistence_provider in order to check things open spots in game
        and to be able to enumerate all known games. This
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
    persistence_provider.set('games', json.dumps(games))
    games = None
    return True


def add_player(game_id, player_type):
    """
        Adds a player to the game in the game dictionary
        Also, has the logic to change the game status when game is filled

        :param game_id: gameId
        :param player_type: a player_type
        :return: True game was successfully added
    """
    # game = Game(None, None, persistence_provider=persistence_provider)  # instance as null to later load from id
    # game.load(game_id)
    update_open_spots(game_id=game_id, player_type=player_type)


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
                    else:
                        return False
                    newgames.append(game)
                else:
                    newgames.append(game)
        except:
            return False
    games.append(game)
    persistence_provider.set('games', json.dumps(games))
    games = None
    return True


def get_key_in_list(spots, match):
    for index, spot in enumerate(spots):
        if spot == match:
            return index