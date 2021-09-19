# Game Rules

|Index| Requirement | Rule |
|:---:|:-----------:|:----:|
|0| Player's health shall decrease by 1 point as long as the player is colliding with active enemy0 |((@enemyChecked == @health) and (not (@enemy_0 == @player_0 and @enemy_1 == @player_1)) and (not (@collisionEnterEnemy >= 1))) or ((@enemyChecked == @health) and (@enemy_0 == @player_0 and @enemy_1 == @player_1) and (@collisionEnterEnemy >= 1))|
|1| Player position according to y axis has to be between -1 and 4 inclusive |@player_1 <= 4 and @player_1 >= -1|
|2| Player's jump force shall be between 0 and 3 inclusive|@jumpForce >= 0 and @jumpForce <= 3|
|3| If player's stamina is more than or equals 10 and player jumps then jump force will be at max 3, otherwise if stamina is less than 10 then jump foce is going to be 1.5 at max when player jumps|((@stamina >= 10) and (@jumpForce >= 0 and @jumpForce <= 3)) or ((@stamina < 10) and (@jumpForce >= 0 and @jumpForce <= 1.5))|
