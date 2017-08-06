from battleshipsync import app, redis_store
from flask import request, jsonify
from battleshipsync.models.account import User
from battleshipsync.models.account import UserService
from battleshipsync.security.idam import find_user
from battleshipsync.extensions.jsonp import enable_jsonp
from battleshipsync.extensions.error_handling import ErrorResponse
from battleshipsync.extensions.error_handling import SuccessResponse
from battleshipsync.models.game import Game, GameStatus, GameMode
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
    owner = None  # TODO use owner id to create a new player
    game = Game(mode=mode, owner=owner, player_layout=layout)
    # TODO perist game in redis and set other attributes


# --------------------------------------------------------------------------
# GET GAME
# --------------------------------------------------------------------------
# Gets the account information associated with current session in the system
@app.route('/api/v1/game/<game_id>', methods=['GET'])
@jwt_required()
@enable_jsonp
def get_game(game_id):
    pass


@app.route('/api/v1/game/setBoard', methods=['POST'])
@jwt_required()
@enable_jsonp
def index():
    board_data = request.get_json()
    key = board_data['key']             #divide gameId and playerId
    board = board_data['board']
    redis_store.set(key, board)
    return "someting more usefull"

##--example payaload"

# {
#             "key": "5:12",
#             "board":[
#                  [0,0,0,5,5,5,5,5,0,0],
#                  [2,2,0,0,0,0,0,0,0,0],
#                  [0,0,1,0,0,0,4,0,0,0],
#                  [0,0,0,0,0,0,4,0,0,0],
#                  [0,0,0,0,0,0,4,0,0,0],
#                  [0,0,0,0,0,0,4,0,0,0],
#                  [0,0,2,0,1,0,0,0,0,0],
#                  [0,0,2,0,0,0,0,0,3,0],
#                  [0,0,0,0,0,0,0,0,3,0],
#                  [3,3,3,0,0,0,0,0,3,0]
#              ]
# } go on from here, resolve jwt auth problems
