import pygame
import Util

class Plant(pygame.sprite.Sprite):
    def __init__(self, game, spritesheet_full, spritesheet_half):
        self.game = game
        self._layer = Util.PLANT_LAYER
        self.groups = self.game.all_sprites, self.game.plants
        self.healthy_image = spritesheet_full
        self.dying_image = spritesheet_half
        self.width = Util.TILESIZE
        self.height = Util.TILESIZE
        self.image = spritesheet_full.get_sprite(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

        self.nourishment = 100

    def update(self):
        if self.nourishment <= 0:
            self.kill()
        elif self.nourishment <= 50:
            self.image = self.dying_image.get_sprite(0,0,self.width,self.height)
            self.rect = self.image.get_rect()