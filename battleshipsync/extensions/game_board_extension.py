from battleshipsync.helpers.board_helper import (
  board_has_space, hits_boat,
  getRandomBoatSize,
  getRandomInitialPosition,
  getRandomDirection,
  insertBoardInMatrix
)

MAX_POPULATION_ATTEMPTS = 100
DIRECTIONS = [
  'LEFT',
  'UP',
  'RIGHT',
  'DOWN'
]

# Populates a board matrix that is assumed to be NxN with boats
def populateBoard(boatsToCreate, boardMatrix):
  isPopulated = False
  boatsCreated = 0
  attemptsCount = 0

  while(boatsCreated < boatsToCreate or attemptsCount > MAX_POPULATION_ATTEMPTS):
    attemptsCount = attemptsCount + 1

    boatSize = getRandomBoatSize()
    initalPosition = getRandomInitialPosition(len(boardMatrix))
    direction = getRandomDirection(
      DIRECTIONS,
      initalPosition,
      boatSize,
      boardMatrix
    )

    if not direction:
      continue

    insertBoardInMatrix(direction, boatSize, initalPosition, boardMatrix)
    boatsCreated = boatsCreated + 1

  return boardMatrix
