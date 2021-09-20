NET = 'net'
import itertools, collections
import random
from zinc.nets import Marking, mset, dot, hdict
event = collections.namedtuple('event', ['trans', 'mode', 'sub', 'add'])

def onGenerateLevel(spawnPoints):
  points = None
  if(len(spawnPoints) > 1):
    points = []
    selected = random.randint(0, len(spawnPoints) - 1)
    points.append(selected)
    
    while selected in points:
      selected = random.randint(0, len(spawnPoints) - 1)
    points.append(selected)

  return (spawnPoints[points[0]], spawnPoints[points[1]])

def createPosPoint(pos, distance):
  return (pos[0] + distance, pos[1])

def updateGravity(pos, mapTXRange, mapTBPos, isactive = True):
  if(isactive):
    if(pos[0] >= mapTXRange[0] and pos[0] <= mapTXRange[1]):
      if((pos[1] > (mapTBPos[0] + 1.0) and pos[1] <= (mapTBPos[1] - 0.5)) or 
         (pos[1] <= (mapTBPos[0] - 0.5)) or (pos[1] > (mapTBPos[1] + 1.0))):
        return (pos[0],pos[1] - 0.5)
      else:
        return pos
    else:
      return (pos[0],pos[1] - 0.5)
  else:
    return pos

def checkCollision(isCollisionObjectActive, returnVal, compVal):
  if isCollisionObjectActive == compVal:
    return returnVal

def resetCollisionEnter(isCollisionObjectActive, colEnter):
  if isCollisionObjectActive == False:
    return 0
  return colEnter
    
def onCollisionEnterWithEnemy(playerPos, enemyPos, colEnter):
  if(playerPos == enemyPos):
    return colEnter + 1
  else:
    return 0

def decreaseHealthWithEnemy(health, playerPos, enemyPos, colEnter):
  if((colEnter == 0) and playerPos == enemyPos):
    return health - 1
  else:
    return health

def onEnemyCollisionChecked(health, playerPos, enemyPos):
  if(playerPos == enemyPos):
    return health - 1
  else:
    return health

def setPotionActive(potionActive, playerPos, potionPos):
  if(potionActive and playerPos == potionPos):
    return False
  else:
    return potionActive

def increasePoints(item, playerPos, potionActive, potionPos, amount):
  if(potionActive and playerPos == potionPos):
    return item + amount 
  else:
    return item

def activateLE(item, playerPos, isActive, itemPos):
  if(isActive and playerPos == itemPos):
    return True 
  else:
    return item

def increaseHealthPoints(item, playerPos, potionActive, potionPos, amount):
  if(potionActive and playerPos == potionPos and (item < 6)):
    return item + amount 
  else:
    return item

def checkHasHat(playerPos, hasHat, hatPos):
  if(hasHat == False and playerPos == hatPos):
    return True 
  else:
    return hasHat

def onCollisionWithBigDamage(health, playerPos, enemyPos, enemyActive, skeletonPos, skeletonActive, bigDamage):
  if((enemyActive and enemyPos[0] >= bigDamage[0] and enemyPos[0] <= bigDamage[1] and enemyPos[1] >= bigDamage[2] and enemyPos[1] <= bigDamage[3]) or
    (playerPos[0] >= bigDamage[0] and playerPos[0] <= bigDamage[1] and playerPos[1] >= bigDamage[2] and playerPos[1] <= bigDamage[3]) or
    (skeletonActive and skeletonPos[0] >= bigDamage[0] and skeletonPos[0] <= bigDamage[1] and skeletonPos[1] >= bigDamage[2] and skeletonPos[1] <= bigDamage[3])):
    return health - 4000
  else:
    return health

def onBigDamageChecked(health, playerPos, enemyPos, enemyActive, skeletonPos, skeletonActive, bigDamage):
  if((enemyActive and enemyPos[0] >= bigDamage[0] and enemyPos[0] <= bigDamage[1] and enemyPos[1] >= bigDamage[2] and enemyPos[1] <= bigDamage[3]) or
    (playerPos[0] >= bigDamage[0] and playerPos[0] <= bigDamage[1] and playerPos[1] >= bigDamage[2] and playerPos[1] <= bigDamage[3]) or
    (skeletonActive and skeletonPos[0] >= bigDamage[0] and skeletonPos[0] <= bigDamage[1] and skeletonPos[1] >= bigDamage[2] and skeletonPos[1] <= bigDamage[3])):
    return 0
  else:
    return health

def isCollidiingWithTiles(playerPos,mapTXRange,mapTBPos,jumps):
  if((playerPos[0] >= mapTXRange[0] and playerPos[0] <= mapTXRange[1])  and 
     ((abs(playerPos[1] - (mapTBPos[0])) <= 1) or (abs(playerPos[1] - (mapTBPos[1])) <= 1) )):
    return 2
  else:
    return jumps

def onTilesChecked(playerPos,mapTXRange,mapTBPos,jumps):
  if((playerPos[0] >= mapTXRange[0] and playerPos[0] <= mapTXRange[1])  and 
     (abs(playerPos[1] - (mapTBPos[0])) <= 1) ):
    return 2
  else:
    return jumps


def checkFireball(fireballPos, enemy0Active, enemy0Pos, skeletonActive, skeletonPos, mapTBPosition, mapTXRange, val):
    if ((enemy0Active == True and fireballPos == enemy0Pos) or (skeletonActive == True and fireballPos == skeletonPos) or 
    ((fireballPos[0] >= mapTXRange[0] and fireballPos[0] <= mapTXRange[1]) and (fireballPos[1] == mapTBPosition[0] or fireballPos[1] == mapTBPosition[1]))) == val:
      if(val == True):
        if enemy0Active == True and fireballPos == enemy0Pos:
          return 1
        elif skeletonActive == True and fireballPos == skeletonPos:
          return 2
        elif((fireballPos[0] >= mapTXRange[0] and fireballPos[0] <= mapTXRange[1]) and (fireballPos[1] == mapTBPosition[0] or fireballPos[1] == mapTBPosition[1])):
          return 3
      else:
        return 0

def onFireballChecked(fireballPos, enemy0Active, enemy0Pos, enemy0Health, skeletonActive, skeletonPos, skeletonHealth):
    if (enemy0Active == True and fireballPos == enemy0Pos):
      return enemy0Health - 1
    if(skeletonActive == True and fireballPos == skeletonPos):
      return skeletonHealth - 1
    else:
      return 1

def onEnemyHitFireballSetActive(hitval, enemyActive, expected):
  if hitval == expected:
    return False
  else:
    return enemyActive

def onEnemyHitFireballSetHealth(hitval, enemyHealth, expected):
  if hitval == expected:
    return enemyHealth - 1
  else:
    return enemyHealth

def onFireballCollidedSetActive(hitval, fireballActive):
  if hitval == 0:
    return fireballActive
  else:
    return False

def onFireballCollidedPosition(hitval, fireballPos):
  if hitval == 0:
    return fireballPos

def canUseLaserEyes(laserEyes, expected):
  if laserEyes == expected:
    return 1

def onMouse0ClickedSetLaserEyesEndPos(playerPos):
  return (playerPos[0] + random.randint(-3,3), playerPos[1] + random.randint(-3,3))

def isHittingLaser(playerPos,lePos, enemyPos):
  m = 0
  if((lePos[0] - playerPos[0]) != 0):
    m = (lePos[1] - playerPos[1]) / (lePos[0] - playerPos[0])
  b = playerPos[1] - (playerPos[0] * m)
  if(((m*enemyPos[0]) + b) == enemyPos[1]):
    return True
  else:
    return False 

def checkEnemyHitLaser(playerPos,lePos, enemyPos, enemyActive):
  if(enemyActive and isHittingLaser(playerPos,lePos, enemyPos)):
    return False
  else:
    return enemyActive

def getDirection(inputVal, direction):
  if(inputVal != 0):
    return inputVal
  else:
    return direction

def calcMoveVal(inputVal,speeding):
  if(speeding == True):
    return inputVal * 2.0
  else:
    return inputVal * 1.0

def updatePositionX(position,moveVal,mapTBPosition,mapTXRange):
  if((position[1] == mapTBPosition[0] or position[1] == mapTBPosition[1])
    and ((position[0]) >= mapTXRange[0]
    and (position[0]) <= mapTXRange[1])):
    return position
  
  if((position[1] == mapTBPosition[0] or position[1] == mapTBPosition[1])
    and ((position[0] + moveVal) >= mapTXRange[0]
    and (position[0] + moveVal) <= mapTXRange[1])):
    return position
  
  return (position[0] + moveVal, position[1])

def moveEnemy(waitingCounter, enemyActive, enemyPos, enemyDirection, enemyPosA, enemyPosB, mapTBPosition,mapTXRange):
  if(enemyActive):
    if(waitingCounter > 0):
      return enemyPos
    if(enemyPos[0] == enemyPosA[0]):
      enemyDirection = 1
    if(enemyPos[0] == enemyPosB[0]):
      enemyDirection = -1
    if((enemyPos[0] + enemyDirection) >= enemyPosA[0] and (enemyPos[0] + enemyDirection) <= enemyPosB[0]):
      return updatePositionX(enemyPos, enemyDirection, mapTBPosition, mapTXRange)
    else:
      return enemyPos
  else:
    return enemyPos

def updateEnemyDirection(waitingCounter, enemyActive, enemyPos, enemyDirection, enemyPosA, enemyPosB):
  if(enemyActive):
    if(waitingCounter > 0):
      return enemyDirection
    if(enemyPos[0] == enemyPosA[0]):
      return 1
    if(enemyPos[0] == enemyPosB[0]):
      return -1
  return enemyDirection

def activateEnemyAwait(waitingCounter, enemyPos, enemyDirection, enemyActive, enemyPosA, enemyPosB):
  if(enemyActive):
    if(enemyPos[0] != enemyPosA[0] and enemyPos[0] != enemyPosB[0]):
      return 0
    
    if(enemyPos[0] == enemyPosA[0] and waitingCounter == 0 and enemyDirection == -1):
      return 2
    elif(enemyPos[0] == enemyPosA[0] and waitingCounter > 0 and enemyDirection == -1):
      return waitingCounter - 1

    if(enemyPos[0] == enemyPosB[0] and waitingCounter == 0 and enemyDirection == 1):
      return 2
    if(enemyPos[0] == enemyPosB[0] and waitingCounter > 0 and enemyDirection == 1):
      return waitingCounter - 1
    else:
      return waitingCounter
  else:
    return 0

def checkFireballActive(fireballActive, val):
  if fireballActive == val:
    return 1

def updateFireballPosition(fireballPosition, fireballDirection):
  return (fireballPosition[0] + (fireballDirection * 2), fireballPosition[1])

def showBlackScreen(health, showGOScreen):
  if(health <= 0 and showGOScreen == False):
    return True
  else:
    return showGOScreen

def onJumped(jumps):
  if(jumps > 0):
    return jumps - 1
  else:
    return jumps

def jump(jumps, playerPos, mapTXRange, mapTBPos):
  if(jumps > 0):
    if((playerPos[0] >= mapTXRange[0] and playerPos[0] <= mapTXRange[1]) and ((playerPos[1] == mapTBPos[0]) or (playerPos[1] == mapTBPos[1]))):
      return playerPos
    if((playerPos[0] >= mapTXRange[0] and playerPos[0] <= mapTXRange[1]) and (playerPos[1] < mapTBPos[0]) and ((playerPos[1] + 1.5 ) > (mapTBPos[0] - 0.5))):
      return (playerPos[0], mapTBPos[0] - 0.5) 
    else:
      if((playerPos[0] >= mapTXRange[0] and playerPos[0] <= mapTXRange[1]) and (playerPos[1] < mapTBPos[1]) and ((playerPos[1] + 1.5 ) > (mapTBPos[1] - 0.5))):
        return (playerPos[0], mapTBPos[1] - 0.5) 
      else:
        return (playerPos[0], playerPos[1] + 1.5) 
  else:
    return playerPos

def tryTeleport(teleports):
  if(teleports > 0):
    return teleports - 1
  else: 
    return teleports

def onTeleported(teleports, playerPos):
  if(teleports > 0):
    return (playerPos[0] + random.randint(-3,3), playerPos[1] + random.randint(-3,3))
  else:
    return playerPos

def canCreateFireball(fireballs, expected):
  if((fireballs > 0) == expected):
    return 1

def onFired(fireBalls):
  if(fireBalls > 0):
    return fireBalls - 1
  return fireBalls

def initFireballPosition(fireBalls, playerPosition, direction):
  if(fireBalls > 0):
    pos = direction * 2
    return (playerPosition[0] + pos, playerPosition[1])

def addsucc_001 (marking, succ):
    "successors of 'arrow clicked'"
    if marking('playerInput'):
        for playerInput in marking('playerInput'):
            a = 1
            sub = Marking({'playerInput': mset([playerInput])})
            if sub <= marking:
                add = Marking({'arrowClicked': mset([a])})
                succ.add(marking - sub + add)

def succ_001 (marking):
    "successors of 'arrow clicked'"
    succ = set()
    addsucc_001(marking, succ)
    return succ

def itersucc_001 (marking):
    "successors of 'arrow clicked'"
    if marking('playerInput'):
        for playerInput in marking('playerInput'):
            a = 1
            sub = Marking({'playerInput': mset([playerInput])})
            if sub <= marking:
                add = Marking({'arrowClicked': mset([a])})
                mode = hdict({'playerInput': playerInput})
                yield event('arrow clicked', mode, sub, add)

def addsucc_002 (marking, succ):
    "successors of 'check collision with big damage'"
    if marking('enemy0Position') and marking('health') and marking('playerPosition') and marking('skeletonPosition') and marking('enemy0Active') and marking('withBigDamage') and marking('bigDamage') and marking('skeletonActive'):
        for withBigDamage in marking('withBigDamage'):
            for playerPosition in marking('playerPosition'):
                for bigDamage in marking('bigDamage'):
                    for health in marking('health'):
                        for enemy0Active in marking('enemy0Active'):
                            for enemy0Position in marking('enemy0Position'):
                                for skeletonActive in marking('skeletonActive'):
                                    for skeletonPosition in marking('skeletonPosition'):
                                        if isinstance(bigDamage, tuple):
                                            if isinstance(playerPosition, tuple):
                                                if isinstance(enemy0Active, bool):
                                                    if isinstance(enemy0Position, tuple):
                                                        if isinstance(skeletonActive, bool):
                                                            if isinstance(skeletonPosition, tuple):
                                                                a = onCollisionWithBigDamage(health, playerPosition, enemy0Position, enemy0Active, skeletonPosition, skeletonActive, bigDamage)
                                                                if isinstance(a, int):
                                                                    b = onBigDamageChecked(health, playerPosition, enemy0Position, enemy0Active, skeletonPosition, skeletonActive, bigDamage)
                                                                    test = Marking({'skeletonActive': mset([skeletonActive]), 'enemy0Active': mset([enemy0Active]), 'bigDamage': mset([bigDamage]), 'playerPosition': mset([playerPosition]), 'skeletonPosition': mset([skeletonPosition]), 'enemy0Position': mset([enemy0Position]), 'withBigDamage': mset([withBigDamage]), 'health': mset([health])})
                                                                    if test <= marking:
                                                                        sub = Marking({'withBigDamage': mset([withBigDamage]), 'health': mset([health])})
                                                                        add = Marking({'health': mset([a]), 'healthWithDamage': mset([a]), 'bigDamageChecked': mset([b])})
                                                                        succ.add(marking - sub + add)

def succ_002 (marking):
    "successors of 'check collision with big damage'"
    succ = set()
    addsucc_002(marking, succ)
    return succ

def itersucc_002 (marking):
    "successors of 'check collision with big damage'"
    if marking('enemy0Position') and marking('withBigDamage') and marking('skeletonActive') and marking('playerPosition') and marking('skeletonPosition') and marking('enemy0Active') and marking('health') and marking('bigDamage'):
        for withBigDamage in marking('withBigDamage'):
            for playerPosition in marking('playerPosition'):
                for bigDamage in marking('bigDamage'):
                    for health in marking('health'):
                        for enemy0Active in marking('enemy0Active'):
                            for enemy0Position in marking('enemy0Position'):
                                for skeletonActive in marking('skeletonActive'):
                                    for skeletonPosition in marking('skeletonPosition'):
                                        if isinstance(bigDamage, tuple):
                                            if isinstance(playerPosition, tuple):
                                                if isinstance(enemy0Active, bool):
                                                    if isinstance(enemy0Position, tuple):
                                                        if isinstance(skeletonActive, bool):
                                                            if isinstance(skeletonPosition, tuple):
                                                                a = onCollisionWithBigDamage(health, playerPosition, enemy0Position, enemy0Active, skeletonPosition, skeletonActive, bigDamage)
                                                                if isinstance(a, int):
                                                                    b = onBigDamageChecked(health, playerPosition, enemy0Position, enemy0Active, skeletonPosition, skeletonActive, bigDamage)
                                                                    test = Marking({'enemy0Position': mset([enemy0Position]), 'skeletonActive': mset([skeletonActive]), 'skeletonPosition': mset([skeletonPosition]), 'playerPosition': mset([playerPosition]), 'enemy0Active': mset([enemy0Active]), 'bigDamage': mset([bigDamage]), 'withBigDamage': mset([withBigDamage]), 'health': mset([health])})
                                                                    if test <= marking:
                                                                        sub = Marking({'withBigDamage': mset([withBigDamage]), 'health': mset([health])})
                                                                        add = Marking({'health': mset([a]), 'bigDamageChecked': mset([b])})
                                                                        mode = hdict({'enemy0Position': enemy0Position, 'playerPosition': playerPosition, 'withBigDamage': withBigDamage, 'skeletonActive': skeletonActive, 'skeletonPosition': skeletonPosition, 'enemy0Active': enemy0Active, 'health': health, 'bigDamage': bigDamage})
                                                                        yield event('check collision with big damage', mode, sub, add)

