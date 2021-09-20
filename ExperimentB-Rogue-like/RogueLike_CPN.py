NET = 'net'
import itertools, collections

from zinc.nets import Marking, mset, dot, hdict
event = collections.namedtuple('event', ['trans', 'mode', 'sub', 'add'])

import random

def initPosition(x, y):
  return (x, y)

def generateListOfPositions(boardBounds):
  availablePositions = []
  xMax = int(boardBounds[1] - 1)
  yMax = int(boardBounds[3] - 1)
  for x in range(1, xMax):
    for y in range(1, yMax):
      pos = (x,y)
      availablePositions.append(pos)

  return tuple(availablePositions)
      
def getPositions(availablePositions, count):
  positions = []

  while(len(positions) != count):
    pos = random.choice(availablePositions)
    if(not (pos in positions)):
      positions.append(pos)
  
  return tuple(positions)

def removePositions(availablePositions, toBeRemoved):
  availablePositionsList = list(availablePositions)
  for pos in toBeRemoved:
    availablePositionsList.remove(pos)
  
  return tuple(availablePositionsList)


def returnRandomInt(x, y):
  return random.randint(x, y)

def returnRandomBool():
  return random.choice([True,False])

def canMove(gameOver):
  if(gameOver == False):
    return 1

def onMovePlayer(moveVal, playerPos, enemy1Pos, wall1Pos, wall1Health,borderBounds):
  newPos = (playerPos[0] + moveVal[0], playerPos[1] + moveVal[1])

  if( (newPos[0] == (borderBounds[0] - 1) ) or 
      (newPos[0] == (borderBounds[1] + 1) ) or 
      (newPos[1] == (borderBounds[2] - 1) ) or 
      (newPos[1] == (borderBounds[3] + 1) )):
      return playerPos
  
  if(newPos[0] == enemy1Pos[0] and newPos[1] == enemy1Pos[1]):
    return playerPos 
  
  if(newPos[0] == wall1Pos[0] and newPos[1] == wall1Pos[1] and wall1Health > 0):
    return playerPos

  return newPos

def updateWallHealth(moveVal, playerPos, wallPos, wallHealth):
  newPos = (playerPos[0] + moveVal[0], playerPos[1] + moveVal[1])

  if(newPos[0] == wallPos[0] and newPos[1] == wallPos[1] and wallHealth > 0):
    return wallHealth - 1
  
  return wallHealth

def decreasePoints(points, moveVal, playerPos, wallPos, wallHealth):
    newPos = (playerPos[0] + moveVal[0], playerPos[1] + moveVal[1])
    newpoints = points 
    if(newPos[0] == wallPos[0] and newPos[1] == wallPos[1] and wallHealth > 0):
        newpoints -= 4

    return newpoints - 1

def checkFoodPoints(playerFoodPoints, gameOver, moveVal, playerPos, wallPos, wallHealth):
  points = decreasePoints(playerFoodPoints, moveVal, playerPos, wallPos, wallHealth)
  if((points) <= 0):
    return True
  return gameOver

def checkExit(playerPos, exitPos, val):
  if((playerPos == exitPos) == val):
    return 1

def increaseLevelCount(levelCount):
  return levelCount + 1

def updateFoodPoints(playerPos, playerFoodPoints, foodActive, foodPos, drinkActive, drinkPos):
  if(foodActive and playerPos == foodPos):
    return playerFoodPoints + 10
  if(drinkActive and playerPos == drinkPos):
    return playerFoodPoints + 20
  
  return playerFoodPoints


def updateFoodActive(playerPos, playerFoodPoints, isActive, itemPos):
  if(isActive and playerPos == itemPos):
    return False
  
  return isActive

def checkGameOverFood(playerFoodPoints, val):
    if((playerFoodPoints > 0) == val):
        return 1

def checkGameOver(gameOver, val):
  if(gameOver == val):
    return 1


def updateEnemyPosition(enemyPos, playerPos, wall1Pos, wall1Health, boardBounds):
  
  yVal = 0
  xVal = 0
  xAbs = abs(enemyPos[0] - playerPos[0])
  if(xAbs == 0):
    if(enemyPos[1] < playerPos[1]):
      yVal = 1
    elif(enemyPos[1] > playerPos[1]):
      yVal = -1
  else:
    if(enemyPos[0] < playerPos[0]):
      xVal = 1
    elif(enemyPos[0] > playerPos[0]):
      xVal = -1

  newPos = (enemyPos[0] + xVal, enemyPos[1] + yVal)

  if(newPos[0] == playerPos[0] and newPos[1] == playerPos[1]):
    return enemyPos

  if( (newPos[0] == (boardBounds[0] - 1) ) or 
      (newPos[0] == (boardBounds[1] + 1) ) or 
      (newPos[1] == (boardBounds[2] - 1) ) or 
      (newPos[1] == (boardBounds[3] + 1) )):
      return enemyPos

  if(newPos[0] == wall1Pos[0] and newPos[1] == wall1Pos[1] and wall1Health > 0):
    return enemyPos

  return newPos

def onEnemyAttack(enemy1Pos, playerPos, playerFoodPoints):
  foodPoints = playerFoodPoints
  yVal = 0
  xVal = 0
  xAbs = abs(enemy1Pos[0] - playerPos[0])
  if(xAbs == 0):
    if(enemy1Pos[1] < playerPos[1]):
      yVal = 1
    elif(enemy1Pos[1] > playerPos[1]):
      yVal = -1
  else:
    if(enemy1Pos[0] < playerPos[0]):
      xVal = 1
    elif(enemy1Pos[0] > playerPos[0]):
      xVal = -1

  newPosEnemy1 = (enemy1Pos[0] + xVal, enemy1Pos[1] + yVal)

  if(newPosEnemy1[0] == playerPos[0] and newPosEnemy1[1] == playerPos[1]):
    foodPoints -= 20

  return foodPoints

def onEnemyAttackUpdateGameOver(gameOver, enemy1Pos, playerPos, playerFoodPoints):
  foodPoints = onEnemyAttack(enemy1Pos, playerPos, playerFoodPoints)

  if(foodPoints <= 0):
    return True
  
  return gameOver

def addsucc_001 (marking, succ):
    "successors of 'check exit collisions'"
    if marking('exitCollision') and marking('exitPos') and marking('playerPos'):
        for exitCollision in marking('exitCollision'):
            for playerPos in marking('playerPos'):
                for exitPos in marking('exitPos'):
                    if isinstance(exitPos, tuple):
                        if isinstance(playerPos, tuple):
                            a = checkExit(playerPos, exitPos, True)
                            if isinstance(a, int) or a == None:
                                b = checkExit(playerPos, exitPos, False)
                                if isinstance(b, int) or b == None:
                                    test = Marking({'playerPos': mset([playerPos]), 'exitPos': mset([exitPos]), 'exitCollision': mset([exitCollision])})
                                    if test <= marking:
                                        sub = Marking({'exitCollision': mset([exitCollision])})
                                        if(a == None):
                                            add = Marking({'notReachedExit': mset([b])})
                                        elif(b == None):
                                            add = Marking({'reachedExit': mset([a])})
                                        succ.add(marking - sub + add)

