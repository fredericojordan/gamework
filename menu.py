"""Menu and game description."""
from loader import load_image
import pygame
from pygame.locals import *


BOUND_MIN = 0
BOUND_MAX = 1000 * 10
NOTE_HALF_X = 211
NOTE_HALF_Y = 242


class Alert(pygame.sprite.Sprite):
    """Alert box."""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('menu.png')
        self.rect = self.image.get_rect()
        self.x =  int(pygame.display.Info().current_w /2) - NOTE_HALF_X
        self.y =  int(pygame.display.Info().current_h /2) - NOTE_HALF_Y
        self.rect.topleft = self.x, self.y
        self.visibility = True