def addsucc_003 (marking, succ):
    "successors of 'check collision with enemy'"
    if marking('enemy0Active') and marking('health') and marking('collisionEnterEnemy') and marking('withEnemy'):
        for withEnemy in marking('withEnemy'):
            for enemy0Active in marking('enemy0Active'):
                for health in marking('health'):
                    for collisionEnterEnemy in marking('collisionEnterEnemy'):
                        if isinstance(enemy0Active, bool):
                            if isinstance(health, int):
                                a = checkCollision(enemy0Active, 1, True)
                                b = checkCollision(enemy0Active, health, False)
                                c = resetCollisionEnter(enemy0Active, collisionEnterEnemy)
                                if isinstance(c, int):
                                    test = Marking({'enemy0Active': mset([enemy0Active]), 'health': mset([health]), 'withEnemy': mset([withEnemy]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                    if test <= marking:
                                        sub = Marking({'withEnemy': mset([withEnemy]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                        if(a == None):
                                            add = Marking({'enemyChecked': mset([b]), 'collisionEnterEnemy': mset([c])})
                                        elif(b == None):
                                            add = Marking({'checkEnemy': mset([a]), 'collisionEnterEnemy': mset([c])})
                                        succ.add(marking - sub + add)

def succ_003 (marking):
    "successors of 'check collision with enemy'"
    succ = set()
    addsucc_003(marking, succ)
    return succ

def itersucc_003 (marking):
    "successors of 'check collision with enemy'"
    if marking('enemy0Active') and marking('health') and marking('collisionEnterEnemy') and marking('withEnemy'):
        for withEnemy in marking('withEnemy'):
            for enemy0Active in marking('enemy0Active'):
                for health in marking('health'):
                    for collisionEnterEnemy in marking('collisionEnterEnemy'):
                        if isinstance(enemy0Active, bool):
                            if isinstance(health, int):
                                a = checkCollision(enemy0Active, 1, True)
                                b = checkCollision(enemy0Active, health, False)
                                c = resetCollisionEnter(enemy0Active, collisionEnterEnemy)
                                if isinstance(c, int):
                                    test = Marking({'enemy0Active': mset([enemy0Active]), 'health': mset([health]), 'withEnemy': mset([withEnemy]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                    if test <= marking:
                                        sub = Marking({'withEnemy': mset([withEnemy]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                        add = Marking({'checkEnemy': mset([a]), 'enemyChecked': mset([b]), 'collisionEnterEnemy': mset([c])})
                                        mode = hdict({'enemy0Active': enemy0Active, 'health': health, 'collisionEnterEnemy': collisionEnterEnemy, 'withEnemy': withEnemy})
                                        yield event('check collision with enemy', mode, sub, add)

def addsucc_004 (marking, succ):
    "successors of 'check collision with fbPotion'"
    if marking('withFireballPotion') and marking('fireBallPotionActive') and marking('fireBalls'):
        for withFireballPotion in marking('withFireballPotion'):
            for fireBallPotionActive in marking('fireBallPotionActive'):
                for fireBalls in marking('fireBalls'):
                    if isinstance(fireBallPotionActive, bool):
                        if isinstance(fireBalls, int):
                            a = checkCollision(fireBallPotionActive, 1, True)
                            b = checkCollision(fireBallPotionActive, fireBalls, False)
                            test = Marking({'fireBallPotionActive': mset([fireBallPotionActive]), 'fireBalls': mset([fireBalls]), 'withFireballPotion': mset([withFireballPotion])})
                            if test <= marking:
                                sub = Marking({'withFireballPotion': mset([withFireballPotion])})
                                if(a == None):
                                    add = Marking({'fireBallsChecked': mset([b])})
                                elif(b == None):
                                    add = Marking({'checkFireball': mset([a])})
                                succ.add(marking - sub + add)

def succ_004 (marking):
    "successors of 'check collision with fbPotion'"
    succ = set()
    addsucc_004(marking, succ)
    return succ

def itersucc_004 (marking):
    "successors of 'check collision with fbPotion'"
    if marking('withFireballPotion') and marking('fireBallPotionActive') and marking('fireBalls'):
        for withFireballPotion in marking('withFireballPotion'):
            for fireBallPotionActive in marking('fireBallPotionActive'):
                for fireBalls in marking('fireBalls'):
                    if isinstance(fireBallPotionActive, bool):
                        if isinstance(fireBalls, int):
                            a = checkCollision(fireBallPotionActive, 1, True)
                            b = checkCollision(fireBallPotionActive, fireBalls, False)
                            test = Marking({'fireBallPotionActive': mset([fireBallPotionActive]), 'fireBalls': mset([fireBalls]), 'withFireballPotion': mset([withFireballPotion])})
                            if test <= marking:
                                sub = Marking({'withFireballPotion': mset([withFireballPotion])})
                                add = Marking({'checkFireball': mset([a]), 'fireBallsChecked': mset([b])})
                                mode = hdict({'withFireballPotion': withFireballPotion, 'fireBallPotionActive': fireBallPotionActive, 'fireBalls': fireBalls})
                                yield event('check collision with fbPotion', mode, sub, add)

def addsucc_005 (marking, succ):
    "successors of 'check collision with hPotion'"
    if marking('withHealthPotion') and marking('healthPotionActive') and marking('health'):
        for withHealthPotion in marking('withHealthPotion'):
            for healthPotionActive in marking('healthPotionActive'):
                for health in marking('health'):
                    if isinstance(healthPotionActive, bool):
                        if isinstance(health, int):
                            a = checkCollision(healthPotionActive, health, True)
                            b = checkCollision(healthPotionActive, health, False)
                            test = Marking({'healthPotionActive': mset([healthPotionActive]), 'health': mset([health]), 'withHealthPotion': mset([withHealthPotion])})
                            if test <= marking:
                                sub = Marking({'withHealthPotion': mset([withHealthPotion])})
                                if(a == None):
                                    add = Marking({'healthChecked': mset([b])})
                                elif(b == None):
                                    add = Marking({'checkHealth': mset([a])})
                                succ.add(marking - sub + add)

def succ_005 (marking):
    "successors of 'check collision with hPotion'"
    succ = set()
    addsucc_005(marking, succ)
    return succ

def itersucc_005 (marking):
    "successors of 'check collision with hPotion'"
    if marking('withHealthPotion') and marking('healthPotionActive') and marking('health'):
        for withHealthPotion in marking('withHealthPotion'):
            for healthPotionActive in marking('healthPotionActive'):
                for health in marking('health'):
                    if isinstance(healthPotionActive, bool):
                        if isinstance(health, int):
                            a = checkCollision(healthPotionActive, health, True)
                            b = checkCollision(healthPotionActive, health, False)
                            test = Marking({'healthPotionActive': mset([healthPotionActive]), 'health': mset([health]), 'withHealthPotion': mset([withHealthPotion])})
                            if test <= marking:
                                sub = Marking({'withHealthPotion': mset([withHealthPotion])})
                                add = Marking({'checkHealth': mset([a]), 'healthChecked': mset([b])})
                                mode = hdict({'withHealthPotion': withHealthPotion, 'healthPotionActive': healthPotionActive, 'health': health})
                                yield event('check collision with hPotion', mode, sub, add)

def addsucc_006 (marking, succ):
    "successors of 'check collision with hat'"
    if marking('withHat') and marking('hasHat'):
        for withHat in marking('withHat'):
            for hasHat in marking('hasHat'):
                if isinstance(hasHat, bool):
                    a = checkCollision(hasHat, hasHat, False)
                    b = checkCollision(hasHat, hasHat, True)
                    test = Marking({'hasHat': mset([hasHat]), 'withHat': mset([withHat])})
                    if test <= marking:
                        sub = Marking({'withHat': mset([withHat])})
                        if(a == None):
                            add = Marking({'hatChecked': mset([b])})
                        elif(b == None):
                            add = Marking({'checkHat': mset([a])})
                        succ.add(marking - sub + add)

def succ_006 (marking):
    "successors of 'check collision with hat'"
    succ = set()
    addsucc_006(marking, succ)
    return succ

def itersucc_006 (marking):
    "successors of 'check collision with hat'"
    if marking('withHat') and marking('hasHat'):
        for withHat in marking('withHat'):
            for hasHat in marking('hasHat'):
                if isinstance(hasHat, bool):
                    a = checkCollision(hasHat, hasHat, False)
                    b = checkCollision(hasHat, hasHat, True)
                    test = Marking({'hasHat': mset([hasHat]), 'withHat': mset([withHat])})
                    if test <= marking:
                        sub = Marking({'withHat': mset([withHat])})
                        add = Marking({'checkHat': mset([a]), 'hatChecked': mset([b])})
                        mode = hdict({'withHat': withHat, 'hasHat': hasHat})
                        yield event('check collision with hat', mode, sub, add)

def addsucc_007 (marking, succ):
    "successors of 'check collision with le potion'"
    if marking('laserEyesPotionActive') and marking('laserEyes') and marking('withLaserEyesPotion'):
        for withLaserEyesPotion in marking('withLaserEyesPotion'):
            for laserEyesPotionActive in marking('laserEyesPotionActive'):
                for laserEyes in marking('laserEyes'):
                    if isinstance(laserEyesPotionActive, bool):
                        if isinstance(laserEyes, bool):
                            a = checkCollision(laserEyesPotionActive, laserEyes, True)
                            b = checkCollision(laserEyesPotionActive, laserEyes, False)
                            test = Marking({'laserEyesPotionActive': mset([laserEyesPotionActive]), 'laserEyes': mset([laserEyes]), 'withLaserEyesPotion': mset([withLaserEyesPotion])})
                            if test <= marking:
                                sub = Marking({'withLaserEyesPotion': mset([withLaserEyesPotion])})
                                if(a == None):
                                    add = Marking({'laserEyesChecked': mset([b])})
                                elif(b == None):
                                    add = Marking({'checkLaserEyes': mset([a])})
                                succ.add(marking - sub + add)

def succ_007 (marking):
    "successors of 'check collision with le potion'"
    succ = set()
    addsucc_007(marking, succ)
    return succ

def itersucc_007 (marking):
    "successors of 'check collision with le potion'"
    if marking('laserEyesPotionActive') and marking('laserEyes') and marking('withLaserEyesPotion'):
        for withLaserEyesPotion in marking('withLaserEyesPotion'):
            for laserEyesPotionActive in marking('laserEyesPotionActive'):
                for laserEyes in marking('laserEyes'):
                    if isinstance(laserEyesPotionActive, bool):
                        if isinstance(laserEyes, bool):
                            a = checkCollision(laserEyesPotionActive, laserEyes, True)
                            b = checkCollision(laserEyesPotionActive, laserEyes, False)
                            test = Marking({'laserEyesPotionActive': mset([laserEyesPotionActive]), 'laserEyes': mset([laserEyes]), 'withLaserEyesPotion': mset([withLaserEyesPotion])})
                            if test <= marking:
                                sub = Marking({'withLaserEyesPotion': mset([withLaserEyesPotion])})
                                add = Marking({'checkLaserEyes': mset([a]), 'laserEyesChecked': mset([b])})
                                mode = hdict({'laserEyesPotionActive': laserEyesPotionActive, 'laserEyes': laserEyes, 'withLaserEyesPotion': withLaserEyesPotion})
                                yield event('check collision with le potion', mode, sub, add)

def addsucc_008 (marking, succ):
    "successors of 'check collision with skeleton'"
    if marking('collisionEnterSkeleton') and marking('health') and marking('skeletonActive') and marking('withSkeleton'):
        for withSkeleton in marking('withSkeleton'):
            for skeletonActive in marking('skeletonActive'):
                for health in marking('health'):
                    for collisionEnterSkeleton in marking('collisionEnterSkeleton'):
                        if isinstance(skeletonActive, bool):
                            if isinstance(health, int):
                                a = checkCollision(skeletonActive, 1, True)
                                b = checkCollision(skeletonActive, health, False)
                                c = resetCollisionEnter(skeletonActive, collisionEnterSkeleton)
                                if isinstance(c, int):
                                    test = Marking({'health': mset([health]), 'skeletonActive': mset([skeletonActive]), 'withSkeleton': mset([withSkeleton]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                    if test <= marking:
                                        sub = Marking({'withSkeleton': mset([withSkeleton]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                        if(a == None):
                                            add = Marking({'skeletonChecked': mset([b]), 'collisionEnterSkeleton': mset([c])})
                                        elif(b == None):
                                            add = Marking({'checkSkeleton': mset([a]), 'collisionEnterSkeleton': mset([c])})
                                        
                                        succ.add(marking - sub + add)

def succ_008 (marking):
    "successors of 'check collision with skeleton'"
    succ = set()
    addsucc_008(marking, succ)
    return succ

def itersucc_008 (marking):
    "successors of 'check collision with skeleton'"
    if marking('collisionEnterSkeleton') and marking('health') and marking('skeletonActive') and marking('withSkeleton'):
        for withSkeleton in marking('withSkeleton'):
            for skeletonActive in marking('skeletonActive'):
                for health in marking('health'):
                    for collisionEnterSkeleton in marking('collisionEnterSkeleton'):
                        if isinstance(skeletonActive, bool):
                            if isinstance(health, int):
                                a = checkCollision(skeletonActive, 1, True)
                                b = checkCollision(skeletonActive, health, False)
                                c = resetCollisionEnter(skeletonActive, collisionEnterSkeleton)
                                if isinstance(c, int):
                                    test = Marking({'health': mset([health]), 'skeletonActive': mset([skeletonActive]), 'withSkeleton': mset([withSkeleton]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                    if test <= marking:
                                        sub = Marking({'withSkeleton': mset([withSkeleton]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                        add = Marking({'checkSkeleton': mset([a]), 'skeletonChecked': mset([b]), 'collisionEnterSkeleton': mset([c])})
                                        mode = hdict({'collisionEnterSkeleton': collisionEnterSkeleton, 'health': health, 'skeletonActive': skeletonActive, 'withSkeleton': withSkeleton})
                                        yield event('check collision with skeleton', mode, sub, add)

def addsucc_009 (marking, succ):
    "successors of 'check collision with tPotion'"
    if marking('teleportPotionActive') and marking('teleports') and marking('withTeleportPotion'):
        for withTeleportPotion in marking('withTeleportPotion'):
            for teleportPotionActive in marking('teleportPotionActive'):
                for teleports in marking('teleports'):
                    if isinstance(teleportPotionActive, bool):
                        if isinstance(teleports, int):
                            a = checkCollision(teleportPotionActive, 1, True)
                            b = checkCollision(teleportPotionActive, teleports, False)
                            test = Marking({'teleportPotionActive': mset([teleportPotionActive]), 'teleports': mset([teleports]), 'withTeleportPotion': mset([withTeleportPotion])})
                            if test <= marking:
                                sub = Marking({'withTeleportPotion': mset([withTeleportPotion])})
                                if(a == None):
                                    add = Marking({'teleportChecked': mset([b])})
                                elif(b == None):
                                    add = Marking({'checkTeleport': mset([a])})
                                succ.add(marking - sub + add)

def succ_009 (marking):
    "successors of 'check collision with tPotion'"
    succ = set()
    addsucc_009(marking, succ)
    return succ

def itersucc_009 (marking):
    "successors of 'check collision with tPotion'"
    if marking('teleportPotionActive') and marking('teleports') and marking('withTeleportPotion'):
        for withTeleportPotion in marking('withTeleportPotion'):
            for teleportPotionActive in marking('teleportPotionActive'):
                for teleports in marking('teleports'):
                    if isinstance(teleportPotionActive, bool):
                        if isinstance(teleports, int):
                            a = checkCollision(teleportPotionActive, 1, True)
                            b = checkCollision(teleportPotionActive, teleports, False)
                            test = Marking({'teleportPotionActive': mset([teleportPotionActive]), 'teleports': mset([teleports]), 'withTeleportPotion': mset([withTeleportPotion])})
                            if test <= marking:
                                sub = Marking({'withTeleportPotion': mset([withTeleportPotion])})
                                add = Marking({'checkTeleport': mset([a]), 'teleportChecked': mset([b])})
                                mode = hdict({'teleportPotionActive': teleportPotionActive, 'teleports': teleports, 'withTeleportPotion': withTeleportPotion})
                                yield event('check collision with tPotion', mode, sub, add)

def addsucc_010 (marking, succ):
    "successors of 'check collisions'"
    if marking('gravityUpdated'):
        for gravityUpdated in marking('gravityUpdated'):
            a = 1
            sub = Marking({'gravityUpdated': mset([gravityUpdated])})
            if sub <= marking:
                add = Marking({'withSkeleton': mset([a]), 'withFireballPotion': mset([a]), 'withLaserEyesPotion': mset([a]), 'withHealthPotion': mset([a]), 'withTeleportPotion': mset([a]), 'withHat': mset([a]), 'withEnemy': mset([a]), 'withBigDamage': mset([a]), 'withTiles': mset([a]), 'checkFireballCollision': mset([a])})
                succ.add(marking - sub + add)

def succ_010 (marking):
    "successors of 'check collisions'"
    succ = set()
    addsucc_010(marking, succ)
    return succ

def itersucc_010 (marking):
    "successors of 'check collisions'"
    if marking('gravityUpdated'):
        for gravityUpdated in marking('gravityUpdated'):
            a = 1
            sub = Marking({'gravityUpdated': mset([gravityUpdated])})
            if sub <= marking:
                add = Marking({'withSkeleton': mset([a]), 'withFireballPotion': mset([a]), 'withLaserEyesPotion': mset([a]), 'withHealthPotion': mset([a]), 'withTeleportPotion': mset([a]), 'withHat': mset([a]), 'withEnemy': mset([a]), 'withBigDamage': mset([a]), 'withTiles': mset([a]), 'checkFireballCollision': mset([a])})
                mode = hdict({'gravityUpdated': gravityUpdated})
                yield event('check collisions', mode, sub, add)

def addsucc_011 (marking, succ):
    "successors of 'check laser hit'"
    if marking('enemy0Position') and marking('skeletonActive') and marking('laserEyesEndPosition') and marking('playerPosition') and marking('skeletonPosition') and marking('enemy0Active'):
        for playerPosition in marking('playerPosition'):
            for laserEyesEndPosition in marking('laserEyesEndPosition'):
                for enemy0Active in marking('enemy0Active'):
                    for enemy0Position in marking('enemy0Position'):
                        for skeletonActive in marking('skeletonActive'):
                            for skeletonPosition in marking('skeletonPosition'):
                                if isinstance(playerPosition, tuple):
                                    a = checkEnemyHitLaser(playerPosition,laserEyesEndPosition, enemy0Position, enemy0Active)
                                    if isinstance(a, bool):
                                        if isinstance(enemy0Position, tuple):
                                            b = checkEnemyHitLaser(playerPosition,laserEyesEndPosition, skeletonPosition, skeletonActive)
                                            if isinstance(b, bool):
                                                if isinstance(skeletonPosition, tuple):
                                                    c = 1
                                                    test = Marking({'enemy0Position': mset([enemy0Position]), 'skeletonPosition': mset([skeletonPosition]), 'playerPosition': mset([playerPosition]), 'laserEyesEndPosition': mset([laserEyesEndPosition]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive])})
                                                    if test <= marking:
                                                        sub = Marking({'laserEyesEndPosition': mset([laserEyesEndPosition]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive])})
                                                        add = Marking({'enemy0Active': mset([a]), 'skeletonActive': mset([b]), 'laserChecked': mset([c])})
                                                        succ.add(marking - sub + add)

def succ_011 (marking):
    "successors of 'check laser hit'"
    succ = set()
    addsucc_011(marking, succ)
    return succ

def itersucc_011 (marking):
    "successors of 'check laser hit'"
    if marking('enemy0Position') and marking('skeletonActive') and marking('laserEyesEndPosition') and marking('playerPosition') and marking('skeletonPosition') and marking('enemy0Active'):
        for playerPosition in marking('playerPosition'):
            for laserEyesEndPosition in marking('laserEyesEndPosition'):
                for enemy0Active in marking('enemy0Active'):
                    for enemy0Position in marking('enemy0Position'):
                        for skeletonActive in marking('skeletonActive'):
                            for skeletonPosition in marking('skeletonPosition'):
                                if isinstance(playerPosition, tuple):
                                    a = checkEnemyHitLaser(playerPosition,laserEyesEndPosition, enemy0Position, enemy0Active)
                                    if isinstance(a, bool):
                                        if isinstance(enemy0Position, tuple):
                                            b = checkEnemyHitLaser(playerPosition,laserEyesEndPosition, skeletonPosition, skeletonActive)
                                            if isinstance(b, bool):
                                                if isinstance(skeletonPosition, tuple):
                                                    c = 1
                                                    test = Marking({'enemy0Position': mset([enemy0Position]), 'skeletonPosition': mset([skeletonPosition]), 'playerPosition': mset([playerPosition]), 'laserEyesEndPosition': mset([laserEyesEndPosition]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive])})
                                                    if test <= marking:
                                                        sub = Marking({'laserEyesEndPosition': mset([laserEyesEndPosition]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive])})
                                                        add = Marking({'enemy0Active': mset([a]), 'skeletonActive': mset([b]), 'laserChecked': mset([c])})
                                                        mode = hdict({'enemy0Position': enemy0Position, 'playerPosition': playerPosition, 'skeletonPosition': skeletonPosition, 'enemy0Active': enemy0Active, 'skeletonActive': skeletonActive, 'laserEyesEndPosition': laserEyesEndPosition})
                                                        yield event('check laser hit', mode, sub, add)

def addsucc_012 (marking, succ):
    "successors of 'check player health'"
    if marking('executePlayerUpdate') and marking('health') and marking('showGameoverUI'):
        for executePlayerUpdate in marking('executePlayerUpdate'):
            for showGameoverUI in marking('showGameoverUI'):
                for health in marking('health'):
                    if isinstance(health, int):
                        a = showBlackScreen(health, showGameoverUI)
                        if isinstance(a, bool):
                            test = Marking({'health': mset([health]), 'executePlayerUpdate': mset([executePlayerUpdate]), 'showGameoverUI': mset([showGameoverUI])})
                            if test <= marking:
                                sub = Marking({'executePlayerUpdate': mset([executePlayerUpdate]), 'showGameoverUI': mset([showGameoverUI])})
                                add = Marking({'showGameoverUI': mset([a]), 'checkSpace': mset([a])})
                                succ.add(marking - sub + add)

def succ_012 (marking):
    "successors of 'check player health'"
    succ = set()
    addsucc_012(marking, succ)
    return succ

def itersucc_012 (marking):
    "successors of 'check player health'"
    if marking('executePlayerUpdate') and marking('health') and marking('showGameoverUI'):
        for executePlayerUpdate in marking('executePlayerUpdate'):
            for showGameoverUI in marking('showGameoverUI'):
                for health in marking('health'):
                    if isinstance(health, int):
                        a = showBlackScreen(health, showGameoverUI)
                        if isinstance(a, bool):
                            test = Marking({'health': mset([health]), 'executePlayerUpdate': mset([executePlayerUpdate]), 'showGameoverUI': mset([showGameoverUI])})
                            if test <= marking:
                                sub = Marking({'executePlayerUpdate': mset([executePlayerUpdate]), 'showGameoverUI': mset([showGameoverUI])})
                                add = Marking({'showGameoverUI': mset([a]), 'checkSpace': mset([a])})
                                mode = hdict({'executePlayerUpdate': executePlayerUpdate, 'health': health, 'showGameoverUI': showGameoverUI})
                                yield event('check player health', mode, sub, add)

def addsucc_013 (marking, succ):
    "successors of 'checkFireballActive'"
    if marking('executeFireballUpdate') and marking('fireballActive'):
        for executeFireballUpdate in marking('executeFireballUpdate'):
            for fireballActive in marking('fireballActive'):
                if isinstance(fireballActive, bool):
                    a = checkFireballActive(fireballActive, True)
                    b = checkFireballActive(fireballActive, False)
                    test = Marking({'fireballActive': mset([fireballActive]), 'executeFireballUpdate': mset([executeFireballUpdate])})
                    if test <= marking:
                        sub = Marking({'executeFireballUpdate': mset([executeFireballUpdate])})
                        if(a == None):
                            add = Marking({'fireballUpdated': mset([b])})
                        elif(b == None):
                            add = Marking({'updateFireball': mset([a])})
                        succ.add(marking - sub + add)

def succ_013 (marking):
    "successors of 'checkFireballActive'"
    succ = set()
    addsucc_013(marking, succ)
    return succ

def itersucc_013 (marking):
    "successors of 'checkFireballActive'"
    if marking('executeFireballUpdate') and marking('fireballActive'):
        for executeFireballUpdate in marking('executeFireballUpdate'):
            for fireballActive in marking('fireballActive'):
                if isinstance(fireballActive, bool):
                    a = checkFireballActive(fireballActive, True)
                    b = checkFireballActive(fireballActive, False)
                    test = Marking({'fireballActive': mset([fireballActive]), 'executeFireballUpdate': mset([executeFireballUpdate])})
                    if test <= marking:
                        sub = Marking({'executeFireballUpdate': mset([executeFireballUpdate])})
                        add = Marking({'updateFireball': mset([a]), 'fireballUpdated': mset([b])})
                        mode = hdict({'executeFireballUpdate': executeFireballUpdate, 'fireballActive': fireballActive})
                        yield event('checkFireballActive', mode, sub, add)

def addsucc_014 (marking, succ):
    "successors of 'create enemies'"
    if marking('levelGenerated'):
        for levelGenerated in marking('levelGenerated'):
            a = levelGenerated[0]
            if isinstance(a, tuple):
                b = levelGenerated[1]
                if isinstance(b, tuple):
                    sub = Marking({'levelGenerated': mset([levelGenerated])})
                    if sub <= marking:
                        add = Marking({'createEnemy0': mset([a]), 'createSkeleton': mset([b])})
                        succ.add(marking - sub + add)

def succ_014 (marking):
    "successors of 'create enemies'"
    succ = set()
    addsucc_014(marking, succ)
    return succ

def itersucc_014 (marking):
    "successors of 'create enemies'"
    if marking('levelGenerated'):
        for levelGenerated in marking('levelGenerated'):
            a = levelGenerated[0]
            if isinstance(a, tuple):
                b = levelGenerated[1]
                if isinstance(b, tuple):
                    sub = Marking({'levelGenerated': mset([levelGenerated])})
                    if sub <= marking:
                        add = Marking({'createEnemy0': mset([a]), 'createSkeleton': mset([b])})
                        mode = hdict({'levelGenerated': levelGenerated})
                        yield event('create enemies', mode, sub, add)

def addsucc_015 (marking, succ):
    "successors of 'ctrl clicked'"
    if marking('speeding') and marking('checkCtrl'):
        for checkCtrl in marking('checkCtrl'):
            for speeding in marking('speeding'):
                a = True
                if isinstance(a, bool):
                    b = 1
                    sub = Marking({'checkCtrl': mset([checkCtrl]), 'speeding': mset([speeding])})
                    if sub <= marking:
                        add = Marking({'speeding': mset([a]), 'checkMouse0': mset([b])})
                        succ.add(marking - sub + add)

def succ_015 (marking):
    "successors of 'ctrl clicked'"
    succ = set()
    addsucc_015(marking, succ)
    return succ

def itersucc_015 (marking):
    "successors of 'ctrl clicked'"
    if marking('speeding') and marking('checkCtrl'):
        for checkCtrl in marking('checkCtrl'):
            for speeding in marking('speeding'):
                a = True
                if isinstance(a, bool):
                    b = 1
                    sub = Marking({'checkCtrl': mset([checkCtrl]), 'speeding': mset([speeding])})
                    if sub <= marking:
                        add = Marking({'speeding': mset([a]), 'checkMouse0': mset([b])})
                        mode = hdict({'speeding': speeding, 'checkCtrl': checkCtrl})
                        yield event('ctrl clicked', mode, sub, add)

def addsucc_016 (marking, succ):
    "successors of 'ctrl not clicked'"
    if marking('speeding') and marking('checkCtrl'):
        for checkCtrl in marking('checkCtrl'):
            for speeding in marking('speeding'):
                a = False
                if isinstance(a, bool):
                    b = 1
                    sub = Marking({'checkCtrl': mset([checkCtrl]), 'speeding': mset([speeding])})
                    if sub <= marking:
                        add = Marking({'speeding': mset([a]), 'checkMouse0': mset([b])})
                        succ.add(marking - sub + add)

def succ_016 (marking):
    "successors of 'ctrl not clicked'"
    succ = set()
    addsucc_016(marking, succ)
    return succ

def itersucc_016 (marking):
    "successors of 'ctrl not clicked'"
    if marking('speeding') and marking('checkCtrl'):
        for checkCtrl in marking('checkCtrl'):
            for speeding in marking('speeding'):
                a = False
                if isinstance(a, bool):
                    b = 1
                    sub = Marking({'checkCtrl': mset([checkCtrl]), 'speeding': mset([speeding])})
                    if sub <= marking:
                        add = Marking({'speeding': mset([a]), 'checkMouse0': mset([b])})
                        mode = hdict({'speeding': speeding, 'checkCtrl': checkCtrl})
                        yield event('ctrl not clicked', mode, sub, add)

def addsucc_017 (marking, succ):
    "successors of 'decrease enemy health'"
    if marking('fireballCollided') and marking('skeletonHealth') and marking('enemy0Active') and marking('skeletonPosition') and marking('fireballActive') and marking('fireballPosition') and marking('enemy0Position') and marking('enemy0Health') and marking('skeletonActive'):
        for fireballCollided in marking('fireballCollided'):
            for enemy0Position in marking('enemy0Position'):
                for enemy0Active in marking('enemy0Active'):
                    for skeletonPosition in marking('skeletonPosition'):
                        for skeletonActive in marking('skeletonActive'):
                            for fireballActive in marking('fireballActive'):
                                for fireballPosition in marking('fireballPosition'):
                                    for enemy0Health in marking('enemy0Health'):
                                        for skeletonHealth in marking('skeletonHealth'):
                                            a = onEnemyHitFireballSetActive(fireballCollided, enemy0Active, 1)
                                            if isinstance(a, bool):
                                                b = onEnemyHitFireballSetHealth(fireballCollided, enemy0Health, 1)
                                                if isinstance(b, int):
                                                    c = onFireballCollidedSetActive(fireballCollided, fireballActive)
                                                    if isinstance(c, bool):
                                                        if isinstance(fireballPosition, tuple):
                                                            d = onEnemyHitFireballSetActive(fireballCollided, skeletonActive, 2)
                                                            if isinstance(d, bool):
                                                                if isinstance(skeletonHealth, int):
                                                                    if isinstance(enemy0Position, tuple):
                                                                        if isinstance(skeletonPosition, tuple):
                                                                            e = onFireballChecked(fireballPosition, enemy0Active, enemy0Position, enemy0Health, skeletonActive, skeletonPosition, skeletonHealth)
                                                                            test = Marking({'enemy0Position': mset([enemy0Position]), 'fireballPosition': mset([fireballPosition]), 'skeletonPosition': mset([skeletonPosition]), 'skeletonHealth': mset([skeletonHealth]), 'fireballCollided': mset([fireballCollided]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive]), 'fireballActive': mset([fireballActive]), 'enemy0Health': mset([enemy0Health])})
                                                                            if test <= marking:
                                                                                sub = Marking({'fireballCollided': mset([fireballCollided]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive]), 'fireballActive': mset([fireballActive]), 'enemy0Health': mset([enemy0Health])})
                                                                                add = Marking({'enemy0Active': mset([a]), 'enemy0Health': mset([b]), 'fireballActive': mset([c]), 'skeletonActive': mset([d]), 'fireballChecked': mset([e])})
                                                                                succ.add(marking - sub + add)

def succ_017 (marking):
    "successors of 'decrease enemy health'"
    succ = set()
    addsucc_017(marking, succ)
    return succ

def itersucc_017 (marking):
    "successors of 'decrease enemy health'"
    if marking('enemy0Position') and marking('fireballPosition') and marking('skeletonHealth') and marking('skeletonActive') and marking('skeletonPosition') and marking('fireballCollided') and marking('enemy0Active') and marking('enemy0Health') and marking('fireballActive'):
        for fireballCollided in marking('fireballCollided'):
            for enemy0Position in marking('enemy0Position'):
                for enemy0Active in marking('enemy0Active'):
                    for skeletonPosition in marking('skeletonPosition'):
                        for skeletonActive in marking('skeletonActive'):
                            for fireballActive in marking('fireballActive'):
                                for fireballPosition in marking('fireballPosition'):
                                    for enemy0Health in marking('enemy0Health'):
                                        for skeletonHealth in marking('skeletonHealth'):
                                            a = onEnemyHitFireballSetActive(fireballCollided, enemy0Active, 1)
                                            if isinstance(a, bool):
                                                b = onEnemyHitFireballSetHealth(fireballCollided, enemy0Health, 1)
                                                if isinstance(b, int):
                                                    c = onFireballCollidedSetActive(fireballCollided, fireballActive)
                                                    if isinstance(c, bool):
                                                        d = onFireballCollidedPosition(fireballCollided, fireballPosition)
                                                        if isinstance(d, tuple):
                                                            e = onEnemyHitFireballSetActive(fireballCollided, enemy0Active, 2)
                                                            if isinstance(e, bool):
                                                                if isinstance(skeletonHealth, int):
                                                                    if isinstance(enemy0Position, tuple):
                                                                        if isinstance(skeletonPosition, tuple):
                                                                            f = onFireballChecked(fireballPosition, enemy0Active, enemy0Position, enemy0Health, skeletonActive, skeletonPosition, skeletonHealth)
                                                                            test = Marking({'enemy0Position': mset([enemy0Position]), 'skeletonHealth': mset([skeletonHealth]), 'skeletonPosition': mset([skeletonPosition]), 'fireballCollided': mset([fireballCollided]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive]), 'fireballActive': mset([fireballActive]), 'fireballPosition': mset([fireballPosition]), 'enemy0Health': mset([enemy0Health])})
                                                                            if test <= marking:
                                                                                sub = Marking({'fireballCollided': mset([fireballCollided]), 'enemy0Active': mset([enemy0Active]), 'skeletonActive': mset([skeletonActive]), 'fireballActive': mset([fireballActive]), 'fireballPosition': mset([fireballPosition]), 'enemy0Health': mset([enemy0Health])})
                                                                                add = Marking({'enemy0Active': mset([a]), 'enemy0Health': mset([b]), 'fireballActive': mset([c]), 'fireballPosition': mset([d]), 'skeletonActive': mset([e]), 'fireballChecked': mset([f])})
                                                                                mode = hdict({'enemy0Position': enemy0Position, 'fireballCollided': fireballCollided, 'skeletonHealth': skeletonHealth, 'skeletonActive': skeletonActive, 'skeletonPosition': skeletonPosition, 'fireballPosition': fireballPosition, 'enemy0Active': enemy0Active, 'enemy0Health': enemy0Health, 'fireballActive': fireballActive})
                                                                                yield event('decrease enemy health', mode, sub, add)

def addsucc_018 (marking, succ):
    "successors of 'execute fixed update'"
    if marking('healthWithSkeleton') and marking('skeletonChecked') and marking('laserEyesChecked') and marking('healCount') and marking('enemyChecked') and marking('healthChecked') and marking('teleportChecked') and marking('healthWithDamage') and marking('fireballChecked') and marking('fireBallsChecked') and marking('tilesChecked') and marking('bigDamageChecked') and marking('hatChecked') and marking('healthWithEnemy'):
        for skeletonChecked in marking('skeletonChecked'):
            for fireBallsChecked in marking('fireBallsChecked'):
                for laserEyesChecked in marking('laserEyesChecked'):
                    for healthChecked in marking('healthChecked'):
                        for teleportChecked in marking('teleportChecked'):
                            for hatChecked in marking('hatChecked'):
                                for enemyChecked in marking('enemyChecked'):
                                    for bigDamageChecked in marking('bigDamageChecked'):
                                        for tilesChecked in marking('tilesChecked'):
                                            for fireballChecked in marking('fireballChecked'):
                                                for healthWithEnemy in marking('healthWithEnemy'):
                                                    for healthWithSkeleton in marking('healthWithSkeleton'):
                                                        for healCount in marking('healCount'):
                                                            for healthWithDamage in marking('healthWithDamage'):
                                                                a = 1
                                                                sub = Marking({'skeletonChecked': mset([skeletonChecked]), 'fireBallsChecked': mset([fireBallsChecked]), 'laserEyesChecked': mset([laserEyesChecked]), 'healthChecked': mset([healthChecked]), 'teleportChecked': mset([teleportChecked]), 'hatChecked': mset([hatChecked]), 'enemyChecked': mset([enemyChecked]), 'bigDamageChecked': mset([bigDamageChecked]), 'tilesChecked': mset([tilesChecked]), 'fireballChecked': mset([fireballChecked]), 'healthWithEnemy': mset([healthWithEnemy]), 'healthWithSkeleton': mset([healthWithSkeleton]), 'healCount': mset([healCount]), 'healthWithDamage': mset([healthWithDamage])})
                                                                if sub <= marking:
                                                                    add = Marking({'usingLaserEyes': mset([a])})
                                                                    succ.add(marking - sub + add)

def succ_018 (marking):
    "successors of 'execute fixed update'"
    succ = set()
    addsucc_018(marking, succ)
    return succ

def itersucc_018 (marking):
    "successors of 'execute fixed update'"
    if marking('enemyChecked') and marking('fireballChecked') and marking('fireBallsChecked') and marking('laserEyesChecked') and marking('bigDamageChecked') and marking('hatChecked') and marking('skeletonChecked') and marking('teleportChecked') and marking('tilesChecked') and marking('healthChecked'):
        for skeletonChecked in marking('skeletonChecked'):
            for fireBallsChecked in marking('fireBallsChecked'):
                for laserEyesChecked in marking('laserEyesChecked'):
                    for healthChecked in marking('healthChecked'):
                        for teleportChecked in marking('teleportChecked'):
                            for hatChecked in marking('hatChecked'):
                                for enemyChecked in marking('enemyChecked'):
                                    for bigDamageChecked in marking('bigDamageChecked'):
                                        for tilesChecked in marking('tilesChecked'):
                                            for fireballChecked in marking('fireballChecked'):
                                                a = 1
                                                sub = Marking({'skeletonChecked': mset([skeletonChecked]), 'fireBallsChecked': mset([fireBallsChecked]), 'laserEyesChecked': mset([laserEyesChecked]), 'healthChecked': mset([healthChecked]), 'teleportChecked': mset([teleportChecked]), 'hatChecked': mset([hatChecked]), 'enemyChecked': mset([enemyChecked]), 'bigDamageChecked': mset([bigDamageChecked]), 'tilesChecked': mset([tilesChecked]), 'fireballChecked': mset([fireballChecked])})
                                                if sub <= marking:
                                                    add = Marking({'usingLaserEyes': mset([a])})
                                                    mode = hdict({'enemyChecked': enemyChecked, 'fireballChecked': fireballChecked, 'fireBallsChecked': fireBallsChecked, 'bigDamageChecked': bigDamageChecked, 'laserEyesChecked': laserEyesChecked, 'hatChecked': hatChecked, 'skeletonChecked': skeletonChecked, 'teleportChecked': teleportChecked, 'tilesChecked': tilesChecked, 'healthChecked': healthChecked})
                                                    yield event('execute fixed update', mode, sub, add)

def addsucc_019 (marking, succ):
    "successors of 'execute start'"
    if marking('startGame'):
        for startGame in marking('startGame'):
            a = 1
            sub = Marking({'startGame': mset([startGame])})
            if sub <= marking:
                add = Marking({'generateLevel': mset([a])})
                succ.add(marking - sub + add)

def succ_019 (marking):
    "successors of 'execute start'"
    succ = set()
    addsucc_019(marking, succ)
    return succ

def itersucc_019 (marking):
    "successors of 'execute start'"
    if marking('startGame'):
        for startGame in marking('startGame'):
            a = 1
            sub = Marking({'startGame': mset([startGame])})
            if sub <= marking:
                add = Marking({'generateLevel': mset([a])})
                mode = hdict({'startGame': startGame})
                yield event('execute start', mode, sub, add)

def addsucc_020 (marking, succ):
    "successors of 'execute update'"
    if marking('playerPosUpdated'):
        for playerPosUpdated in marking('playerPosUpdated'):
            a = 1
            sub = Marking({'playerPosUpdated': mset([playerPosUpdated])})
            if sub <= marking:
                add = Marking({'executeSkeletonUpdate': mset([a]), 'executeEnemyUpdate': mset([a]), 'executeFireballUpdate': mset([a]), 'executePlayerUpdate': mset([a])})
                succ.add(marking - sub + add)

def succ_020 (marking):
    "successors of 'execute update'"
    succ = set()
    addsucc_020(marking, succ)
    return succ

def itersucc_020 (marking):
    "successors of 'execute update'"
    if marking('playerPosUpdated'):
        for playerPosUpdated in marking('playerPosUpdated'):
            a = 1
            sub = Marking({'playerPosUpdated': mset([playerPosUpdated])})
            if sub <= marking:
                add = Marking({'executeSkeletonUpdate': mset([a]), 'executeEnemyUpdate': mset([a]), 'executeFireballUpdate': mset([a]), 'executePlayerUpdate': mset([a])})
                mode = hdict({'playerPosUpdated': playerPosUpdated})
                yield event('execute update', mode, sub, add)

def addsucc_021 (marking, succ):
    "successors of 'fire'"
    if marking('createFireball') and marking('direction') and marking('playerPosition') and marking('fireballActive') and marking('fireBalls'):
        for createFireball in marking('createFireball'):
            for fireballActive in marking('fireballActive'):
                for fireBalls in marking('fireBalls'):
                    for direction in marking('direction'):
                        for playerPosition in marking('playerPosition'):
                            a = onFired(fireBalls)
                            if isinstance(a, int):
                                b = True
                                if isinstance(b, bool):
                                    c = initFireballPosition(fireBalls, playerPosition, direction)
                                    if isinstance(c, tuple):
                                        if isinstance(direction, int):
                                            if isinstance(direction, int):
                                                if isinstance(playerPosition, tuple):
                                                    d = 1
                                                    test = Marking({'direction': mset([direction]), 'playerPosition': mset([playerPosition]), 'createFireball': mset([createFireball]), 'fireballActive': mset([fireballActive]), 'fireBalls': mset([fireBalls])})
                                                    if test <= marking:
                                                        sub = Marking({'createFireball': mset([createFireball]), 'fireballActive': mset([fireballActive]), 'fireBalls': mset([fireBalls])})
                                                        if(c == None):
                                                            add = Marking({'fireBalls': mset([a]), 'fireballActive': mset([b]), 'fireballDirection': mset([direction]), 'updateEnded': mset([d])})
                                                        else:
                                                            add = Marking({'fireBalls': mset([a]), 'fireballActive': mset([b]), 'fireballPosition': mset([c]), 'fireballDirection': mset([direction]), 'updateEnded': mset([d])})
                                                        succ.add(marking - sub + add)

def succ_021 (marking):
    "successors of 'fire'"
    succ = set()
    addsucc_021(marking, succ)
    return succ

def itersucc_021 (marking):
    "successors of 'fire'"
    if marking('playerPosition') and marking('direction') and marking('createFireball') and marking('fireBalls'):
        for createFireball in marking('createFireball'):
            for fireBalls in marking('fireBalls'):
                for direction in marking('direction'):
                    for playerPosition in marking('playerPosition'):
                        a = onFired(fireBalls)
                        if isinstance(a, int):
                            b = True
                            if isinstance(b, bool):
                                c = initFireballPosition(fireBalls, playerPosition, direction)
                                if isinstance(c, tuple):
                                    if isinstance(direction, int):
                                        d = 1
                                        sub = Marking({'createFireball': mset([createFireball]), 'fireBalls': mset([fireBalls]), 'direction': mset([direction]), 'playerPosition': mset([playerPosition])})
                                        if sub <= marking:
                                            add = Marking({'fireBalls': mset([a]), 'fireballActive': mset([b]), 'fireballPosition': mset([c]), 'fireballDirection': mset([direction]), 'updateEnded': mset([d])})
                                            mode = hdict({'playerPosition': playerPosition, 'direction': direction, 'createFireball': createFireball, 'fireBalls': fireBalls})
                                            yield event('fire', mode, sub, add)

def addsucc_022 (marking, succ):
    "successors of 'is fireball active'"
    if marking('checkFireballCollision') and marking('fireballActive'):
        for checkFireballCollision in marking('checkFireballCollision'):
            for fireballActive in marking('fireballActive'):
                if isinstance(fireballActive, bool):
                    a = checkFireballActive(fireballActive, True)
                    b = checkFireballActive(fireballActive, False)
                    test = Marking({'fireballActive': mset([fireballActive]), 'checkFireballCollision': mset([checkFireballCollision])})
                    if test <= marking:
                        sub = Marking({'checkFireballCollision': mset([checkFireballCollision])})
                        if(a == None):
                            add = Marking({'fireballChecked': mset([b])})
                        elif(b == None):
                            add = Marking({'checkfbcollision': mset([a])})
                        succ.add(marking - sub + add)

def succ_022 (marking):
    "successors of 'is fireball active'"
    succ = set()
    addsucc_022(marking, succ)
    return succ

def itersucc_022 (marking):
    "successors of 'is fireball active'"
    if marking('checkFireballCollision') and marking('fireballActive'):
        for checkFireballCollision in marking('checkFireballCollision'):
            for fireballActive in marking('fireballActive'):
                if isinstance(fireballActive, bool):
                    a = checkFireballActive(fireballActive, True)
                    b = checkFireballActive(fireballActive, False)
                    test = Marking({'fireballActive': mset([fireballActive]), 'checkFireballCollision': mset([checkFireballCollision])})
                    if test <= marking:
                        sub = Marking({'checkFireballCollision': mset([checkFireballCollision])})
                        add = Marking({'checkfbcollision': mset([a]), 'fireballChecked': mset([b])})
                        mode = hdict({'checkFireballCollision': checkFireballCollision, 'fireballActive': fireballActive})
                        yield event('is fireball active', mode, sub, add)

def addsucc_023 (marking, succ):
    "successors of 'left arrow clicked'"
    if marking('arrowClicked'):
        for arrowClicked in marking('arrowClicked'):
            a = -1
            if isinstance(a, int):
                sub = Marking({'arrowClicked': mset([arrowClicked])})
                if sub <= marking:
                    add = Marking({'inputValue': mset([a])})
                    succ.add(marking - sub + add)

def succ_023 (marking):
    "successors of 'left arrow clicked'"
    succ = set()
    addsucc_023(marking, succ)
    return succ

def itersucc_023 (marking):
    "successors of 'left arrow clicked'"
    if marking('arrowClicked'):
        for arrowClicked in marking('arrowClicked'):
            a = -1
            if isinstance(a, int):
                sub = Marking({'arrowClicked': mset([arrowClicked])})
                if sub <= marking:
                    add = Marking({'inputValue': mset([a])})
                    mode = hdict({'arrowClicked': arrowClicked})
                    yield event('left arrow clicked', mode, sub, add)

def addsucc_024 (marking, succ):
    "successors of 'mouse0 clicked fixed'"
    if marking('playerPosition') and marking('lasered') and marking('laserEyes'):
        for playerPosition in marking('playerPosition'):
            for laserEyes in marking('laserEyes'):
                for lasered in marking('lasered'):
                    if isinstance(playerPosition, tuple):
                        a = False
                        if isinstance(a, bool):
                            b = onMouse0ClickedSetLaserEyesEndPos(playerPosition)
                            if isinstance(b, tuple):
                                test = Marking({'playerPosition': mset([playerPosition]), 'laserEyes': mset([laserEyes]), 'lasered': mset([lasered])})
                                if test <= marking:
                                    sub = Marking({'laserEyes': mset([laserEyes]), 'lasered': mset([lasered])})
                                    add = Marking({'laserEyes': mset([a]), 'laserEyesEndPosition': mset([b])})
                                    succ.add(marking - sub + add)

def succ_024 (marking):
    "successors of 'mouse0 clicked fixed'"
    succ = set()
    addsucc_024(marking, succ)
    return succ

def itersucc_024 (marking):
    "successors of 'mouse0 clicked fixed'"
    if marking('playerPosition') and marking('lasered') and marking('laserEyes'):
        for playerPosition in marking('playerPosition'):
            for laserEyes in marking('laserEyes'):
                for lasered in marking('lasered'):
                    if isinstance(playerPosition, tuple):
                        a = False
                        if isinstance(a, bool):
                            b = onMouse0ClickedSetLaserEyesEndPos(playerPosition)
                            if isinstance(b, tuple):
                                test = Marking({'playerPosition': mset([playerPosition]), 'laserEyes': mset([laserEyes]), 'lasered': mset([lasered])})
                                if test <= marking:
                                    sub = Marking({'laserEyes': mset([laserEyes]), 'lasered': mset([lasered])})
                                    add = Marking({'laserEyes': mset([a]), 'laserEyesEndPosition': mset([b])})
                                    mode = hdict({'playerPosition': playerPosition, 'lasered': lasered, 'laserEyes': laserEyes})
                                    yield event('mouse0 clicked fixed', mode, sub, add)

def addsucc_025 (marking, succ):
    "successors of 'mouse0 not clicked fixed'"
    if marking('lasered'):
        for lasered in marking('lasered'):
            a = 1
            sub = Marking({'lasered': mset([lasered])})
            if sub <= marking:
                add = Marking({'laserChecked': mset([a])})
                succ.add(marking - sub + add)

def succ_025 (marking):
    "successors of 'mouse0 not clicked fixed'"
    succ = set()
    addsucc_025(marking, succ)
    return succ

def itersucc_025 (marking):
    "successors of 'mouse0 not clicked fixed'"
    if marking('lasered'):
        for lasered in marking('lasered'):
            a = 1
            sub = Marking({'lasered': mset([lasered])})
            if sub <= marking:
                add = Marking({'laserChecked': mset([a])})
                mode = hdict({'lasered': lasered})
                yield event('mouse0 not clicked fixed', mode, sub, add)

def addsucc_026 (marking, succ):
    "successors of 'move'"
    if marking('speeding') and marking('direction') and marking('inputValue'):
        for inputValue in marking('inputValue'):
            for direction in marking('direction'):
                for speeding in marking('speeding'):
                    a = getDirection(inputValue, direction)
                    if isinstance(a, int):
                        if isinstance(speeding, bool):
                            b = calcMoveVal(inputValue, speeding)
                            test = Marking({'speeding': mset([speeding]), 'inputValue': mset([inputValue]), 'direction': mset([direction])})
                            if test <= marking:
                                sub = Marking({'inputValue': mset([inputValue]), 'direction': mset([direction])})
                                add = Marking({'direction': mset([a]), 'moving': mset([b])})
                                succ.add(marking - sub + add)

def succ_026 (marking):
    "successors of 'move'"
    succ = set()
    addsucc_026(marking, succ)
    return succ

def itersucc_026 (marking):
    "successors of 'move'"
    if marking('speeding') and marking('direction') and marking('inputValue'):
        for inputValue in marking('inputValue'):
            for direction in marking('direction'):
                for speeding in marking('speeding'):
                    a = getDirection(inputValue, direction)
                    if isinstance(a, int):
                        if isinstance(speeding, bool):
                            b = calcMoveVal(inputValue, speeding)
                            test = Marking({'speeding': mset([speeding]), 'inputValue': mset([inputValue]), 'direction': mset([direction])})
                            if test <= marking:
                                sub = Marking({'inputValue': mset([inputValue]), 'direction': mset([direction])})
                                add = Marking({'direction': mset([a]), 'moving': mset([b])})
                                mode = hdict({'speeding': speeding, 'direction': direction, 'inputValue': inputValue})
                                yield event('move', mode, sub, add)

def addsucc_027 (marking, succ):
    "successors of 'nextIter'"
    if marking('updateEnded') and marking('fireballUpdated') and marking('skeletonPosUpdated') and marking('enemyPosUpdated'):
        for enemyPosUpdated in marking('enemyPosUpdated'):
            for skeletonPosUpdated in marking('skeletonPosUpdated'):
                for fireballUpdated in marking('fireballUpdated'):
                    for updateEnded in marking('updateEnded'):
                        a = 1
                        sub = Marking({'enemyPosUpdated': mset([enemyPosUpdated]), 'skeletonPosUpdated': mset([skeletonPosUpdated]), 'fireballUpdated': mset([fireballUpdated]), 'updateEnded': mset([updateEnded])})
                        if sub <= marking:
                            add = Marking({'physicsExecution': mset([a])})
                            succ.add(marking - sub + add)

def succ_027 (marking):
    "successors of 'nextIter'"
    succ = set()
    addsucc_027(marking, succ)
    return succ

def itersucc_027 (marking):
    "successors of 'nextIter'"
    if marking('updateEnded'):
        for updateEnded in marking('updateEnded'):
            a = 1
            sub = Marking({'updateEnded': mset([updateEnded])})
            if sub <= marking:
                add = Marking({'physicsExecution': mset([a])})
                mode = hdict({'updateEnded': updateEnded})
                yield event('nextIter', mode, sub, add)

def addsucc_028 (marking, succ):
    "successors of 'no laser'"
    if marking('notLasered'):
        for notLasered in marking('notLasered'):
            a = 1
            sub = Marking({'notLasered': mset([notLasered])})
            if sub <= marking:
                add = Marking({'laserChecked': mset([a])})
                succ.add(marking - sub + add)

def succ_028 (marking):
    "successors of 'no laser'"
    succ = set()
    addsucc_028(marking, succ)
    return succ

def itersucc_028 (marking):
    "successors of 'no laser'"
    if marking('notLasered'):
        for notLasered in marking('notLasered'):
            a = 1
            sub = Marking({'notLasered': mset([notLasered])})
            if sub <= marking:
                add = Marking({'laserChecked': mset([a])})
                mode = hdict({'notLasered': notLasered})
                yield event('no laser', mode, sub, add)

def addsucc_029 (marking, succ):
    "successors of 'on collision enemy'"
    if marking('health') and marking('enemy0Position') and marking('collisionEnterEnemy') and marking('checkEnemy') and marking('playerPosition'):
        for checkEnemy in marking('checkEnemy'):
            for playerPosition in marking('playerPosition'):
                for health in marking('health'):
                    for enemy0Position in marking('enemy0Position'):
                        for collisionEnterEnemy in marking('collisionEnterEnemy'):
                            if isinstance(enemy0Position, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = onCollisionEnterWithEnemy(playerPosition, enemy0Position, collisionEnterEnemy)
                                    if isinstance(a, int):
                                        b = decreaseHealthWithEnemy(health, playerPosition, enemy0Position, collisionEnterEnemy)
                                        if isinstance(b, int):
                                            c = onEnemyCollisionChecked(health, playerPosition, enemy0Position)
                                            test = Marking({'enemy0Position': mset([enemy0Position]), 'playerPosition': mset([playerPosition]), 'checkEnemy': mset([checkEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                            if test <= marking:
                                                sub = Marking({'checkEnemy': mset([checkEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                                add = Marking({'collisionEnterEnemy': mset([a]), 'health': mset([b]), 'healthWithEnemy': mset([b]), 'enemyChecked': mset([c])})
                                                succ.add(marking - sub + add)

def succ_029 (marking):
    "successors of 'on collision enemy'"
    succ = set()
    addsucc_029(marking, succ)
    return succ

def itersucc_029 (marking):
    "successors of 'on collision enemy'"
    if marking('enemy0Position') and marking('checkEnemy') and marking('collisionEnterEnemy') and marking('playerPosition') and marking('health'):
        for checkEnemy in marking('checkEnemy'):
            for playerPosition in marking('playerPosition'):
                for health in marking('health'):
                    for enemy0Position in marking('enemy0Position'):
                        for collisionEnterEnemy in marking('collisionEnterEnemy'):
                            if isinstance(enemy0Position, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = onCollisionEnterWithEnemy(playerPosition, enemy0Position, collisionEnterEnemy)
                                    if isinstance(a, int):
                                        b = decreaseHealthWithEnemy(health, playerPosition, enemy0Position, collisionEnterEnemy)
                                        if isinstance(b, int):
                                            c = onEnemyCollisionChecked(health, playerPosition, enemy0Position)
                                            test = Marking({'enemy0Position': mset([enemy0Position]), 'playerPosition': mset([playerPosition]), 'checkEnemy': mset([checkEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                            if test <= marking:
                                                sub = Marking({'checkEnemy': mset([checkEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                                add = Marking({'collisionEnterEnemy': mset([a]), 'health': mset([b]), 'enemyChecked': mset([c])})
                                                mode = hdict({'collisionEnterEnemy': collisionEnterEnemy, 'enemy0Position': enemy0Position, 'playerPosition': playerPosition, 'checkEnemy': checkEnemy, 'health': health})
                                                yield event('on collision enemy', mode, sub, add)

def addsucc_030 (marking, succ):
    "successors of 'on collision fbPotion'"
    if marking('fireBallPotionActive') and marking('fireballPotionPosition') and marking('checkFireball') and marking('playerPosition') and marking('fireBalls'):
        for checkFireball in marking('checkFireball'):
            for playerPosition in marking('playerPosition'):
                for fireBallPotionActive in marking('fireBallPotionActive'):
                    for fireBalls in marking('fireBalls'):
                        for fireballPotionPosition in marking('fireballPotionPosition'):
                            if isinstance(fireballPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(fireBallPotionActive, playerPosition, fireballPotionPosition)
                                    if isinstance(a, bool):
                                        b = increasePoints(fireBalls, playerPosition, fireBallPotionActive, fireballPotionPosition, 1)
                                        if isinstance(b, int):
                                            test = Marking({'fireballPotionPosition': mset([fireballPotionPosition]), 'playerPosition': mset([playerPosition]), 'checkFireball': mset([checkFireball]), 'fireBallPotionActive': mset([fireBallPotionActive]), 'fireBalls': mset([fireBalls])})
                                            if test <= marking:
                                                sub = Marking({'checkFireball': mset([checkFireball]), 'fireBallPotionActive': mset([fireBallPotionActive]), 'fireBalls': mset([fireBalls])})
                                                add = Marking({'fireBallPotionActive': mset([a]), 'fireBalls': mset([b]), 'fireBallsChecked': mset([b])})
                                                succ.add(marking - sub + add)

def succ_030 (marking):
    "successors of 'on collision fbPotion'"
    succ = set()
    addsucc_030(marking, succ)
    return succ

def itersucc_030 (marking):
    "successors of 'on collision fbPotion'"
    if marking('fireBallPotionActive') and marking('fireballPotionPosition') and marking('checkFireball') and marking('playerPosition') and marking('fireBalls'):
        for checkFireball in marking('checkFireball'):
            for playerPosition in marking('playerPosition'):
                for fireBallPotionActive in marking('fireBallPotionActive'):
                    for fireBalls in marking('fireBalls'):
                        for fireballPotionPosition in marking('fireballPotionPosition'):
                            if isinstance(fireballPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(fireBallPotionActive, playerPosition, fireballPotionPosition)
                                    if isinstance(a, bool):
                                        b = increasePoints(fireBalls, playerPosition, fireBallPotionActive, fireballPotionPosition, 1)
                                        if isinstance(b, int):
                                            test = Marking({'fireballPotionPosition': mset([fireballPotionPosition]), 'playerPosition': mset([playerPosition]), 'checkFireball': mset([checkFireball]), 'fireBallPotionActive': mset([fireBallPotionActive]), 'fireBalls': mset([fireBalls])})
                                            if test <= marking:
                                                sub = Marking({'checkFireball': mset([checkFireball]), 'fireBallPotionActive': mset([fireBallPotionActive]), 'fireBalls': mset([fireBalls])})
                                                add = Marking({'fireBallPotionActive': mset([a]), 'fireBalls': mset([b]), 'fireBallsChecked': mset([b])})
                                                mode = hdict({'checkFireball': checkFireball, 'playerPosition': playerPosition, 'fireBallPotionActive': fireBallPotionActive, 'fireballPotionPosition': fireballPotionPosition, 'fireBalls': fireBalls})
                                                yield event('on collision fbPotion', mode, sub, add)

def addsucc_031 (marking, succ):
    "successors of 'on collision hat'"
    if marking('playerPosition') and marking('hasHat') and marking('hatPosition') and marking('checkHat'):
        for checkHat in marking('checkHat'):
            for playerPosition in marking('playerPosition'):
                for hasHat in marking('hasHat'):
                    for hatPosition in marking('hatPosition'):
                        if isinstance(hatPosition, tuple):
                            if isinstance(playerPosition, tuple):
                                a = checkHasHat(playerPosition, hasHat, hatPosition)
                                if isinstance(a, bool):
                                    test = Marking({'playerPosition': mset([playerPosition]), 'hatPosition': mset([hatPosition]), 'checkHat': mset([checkHat]), 'hasHat': mset([hasHat])})
                                    if test <= marking:
                                        sub = Marking({'checkHat': mset([checkHat]), 'hasHat': mset([hasHat])})
                                        add = Marking({'hasHat': mset([a]), 'hatChecked': mset([a])})
                                        succ.add(marking - sub + add)

def succ_031 (marking):
    "successors of 'on collision hat'"
    succ = set()
    addsucc_031(marking, succ)
    return succ

def itersucc_031 (marking):
    "successors of 'on collision hat'"
    if marking('playerPosition') and marking('hasHat') and marking('hatPosition') and marking('checkHat'):
        for checkHat in marking('checkHat'):
            for playerPosition in marking('playerPosition'):
                for hasHat in marking('hasHat'):
                    for hatPosition in marking('hatPosition'):
                        if isinstance(hatPosition, tuple):
                            if isinstance(playerPosition, tuple):
                                a = checkHasHat(playerPosition, hasHat, hatPosition)
                                if isinstance(a, bool):
                                    test = Marking({'playerPosition': mset([playerPosition]), 'hatPosition': mset([hatPosition]), 'checkHat': mset([checkHat]), 'hasHat': mset([hasHat])})
                                    if test <= marking:
                                        sub = Marking({'checkHat': mset([checkHat]), 'hasHat': mset([hasHat])})
                                        add = Marking({'hasHat': mset([a]), 'hatChecked': mset([a])})
                                        mode = hdict({'playerPosition': playerPosition, 'hasHat': hasHat, 'hatPosition': hatPosition, 'checkHat': checkHat})
                                        yield event('on collision hat', mode, sub, add)

def addsucc_032 (marking, succ):
    "successors of 'on collision health'"
    if marking('healthPotionActive') and marking('healthPotionPosition') and marking('playerPosition') and marking('health') and marking('checkHealth'):
        for checkHealth in marking('checkHealth'):
            for playerPosition in marking('playerPosition'):
                for healthPotionActive in marking('healthPotionActive'):
                    for health in marking('health'):
                        for healthPotionPosition in marking('healthPotionPosition'):
                            if isinstance(healthPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(healthPotionActive, playerPosition, healthPotionPosition)
                                    if isinstance(a, bool):
                                        b = increaseHealthPoints(health, playerPosition, healthPotionActive, healthPotionPosition, 1)
                                        if isinstance(b, int):
                                            test = Marking({'healthPotionPosition': mset([healthPotionPosition]), 'playerPosition': mset([playerPosition]), 'checkHealth': mset([checkHealth]), 'healthPotionActive': mset([healthPotionActive]), 'health': mset([health])})
                                            if test <= marking:
                                                sub = Marking({'checkHealth': mset([checkHealth]), 'healthPotionActive': mset([healthPotionActive]), 'health': mset([health])})
                                                add = Marking({'healthPotionActive': mset([a]), 'health': mset([b]), 'healCount': mset([b]), 'healthChecked': mset([health])})
                                                succ.add(marking - sub + add)

def succ_032 (marking):
    "successors of 'on collision health'"
    succ = set()
    addsucc_032(marking, succ)
    return succ

def itersucc_032 (marking):
    "successors of 'on collision health'"
    if marking('healthPotionActive') and marking('healthPotionPosition') and marking('playerPosition') and marking('health') and marking('checkHealth'):
        for checkHealth in marking('checkHealth'):
            for playerPosition in marking('playerPosition'):
                for healthPotionActive in marking('healthPotionActive'):
                    for health in marking('health'):
                        for healthPotionPosition in marking('healthPotionPosition'):
                            if isinstance(healthPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(healthPotionActive, playerPosition, healthPotionPosition)
                                    if isinstance(a, bool):
                                        b = increaseHealthPoints(health, playerPosition, healthPotionActive, healthPotionPosition, 1)
                                        if isinstance(b, int):
                                            test = Marking({'healthPotionPosition': mset([healthPotionPosition]), 'playerPosition': mset([playerPosition]), 'checkHealth': mset([checkHealth]), 'healthPotionActive': mset([healthPotionActive]), 'health': mset([health])})
                                            if test <= marking:
                                                sub = Marking({'checkHealth': mset([checkHealth]), 'healthPotionActive': mset([healthPotionActive]), 'health': mset([health])})
                                                add = Marking({'healthPotionActive': mset([a]), 'health': mset([b]), 'healthChecked': mset([health])})
                                                mode = hdict({'healthPotionActive': healthPotionActive, 'playerPosition': playerPosition, 'health': health, 'healthPotionPosition': healthPotionPosition, 'checkHealth': checkHealth})
                                                yield event('on collision health', mode, sub, add)

def addsucc_033 (marking, succ):
    "successors of 'on collision le'"
    if marking('laserEyesPotionActive') and marking('laserEyes') and marking('playerPosition') and marking('checkLaserEyes') and marking('laserEyesPotionPosition'):
        for checkLaserEyes in marking('checkLaserEyes'):
            for playerPosition in marking('playerPosition'):
                for laserEyesPotionActive in marking('laserEyesPotionActive'):
                    for laserEyes in marking('laserEyes'):
                        for laserEyesPotionPosition in marking('laserEyesPotionPosition'):
                            if isinstance(laserEyesPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(laserEyesPotionActive, playerPosition, laserEyesPotionPosition)
                                    if isinstance(a, bool):
                                        b = activateLE(laserEyes, playerPosition, laserEyesPotionActive, laserEyesPotionPosition)
                                        if isinstance(b, bool):
                                            test = Marking({'playerPosition': mset([playerPosition]), 'laserEyesPotionPosition': mset([laserEyesPotionPosition]), 'checkLaserEyes': mset([checkLaserEyes]), 'laserEyesPotionActive': mset([laserEyesPotionActive]), 'laserEyes': mset([laserEyes])})
                                            if test <= marking:
                                                sub = Marking({'checkLaserEyes': mset([checkLaserEyes]), 'laserEyesPotionActive': mset([laserEyesPotionActive]), 'laserEyes': mset([laserEyes])})
                                                add = Marking({'laserEyesPotionActive': mset([a]), 'laserEyes': mset([b]), 'laserEyesChecked': mset([b])})
                                                succ.add(marking - sub + add)

def succ_033 (marking):
    "successors of 'on collision le'"
    succ = set()
    addsucc_033(marking, succ)
    return succ

def itersucc_033 (marking):
    "successors of 'on collision le'"
    if marking('laserEyesPotionActive') and marking('laserEyes') and marking('playerPosition') and marking('checkLaserEyes') and marking('laserEyesPotionPosition'):
        for checkLaserEyes in marking('checkLaserEyes'):
            for playerPosition in marking('playerPosition'):
                for laserEyesPotionActive in marking('laserEyesPotionActive'):
                    for laserEyes in marking('laserEyes'):
                        for laserEyesPotionPosition in marking('laserEyesPotionPosition'):
                            if isinstance(laserEyesPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(laserEyesPotionActive, playerPosition, laserEyesPotionPosition)
                                    if isinstance(a, bool):
                                        b = activateLE(laserEyes, playerPosition, laserEyesPotionActive, laserEyesPotionPosition)
                                        if isinstance(b, bool):
                                            test = Marking({'playerPosition': mset([playerPosition]), 'laserEyesPotionPosition': mset([laserEyesPotionPosition]), 'checkLaserEyes': mset([checkLaserEyes]), 'laserEyesPotionActive': mset([laserEyesPotionActive]), 'laserEyes': mset([laserEyes])})
                                            if test <= marking:
                                                sub = Marking({'checkLaserEyes': mset([checkLaserEyes]), 'laserEyesPotionActive': mset([laserEyesPotionActive]), 'laserEyes': mset([laserEyes])})
                                                add = Marking({'laserEyesPotionActive': mset([a]), 'laserEyes': mset([b]), 'laserEyesChecked': mset([b])})
                                                mode = hdict({'laserEyesPotionActive': laserEyesPotionActive, 'playerPosition': playerPosition, 'laserEyes': laserEyes, 'laserEyesPotionPosition': laserEyesPotionPosition, 'checkLaserEyes': checkLaserEyes})
                                                yield event('on collision le', mode, sub, add)

def addsucc_034 (marking, succ):
    "successors of 'on collision skeleton'"
    if marking('checkSkeleton') and marking('health') and marking('collisionEnterSkeleton') and marking('playerPosition') and marking('skeletonPosition'):
        for checkSkeleton in marking('checkSkeleton'):
            for playerPosition in marking('playerPosition'):
                for health in marking('health'):
                    for skeletonPosition in marking('skeletonPosition'):
                        for collisionEnterSkeleton in marking('collisionEnterSkeleton'):
                            if isinstance(skeletonPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = onCollisionEnterWithEnemy(playerPosition, skeletonPosition, collisionEnterSkeleton)
                                    if isinstance(a, int):
                                        b = decreaseHealthWithEnemy(health, playerPosition, skeletonPosition, collisionEnterSkeleton)
                                        if isinstance(b, int):
                                            c = onEnemyCollisionChecked(health, playerPosition, skeletonPosition)
                                            test = Marking({'skeletonPosition': mset([skeletonPosition]), 'playerPosition': mset([playerPosition]), 'checkSkeleton': mset([checkSkeleton]), 'health': mset([health]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                            if test <= marking:
                                                sub = Marking({'checkSkeleton': mset([checkSkeleton]), 'health': mset([health]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                                add = Marking({'collisionEnterSkeleton': mset([a]), 'health': mset([b]), 'healthWithSkeleton': mset([b]), 'skeletonChecked': mset([c])})
                                                succ.add(marking - sub + add)

def succ_034 (marking):
    "successors of 'on collision skeleton'"
    succ = set()
    addsucc_034(marking, succ)
    return succ

def itersucc_034 (marking):
    "successors of 'on collision skeleton'"
    if marking('skeletonPosition') and marking('playerPosition') and marking('checkSkeleton') and marking('collisionEnterSkeleton') and marking('health'):
        for checkSkeleton in marking('checkSkeleton'):
            for playerPosition in marking('playerPosition'):
                for health in marking('health'):
                    for skeletonPosition in marking('skeletonPosition'):
                        for collisionEnterSkeleton in marking('collisionEnterSkeleton'):
                            if isinstance(skeletonPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = onCollisionEnterWithEnemy(playerPosition, skeletonPosition, collisionEnterSkeleton)
                                    if isinstance(a, int):
                                        b = decreaseHealthWithEnemy(health, playerPosition, skeletonPosition, collisionEnterSkeleton)
                                        if isinstance(b, int):
                                            c = onEnemyCollisionChecked(health, playerPosition, skeletonPosition)
                                            test = Marking({'skeletonPosition': mset([skeletonPosition]), 'playerPosition': mset([playerPosition]), 'checkSkeleton': mset([checkSkeleton]), 'health': mset([health]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                            if test <= marking:
                                                sub = Marking({'checkSkeleton': mset([checkSkeleton]), 'health': mset([health]), 'collisionEnterSkeleton': mset([collisionEnterSkeleton])})
                                                add = Marking({'collisionEnterSkeleton': mset([a]), 'health': mset([b]), 'skeletonChecked': mset([c])})
                                                mode = hdict({'skeletonPosition': skeletonPosition, 'playerPosition': playerPosition, 'checkSkeleton': checkSkeleton, 'collisionEnterSkeleton': collisionEnterSkeleton, 'health': health})
                                                yield event('on collision skeleton', mode, sub, add)

def addsucc_035 (marking, succ):
    "successors of 'on collision teleport'"
    if marking('teleportPotionActive') and marking('checkTeleport') and marking('playerPosition') and marking('teleportPotionPosition') and marking('teleports'):
        for checkTeleport in marking('checkTeleport'):
            for playerPosition in marking('playerPosition'):
                for teleportPotionActive in marking('teleportPotionActive'):
                    for teleports in marking('teleports'):
                        for teleportPotionPosition in marking('teleportPotionPosition'):
                            if isinstance(teleportPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(teleportPotionActive, playerPosition, teleportPotionPosition)
                                    if isinstance(a, bool):
                                        b = increasePoints(teleports, playerPosition, teleportPotionActive, teleportPotionPosition, 5)
                                        if isinstance(b, int):
                                            test = Marking({'playerPosition': mset([playerPosition]), 'teleportPotionPosition': mset([teleportPotionPosition]), 'checkTeleport': mset([checkTeleport]), 'teleportPotionActive': mset([teleportPotionActive]), 'teleports': mset([teleports])})
                                            if test <= marking:
                                                sub = Marking({'checkTeleport': mset([checkTeleport]), 'teleportPotionActive': mset([teleportPotionActive]), 'teleports': mset([teleports])})
                                                add = Marking({'teleportPotionActive': mset([a]), 'teleports': mset([b]), 'teleportChecked': mset([b])})
                                                succ.add(marking - sub + add)

def succ_035 (marking):
    "successors of 'on collision teleport'"
    succ = set()
    addsucc_035(marking, succ)
    return succ

def itersucc_035 (marking):
    "successors of 'on collision teleport'"
    if marking('teleportPotionActive') and marking('checkTeleport') and marking('playerPosition') and marking('teleportPotionPosition') and marking('teleports'):
        for checkTeleport in marking('checkTeleport'):
            for playerPosition in marking('playerPosition'):
                for teleportPotionActive in marking('teleportPotionActive'):
                    for teleports in marking('teleports'):
                        for teleportPotionPosition in marking('teleportPotionPosition'):
                            if isinstance(teleportPotionPosition, tuple):
                                if isinstance(playerPosition, tuple):
                                    a = setPotionActive(teleportPotionActive, playerPosition, teleportPotionPosition)
                                    if isinstance(a, bool):
                                        b = increasePoints(teleports, playerPosition, teleportPotionActive, teleportPotionPosition, 5)
                                        if isinstance(b, int):
                                            test = Marking({'playerPosition': mset([playerPosition]), 'teleportPotionPosition': mset([teleportPotionPosition]), 'checkTeleport': mset([checkTeleport]), 'teleportPotionActive': mset([teleportPotionActive]), 'teleports': mset([teleports])})
                                            if test <= marking:
                                                sub = Marking({'checkTeleport': mset([checkTeleport]), 'teleportPotionActive': mset([teleportPotionActive]), 'teleports': mset([teleports])})
                                                add = Marking({'teleportPotionActive': mset([a]), 'teleports': mset([b]), 'teleportChecked': mset([b])})
                                                mode = hdict({'playerPosition': playerPosition, 'teleportPotionPosition': teleportPotionPosition, 'teleportPotionActive': teleportPotionActive, 'teleports': teleports, 'checkTeleport': checkTeleport})
                                                yield event('on collision teleport', mode, sub, add)

def addsucc_036 (marking, succ):
    "successors of 'on create enemy0'"
    if marking('createEnemy0'):
        for createEnemy0 in marking('createEnemy0'):
            a = True
            if isinstance(a, bool):
                if isinstance(createEnemy0, tuple):
                    b = createPosPoint(createEnemy0, -2)
                    if isinstance(b, tuple):
                        c = createPosPoint(createEnemy0, 2)
                        if isinstance(c, tuple):
                            d = -1
                            if isinstance(d, int):
                                e = 1
                                sub = Marking({'createEnemy0': mset([createEnemy0])})
                                if sub <= marking:
                                    add = Marking({'enemy0Active': mset([a]), 'enemy0Position': mset([createEnemy0]), 'enemy0PosA': mset([b]), 'enemy0PosB': mset([c]), 'enemy0Direction': mset([d]), 'enemy0Created': mset([e])})
                                    succ.add(marking - sub + add)

def succ_036 (marking):
    "successors of 'on create enemy0'"
    succ = set()
    addsucc_036(marking, succ)
    return succ

def itersucc_036 (marking):
    "successors of 'on create enemy0'"
    if marking('createEnemy0'):
        for createEnemy0 in marking('createEnemy0'):
            a = True
            if isinstance(a, bool):
                if isinstance(createEnemy0, tuple):
                    b = createPosPoint(createEnemy0, -2)
                    if isinstance(b, tuple):
                        c = createPosPoint(createEnemy0, 2)
                        if isinstance(c, tuple):
                            d = -1
                            if isinstance(d, int):
                                e = 1
                                sub = Marking({'createEnemy0': mset([createEnemy0])})
                                if sub <= marking:
                                    add = Marking({'enemy0Active': mset([a]), 'enemy0Position': mset([createEnemy0]), 'enemy0PosA': mset([b]), 'enemy0PosB': mset([c]), 'enemy0Direction': mset([d]), 'enemy0Created': mset([e])})
                                    mode = hdict({'createEnemy0': createEnemy0})
                                    yield event('on create enemy0', mode, sub, add)

def addsucc_037 (marking, succ):
    "successors of 'on create skeleton'"
    if marking('createSkeleton'):
        for createSkeleton in marking('createSkeleton'):
            a = True
            if isinstance(a, bool):
                if isinstance(createSkeleton, tuple):
                    b = createPosPoint(createSkeleton, -2)
                    if isinstance(b, tuple):
                        c = createPosPoint(createSkeleton, 2)
                        if isinstance(c, tuple):
                            d = 1
                            if isinstance(d, int):
                                sub = Marking({'createSkeleton': mset([createSkeleton])})
                                if sub <= marking:
                                    add = Marking({'skeletonActive': mset([a]), 'skeletonPosition': mset([createSkeleton]), 'skeletonPosA': mset([b]), 'skeletonPosB': mset([c]), 'skeletonDirection': mset([d]), 'skeletonCreated': mset([d])})
                                    succ.add(marking - sub + add)

def succ_037 (marking):
    "successors of 'on create skeleton'"
    succ = set()
    addsucc_037(marking, succ)
    return succ

def itersucc_037 (marking):
    "successors of 'on create skeleton'"
    if marking('createSkeleton'):
        for createSkeleton in marking('createSkeleton'):
            a = True
            if isinstance(a, bool):
                if isinstance(createSkeleton, tuple):
                    b = createPosPoint(createSkeleton, -2)
                    if isinstance(b, tuple):
                        c = createPosPoint(createSkeleton, 2)
                        if isinstance(c, tuple):
                            d = 1
                            if isinstance(d, int):
                                sub = Marking({'createSkeleton': mset([createSkeleton])})
                                if sub <= marking:
                                    add = Marking({'skeletonActive': mset([a]), 'skeletonPosition': mset([createSkeleton]), 'skeletonPosA': mset([b]), 'skeletonPosB': mset([c]), 'skeletonDirection': mset([d]), 'skeletonCreated': mset([d])})
                                    mode = hdict({'createSkeleton': createSkeleton})
                                    yield event('on create skeleton', mode, sub, add)

def addsucc_038 (marking, succ):
    "successors of 'on fireball collision'"
    if marking('mapTBPos') and marking('enemy0Position') and marking('skeletonActive') and marking('mapTXRange') and marking('skeletonPosition') and marking('fireballPosition') and marking('enemy0Active') and marking('checkfbcollision'):
        for checkfbcollision in marking('checkfbcollision'):
            for enemy0Active in marking('enemy0Active'):
                for enemy0Position in marking('enemy0Position'):
                    for skeletonActive in marking('skeletonActive'):
                        for skeletonPosition in marking('skeletonPosition'):
                            for fireballPosition in marking('fireballPosition'):
                                for mapTXRange in marking('mapTXRange'):
                                    for mapTBPos in marking('mapTBPos'):
                                        if isinstance(enemy0Active, bool):
                                            if isinstance(enemy0Position, tuple):
                                                if isinstance(skeletonActive, bool):
                                                    if isinstance(skeletonPosition, tuple):
                                                        if isinstance(fireballPosition, tuple):
                                                            if isinstance(mapTXRange, tuple):
                                                                if isinstance(mapTBPos, tuple):
                                                                    a = checkFireball(fireballPosition, enemy0Active, enemy0Position, skeletonActive, skeletonPosition, mapTBPos, mapTXRange, True)
                                                                    b = checkFireball(fireballPosition, enemy0Active, enemy0Position, skeletonActive, skeletonPosition, mapTBPos, mapTXRange, False)
                                                                    test = Marking({'mapTBPos': mset([mapTBPos]), 'enemy0Position': mset([enemy0Position]), 'skeletonActive': mset([skeletonActive]), 'mapTXRange': mset([mapTXRange]), 'skeletonPosition': mset([skeletonPosition]), 'fireballPosition': mset([fireballPosition]), 'enemy0Active': mset([enemy0Active]), 'checkfbcollision': mset([checkfbcollision])})
                                                                    if test <= marking:
                                                                        sub = Marking({'checkfbcollision': mset([checkfbcollision])})
                                                                        if(a == None):
                                                                            add = Marking({'fireballChecked': mset([b])})
                                                                        elif(b == None):
                                                                            add = Marking({'fireballCollided': mset([a])})
                                                                        succ.add(marking - sub + add)

def succ_038 (marking):
    "successors of 'on fireball collision'"
    succ = set()
    addsucc_038(marking, succ)
    return succ

def itersucc_038 (marking):
    "successors of 'on fireball collision'"
    if marking('mapTBPos') and marking('enemy0Position') and marking('skeletonActive') and marking('mapTXRange') and marking('skeletonPosition') and marking('fireballPosition') and marking('enemy0Active') and marking('checkfbcollision'):
        for checkfbcollision in marking('checkfbcollision'):
            for enemy0Active in marking('enemy0Active'):
                for enemy0Position in marking('enemy0Position'):
                    for skeletonActive in marking('skeletonActive'):
                        for skeletonPosition in marking('skeletonPosition'):
                            for fireballPosition in marking('fireballPosition'):
                                for mapTXRange in marking('mapTXRange'):
                                    for mapTBPos in marking('mapTBPos'):
                                        if isinstance(enemy0Active, bool):
                                            if isinstance(enemy0Position, tuple):
                                                if isinstance(skeletonActive, bool):
                                                    if isinstance(skeletonPosition, tuple):
                                                        if isinstance(fireballPosition, tuple):
                                                            if isinstance(mapTXRange, tuple):
                                                                if isinstance(mapTBPos, tuple):
                                                                    a = checkFireball(fireballPosition, enemy0Active, enemy0Position, skeletonActive, skeletonPosition, mapTBPos, mapTXRange, True)
                                                                    b = checkFireball(fireballPosition, enemy0Active, enemy0Position, skeletonActive, skeletonPosition, mapTBPos, mapTXRange, False)
                                                                    test = Marking({'mapTBPos': mset([mapTBPos]), 'enemy0Position': mset([enemy0Position]), 'skeletonActive': mset([skeletonActive]), 'mapTXRange': mset([mapTXRange]), 'skeletonPosition': mset([skeletonPosition]), 'fireballPosition': mset([fireballPosition]), 'enemy0Active': mset([enemy0Active]), 'checkfbcollision': mset([checkfbcollision])})
                                                                    if test <= marking:
                                                                        sub = Marking({'checkfbcollision': mset([checkfbcollision])})
                                                                        add = Marking({'fireballCollided': mset([a]), 'fireballChecked': mset([b])})
                                                                        mode = hdict({'mapTXRange': mapTXRange, 'mapTBPos': mapTBPos, 'enemy0Position': enemy0Position, 'skeletonPosition': skeletonPosition, 'fireballPosition': fireballPosition, 'enemy0Active': enemy0Active, 'checkfbcollision': checkfbcollision, 'skeletonActive': skeletonActive})
                                                                        yield event('on fireball collision', mode, sub, add)

def addsucc_039 (marking, succ):
    "successors of 'on generate level'"
    if marking('spawnPoints') and marking('generateLevel'):
        for generateLevel in marking('generateLevel'):
            for spawnPoints in marking('spawnPoints'):
                if isinstance(spawnPoints, tuple):
                    a = onGenerateLevel(spawnPoints)
                    test = Marking({'spawnPoints': mset([spawnPoints]), 'generateLevel': mset([generateLevel])})
                    if test <= marking:
                        sub = Marking({'generateLevel': mset([generateLevel])})
                        add = Marking({'levelGenerated': mset([a])})
                        succ.add(marking - sub + add)

def succ_039 (marking):
    "successors of 'on generate level'"
    succ = set()
    addsucc_039(marking, succ)
    return succ

def itersucc_039 (marking):
    "successors of 'on generate level'"
    if marking('spawnPoints') and marking('generateLevel'):
        for generateLevel in marking('generateLevel'):
            for spawnPoints in marking('spawnPoints'):
                if isinstance(spawnPoints, tuple):
                    a = onGenerateLevel(spawnPoints)
                    test = Marking({'spawnPoints': mset([spawnPoints]), 'generateLevel': mset([generateLevel])})
                    if test <= marking:
                        sub = Marking({'generateLevel': mset([generateLevel])})
                        add = Marking({'levelGenerated': mset([a])})
                        mode = hdict({'spawnPoints': spawnPoints, 'generateLevel': generateLevel})
                        yield event('on generate level', mode, sub, add)

def addsucc_040 (marking, succ):
    "successors of 'on mouse0 clicked'"
    if marking('teleports') and marking('playerPosition') and marking('checkMouse0'):
        for checkMouse0 in marking('checkMouse0'):
            for teleports in marking('teleports'):
                for playerPosition in marking('playerPosition'):
                    a = tryTeleport(teleports)
                    if isinstance(a, int):
                        b = onTeleported(teleports, playerPosition)
                        if isinstance(b, tuple):
                            c = 1
                            sub = Marking({'checkMouse0': mset([checkMouse0]), 'teleports': mset([teleports]), 'playerPosition': mset([playerPosition])})
                            if sub <= marking:
                                add = Marking({'teleports': mset([a]), 'playerPosition': mset([b]), 'checkZ': mset([c])})
                                succ.add(marking - sub + add)

def succ_040 (marking):
    "successors of 'on mouse0 clicked'"
    succ = set()
    addsucc_040(marking, succ)
    return succ

def itersucc_040 (marking):
    "successors of 'on mouse0 clicked'"
    if marking('teleports') and marking('playerPosition') and marking('checkMouse0'):
        for checkMouse0 in marking('checkMouse0'):
            for teleports in marking('teleports'):
                for playerPosition in marking('playerPosition'):
                    a = tryTeleport(teleports)
                    if isinstance(a, int):
                        b = onTeleported(teleports, playerPosition)
                        if isinstance(b, tuple):
                            c = 1
                            sub = Marking({'checkMouse0': mset([checkMouse0]), 'teleports': mset([teleports]), 'playerPosition': mset([playerPosition])})
                            if sub <= marking:
                                add = Marking({'teleports': mset([a]), 'playerPosition': mset([b]), 'checkZ': mset([c])})
                                mode = hdict({'teleports': teleports, 'playerPosition': playerPosition, 'checkMouse0': checkMouse0})
                                yield event('on mouse0 clicked', mode, sub, add)

def addsucc_041 (marking, succ):
    "successors of 'on mouse0 not clicked'"
    if marking('checkMouse0'):
        for checkMouse0 in marking('checkMouse0'):
            a = 1
            sub = Marking({'checkMouse0': mset([checkMouse0])})
            if sub <= marking:
                add = Marking({'checkZ': mset([a])})
                succ.add(marking - sub + add)

def succ_041 (marking):
    "successors of 'on mouse0 not clicked'"
    succ = set()
    addsucc_041(marking, succ)
    return succ

def itersucc_041 (marking):
    "successors of 'on mouse0 not clicked'"
    if marking('checkMouse0'):
        for checkMouse0 in marking('checkMouse0'):
            a = 1
            sub = Marking({'checkMouse0': mset([checkMouse0])})
            if sub <= marking:
                add = Marking({'checkZ': mset([a])})
                mode = hdict({'checkMouse0': checkMouse0})
                yield event('on mouse0 not clicked', mode, sub, add)

def addsucc_042 (marking, succ):
    "successors of 'on space clicked'"
    if marking('mapTBPos') and marking('mapTXRange') and marking('checkSpace') and marking('playerPosition') and marking('jumps'):
        for checkSpace in marking('checkSpace'):
            for jumps in marking('jumps'):
                for playerPosition in marking('playerPosition'):
                    for mapTXRange in marking('mapTXRange'):
                        for mapTBPos in marking('mapTBPos'):
                            a = onJumped(jumps)
                            if isinstance(a, int):
                                b = jump(jumps, playerPosition, mapTXRange, mapTBPos)
                                if isinstance(b, tuple):
                                    if isinstance(mapTXRange, tuple):
                                        if isinstance(mapTBPos, tuple):
                                            c = 1
                                            test = Marking({'mapTBPos': mset([mapTBPos]), 'mapTXRange': mset([mapTXRange]), 'checkSpace': mset([checkSpace]), 'jumps': mset([jumps]), 'playerPosition': mset([playerPosition])})
                                            if test <= marking:
                                                sub = Marking({'checkSpace': mset([checkSpace]), 'jumps': mset([jumps]), 'playerPosition': mset([playerPosition])})
                                                add = Marking({'jumps': mset([a]), 'playerPosition': mset([b]), 'checkCtrl': mset([c])})
                                                succ.add(marking - sub + add)

def succ_042 (marking):
    "successors of 'on space clicked'"
    succ = set()
    addsucc_042(marking, succ)
    return succ

def itersucc_042 (marking):
    "successors of 'on space clicked'"
    if marking('mapTBPos') and marking('mapTXRange') and marking('checkSpace') and marking('playerPosition') and marking('jumps'):
        for checkSpace in marking('checkSpace'):
            for jumps in marking('jumps'):
                for playerPosition in marking('playerPosition'):
                    for mapTXRange in marking('mapTXRange'):
                        for mapTBPos in marking('mapTBPos'):
                            a = onJumped(jumps)
                            if isinstance(a, int):
                                b = jump(jumps, playerPosition, mapTXRange, mapTBPos)
                                if isinstance(b, tuple):
                                    if isinstance(mapTXRange, tuple):
                                        if isinstance(mapTBPos, tuple):
                                            c = 1
                                            test = Marking({'mapTBPos': mset([mapTBPos]), 'mapTXRange': mset([mapTXRange]), 'checkSpace': mset([checkSpace]), 'jumps': mset([jumps]), 'playerPosition': mset([playerPosition])})
                                            if test <= marking:
                                                sub = Marking({'checkSpace': mset([checkSpace]), 'jumps': mset([jumps]), 'playerPosition': mset([playerPosition])})
                                                add = Marking({'jumps': mset([a]), 'playerPosition': mset([b]), 'checkCtrl': mset([c])})
                                                mode = hdict({'mapTXRange': mapTXRange, 'mapTBPos': mapTBPos, 'checkSpace': checkSpace, 'playerPosition': playerPosition, 'jumps': jumps})
                                                yield event('on space clicked', mode, sub, add)

def addsucc_043 (marking, succ):
    "successors of 'on space not clicked'"
    if marking('checkSpace'):
        for checkSpace in marking('checkSpace'):
            a = 1
            sub = Marking({'checkSpace': mset([checkSpace])})
            if sub <= marking:
                add = Marking({'checkCtrl': mset([a])})
                succ.add(marking - sub + add)

def succ_043 (marking):
    "successors of 'on space not clicked'"
    succ = set()
    addsucc_043(marking, succ)
    return succ

def itersucc_043 (marking):
    "successors of 'on space not clicked'"
    if marking('checkSpace'):
        for checkSpace in marking('checkSpace'):
            a = 1
            sub = Marking({'checkSpace': mset([checkSpace])})
            if sub <= marking:
                add = Marking({'checkCtrl': mset([a])})
                mode = hdict({'checkSpace': checkSpace})
                yield event('on space not clicked', mode, sub, add)

def addsucc_044 (marking, succ):
    "successors of 'on start ended'"
    if marking('enemy0Created') and marking('skeletonCreated'):
        for enemy0Created in marking('enemy0Created'):
            for skeletonCreated in marking('skeletonCreated'):
                a = 1
                sub = Marking({'enemy0Created': mset([enemy0Created]), 'skeletonCreated': mset([skeletonCreated])})
                if sub <= marking:
                    add = Marking({'physicsExecution': mset([a])})
                    succ.add(marking - sub + add)

def succ_044 (marking):
    "successors of 'on start ended'"
    succ = set()
    addsucc_044(marking, succ)
    return succ

def itersucc_044 (marking):
    "successors of 'on start ended'"
    if marking('enemy0Created') and marking('skeletonCreated'):
        for enemy0Created in marking('enemy0Created'):
            for skeletonCreated in marking('skeletonCreated'):
                a = 1
                sub = Marking({'enemy0Created': mset([enemy0Created]), 'skeletonCreated': mset([skeletonCreated])})
                if sub <= marking:
                    add = Marking({'physicsExecution': mset([a])})
                    mode = hdict({'enemy0Created': enemy0Created, 'skeletonCreated': skeletonCreated})
                    yield event('on start ended', mode, sub, add)

def addsucc_045 (marking, succ):
    "successors of 'reset jumps'"
    if marking('mapTBPos') and marking('mapTXRange') and marking('withTiles') and marking('playerPosition') and marking('jumps'):
        for withTiles in marking('withTiles'):
            for playerPosition in marking('playerPosition'):
                for jumps in marking('jumps'):
                    for mapTXRange in marking('mapTXRange'):
                        for mapTBPos in marking('mapTBPos'):
                            if isinstance(mapTXRange, tuple):
                                if isinstance(mapTBPos, tuple):
                                    if isinstance(playerPosition, tuple):
                                        a = isCollidiingWithTiles(playerPosition,mapTXRange,mapTBPos,jumps)
                                        if isinstance(a, int):
                                            b = onTilesChecked(playerPosition,mapTXRange,mapTBPos,jumps)
                                            if isinstance(b, int):
                                                test = Marking({'mapTBPos': mset([mapTBPos]), 'mapTXRange': mset([mapTXRange]), 'playerPosition': mset([playerPosition]), 'withTiles': mset([withTiles]), 'jumps': mset([jumps])})
                                                if test <= marking:
                                                    sub = Marking({'withTiles': mset([withTiles]), 'jumps': mset([jumps])})
                                                    add = Marking({'jumps': mset([a]), 'tilesChecked': mset([b])})
                                                    succ.add(marking - sub + add)

def succ_045 (marking):
    "successors of 'reset jumps'"
    succ = set()
    addsucc_045(marking, succ)
    return succ

def itersucc_045 (marking):
    "successors of 'reset jumps'"
    if marking('mapTBPos') and marking('mapTXRange') and marking('withTiles') and marking('playerPosition') and marking('jumps'):
        for withTiles in marking('withTiles'):
            for playerPosition in marking('playerPosition'):
                for jumps in marking('jumps'):
                    for mapTXRange in marking('mapTXRange'):
                        for mapTBPos in marking('mapTBPos'):
                            if isinstance(mapTXRange, tuple):
                                if isinstance(mapTBPos, tuple):
                                    if isinstance(playerPosition, tuple):
                                        a = isCollidiingWithTiles(playerPosition,mapTXRange,mapTBPos,jumps)
                                        if isinstance(a, int):
                                            b = onTilesChecked(playerPosition,mapTXRange,mapTBPos,jumps)
                                            if isinstance(b, int):
                                                test = Marking({'mapTBPos': mset([mapTBPos]), 'mapTXRange': mset([mapTXRange]), 'playerPosition': mset([playerPosition]), 'withTiles': mset([withTiles]), 'jumps': mset([jumps])})
                                                if test <= marking:
                                                    sub = Marking({'withTiles': mset([withTiles]), 'jumps': mset([jumps])})
                                                    add = Marking({'jumps': mset([a]), 'tilesChecked': mset([b])})
                                                    mode = hdict({'withTiles': withTiles, 'mapTXRange': mapTXRange, 'mapTBPos': mapTBPos, 'playerPosition': playerPosition, 'jumps': jumps})
                                                    yield event('reset jumps', mode, sub, add)

def addsucc_046 (marking, succ):
    "successors of 'right arrow clicked'"
    if marking('arrowClicked'):
        for arrowClicked in marking('arrowClicked'):
            a = 1
            if isinstance(a, int):
                sub = Marking({'arrowClicked': mset([arrowClicked])})
                if sub <= marking:
                    add = Marking({'inputValue': mset([a])})
                    succ.add(marking - sub + add)

def succ_046 (marking):
    "successors of 'right arrow clicked'"
    succ = set()
    addsucc_046(marking, succ)
    return succ

def itersucc_046 (marking):
    "successors of 'right arrow clicked'"
    if marking('arrowClicked'):
        for arrowClicked in marking('arrowClicked'):
            a = 1
            if isinstance(a, int):
                sub = Marking({'arrowClicked': mset([arrowClicked])})
                if sub <= marking:
                    add = Marking({'inputValue': mset([a])})
                    mode = hdict({'arrowClicked': arrowClicked})
                    yield event('right arrow clicked', mode, sub, add)

def addsucc_047 (marking, succ):
    "successors of 'stay in place'"
    if marking('playerInput'):
        for playerInput in marking('playerInput'):
            a = 0
            if isinstance(a, int):
                sub = Marking({'playerInput': mset([playerInput])})
                if sub <= marking:
                    add = Marking({'inputValue': mset([a])})
                    succ.add(marking - sub + add)

def succ_047 (marking):
    "successors of 'stay in place'"
    succ = set()
    addsucc_047(marking, succ)
    return succ

def itersucc_047 (marking):
    "successors of 'stay in place'"
    if marking('playerInput'):
        for playerInput in marking('playerInput'):
            a = 0
            if isinstance(a, int):
                sub = Marking({'playerInput': mset([playerInput])})
                if sub <= marking:
                    add = Marking({'inputValue': mset([a])})
                    mode = hdict({'playerInput': playerInput})
                    yield event('stay in place', mode, sub, add)

def addsucc_048 (marking, succ):
    "successors of 'take player input'"
    if marking('laserChecked'):
        for laserChecked in marking('laserChecked'):
            a = 1
            sub = Marking({'laserChecked': mset([laserChecked])})
            if sub <= marking:
                add = Marking({'playerInput': mset([a])})
                succ.add(marking - sub + add)

def succ_048 (marking):
    "successors of 'take player input'"
    succ = set()
    addsucc_048(marking, succ)
    return succ

def itersucc_048 (marking):
    "successors of 'take player input'"
    if marking('laserChecked'):
        for laserChecked in marking('laserChecked'):
            a = 1
            sub = Marking({'laserChecked': mset([laserChecked])})
            if sub <= marking:
                add = Marking({'playerInput': mset([a])})
                mode = hdict({'laserChecked': laserChecked})
                yield event('take player input', mode, sub, add)

def addsucc_049 (marking, succ):
    "successors of 'update enemy position'"
    if marking('enemy0PosA') and marking('enemyPosChecked') and marking('enemy0Active') and marking('enemy0Direction') and marking('enemy0Position') and marking('enemy0PosB') and marking('enemyWaitingCounter') and marking('mapTXRange') and marking('mapTBPos'):
        for enemyPosChecked in marking('enemyPosChecked'):
            for enemy0Active in marking('enemy0Active'):
                for enemy0Position in marking('enemy0Position'):
                    for enemy0PosA in marking('enemy0PosA'):
                        for enemy0PosB in marking('enemy0PosB'):
                            for enemy0Direction in marking('enemy0Direction'):
                                for enemyWaitingCounter in marking('enemyWaitingCounter'):
                                    for mapTXRange in marking('mapTXRange'):
                                        for mapTBPos in marking('mapTBPos'):
                                            a = moveEnemy(enemyWaitingCounter, enemy0Active, enemy0Position, enemy0Direction, enemy0PosA, enemy0PosB, mapTBPos, mapTXRange)
                                            if isinstance(a, tuple):
                                                b = updateEnemyDirection(enemyWaitingCounter, enemy0Active, enemy0Position, enemy0Direction, enemy0PosA, enemy0PosB)
                                                if isinstance(b, int):
                                                    if isinstance(enemy0Active, bool):
                                                        if isinstance(enemy0PosA, tuple):
                                                            if isinstance(enemy0PosB, tuple):
                                                                if isinstance(mapTXRange, tuple):
                                                                    if isinstance(enemyWaitingCounter, int):
                                                                        if isinstance(mapTBPos, tuple):
                                                                            c = 1
                                                                            test = Marking({'enemy0PosB': mset([enemy0PosB]), 'enemyWaitingCounter': mset([enemyWaitingCounter]), 'mapTXRange': mset([mapTXRange]), 'mapTBPos': mset([mapTBPos]), 'enemy0PosA': mset([enemy0PosA]), 'enemy0Active': mset([enemy0Active]), 'enemyPosChecked': mset([enemyPosChecked]), 'enemy0Position': mset([enemy0Position]), 'enemy0Direction': mset([enemy0Direction])})
                                                                            if test <= marking:
                                                                                sub = Marking({'enemyPosChecked': mset([enemyPosChecked]), 'enemy0Position': mset([enemy0Position]), 'enemy0Direction': mset([enemy0Direction])})
                                                                                add = Marking({'enemy0Position': mset([a]), 'enemy0Direction': mset([b]), 'enemyPosUpdated': mset([c])})
                                                                                succ.add(marking - sub + add)

def succ_049 (marking):
    "successors of 'update enemy position'"
    succ = set()
    addsucc_049(marking, succ)
    return succ

def itersucc_049 (marking):
    "successors of 'update enemy position'"
    if marking('mapTBPos') and marking('enemy0Position') and marking('enemy0Direction') and marking('mapTXRange') and marking('enemy0PosB') and marking('enemy0Active') and marking('executeEnemyUpdate') and marking('enemy0PosA'):
        for executeEnemyUpdate in marking('executeEnemyUpdate'):
            for enemy0Active in marking('enemy0Active'):
                for enemy0Position in marking('enemy0Position'):
                    for enemy0PosA in marking('enemy0PosA'):
                        for enemy0PosB in marking('enemy0PosB'):
                            for enemy0Direction in marking('enemy0Direction'):
                                for mapTXRange in marking('mapTXRange'):
                                    for mapTBPos in marking('mapTBPos'):
                                        a = moveEnemy(enemy0Active, enemy0Position, enemy0Direction, enemy0PosA, enemy0PosB, mapTBPos, mapTXRange)
                                        if isinstance(a, tuple):
                                            b = updateEnemyDirection(enemy0Active, enemy0Position, enemy0Direction, enemy0PosA, enemy0PosB)
                                            if isinstance(b, int):
                                                if isinstance(enemy0Active, bool):
                                                    if isinstance(enemy0PosA, tuple):
                                                        if isinstance(enemy0PosB, tuple):
                                                            if isinstance(mapTXRange, tuple):
                                                                if isinstance(mapTBPos, tuple):
                                                                    c = 1
                                                                    test = Marking({'mapTBPos': mset([mapTBPos]), 'mapTXRange': mset([mapTXRange]), 'enemy0PosB': mset([enemy0PosB]), 'enemy0Active': mset([enemy0Active]), 'enemy0PosA': mset([enemy0PosA]), 'executeEnemyUpdate': mset([executeEnemyUpdate]), 'enemy0Position': mset([enemy0Position]), 'enemy0Direction': mset([enemy0Direction])})
                                                                    if test <= marking:
                                                                        sub = Marking({'executeEnemyUpdate': mset([executeEnemyUpdate]), 'enemy0Position': mset([enemy0Position]), 'enemy0Direction': mset([enemy0Direction])})
                                                                        add = Marking({'enemy0Position': mset([a]), 'enemy0Direction': mset([b]), 'enemyPosUpdated': mset([c])})
                                                                        mode = hdict({'mapTXRange': mapTXRange, 'mapTBPos': mapTBPos, 'enemy0Position': enemy0Position, 'enemy0Direction': enemy0Direction, 'enemy0PosB': enemy0PosB, 'enemy0Active': enemy0Active, 'executeEnemyUpdate': executeEnemyUpdate, 'enemy0PosA': enemy0PosA})
                                                                        yield event('update enemy position', mode, sub, add)

def addsucc_050 (marking, succ):
    "successors of 'update gravity'"
    if marking('physicsExecution') and marking('mapTBPos') and marking('enemy0Position') and marking('skeletonActive') and marking('mapTXRange') and marking('playerPosition') and marking('skeletonPosition') and marking('enemy0Active'):
        for physicsExecution in marking('physicsExecution'):
            for mapTXRange in marking('mapTXRange'):
                for mapTBPos in marking('mapTBPos'):
                    for playerPosition in marking('playerPosition'):
                        for skeletonPosition in marking('skeletonPosition'):
                            for skeletonActive in marking('skeletonActive'):
                                for enemy0Position in marking('enemy0Position'):
                                    for enemy0Active in marking('enemy0Active'):
                                        a = updateGravity(playerPosition, mapTXRange, mapTBPos)
                                        if isinstance(a, tuple):
                                            b = updateGravity(skeletonPosition, mapTXRange, mapTBPos, skeletonActive)
                                            if isinstance(b, tuple):
                                                c = updateGravity(enemy0Position, mapTXRange, mapTBPos, enemy0Active)
                                                if isinstance(c, tuple):
                                                    if isinstance(mapTXRange, tuple):
                                                        if isinstance(mapTBPos, tuple):
                                                            if isinstance(skeletonActive, bool):
                                                                if isinstance(enemy0Active, bool):
                                                                    d = 1
                                                                    test = Marking({'mapTBPos': mset([mapTBPos]), 'skeletonActive': mset([skeletonActive]), 'mapTXRange': mset([mapTXRange]), 'enemy0Active': mset([enemy0Active]), 'physicsExecution': mset([physicsExecution]), 'playerPosition': mset([playerPosition]), 'skeletonPosition': mset([skeletonPosition]), 'enemy0Position': mset([enemy0Position])})
                                                                    if test <= marking:
                                                                        sub = Marking({'physicsExecution': mset([physicsExecution]), 'playerPosition': mset([playerPosition]), 'skeletonPosition': mset([skeletonPosition]), 'enemy0Position': mset([enemy0Position])})
                                                                        add = Marking({'playerPosition': mset([a]), 'skeletonPosition': mset([b]), 'enemy0Position': mset([c]), 'gravityUpdated': mset([d])})
                                                                        succ.add(marking - sub + add)

def succ_050 (marking):
    "successors of 'update gravity'"
    succ = set()
    addsucc_050(marking, succ)
    return succ

def itersucc_050 (marking):
    "successors of 'update gravity'"
    if marking('physicsExecution') and marking('mapTBPos') and marking('enemy0Position') and marking('skeletonActive') and marking('mapTXRange') and marking('playerPosition') and marking('skeletonPosition') and marking('enemy0Active'):
        for physicsExecution in marking('physicsExecution'):
            for mapTXRange in marking('mapTXRange'):
                for mapTBPos in marking('mapTBPos'):
                    for playerPosition in marking('playerPosition'):
                        for skeletonPosition in marking('skeletonPosition'):
                            for skeletonActive in marking('skeletonActive'):
                                for enemy0Position in marking('enemy0Position'):
                                    for enemy0Active in marking('enemy0Active'):
                                        a = updateGravity(playerPosition, mapTXRange, mapTBPos)
                                        if isinstance(a, tuple):
                                            b = updateGravity(skeletonPosition, mapTXRange, mapTBPos, skeletonActive)
                                            if isinstance(b, tuple):
                                                c = updateGravity(enemy0Position, mapTXRange, mapTBPos, enemy0Active)
                                                if isinstance(c, tuple):
                                                    if isinstance(mapTXRange, tuple):
                                                        if isinstance(mapTBPos, tuple):
                                                            if isinstance(skeletonActive, bool):
                                                                if isinstance(enemy0Active, bool):
                                                                    d = 1
                                                                    test = Marking({'mapTBPos': mset([mapTBPos]), 'skeletonActive': mset([skeletonActive]), 'mapTXRange': mset([mapTXRange]), 'enemy0Active': mset([enemy0Active]), 'physicsExecution': mset([physicsExecution]), 'playerPosition': mset([playerPosition]), 'skeletonPosition': mset([skeletonPosition]), 'enemy0Position': mset([enemy0Position])})
                                                                    if test <= marking:
                                                                        sub = Marking({'physicsExecution': mset([physicsExecution]), 'playerPosition': mset([playerPosition]), 'skeletonPosition': mset([skeletonPosition]), 'enemy0Position': mset([enemy0Position])})
                                                                        add = Marking({'playerPosition': mset([a]), 'skeletonPosition': mset([b]), 'enemy0Position': mset([c]), 'gravityUpdated': mset([d])})
                                                                        mode = hdict({'physicsExecution': physicsExecution, 'mapTXRange': mapTXRange, 'mapTBPos': mapTBPos, 'playerPosition': playerPosition, 'skeletonPosition': skeletonPosition, 'enemy0Position': enemy0Position, 'enemy0Active': enemy0Active, 'skeletonActive': skeletonActive})
                                                                        yield event('update gravity', mode, sub, add)

def addsucc_051 (marking, succ):
    "successors of 'update skeleton position'"
    if marking('skeletonPosChecked') and marking('skeletonPosA') and marking('skeletonActive') and marking('skeletonPosition') and marking('skeletonWaitingCounter') and marking('skeletonPosB') and marking('mapTBPos') and marking('mapTXRange') and marking('skeletonDirection'):
        for skeletonPosChecked in marking('skeletonPosChecked'):
            for skeletonActive in marking('skeletonActive'):
                for skeletonPosition in marking('skeletonPosition'):
                    for skeletonPosA in marking('skeletonPosA'):
                        for skeletonPosB in marking('skeletonPosB'):
                            for skeletonDirection in marking('skeletonDirection'):
                                for skeletonWaitingCounter in marking('skeletonWaitingCounter'):
                                    for mapTXRange in marking('mapTXRange'):
                                        for mapTBPos in marking('mapTBPos'):
                                            a = moveEnemy(skeletonWaitingCounter, skeletonActive, skeletonPosition, skeletonDirection, skeletonPosA, skeletonPosB, mapTBPos,mapTXRange)
                                            if isinstance(a, tuple):
                                                b = updateEnemyDirection(skeletonWaitingCounter, skeletonActive, skeletonPosition, skeletonDirection, skeletonPosA, skeletonPosB)
                                                if isinstance(b, int):
                                                    if isinstance(skeletonActive, bool):
                                                        if isinstance(skeletonPosA, tuple):
                                                            if isinstance(skeletonPosB, tuple):
                                                                if isinstance(skeletonWaitingCounter, int):
                                                                    if isinstance(mapTXRange, tuple):
                                                                        if isinstance(mapTBPos, tuple):
                                                                            c = 1
                                                                            test = Marking({'mapTXRange': mset([mapTXRange]), 'skeletonWaitingCounter': mset([skeletonWaitingCounter]), 'skeletonPosB': mset([skeletonPosB]), 'mapTBPos': mset([mapTBPos]), 'skeletonPosA': mset([skeletonPosA]), 'skeletonActive': mset([skeletonActive]), 'skeletonPosChecked': mset([skeletonPosChecked]), 'skeletonPosition': mset([skeletonPosition]), 'skeletonDirection': mset([skeletonDirection])})
                                                                            if test <= marking:
                                                                                sub = Marking({'skeletonPosChecked': mset([skeletonPosChecked]), 'skeletonPosition': mset([skeletonPosition]), 'skeletonDirection': mset([skeletonDirection])})
                                                                                add = Marking({'skeletonPosition': mset([a]), 'skeletonDirection': mset([b]), 'skeletonPosUpdated': mset([c])})
                                                                                succ.add(marking - sub + add)

def succ_051 (marking):
    "successors of 'update skeleton position'"
    succ = set()
    addsucc_051(marking, succ)
    return succ

def itersucc_051 (marking):
    "successors of 'update skeleton position'"
    if marking('mapTBPos') and marking('skeletonDirection') and marking('skeletonPosA') and marking('skeletonPosB') and marking('skeletonActive') and marking('mapTXRange') and marking('executeSkeletonUpdate') and marking('skeletonPosition'):
        for executeSkeletonUpdate in marking('executeSkeletonUpdate'):
            for skeletonActive in marking('skeletonActive'):
                for skeletonPosition in marking('skeletonPosition'):
                    for skeletonPosA in marking('skeletonPosA'):
                        for skeletonPosB in marking('skeletonPosB'):
                            for skeletonDirection in marking('skeletonDirection'):
                                for mapTXRange in marking('mapTXRange'):
                                    for mapTBPos in marking('mapTBPos'):
                                        a = moveEnemy(skeletonActive, skeletonPosition, skeletonDirection, skeletonPosA, skeletonPosB, mapTBPos,mapTXRange)
                                        if isinstance(a, tuple):
                                            b = updateEnemyDirection(skeletonActive, skeletonPosition, skeletonDirection, skeletonPosA, skeletonPosB)
                                            if isinstance(b, int):
                                                if isinstance(skeletonActive, bool):
                                                    if isinstance(skeletonPosA, tuple):
                                                        if isinstance(skeletonPosB, tuple):
                                                            if isinstance(mapTXRange, tuple):
                                                                if isinstance(mapTBPos, tuple):
                                                                    c = 1
                                                                    test = Marking({'mapTBPos': mset([mapTBPos]), 'skeletonPosA': mset([skeletonPosA]), 'skeletonPosB': mset([skeletonPosB]), 'skeletonActive': mset([skeletonActive]), 'mapTXRange': mset([mapTXRange]), 'executeSkeletonUpdate': mset([executeSkeletonUpdate]), 'skeletonPosition': mset([skeletonPosition]), 'skeletonDirection': mset([skeletonDirection])})
                                                                    if test <= marking:
                                                                        sub = Marking({'executeSkeletonUpdate': mset([executeSkeletonUpdate]), 'skeletonPosition': mset([skeletonPosition]), 'skeletonDirection': mset([skeletonDirection])})
                                                                        add = Marking({'skeletonPosition': mset([a]), 'skeletonDirection': mset([b]), 'skeletonPosUpdated': mset([c])})
                                                                        mode = hdict({'mapTXRange': mapTXRange, 'executeSkeletonUpdate': executeSkeletonUpdate, 'skeletonDirection': skeletonDirection, 'skeletonPosition': skeletonPosition, 'mapTBPos': mapTBPos, 'skeletonPosA': skeletonPosA, 'skeletonPosB': skeletonPosB, 'skeletonActive': skeletonActive})
                                                                        yield event('update skeleton position', mode, sub, add)

def addsucc_052 (marking, succ):
    "successors of 'update x position'"
    if marking('moving') and marking('mapTXRange') and marking('playerPosition') and marking('mapTBPos'):
        for playerPosition in marking('playerPosition'):
            for moving in marking('moving'):
                for mapTXRange in marking('mapTXRange'):
                    for mapTBPos in marking('mapTBPos'):
                        a = updatePositionX(playerPosition,moving,mapTBPos,mapTXRange)
                        if isinstance(a, tuple):
                            if isinstance(mapTXRange, tuple):
                                if isinstance(mapTBPos, tuple):
                                    b = 1
                                    test = Marking({'mapTXRange': mset([mapTXRange]), 'mapTBPos': mset([mapTBPos]), 'playerPosition': mset([playerPosition]), 'moving': mset([moving])})
                                    if test <= marking:
                                        sub = Marking({'playerPosition': mset([playerPosition]), 'moving': mset([moving])})
                                        add = Marking({'playerPosition': mset([a]), 'playerPosUpdated': mset([b])})
                                        succ.add(marking - sub + add)

def succ_052 (marking):
    "successors of 'update x position'"
    succ = set()
    addsucc_052(marking, succ)
    return succ

def itersucc_052 (marking):
    "successors of 'update x position'"
    if marking('moving') and marking('mapTXRange') and marking('playerPosition') and marking('mapTBPos'):
        for playerPosition in marking('playerPosition'):
            for moving in marking('moving'):
                for mapTXRange in marking('mapTXRange'):
                    for mapTBPos in marking('mapTBPos'):
                        a = updatePositionX(playerPosition,moving,mapTBPos,mapTXRange)
                        if isinstance(a, tuple):
                            if isinstance(mapTXRange, tuple):
                                if isinstance(mapTBPos, tuple):
                                    b = 1
                                    test = Marking({'mapTXRange': mset([mapTXRange]), 'mapTBPos': mset([mapTBPos]), 'playerPosition': mset([playerPosition]), 'moving': mset([moving])})
                                    if test <= marking:
                                        sub = Marking({'playerPosition': mset([playerPosition]), 'moving': mset([moving])})
                                        add = Marking({'playerPosition': mset([a]), 'playerPosUpdated': mset([b])})
                                        mode = hdict({'moving': moving, 'mapTXRange': mapTXRange, 'playerPosition': playerPosition, 'mapTBPos': mapTBPos})
                                        yield event('update x position', mode, sub, add)

def addsucc_053 (marking, succ):
    "successors of 'updateFireballPosition'"
    if marking('updateFireball') and marking('fireballDirection') and marking('fireballPosition'):
        for updateFireball in marking('updateFireball'):
            for fireballDirection in marking('fireballDirection'):
                for fireballPosition in marking('fireballPosition'):
                    if isinstance(fireballDirection, int):
                        a = updateFireballPosition(fireballPosition, fireballDirection)
                        if isinstance(a, tuple):
                            b = 1
                            test = Marking({'fireballDirection': mset([fireballDirection]), 'updateFireball': mset([updateFireball]), 'fireballPosition': mset([fireballPosition])})
                            if test <= marking:
                                sub = Marking({'updateFireball': mset([updateFireball]), 'fireballPosition': mset([fireballPosition])})
                                add = Marking({'fireballPosition': mset([a]), 'fireballUpdated': mset([b])})
                                succ.add(marking - sub + add)

def succ_053 (marking):
    "successors of 'updateFireballPosition'"
    succ = set()
    addsucc_053(marking, succ)
    return succ

def itersucc_053 (marking):
    "successors of 'updateFireballPosition'"
    if marking('updateFireball') and marking('fireballDirection') and marking('fireballPosition'):
        for updateFireball in marking('updateFireball'):
            for fireballDirection in marking('fireballDirection'):
                for fireballPosition in marking('fireballPosition'):
                    if isinstance(fireballDirection, int):
                        a = updateFireballPosition(fireballPosition, fireballDirection)
                        if isinstance(a, tuple):
                            b = 1
                            test = Marking({'fireballDirection': mset([fireballDirection]), 'updateFireball': mset([updateFireball]), 'fireballPosition': mset([fireballPosition])})
                            if test <= marking:
                                sub = Marking({'updateFireball': mset([updateFireball]), 'fireballPosition': mset([fireballPosition])})
                                add = Marking({'fireballPosition': mset([a]), 'fireballUpdated': mset([b])})
                                mode = hdict({'updateFireball': updateFireball, 'fireballDirection': fireballDirection, 'fireballPosition': fireballPosition})
                                yield event('updateFireballPosition', mode, sub, add)

def addsucc_054 (marking, succ):
    "successors of 'use laser eyes'"
    if marking('usingLaserEyes') and marking('laserEyes'):
        for usingLaserEyes in marking('usingLaserEyes'):
            for laserEyes in marking('laserEyes'):
                if isinstance(laserEyes, bool):
                    a = canUseLaserEyes(laserEyes, True)
                    b = canUseLaserEyes(laserEyes, False)
                    test = Marking({'laserEyes': mset([laserEyes]), 'usingLaserEyes': mset([usingLaserEyes])})
                    if test <= marking:
                        sub = Marking({'usingLaserEyes': mset([usingLaserEyes])})
                        if(a == None):
                            add = Marking({'notLasered': mset([b])})
                        elif(b == None):
                            add = Marking({'lasered': mset([a])})
                        succ.add(marking - sub + add)

def succ_054 (marking):
    "successors of 'use laser eyes'"
    succ = set()
    addsucc_054(marking, succ)
    return succ

def itersucc_054 (marking):
    "successors of 'use laser eyes'"
    if marking('usingLaserEyes') and marking('laserEyes'):
        for usingLaserEyes in marking('usingLaserEyes'):
            for laserEyes in marking('laserEyes'):
                if isinstance(laserEyes, bool):
                    a = canUseLaserEyes(laserEyes, True)
                    b = canUseLaserEyes(laserEyes, False)
                    test = Marking({'laserEyes': mset([laserEyes]), 'usingLaserEyes': mset([usingLaserEyes])})
                    if test <= marking:
                        sub = Marking({'usingLaserEyes': mset([usingLaserEyes])})
                        add = Marking({'lasered': mset([a]), 'notLasered': mset([b])})
                        mode = hdict({'usingLaserEyes': usingLaserEyes, 'laserEyes': laserEyes})
                        yield event('use laser eyes', mode, sub, add)

def addsucc_055 (marking, succ):
    "successors of 'z clicked'"
    if marking('checkZ') and marking('fireBalls'):
        for checkZ in marking('checkZ'):
            for fireBalls in marking('fireBalls'):
                a = canCreateFireball(fireBalls, True)
                if isinstance(fireBalls, int):
                    b = canCreateFireball(fireBalls, False)
                    test = Marking({'fireBalls': mset([fireBalls]), 'checkZ': mset([checkZ])})
                    if test <= marking:
                        sub = Marking({'checkZ': mset([checkZ])})
                        if(a == None):
                            add = Marking({'updateEnded': mset([b])})
                        elif(b == None):
                            add = Marking({'createFireball': mset([a])})
                        succ.add(marking - sub + add)

def succ_055 (marking):
    "successors of 'z clicked'"
    succ = set()
    addsucc_055(marking, succ)
    return succ

def itersucc_055 (marking):
    "successors of 'z clicked'"
    if marking('checkZ') and marking('fireBalls'):
        for checkZ in marking('checkZ'):
            for fireBalls in marking('fireBalls'):
                a = canCreateFireball(fireBalls, True)
                if isinstance(fireBalls, int):
                    b = canCreateFireball(fireBalls, False)
                    test = Marking({'fireBalls': mset([fireBalls]), 'checkZ': mset([checkZ])})
                    if test <= marking:
                        sub = Marking({'checkZ': mset([checkZ])})
                        add = Marking({'createFireball': mset([a]), 'updateEnded': mset([b])})
                        mode = hdict({'checkZ': checkZ, 'fireBalls': fireBalls})
                        yield event('z clicked', mode, sub, add)

def addsucc_056 (marking, succ):
    "successors of 'z not clicked'"
    if marking('checkZ'):
        for checkZ in marking('checkZ'):
            a = 1
            sub = Marking({'checkZ': mset([checkZ])})
            if sub <= marking:
                add = Marking({'updateEnded': mset([a])})
                succ.add(marking - sub + add)

def succ_056 (marking):
    "successors of 'z not clicked'"
    succ = set()
    addsucc_056(marking, succ)
    return succ

def itersucc_056 (marking):
    "successors of 'z not clicked'"
    if marking('checkZ'):
        for checkZ in marking('checkZ'):
            a = 1
            sub = Marking({'checkZ': mset([checkZ])})
            if sub <= marking:
                add = Marking({'updateEnded': mset([a])})
                mode = hdict({'checkZ': checkZ})
                yield event('z not clicked', mode, sub, add)

def addsucc_057 (marking, succ):
    "successors of 'check skeleton position'"
    if marking('skeletonPosA') and marking('skeletonActive') and marking('skeletonPosition') and marking('skeletonWaitingCounter') and marking('skeletonPosB') and marking('executeSkeletonUpdate') and marking('skeletonDirection'):
        for executeSkeletonUpdate in marking('executeSkeletonUpdate'):
            for skeletonActive in marking('skeletonActive'):
                for skeletonPosition in marking('skeletonPosition'):
                    for skeletonPosA in marking('skeletonPosA'):
                        for skeletonPosB in marking('skeletonPosB'):
                            for skeletonDirection in marking('skeletonDirection'):
                                for skeletonWaitingCounter in marking('skeletonWaitingCounter'):
                                    if isinstance(skeletonPosition, tuple):
                                        if isinstance(skeletonDirection, int):
                                            if isinstance(skeletonActive, bool):
                                                if isinstance(skeletonPosA, tuple):
                                                    if isinstance(skeletonPosB, tuple):
                                                        a = activateEnemyAwait(skeletonWaitingCounter, skeletonPosition, skeletonDirection, skeletonActive, skeletonPosA, skeletonPosB)
                                                        if isinstance(a, int):
                                                            b = 1
                                                            if isinstance(b, int):
                                                                test = Marking({'skeletonDirection': mset([skeletonDirection]), 'skeletonPosB': mset([skeletonPosB]), 'skeletonPosA': mset([skeletonPosA]), 'skeletonPosition': mset([skeletonPosition]), 'skeletonActive': mset([skeletonActive]), 'executeSkeletonUpdate': mset([executeSkeletonUpdate]), 'skeletonWaitingCounter': mset([skeletonWaitingCounter])})
                                                                if test <= marking:
                                                                    sub = Marking({'executeSkeletonUpdate': mset([executeSkeletonUpdate]), 'skeletonWaitingCounter': mset([skeletonWaitingCounter])})
                                                                    add = Marking({'skeletonWaitingCounter': mset([a]), 'skeletonPosChecked': mset([b])})
                                                                    succ.add(marking - sub + add)

def succ_057 (marking):
    "successors of 'check skeleton position'"
    succ = set()
    addsucc_057(marking, succ)
    return succ


def addsucc_058 (marking, succ):
    "successors of 'check enemy position'"
    if marking('enemy0PosA') and marking('enemy0Active') and marking('executeEnemyUpdate') and marking('enemy0Direction') and marking('enemy0Position') and marking('enemy0PosB') and marking('enemyWaitingCounter'):
        for executeEnemyUpdate in marking('executeEnemyUpdate'):
            for enemy0Active in marking('enemy0Active'):
                for enemy0Position in marking('enemy0Position'):
                    for enemy0PosA in marking('enemy0PosA'):
                        for enemy0PosB in marking('enemy0PosB'):
                            for enemy0Direction in marking('enemy0Direction'):
                                for enemyWaitingCounter in marking('enemyWaitingCounter'):
                                    if isinstance(enemy0Position, tuple):
                                        if isinstance(enemy0Direction, int):
                                            if isinstance(enemy0Active, bool):
                                                if isinstance(enemy0PosA, tuple):
                                                    if isinstance(enemy0PosB, tuple):
                                                        a = activateEnemyAwait(enemyWaitingCounter, enemy0Position, enemy0Direction, enemy0Active, enemy0PosA, enemy0PosB)
                                                        if isinstance(a, int):
                                                            b = 1
                                                            if isinstance(b, int):
                                                                test = Marking({'enemy0PosB': mset([enemy0PosB]), 'enemy0Active': mset([enemy0Active]), 'enemy0PosA': mset([enemy0PosA]), 'enemy0Direction': mset([enemy0Direction]), 'enemy0Position': mset([enemy0Position]), 'executeEnemyUpdate': mset([executeEnemyUpdate]), 'enemyWaitingCounter': mset([enemyWaitingCounter])})
                                                                if test <= marking:
                                                                    sub = Marking({'executeEnemyUpdate': mset([executeEnemyUpdate]), 'enemyWaitingCounter': mset([enemyWaitingCounter])})
                                                                    add = Marking({'enemyWaitingCounter': mset([a]), 'enemyPosChecked': mset([b])})
                                                                    succ.add(marking - sub + add)

def succ_058 (marking):
    "successors of 'check enemy position'"
    succ = set()
    addsucc_058(marking, succ)
    return succ

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
    addsucc_020(marking, succ)
    addsucc_021(marking, succ)
    addsucc_022(marking, succ)
    addsucc_023(marking, succ)
    addsucc_024(marking, succ)
    addsucc_025(marking, succ)
    addsucc_026(marking, succ)
    addsucc_027(marking, succ)
    addsucc_028(marking, succ)
    addsucc_029(marking, succ)
    addsucc_030(marking, succ)
    addsucc_031(marking, succ)
    addsucc_032(marking, succ)
    addsucc_033(marking, succ)
    addsucc_034(marking, succ)
    addsucc_035(marking, succ)
    addsucc_036(marking, succ)
    addsucc_037(marking, succ)
    addsucc_038(marking, succ)
    addsucc_039(marking, succ)
    addsucc_040(marking, succ)
    addsucc_041(marking, succ)
    addsucc_042(marking, succ)
    addsucc_043(marking, succ)
    addsucc_044(marking, succ)
    addsucc_045(marking, succ)
    addsucc_046(marking, succ)
    addsucc_047(marking, succ)
    addsucc_048(marking, succ)
    addsucc_049(marking, succ)
    addsucc_050(marking, succ)
    addsucc_051(marking, succ)
    addsucc_052(marking, succ)
    addsucc_053(marking, succ)
    addsucc_054(marking, succ)
    addsucc_055(marking, succ)
    addsucc_056(marking, succ)
    addsucc_057(marking, succ)
    addsucc_058(marking, succ)

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
                           itersucc_019(marking),
                           itersucc_020(marking),
                           itersucc_021(marking),
                           itersucc_022(marking),
                           itersucc_023(marking),
                           itersucc_024(marking),
                           itersucc_025(marking),
                           itersucc_026(marking),
                           itersucc_027(marking),
                           itersucc_028(marking),
                           itersucc_029(marking),
                           itersucc_030(marking),
                           itersucc_031(marking),
                           itersucc_032(marking),
                           itersucc_033(marking),
                           itersucc_034(marking),
                           itersucc_035(marking),
                           itersucc_036(marking),
                           itersucc_037(marking),
                           itersucc_038(marking),
                           itersucc_039(marking),
                           itersucc_040(marking),
                           itersucc_041(marking),
                           itersucc_042(marking),
                           itersucc_043(marking),
                           itersucc_044(marking),
                           itersucc_045(marking),
                           itersucc_046(marking),
                           itersucc_047(marking),
                           itersucc_048(marking),
                           itersucc_049(marking),
                           itersucc_050(marking),
                           itersucc_051(marking),
                           itersucc_052(marking),
                           itersucc_053(marking),
                           itersucc_054(marking),
                           itersucc_055(marking),
                           itersucc_056(marking))

def init ():
    'initial marking'
    return Marking({'startGame': mset([1]), 'spawnPoints': mset([((5.0, 1.0), (-14.0, 1.0), (-5.0, 1.0), (11.0, 1.0))]), 'mapTXRange': mset([(-15.0, 15.0)]), 'mapTBPos': mset([(0.0, 4.0)]), 'playerPosition': mset([(0.0, 1.0)]), 'collisionEnterSkeleton': mset([0]), 'fireBallPotionActive': mset([True]), 'fireballPotionPosition': mset([(-4.0, 1.0)]), 'fireBalls': mset([0]), 'laserEyesPotionActive': mset([True]), 'laserEyesPotionPosition': mset([(9.0, 2.0)]), 'laserEyes': mset([False]), 'healthPotionActive': mset([True]), 'healthPotionPosition': mset([(13.0, 2.0)]), 'health': mset([6]), 'teleportPotionActive': mset([True]), 'teleportPotionPosition': mset([(-9.0, 2.0)]), 'teleports': mset([0]), 'hasHat': mset([False]), 'hatPosition': mset([(11.0, 3.0)]), 'collisionEnterEnemy': mset([0]), 'bigDamage': mset([(-30.0, -16.0, -10.0, 0.0)]), 'jumps': mset([2]), 'enemy0Health': mset([2]), 'skeletonHealth': mset([3]), 'direction': mset([1]), 'speeding': mset([False]), 'showGameoverUI': mset([False]), 'fireballActive': mset([False]), 'skeletonWaitingCounter': mset([0]), 'enemyWaitingCounter': mset([0])})

# map transitions names to successor procs
# '' maps to all-transitions proc
succproc = {'': addsucc,
            'arrow clicked': addsucc_001,
            'check collision with big damage': addsucc_002,
            'check collision with enemy': addsucc_003,
            'check collision with fbPotion': addsucc_004,
            'check collision with hPotion': addsucc_005,
            'check collision with hat': addsucc_006,
            'check collision with le potion': addsucc_007,
            'check collision with skeleton': addsucc_008,
            'check collision with tPotion': addsucc_009,
            'check collisions': addsucc_010,
            'check laser hit': addsucc_011,
            'check player health': addsucc_012,
            'checkFireballActive': addsucc_013,
            'create enemies': addsucc_014,
            'ctrl clicked': addsucc_015,
            'ctrl not clicked': addsucc_016,
            'decrease enemy health': addsucc_017,
            'execute fixed update': addsucc_018,
            'execute start': addsucc_019,
            'execute update': addsucc_020,
            'fire': addsucc_021,
            'is fireball active': addsucc_022,
            'left arrow clicked': addsucc_023,
            'mouse0 clicked fixed': addsucc_024,
            'mouse0 not clicked fixed': addsucc_025,
            'move': addsucc_026,
            'nextIter': addsucc_027,
            'no laser': addsucc_028,
            'on collision enemy': addsucc_029,
            'on collision fbPotion': addsucc_030,
            'on collision hat': addsucc_031,
            'on collision health': addsucc_032,
            'on collision le': addsucc_033,
            'on collision skeleton': addsucc_034,
            'on collision teleport': addsucc_035,
            'on create enemy0': addsucc_036,
            'on create skeleton': addsucc_037,
            'on fireball collision': addsucc_038,
            'on generate level': addsucc_039,
            'on mouse0 clicked': addsucc_040,
            'on mouse0 not clicked': addsucc_041,
            'on space clicked': addsucc_042,
            'on space not clicked': addsucc_043,
            'on start ended': addsucc_044,
            'reset jumps': addsucc_045,
            'right arrow clicked': addsucc_046,
            'stay in place': addsucc_047,
            'take player input': addsucc_048,
            'update enemy position': addsucc_049,
            'update gravity': addsucc_050,
            'update skeleton position': addsucc_051,
            'update x position': addsucc_052,
            'updateFireballPosition': addsucc_053,
            'use laser eyes': addsucc_054,
            'z clicked': addsucc_055,
            'z not clicked': addsucc_056}

# map transitions names to successor funcs
# '' maps to all-transitions func
succfunc = {'': succ,
            'arrow clicked': succ_001,
            'check collision with big damage': succ_002,
            'check collision with enemy': succ_003,
            'check collision with fbPotion': succ_004,
            'check collision with hPotion': succ_005,
            'check collision with hat': succ_006,
            'check collision with le potion': succ_007,
            'check collision with skeleton': succ_008,
            'check collision with tPotion': succ_009,
            'check collisions': succ_010,
            'check laser hit': succ_011,
            'check player health': succ_012,
            'checkFireballActive': succ_013,
            'create enemies': succ_014,
            'ctrl clicked': succ_015,
            'ctrl not clicked': succ_016,
            'decrease enemy health': succ_017,
            'execute fixed update': succ_018,
            'execute start': succ_019,
            'execute update': succ_020,
            'fire': succ_021,
            'is fireball active': succ_022,
            'left arrow clicked': succ_023,
            'mouse0 clicked fixed': succ_024,
            'mouse0 not clicked fixed': succ_025,
            'move': succ_026,
            'nextIter': succ_027,
            'no laser': succ_028,
            'on collision enemy': succ_029,
            'on collision fbPotion': succ_030,
            'on collision hat': succ_031,
            'on collision health': succ_032,
            'on collision le': succ_033,
            'on collision skeleton': succ_034,
            'on collision teleport': succ_035,
            'on create enemy0': succ_036,
            'on create skeleton': succ_037,
            'on fireball collision': succ_038,
            'on generate level': succ_039,
            'on mouse0 clicked': succ_040,
            'on mouse0 not clicked': succ_041,
            'on space clicked': succ_042,
            'on space not clicked': succ_043,
            'on start ended': succ_044,
            'reset jumps': succ_045,
            'right arrow clicked': succ_046,
            'stay in place': succ_047,
            'take player input': succ_048,
            'update enemy position': succ_049,
            'update gravity': succ_050,
            'update skeleton position': succ_051,
            'update x position': succ_052,
            'updateFireballPosition': succ_053,
            'use laser eyes': succ_054,
            'z clicked': succ_055,
            'z not clicked': succ_056,
            'check skeleton position': succ_057,
            'check enemy position': succ_058}

# map transitions names to successor iterators
# '' maps to all-transitions iterator
succiter = {'': itersucc,
            'arrow clicked': itersucc_001,
            'check collision with big damage': itersucc_002,
            'check collision with enemy': itersucc_003,
            'check collision with fbPotion': itersucc_004,
            'check collision with hPotion': itersucc_005,
            'check collision with hat': itersucc_006,
            'check collision with le potion': itersucc_007,
            'check collision with skeleton': itersucc_008,
            'check collision with tPotion': itersucc_009,
            'check collisions': itersucc_010,
            'check laser hit': itersucc_011,
            'check player health': itersucc_012,
            'checkFireballActive': itersucc_013,
            'create enemies': itersucc_014,
            'ctrl clicked': itersucc_015,
            'ctrl not clicked': itersucc_016,
            'decrease enemy health': itersucc_017,
            'execute fixed update': itersucc_018,
            'execute start': itersucc_019,
            'execute update': itersucc_020,
            'fire': itersucc_021,
            'is fireball active': itersucc_022,
            'left arrow clicked': itersucc_023,
            'mouse0 clicked fixed': itersucc_024,
            'mouse0 not clicked fixed': itersucc_025,
            'move': itersucc_026,
            'nextIter': itersucc_027,
            'no laser': itersucc_028,
            'on collision enemy': itersucc_029,
            'on collision fbPotion': itersucc_030,
            'on collision hat': itersucc_031,
            'on collision health': itersucc_032,
            'on collision le': itersucc_033,
            'on collision skeleton': itersucc_034,
            'on collision teleport': itersucc_035,
            'on create enemy0': itersucc_036,
            'on create skeleton': itersucc_037,
            'on fireball collision': itersucc_038,
            'on generate level': itersucc_039,
            'on mouse0 clicked': itersucc_040,
            'on mouse0 not clicked': itersucc_041,
            'on space clicked': itersucc_042,
            'on space not clicked': itersucc_043,
            'on start ended': itersucc_044,
            'reset jumps': itersucc_045,
            'right arrow clicked': itersucc_046,
            'stay in place': itersucc_047,
            'take player input': itersucc_048,
            'update enemy position': itersucc_049,
            'update gravity': itersucc_050,
            'update skeleton position': itersucc_051,
            'update x position': itersucc_052,
            'updateFireballPosition': itersucc_053,
            'use laser eyes': itersucc_054,
            'z clicked': itersucc_055,
            'z not clicked': itersucc_056}

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