def succ_001 (marking):
    "successors of 'check exit collisions'"
    succ = set()
    addsucc_001(marking, succ)
    return succ

def itersucc_001 (marking):
    "successors of 'check exit collisions'"
    if marking('exitCollision') and marking('exitPos') and marking('playerPos'):
        for exitCollision in marking('exitCollision'):
            for playerPos in marking('playerPos'):
                for exitPos in marking('exitPos'):
                    if isinstance(exitPos, tuple):
                        if isinstance(playerPos, tuple):
                            a = checkExit(playerPos, exitPos, True)
                            if isinstance(a, int):
                                b = checkExit(playerPos, exitPos, False)
                                if isinstance(b, int):
                                    test = Marking({'playerPos': mset([playerPos]), 'exitPos': mset([exitPos]), 'exitCollision': mset([exitCollision])})
                                    if test <= marking:
                                        sub = Marking({'exitCollision': mset([exitCollision])})
                                        add = Marking({'reachedExit': mset([a]), 'notReachedExit': mset([b])})
                                        mode = hdict({'playerPos': playerPos, 'exitPos': exitPos, 'exitCollision': exitCollision})
                                        yield event('check exit collisions', mode, sub, add)

def addsucc_002 (marking, succ):
    "successors of 'check food collisions'"
    if marking('foodPos') and marking('drinkActive') and marking('playerFoodPoints') and marking('notReachedExit') and marking('drinkPos') and marking('playerPos') and marking('foodActive'):
        for notReachedExit in marking('notReachedExit'):
            for playerPos in marking('playerPos'):
                for playerFoodPoints in marking('playerFoodPoints'):
                    for foodPos in marking('foodPos'):
                        for foodActive in marking('foodActive'):
                            for drinkPos in marking('drinkPos'):
                                for drinkActive in marking('drinkActive'):
                                        if isinstance(playerPos, tuple):
                                            a = updateFoodPoints(playerPos, playerFoodPoints, foodActive, foodPos, drinkActive, drinkPos)
                                            if isinstance(a, int):
                                                if isinstance(foodPos, tuple):
                                                    b = updateFoodActive(playerPos, playerFoodPoints, foodActive, foodPos)
                                                    if isinstance(b, bool):
                                                        if isinstance(drinkPos, tuple):
                                                            c = updateFoodActive(playerPos, playerFoodPoints, drinkActive, drinkPos)
                                                            if isinstance(c, bool):
                                                                d = checkGameOverFood(playerFoodPoints, True)
                                                                e = checkGameOverFood(playerFoodPoints, False)
                                                                test = Marking({'foodPos': mset([foodPos]), 'drinkPos': mset([drinkPos]), 'playerPos': mset([playerPos]), 'notReachedExit': mset([notReachedExit]), 'playerFoodPoints': mset([playerFoodPoints]), 'foodActive': mset([foodActive]), 'drinkActive': mset([drinkActive])})
                                                                if test <= marking:
                                                                    sub = Marking({'notReachedExit': mset([notReachedExit]), 'playerFoodPoints': mset([playerFoodPoints]), 'foodActive': mset([foodActive]), 'drinkActive': mset([drinkActive])})
                                                                    if(d == None):
                                                                        add = Marking({'playerFoodPoints': mset([a]), 'foodActive': mset([b]), 'drinkActive': mset([c]), 'resetGame': mset([e])})
                                                                    elif(e == None):
                                                                        add = Marking({'playerFoodPoints': mset([a]), 'foodActive': mset([b]), 'drinkActive': mset([c]), 'enemiesTurn': mset([d])})
                                                                    succ.add(marking - sub + add)

def succ_002 (marking):
    "successors of 'check food collisions'"
    succ = set()
    addsucc_002(marking, succ)
    return succ

def itersucc_002 (marking):
    "successors of 'check food collisions'"
    if marking('foodPos') and marking('drinkActive') and marking('gameOver') and marking('playerFoodPoints') and marking('notReachedExit') and marking('drinkPos') and marking('playerPos') and marking('foodActive'):
        for notReachedExit in marking('notReachedExit'):
            for playerPos in marking('playerPos'):
                for playerFoodPoints in marking('playerFoodPoints'):
                    for foodPos in marking('foodPos'):
                        for foodActive in marking('foodActive'):
                            for drinkPos in marking('drinkPos'):
                                for drinkActive in marking('drinkActive'):
                                    for gameOver in marking('gameOver'):
                                        if isinstance(playerPos, tuple):
                                            a = updateFoodPoints(playerPos, playerFoodPoints, foodActive, foodPos, drinkActive, drinkPos)
                                            if isinstance(a, int):
                                                if isinstance(foodPos, tuple):
                                                    b = updateFoodActive(playerPos, playerFoodPoints, foodActive, foodPos)
                                                    if isinstance(b, bool):
                                                        if isinstance(drinkPos, tuple):
                                                            c = updateFoodActive(playerPos, playerFoodPoints, drinkActive, drinkPos)
                                                            if isinstance(c, bool):
                                                                d = checkGameOver(playerFoodPoints, False)
                                                                e = checkGameOver(playerFoodPoints, True)
                                                                test = Marking({'foodPos': mset([foodPos]), 'drinkPos': mset([drinkPos]), 'playerPos': mset([playerPos]), 'notReachedExit': mset([notReachedExit]), 'playerFoodPoints': mset([playerFoodPoints]), 'foodActive': mset([foodActive]), 'drinkActive': mset([drinkActive]), 'gameOver': mset([gameOver])})
                                                                if test <= marking:
                                                                    sub = Marking({'notReachedExit': mset([notReachedExit]), 'playerFoodPoints': mset([playerFoodPoints]), 'foodActive': mset([foodActive]), 'drinkActive': mset([drinkActive]), 'gameOver': mset([gameOver])})
                                                                    add = Marking({'playerFoodPoints': mset([a]), 'foodActive': mset([b]), 'drinkActive': mset([c]), 'enemiesTurn': mset([d]), 'resetGame': mset([e])})
                                                                    mode = hdict({'drinkActive': drinkActive, 'playerFoodPoints': playerFoodPoints, 'foodActive': foodActive, 'drinkPos': drinkPos, 'foodPos': foodPos, 'playerPos': playerPos, 'notReachedExit': notReachedExit, 'gameOver': gameOver})
                                                                    yield event('check food collisions', mode, sub, add)

def addsucc_003 (marking, succ):
    "successors of 'check gameover'"
    if marking('checkHealth') and marking('gameOver'):
        for checkHealth in marking('checkHealth'):
            for gameOver in marking('gameOver'):
                if isinstance(gameOver, bool):
                    a = checkGameOver(gameOver, False)
                    b = checkGameOver(gameOver, True)
                    test = Marking({'gameOver': mset([gameOver]), 'checkHealth': mset([checkHealth])})
                    if test <= marking:
                        sub = Marking({'checkHealth': mset([checkHealth])})
                        if(a == None):
                            add = Marking({'resetGame': mset([b])})
                        elif(b == None):
                            add = Marking({'playerTurn': mset([a])})
                        succ.add(marking - sub + add)

