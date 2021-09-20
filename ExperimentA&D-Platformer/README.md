# Platformer Game

<div align="center">
	<br>
	<img src="https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentA&D-Platformer/platformer.PNG?raw=true">
	<br>
	<em>
	Figure: Platformer Game
	</em>
</div>
<br/>
This game is an [open-source 2D platformer game](https://github.com/MitchellSturba/The-Magic-Hat), where the player can walk, jump, collect items, teleport, and fire fireballs. 
Moreover, the game contains enemies that are spawned at different spawn points each time the game is loaded. 
The goal of the game is to find the hat of the player, which is located somewhere in the game's level.
The locations of collectibles in the game is predefined. However, enemies' positions are randomly selected based on a predefined set of positions that 
the game randomly chooses from when it starts. In addition, each enemy in the game has his own behaviors that are 
executed alone and in parallel with the player's actions. When the player collides with an enemy, one point is 
removed for the player's health. The player dies and the game is over if the player's health is less than or equals zero. 
Two objects could affect player's health negatively, enemies and big damage area (i.e. which acts as lava).

This game is challenging from two aspects, first, the parallel behaviors of enemies and player, and second, 
the random placement of enemies in randomly selected spawn points. The colored Petri nets model of this game 
consists of 110 places and 58 transitions, which reflects the state space it has. Moreover, we established 25 game 
rules for this game using our game rules scheme.

There are several game objects in this game which are described as follows:
* Player : is the main game object in the game that is controlled by the player. This game object can be controlled to walk, jump, run, teleport, shoot fireball, and shoot laser.
  Moreover, the player can interact with other game objects in the game's level, where he can collect items and collectibles. 
  In addition, he has health points which could be affected by colliding with enemy, skeleton, and lava. Although the player can jump, however there is a jump limit of jumping 
  at max twice in sequence. The jump counter is supposed to return to its normal state (2 jumps allowed) if the player is on the ground. The player's health is six points 
  and it should not be less than zero. If it reaches to zero or less the player shall die and the game shall end.
    
* Enemies : there are two enemies in the game that have similar behavior which are skeleton and enemy0. 
  Each enemy in the game acts with his own stand alone behavior. The game spawns an enemy at the beginning of the game in one of the predefined spawn points by 
  randomly selecting a spawn point. An enemy can affect the player's health if both  collide with each other, where one point from player's health is deducted. 
  Thus, as long as they are colliding, one point of health should be removed from the player. In addition, enemies can be killed by the player if the player shoots 
  fireball towards them and it collides with them, where an enemy's health points get deducted. Skeleton has three health points, whereas enemy0 has two health points. 
  If enemy's health points are less than or equals zero, the enemy dies and he becomes inactive. Moreover, an enemy's health can also be affected by laser shot by the player 
  if the enemy touches the laser, which makes his health zero and the laser destroys him making him inactive. Enemies' behavior allows them to walk between two edge points 
  based on the spawn point, where these points are $\pm 2$ points away from the randomly selected spawn point. Enemies wait for two game update loops when they reach one of 
  the edge points before walking towards the other edge point.
    
* Fireball : a game object that gets activated when the player fires fireball and the fireballs count of the player is above zero.
  When fired, the fireball goes into the firing direction, and if it hits one of the enemies, the enemy's health points get affected and the fireball becomes inactive. 
    
* Collectibles : there are various items that can be collected by the player. When the player collides with any one of them, the collectible item gets destroyed, and some 
  positive impact happens to the player. There are several types of them described as follows:
  * Health collectible : a collectible item that increases player's health by one point.
  * Teleport collectible : a collectible item that increases player's teleportation count. 
  * Fireballs collectible : a collectible item that increases player's fireballs count.
  * Laser eyes collectible : a collectible item that enables laser ability for the player.
  * Hat : the main goal of the game is to find and collect the missing hat. Thus, when the player collides with the hat, 
    the player shall win the game, and the level shall end. 
    
* Lava : which is called big damage area in the game. This game object acts as a dangerous area that kills the player when he falls into it.


Note: Petri nets model creation code that was implemented by the authors of this repository and which was used in the experiments can be found in the following [link](https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentA%26D-Platformer/Platformer_CPN.py).

## Game Rules
The following set of requirements and rules were manually created by the authors to serve the purpose of the study, where rules were constructed using the proposed CPN-MCL rules scheme.

|Index| Requirement | Rule |
|:---:|:-----------:|:----:|
|0| The maximum number of jumps shall be 2 and the minimum 0, where 2 is the maximum consquent jumps  | @jumps >= 0 and @jumps <= 2  |
|1| Player shall not be allowed to jump if the jump counter is 2 and player is not on the ground     |  ((@tilesChecked == 2) and (@jumps == 2) and ((@playerPosition_0 >= #mapTXRange_0 and @playerPosition_0 <= #mapTXRange_1) and (@playerPosition_1 >= -1 and @playerPosition_1 <= 1))) or ( (not (@tilesChecked == 2)) and (not (@jumps == 2)) and (@tilesChecked == @jumps) and (not ((@playerPosition_0 >= #mapTXRange_0 and @playerPosition_0 <= #mapTXRange_1) and (@playerPosition_1 >= -1 and @playerPosition_1 <= 1)))) |
|2| An enemy of type enemy0 shall only be located within the map's x range  | (@enemy0Position_0 >= #mapTXRange_0 and @enemy0Position_0 <= #mapTXRange_1) and (@enemy0Position_1 == 1)   |
|3| An enemy of type enemy0 shall only move between two predefined points | ((@enemy0Position_0 >= -7 and @enemy0Position_0 <= -3) or (@enemy0Position_0 >= 3 and @enemy0Position_0 <= 7) or (@enemy0Position_0 >= 9 and @enemy0Position_0 <= 13) or (@enemy0Position_0 >= -15 and @enemy0Position_0 <= -12))|
|4| Player's health shall decrease by 1 point as long as the player is colliding with active enemy0 | ((@enemyChecked == @healthWithEnemy) and (not (@enemy0Position_0 == @playerPosition_0 and @enemy0Position_1 == @playerPosition_1)) and (not (@collisionEnterEnemy >= 1))) or ((@enemyChecked == @healthWithEnemy) and (@enemy0Active == True) and (@enemy0Position_0 == @playerPosition_0 and @enemy0Position_1 == @playerPosition_1) and (@collisionEnterEnemy >= 1)) or ((@enemyChecked == @healthWithEnemy) and (not (@enemy0Active == True)) and (@enemy0Position_0 == @playerPosition_0 and @enemy0Position_1 == @playerPosition_1) and (not (@collisionEnterEnemy >= 1)))|
|5| An enemy of type skeleton shall only be located within the map's x range | (@skeletonPosition_0 >= #mapTXRange_0 and @skeletonPosition_0 <= #mapTXRange_1) and (@skeletonPosition_1 == 1) |
|6| An enemy of type skeleton shall only move between two predefined points | ((@skeletonPosition_0 >= -7 and @skeletonPosition_0 <= -3) or (@skeletonPosition_0 >= 3 and @skeletonPosition_0 <= 7) or (@skeletonPosition_0 >= 9 and @skeletonPosition_0 <= 13) or (@skeletonPosition_0 >= -15 and @skeletonPosition_0 <= -12))|
|7| Player's health shall decrease by 1 point as long as the player is colliding with active skeleton | ((@skeletonChecked == @healthWithSkeleton) and (not (@skeletonPosition_0 == @playerPosition_0 and @skeletonPosition_1 == @playerPosition_1)) and (not (@collisionEnterSkeleton >= 1))) or ((@skeletonChecked == @healthWithSkeleton) and (@skeletonActive == True) and (@skeletonPosition_0 == @playerPosition_0 and @skeletonPosition_1 == @playerPosition_1) and (@collisionEnterSkeleton >= 1)) or ((@skeletonChecked == @healthWithSkeleton) and (not (@skeletonActive == True)) and (@skeletonPosition_0 == @playerPosition_0 and @skeletonPosition_1 == @playerPosition_1) and (not (@collisionEnterSkeleton >= 1))) |
|8| Player's fireball count shall increase if player collides with active fireball potion, and potion shall deactivate after collision| ((not (@fireBallPotionActive == True)) and (@fireBallsChecked == @fireBalls)) or ((not (@playerPosition_0 == #fireballPotionPosition_0 and @playerPosition_1 == #fireballPotionPosition_1)) and (@fireBallPotionActive == True) and (not (@fireBalls > 0)) and (@fireBallsChecked == @fireBalls)) |
|9| Player's laserEyes ability shall get activated if player collides with active laserEyes potion, and potion shall deactivate after collision | ((not (@laserEyesPotionActive == True)) and (@laserEyesChecked == @laserEyes)) or ((not (@playerPosition_0 == #laserEyesPotionPosition_0 and @playerPosition_1 == #laserEyesPotionPosition_1)) and (@laserEyesPotionActive == True) and (@laserEyes == False) and (@laserEyesChecked == @laserEyes))|
|10| Player's health shall increase if player collides with active health potion, and potion shall deactivate after collision | ((not (@playerPosition_0 == #healthPotionPosition_0 and @playerPosition_1 == #healthPotionPosition_1)) and (@healCount >= @healthChecked)) or ((@playerPosition_0 == #healthPotionPosition_0 and @playerPosition_1 == #healthPotionPosition_1) and (@healCount >= @healthChecked) and (not (@healthPotionActive == True)))|
|11| Player's health points shall be between 0 (minimum) and 6 (maximum) | @health >= 0 and @health <= 6 |
|12| Game's system shall show game over screen if player's health is less than or equals 0 | ((not (@health <= 0)) and (not (@showGameoverUI == True)) and (@showGameoverUI == @checkSpace)) or ((@health <= 0) and (@showGameoverUI == True) and (@showGameoverUI == @checkSpace)) |
|13| Player's teleports count shall be between 0 (minimum) and 5 (maximum) | @teleports >= 0 and @teleports <= 5 |
|14| Player's teleports count shall increase if player collides with active teleport potion, and potion shall deactivate after collision | ((not (@teleportPotionActive == True)) and (@teleportChecked == @teleports)) or ((not (@playerPosition_0 == #teleportPotionPosition_0 and @playerPosition_1 == #teleportPotionPosition_1)) and (@teleportPotionActive == True) and (not (@teleports > 0)) and (@teleportChecked == @teleports)) |
|15| Player shall be able to navigate anywhere in the map except tiles' (x,y) points. | not ((@playerPosition_0 > #mapTXRange_0 and @playerPosition_0 < #mapTXRange_1) and (@playerPosition_1 == #mapTBPos_0 or @playerPosition_1 == #mapTBPos_1)) |
|16| Player shall win and game shall stop when the player finds and collides with the hat, where the hat is active and player is not dead (game is not over) | ((not (@playerPosition_0 == #hatPosition_0 and @playerPosition_1 == #hatPosition_1)) and (@hasHat == False) and (@hatChecked == @hasHat))  or ((@playerPosition_0 == #hatPosition_0 and @playerPosition_1 == #hatPosition_1) and (not (@hasHat == False)) and (@hatChecked == @hasHat) and (@health > 0)) |
|17| If player falls into big damage field (lava area), health points shall become 0 | ((@bigDamageChecked == @healthWithDamage) and (@healthWithDamage == 0) and ((@playerPosition_0 >= #bigDamage_0 and @playerPosition_0 <= #bigDamage_1) and (@playerPosition_1 >= #bigDamage_2 and @playerPosition_1 <= #bigDamage_3))) or ((not ((@playerPosition_0 >= #bigDamage_0 and @playerPosition_0 <= #bigDamage_1) and (@playerPosition_1 >= #bigDamage_2 and @playerPosition_1 <= #bigDamage_3))) and (@bigDamageChecked == @healthWithDamage) and (not (@healthWithDamage == 0))) |
|18| An enemy0 is acitve if its health points are more than 0 | ((@enemy0Active == True) and (@enemy0Health > 0)) or ( (not (@enemy0Active == True)) and (not (@enemy0Health > 0))) |
|19| A skeleton is acitve if its health points are more than 0 | ((@skeletonActive == True) and (@skeletonHealth > 0)) or ( (not (@skeletonActive == True)) and (not (@skeletonHealth > 0))) |
|20| Player's laser shall not exceed and go through tiles to the other side | (((@playerPosition_0 >= #mapTXRange_0 and @playerPosition_0 <= #mapTXRange_1) and (@playerPosition_1 > #mapTBPos_0 and @playerPosition_1 < #mapTBPos_1))  and (@laserEyesEndPosition_1 > #mapTBPos_0 and @laserEyesEndPosition_1 < #mapTBPos_1)) or (((@playerPosition_0 >= #mapTXRange_0 and @playerPosition_0 <= #mapTXRange_1) and (@playerPosition_1 < #mapTBPos_0)) and (@laserEyesEndPosition_1 < #mapTBPos_0)) or (((@playerPosition_0 >= #mapTXRange_0 and @playerPosition_0 <= #mapTXRange_1) and (@playerPosition_1 > #mapTBPos_1)) and (@laserEyesEndPosition_1 > #mapTBPos_1)) |
|21| Player's fireballs count shall be more than or equals 0 | @fireBalls >= 0 |
|22| If active fireball collides with tiles it should be set to inactive (get destroyed) | (not (@fireballActive == True)) or ((@fireballActive == True) and (not ((@fireballPosition_1 == #mapTBPos_0 or @fireballPosition_1 == #mapTBPos_1) and (@fireballPosition_0 >= #mapTXRange_0 and @fireballPosition_0 <= #mapTXRange_1)))) |
|23| If active fireball collides with enemy0, fireball shall set to inactive and enemy0 health points shall get decreased | (not (@enemy0Position_0 == @fireballPosition_0 and @enemy0Position_1 == @fireballPosition_1)) or ((@enemy0Position_0 == @fireballPosition_0 and @enemy0Position_1 == @fireballPosition_1) and (not (@fireballActive == True)) and (@fireballChecked == @enemy0Health) ) |
|24| If active fireball collides with skeleton , fireball shall set to inactive and skeleton health points shall get decreased | (not (@skeletonPosition_0 == @fireballPosition_0 and @skeletonPosition_1 == @fireballPosition_1)) or ((@skeletonPosition_0 == @fireballPosition_0 and @skeletonPosition_1 == @fireballPosition_1) and (not (@fireballActive == True)) and (@fireballChecked == @skeletonHealth) ) |



## Experiments
### Experiment A - BSGA and RA
An experiment that consists of two sub experiments using platformer game to check finding bugs using our approach that is a collaboration between BSGA and RA. 
The two sub experiments were conducted ten times each, where the goal of the experiments was not only meant to find bugs, but also to check the influence of mutation rate on BSGA. 

### Experiment D - Random and RA
an experiment that is composed of two sub experiments both applied to platformer game to check finding bugs using a collaboration between an agent the generates 
faulty states randomly (without using GA) and our RA. The first sub experiment uses small ranges of values for the involved places, whereas the second sub experiment 
uses large ranges of values. Each sub experiment was conducted ten times. This experiment is meant to check if there is any difference between using BSGA with RA 
and using random generation with RA.

## Places Ranges Used

### Small Ranges
|          Place         |            Value Ranges           |
|:----------------------:|:---------------------------------:|
|      enemy0Health      |              [-2, 4]              |
|     enemy0Position     | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|   collisionEnterEnemy  |               [0, 5]              |
|     healthWithEnemy    |              [-6, 6]              |
|      enemyChecked      |              [-6, 6]              |
|     skeletonHealth     |              [-2, 4]              |
|    skeletonPosition    | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
| collisionEnterSkeleton |               [0, 5]              |
|   healthWithSkeleton   |              [-6, 6]              |
|     skeletonChecked    |              [-6, 6]              |
|        fireBalls       |              [-2, 2]              |
|     fireballChecked    |              [-2, 4]              |
|  fireballPotionChecked |              [-2, 2]              |
|    fireballPosition    | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|  laserEyesEndPosition  | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|        teleports       |              [-2, 7]              |
|     teleportChecked    |              [-2, 7]              |
|          jumps         |              [-1, 3]              |
|      tilesChecked      |              [-1, 3]              |
|     playerPosition     | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|         health         |              [-6, 6]              |
|        healCount       |              [-6, 6]              |
|      healthChecked     |              [-6, 6]              |
|    bigDamageChecked    |              [-6, 6]              |
|    healthWithDamage    |              [-6, 6]              |

### Large Ranges
|          Place         |            Value Ranges           |
|:----------------------:|:---------------------------------:|
|      enemy0Health      |              [-2, 4]              |
|     enemy0Position     | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|   collisionEnterEnemy  |               [0, 5]              |
|     healthWithEnemy    |           [-1000, 1000]           |
|      enemyChecked      |           [-1000, 1000]           |
|     skeletonHealth     |              [-2, 4]              |
|    skeletonPosition    | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
| collisionEnterSkeleton |               [0, 5]              |
|   healthWithSkeleton   |           [-1000, 1000]           |
|     skeletonChecked    |            [-1000, 1000           |
|        fireBalls       |              [-2, 2]              |
|     fireballChecked    |              [-2, 4]              |
|  fireballPotionChecked |              [-2, 2]              |
|    fireballPosition    | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|  laserEyesEndPosition  | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|        teleports       |              [-2, 7]              |
|     teleportChecked    |              [-2, 7]              |
|          jumps         |              [-1, 3]              |
|      tilesChecked      |              [-1, 3]              |
|     playerPosition     | x: [-16.0, 16.0],  y: [-2.0, 6.0] |
|         health         |           [-1000, 1000]           |
|        healCount       |           [-1000, 1000]           |
|      healthChecked     |           [-1000, 1000]           |
|    bigDamageChecked    |           [-1000, 1000]           |
|    healthWithDamage    |           [-1000, 1000]           |



## Examples of Found Bugs
The following are two examples of found bugs by our approach. The test scenarios of those bugs were applied on the game manually by the authors.

### Jumping Infinitely
This bug violates Rule 1, where the player can jump infinite number of times neglecting the maximum number of consequent jumps while not on the ground.
![alt text](https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentA&D-Platformer/platformer_infiniteJump.gif?raw=true)

### Invalid State / Level Design Issue - Stuck between tiles 
This bug violates Rule 15, where the player gets stuck in the tiles positions when teleporting to the (x,y) coordinates of the tiles.
![alt text](https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentA&D-Platformer/platformer_stuckInTiles.gif?raw=true)

