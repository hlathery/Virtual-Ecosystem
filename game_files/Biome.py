import pygame
import Util

class Biome(pygame.sprite.Sprite):
    def __init__(self, game, spritesheet_set, type):
        self.game = game
        self._layer = Util.GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.tiles
        self.width = Util.TILESIZE
        self.height = Util.TILESIZE
        self.spritesheet_set = spritesheet_set
        self.image = spritesheet_set[0].get_sprite(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.type = type
        self.nourishment = 100
        self.neighbors = []

    def update(self, x, y):
        if self.type == "Dry":
            for tile in self.neighbors:
                if tile.type != "Dry" and tile.nourishment < 50:
                    tile.type = "Dry"
                elif tile.nourishment < 15:
                    tile.type = "Barren"

    def change_state(self, spritesheet):
        if self.nourishment < 75:
            self.image = self.spritesheet_set[1].get_sprite(0,0,self.width,self.height)
            self.rect = self.image.get_rect()