def succ_003 (marking):
    "successors of 'check gameover'"
    succ = set()
    addsucc_003(marking, succ)
    return succ

def itersucc_003 (marking):
    "successors of 'check gameover'"
    if marking('checkHealth') and marking('gameOver'):
        for checkHealth in marking('checkHealth'):
            for gameOver in marking('gameOver'):
                if isinstance(gameOver, bool):
                    a = checkGameOver(gameOver, False)
                    b = checkGameOver(gameOver, True)
                    test = Marking({'gameOver': mset([gameOver]), 'checkHealth': mset([checkHealth])})
                    if test <= marking:
                        sub = Marking({'checkHealth': mset([checkHealth])})
                        add = Marking({'playerTurn': mset([a]), 'resetGame': mset([b])})
                        mode = hdict({'checkHealth': checkHealth, 'gameOver': gameOver})
                        yield event('check gameover', mode, sub, add)

def addsucc_004 (marking, succ):
    "successors of 'execute player round'"
    if marking('playerTurn') and marking('gameOver'):
        for playerTurn in marking('playerTurn'):
            for gameOver in marking('gameOver'):
                a = canMove(gameOver)
                if isinstance(gameOver, bool) or a == None:
                    test = Marking({'gameOver': mset([gameOver]), 'playerTurn': mset([playerTurn])})
                    if test <= marking:
                        sub = Marking({'playerTurn': mset([playerTurn])})
                        if(a != None):
                            add = Marking({'movePlayer': mset([a])})
                            succ.add(marking - sub + add)
                        else:
                            succ.add(marking - sub)

def succ_004 (marking):
    "successors of 'execute player round'"
    succ = set()
    addsucc_004(marking, succ)
    return succ

def itersucc_004 (marking):
    "successors of 'execute player round'"
    if marking('playerTurn') and marking('gameOver'):
        for playerTurn in marking('playerTurn'):
            for gameOver in marking('gameOver'):
                a = canMove(gameOver)
                if isinstance(gameOver, bool):
                    test = Marking({'gameOver': mset([gameOver]), 'playerTurn': mset([playerTurn])})
                    if test <= marking:
                        sub = Marking({'playerTurn': mset([playerTurn])})
                        add = Marking({'movePlayer': mset([a])})
                        mode = hdict({'playerTurn': playerTurn, 'gameOver': gameOver})
                        yield event('execute player round', mode, sub, add)

def addsucc_005 (marking, succ):
    "successors of 'get enemies positions'"
    if marking('setupEnemies') and marking('availablePositions'):
        for setupEnemies in marking('setupEnemies'):
            for availablePositions in marking('availablePositions'):
                a = getPositions(availablePositions, 1)
                if isinstance(a, tuple):
                    sub = Marking({'setupEnemies': mset([setupEnemies]), 'availablePositions': mset([availablePositions])})
                    if sub <= marking:
                        add = Marking({'enemiesPositions': mset([a])})
                        succ.add(marking - sub + add)

def succ_005 (marking):
    "successors of 'get enemies positions'"
    succ = set()
    addsucc_005(marking, succ)
    return succ

def itersucc_005 (marking):
    "successors of 'get enemies positions'"
    if marking('setupEnemies') and marking('availablePositions'):
        for setupEnemies in marking('setupEnemies'):
            for availablePositions in marking('availablePositions'):
                a = getPositions(availablePositions, 1)
                if isinstance(a, tuple):
                    sub = Marking({'setupEnemies': mset([setupEnemies]), 'availablePositions': mset([availablePositions])})
                    if sub <= marking:
                        add = Marking({'enemiesPositions': mset([a])})
                        mode = hdict({'availablePositions': availablePositions, 'setupEnemies': setupEnemies})
                        yield event('get enemies positions', mode, sub, add)

def addsucc_006 (marking, succ):
    "successors of 'get foodTiles positions'"
    if marking('setupFood') and marking('availablePositions'):
        for setupFood in marking('setupFood'):
            for availablePositions in marking('availablePositions'):
                a = getPositions(availablePositions, 2)
                if isinstance(a, tuple):
                    if isinstance(availablePositions, tuple):
                        test = Marking({'availablePositions': mset([availablePositions]), 'setupFood': mset([setupFood])})
                        if test <= marking:
                            sub = Marking({'setupFood': mset([setupFood])})
                            add = Marking({'foodPositions': mset([a])})
                            succ.add(marking - sub + add)

def succ_006 (marking):
    "successors of 'get foodTiles positions'"
    succ = set()
    addsucc_006(marking, succ)
    return succ

def itersucc_006 (marking):
    "successors of 'get foodTiles positions'"
    if marking('setupFood') and marking('availablePositions'):
        for setupFood in marking('setupFood'):
            for availablePositions in marking('availablePositions'):
                a = getPositions(availablePositions, 2)
                if isinstance(a, tuple):
                    if isinstance(availablePositions, tuple):
                        test = Marking({'availablePositions': mset([availablePositions]), 'setupFood': mset([setupFood])})
                        if test <= marking:
                            sub = Marking({'setupFood': mset([setupFood])})
                            add = Marking({'foodPositions': mset([a])})
                            mode = hdict({'setupFood': setupFood, 'availablePositions': availablePositions})
                            yield event('get foodTiles positions', mode, sub, add)

def addsucc_007 (marking, succ):
    "successors of 'get wallTiles positions'"
    if marking('setupWalls') and marking('availablePositions'):
        for setupWalls in marking('setupWalls'):
            for availablePositions in marking('availablePositions'):
                a = getPositions(availablePositions, 1)
                if isinstance(a, tuple):
                    if isinstance(availablePositions, tuple):
                        test = Marking({'availablePositions': mset([availablePositions]), 'setupWalls': mset([setupWalls])})
                        if test <= marking:
                            sub = Marking({'setupWalls': mset([setupWalls])})
                            add = Marking({'wallPositions': mset([a])})
                            succ.add(marking - sub + add)

def succ_007 (marking):
    "successors of 'get wallTiles positions'"
    succ = set()
    addsucc_007(marking, succ)
    return succ

def itersucc_007 (marking):
    "successors of 'get wallTiles positions'"
    if marking('setupWalls') and marking('availablePositions'):
        for setupWalls in marking('setupWalls'):
            for availablePositions in marking('availablePositions'):
                a = getPositions(availablePositions, 1)
                if isinstance(a, tuple):
                    if isinstance(availablePositions, tuple):
                        test = Marking({'availablePositions': mset([availablePositions]), 'setupWalls': mset([setupWalls])})
                        if test <= marking:
                            sub = Marking({'setupWalls': mset([setupWalls])})
                            add = Marking({'wallPositions': mset([a])})
                            mode = hdict({'availablePositions': availablePositions, 'setupWalls': setupWalls})
                            yield event('get wallTiles positions', mode, sub, add)

