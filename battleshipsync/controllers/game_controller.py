from http import HTTPStatus
from battleshipsync import app, redis_store
from flask import request, jsonify, json
from battleshipsync.models.account import User
from battleshipsync.models.account import UserService
from battleshipsync.security.idam import find_user
from battleshipsync import redis_store
from battleshipsync.extensions.jsonp import enable_jsonp
from battleshipsync.extensions.error_handling import ErrorResponse
from battleshipsync.extensions.error_handling import SuccessResponse
from battleshipsync.models.game import Game, GameStatus, GameMode
from battleshipsync.models.player import Player,PlayerType
from flask_jwt import jwt_required, current_identity
import uuid


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
    owner_id = current_identity.id
    owner = owner_id  # TODO create player entity from here
    game = Game(mode=mode, owner=owner, player_layout=layout, persistence_provider=redis_store)
    game.save()
    #app.logger.info('Game with ID: \'' + game.id + '\' was created by user ' + str(current_identity.username )+' mode: ' + str(mode))
    return game.json()



# --------------------------------------------------------------------------
# GET GAME
# --------------------------------------------------------------------------
# Gets the information of a current game (if it's valid or not)
@app.route('/api/v1/game/<game_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_game(game_id):
    game = Game(0, 0, 0, persistence_provider=redis_store)#instace as null to later load from id
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
    #for key in redis_store.scan_iter("F-*"): #check with team first
    for key in redis_store.scan_iter():  # TODO: add filters players/type
        print(key)
        keys.append(str(key))
    return jsonify(keys)


# --------------------------------------------------------------------------
# POST PLAYER
# --------------------------------------------------------------------------
# Moved to player_entity -- will remove comment after merge




