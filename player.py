"""Player module, the car."""
import os, sys, pygame, math, maps
from pygame.locals import *
from random import randint, choice
from utils import load_image, rot_center

GRASS_SPEED = 2
GRASS_GREEN = 75
MIN_COLOR_SUM = 300
CENTER_X = -1
CENTER_Y = -1


def findspawn():
    x = randint(0,9)
    y = randint(0,9)
    while(maps.map_1[y][x] == 5):
            x = randint(0,9)
            y = randint(0,9)
    return x * 1000 + CENTER_X, y * 1000 + CENTER_Y


class Player(pygame.sprite.Sprite):
    """Define car as Player."""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_n = randint(1,5)
        self.image = load_image('player_{}.png'.format(self.image_n))
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        CENTER_X =  int(pygame.display.Info().current_w /2)
        CENTER_Y =  int(pygame.display.Info().current_h /2)
        self.x = CENTER_X
        self.y = CENTER_Y
        self.rect.topleft = self.x, self.y
        self.x, self.y = findspawn()
        self.dir = 0
        self.speed = 0.0
        self.maxspeed = 13
        self.minspeed = -1.85
        self.acceleration = 0.1
        self.deacceleration = 0.1
        self.softening = 0.04
        self.steering = 1.60
        self.tracks = False

    def reset(self):
        """Reset the car."""
        self.x =  int(pygame.display.Info().current_w /2)
        self.y =  int(pygame.display.Info().current_h /2)
        self.speed = 0.0
        self.dir = 0
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)
        self.rect.topleft = self.x, self.y
        self.x, self.y = findspawn()
            
    def emit_tracks(self):
        """Emit tracks.."""
        self.tracks = True
        
    def reset_tracks(self):
        """Don't emit tracks.."""
        self.tracks = False

    def grass(self, rgb):
        """If the car is on grass, decrease speed and emit tracks."""
        color_sum = rgb.r + rgb.g + rgb.b
        if color_sum > MIN_COLOR_SUM:
            if self.speed - self.deacceleration > GRASS_SPEED * 2:
                self.speed = self.speed - self.deacceleration * 2
                self.emit_tracks()

    def impact(self):
        """Push back on impact"""
        if self.speed > 0:
            self.speed = self.minspeed

    def soften(self):
            if self.speed > 0:
                self.speed -= self.softening
            if self.speed < 0:
                self.speed += self.softening

    def accelerate(self):
        """Accelerate the vehicle"""
        if self.speed < self.maxspeed:
            self.speed = self.speed + self.acceleration
            if self.speed < self.maxspeed / 3:
                self.emit_tracks()

    def deaccelerate(self, factor=1):
        """Deaccelerate."""
        if self.speed > 0:
            self.speed = self.speed - self.deacceleration*factor
            self.speed = max(self.speed, 0)
            self.emit_tracks()

    def steerleft(self):
        self.dir = self.dir+self.steering
        if self.dir > 360:
            self.dir = 0
        if (self.speed > self.maxspeed / 2):
            self.emit_tracks()
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

    def steerright(self):
        self.dir = self.dir-self.steering
        if self.dir < 0:
            self.dir = 360
        if (self.speed > self.maxspeed / 2):
            self.emit_tracks()   
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

    def update(self, last_x, last_y):  # FIXME
        self.x = self.x + self.speed * math.cos(math.radians(270-self.dir))
        self.y = self.y + self.speed * math.sin(math.radians(270-self.dir))
        self.reset_tracks()
    
    def change_sprite(self):
        self.image_n = choice([i for i in range(1,5) if not i == self.image_n])
        self.image = load_image('player_{}.png'.format(self.image_n))
        self.image_orig = self.image
        self.image, self.rect = rot_center(self.image_orig, self.rect, self.dir)

    def pull_handbrake(self):
        self.deaccelerate(2)
        self.steering += 0.5
        self.steering = min(self.steering, 5)
                
    def release_handbrake(self):
        self.steering = 1.60