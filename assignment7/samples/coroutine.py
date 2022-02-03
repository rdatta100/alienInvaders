"""
A module to show off a timed animation using coroutines

Making timed animations is messy, because we have to add a lot of
class attributes for all of the loop variables.  A cleaner way is
to do this with coroutines.  Each animation is its own coroutine.

The advantage of the coroutine is that yield allows you to pause
to let the game class draw.  If you do not do that, then your
loop will keep going and you will never get a chance to draw. And
if you do not draw, there is no animation.

Author: Walker M. White (wmw2)
Date:   November 20, 2019
"""

import introcs
import random
import math
from game2d import *
import time
import random


############# CONSTANTS #############
# Window Size
WINDOW_WIDTH  = 512
WINDOW_HEIGHT = 512

# THE ANIMATION SPEED IN SECONDS
ANIMATION_SPEED = 1

############# CONTROLLER CLASS #############
class Animation(GameApp):
    """
    This class is an application to animate an image with the arrow keys

    At each step, the update() method checks for key input
    and moves the image accordingly.

    Attribute view : the view (inherited from GameApp)
    Invariant: view is an instance of GView

    Attribute image: the image to animate
    Invariant: image is a GImage made from a PNG file
    """
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)

    # THE THREE MAIN METHODS
    def start(self):
        """
        Initializes the application, creating new attributes.
        """
        self.image = GImage(x=WINDOW_WIDTH/2,y=WINDOW_HEIGHT/2,source='Walker.png')
        self.image.angle = 0 # Doing this prevents a slow down due to initialization
        self._animator = None

    def update(self,dt):
        """
        Animates the image.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        if not self._animator is None:          # We have something to animate
            try:
                self._animator.send(dt)         # Tell it how far to animate
            except:
                self._animator = None            # Stop animating
        elif self.input.is_key_down('left'):
            self._animator = self._animate_turn('left')
            next(self._animator) # Start up the animator
        elif self.input.is_key_down('right'):
            self._animator = self._animate_turn('right')
            next(self._animator) # Start up the animator
        elif self.input.is_key_down('up'):
            self._animator = self._animate_slide('up')
            next(self._animator) # Start up the animator
        elif self.input.is_key_down('down'):
            self._animator = self._animate_slide('down')
            next(self._animator) # Start up the animator

    def draw(self):
        """
        Draws the image
        """
        self.image.draw(self.view)

    def _animate_turn(self,direction):
        """
        Animates a rotation of the image over ANIMATION_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to rotate.
        Precondition: direction is a string and one of 'left' or 'right'.
        """
        sangle = self.image.angle
        if direction == 'left':
            fangle = sangle+90
        else:
            fangle = sangle-90

        # Degrees per second
        steps = (fangle-sangle)/ANIMATION_SPEED
        animating = True
        while animating:
            # Get the current time
            dt = (yield)
            amount = steps*dt

            # Update the angle
            self.image.angle = self.image.angle+amount

            # If we go to far, clamp and stop animating
            if abs(self.image.angle-sangle) >= 90:
                self.image.angle = fangle
                animating = False

    def _animate_slide(self,direction):
        """
        Animates a  vertical up or down of the image over ANIMATION_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up' or 'down'.
        """
        svert = self.image.y
        if direction == 'up':
            fvert = svert+self.image.height
        else:
            fvert = svert-self.image.height

        # Degrees per second
        steps = (fvert-svert)/ANIMATION_SPEED
        animating = True
        while animating:
            # Get the current time
            dt = (yield)
            amount = steps*dt

            # Update the angle
            self.image.y = self.image.y+amount

            # If we go to far, clamp and stop animating
            if abs(self.image.y-svert) >= self.image.height:
                self.image.y = fvert
                animating = False


# Application Code
if __name__ == '__main__':
    Animation(left=150,width=WINDOW_WIDTH,height=WINDOW_HEIGHT,fps=60.0).run()
