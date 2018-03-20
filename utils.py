"""General utility functions"""
import os, sys, pygame
from pygame.locals import *


def load_image(file, transparent = True):
    """Load an image. :)"""
    print("Loading " + file + " ..")
    fullname = os.path.join('media', file)
    image = pygame.image.load(fullname)
    if transparent == True:
        image = image.convert()
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image


def rot_center(image, rect, angle):
        """Rotate an image while keeping it's center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
