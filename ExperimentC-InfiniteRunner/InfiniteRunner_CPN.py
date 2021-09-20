NET = 'net'
import itertools, collections

from zinc.nets import Marking, mset, dot, hdict
event = collections.namedtuple('event', ['trans', 'mode', 'sub', 'add'])

def updateGravity(pos, platformA, platformB):
  if(pos[0] >= platformA[0] and pos[0] <= platformA[1]):
    if((pos[1] > (platformA[2] + 1.0)) or (pos[1] < (platformA[2]))):
      return (pos[0],pos[1] - 0.5)
    else:
      return pos
  elif(pos[0] >= platformB[0] and pos[0] <= platformB[1]):
    if((pos[1] > (platformB[2] + 1.0)) or (pos[1] < (platformB[2]))):
      return (pos[0],pos[1] - 0.5)
    else:
      return pos
  else:
    return (pos[0],pos[1] - 0.5)


def onCollisionWithPlatform(pos, platformA, platformB):
  if((pos[0] >= platformA[0] and pos[0] <= platformA[1])  and 
     ((abs(pos[1] - (platformA[2])) <= 1) and pos[1] > platformA[2])):
     return (pos[0], platformA[2] + 1)
  
  if((pos[0] >= platformB[0] and pos[0] <= platformB[1])  and 
     ((abs(pos[1] - (platformB[2])) <= 1) and pos[1] > platformB[2])):
     return (pos[0], platformB[2] + 1)

  return pos

def onCollisionWithPlatformCanJump(pos, platformA, platformB):
  if((pos[0] >= platformA[0] and pos[0] <= platformA[1])  and 
     ((abs(pos[1] - (platformA[2])) <= 1) and pos[1] > platformA[2])):
     return True
  
  if((pos[0] >= platformB[0] and pos[0] <= platformB[1])  and 
     ((abs(pos[1] - (platformB[2])) <= 1) and pos[1] > platformB[2])):
     return True

  return False

def onCollisionWithExitPointUpdatePlatform(pos, exitPoint, platformOfExit, otherPlatform):
  if(pos[0] == exitPoint[0] and (pos[1] >= exitPoint[1] and pos[1] <= exitPoint[2])):
    deffer = abs(platformOfExit[0] - platformOfExit[1])
    return (otherPlatform[1] + 2, otherPlatform[1] + 2 + deffer, platformOfExit[2])
  return platformOfExit

def onCollisionWithExitPoint(pos, exitPoint, platformOfExit, otherPlatform):
  newPltExit = onCollisionWithExitPointUpdatePlatform(pos, exitPoint, platformOfExit, otherPlatform)

  if(newPltExit != platformOfExit):
    return (newPltExit[1] + 4, exitPoint[1], exitPoint[2])

  return exitPoint

def onCollisionWithExitPointUpdateScore(score, pos, platformA, exitPointA, platformB, exitPointB):
  newpltA = onCollisionWithExitPointUpdatePlatform(pos, exitPointA, platformA, platformB)
  newpltB = onCollisionWithExitPointUpdatePlatform(pos, exitPointB, platformB, platformA)

  if(newpltA[0] != platformA[0] or newpltA[1] != platformA[1]):
    return score + 1
  
  if(newpltB[0] != platformB[0] or newpltB[1] != platformB[1]):
    return score + 1

  return score

def onCollisionWithExitPointUpdateEnemy(enemy, pos, platformA, exitPointA, platformB):
  newPltExit = onCollisionWithExitPointUpdatePlatform(pos, exitPointA, platformA, platformB)

  if(newPltExit != platformA):
    return (newPltExit[0] + 5, enemy[1])

  return enemy

def onCollisionWithExitPointUpdateEPoint(ePoint, pos, platformA, exitPointA, platformB):
  newPltExit = onCollisionWithExitPointUpdatePlatform(pos, exitPointA, platformA, platformB)

  if(newPltExit != platformA):
    return (newPltExit[0] + 3, newPltExit[1] - 2)
    
  return ePoint

def moveKillZone(pos, platformA, exitPointA, platformB, exitPointB, killZone):
  newpltA = onCollisionWithExitPointUpdatePlatform(pos, exitPointA, platformA, platformB)
  newpltB = onCollisionWithExitPointUpdatePlatform(pos, exitPointB, platformB, platformA)

  return (min(newpltA[0], newpltB[0]), max(newpltA[1], newpltB[1]), killZone[2])


def onCollisionKillZone(pos, killZone):
  if(pos[0] >= killZone[0] and pos[0] <= killZone[1] and pos[1] == killZone[2]):
    return True
  return False
  


def onCollisionEnterWithEnemy(playerPos, enemyPos, colEnter):
  if(playerPos[0] == enemyPos[0] and playerPos[1] == enemyPos[1]):
    return colEnter + 1
  else:
    return 0

def decreaseHealthWithEnemy(health, playerPos, enemyPos, colEnter):
  if((colEnter == 0) and (playerPos[0] == enemyPos[0] and playerPos[1] == enemyPos[1])):
    return health - 1
  else:
    return health

def onEnemyCollisionChecked(health, playerPos, enemyPos):
  if(playerPos[0] == enemyPos[0] and playerPos[1] == enemyPos[1]):
    return health - 1
  else:
    return health


def updateEnemy(enemy, ePoint, direction):
  enemyDirection = direction
  if(enemy[0] == ePoint[0]):
    enemyDirection = 1
  if(enemy[0] == ePoint[1]):
    enemyDirection = -1
  if((enemy[0] + enemyDirection) >= ePoint[0] and (enemy[0] + enemyDirection) <= ePoint[1]):
    return updatePositionX(enemy, enemyDirection)
  else:
    return enemy

def updatePositionX(position,moveVal):
  
  return (position[0] + moveVal, position[1])

def updateEnemyDirection(enemyPos, enemyDirection, ePoint):
  if(enemyPos[0] == ePoint[0]):
    return 1
  if(enemyPos[0] == ePoint[1]):
    return -1
  return enemyDirection


def addJumpForce(jumpForce, canJump, stamina = 0):
  if(canJump):
    returnVal = jumpForce + 1.5
    if(stamina >= 10):
      returnVal += 1.5

    return returnVal
  else:
    return jumpForce

def onFixedUpdate(withKillZone, val):
  if(withKillZone == val):
    return 1
    
def decreaseStamina(stamina):
  if(stamina > 0):
    newStamina = stamina - 10

    if(newStamina < 0):
      return 0
    return newStamina
  return 0


