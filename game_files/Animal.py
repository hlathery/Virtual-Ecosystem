import pygame
import Util

class Animal(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.hunted = False
        self.nourishment = 100

    def hunt(self):
        if self.hunted:
            self.kill()