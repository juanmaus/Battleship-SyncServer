from battleshipsync.helpers.board_helper import (
  board_has_space, hits_boat,
  get_random_boat_size,
  get_random_initial_position,
  get_random_direction,
  insert_board_in_matrix
)

MAX_POPULATION_ATTEMPTS = 100
DIRECTIONS = [
  'LEFT',
  'UP',
  'RIGHT',
  'DOWN'
]

# Populates a board matrix that is assumed to be NxN with boats
def populateBoard(boats_to_create, board_matrix):
  isPopulated = False
  boatsCreated = 0
  attemptsCount = 0

  while(boatsCreated < boats_to_create or attemptsCount > MAX_POPULATION_ATTEMPTS):
    attemptsCount = attemptsCount + 1

    boat_size = get_random_boat_size()
    initalPosition = get_random_initial_position(len(board_matrix))
    direction = get_random_direction(
      DIRECTIONS,
      initalPosition,
      boat_size,
      board_matrix
    )

    if not direction:
      continue

    insert_board_in_matrix(direction, boat_size, initalPosition, board_matrix)
    boatsCreated = boatsCreated + 1

  return board_matrix