def addsucc_008 (marking, succ):
    "successors of 'go to next level'"
    if marking('reachedExit') and marking('wall1Pos') and marking('foodPos') and marking('foodActive') and marking('drinkActive') and marking('boardBounds') and marking('levelCount') and marking('drinkPos') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for reachedExit in marking('reachedExit'):
            for playerPos in marking('playerPos'):
                for enemy1Pos in marking('enemy1Pos'):
                    for wall1Pos in marking('wall1Pos'):
                        for wall1Health in marking('wall1Health'):
                            for foodPos in marking('foodPos'):
                                for foodActive in marking('foodActive'):
                                    for drinkPos in marking('drinkPos'):
                                        for drinkActive in marking('drinkActive'):
                                            for levelCount in marking('levelCount'):
                                                for boardBounds in marking('boardBounds'):
                                                    a = generateListOfPositions(boardBounds)
                                                    if isinstance(a, tuple):
                                                        b = initPosition(0,0)
                                                        if isinstance(b, tuple):
                                                            c = increaseLevelCount(levelCount)
                                                            if isinstance(c, int):
                                                                if isinstance(boardBounds, tuple):
                                                                    d = 1
                                                                    test = Marking({'boardBounds': mset([boardBounds]), 'reachedExit': mset([reachedExit]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount])})
                                                                    if test <= marking:
                                                                        sub = Marking({'reachedExit': mset([reachedExit]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount])})
                                                                        add = Marking({'availablePositions': mset([a]), 'playerPos': mset([b]), 'levelCount': mset([c]), 'setupWalls': mset([d])})
                                                                        succ.add(marking - sub + add)

def succ_008 (marking):
    "successors of 'go to next level'"
    succ = set()
    addsucc_008(marking, succ)
    return succ

def itersucc_008 (marking):
    "successors of 'go to next level'"
    if marking('reachedExit') and marking('wall1Pos') and marking('foodPos') and marking('foodActive') and marking('drinkActive') and marking('boardBounds') and marking('levelCount') and marking('drinkPos') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for reachedExit in marking('reachedExit'):
            for playerPos in marking('playerPos'):
                for enemy1Pos in marking('enemy1Pos'):
                    for wall1Pos in marking('wall1Pos'):
                        for wall1Health in marking('wall1Health'):
                            for foodPos in marking('foodPos'):
                                for foodActive in marking('foodActive'):
                                    for drinkPos in marking('drinkPos'):
                                        for drinkActive in marking('drinkActive'):
                                            for levelCount in marking('levelCount'):
                                                for boardBounds in marking('boardBounds'):
                                                    a = generateListOfPositions(boardBounds)
                                                    if isinstance(a, tuple):
                                                        b = initPosition(0,0)
                                                        if isinstance(b, tuple):
                                                            c = increaseLevelCount(levelCount)
                                                            if isinstance(c, int):
                                                                if isinstance(boardBounds, tuple):
                                                                    d = 1
                                                                    test = Marking({'boardBounds': mset([boardBounds]), 'reachedExit': mset([reachedExit]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount])})
                                                                    if test <= marking:
                                                                        sub = Marking({'reachedExit': mset([reachedExit]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount])})
                                                                        add = Marking({'availablePositions': mset([a]), 'playerPos': mset([b]), 'levelCount': mset([c]), 'setupWalls': mset([d])})
                                                                        mode = hdict({'drinkActive': drinkActive, 'reachedExit': reachedExit, 'wall1Pos': wall1Pos, 'foodPos': foodPos, 'boardBounds': boardBounds, 'enemy1Pos': enemy1Pos, 'foodActive': foodActive, 'drinkPos': drinkPos, 'levelCount': levelCount, 'playerPos': playerPos, 'wall1Health': wall1Health})
                                                                        yield event('go to next level', mode, sub, add)

def addsucc_009 (marking, succ):
    "successors of 'layout enemies'"
    if marking('enemiesPositions'):
        for enemiesPositions in marking('enemiesPositions'):
            a = enemiesPositions[0]
            if isinstance(a, tuple):
                b = 1
                sub = Marking({'enemiesPositions': mset([enemiesPositions])})
                if sub <= marking:
                    add = Marking({'enemy1Pos': mset([a]), 'playerTurn': mset([b])})
                    succ.add(marking - sub + add)

def succ_009 (marking):
    "successors of 'layout enemies'"
    succ = set()
    addsucc_009(marking, succ)
    return succ

def itersucc_009 (marking):
    "successors of 'layout enemies'"
    if marking('enemiesPositions'):
        for enemiesPositions in marking('enemiesPositions'):
            a = enemiesPositions[0]
            if isinstance(a, tuple):
                b = 1
                sub = Marking({'enemiesPositions': mset([enemiesPositions])})
                if sub <= marking:
                    add = Marking({'enemy1Pos': mset([a]), 'playerTurn': mset([b])})
                    mode = hdict({'enemiesPositions': enemiesPositions})
                    yield event('layout enemies', mode, sub, add)

def addsucc_010 (marking, succ):
    "successors of 'layout foodTiles'"
    if marking('foodPositions') and marking('availablePositions'):
        for foodPositions in marking('foodPositions'):
            for availablePositions in marking('availablePositions'):
                a = removePositions(availablePositions, foodPositions)
                if isinstance(a, tuple):
                    b = returnRandomBool()
                    if isinstance(b, bool):
                        c = foodPositions[0]
                        if isinstance(c, tuple):
                            if isinstance(b, bool):
                                d = foodPositions[1]
                                if isinstance(d, tuple):
                                    e = 1
                                    sub = Marking({'foodPositions': mset([foodPositions]), 'availablePositions': mset([availablePositions])})
                                    if sub <= marking:
                                        add = Marking({'availablePositions': mset([a]), 'foodActive': mset([b]), 'foodPos': mset([c]), 'drinkActive': mset([b]), 'drinkPos': mset([d]), 'setupEnemies': mset([e])})
                                        succ.add(marking - sub + add)

def succ_010 (marking):
    "successors of 'layout foodTiles'"
    succ = set()
    addsucc_010(marking, succ)
    return succ

def itersucc_010 (marking):
    "successors of 'layout foodTiles'"
    if marking('foodPositions') and marking('availablePositions'):
        for foodPositions in marking('foodPositions'):
            for availablePositions in marking('availablePositions'):
                a = removePositions(availablePositions, foodPositions)
                if isinstance(a, tuple):
                    b = returnRandomBool()
                    if isinstance(b, bool):
                        c = foodPositions[0]
                        if isinstance(c, tuple):
                            if isinstance(b, bool):
                                d = foodPositions[1]
                                if isinstance(d, tuple):
                                    e = 1
                                    sub = Marking({'foodPositions': mset([foodPositions]), 'availablePositions': mset([availablePositions])})
                                    if sub <= marking:
                                        add = Marking({'availablePositions': mset([a]), 'foodActive': mset([b]), 'foodPos': mset([c]), 'drinkActive': mset([b]), 'drinkPos': mset([d]), 'setupEnemies': mset([e])})
                                        mode = hdict({'availablePositions': availablePositions, 'foodPositions': foodPositions})
                                        yield event('layout foodTiles', mode, sub, add)

