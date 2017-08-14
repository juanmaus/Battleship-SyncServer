from battleshipsync.helpers.board_helper import (
    board_has_space, hits_boat,
    get_random_boat_size,
    get_random_initial_position,
    get_random_direction,
    insert_boat_in_matrix
)

MAX_POPULATION_ATTEMPTS = 100
DIRECTIONS = [
  'LEFT',
  'UP',
  'RIGHT',
  'DOWN'
]


# ---------------------------------------------------------------------------------------
#  FUNCTION POPULATE BOARD
# ---------------------------------------------------------------------------------------
def populate_board(boats_to_create, board_matrix):

    """
        This functions fills a given matrix with a given set of boats that should be randomly placed on 
        the matrix. 
        :param boats_to_create: The boats that should be placed on the matrix
        :param board_matrix: The matrix that will be populated with randomly located boats.
        :return: The populated matrix. 
    """

    is_populated = False
    boats_created = 0
    attempts_count = 0

    while boats_created < boats_to_create or attempts_count > MAX_POPULATION_ATTEMPTS:
        attempts_count = attempts_count + 1

        boat_size = get_random_boat_size()
        initial_position = get_random_initial_position(len(board_matrix))
        direction = get_random_direction(
          DIRECTIONS,
          initial_position,
          boat_size,
          board_matrix
        )
        if not direction:
            continue
        insert_boat_in_matrix(direction, boat_size, initial_position, board_matrix)
        boats_created = boats_created + 1

    return board_matrix
