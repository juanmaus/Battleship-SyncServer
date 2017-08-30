#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randrange

BOARD_SIZE = 10


# ---------------------------------------------------------------------------------------
#  FUNCTION POPULATE BOARD
# ---------------------------------------------------------------------------------------
def board_has_space(
    direction,
    position,
    boat_size,
    board_size,
    ):
    """

    :param direction:
    :param position:
    :param boat_size:
    :param board_size:
    :return:
    """
    if direction == 'UP' or direction == 'LEFT':
        working_axis = ('y' if direction == 'UP' else 'x')

        return position[working_axis] + 1 - boat_size >= 0
    elif direction == 'RIGHT' or direction == 'DOWN':

        working_axis = ('y' if direction == 'DOWN' else 'x')

        return position[working_axis] + boat_size <= board_size


# ---------------------------------------------------------------------------------------
#  FUNCTION POPULATE BOARD
# ---------------------------------------------------------------------------------------
def hits_boat(
    direction,
    position,
    boat_size,
    board_matrix,
    ):
    """

    :param direction:
    :param position:
    :param boat_size:
    :param board_matrix:
    :return:
    """
    if direction == 'UP':
        first_square = position['y']

        for currentY in range(first_square + 1 - boat_size, first_square + 1):
            if board_matrix[currentY][position['x']] != 0:
                return True

    elif direction == 'DOWN':

        first_square = position['y']

        for currentY in range(first_square, first_square + boat_size):
            if board_matrix[currentY][position['x']] != 0:
                return True
    elif direction == 'RIGHT':

        first_square = position['x']

        for currentX in range(first_square, first_square + boat_size):
            if board_matrix[position['y']][currentX] != 0:
                return True

    elif direction == 'LEFT':

        first_square = position['x']

        for currentX in range(first_square + 1 - boat_size, first_square + 1):
            if board_matrix[position['y']][currentX] != 0:
                return True

    return False

# ---------------------------------------------------------------------------------------
#  FUNCTION POPULATE BOARD
# ---------------------------------------------------------------------------------------
def insert_boat_in_matrix(
    direction,
    boat_size,
    initial_position,
    board_matrix,
    ):

    """

    :param direction:
    :param boat_size:
    :param initial_position:
    :param board_matrix:
    :return:
    """

    if direction == 'UP':
        first_square = initial_position['y']

        for currentY in range(first_square + 1 - boat_size, first_square + 1):
            board_matrix[currentY][initial_position['x']] = boat_size
    elif direction == 'DOWN':

        first_square = initial_position['y']

        for currentY in range(first_square, first_square + boat_size):
            board_matrix[currentY][initial_position['x']] = boat_size
    elif direction == 'RIGHT':

        first_square = initial_position['x']

        for currentX in range(first_square, first_square + boat_size):
            board_matrix[initial_position['y']][currentX] = boat_size
    elif direction == 'LEFT':

        first_square = initial_position['x']

        for currentX in range(first_square + 1 - boat_size, first_square
                              + 1):
            board_matrix[initial_position['y']][currentX] = boat_size

    return board_matrix

# ---------------------------------------------------------------------------------------
#  FUNCTION POPULATE BOARD
# ---------------------------------------------------------------------------------------
def get_random_initial_position(matrix_size):
    """

    :param matrix_size:
    :return:
    """
    return {'x': randrange(0, matrix_size), 'y': randrange(0,
                                                           matrix_size)}


# Gets de direction for the boat checking that there is space for the boat

# ---------------------------------------------------------------------------------------
#  FUNCTION POPULATE BOARD
# ---------------------------------------------------------------------------------------
def get_random_direction(
    directions,
    position,
    boat_size,
    board_matrix,
    ):

    """

    :param directions:
    :param position:
    :param boat_size:
    :param board_matrix:
    :return:
    """
    if not directions:
        return None

    board_size = len(board_matrix)
    index = randrange(0, len(directions))
    direction = directions[index]

    if not board_has_space(direction, position, boat_size, board_size):
        del directions[index]

        return get_random_direction(directions, position, boat_size,
                                    board_matrix)

    if hits_boat(direction, position, boat_size, board_matrix):
        del directions[index]

        return get_random_direction(directions, position, boat_size,
                                    board_matrix)
    return direction

# ---------------------------------------------------------------------------------------
#  FUNCTION GENERATE EMPTY MATRIX
# ---------------------------------------------------------------------------------------
def generate_matrix():
    matrix = [None] * BOARD_SIZE

    for x in range(0, BOARD_SIZE):
        matrix[x] = [0] * BOARD_SIZE

    return matrix
