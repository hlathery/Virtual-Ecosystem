import pygame
from Util import *
from World import *
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
        self.menu_options = ["Catalog", "Village Info", "Assignments", "Eco Info"]
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
        self.building_tile = self.tilesheet.subsurface((building_coords[0], building_coords[1], TILESIZE, TILESIZE))

    def run_fastapi():
        import main

    def draw(self):
        while True:
            orders = World.count_biomes(self=World, tile_map=self.height_map)
            self.draw_tiles(self.height_map, orders)
            pygame.display.flip()
            self.decisions()
            self.draw_tiles(self.height_map, orders)
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
        build = []
        job_list = requests.get("http://127.0.0.1:3000/assignments/get_job_list", headers=self.get_headers).json()
        overview = requests.get("http://127.0.0.1:3000/village/", headers=self.get_headers).json()
        catalog_list = requests.get("http://127.0.0.1:3000/village/catalog", headers=self.get_headers).json()
        eco_overview = requests.get("http://127.0.0.1:3000/eco/", headers=self.get_headers).json()
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
                for i in range(0, len(catalog_list["buildings"])):
                    button = pygame.Rect(x, y+50+((interval+height)*c), 150, height)
                    buttons.append(button)
                    pygame.draw.rect(self.display_surface, (0,0,255), button)
                    self.draw_text("Add "+catalog_list['buildings'][i], (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{round(catalog_list['funds']/catalog_list['costs'][i])}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1

                mx, my = pygame.mouse.get_pos()
                c = 0
                for b in buttons:
                    if b.collidepoint(mx, my):
                        if click:
                            if catalog_list["funds"] >= catalog_list["costs"][c]:
                                catalog_list["funds"] -= catalog_list["costs"][c]
                                if {"quantity": 1, "building_name": catalog_list["buildings"][c]} not in build:
                                    build.append({
                                        "quantity": 1,
                                        "building_name": catalog_list["buildings"][c]
                                    })
                                else:
                                    for elem in build:
                                        if elem["building_name"] == catalog_list["buildings"][c]:
                                            elem["quantity"] += 1
                    c += 1
            elif option == "Village Info":
                interval = 20
                height = 20
                c = 0
                for i in range(0, len(overview["buildings"])):
                    self.draw_text(overview["buildings"][i], (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{overview['num_buildings'][i]}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1
                for job in job_list:
                    self.draw_text(job["job_title"], (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{job['villagers_assigned']}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1
                self.draw_text("Population", (255,255,255), x+5, y+55+((interval+height)*c))
                self.draw_text(f"{overview['num_villager']}", (255,255,255), x+375, y+55+((interval+height)*c))

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
                for b in eco_overview:
                    self.draw_text(b["biome"], (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{b['count']}", (255,255,255), x+375, y+55+((interval+height)*c))
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
                res = requests.put("http://127.0.0.1:3000/assignments/assign_villager", json=job_list, headers=self.post_headers)
                res = requests.post("http://127.0.0.1:3000/village/build_building", json=build, data=catalog_list["funds"], headers=self.post_headers)


    def cont(self):
        time.sleep(5)

    def draw_tiles(self, terrain_type_map, ord):
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

        max = 0
        c = 0
        for i in range(0, len(ord)):
            if len(ord[i].get('Grassland', [])) > max and len(ord[i].get('Grassland', [])) >= sum(overview["num_buildings"]):
                max = len(ord[i].get('Grassland', []))
                c = i
        if max > 0:
            overview = requests.get("http://127.0.0.1:3000/village/", headers=self.get_headers).json()
            for i in range(0, sum(overview["num_buildings"])):
                self.display_surface.blit(self.building_tile, (ord[c]['Grassland'][i][0]*TILESIZE,ord[c]['Grassland'][i][1]*TILESIZE))


    def get_tile_index_for_type(self, tile_corners, terrain_type):
        tile_index = 0
        for power, corner_type in enumerate(tile_corners):
                if corner_type == terrain_type:
                    tile_index += 2 ** power
        return tile_index