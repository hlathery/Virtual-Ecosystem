import pygame
import Util

class Person(pygame.sprite.Sprite):
    def __init__(self, game, x, y, job):
        self.game = game
        self._layer = Util.PERSON_LAYER
        self.groups = self.game.all_sprites, self.game.people
        self.width = Util.TILESIZE/2
        self.height = Util.TILESIZE/2
        self.image = spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

        self.hunted = False
        self.nourishment = 100