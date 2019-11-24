# CircuitPython-Badge-2-Player-Pong-Game

This is a simple example game. It's like the classic 2 player pong. It's meant to be played with the badge held longways by both players one at each end. One player uses the select and down buttons to move their paddle, and the other uses the start and b buttons.

I believe this example should work on the [Adafruit PyBadge](https://www.adafruit.com/product/4200) and [Adafruit PyBadge LC](https://www.adafruit.com/product/3939).

This example has been tested and is known to work on the [Adafruit EdgeBadge](https://www.adafruit.com/product/4400).

The game is broken into two files: 

 - code.py - Contains the main loop, screen setup, and manages high-level game object update function calls.
 - pong_helpsers.py - contains helper objects for the game elements. code.py imports, creates, and calls update() on these objects at the appropriate time. The update() functions that are defined in this file control the behavior of the two types of game elements, paddles and balls. The paddles in this variant of the game are controlled by two buttons each, one for up and one for down. The ball moves automatically. 
 
I have done my best to thoroughly comment both python files. Intention is that these scripts are basic enough for beginners to use to learn about building games with CircuitPython.

If you have additional questions or comments about this project please feel free to open an issue here on github.

# Programming Exersises:
If you are trying to practice programming games with CircuitPython here are a few basic exersises that you could try out by modifying the code in this project:

 - Change the FPS setting in code.py and observe how higher and lower values impact the game play. 
 - Change the code to increment the FPS setting the longer the players are "alive" so the game gets faster (harder) over time like Tetris. Don't forget to reset FPS back to default when one player loses and the ball resets.
 - Manipulate the size of the paddles and/or balls, observe the results. Is the game easier or harder if you make the ball bigger or smaller? Same question for the paddles.
 - Manipulate the speed that the ball moves at by changing how many pixels it moves by during each game update iteration.
 - Manipulate the speed that the paddles move at by changing how many pixels they move during each game update iteration.
 - Allow the player to speed up and slow down the horizontal movement of the ball with the left and right buttons on the d-pad.
 - Make a list of colors, change the color of the ball each time it collides with a paddle.
 - Change the behavior of ball colliding with paddle in motion to allow for a steeper angle.

