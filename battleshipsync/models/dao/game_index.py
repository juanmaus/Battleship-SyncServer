from battleshipsync import redis_store as persistence_provider
from battleshipsync.models.game import Game
from itertools import cycle
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
    persistence_provider.set('games', json.dumps(games))
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
    if game.join_player(player_id=player_id, player_type=player_type):
        update_game_index(game_id=game_id, gameinfo=game.static_metadata())
        return True
    else:
        return False


def move_to_next_player(game_id):
    """
        Updates a game(entity and DAO) to move to the next player

        :param game_id: gameId
        :return: Next player id to move or None if error
    """
    game = Game(None, None, persistence_provider=persistence_provider)  # instance as null to later load from id
    game.load(game_id)

    pool = cycle(game.players)
    for player in pool:
        if player == game.moves_next:
            game.moves_next = next(pool)
            break

    if game.save():
        update_game_index(game_id=game_id, gameinfo=game.static_metadata())
        return True
    else:
        return False

def update_game_index(game_id, gameinfo):
    """
        Updates the persistence provider, removing a spot from it

        :param game_id: Game id
        :param gameinfo: full static metadata of a game
        :return: True if game was successfully updated
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
                    newgames.append(gameinfo)
                else:
                    newgames.append(game)
        except:
            return False
    persistence_provider.set('games', json.dumps(newgames))
    games = None
    newgames = None
    return True






