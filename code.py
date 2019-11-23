import board
import displayio

from adafruit_display_shapes.circle import Circle
import time
from pong_helpers import ManualPaddle, AutoBall
from adafruit_pybadger import PyBadger

# width and height variables used to check the edges
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

# FPS setting raise or lower this to make the game faster or slower
FPS = 60

# what fraction of a second to wait in order to achieve FPS setting
FPS_DELAY = 1 / FPS

# Badger object for easy button handling
badger = PyBadger()

# Make the display context
splash = displayio.Group(max_size=10)
board.DISPLAY.show(splash)

# Make a background color fill
color_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
splash.append(bg_sprite)

# holde the time we last updated the game state
last_update_time = 0

# create left paddle
left_paddle = ManualPaddle(5,30,1,0, badger, "select", "down")

# add it to screen group
splash.append(left_paddle.rect)

# create right paddle
right_paddle = ManualPaddle(5,30,SCREEN_WIDTH-6,SCREEN_HEIGHT-30-6, badger, "start", "b")

# add it to screen group
splash.append(right_paddle.rect)

# create ball
ball = AutoBall(3, int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))

# add it to screen group
splash.append(ball.circle)

# variable to hold current time
now = 0

# debug variable to count loops inbetween updates
loops_since_update = 0

# update() function will get called from main loop
# hopefully at correct speed to match FPS setting
def update():
    #print("inside update

    # call update on all objects
    left_paddle.update()
    right_paddle.update()
    ball.update(left_paddle, right_paddle)


while True:
    # update time variable
    now = time.monotonic()

    # check if the delay time has passed since the last game update
    if last_update_time + FPS_DELAY <= now:
        #print("%s - %s" % ((last_loop_time + FPS_DELAY), now))

        # call update
        update()

        # set the last update time to now
        last_update_time = now

        #print(loops_since_update)
        # reset debug loop counter
        loops_since_update = 0
    else:
        # update debug loop counter
        loops_since_update += 1