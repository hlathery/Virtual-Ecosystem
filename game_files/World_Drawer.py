import pygame
from Util import *
import time
import threading
import requests
import json

class WorldDrawer:

    def __init__(self, height_map):
        # open window
        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # load tile sheet, and extract the cell images
        self.tilesheet = pygame.image.load(TILESHEET_PATH)

        self.height_map = height_map
        self.font = pygame.font.SysFont(None, 20)
        self.get_headers = {"accept": "application/json", "access_token": "hlath"}
        self.post_headers = {"accept": "application/json", "access_token": "hlath", "Content-Type": "application/json"}
        self.building_types = ["House", "Farm", "Hunter/Forager", "Mine", "Lumber Mill"]
        self.wood = 100
        self.buildings = {"Houses":0, "Farms":0, "Hunter/Forager Huts":0, "Mines":0, "Lumber Mills":0}
        self.menu_options = ["Catalog", "Village Info", "Assignments", "Eco Info"]
        self.eco = {"Water Bodies":0, "Forests":0, "Grass":0, "Desert":0}

        if __name__ == "__main__":
            # Start FastAPI in a separate thread
            fastapi_thread = threading.Thread(target=self.run_fastapi)
            fastapi_thread.start()

        # get images for all tiles for every terrain type
        self.terrain_tiles = []
        for terrain_type in ALL_TERRAIN_TYPES:
            tile_types = []
            for tile_pos in TERRAIN_TILES[terrain_type]:
                tile_types.append(self.tilesheet.subsurface((tile_pos[0], tile_pos[1], TILESIZE, TILESIZE)))
            self.terrain_tiles.append(tile_types)

    def run_fastapi():
        import main

    def draw(self):
        while True:
            self.draw_tiles(self.height_map)
            pygame.display.flip()
            self.decisions()
            self.draw_tiles(self.height_map)
            pygame.display.flip()
            self.cont()
            c, m = self.wait_key()

    def wait_key(self, click=False, menu=True):
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            return click, menu

    def draw_text(self, text, color, x, y):
        textobj = self.font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        self.display_surface.blit(textobj, textrect)

    def decisions(self):
        menu = True
        click = False
        x = 600
        y = 250
        option = "Catalog"
        job_list = requests.get("http://127.0.0.1:3000/assignments/", headers=self.get_headers).json()
        while menu:
            menu = pygame.Rect(x, y, 400, 600)
            pygame.draw.rect(self.display_surface, (0,0,0), menu)
            self.draw_text("DECISION MENU", (255,255,255), x+150, y)

            c = 0
            header =[]
            for b in self.menu_options:
                button = pygame.Rect(x+c, y+15, 100, 20)
                header.append(button)
                if option == b:
                    pygame.draw.rect(self.display_surface, (255,0,0), button)
                else:
                    pygame.draw.rect(self.display_surface, (0,0,0), button)
                self.draw_text(b, (255,255,255), x+c, y+15)
                c += 100

            if option == "Catalog":
                interval = 50
                height = 30
                c = 0
                buttons = []
                for type in self.building_types:
                    button = pygame.Rect(x, y+50+((interval+height)*c), 150, height)
                    buttons.append(button)
                    pygame.draw.rect(self.display_surface, (0,0,255), button)
                    self.draw_text("Add "+type, (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{self.wood/20}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1

                mx, my = pygame.mouse.get_pos()
                c = 0
                for b in buttons:
                    if b.collidepoint(mx, my):
                        if click:
                            k = list(self.buildings)[c]
                            self.wood -= 20
                            self.buildings[k] += 1
                    c += 1
            elif option == "Village Info":
                interval = 20
                height = 20
                c = 0
                for type, num in self.buildings.items():
                    self.draw_text(type, (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{num}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1
                for job in job_list:
                    self.draw_text(job["job_title"], (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{job['villagers_assigned']}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1
            elif option == "Assignments":
                interval = 15
                height = 20
                c = 1
                buttons = []
                for job in job_list:
                    if job["job_title"] != "unassigned":
                        button = pygame.Rect(x, y+50+((interval+height)*c), 150, height)
                        buttons.append(button)
                        pygame.draw.rect(self.display_surface, (0,0,255), button)
                        self.draw_text("Add "+job["job_title"], (255,255,255), x+5, y+55+((interval+height)*c))
                        self.draw_text(f"{job['villagers_assigned']}", (255,255,255), x+375, y+55+((interval+height)*c))
                    else:
                        c -= 1
                        self.draw_text(job["job_title"], (255,255,255), x+5, y+55)
                        self.draw_text(f"{job['villagers_assigned']}", (255,255,255), x+375, y+55)
                    c += 1
                for job in job_list:
                    if job["job_title"] != "unassigned":
                        button = pygame.Rect(x, y+50+((interval+height)*c), 150, height)
                        buttons.append(button)
                        pygame.draw.rect(self.display_surface, (0,0,255), button)
                        self.draw_text("Remove "+job["job_title"], (255,255,255), x+5, y+55+((interval+height)*c))
                        c += 1

                mx, my = pygame.mouse.get_pos()
                c = 0
                for b in buttons:
                    if b.collidepoint(mx, my):
                        if click:
                            if c < 6:
                                if job_list[c%7]["job_title"] == "unassigned":
                                    c += 1
                                job_list[c%7]["villagers_assigned"] += 1
                                for job in job_list:
                                    if job["job_title"] == "unassigned":
                                        job["villagers_assigned"] -= 1
                            else:
                                if job_list[(c+1)%7]["job_title"] == "unassigned":
                                    c += 1
                                job_list[(c+1)%7]["villagers_assigned"] -= 1
                                for job in job_list:
                                    if job["job_title"] == "unassigned":
                                        job["villagers_assigned"] += 1
                    c += 1
            else:
                interval = 20
                height = 20
                c = 0
                for type, num in self.eco.items():
                    self.draw_text(type, (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{num}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1

            pygame.display.flip()
            mx, my = pygame.mouse.get_pos()
            c = 0
            for h in header:
                if h.collidepoint(mx, my):
                    if click:
                        option = self.menu_options[c]
                c += 1

            click = False
            click, menu = self.wait_key()
            if menu == False:
                requests.post("http://127.0.0.1:3000/assignments/plan", headers=self.post_headers, data={"list": job_list})

    def cont(self):
        time.sleep(5)

    def draw_tiles(self, terrain_type_map):
        for y, row in enumerate(terrain_type_map):
            for x, value in enumerate(row):

                if x == WORLD_X or y == WORLD_Y:
                    continue

                # get the terrain types of each tile corner
                tile_corner_types = []
                tile_corner_types.append(terrain_type_map[y + 1][x + 1])
                tile_corner_types.append(terrain_type_map[y + 1][x])
                tile_corner_types.append(terrain_type_map[y][x + 1])
                tile_corner_types.append(terrain_type_map[y][x])

                for terrain_type in ALL_TERRAIN_TYPES:
                    if terrain_type in tile_corner_types:
                        tile_index = self.get_tile_index_for_type(tile_corner_types, terrain_type)
                        image = self.terrain_tiles[terrain_type][tile_index]
                        break
                self.display_surface.blit(image, (x * TILESIZE, y * TILESIZE))


    def get_tile_index_for_type(self, tile_corners, terrain_type):
        tile_index = 0
        for power, corner_type in enumerate(tile_corners):
                if corner_type == terrain_type:
                    tile_index += 2 ** power
        return tile_index