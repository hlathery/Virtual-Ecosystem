import pygame.freetype

class Error:
    def __init__(self, msg):
        self.font = pygame.freetype.Font("Comic Sans MS", 30)
        self.msg = msg

    def display(self, x, y):
        self.font.render_to(self.game.screen, (x, y), self.msg, (255,0,0), (0,0,0))