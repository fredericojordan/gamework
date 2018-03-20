"""Show the player where to find the flag."""
import pygame, math
from pygame.locals import *
from loader import load_image

PI = 3.14

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect


class Tracker(pygame.sprite.Sprite):
    """Guide the player with a giant arrow."""

    def __init__(self, screen_x, screen_y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = load_image('direction.png', False)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect_orig = self.rect
        self.x = screen_x - 150
        self.y = screen_y - 150
        self.rect.topleft = self.x, self.y
        self.dir = 0

    def update(self, point_x, point_y, target_x, target_y):
        """Update the rotation of the arrow."""
        self.dir = (math.atan2(point_y - target_y, target_x - point_x) * 180 / PI)
        self.image, self.rect = rot_center(self.image_orig, self.rect_orig, self.dir)
