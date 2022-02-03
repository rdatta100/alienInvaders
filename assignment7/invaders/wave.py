"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Sanjana Kasetti sk2465, Rani Datta rd447
# 12/9/2021
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _movetotheright: determines if the alien should move to the right
    # Invariant: _movetotheright is a boolean
    #
    # Attribute _movetotheleft: determines if the alien should move to the left
    # Invariant: _movetotheleft is a boolean
    #
    # Attribute _numstepsuntilfire: randomly generated, stores how many steps an
    # alien can take until it can fire again
    # Invariant: _numstepsuntilfire is an int
    #
    # Attribute _randomalien: alien randomly picked to fire
    # Invariant: _randomalien is an Alien object
    #
    # Attribute _steps: counter variable, until _steps == _numstepsuntilfire,
    # alien cannot fire
    # Invariant: _steps is an int
    #
    # Attribute _animator: determines if the coroutine can run or not based on
    # whether the ship exploded
    # Invariant: _animator is a boolean
    #
    # Attribute _shipExplode: state of ship being exploded or not
    # Invariant: _shipExplode is a boolean
    #
    # Attribute _score: stores the score of the player
    # Invariant: _score is an int
    #
    # Attribute _lives: stores the lives the player has
    # Invariant: _lives is an int
    #
    # Attribute _paused: determines if the game is paused or not
    # Invariant: _paused is a boolean
    #
    # Attribute _shipNoise: stores the sound the ship makes when it explodes
    # Invariant: _shipNoise is a Sound object
    #
    # Attribute _boltNoise: stores the sound the bolts make when the ship fires
    # Invariant: _boltNoise is a Sound object
    #
    # Attribute _alienNoise: stores the sound the bolts make when the alien explodes
    # Invariant: _alienNoise is a Sound object
    #
    # Attribute _alienShoot: stores the sound the bolts make when the alien fires
    # Invariant: _alienShoot is a Sound object
    #

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def _getPaused(self):
        '''
        This returns the self._paused attribute
        '''
        return self._paused

    def _setPaused(self, val):
        '''
        This sets the value of self._paused to val
        '''
        assert type(val) == bool
        self._paused = val

    def _getExplodeState(self):
        '''
        This returns the self._shipExplode attribute
        '''
        return self._shipExplode

    def _setExplodeState(self,boo):
        '''
        This sets the value of self._shipExplode to boo
        '''
        assert type(boo) == bool
        self._shipExplode = boo

    def _getLives(self):
        '''
        This returns the self._lives attribute
        '''
        return self._lives

    def _setLives(self, val):
        '''
        This sets the value of self._lives to val
        '''
        assert type(val) == int
        self._lives = val

    def _getScore(self):
        '''
        This returns the self._score attribute
        '''
        return self._score

    def _setScore(self,val):
        '''
        This sets the value of self._score to val
        '''
        assert type(val) == int
        self._score = val

    def _getShip(self):
        '''
        This returns the self._ship attribute
        '''
        return self._ship

    def _setShip(self, newShip):
        '''
        This sets the value of self._ship to newShip
        '''
        assert isinstance(newShip, Ship)
        self._ship = newShip

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        '''
        Intializes all of the attributes that are listed above

        EXTRA CREDIT: Implemented sound

        '''
        self._aliens = []
        self._createAliens()
        x = GAME_WIDTH/2
        y = SHIP_BOTTOM
        width = SHIP_WIDTH
        height = SHIP_HEIGHT
        self._ship = Ship(x,y,width,height,source = 'ship-strip.png', frame = 0)
        self._dline = GPath(points = [0,DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
        linewidth = 3)
        self._dline.linecolor = 'gray'
        self._time = 0
        self._movetotheright = True
        self._movetotheleft = True
        self._bolts = []
        self._numstepsuntilfire = random.randint(1,BOLT_RATE)
        self._randomalien = 0
        self._steps = 0
        self._animator = None
        self._shipExplode = None
        self._score = 0
        self._lives = SHIP_LIVES
        self._paused = False
        self._shipNoise = Sound('blast3.wav')
        self._boltNoise = Sound('pew1.wav')
        self._alienNoise = Sound('pop1.wav')
        self._alienShoot = Sound('blast2.wav')

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        '''
        Constantly updates the game

        Parameter input: The user input
        Precondition: input is an instance of the GInput
        Parameter dt: The time in seconds since the last call to update.
        Precondition: dt is an int or float
        '''
        assert type(dt) == int or type(dt) == float
        if(self._animator is None):
            self._move(input)
            self._updateAlien(dt)
        self._moveb(input)
        self._makeanddelete()
        self._scollision()
        self._acollision()

        if not self._animator is None:
            try:
                self._animator.send(dt)
            except StopIteration:
                self._animator = None
                self._shipExplode = True
                self._ship = None
                self._bolts = []
                self._paused = True
                self._lives -= 1
        elif (self._getExplodeState()):
            self._animator = self._ship._animate_ship(dt)
            next(self._animator)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        if self._aliens != None:
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[0])):
                    if self._aliens[row][col] != None:
                        index = self._aliens[row][col]
                        index.draw(view)
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)
        if self._bolts != None:
            for row in range(len(self._bolts)):
                index = self._bolts[row]
                index.draw(view)

    # HELPER METHODS
    def _createAliens(self):
        '''
        Creates the 2d list alien object
        '''
        x = ALIEN_H_SEP
        y = GAME_HEIGHT - ALIEN_CEILING
        width = ALIEN_WIDTH
        height = ALIEN_HEIGHT
        images = ALIEN_IMAGES
        index = 0
        for row in range(ALIEN_ROWS):
            x = ALIEN_H_SEP + (width) + ALIEN_H_SEP
            self._aliens.append([])
            for col in range(ALIENS_IN_ROW):
                alien = Alien(x,y,width,height,source=images[(ALIEN_ROWS -index)%3])
                self._aliens[row].append(alien)
                x = ALIEN_H_SEP + width + x

            if(row%2 == 0):
                index = index + 1
            y = y - height - ALIEN_V_SEP

    def _makeanddelete(self):
        '''
        Goes through the bolt and determines whether to delete it or make it
        continue moving based on x and y coordinates and if it is a player bolt
        or not
        '''
        i = 0
        while i < len(self._bolts):
            if(self._bolts[i]._isPlayerBolt()):
                if self._bolts[i].y - (BOLT_HEIGHT/ 2) > GAME_HEIGHT:
                    del self._bolts[i]
                else:
                    y = self._bolts[i].y
                    y += BOLT_SPEED
                    self._bolts[i].y = y
            else:
                if self._bolts[i].y + (BOLT_HEIGHT/ 2)  < 0:
                    del self._bolts[i]
                else:
                    y = self._bolts[i].y
                    y -= BOLT_SPEED
                    self._bolts[i].y = y
            i += 1

    def _move(self,input):
        '''
        Moves the player bolt based on user input
        '''
        if(not self._ship is None):
            x = self._ship.x
            if input.is_key_down('left'):
                if(x > SHIP_WIDTH/2):
                    x -= SHIP_MOVEMENT
                    self._ship.x = x
            if input.is_key_down('right'):
                if(self._ship.x < GAME_WIDTH-SHIP_WIDTH/2):
                    x += SHIP_MOVEMENT
                    self._ship.x = x

    def _updateAlien(self, dt):
        '''
        Decided whether to update alien based on the dt

        Parameter dt: The time in seconds since the last call to update.
        Precondition: dt is an int or float
        '''
        assert type(dt) == int or type(dt) == float

        if(self._time < ALIEN_SPEED):
            self._time += dt
        else:
            if(self._firstAlien() != []):
                self._time = 0
                self._movea(dt)
                self._firealiens()

    def _firstAlien(self):
        '''
        Goes through the entire alien attribute and finds the righmost alien
        that is not None and remove it from our first list that stores aliens
        that are not None
        '''
        first = []
        right = 0
        if (len(self._aliens) > 0):
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    if self._aliens[row][col] != None:
                        first.append(self._aliens[row][col])
        if(len(first)>0):
            for row in range(len(first)):
                if(first[row] is None and len(first) > 0):
                    first.remove(first[row])
        return first

    def _lastAlien(self):
        '''
        Goes through the entire alien attribute and finds the leftmost
        alien that is not None and remove it from our last list that stores aliens
        that are not None
        '''
        last = []
        if (len(self._aliens) > 0):
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    if self._aliens[row][col] != None:
                        lastalien = (self._aliens[row][col])
                        last.append(lastalien)
        if(len(last)>0):
            for row in range(len(last)):
                if(last[row] is None and len(last) > 0):
                    last.remove(last[row])
        return last

    def _movea(self,dt):
        '''
        Moves the aliens based on x and y coordinates

        Parameter dt: The time in seconds since the last call to update.
        Precondition: dt is an int or float
        '''
        if(not self._lastAlien() == []):
            if self._movetotheright:
                if (len(self._aliens) > 0):
                    last = self._firstAlien()
                    if(last[-1].x + ALIEN_H_WALK + ALIEN_WIDTH/2 < GAME_WIDTH):
                        for row in range(len(self._aliens)):
                            for col in range(len(self._aliens[row])):
                                if self._aliens[row][col] != None:
                                    self._aliens[row][col].x += ALIEN_H_WALK
                    else:
                        for row in range(len(self._aliens)):
                            for col in range(len(self._aliens[row])):
                                if self._aliens[row][col] != None:
                                    self._aliens[row][col].y -= ALIEN_V_WALK
                                    self._movetotheright = False
            elif self._movetotheleft:
                if (len(self._aliens) > 0):
                    first = self._lastAlien()
                    if(first[0].x - ALIEN_H_WALK - ALIEN_WIDTH/2 > 0):
                        for row in range(len(self._aliens)):
                            for col in range(len(self._aliens[row])):
                                if self._aliens[row][col] != None:
                                    self._aliens[row][col].x -= ALIEN_H_WALK
                    else:
                        for row in range(len(self._aliens)):
                            for col in range(len(self._aliens[row])):
                                if self._aliens[row][col] != None:
                                    self._aliens[row][col].y -= ALIEN_V_WALK
                                    self._movetotheright = True

    def _moveb(self, input):
        '''
        Moves the bolt based on user input
        '''
        if input.is_key_down('up'):
            if(not self._ship is None):
                if (not self._checkOnePlayerBolt()):
                    x = self._ship.x
                    y = self._ship.y + SHIP_HEIGHT/2
                    width = BOLT_WIDTH
                    height = BOLT_HEIGHT
                    fillcolor = 'red'
                    linecolor = "black"
                    bolt = Bolt(x,y,width,height,fillcolor,linecolor, True)
                    self._bolts.append(bolt)
                    self._boltNoise.play()

    def _checkOnePlayerBolt(self):
        '''
        Checks how many player bolts there are, there should be one at a time
        '''
        count = 0
        for x in range(len(self._bolts)):
            if(self._bolts[x]._isPlayerBolt()):
                count += 1

        if(count == 1):
            return True

        return False

    def _firealiens(self):
        '''
        Determines whether the alien can fire bases on self._numstepsuntilfire
        '''
        if(self._steps == self._numstepsuntilfire):
            self._alientofire()
            self._steps = 0
        else:
            self._steps += 1

    def _alientofire(self):
        '''
        Chooses which alien to fire randomly and after a random amount of steps
        '''
        if (self._steps == self._numstepsuntilfire):
            colsnotNone = []
            for row in range(len(self._aliens)):
                for col in range(len(self._aliens[row])):
                    if(self._aliens[row][col] != None):
                        if(col not in colsnotNone):
                            colsnotNone.append(col)

            col = random.choice(colsnotNone)

            bottom = 0
            for x in range(ALIEN_ROWS):
                if(self._aliens[x][col] != None):
                    bottom = self._aliens[x][col]

            self._randomalien = bottom
            x = bottom.x
            y = bottom.y
            width = BOLT_WIDTH
            height = BOLT_HEIGHT
            fillcolor = 'red'
            linecolor = "black"
            self._bolts.append(Bolt(x,y,width,height,fillcolor,linecolor, False))
            self._numstepsuntilfire = random.randint(1,BOLT_RATE)
            self._alienShoot.play()

    def _findBottomMost(self):
        """
        Finds the bottommost alien
        """
        bottom = 0
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if(not self._aliens[row][col] is None):
                    bottom = self._aliens[row][col]
        return bottom

    # HELPER METHODS FOR COLLISION DETECTION
    def _acollision(self):
        '''
        Goes through the alien object and finds if an alien collided with a
        player bolt
        '''
        score_mult = 0
        temp = None
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if self._aliens[row][col] != None:
                    if len(self._bolts) > 0:
                        for x in range(len(self._bolts)):
                            if self._bolts[x]._isPlayerBolt():
                                 temp = self._bolts[x]
                        if(not temp is None):
                            if self._aliens[row][col]._aliencollides(temp):
                                self._alienNoise.play()
                                self._aliens[row][col] = None
                                if(row % ALIENS_IN_ROW == 0):
                                    score_mult = (ALIENS_IN_ROW) * 10
                                else:
                                    score_mult = (row % ALIENS_IN_ROW) * 10
                                self._score += score_mult
                                self._bolts.remove(temp)

    def _scollision(self):
        '''
        Sees if an alien bolt collided with the ship
        '''
        temp = None
        x = 0
        if(len(self._bolts) > 0):
                if not self._bolts[x]._isPlayerBolt():
                    temp = self._bolts[x]
                    if(not self._ship is None):
                        if(not temp is None):
                            if self._ship._shipcollides(temp):
                                self._shipExplode = True
                                del self._bolts[x]
                                self._shipNoise.play()
                x = 0
        else:
            x += 1

    def _shipDead(self):
        '''
        Checks whether the ship is dead or not, if it is, decrements a life
        '''
        if (self._getExplodeState()):
            self._lives -= 1
            return True

    def _alienReachDline(self):
        '''
        Looks at the bottom most alien and sees if it reached the defense line
        '''
        last = self._findBottomMost()
        if(not type(last) == int):
            if (last.y - ALIEN_HEIGHT/2) < DEFENSE_LINE:
                return True

        return False

    def _allAlienDead(self):
        '''
        Looks throught the alien object and sees if they are all dead
        '''
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if(not self._aliens[row][col] is None):
                    return False

        return True
