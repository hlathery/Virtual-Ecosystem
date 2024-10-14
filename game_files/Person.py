import pygame
import Util

class Person(pygame.sprite.Sprite):
    def __init__(self, game, job = None):
        self.game = game
        self.job = job
        self.hunted = False
        self.nourishment = 100