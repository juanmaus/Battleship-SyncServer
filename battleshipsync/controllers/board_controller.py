from http import HTTPStatus
from battleshipsync import app
from flask import request, jsonify
from battleshipsync import redis_store
from battleshipsync.security.idam import find_user
from battleshipsync.models.board import Board, ShootResult, parse_board_id
from battleshipsync.models.dao.player_index import verify_ownership
from battleshipsync.extensions.error_handling import ErrorResponse
from battleshipsync.extensions.error_handling import SuccessResponse
from flask_jwt import jwt_required, current_identity
import uuid


# ---------------------------------------------------------------------------------------
# GET BOARD
# ---------------------------------------------------------------------------------------
@app.route('/api/v1/board/<board_id>', methods=['GET'])
@jwt_required()
def get_initial_board(board_id):
    """
        This endpoint allows a user to get it's current board. This method will only allow
        the player's own board. If another player's board is attempted to access, then a 
        401 Not authorized error code should be returned.
        :return: A json representation of the player's board.
    """
    if board_id is not None:
        # Check current identity matches owner of the board.
        identifiers = parse_board_id(board_id)
        if verify_ownership(player_id=identifiers['player_id'], user_id=current_identity.id):
            # If the user is the actual owner of the board, then we can provide the complete
            # and updated representation of the board.
            board = Board(
                game_id=identifiers['game_id'],
                player_id=identifiers['player_id'],
                redis_store=redis_store
            )
            return jsonify(board.export_state()), 200
        return jsonify({
            "Error": True,
            "Message": "You are not the owner of the requested board. Only owner can request he's board"
        }), 401
    return jsonify({
        "Error": True,
        "Message": "No board id provided"
    }), int(HTTPStatus.BAD_REQUEST)


# ---------------------------------------------------------------------------------------
# POST BOMB
# ---------------------------------------------------------------------------------------
@app.route('/api/v1/board/<board_id>/torpedo', methods=['POST'])
@jwt_required()
def post_torpedo(board_id):

    """
        ---------------------------------------------------------------------------------
        This method allows to drop a torpedo in a given pair of coordinates on a board belonging 
        to an opponent that is currently playing within the same game instance. The boards are
        uniquely identified by a key formed from the game's id and the player' id like in:
        
            [<game_id>:<player_id>]
            
        In order to specify the coordinates that are going to indicate the location where 
        the torpedo is going to be sent, the following payload must be provided (example 
        values):
        
            {
                "destination_board": "1c1b28ac-7973-11e7-b5a5-be2e44b06b34:1c1b2e42-7973-11e7-b5a5-be2e44b06b34",
                "x_coordinate": 3,
                "y_coordinate": 4
            }
        
        :param board_id: The id of the board to where the 
        :return: A json payload containing the result of the bombing operation in the 
                 given board. 
        ---------------------------------------------------------------------------------
    """
    torpedo_coordinates = request.get_json()
    board_data = redis_store.get(board_id)

    # First we check if the board instance actually exists within redis store.
    if board_data is not None:
        # Next we verify the user is not trying to send torpedo to his own board.
        identifiers = parse_board_id(board_id)
        board = Board(game_id=identifiers['game_id'], player_id=identifiers['player_id'], redis_store=redis_store)
        if board.get_player_id() != current_identity.id:
            if torpedo_coordinates is not None:
                result = board.shoot(torpedo_coordinates['x'], torpedo_coordinates['y'])
                if result >= 0:
                    # We update the state on the redis store
                    board.save()
                    # TODO update player's state with new score
                return jsonify({
                    "result_code": result
                    # TODO include player' data
                }), HTTPStatus.CREATED
            else:
                app.logger.error('Player tried to shoot a torpedo into a non-valid location')
                return jsonify(
                    ErrorResponse(
                        'Invalid coordinates for torpedo', 'You cannot shoot to nowhere. Provide a valid json payload to shoot'
                    )
                ), HTTPStatus.BAD_REQUEST
        else:
            return jsonify(ErrorResponse('Invalid torpedo operation',
                                         'Dude, you cannot shoot your own crappy boats!')), HTTPStatus.BAD_REQUEST
    else:
        return jsonify(
            ErrorResponse('Unable to find board', 'The provided board is does not correspond to a valid board')
        ), HTTPStatus.NOT_FOUND


