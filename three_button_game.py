# three_button_game.py

import pyxel
from random import choice
from threading import Timer

WINDOW_WIDTH = 192
WINDOW_HEIGHT = 108

LEFT_RECT_POS = 0
MIDDLE_RECT_POS = WINDOW_WIDTH // 3
RIGHT_RECT_POS = MIDDLE_RECT_POS * 2
RECT_WIDTH = WINDOW_WIDTH // 3
RECT_HEIGHT = WINDOW_HEIGHT

CHOICES = ("left", "middle", "right")
MODES = ("title", "instructions", "play", "gameover")

class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Three Button Game", fps=60, quit_key=pyxel.KEY_NONE)
        self.mode = "title"                 # starts showing title screen
        self.timer = Timer(2.0, None)           
        self.interval = 2.0                 # how long the game waits for correct button push
        self.which_rect = choice(CHOICES)   # pick first rectangle position
        self.score = 0
        self.lives = 5
        self.normal_color = 6
        self.bad_color = 8
        self.current_color = self.normal_color
        self.pause = False
        pyxel.run(self.update, self.draw)
    

    def new_choice(self):
        """Chooses a new rectange (different from the current one) and resets the timer."""
        if self.which_rect == "left":
            self.which_rect = choice(("middle", "right"))
        elif self.which_rect == "middle":
            self.which_rect = choice(("left", "right"))
        elif self.which_rect == "right":
            self.which_rect = choice(("left", "middle"))
        else:
            self.which_rect = choice(CHOICES)
        # if the player failed with the last rectangle, current_color will be bad_color and 
        # pause will be True
        self.current_color = self.normal_color
        self.pause = False

        # shorten the interval and reset the timer
        self.interval = self.interval * 0.99
        # if the timer runs out, the result is the same a pressing the wrong button
        # so, we use the same method as for a bad key press
        self.timer = Timer(self.interval, self.bad_press) 
        self.timer.start()

    
    def change_mode_to_play(self):
        """Sets all variables for a new game."""
        self.mode = "play"
        self.score = 0
        self.lives = 5
        self.pause = False
        self.interval = 2.0
        self.new_choice()
    

    def good_press(self):
        """Increase score, cancel timer and get the next rectangle."""
        self.score = self.score + 1
        self.timer.cancel()
        self.new_choice()
    

    def bad_press(self):
        """Decrease lives, check if lives are all gone, if yes, go to gameover mode, 
        else get next rectangle after a short pause during which the rectanlge displays 
        as bad_color."""
        self.lives = self.lives - 1
        self.timer.cancel()
        self.pause = True
        self.current_color = self.bad_color
        if self.lives == 0:
            self.mode = "gameover"
        else:
            self.timer = Timer(1.0, self.new_choice)
            self.timer.start()


    def update(self):
        """Reacts to button presses based on what self.mode the game is in."""
        if self.mode == "title":
            if pyxel.btnp(pyxel.KEY_I):
                self.mode = "instructions"
            if pyxel.btnp(pyxel.KEY_X):
                self.change_mode_to_play()
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
        
        elif self.mode == "instructions":
            if pyxel.btnp(pyxel.KEY_T):
                self.mode = "title"
            if pyxel.btnp(pyxel.KEY_X):
                self.change_mode_to_play()
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
        
        elif self.mode == "play":
            # get key press, if it is correct key, call self.good_press, else
            # call self.bad_press
            if not self.pause:
                if pyxel.btnp(pyxel.KEY_G):
                    self.mode = "gameover"
                elif pyxel.btnp(pyxel.KEY_Z):
                    if self.which_rect == "left":
                        self.good_press()
                    else:
                        self.bad_press()
                elif pyxel.btnp(pyxel.KEY_X):
                    if self.which_rect == "middle":
                        self.good_press()
                    else:
                        self.bad_press()
                elif pyxel.btnp(pyxel.KEY_C):
                    if self.which_rect == "right":
                        self.good_press()
                    else:
                        self.bad_press()

            
        elif self.mode == "gameover":
            #print(self.score)
            self.timer.cancel()
            if pyxel.btnp(pyxel.KEY_X):
                self.change_mode_to_play()
            if pyxel.btnp(pyxel.KEY_I):
                self.mode = "instructions"
            if pyxel.btnp(pyxel.KEY_T):
                self.mode = "title"
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
    
    
    def draw(self):
        """Clears screen and draws appropriate content on screen based on self_mode."""
        pyxel.cls(1)
        #pyxel.text(150, 0, str(pyxel.frame_count), 9)
        if self.mode == "title":
            pyxel.text(2, 5,  "33    BB  U U TTT TTT  O  NN     GG  A  M M EEE", 8)
            pyxel.text(2, 10, "  3   B B U U  T   T  O O N N   G   A A MMM E", 9)
            pyxel.text(2, 15, "33    BB  U U  T   T  O O N N   GGG AAA MMM EE", 10)
            pyxel.text(2, 20, "  3   B B U U  T   T  O O N N   G G A A M M E", 11)
            pyxel.text(2, 25, "33    BB   UU  T   T   O  N N    GG A A M M EEE", 12)
            pyxel.text(56, 60, "'I' for instructions", 14)
            pyxel.text(74, 48, "'X' to play", 6)
            pyxel.text(74, 72, "'Q' to quit", 13)
            pyxel.text(36, 102, "3 Button Game by Eric Shumaker", 15)

        elif self.mode == "instructions":
            pyxel.text(74, 0,  "HOW TO PLAY", 9)
            pyxel.text(4, 12, "When the screen lights up light blue on the", 7)
            pyxel.text(12, 18,"left, press the 'Z' key.", 7)
            pyxel.text(4, 30, "When the screen lights up light blue in the", 7)
            pyxel.text(12, 36,"middle, press the 'X' key.", 7)
            pyxel.text(4, 48, "When the screen lights up light blue on the", 7)
            pyxel.text(12, 54,"right, press the 'C' key.", 7)
            pyxel.text(4, 66, "If you press the right key fast enough, you", 7)
            pyxel.text(12, 72,"get 1 point.", 7)            
            pyxel.text(4, 84, "If you press the wrong key, or are too slow,", 7)
            pyxel.text(12, 90,"you lose a 'life.' You have 5 'lives'.", 7)
            pyxel.text(4, 102,"'T' for Title Screen, 'X' to play, 'Q' to quit", 9)

        elif self.mode == "play":
            if self.which_rect == "left":
                pyxel.rect(LEFT_RECT_POS, 0, RECT_WIDTH, RECT_HEIGHT, self.current_color)
            elif self.which_rect == "middle":
                pyxel.rect(MIDDLE_RECT_POS, 0, RECT_WIDTH, RECT_HEIGHT, self.current_color)
            elif self.which_rect == "right":
                pyxel.rect(RIGHT_RECT_POS, 0, RECT_WIDTH, RECT_HEIGHT, self.current_color)
            else:
                pass
            pyxel.text(0, 0, f"SCORE: {str(self.score)}", 9)
            pyxel.text(155, 0, f"LIVES: {str(self.lives)}", 9)
        
        elif self.mode == "gameover":
            #pyxel.text(0, 0, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijkl", 7)
            pyxel.text(24, 10,  " GG  A  M M EEE      O  V V EEE RR ", 12)
            pyxel.text(24, 15,  "G   A A MMM E       O O V V E   R R", 11)
            pyxel.text(24, 20, "GGG AAA MMM EEE     O O V V EEE RRR", 10)
            pyxel.text(24, 25, "G G A A M M E       O O V V E   RR ", 9)
            pyxel.text(24, 30, " GG A A M M EEE      O   V  EEE R R", 8)
            
            pyxel.text(76, 42, f"SCORE: {str(self.score)}", 4)
            pyxel.text(56, 54, "'T' for Title Screen", 9)
            pyxel.text(56, 66, "'I' for Instructions", 9)
            pyxel.text(62, 78, "'X' to play again", 9)
            pyxel.text(74, 90, "'Q' to quit", 9)
            

App()