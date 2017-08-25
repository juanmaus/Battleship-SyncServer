from http import HTTPStatus
from battleshipsync import app
from flask import request, jsonify
from battleshipsync import redis_store
from battleshipsync.models.board import Board
from battleshipsync.models.dao.player_index import verify_ownership
from battleshipsync.helpers.player_helper import get_player
from battleshipsync.models.dao.game_index import move_to_next_player
from battleshipsync.extensions.error_handling import ErrorResponse
from flask_jwt import jwt_required, current_identity
import uuid
import json


# ---------------------------------------------------------------------------------------
# GET BOARD
# ---------------------------------------------------------------------------------------
@app.route('/api/v1/board/<board_id>', methods=['GET'])
@jwt_required()
def get_board(board_id):
    """
        This endpoint allows a user to get it's current board. This method will only allow
        the player's own board. If another player's board is attempted to access, then a 
        401 Not authorized error code should be returned.
        :return: A json representation of the player's board.
    """
    if board_id is not None:
        # Check current identity matches owner of the board.
        board_data = redis_store.get(board_id)
        board = json.loads(board_data)
        if verify_ownership(player_id=board['player_id'], user_id=current_identity.id):
            # If the user is the actual owner of the board, then we can provide the complete
            # and updated representation of the board.
            board = Board(
                game_id=board['game_id'],
                player_id=board['player_id'],
                board_id=board_id,
                persistence_provider=redis_store
            )
            board.load(board_data)
            result = board.export_state()
            board = None
            return jsonify(result), 200
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
        uniquely identified by a key. 
            
        In order to specify the coordinates that are going to indicate the location where 
        the torpedo is going to be sent, the following payload must be provided (example 
        values):
        
            {
                "x_coordinate": 3,
                "y_coordinate": 4, 
                "shooter": "56c142a9-8946-4b50-9e12-e12867573d3f"
            }
        
        :param board_id: The id of the board to where the 
        :return: A json payload containing the result of the bombing operation in the 
                 given board. 
        ---------------------------------------------------------------------------------
    """
    torpedo_coordinates = request.get_json()
    board_data = redis_store.get(board_id)

    # First we check if the board instance actually exists within redis store.
    app.logger.info('Checking board...')
    if board_data is not None:
        brt = json.loads(board_data)
        # Next we verify the user is not trying to send torpedo to his own board.

        board = Board(
            game_id=brt['game_id'],
            player_id=brt['player_id'],
            board_id=brt['board_id'],
            persistence_provider=redis_store
        )

        app.logger.info('Instantiating board...')
        board.load(board_data)

        app.logger.info('board loaded with data: ' + str(board_data))

        app.logger.info('Getting shooter...')
        shooter = get_player(torpedo_coordinates['shooter'])

        app.logger.info('Getting receiver...')
        receiver = get_player(board.get_player_id())

        if board.get_owner_id() != current_identity.id and current_identity.id == shooter.get_owner():
            app.logger.info('Seems its working...')

            if torpedo_coordinates is not None:
                result = board.shoot(torpedo_coordinates['x_coordinate'], torpedo_coordinates['y_coordinate'])

                if result >= 0:
                    # We update the state on the redis store
                    board.save()
                    app.logger.info('Torpedo was sent: shooter: ['+current_identity.id + '] destination ->> [' + board.get_player_id() + ']')

                    if shooter is not None and receiver is not None:
                        print('Shooter and affected found!... moving on')
                        app.logger.info('Shoot result was: [' + str(result) + ']')
                        if result > 0:
                            shooter.add_points(result)
                            receiver.update_fleet_value(result)
                            app.logger.info('Boat was damaged by torpedo...')
                        app.logger.info('moving to next player...')
                        move_to_next_player(board.get_game_id())
                        app.logger.info('building result...')
                        s = shooter.export_state()
                        r = receiver.export_state()
                        shooter = None
                        receiver = None
                        return jsonify({
                            "result_code": result,
                            "shooter": s,
                            "receiver": r
                        }), HTTPStatus.CREATED
                    else:
                        app.logger.error('If you get here...This shit is nasty... players not found for transaction')
                        return jsonify(
                            {
                                'Error': 'Internal player reference error',
                                'Message': 'Players in transaction could not be found'
                            }
                        )
            else:
                app.logger.error('Some stupid player tried to shoot a torpedo into a non-valid location')
                return jsonify(
                    ErrorResponse(
                        'Invalid coordinates for torpedo',
                        'You cannot shoot to nowhere. Provide a valid json payload to shoot'
                    ).get()
                ), int(HTTPStatus.BAD_REQUEST)
        else:
            return jsonify({'Error': 'Invalid torpedo operation',
                                     'Message': 'Dude, you cannot shoot your own crappy boats nor steal identities...!'}), int(HTTPStatus.BAD_REQUEST)
    else:
        return jsonify(
            ErrorResponse(
                'Unable to find board',
                'The provided board is does not correspond to a valid board'
            ).get()
        ), int(HTTPStatus.NOT_FOUND)


