# Game Rules

|Index | Requirement | Rule |
|:----:|:-----------:|:----:|
|0| Player shall lose if FoodPoints are less than or equals 0 |  (@gameOver == True and @playerFoodPoints <= 0) or (@gameOver == False and @playerFoodPoints > 0)    |
|1| Player shall go to the next level if he collides with exit| (@reachedExit == 1 and @playerPos_0 == #exitPos_0 and @playerPos_1 == #exitPos_1) |
|2| Next level shall be loaded only when the game is not over | (@reachedExit == 1 and @gameOver == False) or ( (not (@reachedExit == 1)) and @gameOver == True)     |
|3| enemy shall not be able to move on top of the exit point  | (not (@enemy1Pos_0 == #exitPos_0 and @enemy1Pos_1 == #exitPos_1))      |
|4| Player and enemy shall not have similar (x,y) point       | (not (@playerPos_0 == @enemy1Pos_0 and @playerPos_1 == @enemy1Pos_1))     |
|5| Player shall not exceed level bounds            | (@playerPos_0 >= #boardBounds_0 and @playerPos_0 <= #boardBounds_1 and @playerPos_1 >= #boardBounds_2 and @playerPos_1 <= #boardBounds_3)     |