def addsucc_011 (marking, succ):
    "successors of 'layout wallTiles'"
    if marking('availablePositions') and marking('wallPositions'):
        for wallPositions in marking('wallPositions'):
            for availablePositions in marking('availablePositions'):
                a = removePositions(availablePositions, wallPositions)
                if isinstance(a, tuple):
                    b = returnRandomInt(1, 3)
                    if isinstance(b, int):
                        c = wallPositions[0]
                        if isinstance(c, tuple):
                            if isinstance(b, int):
                                e = 1
                                sub = Marking({'wallPositions': mset([wallPositions]), 'availablePositions': mset([availablePositions])})
                                if sub <= marking:
                                    add = Marking({'availablePositions': mset([a]), 'wall1Health': mset([b]), 'wall1Pos': mset([c]), 'setupFood': mset([e])})
                                    succ.add(marking - sub + add)

def succ_011 (marking):
    "successors of 'layout wallTiles'"
    succ = set()
    addsucc_011(marking, succ)
    return succ

def itersucc_011 (marking):
    "successors of 'layout wallTiles'"
    if marking('availablePositions') and marking('wallPositions'):
        for wallPositions in marking('wallPositions'):
            for availablePositions in marking('availablePositions'):
                a = removePositions(availablePositions, wallPositions)
                if isinstance(a, tuple):
                    b = returnRandomInt(1, 3)
                    if isinstance(b, int):
                        c = wallPositions[0]
                        if isinstance(c, tuple):
                            if isinstance(b, int):
                                e = 1
                                sub = Marking({'wallPositions': mset([wallPositions]), 'availablePositions': mset([availablePositions])})
                                if sub <= marking:
                                    add = Marking({'availablePositions': mset([a]), 'wall1Health': mset([b]), 'wall1Pos': mset([c]), 'setupFood': mset([e])})
                                    mode = hdict({'wallPositions': wallPositions, 'availablePositions': availablePositions})
                                    yield event('layout wallTiles', mode, sub, add)

def addsucc_012 (marking, succ):
    "successors of 'move down'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (0,-1)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    succ.add(marking - sub + add)

def succ_012 (marking):
    "successors of 'move down'"
    succ = set()
    addsucc_012(marking, succ)
    return succ

def itersucc_012 (marking):
    "successors of 'move down'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (0,-1)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    mode = hdict({'movePlayer': movePlayer})
                    yield event('move down', mode, sub, add)

def addsucc_013 (marking, succ):
    "successors of 'move enemies'"
    if marking('enemiesTurn') and marking('wall1Pos') and marking('gameOver') and marking('playerFoodPoints') and marking('boardBounds') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for enemiesTurn in marking('enemiesTurn'):
            for boardBounds in marking('boardBounds'):
                for playerPos in marking('playerPos'):
                    for playerFoodPoints in marking('playerFoodPoints'):
                        for enemy1Pos in marking('enemy1Pos'):
                            for wall1Pos in marking('wall1Pos'):
                                for wall1Health in marking('wall1Health'):
                                    for gameOver in marking('gameOver'):
                                        if isinstance(playerPos, tuple):
                                            if isinstance(wall1Health, int):
                                                if isinstance(wall1Pos, tuple):
                                                    a = updateEnemyPosition(enemy1Pos, playerPos, wall1Pos, wall1Health, boardBounds)
                                                    if isinstance(a, tuple):
                                                        b = onEnemyAttack(enemy1Pos, playerPos, playerFoodPoints)
                                                        if isinstance(b, int):
                                                            if isinstance(boardBounds, tuple):
                                                                c = onEnemyAttackUpdateGameOver(gameOver, enemy1Pos, playerPos, playerFoodPoints)
                                                                if isinstance(c, bool):
                                                                    d = 1
                                                                    test = Marking({'wall1Pos': mset([wall1Pos]), 'boardBounds': mset([boardBounds]), 'playerPos': mset([playerPos]), 'wall1Health': mset([wall1Health]), 'enemiesTurn': mset([enemiesTurn]), 'playerFoodPoints': mset([playerFoodPoints]), 'enemy1Pos': mset([enemy1Pos]), 'gameOver': mset([gameOver])})
                                                                    if test <= marking:
                                                                        sub = Marking({'enemiesTurn': mset([enemiesTurn]), 'playerFoodPoints': mset([playerFoodPoints]), 'enemy1Pos': mset([enemy1Pos]), 'gameOver': mset([gameOver])})
                                                                        add = Marking({'enemy1Pos': mset([a]), 'playerFoodPoints': mset([b]), 'gameOver': mset([c]), 'checkHealth': mset([d])})
                                                                        succ.add(marking - sub + add)

def succ_013 (marking):
    "successors of 'move enemies'"
    succ = set()
    addsucc_013(marking, succ)
    return succ

def itersucc_013 (marking):
    "successors of 'move enemies'"
    if marking('enemiesTurn') and marking('wall1Pos') and marking('gameOver') and marking('playerFoodPoints') and marking('boardBounds') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for enemiesTurn in marking('enemiesTurn'):
            for boardBounds in marking('boardBounds'):
                for playerPos in marking('playerPos'):
                    for playerFoodPoints in marking('playerFoodPoints'):
                        for enemy1Pos in marking('enemy1Pos'):
                            for wall1Pos in marking('wall1Pos'):
                                for wall1Health in marking('wall1Health'):
                                    for gameOver in marking('gameOver'):
                                        if isinstance(playerPos, tuple):
                                            if isinstance(wall1Health, int):
                                                if isinstance(wall1Pos, tuple):
                                                    a = updateEnemyPosition(enemy1Pos, playerPos, wall1Pos, wall1Health, boardBounds)
                                                    if isinstance(a, tuple):
                                                        b = onEnemyAttack(enemy1Pos, playerPos, playerFoodPoints)
                                                        if isinstance(b, int):
                                                            if isinstance(boardBounds, tuple):
                                                                c = onEnemyAttackUpdateGameOver(gameOver, enemy1Pos, playerPos, playerFoodPoints)
                                                                if isinstance(c, bool):
                                                                    d = 1
                                                                    test = Marking({'wall1Pos': mset([wall1Pos]), 'boardBounds': mset([boardBounds]), 'playerPos': mset([playerPos]), 'wall1Health': mset([wall1Health]), 'enemiesTurn': mset([enemiesTurn]), 'playerFoodPoints': mset([playerFoodPoints]), 'enemy1Pos': mset([enemy1Pos]), 'gameOver': mset([gameOver])})
                                                                    if test <= marking:
                                                                        sub = Marking({'enemiesTurn': mset([enemiesTurn]), 'playerFoodPoints': mset([playerFoodPoints]), 'enemy1Pos': mset([enemy1Pos]), 'gameOver': mset([gameOver])})
                                                                        add = Marking({'enemy1Pos': mset([a]), 'playerFoodPoints': mset([b]), 'gameOver': mset([c]), 'checkHealth': mset([d])})
                                                                        mode = hdict({'enemiesTurn': enemiesTurn, 'wall1Pos': wall1Pos, 'playerFoodPoints': playerFoodPoints, 'boardBounds': boardBounds, 'gameOver': gameOver, 'enemy1Pos': enemy1Pos, 'playerPos': playerPos, 'wall1Health': wall1Health})
                                                                        yield event('move enemies', mode, sub, add)

