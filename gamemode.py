"""The gamemode is defined in this module."""
import pygame, maps
from pygame.locals import *
from utils import load_image
from random import randint

PENALTY_COOL = 180
FLAG_SCORE = 15
CRASH_PENALTY = -2
HALF_TILE = 500
FULL_TILE = 1000
COUNTDOWN_FULL = 3600
COUNTDOWN_EXTEND = 750


class Finish(pygame.sprite.Sprite):
    """
    This class is used as a single object, which moves around
    and keeps track of player score. It also manages the countdown timer.
    """
    
    def claim_flag(self):
        """The player has collided and should pick the flag."""
        self.score += FLAG_SCORE
        self.timeleft += COUNTDOWN_EXTEND
        if self.timeleft > COUNTDOWN_FULL:
            self.timeleft = COUNTDOWN_FULL
            
    def car_crash(self):
        """The player has crashed into another vehicle, deduct some points."""
        if (self.penalty_cool == 0):
            self.score += CRASH_PENALTY
            self.penalty_cool = PENALTY_COOL
     
    def generate_finish(self):
        """Find an adequate point to spawn flag."""
        x = randint(0,9)
        y = randint(0,9)
        while (maps.map_1[y][x] == 5):
            x = randint(0,9)
            y = randint(0,9)
            
        self.x = x * FULL_TILE + HALF_TILE
        self.y = y * FULL_TILE + HALF_TILE
        self.rect.topleft = self.x, self.y

    def reset(self):
        """Reset the state of the timer, score and respawn the flag."""
        self.timeleft = COUNTDOWN_FULL
        self.score = 0
        self.generate_finish()
        
    def __init__(self):
        """Initialize.. yes."""
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('finish.png', False)
        self.rect = self.image.get_rect()
        self.x = 5
        self.y = 5
        self.penalty_cool = PENALTY_COOL
        self.generate_finish()
        self.rect.topleft = self.x, self.y
        self.score = 0
        self.timeleft = COUNTDOWN_FULL

    def update(self, cam_x, cam_y):
        """Update the timer and reposition the flag by offset."""
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        if (self.penalty_cool > 0):
            self.penalty_cool -= 1
        if (self.timeleft > 0):
            self.timeleft -= 1
