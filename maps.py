"""Map file."""
import pygame

from utils import load_image


MAP_FILE = 'gta_street_I_square.png'
MAP_SIZE = [1000, 1000]
LANE_X = [-640, -585, -535, -405, -355, -305]
OUT_OF_BOUNDS_X_LIMITS = [-665, -275]
GRASS_X_LIMITS = [-500, -440]


def initialize():
    global MAP_IMAGE
    MAP_IMAGE = load_image(MAP_FILE, False)


class Map(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = MAP_IMAGE
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self, cam_x, cam_y):
        """Realign the map"""
        self.rect.topleft = self.x - cam_x, self.y - cam_y
