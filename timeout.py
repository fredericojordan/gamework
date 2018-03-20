"""Show a dialog when time is out."""
from loader import load_image
import pygame
from pygame.locals import *


NOTE_HALF_X = 212
NOTE_HALF_Y = 112


class Alert(pygame.sprite.Sprite):
    """Alert body."""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('timeout.png')
        self.rect = self.image.get_rect()
        self.x =  int(pygame.display.Info().current_w /2) - NOTE_HALF_X
        self.y =  int(pygame.display.Info().current_h /2) - NOTE_HALF_Y
        self.rect.topleft = self.x, self.y
