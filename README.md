The university project where I with my team implemented alpha-beta pruning and minimax algorithms for zero-sum game. Analyzed them to understand which one works better and in which cases.


The game rules are:

At the beginning of the game, the human player chooses which number between 8 and 18 to start the game with. 

Game Description 

At the beginning of the game, a number chosen by the human player is given. Both players have 0 points. In addition, the game uses a pot of play that is initially 0. Players take turns multiplying the current number by 2, 3, or 4. If the result of multiplication is an even number, then 1 point is subtracted from the player's score, and if the number is odd, then 1 point is added. On the other hand, if a number ending in 0 or 5 is obtained, then 1 point is added to the pot. The game ends when a number greater than or equal to 1200 has just been obtained. The player whose turn the game is over empties the pot by adding his points to his score. The player with the most points wins the game. If the number of points is equal, then the result is a draw. 
