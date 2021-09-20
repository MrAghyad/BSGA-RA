# InfiniteRunner Game

<div align="center">
	<br>
	<img src="https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentC-InfiniteRunner/infiniteRunner.PNG?raw=true">
	<br>
	<em>
	Figure: InfiniteRunner Game
	</em>
</div>
<br/>

This game is an [open-source 2D infinite runner game](https://github.com/alexFiorenza/SpaceMan-Game). The goal of the game is to reach the highest possible score by going through an infinite level of regenerated platforms. The player in the game has two abilities which are walking and jumping. In addition, the player is able to perform a super jump by using his stamina points. The player has health points which can be negatively affected when he collides with an enemy. If player's health points are less than or equal to zero the game ends. In addition, if the player falls downwards beyond the platforms' axis level, the game ends. The enemy moves between two predefined points on a certain platform. Every time a platform with an enemy gets regenerated, the enemy gets re-positioned with the platform it belongs to.    

The colored Petri nets model of this game consists of 37 places and 21 transitions. Moreover, for this game we defined 4 game rules, which were created using our scheme.

## Game Rules

|Index| Requirement | Rule |
|:---:|:-----------:|:----:|
|0| Player's health shall decrease by 1 point as long as the player is colliding with active enemy0 |((@enemyChecked == @health) and (not (@enemy_0 == @player_0 and @enemy_1 == @player_1)) and (not (@collisionEnterEnemy >= 1))) or ((@enemyChecked == @health) and (@enemy_0 == @player_0 and @enemy_1 == @player_1) and (@collisionEnterEnemy >= 1))|
|1| Player position according to y axis has to be between -1 and 4 inclusive |@player_1 <= 4 and @player_1 >= -1|
|2| Player's jump force shall be between 0 and 3 inclusive|@jumpForce >= 0 and @jumpForce <= 3|
|3| If player's stamina is more than or equals 10 and player jumps then jump force will be at max 3, otherwise if stamina is less than 10 then jump foce is going to be 1.5 at max when player jumps|((@stamina >= 10) and (@jumpForce >= 0 and @jumpForce <= 3)) or ((@stamina < 10) and (@jumpForce >= 0 and @jumpForce <= 1.5))|

## Places Ranges
|        Place        |           Value Ranges          |
|:-------------------:|:-------------------------------:|
|    enemy0Position   |   x: [4.0,20.0],  y: [0.0,4.0]  |
| collisionEnterEnemy |              [0, 5]             |
|     enemyChecked    |             [-6, 6]             |
|      jumpForce      |              [0,5]              |
|       stamina       |              [0,30]             |
|    playerPosition   | x: [-5.0,20.0],  y: [-2.0, 6.0] |
|        health       |              [-5,5]             |

## Experiments

### Infinite runner Game - Experiment C: BSGA and RA
an experiment that studies applying our approach (BSGA-RA) on infinite runner game to check finding bugs and the ability of breaking rules. This experiment was repeated ten times.


## Examples of Found Bugs
The following is an example of found bugs by our approach. The test scenarios of those bugs were applied on the game manually by the authors.

### Invalid state - jump force exceeds limits
This bug violates Rule 3, where the player can jump very high exceeding the rule limits.
![alt text](https://github.com/MrAghyad/BSGA-RA/blob/main/ExperimentC-InfiniteRunner/infiniterunner_invalidJumpForce.gif?raw=true)
