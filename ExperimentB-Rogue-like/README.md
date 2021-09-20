# Rogue-like Game

<div align="center">
	<br>
	<img src="https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentB-Rogue-like/roguelike.PNG?raw=true" width="600">
	<br>
	<em>
	Figure: Rogue-like Game
	</em>
</div>
<br/>

One of the very popular Unity full games that is [freely available for developers in the Unity Asset Store is called 2D rogue-like game](https://assetstore.unity.com/packages/templates/tutorials/2d-roguelike-29825), which is a 2D turn-based game with an 8x8 grid including start and exit points. The player starts at the starting point of the first level and he has to avoid enemies and collect foods and drinks to keep his food points high and survive going through the levels. The player can win a level by going to the exit point of that level. The exit and start points have predefined positions that are fixed for all levels. Each level is procedurally generated, where level's grid tiles are randomly generated in each level, specifically tiles that contain enemy, breakable wall, food, and drink. The player can move one step at a time in the main four directions, up, down, right and left. The player's food points decrease by one point every time the player moves one step, and it decreases by five points when he tries to break a breakable wall. Moreover, an enemy can move after the player's move ends. When the player is close to an enemy (i.e. in the next tile, either up, down, right, or left) and the enemy attacks the player, 20 points are deducted from player's food points. If the food points are less than or equals zero, the player looses, and he goes back to the first level. 

We considered testing this game due to the non deterministic behavior it has, where levels are procedurally generated, which makes it challenging for RA to find and reach bugs since levels are changing randomly. It is also challenging for BSGA to generate feasible buggy states that can be reached. The colored Petri nets model of this game consists of 30 places and 19 transitions. Moreover, for this game we defined 6 game rules, which were created using our scheme.

The game consists of several game objects that are described as follows:
* Player : a game object that is controlled by the player. The player can move, break breakable walls, and collect food and drink items. The player dies when his food points are less than or equal zero.
* Enemy : a game object that follows the player and tries to prevent him from winning the game and going through exit point. The enemy has his own behavior that allows him to move. If the enemy is in one of the neighbouring tiles of the player and the current round is enemy's round, the enemy attacks the player and he removes 20 points from player's food points. At the beginning of each level in the game, the game randomly places the enemy at one of the tiles between (1,7) in both x and y axes, where the selected tile is not occupied by other game object.
* Breakable walls : a game object that is placed by the game randomly at the beginning of each level at in one of the tiles between (1,7) in both x and y axes, where the selected tile is not occupied by other game object. This wall acts as an obstacle, where it prevents any game object from going though it. However, if the player tries to go through it, he removes one of its health points which are assigned randomly to it at the beginning of each level, which can be between (1,3). When the health points of the breakable wall are equal to zero, the wall gets destroyed.
* Collectibles : there are two collectibles in this game which are food and drink. Both are spawned randomly at the beginning of each level in positions between (1,7) in both x and y axes, where the selected position is not occupied by other game object. The drink increases player's food points by 20 points, whereas the food increases the food points by 10 points.
* Exit point: the objective of the game is that the player has to go to the exit point in each level to be able to proceed through levels.


Note: Petri nets model creation code that was implemented by the authors of this repository and which was used in the experiments can be found in the following [link](https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentB-Rogue-like/RogueLike_CPN.py).

## Game Rules
The following set of requirements and rules were manually created by the authors to serve the purpose of the study, where rules were constructed using the proposed CPN-MCL rules scheme.

|Index | Requirement | Rule |
|:----:|:-----------:|:----:|
|0| Player shall lose if FoodPoints are less than or equals 0 |  (@gameOver == True and @playerFoodPoints <= 0) or (@gameOver == False and @playerFoodPoints > 0)    |
|1| Player shall go to the next level if he collides with exit| (@reachedExit == 1 and @playerPos_0 == #exitPos_0 and @playerPos_1 == #exitPos_1) |
|2| Next level shall be loaded only when the game is not over | (@reachedExit == 1 and @gameOver == False) or ( (not (@reachedExit == 1)) and @gameOver == True)     |
|3| enemy shall not be able to move on top of the exit point  | (not (@enemy1Pos_0 == #exitPos_0 and @enemy1Pos_1 == #exitPos_1))      |
|4| Player and enemy shall not have similar (x,y) point       | (not (@playerPos_0 == @enemy1Pos_0 and @playerPos_1 == @enemy1Pos_1))     |
|5| Player shall not exceed level bounds            | (@playerPos_0 >= #boardBounds_0 and @playerPos_0 <= #boardBounds_1 and @playerPos_1 >= #boardBounds_2 and @playerPos_1 <= #boardBounds_3)     |

## Experiments

### Experiment B: BSGA and RA
An experiment of two sub experiments that is applied to rogue-like game to check finding bugs using our approach (BSGA-RA). The two sub experiments focus on finding bugs, and also checking the effects of mutation rate on BSGA. Each sub experiment was conducted ten times.

## Places Ranges
|       Place      |           Value Ranges           |
|:----------------:|:--------------------------------:|
|     enemy1Pos    | x: [-2.0, 10.0], y: [-2.0, 10.0] |
|     playerPos    | x: [-2.0, 10.0], y: [-2.0, 10.0] |
| playerFoodPoints |          [-20.0, 100.0]          |
|    reachedExit   |              [0, 1]              |


## Examples of Found Bugs
The following is an example of a found bug by our approach. The test scenarios of those bugs were applied on the game manually by the authors.

### Conflicting Overlapping Goal States - Winning and Losing at The Same Time
This bug violates Rule 2, where the player wins the game win colliding with the exit and loses because the food points reached 0.
![alt text](https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentB-Rogue-like/roguelile_winloseconflict.gif)