def updatePlayerY(player, jumpForce):
  return (player[0], player[1] + jumpForce)

def onJump(canJump, player, jumpForce):
  newPos = updatePlayerY(player, jumpForce)

  if(player[1] != newPos[1]):
    return False
  
  return canJump


def isDead(health, val):
  if((health <= 0) == val):
    return 1


def addsucc_001 (marking, succ):
    "successors of 'E not pressed'"
    if marking('superJump'):
        for superJump in marking('superJump'):
            a = 1
            sub = Marking({'superJump': mset([superJump])})
            if sub <= marking:
                add = Marking({'eChecked': mset([a])})
                succ.add(marking - sub + add)

def succ_001 (marking):
    "successors of 'E not pressed'"
    succ = set()
    addsucc_001(marking, succ)
    return succ

def itersucc_001 (marking):
    "successors of 'E not pressed'"
    if marking('superJump'):
        for superJump in marking('superJump'):
            a = 1
            sub = Marking({'superJump': mset([superJump])})
            if sub <= marking:
                add = Marking({'eChecked': mset([a])})
                mode = hdict({'superJump': superJump})
                yield event('E not pressed', mode, sub, add)

def addsucc_002 (marking, succ):
    "successors of 'E pressed'"
    if marking('stamina') and marking('jumpForce') and marking('superJump') and marking('canJump'):
        for superJump in marking('superJump'):
            for stamina in marking('stamina'):
                for jumpForce in marking('jumpForce'):
                    for canJump in marking('canJump'):
                        a = addJumpForce(jumpForce, canJump, stamina)
                        if isinstance(a, float):
                            if isinstance(canJump, bool):
                                b = decreaseStamina(stamina)
                                if isinstance(b, int):
                                    c = 1
                                    test = Marking({'canJump': mset([canJump]), 'superJump': mset([superJump]), 'stamina': mset([stamina]), 'jumpForce': mset([jumpForce])})
                                    if test <= marking:
                                        sub = Marking({'superJump': mset([superJump]), 'stamina': mset([stamina]), 'jumpForce': mset([jumpForce])})
                                        add = Marking({'jumpForce': mset([a]), 'stamina': mset([b]), 'eChecked': mset([c])})
                                        succ.add(marking - sub + add)

def succ_002 (marking):
    "successors of 'E pressed'"
    succ = set()
    addsucc_002(marking, succ)
    return succ

def itersucc_002 (marking):
    "successors of 'E pressed'"
    if marking('stamina') and marking('jumpForce') and marking('superJump') and marking('canJump'):
        for superJump in marking('superJump'):
            for stamina in marking('stamina'):
                for jumpForce in marking('jumpForce'):
                    for canJump in marking('canJump'):
                        a = addJumpForce(jumpForce, canJump, stamina)
                        if isinstance(a, int):
                            if isinstance(canJump, bool):
                                b = decreaseStamina(stamina)
                                if isinstance(b, int):
                                    c = 1
                                    test = Marking({'canJump': mset([canJump]), 'superJump': mset([superJump]), 'stamina': mset([stamina]), 'jumpForce': mset([jumpForce])})
                                    if test <= marking:
                                        sub = Marking({'superJump': mset([superJump]), 'stamina': mset([stamina]), 'jumpForce': mset([jumpForce])})
                                        add = Marking({'jumpForce': mset([a]), 'stamina': mset([b]), 'eChecked': mset([c])})
                                        mode = hdict({'superJump': superJump, 'canJump': canJump, 'stamina': stamina, 'jumpForce': jumpForce})
                                        yield event('E pressed', mode, sub, add)

def addsucc_003 (marking, succ):
    "successors of 'check collisions'"
    if marking('gravityUpdated') and marking('player'):
        for gravityUpdated in marking('gravityUpdated'):
            for player in marking('player'):
                if isinstance(player, tuple):
                    test = Marking({'player': mset([player]), 'gravityUpdated': mset([gravityUpdated])})
                    if test <= marking:
                        sub = Marking({'gravityUpdated': mset([gravityUpdated])})
                        add = Marking({'withPlatform': mset([player]), 'withKillzone': mset([player]), 'withExit': mset([player]), 'withEnemy': mset([player])})
                        succ.add(marking - sub + add)

def succ_003 (marking):
    "successors of 'check collisions'"
    succ = set()
    addsucc_003(marking, succ)
    return succ

def itersucc_003 (marking):
    "successors of 'check collisions'"
    if marking('gravityUpdated') and marking('player'):
        for gravityUpdated in marking('gravityUpdated'):
            for player in marking('player'):
                if isinstance(player, tuple):
                    test = Marking({'player': mset([player]), 'gravityUpdated': mset([gravityUpdated])})
                    if test <= marking:
                        sub = Marking({'gravityUpdated': mset([gravityUpdated])})
                        add = Marking({'withPlatform': mset([player]), 'withKillzone': mset([player]), 'withExit': mset([player]), 'withEnemy': mset([player])})
                        mode = hdict({'player': player, 'gravityUpdated': gravityUpdated})
                        yield event('check collisions', mode, sub, add)

def addsucc_004 (marking, succ):
    "successors of 'check gravity'"
    if marking('platformB') and marking('platformA') and marking('player') and marking('gravity'):
        for gravity in marking('gravity'):
            for platformA in marking('platformA'):
                for platformB in marking('platformB'):
                    for player in marking('player'):
                        a = updateGravity(player, platformA, platformB)
                        if isinstance(a, tuple):
                            if isinstance(platformA, tuple):
                                if isinstance(platformB, tuple):
                                    b = 1
                                    test = Marking({'platformA': mset([platformA]), 'platformB': mset([platformB]), 'gravity': mset([gravity]), 'player': mset([player])})
                                    if test <= marking:
                                        sub = Marking({'gravity': mset([gravity]), 'player': mset([player])})
                                        add = Marking({'player': mset([a]), 'gravityUpdated': mset([b])})
                                        succ.add(marking - sub + add)

def succ_004 (marking):
    "successors of 'check gravity'"
    succ = set()
    addsucc_004(marking, succ)
    return succ