def addsucc_014 (marking, succ):
    "successors of 'move left'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (-1,0)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    succ.add(marking - sub + add)

def succ_014 (marking):
    "successors of 'move left'"
    succ = set()
    addsucc_014(marking, succ)
    return succ

def itersucc_014 (marking):
    "successors of 'move left'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (-1,0)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    mode = hdict({'movePlayer': movePlayer})
                    yield event('move left', mode, sub, add)

def addsucc_015 (marking, succ):
    "successors of 'move right'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (1,0)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    succ.add(marking - sub + add)

def succ_015 (marking):
    "successors of 'move right'"
    succ = set()
    addsucc_015(marking, succ)
    return succ

def itersucc_015 (marking):
    "successors of 'move right'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (1,0)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    mode = hdict({'movePlayer': movePlayer})
                    yield event('move right', mode, sub, add)

def addsucc_016 (marking, succ):
    "successors of 'move up'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (0,1)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    succ.add(marking - sub + add)

def succ_016 (marking):
    "successors of 'move up'"
    succ = set()
    addsucc_016(marking, succ)
    return succ

def itersucc_016 (marking):
    "successors of 'move up'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = (0,1)
            if isinstance(a, tuple):
                sub = Marking({'movePlayer': mset([movePlayer])})
                if sub <= marking:
                    add = Marking({'moveVal': mset([a])})
                    mode = hdict({'movePlayer': movePlayer})
                    yield event('move up', mode, sub, add)

def addsucc_017 (marking, succ):
    "successors of 'onMove'"
    if marking('wall1Pos') and marking('moveVal') and marking('gameOver') and marking('playerFoodPoints') and marking('boardBounds') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for moveVal in marking('moveVal'):
            for boardBounds in marking('boardBounds'):
                for playerPos in marking('playerPos'):
                    for playerFoodPoints in marking('playerFoodPoints'):
                        for enemy1Pos in marking('enemy1Pos'):
                            for wall1Pos in marking('wall1Pos'):
                                for wall1Health in marking('wall1Health'):
                                    for gameOver in marking('gameOver'):
                                        a = onMovePlayer(moveVal, playerPos, enemy1Pos, wall1Pos, wall1Health, boardBounds)
                                        if isinstance(a, tuple):
                                            b = updateWallHealth(moveVal, playerPos, wall1Pos, wall1Health)
                                            if isinstance(b, int):
                                                if isinstance(wall1Pos, tuple):
                                                    if isinstance(enemy1Pos, tuple):
                                                        d = decreasePoints(playerFoodPoints, moveVal, playerPos, wall1Pos, wall1Health)
                                                        if isinstance(d, int):
                                                            if isinstance(boardBounds, tuple):
                                                                e = checkFoodPoints(playerFoodPoints, gameOver, moveVal, playerPos, wall1Pos, wall1Health)
                                                                if isinstance(e, bool):
                                                                    f = 1
                                                                    test = Marking({'wall1Pos': mset([wall1Pos]), 'boardBounds': mset([boardBounds]), 'enemy1Pos': mset([enemy1Pos]), 'moveVal': mset([moveVal]), 'playerPos': mset([playerPos]), 'playerFoodPoints': mset([playerFoodPoints]), 'wall1Health': mset([wall1Health]), 'gameOver': mset([gameOver])})
                                                                    if test <= marking:
                                                                        sub = Marking({'moveVal': mset([moveVal]), 'playerPos': mset([playerPos]), 'playerFoodPoints': mset([playerFoodPoints]), 'wall1Health': mset([wall1Health]), 'gameOver': mset([gameOver])})
                                                                        add = Marking({'playerPos': mset([a]), 'wall1Health': mset([b]), 'playerFoodPoints': mset([d]), 'gameOver': mset([e]), 'exitCollision': mset([f])})
                                                                        succ.add(marking - sub + add)

def succ_017 (marking):
    "successors of 'onMove'"
    succ = set()
    addsucc_017(marking, succ)
    return succ

def itersucc_017 (marking):
    "successors of 'onMove'"
    if marking('wall1Pos') and marking('moveVal') and marking('gameOver') and marking('playerFoodPoints') and marking('boardBounds') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for moveVal in marking('moveVal'):
            for boardBounds in marking('boardBounds'):
                for playerPos in marking('playerPos'):
                    for playerFoodPoints in marking('playerFoodPoints'):
                        for enemy1Pos in marking('enemy1Pos'):
                            for wall1Pos in marking('wall1Pos'):
                                for wall1Health in marking('wall1Health'):
                                    for gameOver in marking('gameOver'):
                                        a = onMovePlayer(moveVal, playerPos, enemy1Pos, wall1Pos, wall1Health, boardBounds)
                                        if isinstance(a, tuple):
                                            b = updateWallHealth(moveVal, playerPos, wall1Pos, wall1Health)
                                            if isinstance(b, int):
                                                if isinstance(wall1Pos, tuple):
                                                    if isinstance(enemy1Pos, tuple):
                                                        d = decreasePoints(playerFoodPoints)
                                                        if isinstance(d, int):
                                                            if isinstance(boardBounds, tuple):
                                                                e = checkFoodPoints(playerFoodPoints, gameOver, moveVal, playerPos, wall1Pos, wall1Health)
                                                                if isinstance(e, bool):
                                                                    f = 1
                                                                    test = Marking({'wall1Pos': mset([wall1Pos]), 'boardBounds': mset([boardBounds]), 'enemy1Pos': mset([enemy1Pos]), 'moveVal': mset([moveVal]), 'playerPos': mset([playerPos]), 'playerFoodPoints': mset([playerFoodPoints]), 'wall1Health': mset([wall1Health]), 'gameOver': mset([gameOver])})
                                                                    if test <= marking:
                                                                        sub = Marking({'moveVal': mset([moveVal]), 'playerPos': mset([playerPos]), 'playerFoodPoints': mset([playerFoodPoints]), 'wall1Health': mset([wall1Health]), 'gameOver': mset([gameOver])})
                                                                        add = Marking({'playerPos': mset([a]), 'wall1Health': mset([b]), 'playerFoodPoints': mset([d]), 'gameOver': mset([e]), 'exitCollision': mset([f])})
                                                                        mode = hdict({'wall1Pos': wall1Pos, 'playerFoodPoints': playerFoodPoints, 'boardBounds': boardBounds, 'moveVal': moveVal, 'gameOver': gameOver, 'enemy1Pos': enemy1Pos, 'playerPos': playerPos, 'wall1Health': wall1Health})
                                                                        yield event('onMove', mode, sub, add)

