from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
import digitalio
from adafruit_pybadger import PyBadger
import math


class AutoBall:
    def __init__(self, diameter, start_x, start_y, debug=False):
        # Store local variables in our object to access later in other functions
        self.diameter = diameter
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y

        # Create a circle object for the screen
        self.circle = Circle(self.x, self.y, self.diameter, fill=0x00FF00, outline=0xFF00FF)

        # default to moving right
        self.going_right = True

        # up/down movement amount. Default to horizontal only
        self.y_offset = 0

        # Need screen height and width to check for collision with top/bottom and both side edges
        self.SCREEN_HEIGHT = 128
        self.SCREEN_WIDTH = 160


    # function to check for collisions between this ball
    # and the left and right paddle objects that get passed in as parameters
    def check_collisions(self, left_paddle, right_paddle):
        #TODO: figure out if the x/y coordinate of the ball is centered or top left and adjust the collision check accordingly.

        if self.x == left_paddle.x + left_paddle.width and left_paddle.y < self.y < left_paddle.y + left_paddle.height:
            # if we collide with left paddle then check if the paddle was in motion, if so adjust the y_offset.
            if left_paddle.prev_y > left_paddle.y:
                #print("left paddle moving down")
                
                # paddle is moving down on screen
                if self.y_offset > -1:
                    self.y_offset -= 1

            elif left_paddle.prev_y < left_paddle.y:
                #print("left paddle moving up")
                
                # paddle is moving up on screen
                if self.y_offset < 1:
                    self.y_offset += 1
                    
            #change direction to move right
            self.going_right = True
            
            #print("collide left paddle")

        if self.x == right_paddle.x - right_paddle.width and right_paddle.y < self.y < right_paddle.y + right_paddle.height:
            # if we collide with right paddle then then check if the paddle was in motion, if so adjust the y_offset.

            if right_paddle.prev_y > right_paddle.y:
                # paddle is moving down on screen
                if self.y_offset > -1:
                    self.y_offset -= 1

            elif right_paddle.prev_y < right_paddle.y:
                # paddle is moving up on screen
                if self.y_offset < 1:
                    self.y_offset += 1

            #change direction to move left
            self.going_right = False
            
            #print("collide right paddle")

    # you must call update() from inside of main loop and pass the paddle objects
    def update(self, left_paddle, right_paddle):

        # check which horizontal direction we are moving and adjust x coordinate accordingly.
        if self.going_right == True:
            self.x += 1
        else:
            self.x -= 1
        
        # move in y direction by y_offset. This makes the ball move diagonal if y_offset is not 0.
        self.y += self.y_offset


        # check if ball went off left edge
        if self.x <= 0:
            # reset back to center
            self.x = self.start_x
            self.y = self.start_y

        # check if ball went off right edge
        if self.x >= self.SCREEN_WIDTH - self.diameter:
            # reset back to center
            self.x = self.start_x
            self.y = self.start_y
        
        # if we are at the top wall
        if self.y == 0:
            # flip y_offset to opposite side of 0 to change direction
            self.y_offset = self.y_offset * -1
        
        # if we are at the bottom wall
        if self.y == self.SCREEN_HEIGHT - (self.diameter+1)*2:
            # flip y_offset to opposite side of 0 to change direction
            self.y_offset = self.y_offset * -1

        # check for collisions with paddles
        self.check_collisions(left_paddle, right_paddle)

        # copy over x and y coordinates to the circle object so it takes effect on the screen
        self.circle.x = self.x
        self.circle.y = self.y


"""
Pong paddle controlled manually by two buttons specified as strings passed into the constructor.
"""
class ManualPaddle:
    def __init__(self, width, height, start_x, start_y, badger, up_btn_str, down_btn_str, debug=False):
        self.badger = badger

        # Store local variables in our object to access later in other functions
        self.height = height
        self.width = width
        self.x = start_x
        self.y = start_y
        
        # will store previous update y position to determine if paddle is in motion
        self.prev_y = self.y
        
        # will store the int values of the buttons we are interested in for this update frame
        self.up_btn = 0
        self.down_btn = 0
        
        # stores the string representation of the buttons we care about
        self.up_btn_str = up_btn_str
        self.down_btn_str = down_btn_str

        # create a rect object
        self.rect = Rect(self.x, self.y, self.width, self.height, fill=0x0)


        # screen height needed so it knows when to stop moving
        self.SCREEN_HEIGHT = 128

    # this will get called early in each frame to update the button values
    def update_btns(self):
        # build a dictionary with all button values in it.
        button_dict = {
            "select": self.badger.button.select,
            "start": self.badger.button.start,
            "down": self.badger.button.down,
            "up": self.badger.button.up,
            "left": self.badger.button.left,
            "right": self.badger.button.right,
            "a": self.badger.button.a,
            "b": self.badger.button.b,
        }
        # set the two buttons we care about by looking up their values from the dictionary.
        self.up_btn = button_dict[self.up_btn_str]
        self.down_btn = button_dict[self.down_btn_str]

    # You must call update() from inside the main loop of code.py
    def update(self):
        self.update_btns()
        self.prev_y = self.y
        # Check if the up button is pressed, and the ball is not at the top edge
        if self.up_btn > 0 and self.y > 0:
            # move up
            self.y -= 1

        # check if the down button is pressed, and the ball is not at the bottom edge
        if self.down_btn > 0 and self.y < self.SCREEN_HEIGHT - self.height:
            # move down
            self.y += 1

        # copy over x and y from local vars into the rect so it takes effect on the screen
        self.rect.x = self.x
        self.rect.y = self.y