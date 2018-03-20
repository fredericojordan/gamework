"""Alert shown when the car is outside the map."""
from utils import load_image
import pygame
from pygame.locals import *


BOUND_MIN = 0
BOUND_MAX = 1000 * 10
NOTE_HALF_X = 211
NOTE_HALF_Y = 112


def breaking(car_x, car_y):
    """check the bounds vs car coordinates."""
    if car_x < BOUND_MIN or car_x > BOUND_MAX:
       return True
    if (car_y < BOUND_MIN or car_y > BOUND_MAX):
        return True
    return False


class Alert(pygame.sprite.Sprite):
    """alertbox."""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('bounds.png')
        self.rect = self.image.get_rect()
        self.x =  int(pygame.display.Info().current_w /2) - NOTE_HALF_X
        self.y =  int(pygame.display.Info().current_h /2) - NOTE_HALF_Y
        self.rect.topleft = self.x, self.y
