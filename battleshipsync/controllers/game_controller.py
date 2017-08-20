from http import HTTPStatus
from battleshipsync import app, redis_store
from flask import request, jsonify, json
from battleshipsync import redis_store
from battleshipsync.extensions.jsonp import enable_jsonp
from battleshipsync.extensions.error_handling import ErrorResponse
from battleshipsync.models.dao.game_index import add_player
from battleshipsync.models.game import Game, GameStatus, GameMode
from flask_jwt import jwt_required, current_identity


# --------------------------------------------------------------------------
# POST GAME
# --------------------------------------------------------------------------
# Creates a new game with the given parameters specified in the json body
@app.route('/api/v1/game', methods=['POST'])
@jwt_required()
def post_game():
    game_data = request.get_json()
    mode = game_data['mode']
    layout = game_data['player_layout']
    if game_data is not None and layout is not None:
        game = Game(mode=mode, player_layout=layout, persistence_provider=redis_store)
        if game.register():
            # app.logger.info('Game with ID: \'' + game.id + '\' was created by user ' + str(current_identity.username )+' mode: ' + str(mode))
            return jsonify(game.export_state()), int(HTTPStatus.CREATED)
        else:
            return jsonify({
                "Error": "Unable to register game"
            }), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return jsonify({
            "Error": "Invalid game data"
        }), HTTPStatus.BAD_REQUEST

# --------------------------------------------------------------------------
# GET GAME
# --------------------------------------------------------------------------
# Gets the information of a current game (if it's valid or not)
@app.route('/api/v1/game/<game_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_game(game_id):
    game = Game(None, None, persistence_provider=redis_store)#instace as null to later load from id
    game.load(game_id)
    if game.load(game_id) is None:
        return (ErrorResponse('Game does not exists',
                                     'Please enter a valid game id')).as_json(), HTTPStatus.BAD_REQUEST
    else:
        return game.json()

# --------------------------------------------------------------------------
# GET GAME LIST
# --------------------------------------------------------------------------
# Fetches a list of the current joinable games
@app.route('/api/v1/game/', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_game_list():
    keys= []
    games_data = redis_store.get('games')
    # If there are no players, then we create an empty list
    if games_data is not None:
        games = json.loads(games_data)
        try:
            for game in games:
                if game["game_status"] is GameStatus.WAITING_FOR_PLAYERS.value:
                    keys.append(game["game_id"])
                    if add_player(game["game_id"], "HUMAN"):
                        print("test")
            return jsonify(keys)
        except:
            return False


# --------------------------------------------------------------------------
# POST PLAYER
# --------------------------------------------------------------------------
# Moved to player_entity -- will remove comment after merge