def itersucc_004 (marking):
    "successors of 'check gravity'"
    if marking('platformB') and marking('platformA') and marking('player') and marking('gravity'):
        for gravity in marking('gravity'):
            for platformA in marking('platformA'):
                for platformB in marking('platformB'):
                    for player in marking('player'):
                        a = updateGravity(player, platformA, platformB)
                        if isinstance(a, tuple):
                            if isinstance(platformA, tuple):
                                if isinstance(platformB, tuple):
                                    b = 1
                                    test = Marking({'platformA': mset([platformA]), 'platformB': mset([platformB]), 'gravity': mset([gravity]), 'player': mset([player])})
                                    if test <= marking:
                                        sub = Marking({'gravity': mset([gravity]), 'player': mset([player])})
                                        add = Marking({'player': mset([a]), 'gravityUpdated': mset([b])})
                                        mode = hdict({'platformA': platformA, 'player': player, 'gravity': gravity, 'platformB': platformB})
                                        yield event('check gravity', mode, sub, add)

def addsucc_005 (marking, succ):
    "successors of 'checkHealth'"
    if marking('health') and marking('yUpdated'):
        for health in marking('health'):
            for yUpdated in marking('yUpdated'):
                if isinstance(health, int):
                    a = isDead(health, True)
                    b = isDead(health, False)
                    test = Marking({'health': mset([health]), 'yUpdated': mset([yUpdated])})
                    if test <= marking:
                        sub = Marking({'yUpdated': mset([yUpdated])})
                        if(a == None):
                            add = Marking({'gravity': mset([b])})
                        elif(b == None):
                            add = Marking({'gameOver': mset([a])})

                        succ.add(marking - sub + add)

def succ_005 (marking):
    "successors of 'checkHealth'"
    succ = set()
    addsucc_005(marking, succ)
    return succ

def itersucc_005 (marking):
    "successors of 'checkHealth'"
    if marking('health') and marking('yUpdated'):
        for health in marking('health'):
            for yUpdated in marking('yUpdated'):
                if isinstance(health, int):
                    a = isDead(health, True)
                    if isinstance(a, int):
                        b = isDead(health, False)
                        test = Marking({'health': mset([health]), 'yUpdated': mset([yUpdated])})
                        if test <= marking:
                            sub = Marking({'yUpdated': mset([yUpdated])})
                            add = Marking({'startGame': mset([a]), 'gravity': mset([b])})
                            mode = hdict({'yUpdated': yUpdated, 'health': health})
                            yield event('checkHealth', mode, sub, add)

def addsucc_006 (marking, succ):
    "successors of 'fixedUpdate'"
    if marking('platformsChecked') and marking('exitChecked') and marking('killzoneChecked') and marking('enemyChecked'):
        for platformsChecked in marking('platformsChecked'):
            for exitChecked in marking('exitChecked'):
                for killzoneChecked in marking('killzoneChecked'):
                    for enemyChecked in marking('enemyChecked'):
                        a = onFixedUpdate(killzoneChecked, True)
                        b = onFixedUpdate(killzoneChecked, False)
                        sub = Marking({'platformsChecked': mset([platformsChecked]), 'exitChecked': mset([exitChecked]), 'killzoneChecked': mset([killzoneChecked]), 'enemyChecked': mset([enemyChecked])})
                        if sub <= marking:
                            if(a == None):
                                add = Marking({'moveEnemy': mset([b]), 'movePlayer': mset([b])})
                            else:
                                add = Marking({'gameOver': mset([a])})

                            succ.add(marking - sub + add)

def succ_006 (marking):
    "successors of 'fixedUpdate'"
    succ = set()
    addsucc_006(marking, succ)
    return succ

def itersucc_006 (marking):
    "successors of 'fixedUpdate'"
    if marking('withPlatform') and marking('withExit') and marking('withKillzone') and marking('withEnemy'):
        for withPlatform in marking('withPlatform'):
            for withExit in marking('withExit'):
                for withKillzone in marking('withKillzone'):
                    for withEnemy in marking('withEnemy'):
                        a = onFixedUpdate(withKillzone, True)
                        if isinstance(a, bool):
                            b = onFixedUpdate(withKillzone, False)
                            sub = Marking({'withPlatform': mset([withPlatform]), 'withExit': mset([withExit]), 'withKillzone': mset([withKillzone]), 'withEnemy': mset([withEnemy])})
                            if sub <= marking:
                                add = Marking({'gameOver': mset([a]), 'moveEnemy': mset([b]), 'movePlayer': mset([b])})
                                mode = hdict({'withKillzone': withKillzone, 'withEnemy': withEnemy, 'withPlatform': withPlatform, 'withExit': withExit})
                                yield event('fixedUpdate', mode, sub, add)

def addsucc_007 (marking, succ):
    "successors of 'left'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = -1
            sub = Marking({'movePlayer': mset([movePlayer])})
            if sub <= marking:
                add = Marking({'moveVal': mset([a])})
                succ.add(marking - sub + add)

def succ_007 (marking):
    "successors of 'left'"
    succ = set()
    addsucc_007(marking, succ)
    return succ

def itersucc_007 (marking):
    "successors of 'left'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = -1
            sub = Marking({'movePlayer': mset([movePlayer])})
            if sub <= marking:
                add = Marking({'moveVal': mset([a])})
                mode = hdict({'movePlayer': movePlayer})
                yield event('left', mode, sub, add)