def addsucc_018 (marking, succ):
    "successors of 'restart game'"
    if marking('wall1Pos') and marking('foodPos') and marking('foodActive') and marking('drinkActive') and marking('gameOver') and marking('playerFoodPoints') and marking('boardBounds') and marking('levelCount') and marking('resetGame') and marking('drinkPos') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for resetGame in marking('resetGame'):
            for gameOver in marking('gameOver'):
                for playerPos in marking('playerPos'):
                    for enemy1Pos in marking('enemy1Pos'):
                        for wall1Pos in marking('wall1Pos'):
                            for wall1Health in marking('wall1Health'):
                                for foodPos in marking('foodPos'):
                                    for foodActive in marking('foodActive'):
                                        for drinkPos in marking('drinkPos'):
                                            for drinkActive in marking('drinkActive'):
                                                for levelCount in marking('levelCount'):
                                                    for boardBounds in marking('boardBounds'):
                                                        for playerFoodPoints in marking('playerFoodPoints'):
                                                            a = generateListOfPositions(boardBounds)
                                                            if isinstance(a, tuple):
                                                                b = 100
                                                                if isinstance(b, int):
                                                                    c = initPosition(0,0)
                                                                    if isinstance(c, tuple):
                                                                        d = False
                                                                        if isinstance(d, bool):
                                                                            e = 1
                                                                            if isinstance(e, int):
                                                                                if isinstance(boardBounds, tuple):
                                                                                    test = Marking({'boardBounds': mset([boardBounds]), 'resetGame': mset([resetGame]), 'gameOver': mset([gameOver]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount]), 'playerFoodPoints': mset([playerFoodPoints])})
                                                                                    if test <= marking:
                                                                                        sub = Marking({'resetGame': mset([resetGame]), 'gameOver': mset([gameOver]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount]), 'playerFoodPoints': mset([playerFoodPoints])})
                                                                                        add = Marking({'availablePositions': mset([a]), 'playerFoodPoints': mset([b]), 'playerPos': mset([c]), 'gameOver': mset([d]), 'levelCount': mset([e]), 'setupWalls': mset([e])})
                                                                                        succ.add(marking - sub + add)

def succ_018 (marking):
    "successors of 'restart game'"
    succ = set()
    addsucc_018(marking, succ)
    return succ

def itersucc_018 (marking):
    "successors of 'restart game'"
    if marking('wall1Pos') and marking('foodPos') and marking('foodActive') and marking('drinkActive') and marking('gameOver') and marking('playerFoodPoints') and marking('boardBounds') and marking('levelCount') and marking('resetGame') and marking('drinkPos') and marking('enemy1Pos') and marking('playerPos') and marking('wall1Health'):
        for resetGame in marking('resetGame'):
            for gameOver in marking('gameOver'):
                for playerPos in marking('playerPos'):
                    for enemy1Pos in marking('enemy1Pos'):
                        for wall1Pos in marking('wall1Pos'):
                            for wall1Health in marking('wall1Health'):
                                for foodPos in marking('foodPos'):
                                    for foodActive in marking('foodActive'):
                                        for drinkPos in marking('drinkPos'):
                                            for drinkActive in marking('drinkActive'):
                                                for levelCount in marking('levelCount'):
                                                    for boardBounds in marking('boardBounds'):
                                                        for playerFoodPoints in marking('playerFoodPoints'):
                                                            a = generateListOfPositions(boardBounds)
                                                            if isinstance(a, tuple):
                                                                b = 100
                                                                if isinstance(b, int):
                                                                    c = initPosition(0,0)
                                                                    if isinstance(c, tuple):
                                                                        d = False
                                                                        if isinstance(d, bool):
                                                                            e = 1
                                                                            if isinstance(e, int):
                                                                                if isinstance(boardBounds, tuple):
                                                                                    test = Marking({'boardBounds': mset([boardBounds]), 'resetGame': mset([resetGame]), 'gameOver': mset([gameOver]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount]), 'playerFoodPoints': mset([playerFoodPoints])})
                                                                                    if test <= marking: 
                                                                                        sub = Marking({'resetGame': mset([resetGame]), 'gameOver': mset([gameOver]), 'playerPos': mset([playerPos]), 'enemy1Pos': mset([enemy1Pos]), 'wall1Pos': mset([wall1Pos]), 'wall1Health': mset([wall1Health]), 'foodPos': mset([foodPos]), 'foodActive': mset([foodActive]), 'drinkPos': mset([drinkPos]), 'drinkActive': mset([drinkActive]), 'levelCount': mset([levelCount]), 'playerFoodPoints': mset([playerFoodPoints])})
                                                                                        add = Marking({'availablePositions': mset([a]), 'playerFoodPoints': mset([b]), 'playerPos': mset([c]), 'gameOver': mset([d]), 'levelCount': mset([e]), 'setupWalls': mset([e])})
                                                                                        mode = hdict({'drinkActive': drinkActive, 'wall1Pos': wall1Pos, 'foodPos': foodPos, 'playerFoodPoints': playerFoodPoints, 'boardBounds': boardBounds, 'gameOver': gameOver, 'enemy1Pos': enemy1Pos, 'resetGame': resetGame, 'foodActive': foodActive, 'drinkPos': drinkPos, 'levelCount': levelCount, 'playerPos': playerPos, 'wall1Health': wall1Health})
                                                                                        yield event('restart game', mode, sub, add)

def addsucc_019 (marking, succ):
    "successors of 'start game'"
    if marking('startGame') and marking('boardBounds'):
        for startGame in marking('startGame'):
            for boardBounds in marking('boardBounds'):
                if isinstance(boardBounds, tuple):
                    a = generateListOfPositions(boardBounds)
                    if isinstance(a, tuple):
                        b = initPosition(8,8)
                        if isinstance(b, tuple):
                            c = initPosition(0,0)
                            if isinstance(c, tuple):
                                d = 100
                                if isinstance(d, int):
                                    e = 1
                                    if isinstance(e, int):
                                        test = Marking({'boardBounds': mset([boardBounds]), 'startGame': mset([startGame])})
                                        if test <= marking:
                                            sub = Marking({'startGame': mset([startGame])})
                                            add = Marking({'availablePositions': mset([a]), 'exitPos': mset([b]), 'playerPos': mset([c]), 'playerFoodPoints': mset([d]), 'levelCount': mset([e]), 'setupWalls': mset([e])})
                                            succ.add(marking - sub + add)

def succ_019 (marking):
    "successors of 'start game'"
    succ = set()
    addsucc_019(marking, succ)
    return succ

def itersucc_019 (marking):
    "successors of 'start game'"
    if marking('startGame') and marking('boardBounds'):
        for startGame in marking('startGame'):
            for boardBounds in marking('boardBounds'):
                if isinstance(boardBounds, tuple):
                    a = generateListOfPositions(boardBounds)
                    if isinstance(a, tuple):
                        b = initPosition(8,8)
                        if isinstance(b, tuple):
                            c = initPosition(0,0)
                            if isinstance(c, tuple):
                                d = 100
                                if isinstance(d, int):
                                    e = 1
                                    if isinstance(e, int):
                                        test = Marking({'boardBounds': mset([boardBounds]), 'startGame': mset([startGame])})
                                        if test <= marking:
                                            sub = Marking({'startGame': mset([startGame])})
                                            add = Marking({'availablePositions': mset([a]), 'exitPos': mset([b]), 'playerPos': mset([c]), 'playerFoodPoints': mset([d]), 'levelCount': mset([e]), 'setupWalls': mset([e])})
                                            mode = hdict({'boardBounds': boardBounds, 'startGame': startGame})
                                            yield event('start game', mode, sub, add)

