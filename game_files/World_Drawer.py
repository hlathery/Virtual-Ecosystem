import pygame
from Util import *
import time
import threading
import requests
import json
from World import *
import math

class WorldDrawer:

    def __init__(self, height_map):
        # open window
        pygame.init()
        self.display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # load tile sheet, and extract the cell images
        self.tilesheet = pygame.image.load(TILESHEET_PATH)
        self.costs = ['30', '35', '40', '25']

        self.height_map = height_map
        self.font = pygame.font.SysFont(None, 20)
        self.get_headers = {"accept": "application/json", "access_token": "hlath"}
        self.post_headers = {"accept": "application/json", "access_token": "hlath", "Content-Type": "application/json"}
        self.menu_options = ["Catalog", "Village Info", "Jobs", "Eco Info"]
        self.ord = []

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
        self.building_tile = self.tilesheet.subsurface((BUILDING_TILE[0], BUILDING_TILE[1], TILESIZE, TILESIZE))

    def run_fastapi():
        import main

    def draw(self):
        self.ord = World.count_biomes(World,self.height_map)
        eco = requests.get("http://127.0.0.1:3000/eco/", headers=self.get_headers).json()
        update = []
        for elem in eco:
            if elem['biome_name'] == 'grassland':
                update.append({
                    'nourishment':100,
                    'entity_type':'predators',
                    'biome_id':elem['biome_id']
                })
                update.append({
                    'nourishment':100,
                    'entity_type':'prey',
                    'biome_id':elem['biome_id']
                })
                update.append({
                    'nourishment':100,
                    'entity_type':'plants',
                    'biome_id':elem['biome_id']
                })
            elif elem['biome_name'] == 'forest':
                update.append({
                    'nourishment':100,
                    'entity_type':'predators',
                    'biome_id':elem['biome_id']
                })
                update.append({
                    'nourishment':100,
                    'entity_type':'prey',
                    'biome_id':elem['biome_id']
                })
                update.append({
                    'nourishment':100,
                    'entity_type':'trees',
                    'biome_id':elem['biome_id']
                })
                update.append({
                    'nourishment':100,
                    'entity_type':'plants',
                    'biome_id':elem['biome_id']
                })
            elif elem['biome_name'] == 'ocean':
                update.append({
                    'nourishment':100,
                    'entity_type':'water',
                    'biome_id':elem['biome_id']
                })

        res = requests.post("http://127.0.0.1:3000/eco/entity", json=update, headers=self.post_headers)

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
                    res = requests.post("http://127.0.0.1:3000/admin/reset", headers=self.post_headers)
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
        build = []
        option = "Catalog"
        job_list = requests.get("http://127.0.0.1:3000/jobs/", headers=self.get_headers).json()
        overview = requests.get("http://127.0.0.1:3000/village/", headers=self.get_headers).json()
        catalog_list = requests.get("http://127.0.0.1:3000/village/catalog", headers=self.get_headers).json()
        eco = requests.get("http://127.0.0.1:3000/eco/", headers=self.get_headers).json()
        resources = requests.get("http://127.0.0.1:3000/village/village_inventory", headers=self.get_headers).json()
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
                    self.draw_text(f"{math.floor(catalog_list['funds']/catalog_list['costs'][i])}", (255,255,255), x+375, y+55+((interval+height)*c))
                    self.draw_text("Cost: " + self.costs[i] + " Wood", (255,255,255), x+5, y+55+((interval+height)*c)+30)
                    c += 1

                mx, my = pygame.mouse.get_pos()
                c = 0
                for b in buttons:
                    if b.collidepoint(mx, my):
                        if click and catalog_list["funds"] >= catalog_list["costs"][c]:
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
                interval = 10
                height = 20
                c = 0
                for i in range(0, len(overview["buildings"])):
                    self.draw_text(overview["buildings"][i], (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{overview['num_buildings'][i]}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1
                for r in resources:
                    self.draw_text(r["resource_name"], (255,255,255), x+5, y+55+((interval+height)*c))
                    self.draw_text(f"{r['quantity']}", (255,255,255), x+375, y+55+((interval+height)*c))
                    c += 1
                self.draw_text("Population", (255,255,255), x+5, y+55+((interval+height)*c))
                self.draw_text(f"{overview['num_villager']}", (255,255,255), x+375, y+55+((interval+height)*c))

            elif option == "Jobs":
                interval = 15
                height = 20
                c = 1
                buttons = []
                for job in job_list:
                    if job["job_name"] != "unassigned":
                        button = pygame.Rect(x, y+50+((interval+height)*c), 150, height)
                        buttons.append(button)
                        pygame.draw.rect(self.display_surface, (0,0,255), button)
                        self.draw_text("Add "+job["job_name"], (255,255,255), x+5, y+55+((interval+height)*c))
                        self.draw_text(f"{job['villagers_assigned']}", (255,255,255), x+375, y+55+((interval+height)*c))
                    else:
                        c -= 1
                        self.draw_text(job["job_name"], (255,255,255), x+5, y+55)
                        self.draw_text(f"{job['villagers_assigned']}", (255,255,255), x+375, y+55)
                    c += 1
                unassigned = 0
                for job in job_list:
                    if job["job_name"] != "unassigned":
                        button = pygame.Rect(x, y+50+((interval+height)*c), 150, height)
                        buttons.append(button)
                        pygame.draw.rect(self.display_surface, (0,0,255), button)
                        self.draw_text("Remove "+job["job_name"], (255,255,255), x+5, y+55+((interval+height)*c))
                        c += 1
                    else:
                        unassigned = job['villagers_assigned']

                mx, my = pygame.mouse.get_pos()
                c = 0
                for b in buttons:
                    if b.collidepoint(mx, my):
                        if click:
                            if c < 5:
                                if unassigned > 0:
                                    job_list[(c+1)%6]["villagers_assigned"] += 1
                                    for job in job_list:
                                        if job["job_name"] == "unassigned":
                                            job["villagers_assigned"] -= 1
                                            unassigned -= 1
                            else:
                                i = (c+1)%5
                                if i == 0:
                                    i = 5
                                if job_list[i]["villagers_assigned"] > 0:
                                    job_list[i]["villagers_assigned"] -= 1
                                    for job in job_list:
                                        if job["job_name"] == "unassigned":
                                            job["villagers_assigned"] += 1
                                            unassigned += 1
                    c += 1
            else:
                interval = 15
                height = 10
                c = 0
                for elem in eco:
                    if elem['entities'] != 'No entities':
                        self.draw_text(elem['biome_name'], (255,255,255), x+5, y+55+((interval+height)*c))
                        self.draw_text(elem['entities'], (255,255,255), x+90, y+55+((interval+height)*c))
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
                res = requests.put("http://127.0.0.1:3000/jobs/assignments", json=job_list, headers=self.post_headers)
                res = requests.post("http://127.0.0.1:3000/village/building", json=build, headers=self.post_headers)
                num = 0
                sum = 0
                for elem in build:
                    num = elem['quantity']
                    for i in range(0,len(catalog_list['buildings'])):
                        if elem['building_name'] == catalog_list['buildings'][i]:
                            sum += num*catalog_list['costs'][i]
                            break
                res = requests.put("http://127.0.0.1:3000/village/storage",
                           json=[{'resource_name':'wood', 'amount':(-1*sum)}],
                           headers=self.post_headers)


    def cont(self):
        eco = requests.get("http://127.0.0.1:3000/eco/", headers=self.get_headers).json()
        jobs = requests.get("http://127.0.0.1:3000/jobs/", headers=self.get_headers).json()

        w, f = [], []
        for elem in self.ord:
            if elem['biome'] == 'ocean' and len(w) < len(elem['order']):
                w = elem['order']
            elif elem['biome'] == 'forest' and len(f) < len(elem['order']):
                f = elem['order']

        forager, lumber, hunter = 0, 0, 0
        for elem in jobs:
            if elem['job_name'] == 'forager':
                forager = elem['villagers_assigned']
            elif elem['job_name'] == 'lumberjack':
                lumber = elem['villagers_assigned']
            elif elem['job_name'] == 'hunter':
                hunter = elem['villagers_assigned']

        w_bool = False
        f_bool = False
        for elem in eco:
            if elem['biome_name'] == 'grassland':
                biome_pred = requests.get(f"http://127.0.0.1:3000/eco/predator/{elem['biome_id']}", headers=self.get_headers).json()
                biome_prey = requests.get(f"http://127.0.0.1:3000/eco/prey/{elem['biome_id']}", headers=self.get_headers).json()
                biome_plants = requests.get(f"http://127.0.0.1:3000/eco/plants/{elem['biome_id']}", headers=self.get_headers).json()
                res = requests.put("http://127.0.0.1:3000/eco/entity/nourishment",
                                json=[{'id':biome_pred['id'], 'nourishment':(-1*hunter*5)+10},
                                {'id':biome_prey['id'], 'nourishment':(-1*hunter*5)+10},
                                {'id':biome_plants['id'], 'nourishment':(-1*forager*5)+10}],
                                headers=self.post_headers)
            elif elem['biome_name'] == 'ocean' and w_bool == False:
                w_bool = True
                biome_water = requests.get(f"http://127.0.0.1:3000/eco/water/{elem['biome_id']}", headers=self.get_headers).json()
                res = requests.put("http://127.0.0.1:3000/eco/entity/nourishment", json=[{'id':biome_water['id'], 'nourishment':(-1*forager*5)+10}], headers=self.post_headers)
                for o in self.ord:
                    if o['biome'] == 'ocean':
                        update = 10+biome_water['nourishment']-forager*10
                        if update >= 100:
                            update = 1
                        else:
                            update = update/100
                        c = round(len(o['order'])*(1-(update)))
                        i = 0
                        if c > 0:
                            for coord in reversed(o['order']):
                                self.height_map[coord[1]][coord[0]] = 3
                                i += 1
                                if i >= c:
                                    break
                        break
            elif elem['biome_name'] == 'forest':
                biome_pred = requests.get(f"http://127.0.0.1:3000/eco/predator/{elem['biome_id']}", headers=self.get_headers).json()
                biome_prey = requests.get(f"http://127.0.0.1:3000/eco/prey/{elem['biome_id']}", headers=self.get_headers).json()
                biome_plants = requests.get(f"http://127.0.0.1:3000/eco/plants/{elem['biome_id']}", headers=self.get_headers).json()
                res = requests.put("http://127.0.0.1:3000/eco/entity/nourishment",
                                json=[{'id':biome_pred['id'], 'nourishment':(-1*hunter*5)+10},
                                {'id':biome_prey['id'], 'nourishment':(-1*hunter*5)+10},
                                {'id':biome_plants['id'], 'nourishment':(-1*forager*5)+10}],
                                headers=self.post_headers)
                if f_bool == False:
                    f_bool = True
                    biome_trees = requests.get(f"http://127.0.0.1:3000/eco/trees/{elem['biome_id']}", headers=self.get_headers).json()
                    res = requests.put("http://127.0.0.1:3000/eco/entity/nourishment", json=[{'id':biome_trees['id'], 'nourishment':(-1*lumber*5)+10}], headers=self.post_headers)
                    for o in self.ord:
                        if o['biome'] == 'forest':
                            update = 10+biome_trees['nourishment']-lumber*10
                            if update >= 100:
                                update = 1
                            else:
                                update = update/100
                            c = round(len(o['order'])*(1-(update)))
                            i = 0
                            if c > 0:
                                for coord in reversed(o['order']):
                                    self.height_map[coord[1]][coord[0]] = 4
                                    i += 1
                                    if i >= c:
                                        break
                            break
        res = requests.delete("http://127.0.0.1:3000/eco/clean/", headers=self.get_headers)
        pop = requests.get("http://127.0.0.1:3000/village/", headers=self.get_headers).json()
        res = requests.put("http://127.0.0.1:3000/village/storage",
                           json=[{'resource_name':'water', 'amount':(-1*pop['num_villager']*5)+(forager*5)},
                                 {'resource_name':'food', 'amount':(-1*pop['num_villager']*5)+(hunter*5)},
                                 {'resource_name':'wood', 'amount':(lumber*20)}],
                           headers=self.post_headers)
        res = requests.post("http://127.0.0.1:3000/village/villager_update", headers=self.post_headers)
        res = requests.delete(f"http://127.0.0.1:3000/village/villager/{round(pop['num_villager']/5)}", headers=self.get_headers)
        buildings = requests.get("http://127.0.0.1:3000/village/", headers=self.get_headers).json()
        for i in range(0,len(buildings['buildings'])):
            if buildings['buildings'][i] == 'Villager Hut':
                result = (buildings['num_buildings'][i]*5)-pop['num_villager']
                if result > 0:
                    res = requests.put(f"http://127.0.0.1:3000/village/villager/{result}", headers=self.post_headers)
                break
        res = requests.post("http://127.0.0.1:3000/eco/disaster", headers=self.post_headers)

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

        buildings = requests.get("http://127.0.0.1:3000/village/", headers=self.get_headers).json()
        buildings = sum(buildings['num_buildings'])
        g = []
        for elem in self.ord:
            if elem['biome'] == "grassland" and g == [] and len(elem['order']) >= buildings:
                g = elem['order']
                break

        for i in range(0,buildings):
            self.display_surface.blit(self.building_tile, (g[i][1] * TILESIZE, g[i][0] * TILESIZE))

    def get_tile_index_for_type(self, tile_corners, terrain_type):
        tile_index = 0
        for power, corner_type in enumerate(tile_corners):
                if corner_type == terrain_type:
                    tile_index += 2 ** power
        return tile_index