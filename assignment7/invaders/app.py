"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Sanjana Kasetti sk2465, Rani Datta, rd447
# 12/9/2021
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py


class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _lastkeys: the number of keys pressed in the last frame
    # Invariant: _lastkeys is an int that is >=0
    #
    # Attribute _scoreText: displays the current score
    # Invariant: _scoreText is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #

    #state = [STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
    # STATE_CONTINUE,STATE_COMPLETE]

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self._lastkeys = 0
        self._scoreText = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the follokwing states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you
        should describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) == int or type(dt) == float

        if (self._state == STATE_NEWWAVE):
            self._newWave(dt)
        elif (self._state == STATE_INACTIVE):
            self._text = GLabel(text = "Press 'S' to Play", font_size = 64,
            x = self.width/2, y = self.height/2, font_name = 'Arcade.ttf')
            self._becomeActive()
        elif (self._state == STATE_ACTIVE):
            self._activeGame(dt)
        elif (self._state == STATE_PAUSED):
            self._pauseGame()
        elif (self._state == STATE_CONTINUE):
            self._continueGame(dt)
        elif (self._state == STATE_COMPLETE):
            self._text = GLabel(text = "Game Over", font_size = 64,
            x = self.width/2, y = self.height/2, font_name = 'Arcade.ttf')
            self._wave = None
        else:
            self._text = None
            self._scoreText = None

    def draw(self):
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
        if(not self._text is None):
            self._text.draw(self.view)
        if(not self._scoreText is None):
            self._scoreText.draw(self.view)
        if(not self._wave is None):
            if(self._state == STATE_ACTIVE):
                self._wave.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _newWave(self,dt):
        '''
        Starts a new wave of aliens

        Parameter dt: The time in seconds since the last call to update.
        Precondition: dt is an int or float
        '''
        self._text = None
        self._wave = Wave()
        self._state = STATE_ACTIVE

    def _activeGame(self,dt):
        '''
        Keeps updating the update in wave and checks whether the round is
        over if:
        1) The ship exploded
        2) The aliens reached the defense line
        3) All of the aliens are dead

        EXTRA CREDIT: After the player kills all the aliens, they are given the
        option to continue and if they press "c" a new wave of aliens is created,
        but the player's lives and score remains the same

        EXTRA CREDIT: Everytime a player kills an alien the player is awarded
        some amount of points. The point value associated with each alien
        increases based on the row they are in so the aliens higher up will be
        valued more than the aliens at the bottom. The player's score is not
        changed when they continue are losing a life

        Parameter dt: The time in seconds since the last call to update.
        Precondition: dt is an int or float
        '''
        if(self._wave != None):
            self._wave.update(self.input, dt)
            self._text = GLabel(text = "Player Lives: " + str(self._wave._getLives()),
            font_size = 50, x = GAME_WIDTH-(GAME_WIDTH - 200), y = GAME_HEIGHT-50,
            font_name = 'Arcade.ttf')
            self._scoreText = GLabel(text = "Score: " + str(self._wave._getScore()),
            font_size = 50, x = GAME_WIDTH-150, y = GAME_HEIGHT-50,
            font_name = 'Arcade.ttf')
            if self._wave._allAlienDead() == True:
                if self._wave._getLives() > 0:
                    score = self._wave._getScore()
                    lives = self._wave._getLives()
                    self._wave = Wave()
                    self._wave._setScore(score)
                    self._wave._setLives(lives)
                    self._state = STATE_PAUSED
                else:
                    self._state = STATE_COMPLETE
            if (self._wave._getPaused()):
                self._state = STATE_PAUSED
            if (self._wave._alienReachDline()):
                self._state = STATE_COMPLETE

    def _pauseGame(self):
        """
        When the game is paused, asks player if s/he wants to continue or ends
        the game based on the amount of lives left

        This is inspired by Walker White's state.py
        """
        if self._wave._getLives() > 0:
            self._text = GLabel(text = "Press 'C' to Continue", font_size = 64,
             x = self.width/2, y = self.height/2, font_name = 'Arcade.ttf')

            curr_keys = self.input.key_count

            change = curr_keys > 0
            change = self.input.is_key_down('c') and self._lastkeys == 0

            if change:
                self._state = STATE_CONTINUE
                self._text = None
            self._lastkeys= curr_keys

        if self._wave._getLives() == 0:
            self._state = STATE_COMPLETE

    def _continueGame(self,dt):
        '''
        Creates a new wave if the aliens reached the defense line, or restarts
        round by setting the state to active

        Parameter dt: The time in seconds since the last call to update.
        Precondition: dt is an int or float
        '''
        self._wave._setPaused(False)
        self._wave._setExplodeState(False)
        x = GAME_WIDTH/2
        y = SHIP_BOTTOM
        width = SHIP_WIDTH
        height = SHIP_HEIGHT
        self._wave._setShip(Ship(x,y,width,height,source='ship-strip.png',frame=0))
        self._state = STATE_ACTIVE

    def _becomeActive(self):
        '''
        Starts the game based on user input

        This is inspired by Walker White's state.py
        '''
        curr_keys = self.input.key_count

        change = curr_keys > 0
        change = self.input.is_key_down('s') and self._lastkeys == 0

        if change:
            self._state = STATE_NEWWAVE
            self._text = None

        self._lastkeys= curr_keys