def addsucc (marking, succ):
    'successors for all transitions'
    addsucc_001(marking, succ)
    addsucc_002(marking, succ)
    addsucc_003(marking, succ)
    addsucc_004(marking, succ)
    addsucc_005(marking, succ)
    addsucc_006(marking, succ)
    addsucc_007(marking, succ)
    addsucc_008(marking, succ)
    addsucc_009(marking, succ)
    addsucc_010(marking, succ)
    addsucc_011(marking, succ)
    addsucc_012(marking, succ)
    addsucc_013(marking, succ)
    addsucc_014(marking, succ)
    addsucc_015(marking, succ)
    addsucc_016(marking, succ)
    addsucc_017(marking, succ)
    addsucc_018(marking, succ)
    addsucc_019(marking, succ)

def succ (marking):
    'successors for all transitions'
    succ = set()
    addsucc(marking, succ)
    return succ

def itersucc (marking):
    return itertools.chain(itersucc_001(marking),
                           itersucc_002(marking),
                           itersucc_003(marking),
                           itersucc_004(marking),
                           itersucc_005(marking),
                           itersucc_006(marking),
                           itersucc_007(marking),
                           itersucc_008(marking),
                           itersucc_009(marking),
                           itersucc_010(marking),
                           itersucc_011(marking),
                           itersucc_012(marking),
                           itersucc_013(marking),
                           itersucc_014(marking),
                           itersucc_015(marking),
                           itersucc_016(marking),
                           itersucc_017(marking),
                           itersucc_018(marking),
                           itersucc_019(marking))

def init ():
    'initial marking'
    return Marking({'startGame': mset([1]), 'boardBounds': mset([(0.0, 8.0, 0.0, 8.0)]), 'gameOver': mset([False])})

# map transitions names to successor procs
# '' maps to all-transitions proc
succproc = {'': addsucc,
            'check exit collisions': addsucc_001,
            'check food collisions': addsucc_002,
            'check gameover': addsucc_003,
            'execute player round': addsucc_004,
            'get enemies positions': addsucc_005,
            'get foodTiles positions': addsucc_006,
            'get wallTiles positions': addsucc_007,
            'go to next level': addsucc_008,
            'layout enemies': addsucc_009,
            'layout foodTiles': addsucc_010,
            'layout wallTiles': addsucc_011,
            'move down': addsucc_012,
            'move enemies': addsucc_013,
            'move left': addsucc_014,
            'move right': addsucc_015,
            'move up': addsucc_016,
            'onMove': addsucc_017,
            'restart game': addsucc_018,
            'start game': addsucc_019}

# map transitions names to successor funcs
# '' maps to all-transitions func
succfunc = {'': succ,
            'check exit collisions': succ_001,
            'check food collisions': succ_002,
            'check gameover': succ_003,
            'execute player round': succ_004,
            'get enemies positions': succ_005,
            'get foodTiles positions': succ_006,
            'get wallTiles positions': succ_007,
            'go to next level': succ_008,
            'layout enemies': succ_009,
            'layout foodTiles': succ_010,
            'layout wallTiles': succ_011,
            'move down': succ_012,
            'move enemies': succ_013,
            'move left': succ_014,
            'move right': succ_015,
            'move up': succ_016,
            'onMove': succ_017,
            'restart game': succ_018,
            'start game': succ_019}

# map transitions names to successor iterators
# '' maps to all-transitions iterator
succiter = {'': itersucc,
            'check exit collisions': itersucc_001,
            'check food collisions': itersucc_002,
            'check gameover': itersucc_003,
            'execute player round': itersucc_004,
            'get enemies positions': itersucc_005,
            'get foodTiles positions': itersucc_006,
            'get wallTiles positions': itersucc_007,
            'go to next level': itersucc_008,
            'layout enemies': itersucc_009,
            'layout foodTiles': itersucc_010,
            'layout wallTiles': itersucc_011,
            'move down': itersucc_012,
            'move enemies': itersucc_013,
            'move left': itersucc_014,
            'move right': itersucc_015,
            'move up': itersucc_016,
            'onMove': itersucc_017,
            'restart game': itersucc_018,
            'start game': itersucc_019}

def dumpmarking (m) :
    if hasattr(m, "ident") :
        return "[%s] %s" % (m.ident, {p : list(t) for p, t in m.items()})
    else :
        return str({p : list(t) for p, t in m.items()})

def statespace (print_states, print_succs, print_dead) :
    i = init()
    i.ident = 0
    todo = collections.deque([i])
    seen = {i : 0}
    dead = 0
    while todo:
        state = todo.popleft()
        succ = set()
        addsucc(state, succ)
        if not succ :
            dead += 1
        if (print_dead and not succ) or print_states :
            print(dumpmarking(state))
        for s in succ :
            if s in seen :
                s.ident = seen[s]
            else :
                s.ident = seen[s] = len(seen)
                todo.append(s)
            if print_succs :
                print(" >", dumpmarking(s))
    return len(seen), dead

def lts () :
    i = init()
    i.ident = 0
    todo = collections.deque([i])
    seen = {i : 0}
    while todo:
        state = todo.popleft()
        print(dumpmarking(state))
        for trans, mode, sub, add in itersucc(state) :
            succ = state - sub + add
            if succ in seen :
                succ.ident = seen[succ]
            else :
                succ.ident = seen[succ] = len(seen)
                todo.append(succ)
            print("@ %s = %s" % (trans, mode))
            print(" -", dumpmarking(sub))
            print(" +", dumpmarking(add))
            print(" >", dumpmarking(succ))

def main () :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="size",
                        default=False, action="store_true",
                        help="only print size")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", dest="mode", action="store_const", const="g",
                       help="print marking graph")
    group.add_argument("-l", dest="mode", action="store_const", const="l",
                       help="print LTS (detailled marking graph)")
    group.add_argument("-m", dest="mode", action="store_const", const="m",
                       help="only print markings")
    group.add_argument("-d", dest="mode", action="store_const", const="d",
                       help="only print deadlocks")
    args = parser.parse_args()
    if args.mode in "gml" and args.size :
        n, _ = statespace(False, False, False)
        print("%s reachable states" % n)
    elif args.mode == "d" and args.size :
        _, n = statespace(False, False, False)
        print("%s deadlocks" % n)
    elif args.mode == "g" :
        statespace(True, True, False)
    elif args.mode in "m" :
        statespace(True, False, False)
    elif args.mode in "d" :
        statespace(False, False, True)
    elif args.mode == "l" :
        lts()

if __name__ == '__main__':
    main()
