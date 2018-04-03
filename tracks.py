"""The car will emit tracks."""
import pygame

from utils import load_image, rot_center

LIFETIME = 300
DISPLACEMENT = [3, 20]


def initialize():
    global TRACK_IMAGE
    TRACK_IMAGE = load_image('tracks.png', False)


class Track(pygame.sprite.Sprite):
    """Track sprite class."""
    def __init__(self, car_x, car_y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = rot_center(TRACK_IMAGE, TRACK_IMAGE.get_rect(), angle)
        self.lifetime = LIFETIME
        self.x = car_x  + DISPLACEMENT[0] + int(pygame.display.Info().current_w/2)
        self.y = car_y  + DISPLACEMENT[1] + int(pygame.display.Info().current_h/2)
        self.rect.topleft = self.x, self.y

    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
        self.lifetime = self.lifetime - 1

        if (self.lifetime < 1):
            pygame.sprite.Sprite.kill(self)
