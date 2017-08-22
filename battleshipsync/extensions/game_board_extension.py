from battleshipsync.helpers.board_helper import (
    board_has_space, hits_boat,
    get_random_initial_position,
    get_random_direction,
    insert_boat_in_matrix,
    generate_matrix
)

MAX_POPULATION_ATTEMPTS = 100
DIRECTIONS = [
  'LEFT',
  'UP',
  'RIGHT',
  'DOWN'
]
BOATS_TO_CREATE = [5, 4, 3, 3, 2]

# ---------------------------------------------------------------------------------------
#  FUNCTION CREATE AND POPULATE BOARD
# ---------------------------------------------------------------------------------------
def create_board():

    """
        This functions creates a matrix and fills it with boats
        :return: The populated matrix.
    """

    board_matrix = generate_matrix()
    attempts_count = 0
    boats_to_create = len(BOATS_TO_CREATE)

    for boat_size in BOATS_TO_CREATE:
        while attempts_count < MAX_POPULATION_ATTEMPTS:
            attempts_count = attempts_count + 1

            initial_position = get_random_initial_position(len(board_matrix))
            direction = get_random_direction(
              DIRECTIONS[:],
              initial_position,
              boat_size,
              board_matrix
            )

            if not direction:
                continue

            insert_boat_in_matrix(direction, boat_size, initial_position, board_matrix)
            break

    return board_matrix
