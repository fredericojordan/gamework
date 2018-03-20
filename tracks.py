"""The car will emit tracks."""
import os, sys, pygame
from pygame.locals import *
from utils import load_image, rot_center

LIFETIME = 300


def initialize():
    """Initialize, load the tracks image."""
    global tracks_img
    tracks_img = load_image('tracks.png', False)


class Track(pygame.sprite.Sprite):
    """Track sprite class."""
    def __init__(self, car_x, car_y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = rot_center(tracks_img, tracks_img.get_rect(), angle)
        self.lifetime = LIFETIME
        self.screen = pygame.display.get_surface()
        self.x = car_x  + 3 
        self.y = car_y  + 20
        self.rect.topleft = self.x, self.y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        self.lifetime = self.lifetime - 1

        if (self.lifetime < 1):
            pygame.sprite.Sprite.kill(self)