def addsucc_008 (marking, succ):
    "successors of 'onCollision enemy'"
    if marking('enemy') and marking('collisionEnterEnemy') and marking('health') and marking('withEnemy'):
        for withEnemy in marking('withEnemy'):
            for health in marking('health'):
                for enemy in marking('enemy'):
                    for collisionEnterEnemy in marking('collisionEnterEnemy'):
                        if isinstance(enemy, tuple):
                            a = onCollisionEnterWithEnemy(withEnemy, enemy, collisionEnterEnemy)
                            if isinstance(a, int):
                                b = decreaseHealthWithEnemy(health, withEnemy, enemy, collisionEnterEnemy)
                                if isinstance(b, int):
                                    c = onEnemyCollisionChecked(health, withEnemy, enemy)
                                    test = Marking({'enemy': mset([enemy]), 'withEnemy': mset([withEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                    if test <= marking:
                                        sub = Marking({'withEnemy': mset([withEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                        add = Marking({'collisionEnterEnemy': mset([a]), 'health': mset([b]), 'enemyChecked': mset([c])})
                                        succ.add(marking - sub + add)

def succ_008 (marking):
    "successors of 'onCollision enemy'"
    succ = set()
    addsucc_008(marking, succ)
    return succ

def itersucc_008 (marking):
    "successors of 'onCollision enemy'"
    if marking('enemy') and marking('collisionEnterEnemy') and marking('health') and marking('withEnemy'):
        for withEnemy in marking('withEnemy'):
            for health in marking('health'):
                for enemy in marking('enemy'):
                    for collisionEnterEnemy in marking('collisionEnterEnemy'):
                        if isinstance(enemy, tuple):
                            a = onCollisionEnterWithEnemy(withEnemy, enemy, collisionEnterEnemy)
                            if isinstance(a, int):
                                b = decreaseHealthWithEnemy(health, withEnemy, enemy, collisionEnterEnemy)
                                if isinstance(b, int):
                                    c = onEnemyCollisionChecked(health, withEnemy, enemy)
                                    test = Marking({'enemy': mset([enemy]), 'withEnemy': mset([withEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                    if test <= marking:
                                        sub = Marking({'withEnemy': mset([withEnemy]), 'health': mset([health]), 'collisionEnterEnemy': mset([collisionEnterEnemy])})
                                        add = Marking({'collisionEnterEnemy': mset([a]), 'health': mset([b]), 'enemyChecked': mset([c])})
                                        mode = hdict({'enemy': enemy, 'collisionEnterEnemy': collisionEnterEnemy, 'health': health, 'withEnemy': withEnemy})
                                        yield event('onCollision enemy', mode, sub, add)

def addsucc_009 (marking, succ):
    "successors of 'onCollision exitPoint'"
    if marking('killZone') and marking('score') and marking('platformB') and marking('ePoint') and marking('withExit') and marking('exitPointB') and marking('enemy') and marking('platformA') and marking('exitPointA'):
        for withExit in marking('withExit'):
            for exitPointA in marking('exitPointA'):
                for exitPointB in marking('exitPointB'):
                    for platformA in marking('platformA'):
                        for platformB in marking('platformB'):
                            for killZone in marking('killZone'):
                                for score in marking('score'):
                                    for enemy in marking('enemy'):
                                        for ePoint in marking('ePoint'):
                                            a = onCollisionWithExitPoint(withExit, exitPointA, platformA, platformB)
                                            if isinstance(a, tuple):
                                                b = onCollisionWithExitPoint(withExit, exitPointB, platformB, platformA)
                                                if isinstance(b, tuple):
                                                    c = onCollisionWithExitPointUpdatePlatform(withExit, exitPointA, platformA, platformB)
                                                    if isinstance(c, tuple):
                                                        d = onCollisionWithExitPointUpdatePlatform(withExit, exitPointB, platformB, platformA)
                                                        if isinstance(d, tuple):
                                                            e = onCollisionWithExitPointUpdateScore(score, withExit, platformA, exitPointA, platformB, exitPointB)
                                                            if isinstance(e, int):
                                                                f = onCollisionWithExitPointUpdateEnemy(enemy, withExit, platformA, exitPointA, platformB)
                                                                if isinstance(f, tuple):
                                                                    g = onCollisionWithExitPointUpdateEPoint(ePoint, withExit, platformA, exitPointA, platformB)
                                                                    if isinstance(g, tuple):
                                                                        h = moveKillZone(withExit, platformA, exitPointA, platformB, exitPointB, killZone)
                                                                        if isinstance(h, tuple):
                                                                            i = 1
                                                                            sub = Marking({'withExit': mset([withExit]), 'exitPointA': mset([exitPointA]), 'exitPointB': mset([exitPointB]), 'platformA': mset([platformA]), 'platformB': mset([platformB]), 'killZone': mset([killZone]), 'score': mset([score]), 'enemy': mset([enemy]), 'ePoint': mset([ePoint])})
                                                                            if sub <= marking:
                                                                                add = Marking({'exitPointA': mset([a]), 'exitPointB': mset([b]), 'platformA': mset([c]), 'platformB': mset([d]), 'score': mset([e]), 'enemy': mset([f]), 'ePoint': mset([g]), 'killZone': mset([h]), 'exitChecked': mset([i])})
                                                                                succ.add(marking - sub + add)

def succ_009 (marking):
    "successors of 'onCollision exitPoint'"
    succ = set()
    addsucc_009(marking, succ)
    return succ

def itersucc_009 (marking):
    "successors of 'onCollision exitPoint'"
    if marking('killZone') and marking('score') and marking('platformB') and marking('ePoint') and marking('withExit') and marking('exitPointB') and marking('enemy') and marking('platformA') and marking('exitPointA'):
        for withExit in marking('withExit'):
            for exitPointA in marking('exitPointA'):
                for exitPointB in marking('exitPointB'):
                    for platformA in marking('platformA'):
                        for platformB in marking('platformB'):
                            for killZone in marking('killZone'):
                                for score in marking('score'):
                                    for enemy in marking('enemy'):
                                        for ePoint in marking('ePoint'):
                                            a = onCollisionWithExitPoint(withExit, exitPointA, platformA, platformB)
                                            if isinstance(a, tuple):
                                                b = onCollisionWithExitPoint(withExit, exitPointB, platformB, platformA)
                                                if isinstance(b, tuple):
                                                    c = onCollisionWithExitPointUpdatePlatform(withExit, exitPointA, platformA, platformB)
                                                    if isinstance(c, tuple):
                                                        d = onCollisionWithExitPointUpdatePlatform(withExit, exitPointB, platformB, platformA)
                                                        if isinstance(d, tuple):
                                                            e = onCollisionWithExitPointUpdateScore(score, withExit, platformA, exitPointA, platformB, exitPointB)
                                                            if isinstance(e, int):
                                                                f = onCollisionWithExitPointUpdateEnemy(enemy, withExit, platformA, exitPointA, platformB)
                                                                if isinstance(f, tuple):
                                                                    g = onCollisionWithExitPointUpdateEPoint(ePoint, withExit, platformA, exitPointA, platformB)
                                                                    if isinstance(g, tuple):
                                                                        h = moveKillZone(withExit, platformA, exitPointA, platformB, exitPointB, killZone)
                                                                        if isinstance(h, tuple):
                                                                            i = 1
                                                                            sub = Marking({'withExit': mset([withExit]), 'exitPointA': mset([exitPointA]), 'exitPointB': mset([exitPointB]), 'platformA': mset([platformA]), 'platformB': mset([platformB]), 'killZone': mset([killZone]), 'score': mset([score]), 'enemy': mset([enemy]), 'ePoint': mset([ePoint])})
                                                                            if sub <= marking:
                                                                                add = Marking({'exitPointA': mset([a]), 'exitPointB': mset([b]), 'platformA': mset([c]), 'platformB': mset([d]), 'score': mset([e]), 'enemy': mset([f]), 'ePoint': mset([g]), 'killZone': mset([h]), 'exitChecked': mset([i])})
                                                                                mode = hdict({'ePoint': ePoint, 'score': score, 'platformB': platformB, 'killZone': killZone, 'platformA': platformA, 'exitPointA': exitPointA, 'exitPointB': exitPointB, 'enemy': enemy, 'withExit': withExit})
                                                                                yield event('onCollision exitPoint', mode, sub, add)

def addsucc_010 (marking, succ):
    "successors of 'onCollision killZone'"
    if marking('killZone') and marking('withKillzone'):
        for withKillzone in marking('withKillzone'):
            for killZone in marking('killZone'):
                if isinstance(killZone, tuple):
                    a = onCollisionKillZone(withKillzone, killZone)
                    test = Marking({'killZone': mset([killZone]), 'withKillzone': mset([withKillzone])})
                    if test <= marking:
                        sub = Marking({'withKillzone': mset([withKillzone])})
                        add = Marking({'killzoneChecked': mset([a])})
                        succ.add(marking - sub + add)

def succ_010 (marking):
    "successors of 'onCollision killZone'"
    succ = set()
    addsucc_010(marking, succ)
    return succ

def itersucc_010 (marking):
    "successors of 'onCollision killZone'"
    if marking('killZone') and marking('withKillzone'):
        for withKillzone in marking('withKillzone'):
            for killZone in marking('killZone'):
                if isinstance(killZone, tuple):
                    a = onCollisionKillZone(withKillzone, killZone)
                    test = Marking({'killZone': mset([killZone]), 'withKillzone': mset([withKillzone])})
                    if test <= marking:
                        sub = Marking({'withKillzone': mset([withKillzone])})
                        add = Marking({'killzoneChecked': mset([a])})
                        mode = hdict({'withKillzone': withKillzone, 'killZone': killZone})
                        yield event('onCollision killZone', mode, sub, add)

def addsucc_011 (marking, succ):
    "successors of 'onCollision platform'"
    if marking('platformB') and marking('player') and marking('canJump') and marking('withPlatform') and marking('platformA'):
        for withPlatform in marking('withPlatform'):
            for platformA in marking('platformA'):
                for platformB in marking('platformB'):
                    for player in marking('player'):
                        for canJump in marking('canJump'):
                            a = onCollisionWithPlatform(withPlatform, platformA, platformB)
                            if isinstance(a, tuple):
                                b = onCollisionWithPlatformCanJump(withPlatform, platformA, platformB)
                                if isinstance(b, bool):
                                    if isinstance(platformA, tuple):
                                        if isinstance(platformB, tuple):
                                            c = 1
                                            test = Marking({'platformA': mset([platformA]), 'platformB': mset([platformB]), 'withPlatform': mset([withPlatform]), 'player': mset([player]), 'canJump': mset([canJump])})
                                            if test <= marking:
                                                sub = Marking({'withPlatform': mset([withPlatform]), 'player': mset([player]), 'canJump': mset([canJump])})
                                                add = Marking({'player': mset([a]), 'canJump': mset([b]), 'platformsChecked': mset([c])})
                                                succ.add(marking - sub + add)

def succ_011 (marking):
    "successors of 'onCollision platform'"
    succ = set()
    addsucc_011(marking, succ)
    return succ

def itersucc_011 (marking):
    "successors of 'onCollision platform'"
    if marking('platformB') and marking('player') and marking('canJump') and marking('withPlatform') and marking('platformA'):
        for withPlatform in marking('withPlatform'):
            for platformA in marking('platformA'):
                for platformB in marking('platformB'):
                    for player in marking('player'):
                        for canJump in marking('canJump'):
                            a = onCollisionWithPlatform(withPlatform, platformA, platformB)
                            if isinstance(a, tuple):
                                b = onCollisionWithPlatformCanJump(withPlatform, platformA, platformB)
                                if isinstance(b, bool):
                                    if isinstance(platformA, tuple):
                                        if isinstance(platformB, tuple):
                                            c = 1
                                            test = Marking({'platformA': mset([platformA]), 'platformB': mset([platformB]), 'withPlatform': mset([withPlatform]), 'player': mset([player]), 'canJump': mset([canJump])})
                                            if test <= marking:
                                                sub = Marking({'withPlatform': mset([withPlatform]), 'player': mset([player]), 'canJump': mset([canJump])})
                                                add = Marking({'player': mset([a]), 'canJump': mset([b]), 'platformsChecked': mset([c])})
                                                mode = hdict({'platformA': platformA, 'player': player, 'platformB': platformB, 'withPlatform': withPlatform, 'canJump': canJump})
                                                yield event('onCollision platform', mode, sub, add)

def addsucc_012 (marking, succ):
    "successors of 'onMove Enemy'"
    if marking('eDirection') and marking('enemy') and marking('ePoint') and marking('moveEnemy'):
        for moveEnemy in marking('moveEnemy'):
            for enemy in marking('enemy'):
                for ePoint in marking('ePoint'):
                    for eDirection in marking('eDirection'):
                        a = updateEnemy(enemy, ePoint, eDirection)
                        if isinstance(a, tuple):
                            b = updateEnemyDirection(enemy, eDirection, ePoint)
                            if isinstance(b, int):
                                if isinstance(ePoint, tuple):
                                    c = 1
                                    test = Marking({'ePoint': mset([ePoint]), 'moveEnemy': mset([moveEnemy]), 'enemy': mset([enemy]), 'eDirection': mset([eDirection])})
                                    if test <= marking:
                                        sub = Marking({'moveEnemy': mset([moveEnemy]), 'enemy': mset([enemy]), 'eDirection': mset([eDirection])})
                                        add = Marking({'enemy': mset([a]), 'eDirection': mset([b]), 'enemyMoved': mset([c])})
                                        succ.add(marking - sub + add)

def succ_012 (marking):
    "successors of 'onMove Enemy'"
    succ = set()
    addsucc_012(marking, succ)
    return succ

def itersucc_012 (marking):
    "successors of 'onMove Enemy'"
    if marking('eDirection') and marking('enemy') and marking('ePoint') and marking('moveEnemy'):
        for moveEnemy in marking('moveEnemy'):
            for enemy in marking('enemy'):
                for ePoint in marking('ePoint'):
                    for eDirection in marking('eDirection'):
                        a = updateEnemy(enemy, ePoint, eDirection)
                        if isinstance(a, tuple):
                            b = updateEnemyDirection(enemy, eDirection, ePoint)
                            if isinstance(b, bool):
                                if isinstance(ePoint, tuple):
                                    c = 1
                                    test = Marking({'ePoint': mset([ePoint]), 'moveEnemy': mset([moveEnemy]), 'enemy': mset([enemy]), 'eDirection': mset([eDirection])})
                                    if test <= marking:
                                        sub = Marking({'moveEnemy': mset([moveEnemy]), 'enemy': mset([enemy]), 'eDirection': mset([eDirection])})
                                        add = Marking({'enemy': mset([a]), 'eDirection': mset([b]), 'enemyMoved': mset([c])})
                                        mode = hdict({'ePoint': ePoint, 'moveEnemy': moveEnemy, 'eDirection': eDirection, 'enemy': enemy})
                                        yield event('onMove Enemy', mode, sub, add)

def addsucc_013 (marking, succ):
    "successors of 'onMove Player'"
    if marking('moveVal') and marking('player'):
        for player in marking('player'):
            for moveVal in marking('moveVal'):
                a = updatePositionX(player,moveVal)
                if isinstance(a, tuple):
                    b = 1
                    sub = Marking({'player': mset([player]), 'moveVal': mset([moveVal])})
                    if sub <= marking:
                        add = Marking({'player': mset([a]), 'playerMoved': mset([b])})
                        succ.add(marking - sub + add)

def succ_013 (marking):
    "successors of 'onMove Player'"
    succ = set()
    addsucc_013(marking, succ)
    return succ

def itersucc_013 (marking):
    "successors of 'onMove Player'"
    if marking('moveVal') and marking('player'):
        for player in marking('player'):
            for moveVal in marking('moveVal'):
                a = updatePositionX(player,moveVal)
                if isinstance(a, tuple):
                    b = 1
                    sub = Marking({'player': mset([player]), 'moveVal': mset([moveVal])})
                    if sub <= marking:
                        add = Marking({'player': mset([a]), 'playerMoved': mset([b])})
                        mode = hdict({'player': player, 'moveVal': moveVal})
                        yield event('onMove Player', mode, sub, add)

def addsucc_014 (marking, succ):
    "successors of 'restart game'"
    if marking('jumpForce') and marking('player') and marking('stamina') and marking('killZone') and marking('gameOver') and marking('health') and marking('collisionEnterEnemy') and marking('enemy') and marking('platformB') and marking('canJump') and marking('platformA') and marking('exitPointA') and marking('exitPointB') and marking('ePoint') and marking('score') and marking('eDirection'):
        for gameOver in marking('gameOver'):
            for player in marking('player'):
                for platformA in marking('platformA'):
                    for platformB in marking('platformB'):
                        for enemy in marking('enemy'):
                            for ePoint in marking('ePoint'):
                                for eDirection in marking('eDirection'):
                                    for jumpForce in marking('jumpForce'):
                                        for stamina in marking('stamina'):
                                            for health in marking('health'):
                                                for score in marking('score'):
                                                    for exitPointA in marking('exitPointA'):
                                                        for exitPointB in marking('exitPointB'):
                                                            for killZone in marking('killZone'):
                                                                for collisionEnterEnemy in marking('collisionEnterEnemy'):
                                                                    for canJump in marking('canJump'):
                                                                        a = 1
                                                                        if isinstance(a, int):
                                                                            sub = Marking({'gameOver': mset([gameOver]), 'player': mset([player]), 'platformA': mset([platformA]), 'platformB': mset([platformB]), 'enemy': mset([enemy]), 'ePoint': mset([ePoint]), 'eDirection': mset([eDirection]), 'jumpForce': mset([jumpForce]), 'stamina': mset([stamina]), 'health': mset([health]), 'score': mset([score]), 'exitPointA': mset([exitPointA]), 'exitPointB': mset([exitPointB]), 'killZone': mset([killZone]), 'collisionEnterEnemy': mset([collisionEnterEnemy]), 'canJump': mset([canJump])})
                                                                            if sub <= marking:
                                                                                add = Marking({'startGame': mset([a])})
                                                                                succ.add(marking - sub + add)

def succ_014 (marking):
    "successors of 'restart game'"
    succ = set()
    addsucc_014(marking, succ)
    return succ

def itersucc_014 (marking):
    "successors of 'restart game'"
    if marking('gameOver'):
        for gameOver in marking('gameOver'):
            a = 1
            if isinstance(a, int):
                sub = Marking({'gameOver': mset([gameOver])})
                if sub <= marking:
                    add = Marking({'startGame': mset([a])})
                    mode = hdict({'gameOver': gameOver})
                    yield event('restart game', mode, sub, add)

def addsucc_015 (marking, succ):
    "successors of 'right'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = 1
            sub = Marking({'movePlayer': mset([movePlayer])})
            if sub <= marking:
                add = Marking({'moveVal': mset([a])})
                succ.add(marking - sub + add)

def succ_015 (marking):
    "successors of 'right'"
    succ = set()
    addsucc_015(marking, succ)
    return succ

def itersucc_015 (marking):
    "successors of 'right'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = 1
            sub = Marking({'movePlayer': mset([movePlayer])})
            if sub <= marking:
                add = Marking({'moveVal': mset([a])})
                mode = hdict({'movePlayer': movePlayer})
                yield event('right', mode, sub, add)

def addsucc_016 (marking, succ):
    "successors of 'space not pressed'"
    if marking('jump'):
        for jump in marking('jump'):
            a = 1
            sub = Marking({'jump': mset([jump])})
            if sub <= marking:
                add = Marking({'spaceChecked': mset([a])})
                succ.add(marking - sub + add)

def succ_016 (marking):
    "successors of 'space not pressed'"
    succ = set()
    addsucc_016(marking, succ)
    return succ

def itersucc_016 (marking):
    "successors of 'space not pressed'"
    if marking('jump'):
        for jump in marking('jump'):
            a = 1
            sub = Marking({'jump': mset([jump])})
            if sub <= marking:
                add = Marking({'spaceChecked': mset([a])})
                mode = hdict({'jump': jump})
                yield event('space not pressed', mode, sub, add)

def addsucc_017 (marking, succ):
    "successors of 'space pressed'"
    if marking('jumpForce') and marking('canJump') and marking('jump'):
        for jump in marking('jump'):
            for jumpForce in marking('jumpForce'):
                for canJump in marking('canJump'):
                    a = addJumpForce(jumpForce, canJump)
                    if isinstance(a, float):
                        if isinstance(canJump, bool):
                            b = 1
                            test = Marking({'canJump': mset([canJump]), 'jump': mset([jump]), 'jumpForce': mset([jumpForce])})
                            if test <= marking:
                                sub = Marking({'jump': mset([jump]), 'jumpForce': mset([jumpForce])})
                                add = Marking({'jumpForce': mset([a]), 'spaceChecked': mset([b])})
                                succ.add(marking - sub + add)

def succ_017 (marking):
    "successors of 'space pressed'"
    succ = set()
    addsucc_017(marking, succ)
    return succ

def itersucc_017 (marking):
    "successors of 'space pressed'"
    if marking('jumpForce') and marking('canJump') and marking('jump'):
        for jump in marking('jump'):
            for jumpForce in marking('jumpForce'):
                for canJump in marking('canJump'):
                    a = addJumpForce(jumpForce, canJump)
                    if isinstance(a, int):
                        if isinstance(canJump, bool):
                            b = 1
                            test = Marking({'canJump': mset([canJump]), 'jump': mset([jump]), 'jumpForce': mset([jumpForce])})
                            if test <= marking:
                                sub = Marking({'jump': mset([jump]), 'jumpForce': mset([jumpForce])})
                                add = Marking({'jumpForce': mset([a]), 'spaceChecked': mset([b])})
                                mode = hdict({'canJump': canJump, 'jump': jump, 'jumpForce': jumpForce})
                                yield event('space pressed', mode, sub, add)

def addsucc_018 (marking, succ):
    "successors of 'start'"
    if marking('startGame'):
        for startGame in marking('startGame'):
            a = 1
            b = (0.0,1.0)
            if isinstance(b, tuple):
                c = (-1.0,8.0,0.0)
                if isinstance(c, tuple):
                    d = (10.0,16.0,0.0)
                    if isinstance(d, tuple):
                        e = (4.0,1.0)
                        if isinstance(e, tuple):
                            f = (2.0,6.0)
                            if isinstance(f, tuple):
                                g = -1
                                if isinstance(g, int):
                                    h = 0
                                    if isinstance(h, int):
                                        i = 30
                                        if isinstance(i, int):
                                            j = 5
                                            if isinstance(j, int):
                                                if isinstance(h, int):
                                                    k = (12.0,-3.0,5.0)
                                                    if isinstance(k, tuple):
                                                        l = (20.0,-3.0,5.0)
                                                        if isinstance(l, tuple):
                                                            m = (-1.0,16.0,-1.0)
                                                            if isinstance(m, tuple):
                                                                if isinstance(h, int):
                                                                    n = True
                                                                    if isinstance(n, bool):
                                                                        sub = Marking({'startGame': mset([startGame])})
                                                                        if sub <= marking:
                                                                            add = Marking({'gravity': mset([a]), 'player': mset([b]), 'platformA': mset([c]), 'platformB': mset([d]), 'enemy': mset([e]), 'ePoint': mset([f]), 'eDirection': mset([g]), 'jumpForce': mset([h]), 'stamina': mset([i]), 'health': mset([j]), 'score': mset([h]), 'exitPointA': mset([k]), 'exitPointB': mset([l]), 'killZone': mset([m]), 'collisionEnterEnemy': mset([h]), 'canJump': mset([n])})
                                                                            succ.add(marking - sub + add)

def succ_018 (marking):
    "successors of 'start'"
    succ = set()
    addsucc_018(marking, succ)
    return succ

def itersucc_018 (marking):
    "successors of 'start'"
    if marking('startGame'):
        for startGame in marking('startGame'):
            a = 1
            b = (0.0,1.0)
            if isinstance(b, tuple):
                c = (-1.0,8.0,0.0)
                if isinstance(c, tuple):
                    d = (10.0,16.0,0.0)
                    if isinstance(d, tuple):
                        e = (4.0,1.0)
                        if isinstance(e, tuple):
                            f = (2.0,6.0)
                            if isinstance(f, tuple):
                                g = -1
                                if isinstance(g, bool):
                                    h = 0
                                    if isinstance(h, int):
                                        i = 30
                                        if isinstance(i, int):
                                            j = 5
                                            if isinstance(j, int):
                                                if isinstance(h, int):
                                                    k = (12.0,-3.0,5.0)
                                                    if isinstance(k, tuple):
                                                        l = (20.0,-3.0,5.0)
                                                        if isinstance(l, tuple):
                                                            m = (-1.0,16.0,-1.0)
                                                            if isinstance(m, tuple):
                                                                if isinstance(h, int):
                                                                    n = True
                                                                    if isinstance(n, bool):
                                                                        sub = Marking({'startGame': mset([startGame])})
                                                                        if sub <= marking:
                                                                            add = Marking({'gravity': mset([a]), 'player': mset([b]), 'platformA': mset([c]), 'platformB': mset([d]), 'enemy': mset([e]), 'ePoint': mset([f]), 'eDirection': mset([g]), 'jumpForce': mset([h]), 'stamina': mset([i]), 'health': mset([j]), 'score': mset([h]), 'exitPointA': mset([k]), 'exitPointB': mset([l]), 'killZone': mset([m]), 'collisionEnterEnemy': mset([h]), 'canJump': mset([n])})
                                                                            mode = hdict({'startGame': startGame})
                                                                            yield event('start', mode, sub, add)

def addsucc_019 (marking, succ):
    "successors of 'stay'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = 0
            sub = Marking({'movePlayer': mset([movePlayer])})
            if sub <= marking:
                add = Marking({'moveVal': mset([a])})
                succ.add(marking - sub + add)

def succ_019 (marking):
    "successors of 'stay'"
    succ = set()
    addsucc_019(marking, succ)
    return succ

def itersucc_019 (marking):
    "successors of 'stay'"
    if marking('movePlayer'):
        for movePlayer in marking('movePlayer'):
            a = 0
            sub = Marking({'movePlayer': mset([movePlayer])})
            if sub <= marking:
                add = Marking({'moveVal': mset([a])})
                mode = hdict({'movePlayer': movePlayer})
                yield event('stay', mode, sub, add)

def addsucc_020 (marking, succ):
    "successors of 'update'"
    if marking('enemyMoved') and marking('playerMoved'):
        for playerMoved in marking('playerMoved'):
            for enemyMoved in marking('enemyMoved'):
                a = 1
                sub = Marking({'playerMoved': mset([playerMoved]), 'enemyMoved': mset([enemyMoved])})
                if sub <= marking:
                    add = Marking({'jump': mset([a]), 'superJump': mset([a])})
                    succ.add(marking - sub + add)

def succ_020 (marking):
    "successors of 'update'"
    succ = set()
    addsucc_020(marking, succ)
    return succ

def itersucc_020 (marking):
    "successors of 'update'"
    if marking('enemyMoved') and marking('playerMoved'):
        for playerMoved in marking('playerMoved'):
            for enemyMoved in marking('enemyMoved'):
                a = 1
                sub = Marking({'playerMoved': mset([playerMoved]), 'enemyMoved': mset([enemyMoved])})
                if sub <= marking:
                    add = Marking({'jump': mset([a]), 'superJump': mset([a])})
                    mode = hdict({'enemyMoved': enemyMoved, 'playerMoved': playerMoved})
                    yield event('update', mode, sub, add)

def addsucc_021 (marking, succ):
    "successors of 'update player y'"
    if marking('jumpForce') and marking('spaceChecked') and marking('player') and marking('eChecked') and marking('canJump'):
        for player in marking('player'):
            for canJump in marking('canJump'):
                for eChecked in marking('eChecked'):
                    for spaceChecked in marking('spaceChecked'):
                        for jumpForce in marking('jumpForce'):
                            a = updatePlayerY(player, jumpForce)
                            if isinstance(a, tuple):
                                b = onJump(canJump, player, jumpForce)
                                if isinstance(b, bool):
                                    c = 0
                                    if isinstance(c, int):
                                        d = 1
                                        sub = Marking({'player': mset([player]), 'canJump': mset([canJump]), 'eChecked': mset([eChecked]), 'spaceChecked': mset([spaceChecked]), 'jumpForce': mset([jumpForce])})
                                        if sub <= marking:
                                            add = Marking({'player': mset([a]), 'canJump': mset([b]), 'jumpForce': mset([c]), 'yUpdated': mset([d])})
                                            succ.add(marking - sub + add)

def succ_021 (marking):
    "successors of 'update player y'"
    succ = set()
    addsucc_021(marking, succ)
    return succ

def itersucc_021 (marking):
    "successors of 'update player y'"
    if marking('jumpForce') and marking('spaceChecked') and marking('player') and marking('eChecked') and marking('canJump'):
        for player in marking('player'):
            for canJump in marking('canJump'):
                for eChecked in marking('eChecked'):
                    for spaceChecked in marking('spaceChecked'):
                        for jumpForce in marking('jumpForce'):
                            a = updatePlayerY(player, jumpForce)
                            if isinstance(a, tuple):
                                b = onJump(canJump, player, jumpForce)
                                if isinstance(b, bool):
                                    c = 0
                                    if isinstance(c, int):
                                        d = 1
                                        sub = Marking({'player': mset([player]), 'canJump': mset([canJump]), 'eChecked': mset([eChecked]), 'spaceChecked': mset([spaceChecked]), 'jumpForce': mset([jumpForce])})
                                        if sub <= marking:
                                            add = Marking({'player': mset([a]), 'canJump': mset([b]), 'jumpForce': mset([c]), 'yUpdated': mset([d])})
                                            mode = hdict({'player': player, 'spaceChecked': spaceChecked, 'canJump': canJump, 'eChecked': eChecked, 'jumpForce': jumpForce})
                                            yield event('update player y', mode, sub, add)

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
                           itersucc_021(marking))

def init ():
    'initial marking'
    return Marking({'startGame': mset([1])})

# map transitions names to successor procs
# '' maps to all-transitions proc
succproc = {'': addsucc,
            'E not pressed': addsucc_001,
            'E pressed': addsucc_002,
            'check collisions': addsucc_003,
            'check gravity': addsucc_004,
            'checkHealth': addsucc_005,
            'fixedUpdate': addsucc_006,
            'left': addsucc_007,
            'onCollision enemy': addsucc_008,
            'onCollision exitPoint': addsucc_009,
            'onCollision killZone': addsucc_010,
            'onCollision platform': addsucc_011,
            'onMove Enemy': addsucc_012,
            'onMove Player': addsucc_013,
            'restart game': addsucc_014,
            'right': addsucc_015,
            'space not pressed': addsucc_016,
            'space pressed': addsucc_017,
            'start': addsucc_018,
            'stay': addsucc_019,
            'update': addsucc_020,
            'update player y': addsucc_021}

# map transitions names to successor funcs
# '' maps to all-transitions func
succfunc = {'': succ,
            'E not pressed': succ_001,
            'E pressed': succ_002,
            'check collisions': succ_003,
            'check gravity': succ_004,
            'checkHealth': succ_005,
            'fixedUpdate': succ_006,
            'left': succ_007,
            'onCollision enemy': succ_008,
            'onCollision exitPoint': succ_009,
            'onCollision killZone': succ_010,
            'onCollision platform': succ_011,
            'onMove Enemy': succ_012,
            'onMove Player': succ_013,
            'restart game': succ_014,
            'right': succ_015,
            'space not pressed': succ_016,
            'space pressed': succ_017,
            'start': succ_018,
            'stay': succ_019,
            'update': succ_020,
            'update player y': succ_021}

# map transitions names to successor iterators
# '' maps to all-transitions iterator
succiter = {'': itersucc,
            'E not pressed': itersucc_001,
            'E pressed': itersucc_002,
            'check collisions': itersucc_003,
            'check gravity': itersucc_004,
            'checkHealth': itersucc_005,
            'fixedUpdate': itersucc_006,
            'left': itersucc_007,
            'onCollision enemy': itersucc_008,
            'onCollision exitPoint': itersucc_009,
            'onCollision killZone': itersucc_010,
            'onCollision platform': itersucc_011,
            'onMove Enemy': itersucc_012,
            'onMove Player': itersucc_013,
            'restart game': itersucc_014,
            'right': itersucc_015,
            'space not pressed': itersucc_016,
            'space pressed': itersucc_017,
            'start': itersucc_018,
            'stay': itersucc_019,
            'update': itersucc_020,
            'update player y': itersucc_021}

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
