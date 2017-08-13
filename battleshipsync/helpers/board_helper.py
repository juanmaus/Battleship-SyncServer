from random import randrange

MIN_BOAT_SIZE = 2
MAX_BOAT_SIZE = 5

def board_has_space(direction, position, boat_size, boardSize):
  if(direction == 'UP' or direction == 'LEFT'):
    workingAxis = 'y' if direction == 'UP' else 'x'

    return (position[workingAxis] + 1) - boat_size >= 0

  elif(direction == 'RIGHT' or direction == 'DOWN'):
    workingAxis = 'y' if direction == 'DOWN' else 'x'

    return  position[workingAxis] + boat_size <= boardSize

def hits_boat(direction, position, boat_size, board_matrix):
  if(direction == 'UP'):
    firstSquare = position['y']

    for currentY in range(firstSquare + 1 - boat_size, firstSquare + 1):
      if(board_matrix[currentY][position['x']] != 0):
        isHittingBoat = True
        break

  elif(direction == 'DOWN'):
    firstSquare = position['y']

    for currentY in range(firstSquare, firstSquare + boat_size):
      if(board_matrix[currentY][position['x']] != 0):
        isHittingBoat = True
        break

  elif(direction == 'RIGHT'):
    firstSquare = position['x']

    for currentX in range(firstSquare, firstSquare + boat_size):
      if(board_matrix[position['y']][currentX] != 0):
        isHittingBoat = True
        break

  elif(direction == 'LEFT'):
    firstSquare = position['x']

    for currentX in range(firstSquare + 1 - boat_size, firstSquare + 1):
      if(board_matrix[position['y']][currentX] != 0):
        isHittingBoat = True
        break

def insert_board_in_matrix(direction, boat_size, initialPosition, board_matrix):
  if(direction == 'UP'):
    firstSquare = initialPosition['y']

    for currentY in range(firstSquare + 1 - boat_size, firstSquare + 1):
      board_matrix[currentY][initialPosition['x']] = boat_size

  elif(direction == 'DOWN'):
    firstSquare = initialPosition['y']

    for currentY in range(firstSquare, firstSquare + boat_size):
      board_matrix[currentY][initialPosition['x']] = boat_size

  elif(direction == 'RIGHT'):
    firstSquare = initialPosition['x']

    for currentX in range(firstSquare, firstSquare + boat_size):
      board_matrix[initialPosition['y']][currentX] = boat_size

  elif(direction == 'LEFT'):
    firstSquare = initialPosition['x']

    for currentX in range(firstSquare + 1 - boat_size, firstSquare + 1):
      board_matrix[initialPosition['y']][currentX] = boat_size

  return board_matrix

def get_random_boat_size():
  return randrange(MIN_BOAT_SIZE, MAX_BOAT_SIZE)

def get_random_initial_position(matrixSize):
  return { 'x': randrange(0, matrixSize), 'y': randrange(0, matrixSize) }

# Gets de direction for the boat checking that there is space for the boat
def get_random_direction(directions, position, boat_size, board_matrix):
  if not directions:
    return None

  boardSize = len(board_matrix)
  index = randrange(0, len(directions))
  direction = directions[index]
  hasSpace = True
  isHittingBoat = False

  if not board_has_space(direction, position, boat_size, boardSize):
    del directions[index]

    return get_random_direction(directions, position, boat_size, board_matrix)

  if hits_boat(direction, position, boat_size, board_matrix):
    del directions[index]

    return get_random_direction(directions, position, boat_size, board_matrix)

  return direction
