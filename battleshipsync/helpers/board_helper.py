from random import randrange

MIN_BOAT_SIZE = 2
MAX_BOAT_SIZE = 5

def board_has_space(direction, position, boatSize, boardSize):
  if(direction == 'UP' or direction == 'LEFT'):
    workingAxis = 'y' if direction == 'UP' else 'x'

    return (position[workingAxis] + 1) - boatSize >= 0

  elif(direction == 'RIGHT' or direction == 'DOWN'):
    workingAxis = 'y' if direction == 'DOWN' else 'x'

    return  position[workingAxis] + boatSize <= boardSize

def hits_boat(direction, position, boatSize, boardMatrix):
  if(direction == 'UP'):
    firstSquare = position['y']

    for currentY in range(firstSquare + 1 - boatSize, firstSquare + 1):
      if(boardMatrix[currentY][position['x']] != 0):
        isHittingBoat = True
        break

  elif(direction == 'DOWN'):
    firstSquare = position['y']

    for currentY in range(firstSquare, firstSquare + boatSize):
      if(boardMatrix[currentY][position['x']] != 0):
        isHittingBoat = True
        break

  elif(direction == 'RIGHT'):
    firstSquare = position['x']

    for currentX in range(firstSquare, firstSquare + boatSize):
      if(boardMatrix[position['y']][currentX] != 0):
        isHittingBoat = True
        break

  elif(direction == 'LEFT'):
    firstSquare = position['x']

    for currentX in range(firstSquare + 1 - boatSize, firstSquare + 1):
      if(boardMatrix[position['y']][currentX] != 0):
        isHittingBoat = True
        break

def insertBoardInMatrix(direction, boatSize, initialPosition, boardMatrix):
  if(direction == 'UP'):
    firstSquare = initialPosition['y']

    for currentY in range(firstSquare + 1 - boatSize, firstSquare + 1):
      boardMatrix[currentY][initialPosition['x']] = boatSize

  elif(direction == 'DOWN'):
    firstSquare = initialPosition['y']

    for currentY in range(firstSquare, firstSquare + boatSize):
      boardMatrix[currentY][initialPosition['x']] = boatSize

  elif(direction == 'RIGHT'):
    firstSquare = initialPosition['x']

    for currentX in range(firstSquare, firstSquare + boatSize):
      boardMatrix[initialPosition['y']][currentX] = boatSize

  elif(direction == 'LEFT'):
    firstSquare = initialPosition['x']

    for currentX in range(firstSquare + 1 - boatSize, firstSquare + 1):
      boardMatrix[initialPosition['y']][currentX] = boatSize

  return boardMatrix

def getRandomBoatSize():
  return randrange(MIN_BOAT_SIZE, MAX_BOAT_SIZE)

def getRandomInitialPosition(matrixSize):
  return { 'x': randrange(0, matrixSize), 'y': randrange(0, matrixSize) }

# Gets de direction for the boat checking that there is space for the boat
def getRandomDirection(directions, position, boatSize, boardMatrix):
  if not directions:
    return None

  boardSize = len(boardMatrix)
  index = randrange(0, len(directions))
  direction = directions[index]
  hasSpace = True
  isHittingBoat = False

  if not board_has_space(direction, position, boatSize, boardSize):
    del directions[index]

    return getRandomDirection(directions, position, boatSize, boardMatrix)

  if hits_boat(direction, position, boatSize, boardMatrix):
    del directions[index]

    return getRandomDirection(directions, position, boatSize, boardMatrix)

  return direction
