import pygame
import pygame.freetype
import Util
import Error

class Building(pygame.sprite.Sprite):
    def __init__(self, game, spritesheet, num_workers=0, res=0):
        self.game = game
        self._layer = Util.BUILDING_LAYER
        self.groups = self.game.all_sprites, self.game.buildings
        self.width = Util.TILESIZE
        self.height = Util.TILESIZE
        self.image = spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.res = res
        self.num_workers = num_workers
        self.workers = []
        self.placing = True

    def place(self, x, y, resources):
        if self.res > resources:
            Error.Error("Can't Build Building: Insufficient Resources").display(x,y)
        else:
            self.x = x
            self.y = y
            self.placing = False

    def destroy(self):
        if self.num_workers == 0:
            Error.Error("Can't Destroy Building: Must Be At Least One Person Per Job/Building").display(self.x,self.y)
        else:
            self.kill()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.placing:
            self.rect.move_ip(5, 10)

    def options(self):
        return