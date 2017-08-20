from http import HTTPStatus
from flask import jsonify, request
from battleshipsync import app, redis_store
from battleshipsync.models.player import Player
from battleshipsync import redis_store as redis
from flask_jwt import jwt_required, current_identity


# ---------------------------------------------------------------------------------------
# POST PLAYER
# ---------------------------------------------------------------------------------------
@app.route('/api/v1/game/<game_id>/player', methods=['POST'])
@jwt_required()
def post_game_player(game_id):
    """
        To join a game, a new player must be created within the context of the
        game, In order to do this, this endpoint is provided so a new player can
        be generated in a Game instance. 

        TODO add validation for repeated users
    """

    user_id = current_identity.id
    player_data = request.get_json()
    if player_data is not None and user_id is not None:
        player = Player(user_id=user_id, game_id=game_id, persistence_provider=redis)
        if player.register(nickname=player_data['nickname'], is_human=player_data['is_human']):
            return jsonify(player.export_state()), int(HTTPStatus.CREATED)
        else:
            return jsonify({
                "Error": "Unable to register player"
            }), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return jsonify({
            "Error": "Invalid player data"
        }), HTTPStatus.BAD_REQUEST


# ---------------------------------------------------------------------------------------
# GET PLAYER
# ---------------------------------------------------------------------------------------
@app.route('/api/v1/player/<player_id>', methods=['GET'])
@jwt_required()
def get_player(player_id):
    """
        Gets the data of a given player identified bu user id
    """

    if player_id is not None:
        user_id = current_identity.id
        player = Player(user_id=user_id, game_id=None, persistence_provider=redis)
        if player.load(player_id=player_id):
            return jsonify(player.export_state), HTTPStatus.OK
        else:
            return jsonify({
                "Error": "Player not found"
            }), HTTPStatus.NOT_FOUND
    else:
        return jsonify({"Error": "Invalid player_id"}), HTTPStatus.BAD_REQUEST