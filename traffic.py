"""Traffic module."""
import math
import pygame
from random import choice, randint

import maps
from utils import load_image, rot_center


cars = []
car_files = ['player_2.png', 'player_3.png',
             'player_4.png', 'player_5.png']

CRASH_DECELERATION = 0.05
MIN_SPEED = 0.2
DISPLACEMENT = 955
MIN_Y = 200
MAX_Y = 30000


def initialize():
    """Initialize cars."""
    for index in range(0, len(car_files)):
        cars.append(load_image(car_files[index], True))


class Traffic(pygame.sprite.Sprite):
    """Traffic sprite and AI controller."""

    def get_initial_position(self):
        x = choice(maps.LANE_X) + DISPLACEMENT
        y = -randint(MIN_Y, MAX_Y)
        return x, y

    def rotate(self):
        """Rotate the image."""
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)


    def __init__(self):
        """Initialize the object."""
        pygame.sprite.Sprite.__init__(self)
        self.image = choice(cars) 
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.x, self.y = self.get_initial_position()
        self.rect.topleft = self.x, self.y
        self.dir = 0
        self.rotate()
        self.speed = randint(60, 240) / 100
        self.crashed = False
        
    def impact(self, direction, speed):
        """Push back on impact"""
        self.crashed = True
        self.dir = direction
        self.speed = 0.8*speed
        
    def update_speed(self):
        if self.crashed and self.speed > 0:
            self.speed -= CRASH_DECELERATION*self.speed
            if self.speed < MIN_SPEED:
                self.speed = 0

    def update(self, cam_x, cam_y):
        """Update the position.
        update direction of traffic based on current tile
        """
        self.update_speed()
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))

        self.rect.topleft = self.x - cam_x, self.y - cam_y
